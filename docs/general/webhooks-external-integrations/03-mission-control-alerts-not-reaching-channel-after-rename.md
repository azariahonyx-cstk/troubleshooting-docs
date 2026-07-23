---
title: "Mission Control Alerts Stop Reaching Notification Channel After Channel Rename"
slug: "mission-control-alerts-not-reaching-channel-after-rename"
pod: "General"
section: "Webhooks & External Integrations"
order: 3
meta_title: "Mission Control Alerts Not Reaching Notification Channel | Contentstack"
meta_description: "Mission Control alerts can stop reaching a team's notification channel when the channel is renamed on the connected messaging platform, breaking the webhook link. Learn how to reconnect the integration to restore alerts."
status: "draft"
source_case_id: "00099004"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# Mission Control Alerts Stop Reaching Notification Channel After Channel Rename

Mission Control alerts may fail to reach the assigned team's notification channel when the channel has been renamed on the connected messaging platform.

## Root cause

Renaming the notification channel on the messaging platform breaks the existing webhook link that Mission Control uses to deliver alerts, so notifications stop arriving.

## Resolution

1. Reconnect Mission Control's notification integration to the renamed channel in your messaging platform.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
