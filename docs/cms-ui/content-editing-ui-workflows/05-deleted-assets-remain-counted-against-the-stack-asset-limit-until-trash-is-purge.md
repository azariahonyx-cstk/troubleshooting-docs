---
title: "Deleted Assets Remain Counted Against the Stack Asset Limit Until Trash Is Purged"
slug: "deleted-assets-remain-counted-against-the-stack-asset-limit-until-trash-is-purge"
pod: "CMS - UI"
section: "Content Editing & UI Workflows"
order: 5
meta_title: "Troubleshooting Content Editing & UI Workflows | Contentstack"
meta_description: "Solutions for common Contentstack UI issues including audit log access limitations, entry list column order persistence, slow entry loading, content model versioning, asset limits, and custom role assignment."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - UI (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Deleted Assets Remain Counted Against the Stack Asset Limit Until Trash Is Purged

Reaching the stack asset limit and deleting assets to free up capacity may not reduce the asset count, because deleted assets are retained in the Trash and continue to count toward the limit.

## Root cause

Contentstack moves deleted assets to a Trash folder rather than permanently removing them immediately. Assets in the Trash continue to count toward the stack's asset limit until the Trash is explicitly purged.

## Resolution

1. Review the current asset count for your stack by navigating to the Assets section.
2. Check the Trash within the Assets section to identify the number of assets currently held there.
3. Permanently delete (purge) assets from the Trash to reduce the active asset count and free up capacity toward the limit.
4. If the asset limit has already been reached and a temporary increase is needed to unblock urgent work, contact Contentstack Support with your stack API key and a description of the situation to request a temporary limit increase while the Trash is being cleared.

## Verification

After completing these steps, verify that the asset count has decreased to reflect the purged assets. If the count does not update after purging, or if you need a permanent increase to the asset limit, escalate with your stack UID, the current and required asset limits, and a description of your use case.
