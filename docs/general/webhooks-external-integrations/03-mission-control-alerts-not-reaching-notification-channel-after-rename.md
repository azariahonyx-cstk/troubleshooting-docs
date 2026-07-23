---
title: "Mission Control Alerts Stop Reaching Notification Channel After It Is Renamed"
slug: "mission-control-alerts-not-reaching-notification-channel-after-rename"
pod: "General"
section: "Webhooks & External Integrations"
order: 3
meta_title: "Mission Control Alerts Not Reaching Notification Channel | Contentstack"
meta_description: "Mission Control alerts can stop arriving in a team's notification channel after that channel is renamed on the messaging platform. Learn how to reconnect the integration to restore alerts."
status: "draft"
source_case_id: "00099004"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# Mission Control Alerts Stop Reaching Notification Channel After It Is Renamed

Mission Control alerts may stop reaching a team's assigned notification channel when that channel is renamed on the connected messaging platform.

## Root cause

Renaming the notification channel on the messaging platform breaks the existing webhook link that Mission Control's notification integration relies on to deliver alerts.

## Resolution

1. Reconnect Mission Control's notification integration to the renamed channel.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
