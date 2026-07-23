#!/usr/bin/env bash
# Run the docs-pipeline "generate" step LOCALLY instead of in GitHub Actions.
#
# Why: CLAUDE_CODE_OAUTH_TOKEN hits a known Anthropic bug when the claude CLI
# is invoked non-interactively inside a GitHub Actions runner
# (anthropics/claude-code-action#1316 — "Header '14' has invalid value").
# The exact same token + exact same `claude -p ... --output-format json`
# call works fine outside Actions, which is what this script does.
#
# validate.yml and publish.yml stay untouched in GitHub Actions — they never
# call Claude, so they aren't affected by the bug and don't need to move.
#
# Prereqs (one-time):
#   - `claude` CLI installed and logged in to your subscription (already true)
#   - `gh` CLI installed and authenticated: run `gh auth login` if you haven't
#   - Run this from the repo root, on a clean `main`
#
# Usage:
#   export SLACK_BOT_TOKEN=xoxb-...
#   export CLAUDE_CODE_OAUTH_TOKEN=sk-ant-oat01-...
#   ./run_generate_local.sh                # defaults: days_back=7 max=10
#   DAYS_BACK=14 MAX_ARTICLES=5 ./run_generate_local.sh

set -euo pipefail

: "${SLACK_BOT_TOKEN:?Set SLACK_BOT_TOKEN in your shell first}"
: "${CLAUDE_CODE_OAUTH_TOKEN:?Set CLAUDE_CODE_OAUTH_TOKEN in your shell first}"

export SLACK_FEED_CHANNEL="${SLACK_FEED_CHANNEL:-C0BH0HRCNFJ}"
export SLACK_REPORT_CHANNEL="${SLACK_REPORT_CHANNEL:-C0BGA0VF6KW}"
export DAYS_BACK="${DAYS_BACK:-7}"
export MAX_ARTICLES="${MAX_ARTICLES:-10}"

if [ -n "$(git status --porcelain)" ]; then
  echo "Working tree isn't clean. Commit/stash first." >&2
  exit 1
fi
git checkout main
git pull --ff-only

echo "== Smoke-testing claude CLI auth locally =="
claude -p "Reply with exactly: OK" --output-format json --model sonnet >/dev/null
echo "  ok"

echo "== Generating + verifying articles =="
python3 scripts/generate_articles.py

echo "== Validating generated articles =="
CLEAN=1
python3 scripts/validate_articles.py || CLEAN=0

echo "== Deciding outcome =="
python3 - <<'EOF'
import json
r = json.load(open("run-report.json"))
changes = bool(r["drafted"] or r["flagged"])
automerge = not r["flagged"]
open(".decide_env", "w").write(f"CHANGES={1 if changes else 0}\nAUTOMERGE={1 if automerge else 0}\n")
summary = [f"Run {r['run_date']}: {r['new_cases']} new cases · {len(r['drafted'])} approved · "
           f"{len(r['flagged'])} flagged · {len(r['rejected'])} rejected · {len(r['errors'])} errors"]
for a in r["drafted"]:
    summary.append(f"  APPROVED {a['case']} — {a['title']} (accuracy {a['accuracy']}/10)")
for a in r["flagged"]:
    summary.append(f"  FLAGGED {a['case']} — {a['title']} ({a['verdict']})")
for a in r["rejected"]:
    summary.append(f"  rejected {a['case']}: {a['reason']}")
for e in r["errors"]:
    summary.append(f"  error: {e}")
open("run-summary.txt", "w").write("\n".join(summary))
EOF
# shellcheck disable=SC1091
source .decide_env
rm -f .decide_env

PR_URL=""
OPENED=0
if [ "$CHANGES" = "1" ] || [ -f pipeline/processed_cases.json ]; then
  BRANCH="articles/run-$(date -u +%Y-%m-%d-%H%M)"
  git config user.name "docs-pipeline-bot"
  git config user.email "docs-pipeline@users.noreply.github.com"
  git checkout -b "$BRANCH"
  git add docs/ pipeline/
  if git diff --cached --quiet; then
    echo "Nothing to commit."
    git checkout main
    git branch -D "$BRANCH"
  else
    N=$(python3 -c "import json;r=json.load(open('run-report.json'));print(len(r['drafted'])+len(r['flagged']))")
    git commit -m "Articles: run $(date -u +%Y-%m-%d) ($N articles)"
    git push origin "$BRANCH"
    PR_URL=$(gh pr create --base main --head "$BRANCH" \
      --title "Articles: run $(date -u +%Y-%m-%d)" \
      --body-file run-summary.txt)
    OPENED=1
    echo "PR opened: $PR_URL"
  fi
fi

if [ "$OPENED" = "1" ]; then
  echo "== Posting review-needed summary comment (no auto-merge — every article needs manual approval) =="
  python3 - <<'EOF'
import json
r = json.load(open("run-report.json"))
lines = ["## Review needed — every article here requires your manual approval before it merges. No auto-merge.\n"]
if r["drafted"]:
    lines.append("### Verifier-approved")
    for a in r["drafted"]:
        rev = f" (after {a['revisions']} revision{'s' if a['revisions'] != 1 else ''})" if a.get("revisions") else ""
        lines.append(f"- `{a['path']}` — accuracy {a['accuracy']}/10{rev}")
    lines.append("")
if r["flagged"]:
    lines.append("### Flagged — needs your judgment, not just a rubber stamp")
    for a in r["flagged"]:
        lines.append(f"#### `{a['path']}` — verdict: **{a['verdict']}**")
        m = json.load(open(a["path"].replace(".md", ".manifest.json")))
        v = m["verification"]
        for h in v["hallucinations"]:
            lines.append(f"- HALLUCINATION: \"{h['claim']}\" — {h['problem']}")
        for s in v["sensitive_data"]:
            lines.append(f"- SENSITIVE: {s['found']} -> {s['replace_with']}")
        for n in v["revision_notes"]:
            lines.append(f"- fix: {n}")
        lines.append("")
open("pr-comment.md", "w").write("\n".join(lines))
EOF
  gh pr comment "$PR_URL" --body-file pr-comment.md
fi

echo "== Posting run report to Slack =="
PR_URL="$PR_URL" python3 - <<'EOF'
import json, os, urllib.request
try:
    text = open("run-summary.txt").read()
except FileNotFoundError:
    text = "Generate articles run finished with no report (check local script output above)."
pr_url = os.environ.get("PR_URL", "")
if pr_url:
    text += f"\nPR: {pr_url}"
req = urllib.request.Request(
    "https://slack.com/api/chat.postMessage",
    data=json.dumps({"channel": os.environ["SLACK_REPORT_CHANNEL"],
                     "text": f"*Docs pipeline — generate run (local)*\n```{text}```"}).encode(),
    headers={"Authorization": f"Bearer {os.environ['SLACK_BOT_TOKEN']}",
             "Content-Type": "application/json; charset=utf-8"})
urllib.request.urlopen(req, timeout=30)
EOF

echo "Done."
