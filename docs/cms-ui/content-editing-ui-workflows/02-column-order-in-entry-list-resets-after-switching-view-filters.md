---
title: "Column Order in Entry List Resets After Switching View Filters"
slug: "column-order-in-entry-list-resets-after-switching-view-filters"
pod: "CMS - UI"
section: "Content Editing & UI Workflows"
order: 2
meta_title: "Troubleshooting Content Editing & UI Workflows | Contentstack"
meta_description: "Solutions for common Contentstack UI issues including audit log access limitations, entry list column order persistence, slow entry loading, content model versioning, asset limits, and custom role assignment."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - UI (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Column Order in Entry List Resets After Switching View Filters

Configuring a custom column order in the entry list view may not persist correctly, with columns reverting to their default order when filters are applied or the view type is changed.

## Root cause

Root cause was not documented in the source case. The resolution below addresses the reported symptom.

## Resolution

1. On the top-left of the entry list, select the Views type and set it to All Entries.
2. Adjust the column order to the desired configuration.
3. Switch from the Views tab to the Filters tab using the top-left toggle.
4. Apply any required filters (such as selecting specific content types).
5. Verify that the column order is now maintained after the filter is applied.

## Verification

After completing these steps, confirm that the column order persists when toggling between view types and applying filters. If column order continues to reset unexpectedly, escalate with the content type name, browser version, and a screen recording of the behavior.
