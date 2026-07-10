#!/usr/bin/env python3
"""Publish changed articles to Contentstack via the Management API.

Runs in GitHub Actions on merge to main. Each pod has ONE shared Contentstack
entry (its "<Pod> Troubleshooting Guides" FAQ page — see
pipeline/pod_entry_map.json for the UIDs). Articles are NOT their own entries.
For each changed .md under docs/:
  - parse frontmatter + body
  - look up the article's pod -> that pod's shared parent entry UID
  - fetch the parent entry's current faqs_section
  - find a category group whose heading matches this article's section;
    append the FAQ into it, or create a new category group if none matches
  - write the updated faqs_section back to the parent entry, publish it
  - write the returned parent UID + category heading back into the
    frontmatter + manifest (handled by the workflow step, not this script)

Environment variables (set as GitHub Actions repo secrets/vars):
  CS_API_KEY        stack API key
  CS_MGMT_TOKEN     management token with entry read/update/publish scope
  CS_REGION_HOST    e.g. api.contentstack.io (default) or eu-api.contentstack.com
  CS_CONTENT_TYPE   FAQ content type UID (default: product_faqs_2026)
  CS_ENVIRONMENT    target environment (default: staging — the only environment
                     that exists on the docs sandbox stack)
  DRY_RUN           "1" = log payloads, make no real API calls (GET is stubbed
                     with an empty faqs_section, so dry-run can't reflect real
                     existing categories — good enough to sanity-check the
                     find-or-create logic runs, not to preview real output)

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

POD_ENTRY_MAP = json.loads((ROOT / "pipeline" / "pod_entry_map.json").read_text())


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
        if method == "GET":
            return {"entry": {"uid": "dry-run-uid", "faqs_section": []}}
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


def to_site_format(body):
    """Repo format -> docs site format (per the docs editorial standard):
    drop the H1 title (the question field already carries it), remove the
    '## Verification' heading but keep its sentence untitled after the last
    step, and demote '## See also' to an inline lead-in. Only 'Root cause'
    and 'Resolution' remain as titled sections.
    """
    body = re.sub(r"(?m)^# .+\n", "", body, count=1)
    body = re.sub(r"(?m)^## Verification\s*\n", "", body)
    body = re.sub(r"(?m)^## See also\s*\n", "**See also:** ", body)
    return body.strip()


def build_faq_item(fm, body):
    """Map one article's frontmatter + body to a single FAQ (question/answer)
    item — NOT a whole entry. This gets appended into a category group inside
    the pod's shared parent entry, never created as its own entry."""
    return {
        "question": fm["title"],
        "answer": md_to_json_rte(to_site_format(body)),
    }


def find_or_append_category(faqs_section, category_heading, faq_item):
    """Mutate faqs_section in place: append faq_item into the category group
    whose heading matches (case-insensitive, whitespace-trimmed), or create a
    new category group if none matches. Returns True if a new category was
    created, False if it appended into an existing one."""
    target = category_heading.strip().lower()
    for group in faqs_section:
        if group.get("heading", "").strip().lower() == target:
            group.setdefault("faqs", []).append(faq_item)
            return False
    faqs_section.append({"heading": category_heading, "faqs": [faq_item]})
    return True


def main(changed_files):
    failures = 0
    for f in changed_files:
        path = ROOT / f
        if not path.exists() or path.suffix != ".md":
            continue
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        pod = fm.get("pod", "")
        parent_uid = POD_ENTRY_MAP.get(pod)
        if not parent_uid:
            failures += 1
            print(f"::error file={f}::pod {pod!r} has no entry in pipeline/pod_entry_map.json — "
                  f"not auto-creating one, add it via scripts/seed_pod_entries.py first")
            continue
        category = fm.get("section") or "Unspecified"
        try:
            current = api("GET", f"/v3/content_types/{CONTENT_TYPE}/entries/{parent_uid}")
            faqs_section = current["entry"].get("faqs_section") or []
            faq_item = build_faq_item(fm, body)
            created_category = find_or_append_category(faqs_section, category, faq_item)
            api(
                "PUT",
                f"/v3/content_types/{CONTENT_TYPE}/entries/{parent_uid}",
                {"entry": {"faqs_section": faqs_section}},
            )
            api(
                "POST",
                f"/v3/content_types/{CONTENT_TYPE}/entries/{parent_uid}/publish",
                {"entry": {"environments": [ENVIRONMENT], "locales": ["en-us"]}},
            )
            action = "new category" if created_category else "existing category"
            print(f"OK {f} -> pod {pod!r} entry {parent_uid}, {action} {category!r}, published to {ENVIRONMENT}")
            if not DRY_RUN:
                with open(ROOT / "publish-report.jsonl", "a") as out:
                    out.write(json.dumps({
                        "file": f,
                        "parent_uid": parent_uid,
                        "category_heading": category,
                    }) + "\n")
        except Exception as e:
            failures += 1
            print(f"::error file={f}::publish failed: {e}")
    return 1 if failures else 0


if __name__ == "__main__":
    files = sys.argv[1:] or [
        str(p.relative_to(ROOT)) for p in (ROOT / "docs").rglob("*.md")
    ]
    sys.exit(main(files))
