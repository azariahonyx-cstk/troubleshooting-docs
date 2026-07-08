---
title: "Entry Locked After Page Reload When Auto-Save Is Enabled"
slug: "entry-locked-after-page-reload-when-auto-save-is-enabled"
pod: "CMS - UI"
section: "Content Editing & UI Workflows"
order: 9
meta_title: "Troubleshooting Content Editing & UI Workflows | Contentstack"
meta_description: "Resolve issues with entry search delays, localization errors, entry locks, workflow deletion restrictions, and stale content after publishing in Contentstack CMS."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - UI Additions (Jun 28 2026)"
migrated_on: "2026-07-08"
---

# Entry Locked After Page Reload When Auto-Save Is Enabled

Reloading an entry page while the draft auto-save feature is active may intermittently leave the entry in a locked state, preventing other users from editing it.

## Root cause

Root cause was not documented in the source case. The behavior appears intermittent and may relate to how the auto-save feature interacts with entry lock management during page reload events.

## Resolution

1. As a workaround, disable the auto-saving feature in your stack settings. Navigate to Settings > Entries and turn off the auto-save option.
2. If an entry is currently locked, wait a few minutes for the lock to expire automatically, or ask the user whose session holds the lock to navigate away from the entry.
3. Retry accessing the entry after the lock clears.

## Verification

After completing these steps, verify that entries remain accessible after a page reload. If the lock persists after disabling auto-save, escalate with the entry UID, content type, and the browser and Contentstack version in use.
