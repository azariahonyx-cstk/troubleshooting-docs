---
title: "Entry Search Results Delayed After Bulk Migration Import"
slug: "entry-search-results-delayed-after-bulk-migration-import"
pod: "CMS - UI"
section: "Content Editing & UI Workflows"
order: 7
meta_title: "Troubleshooting Content Editing & UI Workflows | Contentstack"
meta_description: "Resolve issues with entry search delays, localization errors, entry locks, workflow deletion restrictions, and stale content after publishing in Contentstack CMS."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - UI Additions (Jun 28 2026)"
migrated_on: "2026-07-08"
---

# Entry Search Results Delayed After Bulk Migration Import

Bulk-creating entries through a migration script may cause newly added entries to be absent from the Contentstack search and listing UI for several hours after creation.

## Root cause

When a large number of entries are created within a short period, the search indexing service experiences synchronization delays due to the high load. Entries exist in the database but may not immediately appear in the UI search or listing views.

## Resolution

1. Throttle your entry creation script by reducing the number of simultaneous API requests.
2. Create entries in smaller batches (for example, 50-100 entries at a time) rather than all at once.
3. Introduce short delays (for example, 1-2 seconds) between batch requests to allow the indexing service to keep pace.
4. If entries are already created and missing from search, allow several hours for indexing to complete — no manual intervention is required.

## Verification

After completing these steps, verify that newly created entries appear in the Contentstack search and listing UI. If entries remain missing after several hours, escalate with the stack UID, an approximate timestamp of the entry creation, and a count of entries not appearing in search results.
