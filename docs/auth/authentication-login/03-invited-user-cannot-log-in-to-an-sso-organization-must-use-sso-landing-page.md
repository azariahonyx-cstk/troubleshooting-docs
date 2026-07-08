---
title: "Invited User Cannot Log In to an SSO Organization \u2014 Must Use SSO Landing Page"
slug: "invited-user-cannot-log-in-to-an-sso-organization-must-use-sso-landing-page"
pod: "AUTH"
section: "Authentication & Login"
order: 3
meta_title: "Troubleshooting Authentication & Login | Contentstack"
meta_description: "Solutions for SSO login failures, invitation acceptance issues, organization ownership transfers, account state problems, and Management Token identification in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "AUTH (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Invited User Cannot Log In to an SSO Organization — Must Use SSO Landing Page

After accepting a stack invitation and creating an account using the email and password provided in the invitation email, a user may be unable to log in to a Contentstack organization that uses SSO.

## Root cause

Organizations configured to use SSO require users to authenticate exclusively through the organization's SSO landing page. Attempting to log in via the standard email/password flow does not work for SSO-enabled organizations. Additionally, the SSO username may differ from the email address used to receive the invitation, which can create further confusion about the correct authentication method.

## Resolution

1. Obtain the SSO landing page URL for your organization from your Org Admin. This is typically provided as a dedicated login link specific to your organization.
2. Navigate to the SSO landing page URL directly in the browser rather than using the standard Contentstack login page.
3. Log in using your SSO credentials — these may differ from the email address used to receive the original invitation.
4. If the original invitation link is no longer usable, ask your Org Admin to provide the SSO landing page URL directly.

## Verification

After completing these steps, confirm that login via the SSO landing page succeeds and that access to the invited stack is available. Escalate with the organization UID, the SSO provider name, and any browser errors or redirect issues if login continues to fail.
