---
title: "Cannot Receive 2FA SMS Code \u2013 Maximum Verification Attempts Reached"
slug: "cannot-receive-2fa-sms-code-maximum-verification-attempts-reached"
pod: "CMS - UI"
section: "Authentication & Login"
order: 1
meta_title: "Troubleshooting Authentication & Login Issues in CMS UI | Contentstack"
meta_description: "Fix 2FA SMS lockout issues in Contentstack. Learn how to restore MFA access when verification codes stop arriving."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - UI Additions (Jun 28 2026)"
migrated_on: "2026-07-08"
---

# Cannot Receive 2FA SMS Code – Maximum Verification Attempts Reached

Attempting to log in with two-factor authentication (2FA) via SMS fails because no verification code is delivered, even after multiple requests. The system has temporarily blocked further SMS codes for the account.

## Root cause

Contentstack enforces a maximum number of SMS verification attempts per account within a time window. Once this limit is reached, the system temporarily blocks additional SMS codes from being sent, making it impossible to complete SMS-based 2FA login until the restriction is lifted.

## Resolution

1. Contact your Organization Owner and request that they temporarily disable multi-factor authentication (MFA) for the affected user account.
2. The Organization Owner can manage MFA settings from Settings > Organization > Security > Multi-factor Authentication.
3. Once MFA is disabled for the account, log in without 2FA to restore access.
4. After regaining access, re-enable and reconfigure MFA from the account's security settings.

## Verification

After completing these steps, verify that login succeeds without requiring an SMS code. If the Organization Owner is also unable to access MFA settings or cannot be reached, escalate to Contentstack Support with the affected user's email address and organization UID.
