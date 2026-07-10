---
title: "\"project_id should not be empty\" Error When Reauthorizing Contentstack Connection in Automate"
slug: "project-id-should-not-be-empty-error-reauthorizing-contentstack-connection-autom"
pod: "AgentOS - Automate"
section: "Authentication & Login"
order: 1
meta_title: "\"project_id should not be empty\" Error When Reauthorizing Contentstack Connection in Automate | Contentstack"
meta_description: "Reauthorizing an existing Contentstack connected app in Automate (Agent OS) can trigger a \"project_id should not be empty\" HTTP 400 error. Learn the workaround: create a new connection instead of reauthorizing."
status: "draft"
source_case_id: "00059958"
contentstack_entry_uid: null
migrated_from: null
migrated_on: null
---

# "project_id should not be empty" Error When Reauthorizing Contentstack Connection in Automate

Reauthorizing an existing Contentstack connected app in Automate (Agent OS) may return a "project_id should not be empty" HTTP 400 Bad Request error. This prevents creating new automations that use the Contentstack connector with workflow access.

## Root cause

Based on a reproduction video provided by the customer, the error occurs specifically during the reauthorization flow of an existing connected Contentstack app in Automate.

## Resolution

1. Do not reauthorize the existing Contentstack connected app.
2. Create a new Contentstack connection instead, either from Settings → Connected Apps or by selecting "Add new account" within the automation step.
3. Grant the required permissions during the initial authorization of the new connection.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
