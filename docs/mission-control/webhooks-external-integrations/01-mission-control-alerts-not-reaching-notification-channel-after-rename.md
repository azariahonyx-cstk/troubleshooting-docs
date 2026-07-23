---
title: "Mission Control Alerts Stop Reaching Notification Channel After Renaming It"
slug: "mission-control-alerts-not-reaching-notification-channel-after-rename"
pod: "Mission Control"
section: "Webhooks & External Integrations"
order: 1
meta_title: "Mission Control Alerts Not Reaching Notification Channel After Rename | Contentstack"
meta_description: "Mission Control deployment alerts can stop arriving in a team's notification channel after the channel is renamed on the connected messaging platform, breaking the webhook link."
status: "published"
source_case_id: "00099004"
contentstack_parent_entry_uid: "blt7a1952301fed723e"
contentstack_category_heading: "Webhooks & External Integrations"
migrated_from: null
migrated_on: null
---

# Mission Control Alerts Stop Reaching Notification Channel After Renaming It

Mission Control deployment alerts may stop reaching the assigned team's notification channel after that channel is renamed on the connected messaging platform.

## Root cause

The notification channel was renamed on the connected messaging platform, which broke the existing webhook link between Mission Control and that channel, preventing alerts from being delivered.

## Resolution

1. Reconnect Mission Control's notification integration to the renamed channel.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
