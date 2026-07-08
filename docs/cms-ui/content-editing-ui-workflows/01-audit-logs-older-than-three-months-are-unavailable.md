---
title: "Audit Logs Older Than Three Months Are Unavailable"
slug: "audit-logs-older-than-three-months-are-unavailable"
pod: "CMS - UI"
section: "Content Editing & UI Workflows"
order: 1
meta_title: "Troubleshooting Content Editing & UI Workflows | Contentstack"
meta_description: "Solutions for common Contentstack UI issues including audit log access limitations, entry list column order persistence, slow entry loading, content model versioning, asset limits, and custom role assignment."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - UI (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Audit Logs Older Than Three Months Are Unavailable

Requesting Organization Audit Logs or User Activity Logs for a date range that extends beyond approximately three months in the past will result in those records being unavailable.

## Root cause

Contentstack retains audit log data for approximately three months only. Logs older than this retention window are automatically purged from the platform and cannot be recovered or re-exported retroactively.

## Resolution

1. Before requesting historical audit logs, confirm the date range falls within the last three months.
2. If audit logs for a period older than three months are required, note that these records cannot be retrieved — no workaround exists once data has been purged.
3. To ensure ongoing access to historical activity data, implement a regular audit log export process using the Contentstack Management API before records fall outside the retention window.
4. For compliance or audit requirements that necessitate longer retention, store exported logs in an external system such as a data warehouse or log management service.

## Verification

After completing these steps, verify the date range of the requested logs falls within the retention window. If logs within the three-month period are still not accessible, escalate with the specific date range, the organization UID, and the stack UID.
