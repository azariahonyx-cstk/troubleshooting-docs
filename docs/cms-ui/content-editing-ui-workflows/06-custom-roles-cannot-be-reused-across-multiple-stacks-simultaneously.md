---
title: "Custom Roles Cannot Be Reused Across Multiple Stacks Simultaneously"
slug: "custom-roles-cannot-be-reused-across-multiple-stacks-simultaneously"
pod: "CMS - UI"
section: "Content Editing & UI Workflows"
order: 6
meta_title: "Troubleshooting Content Editing & UI Workflows | Contentstack"
meta_description: "Solutions for common Contentstack UI issues including audit log access limitations, entry list column order persistence, slow entry loading, content model versioning, asset limits, and custom role assignment."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - UI (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Custom Roles Cannot Be Reused Across Multiple Stacks Simultaneously

Attempting to assign a custom role across all stacks in an organization in a single operation, or to create an organization-level custom role that applies globally, is not supported.

## Root cause

Custom CMS roles in Contentstack are stack-scoped and cannot be reused or inherited across multiple stacks. The "Select Default Roles" option in Teams only supports default system roles and does not allow bulk assignment of custom roles across selected stacks. There is no organization-level custom role that applies across all stacks at this time.

## Resolution

1. Navigate to the target stack and open its Settings > Roles section.
2. Assign custom roles to the relevant users or teams individually through the Roles Per Stacks section within each stack.
3. Repeat this process for each stack that requires the same custom role assignment.
4. If managing a large number of stacks, consider using the Contentstack Management API to programmatically assign custom roles across stacks.

## Verification

After completing these steps, confirm that the required users have the expected custom role assignment on each target stack. If a cross-stack role assignment mechanism is needed for your organization, consider submitting a product feedback request for enhanced RBAC functionality.
