---
title: "Automate Connector Repeatedly Prompts for Re-authentication"
slug: "automate-connector-repeatedly-prompts-reauthentication-session-expiry"
pod: "AgentOS - Automate"
section: "Authentication & Login"
order: 2
meta_title: "Automate Connector Repeatedly Prompts for Re-authentication | Contentstack"
meta_description: "The Automate connector may repeatedly prompt for re-authentication due to a short session expiry policy on the connected login. Learn how switching to a dedicated service account resolves it."
status: "published"
source_case_id: "00090001"
contentstack_parent_entry_uid: "bltf28cead7084dceac"
contentstack_category_heading: "Authentication & Login"
migrated_from: null
migrated_on: null
---

# Automate Connector Repeatedly Prompts for Re-authentication

Automate connector repeatedly prompts for re-authentication every few hours when connected using a personal Contentstack login, interrupting scheduled automations.

## Root cause

The connected app was authorized using a personal Contentstack login that was subject to a short session expiry set by internal IT policy. Because the session expired frequently, the Automate connector was forced to prompt for re-authentication repeatedly, breaking scheduled automation runs.

## Resolution

1. Create a dedicated service-account login with standard session settings instead of using a personal login.
2. Reconnect the Automate app using the new service-account login.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
