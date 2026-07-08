---
title: "Variant Group Settings Cannot Be Modified \u2014 Admin Role Required"
slug: "variant-group-settings-cannot-be-modified-admin-role-required"
pod: "General"
section: "Content Editing & UI Workflows"
order: 1
meta_title: "Troubleshooting Content Editing & UI Workflows | Contentstack"
meta_description: "Solutions for Variant Group permission errors and role-based access restrictions when configuring content variants in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "General (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Variant Group Settings Cannot Be Modified — Admin Role Required

Attempting to add or link a content type in Variant Group settings results in a "Failed to update" error, preventing the Variant Group configuration from being saved.

## Root cause

Modifications to Variant Group settings are restricted to users with the Admin role in Contentstack. Users with non-admin or custom roles do not have the permissions required to make changes to Variant Groups, regardless of their other stack access levels.

## Resolution

1. Confirm the role of the user account attempting to modify the Variant Group by navigating to Settings > Users in the relevant stack and reviewing the assigned role.
2. If the user does not have the Admin role, either temporarily assign the Admin role to allow the Variant Group configuration to be completed, or ask an existing Admin user to make the required changes.
3. After completing the Variant Group configuration, reassign the user back to the appropriate custom role if needed.

## Verification

After completing these steps, confirm that the content type has been successfully linked or added in the Variant Group settings and that the configuration saves without errors. Escalate with the stack UID, the user's current role, and a description of the attempted Variant Group changes if the error persists after switching to an Admin account.
