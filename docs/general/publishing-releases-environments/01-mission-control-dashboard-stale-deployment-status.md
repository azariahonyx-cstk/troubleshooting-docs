---
title: "Mission Control Dashboard Shows Deployment Stuck in \"In Progress\" After It Completed"
slug: "mission-control-dashboard-stale-deployment-status"
pod: "General"
section: "Publishing, Releases & Environments"
order: 1
meta_title: "Mission Control Dashboard Shows Stale Deployment Status | Contentstack"
meta_description: "Learn why the Mission Control dashboard may keep showing a deployment as in progress after it has finished, and how refreshing the page resolves it."
status: "published"
source_case_id: "00090009"
contentstack_parent_entry_uid: "blt126bd9f8c6e8e9bb"
contentstack_category_heading: "Publishing, Releases & Environments"
migrated_from: null
migrated_on: null
---

# Mission Control Dashboard Shows Deployment Stuck in "In Progress" After It Completed

The Mission Control dashboard may continue showing a deployment as "in progress" long after the deployment has actually completed.

## Root cause

When a dashboard browser tab is left idle for an extended period, the underlying status polling that keeps the deployment view up to date can stall. As a result, the dashboard stops receiving updates and continues to display the deployment's last known state instead of its current, completed state.

## Resolution

1. Refresh the Mission Control dashboard page in your browser.

## Verification

After completing these steps, confirm the deployment status updates to reflect its current state (e.g., completed). If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
