---
title: "Partner Academy Login Fails Despite an Active Partner Portal Account"
slug: "partner-academy-login-fails-despite-an-active-partner-portal-account"
pod: "General"
section: "Authentication & Login"
order: 1
meta_title: "Troubleshooting Authentication & Login | Contentstack"
meta_description: "Solutions for Partner Academy access failures, Support Portal connectivity issues on VPN networks, and forced logout incidents in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "General (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Partner Academy Login Fails Despite an Active Partner Portal Account

Attempting to log in to the Contentstack Partner Academy using email/password credentials, cloud provider login (AWS or Azure), or SSO consistently fails even though the user is already successfully logged in to the Partner Portal dashboard.

## Root cause

The Contentstack Partner Academy requires a separate registration process that is independent of the Partner Portal login. Having an active Partner Portal account does not automatically grant access to the Partner Academy — users must complete a distinct Partner Academy registration before they can authenticate.

## Resolution

1. Navigate to the Contentstack Partner Academy registration page and complete the separate registration process using your details.
2. After registering, attempt to log in to the Partner Academy using the credentials established during the academy registration.
3. If password reset emails are not being received during registration or account recovery, check your spam or junk folder and verify that the email address on file is correct.
4. If standard troubleshooting steps — such as using an incognito or private browsing window, clearing browser cache and cookies, and testing in alternative browsers — do not resolve login failures after completing the registration, contact Contentstack Support for assistance with account provisioning.

## Verification

After completing these steps, confirm that access to the Partner Academy is established and that required training content is accessible. Escalate with your Partner Portal email address, the login method attempted, and any specific error messages received if access cannot be established after completing the Partner Academy registration.
