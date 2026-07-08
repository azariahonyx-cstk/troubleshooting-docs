---
title: "Restricting Entry Deletion to Specific Workflow Stages"
slug: "restricting-entry-deletion-to-specific-workflow-stages"
pod: "CMS - UI"
section: "Content Editing & UI Workflows"
order: 10
meta_title: "Troubleshooting Content Editing & UI Workflows | Contentstack"
meta_description: "Resolve issues with entry search delays, localization errors, entry locks, workflow deletion restrictions, and stale content after publishing in Contentstack CMS."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - UI Additions (Jun 28 2026)"
migrated_on: "2026-07-08"
---

# Restricting Entry Deletion to Specific Workflow Stages

Role-based permissions in Contentstack do not natively support conditional entry deletion rules tied to workflow stages. Users with delete permissions can bypass workflow-stage restrictions by moving entries back to a deletable stage before deleting them.

## Root cause

Contentstack ACL (Access Control List) role configurations apply delete permissions globally across all workflow stages. Native conditional deletion rules tied to specific workflow stages are not currently available, creating a gap when organizations require a 4-Eyes Principle for deletion governance.

## Resolution

1. Create a dedicated workflow stage named Request for Deletion to serve as a gate before entries can be permanently removed.
2. Create a specialized role (for example, Deletion_Privileged_Role) with delete permissions for the relevant content types.
3. Using ACL configurations, remove delete permissions from all other standard roles (including editors and publishers).
4. Require users who need to delete an entry to move it to the Request for Deletion workflow stage using a standard workflow transition.
5. Assign only members of Deletion_Privileged_Role as reviewers for that stage so they are notified and can review before executing the deletion.

## Verification

After completing these steps, verify that non-privileged roles cannot delete entries directly and must use the workflow stage route instead. Escalate with your current ACL and workflow configuration if delete permissions continue to bypass the restriction.
