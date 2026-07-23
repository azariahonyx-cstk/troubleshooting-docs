---
title: "Mission Control Alerts Stop Reaching Notification Channel After Channel Rename"
slug: "mission-control-alerts-not-reaching-channel-after-rename"
pod: "General"
section: "Webhooks & External Integrations"
order: 3
meta_title: "Mission Control Alerts Not Reaching Notification Channel | Contentstack"
meta_description: "Mission Control deployment alerts can stop arriving in a team's notification channel after the channel is renamed on the connected messaging platform, breaking the webhook link. Learn how to reconnect the integration."
status: "draft"
source_case_id: "00099004"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# Mission Control Alerts Stop Reaching Notification Channel After Channel Rename

Mission Control deployment alerts may stop reaching the assigned team's notification channel when that channel has been renamed on the connected messaging platform, breaking the existing webhook link.

## Root cause

The notification channel had been renamed on the messaging platform, which broke the existing webhook link that Mission Control used to deliver alerts.

## Resolution

1. Reconnect Mission Control's notification integration to the renamed channel.

## Verification

After completing these steps, confirm alerts arrive in the renamed channel. If the issue persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
