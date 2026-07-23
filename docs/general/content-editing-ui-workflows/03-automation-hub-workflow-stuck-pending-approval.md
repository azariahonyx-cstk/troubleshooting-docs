---
title: "Automation Hub Workflow Stuck in \"Pending Approval\" Status"
slug: "automation-hub-workflow-stuck-pending-approval"
pod: "General"
section: "Content Editing & UI Workflows"
order: 3
meta_title: "Automation Hub Workflow Stuck in Pending Approval | Contentstack"
meta_description: "An Automation Hub workflow can remain in Pending Approval indefinitely when its approval step references a renamed user role. Learn how to update the role reference to restore approval routing."
status: "published"
source_case_id: "00099002"
contentstack_parent_entry_uid: "blt126bd9f8c6e8e9bb"
contentstack_category_heading: "Content Editing & UI Workflows"
migrated_from: null
migrated_on: null
---

# Automation Hub Workflow Stuck in "Pending Approval" Status

Automation Hub workflows may remain in "Pending Approval" status indefinitely, with no approver ever notified.

## Root cause

The workflow's approval step referenced a user role that had since been renamed. Because the referenced role no longer existed under that name, the approval notification had no valid recipient to route to, leaving the workflow stuck in the "Pending Approval" state.

## Resolution

1. Update the workflow's approval step to reference the current role name.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
