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
  CS_CONTENT_TYPE   FAQ content type UID (default: product_faqs_2026)
  CS_ENVIRONMENT    target environment (default: staging — the only environment
                     that exists on the docs sandbox stack)
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
CONTENT_TYPE = os.environ.get("CS_CONTENT_TYPE", "product_faqs_2026")
ENVIRONMENT = os.environ.get("CS_ENVIRONMENT", "staging")
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


INLINE_PATTERN = re.compile(r"\*\*(.+?)\*\*|`(.+?)`|\[(.+?)\]\((.+?)\)|_(.+?)_")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
OL_RE = re.compile(r"^\d+\.\s+(.*)$")
UL_RE = re.compile(r"^[-*]\s+(.*)$")


def _parse_inline(text):
    """Split a line into JSON-RTE text/link children, handling **bold**, `code`, _italic_, [text](url)."""
    children, pos = [], 0
    for m in INLINE_PATTERN.finditer(text):
        if m.start() > pos:
            children.append({"text": text[pos:m.start()]})
        if m.group(1) is not None:
            children.append({"text": m.group(1), "bold": True})
        elif m.group(2) is not None:
            children.append({"text": m.group(2), "inlineCode": True})
        elif m.group(3) is not None:
            children.append({"type": "link", "attrs": {"url": m.group(4)}, "children": [{"text": m.group(3)}]})
        elif m.group(5) is not None:
            children.append({"text": m.group(5), "italic": True})
        pos = m.end()
    if pos < len(text):
        children.append({"text": text[pos:]})
    return children or [{"text": ""}]


def _list_block(lines, i, item_re, list_type):
    items = []
    while i < len(lines) and item_re.match(lines[i].strip()):
        text = item_re.match(lines[i].strip()).group(1)
        items.append({"type": "li", "attrs": {}, "children": [{"type": "p", "attrs": {}, "children": _parse_inline(text)}]})
        i += 1
    return {"type": list_type, "attrs": {}, "children": items}, i


def md_to_json_rte(markdown_text):
    """Minimal stdlib markdown -> Contentstack JSON RTE doc converter.

    Covers what the article format actually uses: headings, paragraphs,
    numbered/bulleted lists, and inline bold/italic/code/links. Not a general
    markdown parser — extend the regexes above if the article format grows.
    """
    lines = markdown_text.strip().splitlines()
    children, i = [], 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue
        h = HEADING_RE.match(stripped)
        if h:
            level = min(len(h.group(1)), 6)
            children.append({"type": f"h{level}", "attrs": {}, "children": _parse_inline(h.group(2))})
            i += 1
            continue
        if OL_RE.match(stripped):
            block, i = _list_block(lines, i, OL_RE, "ol")
            children.append(block)
            continue
        if UL_RE.match(stripped):
            block, i = _list_block(lines, i, UL_RE, "ul")
            children.append(block)
            continue
        para = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not HEADING_RE.match(lines[i].strip()) \
                and not OL_RE.match(lines[i].strip()) and not UL_RE.match(lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        children.append({"type": "p", "attrs": {}, "children": _parse_inline(" ".join(para))})
    return {"type": "doc", "attrs": {}, "children": children or [{"type": "p", "attrs": {}, "children": [{"text": ""}]}]}


def build_entry(fm, body):
    """Map article frontmatter + body to the product_faqs_2026 content type.

    Schema (fetched from the sandbox stack): title (text, mandatory), url
    (text), breadcrumb (reference -> navigation, unused here), faqs_section
    (group, repeatable) > heading (text) + faqs (group, repeatable) >
    question (text) / answer (JSON RTE), seo (global field: title,
    description, image, robots).

    Each article becomes one faqs_section with a single faqs entry: question
    is the article title, answer is the full body converted to JSON RTE.
    """
    return {
        "entry": {
            "title": fm["title"],
            "url": f"/troubleshooting/{fm['slug']}",
            "faqs_section": [
                {
                    "heading": fm.get("section", ""),
                    "faqs": [
                        {
                            "question": fm["title"],
                            "answer": md_to_json_rte(body),
                        }
                    ],
                }
            ],
            "seo": {
                "title": fm.get("meta_title", ""),
                "description": fm.get("meta_description", ""),
            },
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
            # emit uid mapping for the workflow to write back (never in dry-run:
            # a placeholder uid must not be committed into article frontmatter)
            if not DRY_RUN:
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
