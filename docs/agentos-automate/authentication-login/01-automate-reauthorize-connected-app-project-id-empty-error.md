---
title: "Automate Reauthorization Fails with \"project_id should not be empty\" Error"
slug: "automate-reauthorize-connected-app-project-id-empty-error"
pod: "AgentOS - Automate"
section: "Authentication & Login"
order: 1
meta_title: "Automate \"project_id should not be empty\" Error During Reauthorization | Contentstack"
meta_description: "Reauthorizing an existing connected app in Automate can trigger a \"project_id should not be empty\" HTTP 400 error. Learn the workaround of creating a new Contentstack connection instead."
status: "draft"
source_case_id: "00059958"
contentstack_entry_uid: null
migrated_from: null
migrated_on: null
---

# Automate Reauthorization Fails with "project_id should not be empty" Error

Reauthorizing an existing Contentstack connected app in Automate (Agent OS) may fail with a "project_id should not be empty" HTTP 400 Bad Request error, preventing new automations from being created with the Contentstack connector and workflow access.

## Root cause

Root cause was not documented in the source case. The resolution below addresses the reported symptom. Based on the reported case details, the error appears specifically during the reauthorization flow of an existing connected app, rather than during the initial authorization of a new connection.

## Resolution

1. Create a new Contentstack connection instead of reauthorizing the existing one, either from Settings → Connected Apps or by selecting "Add new account" within the automation step.
2. Grant the required permissions during the initial authorization of the new connection.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
