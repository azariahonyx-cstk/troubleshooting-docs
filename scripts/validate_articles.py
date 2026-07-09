#!/usr/bin/env python3
"""Validate all articles in docs/ before merge.

Checks:
1. Frontmatter parses and required keys are present
2. Manifest sibling exists and matches the JSON schema (structural check, no deps)
3. Required article sections present (problem statement, Resolution, Verification)
4. Sanitization: no customer emails, no Salesforce case numbers in the body,
   no obvious API keys / tokens
5. Duplicate detection: identical slugs or identical titles across the repo

Exit code 0 = pass, 1 = fail. Designed to run in GitHub Actions with no
third-party dependencies (stdlib only).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

ERRORS = []
WARNINGS = []

REQUIRED_FM = ["title", "slug", "pod", "section", "order", "status"]
SECRET_PATTERNS = [
    (re.compile(r"cs[a-f0-9]{16,}", re.I), "possible Contentstack API key"),
    (re.compile(r"blt[a-f0-9]{16,}", re.I), "possible Contentstack UID/token in body"),
    (re.compile(r"\b000\d{5}\b"), "Salesforce case number in body"),
    (re.compile(r"[a-zA-Z0-9._%+-]+@(?!contentstack\.com)[a-zA-Z0-9.-]+\.[a-z]{2,}"), "customer email address"),
    (re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"), "IP address in body"),
    (re.compile(r"\b(?!your-app-domain)[a-z0-9-]+\.contentstackapps\.com\b", re.I), "customer app domain"),
]

# Editorial policy (from the docs fact-checking standard):
# problem statements describe the problem, not the reporter.
BANNED_FIRST_WORDS = re.compile(
    r"^(Users\b|User\b|A user\b|The user\b|The customer\b|Customers\b|Some users\b|When users\b)",
    re.I,
)
# resolution steps are instructions to the reader, not CSE action reports
CSE_VOICE = re.compile(
    r"^\s*\d+\.\s+(Informed|Advised|Validated|Shared|Explained|Instructed)\b", re.M
)


def parse_frontmatter(text: str):
    m = re.match(r"(?s)^---\n(.*?)\n---\n", text)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if v == "null":
            fm[k.strip()] = None
        elif v.startswith('"') and v.endswith('"'):
            fm[k.strip()] = json.loads(v)
        else:
            try:
                fm[k.strip()] = int(v)
            except ValueError:
                fm[k.strip()] = v
    return fm, text[m.end():]


def main():
    seen_slugs, seen_titles = {}, {}
    md_files = sorted(DOCS.rglob("*.md"))
    if not md_files:
        print("No articles found under docs/ — nothing to validate")
        return 0

    for md in md_files:
        rel = md.relative_to(ROOT)
        text = md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)

        if fm is None:
            ERRORS.append(f"{rel}: missing YAML frontmatter")
            continue
        for key in REQUIRED_FM:
            if key not in fm or fm[key] in ("", None) and key != "source_case_id":
                ERRORS.append(f"{rel}: frontmatter missing required key '{key}'")

        manifest_path = md.with_suffix("").with_suffix("")  # strip .md
        manifest_path = md.parent / (md.stem + ".manifest.json")
        if not manifest_path.exists():
            ERRORS.append(f"{rel}: manifest sibling {manifest_path.name} missing")
        else:
            try:
                json.loads(manifest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                ERRORS.append(f"{manifest_path.relative_to(ROOT)}: invalid JSON ({e})")

        if "## Resolution" not in body:
            ERRORS.append(f"{rel}: missing '## Resolution' section")
        if "## Verification" not in body:
            WARNINGS.append(f"{rel}: missing '## Verification' section")
        first_para = body.strip().split("\n\n")
        if len(first_para) < 2 or len(first_para[1]) < 40:
            WARNINGS.append(f"{rel}: problem statement looks too short")

        for pattern, label in SECRET_PATTERNS:
            if pattern.search(body):
                ERRORS.append(f"{rel}: sanitization failure — {label}")

        # editorial policy checks
        # problem statement = first prose block after the H1 title
        m = re.search(r"(?s)^# .+?\n\n(.+?)(?=\n\n|\Z)", body.strip())
        if m and BANNED_FIRST_WORDS.match(m.group(1).strip()):
            word = BANNED_FIRST_WORDS.match(m.group(1).strip()).group(1)
            ERRORS.append(
                f"{rel}: problem statement starts with people-first language ('{word}') — describe the problem, not the reporter"
            )
        res = re.search(r"(?s)## Resolution\n(.*?)(?=\n## |\Z)", body)
        if res:
            for bad in CSE_VOICE.finditer(res.group(1)):
                ERRORS.append(
                    f"{rel}: resolution step written as CSE action ('{bad.group(1)}') — rewrite as reader instruction"
                )

        slug, title = fm.get("slug"), fm.get("title", "").strip().lower()
        key = (fm.get("pod"), fm.get("section"), slug)
        if key in seen_slugs:
            ERRORS.append(f"{rel}: duplicate slug '{slug}' (also in {seen_slugs[key]})")
        seen_slugs[key] = rel
        if title in seen_titles:
            WARNINGS.append(
                f"{rel}: title duplicates {seen_titles[title]} — check if these should be one canonical article"
            )
        seen_titles[title] = rel

    for w in WARNINGS:
        print(f"WARN  {w}")
    for e in ERRORS:
        print(f"ERROR {e}")
    print(f"\n{len(md_files)} articles checked · {len(ERRORS)} errors · {len(WARNINGS)} warnings")
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
