---
title: "SSO User Accounts Advance to Accepted State Without Completing a Login"
slug: "sso-user-accounts-advance-to-accepted-state-without-completing-a-login"
pod: "AUTH"
section: "Authentication & Login"
order: 4
meta_title: "Troubleshooting Authentication & Login | Contentstack"
meta_description: "Solutions for SSO login failures, invitation acceptance issues, organization ownership transfers, account state problems, and Management Token identification in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "AUTH (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# SSO User Accounts Advance to Accepted State Without Completing a Login

Several users provisioned through SSO may show an account state of "Accepted" without having completed a full login, leaving their accounts in an incorrect authentication state.

## Root cause

Users who were added to an SSO-enabled organization but then attempted to use the standard password reset flow caused their accounts to advance to the "Accepted" state without completing SSO authentication. SSO-provisioned users should not use the password reset feature, as this triggers account state changes that are incompatible with SSO-only authentication flows.

## Resolution

1. Identify the affected users — look for accounts showing an "Accepted" state that have not logged in through SSO.
2. Remove the affected user accounts from the organization.
3. Re-add the users to the organization through the standard invitation process.
4. Instruct the re-added users to log in exclusively through the organization's SSO landing page, and not to use the "Forgot Password" or password reset features.

## Verification

After completing these steps, confirm that the re-added users can log in successfully via SSO and that their account state reflects an authenticated session. Escalate with the organization UID, the affected user email addresses, and the SSO provider configuration if accounts continue to show unexpected states.
