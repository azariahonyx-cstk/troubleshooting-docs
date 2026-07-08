#!/usr/bin/env python3
"""One-time migration: Google Docs troubleshooting exports -> per-article markdown + manifest.

Input : raw text exports of the POD Google Docs (mains + "Additions" side-docs)
Output: docs/{pod}/{section}/{NN}-{slug}.md  (YAML frontmatter + article body)
        docs/{pod}/{section}/{NN}-{slug}.manifest.json

The "Additions" docs are merged into their POD's section folders, resolving the
append limitation that forced side-doc sprawl in Google Drive.
"""
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

RAW_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/home/claude/raw")
OUT_DIR = Path(__file__).resolve().parents[1] / "docs"
TODAY = date.today().isoformat()

# source file -> (POD name, source doc label)
SOURCES = [
    ("cms-ui.txt", "CMS - UI", "CMS - UI (main, Jun 21 2026)"),
    ("cms-ui-add.txt", "CMS - UI", "CMS - UI Additions (Jun 28 2026)"),
    ("auth.txt", "AUTH", "AUTH (main, Jun 21 2026)"),
    ("auth-add.txt", "AUTH", "AUTH Additions (Jun 28 2026)"),
    ("launch.txt", "Launch", "Launch (main, Jun 21 2026)"),
    ("launch-add.txt", "Launch", "Launch Additions (Jun 28 2026)"),
    ("cda.txt", "CMS - CDA(Rest)", "CMS - CDA(Rest) (main, Jun 21 2026)"),
    ("cda-add.txt", "CMS - CDA(Rest)", "CMS - CDA(Rest) Additions (Jun 28 2026)"),
    ("general.txt", "General", "General (main, Jun 21 2026)"),
    ("general-add.txt", "General", "General Additions (Jun 28 2026)"),
    ("marketplace.txt", "Marketplace - Public Apps", "Marketplace - Public Apps (main, Jun 21 2026)"),
]


def unescape(text: str) -> str:
    """Undo Google Docs markdown-export escaping and normalize line endings."""
    text = text.replace("\ufeff", "").replace("\r\n", "\n")
    # \# \- \. \> \[ \] \_ \--- etc.
    text = re.sub(r"\\([#\-.>\[\]_*&])", r"\1", text)
    return text


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value[:80].rstrip("-")


def parse_doc(text: str):
    """Yield (section, meta_title, meta_description, order, title, body) per article."""
    # split into section blocks on top-level headings
    parts = re.split(r"(?m)^# (?!#)", text)
    for part in parts:
        if not part.strip():
            continue
        lines = part.split("\n")
        section = lines[0].strip()
        section = re.sub(r"\s*\(continued\)\s*$", "", section, flags=re.I)
        block = "\n".join(lines[1:])
        mt = re.search(r"(?m)^Meta Title:\s*(.+)$", block)
        md = re.search(r"(?m)^Meta Description:\s*(.+)$", block)
        meta_title = mt.group(1).strip() if mt else ""
        meta_desc = md.group(1).strip() if md else ""
        for m in re.finditer(
            r"(?ms)^## (\d+)\.\s*(.+?)\n(.*?)(?=^## \d+\.|^# (?!#)|\Z)", block
        ):
            order = int(m.group(1))
            title = m.group(2).strip()
            body = m.group(3)
            yield section, meta_title, meta_desc, order, title, body


def structure_article(body: str):
    """Split article body into problem / root cause / resolution steps / verification / see also."""
    body = re.sub(r"(?m)^---\s*$", "", body).strip()
    see_also = ""
    sa = re.search(r"(?ms)^See Also:\s*(.+?)\Z", body)
    if sa:
        see_also = sa.group(1).strip()
        body = body[: sa.start()].strip()

    rc_split = re.split(r"(?m)^Root Cause\s*$", body, maxsplit=1)
    problem = rc_split[0].strip()
    root_cause, steps, verification = "", "", ""
    if len(rc_split) == 2:
        res_split = re.split(r"(?m)^Resolution\s*$", rc_split[1], maxsplit=1)
        root_cause = res_split[0].strip()
        if len(res_split) == 2:
            rest = res_split[1].strip()
            ver = re.search(r"(?ms)^(After completing these steps.*)\Z", rest)
            if ver:
                verification = ver.group(1).strip()
                steps = rest[: ver.start()].strip()
            else:
                steps = rest
    return problem, root_cause, steps, verification, see_also


def main():
    articles = []
    for filename, pod, source_label in SOURCES:
        path = RAW_DIR / filename
        if not path.exists():
            print(f"WARN missing {path}", file=sys.stderr)
            continue
        text = unescape(path.read_text(encoding="utf-8"))
        for section, meta_title, meta_desc, order, title, body in parse_doc(text):
            problem, root_cause, steps, verification, see_also = structure_article(body)
            articles.append(
                dict(
                    pod=pod, source_label=source_label, section=section,
                    meta_title=meta_title, meta_description=meta_desc,
                    order=order, title=title, problem=problem,
                    root_cause=root_cause, steps=steps,
                    verification=verification, see_also=see_also,
                )
            )

    written = 0
    for a in articles:
        pod_slug = slugify(a["pod"])
        sec_slug = slugify(a["section"])
        art_slug = slugify(a["title"])
        folder = OUT_DIR / pod_slug / sec_slug
        folder.mkdir(parents=True, exist_ok=True)
        base = f"{a['order']:02d}-{art_slug}"

        fm = {
            "title": a["title"],
            "slug": art_slug,
            "pod": a["pod"],
            "section": a["section"],
            "order": a["order"],
            "meta_title": a["meta_title"],
            "meta_description": a["meta_description"],
            "status": "published-in-drive",
            "source_case_id": None,
            "contentstack_entry_uid": None,
            "migrated_from": a["source_label"],
            "migrated_on": TODAY,
        }
        fm_yaml = "\n".join(
            f"{k}: {json.dumps(v) if not isinstance(v, int) and v is not None else ('null' if v is None else v)}"
            for k, v in fm.items()
        )

        md = [f"---\n{fm_yaml}\n---", "", f"# {a['title']}", "", a["problem"], ""]
        if a["root_cause"]:
            md += ["## Root cause", "", a["root_cause"], ""]
        if a["steps"]:
            md += ["## Resolution", "", a["steps"], ""]
        if a["verification"]:
            md += ["## Verification", "", a["verification"], ""]
        if a["see_also"]:
            md += ["## See also", "", a["see_also"], ""]
        (folder / f"{base}.md").write_text("\n".join(md).strip() + "\n", encoding="utf-8")

        manifest = {
            "title": a["title"],
            "slug": art_slug,
            "pod": a["pod"],
            "section": a["section"],
            "order": a["order"],
            "status": "published-in-drive",
            "source_case_id": None,
            "contentstack_entry_uid": None,
            "confidence_score": None,
            "keywords": [],
            "alternate_search_terms": [],
            "related_articles": [],
            "traceability": {
                "migrated_from": a["source_label"],
                "migrated_on": TODAY,
                "pipeline": "gdocs-migration-v1",
            },
        }
        (folder / f"{base}.manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        written += 1

    print(f"Wrote {written} articles across {len({(a['pod'], a['section']) for a in articles})} sections")


if __name__ == "__main__":
    main()
