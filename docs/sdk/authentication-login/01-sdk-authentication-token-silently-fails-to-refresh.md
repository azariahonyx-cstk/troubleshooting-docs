---
title: "SDK Authentication Token Silently Fails to Refresh After Long-Running Sessions"
slug: "sdk-authentication-token-silently-fails-to-refresh"
pod: "SDK"
section: "Authentication & Login"
order: 1
meta_title: "SDK Authentication Token Silently Fails to Refresh | Contentstack"
meta_description: "SDK-based integrations can start returning authentication errors after several hours of continuous use. Learn why this happens and how to configure automatic token refresh."
status: "published"
source_case_id: "00099010"
contentstack_parent_entry_uid: "bltef47181f70dc4e80"
contentstack_category_heading: "Authentication & Login"
migrated_from: null
migrated_on: null
---

# SDK Authentication Token Silently Fails to Refresh After Long-Running Sessions

SDK authentication may fail silently after several hours of continuous use, with no warning before the errors begin.

## Root cause

The SDK client was initialized once at application startup with a short-lived token and never configured to refresh it automatically. Once that token expired, the client had no mechanism to obtain a new one, so requests began failing with authentication errors.

## Resolution

1. Update the SDK initialization to use the auto-refresh token option instead of a static token.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
