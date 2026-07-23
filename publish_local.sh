#!/usr/bin/env bash
# Run the docs-pipeline "publish" step LOCALLY, for when GitHub Actions'
# push-triggered publish.yml doesn't fire reliably (observed: intermittent
# webhook delivery misses on rapid successive pushes — not a code bug, not
# a billing block, just GitHub Actions being occasionally unreliable here).
#
# Publishes any article still sitting at status: "draft" on main with no
# contentstack_parent_entry_uid yet — i.e., merged but never actually
# published to Contentstack.
#
# Prereqs:
#   export SANDBOX_CS_API_KEY=blt...
#   export SANDBOX_CS_MGMT_TOKEN=cs...
#
# Usage: ./publish_local.sh

set -euo pipefail

: "${SANDBOX_CS_API_KEY:?Set SANDBOX_CS_API_KEY in your shell first}"
: "${SANDBOX_CS_MGMT_TOKEN:?Set SANDBOX_CS_MGMT_TOKEN in your shell first}"

export CS_API_KEY="$SANDBOX_CS_API_KEY"
export CS_MGMT_TOKEN="$SANDBOX_CS_MGMT_TOKEN"
export CS_CONTENT_TYPE="${CS_CONTENT_TYPE:-product_faqs_2026}"
export CS_ENVIRONMENT="${CS_ENVIRONMENT:-staging}"

if [ -n "$(git status --porcelain)" ]; then
  echo "Working tree isn't clean. Commit/stash first." >&2
  exit 1
fi
git checkout main
git pull --ff-only

echo "== Finding unpublished articles (status: draft, no parent_entry_uid) =="
UNPUBLISHED=$(python3 - <<'EOF'
import json
from pathlib import Path
files = []
for mf in Path("docs").rglob("*.manifest.json"):
    m = json.loads(mf.read_text())
    if m.get("status") == "draft" and not m.get("contentstack_parent_entry_uid"):
        files.append(str(mf.with_suffix("").with_suffix(".md")))
print("\n".join(files))
EOF
)

if [ -z "$UNPUBLISHED" ]; then
  echo "Nothing to publish — every article already has a parent_entry_uid."
  exit 0
fi

echo "$UNPUBLISHED"
echo "== Publishing =="
echo "$UNPUBLISHED" | xargs python3 scripts/publish_to_contentstack.py

echo "== Writing back parent_entry_uid + category_heading =="
python3 - <<'EOF'
import json, re
from pathlib import Path
if not Path("publish-report.jsonl").exists():
    print("No publish-report.jsonl — nothing published this run.")
else:
    for line in Path("publish-report.jsonl").read_text().splitlines():
        rec = json.loads(line)
        p = Path(rec["file"])
        text = p.read_text()
        text = re.sub(r'(?m)^contentstack_parent_entry_uid: null$',
                      f'contentstack_parent_entry_uid: "{rec["parent_uid"]}"', text)
        text = re.sub(r'(?m)^contentstack_category_heading: null$',
                      f'contentstack_category_heading: "{rec["category_heading"]}"', text)
        text = re.sub(r'(?m)^status: "(published-in-drive|approved|in-review|draft)"$',
                      'status: "published"', text)
        p.write_text(text)
        m = p.parent / (p.stem + ".manifest.json")
        if m.exists():
            data = json.loads(m.read_text())
            data["contentstack_parent_entry_uid"] = rec["parent_uid"]
            data["contentstack_category_heading"] = rec["category_heading"]
            data["status"] = "published"
            m.write_text(json.dumps(data, indent=2) + "\n")
    print("Done.")
EOF
rm -f publish-report.jsonl

git config user.name "docs-pipeline-bot"
git config user.email "docs-pipeline@users.noreply.github.com"
git add -A
git diff --cached --quiet || git commit -m "chore: write back Contentstack parent entry UID + category (local publish) [skip ci]"
git push

echo "Done."
