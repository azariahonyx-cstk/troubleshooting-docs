---
title: "SSO Login Button Appears Unresponsive After Accepting an Invitation"
slug: "sso-login-button-appears-unresponsive-after-accepting-an-invitation"
pod: "AUTH"
section: "Authentication & Login"
order: 1
meta_title: "Troubleshooting Authentication & Login | Contentstack"
meta_description: "Solutions for SSO login failures, invitation acceptance issues, organization ownership transfers, account state problems, and Management Token identification in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "AUTH (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# SSO Login Button Appears Unresponsive After Accepting an Invitation

After accepting an invitation to join a Contentstack organization that uses SSO, the login button on the SSO-enabled organization landing page may appear unresponsive and cannot be clicked.

## Root cause

Root cause was not documented in the source case. The resolution below addresses the reported symptom. The behavior may indicate that the user's account is locked within the organization, or that the user has not been provisioned in the Identity Provider for SSO authentication.

## Resolution

1. Verify whether the invited user's account is locked within the organization by checking the user list under Settings > Users in the organization.
2. Confirm that the user has been provisioned in the Identity Provider (IdP) configured for SSO in this organization.
3. If the user is not provisioned in the IdP, add the user to the IdP and retry the login flow.
4. If the user is provisioned but the login button remains unresponsive, collect a HAR file from the browser during the login attempt and capture any network errors from the browser's developer console.

## Verification

After completing these steps, confirm that the user can click the login button and authenticate successfully. Escalate with the organization UID, the user's email address, a description of the observed behavior, and a browser HAR file or network error details if the issue persists.
