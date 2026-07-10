#!/usr/bin/env python3
"""Generate troubleshooting articles from resolved Salesforce cases in Slack.

Pipeline per run:
  1. Read case-closed notifications from #feed-salesforce-docs (last N days)
  2. Dedup: skip any Salesforce case ID already present in a manifest or in
     pipeline/processed_cases.json (the repo IS the dedup database)
  3. Generator (Claude): apply rejection taxonomy, draft article JSON
  4. Verifier (Claude, adversarial): fact-check draft against the raw case
  5. Write .md + .manifest.json (with verification block) for drafted articles
  6. Emit run-report.json for the workflow (PR body, auto-merge decision,
     Slack summary)

Env: SLACK_BOT_TOKEN, ANTHROPIC_API_KEY required.
     SLACK_FEED_CHANNEL (default C0B0U9175PS = #feed-salesforce-docs)
     DAYS_BACK (default 7), MAX_ARTICLES per run (default 10)
Stdlib only.
"""
import json
import os
import re
import sys
import time
import unicodedata
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
STATE_FILE = ROOT / "pipeline" / "processed_cases.json"
REPORT_FILE = ROOT / "run-report.json"

SLACK_TOKEN = os.environ["SLACK_BOT_TOKEN"]
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OAUTH_TOKEN = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "")
if not ANTHROPIC_KEY and not OAUTH_TOKEN:
    sys.exit("Need ANTHROPIC_API_KEY or CLAUDE_CODE_OAUTH_TOKEN (from `claude setup-token`)")
FEED_CHANNEL = os.environ.get("SLACK_FEED_CHANNEL", "C0B0U9175PS")
DAYS_BACK = int(os.environ.get("DAYS_BACK", "7"))
MAX_ARTICLES = int(os.environ.get("MAX_ARTICLES", "10"))
MAX_REVISION_ROUNDS = int(os.environ.get("MAX_REVISION_ROUNDS", "2"))
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")
TODAY = date.today().isoformat()

CASE_ID_RE = re.compile(r"\b(000\d{5})\b")
PODS = ["CMS - UI", "CMS - CDA(Rest)", "CMS - CMA", "AUTH", "Launch",
        "General", "Marketplace - Public Apps", "AgentOS - Automate"]


def slack(method, params):
    url = f"https://slack.com/api/{method}"
    data = json.dumps(params).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json; charset=utf-8",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.loads(r.read().decode())
    if not out.get("ok"):
        raise RuntimeError(f"Slack {method} failed: {out.get('error')}")
    return out


def claude(system, user, max_tokens=4000, retries=3):
    """Call Claude via API key if present, else via Claude Code CLI using the
    subscription OAuth token (CLAUDE_CODE_OAUTH_TOKEN from `claude setup-token`)."""
    for attempt in range(retries):
        try:
            if ANTHROPIC_KEY:
                text = _claude_api(system, user, max_tokens)
            else:
                text = _claude_cli(system, user)
            text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.M).strip()
            # tolerate prose around the JSON object
            if not text.startswith("{"):
                m = re.search(r"(?s)\{.*\}", text)
                if m:
                    text = m.group(0)
            return json.loads(text)
        except Exception:  # noqa: BLE001 — retry then surface
            if attempt == retries - 1:
                raise
            time.sleep(5 * (attempt + 1))


