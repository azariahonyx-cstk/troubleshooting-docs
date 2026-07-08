#!/usr/bin/env python3
"""Publish changed articles to Contentstack via the Management API.

Runs in GitHub Actions on merge to main. For each changed .md under docs/:
  - parse frontmatter + body
  - create the FAQ entry if contentstack_entry_uid is null, else update it
  - publish the entry to the configured environment
  - write the returned entry UID back into the frontmatter + manifest and
    commit that change (handled by the workflow step, not this script)

Environment variables (set as GitHub Actions repo secrets/vars):
  CS_API_KEY        stack API key
  CS_MGMT_TOKEN     management token with entry create/update/publish scope
  CS_REGION_HOST    e.g. api.contentstack.io (default) or eu-api.contentstack.com
  CS_CONTENT_TYPE   FAQ content type UID (default: troubleshooting_faq)
  CS_ENVIRONMENT    target environment (default: production)
  DRY_RUN           "1" = log payloads, make no API calls

Stdlib only — no pip install needed in CI.
"""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

API_KEY = os.environ.get("CS_API_KEY", "")
MGMT_TOKEN = os.environ.get("CS_MGMT_TOKEN", "")
HOST = os.environ.get("CS_REGION_HOST", "api.contentstack.io")
CONTENT_TYPE = os.environ.get("CS_CONTENT_TYPE", "troubleshooting_faq")
ENVIRONMENT = os.environ.get("CS_ENVIRONMENT", "production")
DRY_RUN = os.environ.get("DRY_RUN", "0") == "1"


def parse_frontmatter(text):
    m = re.match(r"(?s)^---\n(.*?)\n---\n", text)
    fm = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        v = v.strip()
        if v == "null":
            fm[k.strip()] = None
        elif v.startswith('"'):
            fm[k.strip()] = json.loads(v)
        else:
            try:
                fm[k.strip()] = int(v)
            except ValueError:
                fm[k.strip()] = v
    return fm, text[m.end():].strip()


def api(method, path, payload=None):
    url = f"https://{HOST}{path}"
    headers = {
        "api_key": API_KEY,
        "authorization": MGMT_TOKEN,
        "Content-Type": "application/json",
    }
    data = json.dumps(payload).encode() if payload is not None else None
    if DRY_RUN:
        print(f"DRY-RUN {method} {url}\n{json.dumps(payload, indent=2)[:800] if payload else ''}")
        return {"entry": {"uid": "dry-run-uid"}}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def build_entry(fm, body):
    """Map article frontmatter + body to the FAQ content type fields.

    Adjust the field UIDs below to match the actual FAQ content type schema
    on the docs stack before first production run.
    """
    return {
        "entry": {
            "title": fm["title"],
            "url": f"/troubleshooting/{fm['slug']}",
            "question": fm["title"],
            "answer": body,
            "pod": fm["pod"],
            "issue_bucket": fm["section"],
            "seo": {
                "meta_title": fm.get("meta_title", ""),
                "meta_description": fm.get("meta_description", ""),
            },
            "tags": [fm["pod"], fm["section"]],
        }
    }


def main(changed_files):
    failures = 0
    for f in changed_files:
        path = ROOT / f
        if not path.exists() or path.suffix != ".md":
            continue
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        payload = build_entry(fm, body)
        uid = fm.get("contentstack_entry_uid")
        try:
            if uid:
                res = api("PUT", f"/v3/content_types/{CONTENT_TYPE}/entries/{uid}", payload)
            else:
                res = api("POST", f"/v3/content_types/{CONTENT_TYPE}/entries", payload)
                uid = res["entry"]["uid"]
                print(f"::notice::created entry {uid} for {f}")
            api(
                "POST",
                f"/v3/content_types/{CONTENT_TYPE}/entries/{uid}/publish",
                {"entry": {"environments": [ENVIRONMENT], "locales": ["en-us"]}},
            )
            print(f"OK {f} -> entry {uid} published to {ENVIRONMENT}")
            # emit uid mapping for the workflow to write back
            with open(ROOT / "publish-report.jsonl", "a") as out:
                out.write(json.dumps({"file": f, "uid": uid}) + "\n")
        except Exception as e:
            failures += 1
            print(f"::error file={f}::publish failed: {e}")
    return 1 if failures else 0


if __name__ == "__main__":
    files = sys.argv[1:] or [
        str(p.relative_to(ROOT)) for p in (ROOT / "docs").rglob("*.md")
    ]
    sys.exit(main(files))
