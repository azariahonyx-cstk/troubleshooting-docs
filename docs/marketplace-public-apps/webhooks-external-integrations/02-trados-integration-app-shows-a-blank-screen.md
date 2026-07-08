---
title: "Trados Integration App Shows a Blank Screen"
slug: "trados-integration-app-shows-a-blank-screen"
pod: "Marketplace - Public Apps"
section: "Webhooks & External Integrations"
order: 2
meta_title: "Troubleshooting Webhooks & External Integrations | Contentstack"
meta_description: "Solutions for Marketplace app delivery failures, authentication errors, and integration issues including XTM translation app and Trados connector problems in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "Marketplace - Public Apps (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Trados Integration App Shows a Blank Screen

Accessing the Trados integration app from within Contentstack may result in a blank screen with no content rendered and no error message displayed.

## Root cause

Root cause was not documented in the source case. The resolution below addresses the reported symptom. Analysis of browser console logs from a reported occurrence identified a 403 (Forbidden) response on one of the API requests made by the app. A 403 response typically indicates an authentication or permissions-related issue rather than an application-level defect, and does not reproduce consistently in all environments.

## Resolution

1. Open the browser developer tools (press F12) and navigate to the Network tab.
2. Refresh the Trados app within Contentstack and observe the network requests as the page loads.
3. Identify any requests returning a 403 (Forbidden) status code and note the affected endpoint URL.
4. Verify that the authentication credentials and API tokens configured for the Trados integration are current and have not expired.
5. Confirm that the user account accessing the Trados app has the required permissions within Contentstack — at minimum, read and write access to the relevant stack and content types.

## Verification

After completing these steps, retry accessing the Trados app to confirm the blank screen no longer occurs. If a 403 error persists after verifying credentials and permissions, escalate with the specific failing request URL, the full error response body, your stack UID, and the Trados app version from your Marketplace installation.
