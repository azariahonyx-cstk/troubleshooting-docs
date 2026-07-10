#!/usr/bin/env python3
"""One-time (per stack) setup: create one product_faqs_2026 entry per pod in
the sandbox, each acting as that pod's shared 'Troubleshooting Guides' page —
mirrors the real production pattern (one entry per product, FAQs nested by
category/instance inside it).

Idempotent: matches by title, skips pods that already have an entry rather
than creating a duplicate. Safe to re-run.

Prints the pod -> entry_uid mapping and writes it to pipeline/pod_entry_map.json.

Env required: SANDBOX_CS_API_KEY, SANDBOX_CS_MGMT_TOKEN
Env optional: CS_REGION_HOST (default api.contentstack.io),
              CS_CONTENT_TYPE (default product_faqs_2026),
              CS_ENVIRONMENT (default staging)

Usage:
  export SANDBOX_CS_API_KEY=blt...
  export SANDBOX_CS_MGMT_TOKEN=cs...
  python3 scripts/seed_pod_entries.py
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

API_KEY = os.environ["SANDBOX_CS_API_KEY"]
MGMT_TOKEN = os.environ["SANDBOX_CS_MGMT_TOKEN"]
HOST = os.environ.get("CS_REGION_HOST", "api.contentstack.io")
CONTENT_TYPE = os.environ.get("CS_CONTENT_TYPE", "product_faqs_2026")
ENVIRONMENT = os.environ.get("CS_ENVIRONMENT", "staging")

# Must match the `pod` enum in prompts/generator.md exactly.
PODS = ["Academy", "AgentOS - Automate", "AUTH", "Automation Hub", "BrandKit",
        "CDP", "CLI", "CMS", "General", "Key Change Requests", "Launch",
        "Marketplace - DevHub", "Marketplace - Public Apps", "Miscellaneous",
        "Mission Control", "Personalize", "SDK", "Security", "TSO",
        "Unspecified", "Variants"]


def slugify(pod):
    return (pod.lower().replace(" - ", "-").replace(" ", "-")
            .replace("(", "").replace(")", ""))


def api(method, path, payload=None):
    url = f"https://{HOST}{path}"
    headers = {"api_key": API_KEY, "authorization": MGMT_TOKEN,
               "Content-Type": "application/json"}
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def find_existing(title):
    query = urllib.parse.quote(json.dumps({"title": title}))
    res = api("GET", f"/v3/content_types/{CONTENT_TYPE}/entries?query={query}")
    entries = res.get("entries", [])
    return entries[0]["uid"] if entries else None


def main():
    mapping = {}
    for pod in PODS:
        title = f"{pod} Troubleshooting Guides"
        existing = find_existing(title)
        if existing:
            print(f"SKIP (already exists): {pod} -> {existing}")
            mapping[pod] = existing
            continue
        payload = {"entry": {
            "title": title,
            "url": f"/{slugify(pod)}-troubleshooting/faqs",
            "faqs_section": [],
            "seo": {
                "title": f"{title} | Contentstack",
                "description": f"Troubleshooting FAQs for {pod}.",
            },
        }}
        res = api("POST", f"/v3/content_types/{CONTENT_TYPE}/entries", payload)
        uid = res["entry"]["uid"]
        api("POST", f"/v3/content_types/{CONTENT_TYPE}/entries/{uid}/publish",
            {"entry": {"environments": [ENVIRONMENT], "locales": ["en-us"]}})
        print(f"CREATED: {pod} -> {uid}")
        mapping[pod] = uid

    out_path = ROOT / "pipeline" / "pod_entry_map.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(mapping, indent=2, sort_keys=True) + "\n")
    print(f"\nWrote {out_path.relative_to(ROOT)}:")
    print(json.dumps(mapping, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
