---
title: "Application Interface Stuck on Loading Spinner After Successful Login"
slug: "application-interface-stuck-on-loading-spinner-after-successful-login"
pod: "AUTH"
section: "Authentication & Login"
order: 6
meta_title: "Troubleshooting Authentication & Login Issues | Contentstack"
meta_description: "Resolve loading spinner failures and forced logout 502 errors in Contentstack AUTH."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "AUTH Additions (Jun 28 2026)"
migrated_on: "2026-07-08"
---

# Application Interface Stuck on Loading Spinner After Successful Login

After authenticating successfully, the Contentstack application UI fails to load and remains on an indefinite loading spinner, preventing access to any CMS modules or content.

## Root cause

Root cause was not documented in the source case. The behavior may occur when a user's account record within the organization becomes corrupted or enters an inconsistent state, preventing the post-authentication application initialization from completing.

## Resolution

1. Ask the Org Admin or Org Owner to navigate to Settings > Organization > Users.
2. Remove the affected user from the organization.
3. Re-add the user by sending a fresh invitation to the same email address.
4. Have the user accept the invitation and attempt to log in again.

## Verification

After completing these steps, the application dashboard and modules should load successfully after login. Escalate with the affected user's email address, organization UID, browser name and version, and a description of how long the issue has persisted if the loading spinner continues after re-invitation.