def _claude_api(system, user, max_tokens):
    payload = {
        "model": MODEL, "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode(),
        headers={"x-api-key": ANTHROPIC_KEY,
                 "anthropic-version": "2023-06-01",
                 "content-type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        out = json.loads(r.read().decode())
    return "".join(b.get("text", "") for b in out.get("content", []))


def _claude_cli(system, user):
    import subprocess
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    env["CLAUDE_CODE_OAUTH_TOKEN"] = OAUTH_TOKEN
    # single combined prompt via -p arg; avoids flag drift across CLI versions
    prompt = f"{system}\n\n====\n\n{user}"
    proc = subprocess.run(
        ["claude", "-p", prompt, "--output-format", "json",
         "--model", os.environ.get("CLAUDE_CLI_MODEL", "sonnet")],
        capture_output=True, text=True, timeout=300, env=env,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"claude CLI rc={proc.returncode} stderr={proc.stderr[:300]!r} stdout={proc.stdout[:300]!r}"
        )
    out = json.loads(proc.stdout)
    if out.get("is_error"):
        raise RuntimeError(f"claude CLI error result: {str(out)[:300]}")
    return out.get("result", "")


def fetch_cases():
    """Pull messages from the feed channel; one message = one case notification."""
    oldest = time.time() - DAYS_BACK * 86400
    cases, cursor = [], None
    while True:
        params = {"channel": FEED_CHANNEL, "oldest": f"{oldest:.6f}", "limit": 200}
        if cursor:
            params["cursor"] = cursor
        out = slack("conversations.history", params)
        for msg in out.get("messages", []):
            text = msg.get("text", "") or ""
            for att in msg.get("attachments", []) or []:
                text += "\n" + (att.get("text") or att.get("fallback") or "")
            for blk in msg.get("blocks", []) or []:
                if blk.get("type") == "section" and blk.get("text"):
                    text += "\n" + blk["text"].get("text", "")
            m = CASE_ID_RE.search(text)
            if m and len(text) > 80:
                cases.append({"case_id": m.group(1), "raw": text.strip(),
                              "ts": msg.get("ts")})
        cursor = out.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break
    # newest first, dedupe within the run keeping the longest text per case
    best = {}
    for c in cases:
        if c["case_id"] not in best or len(c["raw"]) > len(best[c["case_id"]]["raw"]):
            best[c["case_id"]] = c
    return list(best.values())


def known_case_ids():
    ids = set()
    for mf in DOCS.rglob("*.manifest.json"):
        try:
            cid = json.loads(mf.read_text()).get("source_case_id")
            if cid:
                ids.add(cid)
        except json.JSONDecodeError:
            continue
    if STATE_FILE.exists():
        ids.update(json.loads(STATE_FILE.read_text()).keys())
    return ids


def slugify(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()[:80].rstrip("-")


def next_order(folder):
    orders = [int(m.group(1)) for f in folder.glob("*.md")
              if (m := re.match(r"(\d+)-", f.name))]
    return max(orders, default=0) + 1


def write_article(gen, ver, case, history=None):
    pod = gen["pod"] if gen["pod"] in PODS else "General"
    folder = DOCS / slugify(pod) / slugify(gen["section"])
    folder.mkdir(parents=True, exist_ok=True)
    order = next_order(folder)
    slug = slugify(gen.get("slug") or gen["title"])
    base = f"{order:02d}-{slug}"
    fm = {
        "title": gen["title"], "slug": slug, "pod": pod,
        "section": gen["section"], "order": order,
        "meta_title": gen.get("meta_title", ""),
        "meta_description": gen.get("meta_description", ""),
        "status": "draft", "source_case_id": case["case_id"],
        "contentstack_entry_uid": None,
        "migrated_from": None, "migrated_on": None,
    }
    fm_yaml = "\n".join(
        f"{k}: {json.dumps(v)}" if not isinstance(v, int) or isinstance(v, bool)
        else f"{k}: {v}" for k, v in fm.items()
    ).replace(': null', ': null')
    body = gen["body_markdown"].strip()
    (folder / f"{base}.md").write_text(f"---\n{fm_yaml}\n---\n\n{body}\n")
    manifest = {
        "title": gen["title"], "slug": slug, "pod": pod,
        "section": gen["section"], "order": order, "status": "draft",
        "source_case_id": case["case_id"], "contentstack_entry_uid": None,
        "confidence_score": gen.get("confidence"),
        "keywords": gen.get("keywords", []),
        "alternate_search_terms": gen.get("alternate_search_terms", []),
        "related_articles": [],
        "extracted_facts": gen.get("extracted_facts", {}),
        "verification": {
            "verdict": ver["verdict"],
            "accuracy_score": ver.get("accuracy_score"),
            "hallucinations": ver.get("hallucinations", []),
            "missing_info": ver.get("missing_info", []),
            "sensitive_data": ver.get("sensitive_data", []),
            "revision_notes": ver.get("revision_notes", []),
            "verified_on": TODAY, "verifier_model": MODEL,
            "revisions": max(len(history) - 1, 0) if history else 0,
        },
        "verification_history": history or [],
        "traceability": {"generated_on": TODAY, "pipeline": "generate-v1"},
    }
    (folder / f"{base}.manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return str((folder / f"{base}.md").relative_to(ROOT))


def revise(rev_prompt, case, gen, ver):
    """Ask Claude to surgically correct the draft per the verifier's findings.
    Returns a new gen dict (same metadata, corrected body_markdown)."""
    findings = {
        "hallucinations": ver.get("hallucinations", []),
        "missing_info": ver.get("missing_info", []),
        "sensitive_data": ver.get("sensitive_data", []),
        "revision_notes": ver.get("revision_notes", []),
    }
    user = (
        f"RAW SOURCE CASE:\n\n{case['raw']}\n\n---\n\n"
        f"EXTRACTED FACTS:\n\n{json.dumps(gen.get('extracted_facts', {}), indent=2)}\n\n---\n\n"
        f"CURRENT DRAFT:\n\n{gen['body_markdown']}\n\n---\n\n"
        f"VERIFIER FINDINGS:\n\n{json.dumps(findings, indent=2)}"
    )
    result = claude(rev_prompt, user)
    new_gen = dict(gen)
    new_gen["body_markdown"] = result["body_markdown"]
    new_gen["_revision_summary"] = result.get("revision_summary", "")
    return new_gen


def verify_and_revise(ver_prompt, rev_prompt, case, gen):
    """Verify a draft; if it needs correctable fixes, revise and re-verify,
    up to MAX_REVISION_ROUNDS times. Returns (final_gen, final_ver, history).

    history is a list of per-round verifier verdicts (round 0 = first pass,
    before any revision) for full traceability in the manifest.
    """
    history = []
    current = gen
    ver = None
    for round_num in range(MAX_REVISION_ROUNDS + 1):
        ver = claude(
            ver_prompt,
            f"RAW SOURCE CASE:\n\n{case['raw']}\n\n---\n\n"
            f"DRAFTED ARTICLE:\n\n{current['body_markdown']}",
        )
        history.append({
            "round": round_num,
            "verdict": ver.get("verdict"),
            "publishable": ver.get("publishable"),
            "accuracy_score": ver.get("accuracy_score"),
            "hallucinations": ver.get("hallucinations", []),
            "missing_info": ver.get("missing_info", []),
            "sensitive_data": ver.get("sensitive_data", []),
            "revision_notes": ver.get("revision_notes", []),
            "revision_summary": current.get("_revision_summary", "") if round_num > 0 else None,
        })
        if ver.get("verdict") == "approved":
            break
        # Not fixable by revising the body: source itself fails publishability,
        # or there's nothing to verify against. Stop and let a human look.
        if ver.get("verdict") == "cannot_verify" or ver.get("publishable") is False:
            break
        if round_num == MAX_REVISION_ROUNDS:
            break
        current = revise(rev_prompt, case, current, ver)
    return current, ver, history



def main():
    gen_prompt = (ROOT / "prompts" / "generator.md").read_text()
    ver_prompt = (ROOT / "prompts" / "verifier.md").read_text()
    rev_prompt = (ROOT / "prompts" / "reviser.md").read_text()
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    known = known_case_ids()

    cases = fetch_cases()
    new_cases = [c for c in cases if c["case_id"] not in known]
    report = {"run_date": TODAY, "channel_messages": len(cases),
              "new_cases": len(new_cases), "drafted": [], "rejected": [],
              "flagged": [], "errors": []}

    drafted = 0
    for case in new_cases:
        if drafted >= MAX_ARTICLES:
            report["errors"].append(f"MAX_ARTICLES={MAX_ARTICLES} reached; remaining cases deferred to next run")
            break
        try:
            gen = claude(gen_prompt, f"SOURCE CASE (Slack notification):\n\n{case['raw']}")
            if gen.get("decision") != "draft":
                reason = gen.get("reject_reason", "unspecified")
                state[case["case_id"]] = {"outcome": "rejected", "reason": reason, "on": TODAY}
                report["rejected"].append({"case": case["case_id"], "reason": reason})
                continue
            final_gen, ver, history = verify_and_revise(ver_prompt, rev_prompt, case, gen)
            path = write_article(final_gen, ver, case, history)
            revisions = max(len(history) - 1, 0)
            state[case["case_id"]] = {"outcome": "drafted", "path": path,
                                      "verdict": ver["verdict"], "revisions": revisions, "on": TODAY}
            entry = {"case": case["case_id"], "path": path,
                     "title": final_gen["title"], "verdict": ver["verdict"],
                     "accuracy": ver.get("accuracy_score"), "revisions": revisions}
            (report["drafted"] if ver["verdict"] == "approved" else report["flagged"]).append(entry)
            drafted += 1
        except Exception as e:  # noqa: BLE001 — one bad case must not kill the run
            report["errors"].append(f"{case['case_id']}: {e}")

    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    REPORT_FILE.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    # exit 0 even with flagged articles; the workflow decides merge policy
    return 0


if __name__ == "__main__":
    sys.exit(main())
