---
title: "Administration Troubleshooting Guides"
description: "Discover answers to common troubleshooting questions about Administration."
url: "https://www.contentstack.com/docs/administration-troubleshooting/faqs"
product: "Contentstack"
doc_type: "guide"
audience:
  - developers
  - admins
version: "current"
last_updated: "2026-07-16"
---

# Administration Troubleshooting Guides

## Basic Login, Passwords & Account Lockouts

### Resolving Account Login Failure Due to Lockout

Login attempts fail when an account has been locked, typically following multiple failed password attempts. Access to the platform is not granted and authentication cannot proceed.

**Root Cause**

The account has been locked, preventing any successful authentication attempts.

**Resolution**

1.  Contact the Organization Owner or Admin to unlock the user account via the Organization settings.
2.  Contact Contentstack Support if the Organization Admin is unable to perform the unlock.

After following the instructions in the reactivation email, attempt to log in to verify if access is restored.

### Password Reset Email Failure Due to Expired Organization

Login attempts fail due to an invalid password, and the Forgot Password flow does not send a reset email. Access to the account is not granted because the organization has expired, disabling automated email triggers.

**Root Cause**

The organization associated with the account has reached its expiration date, which prevents the password reset process from functioning and sending emails.

**Resolution**

1.  Obtain access to an active organization.

After obtaining access to an active organization, attempt to log in or trigger a password reset to verify if access is restored.

### Account Activation Failure Due to Non-Identifiable User Account

Invite emails for new accounts fail to deliver or the accounts cannot be activated. This occurs when the user account does not comply with the user-license policy.

**Root Cause**

User licenses must correspond to real, personally identifiable users; generic or shared accounts are not supported and cannot be activated.

**Resolution**

1.  Identify a specific, personally identifiable user.
2.  Send the invitation to the identifiable user's email address.

After inviting an identifiable user, verify if the invitation process completes.

### Resolving NoSuchBucket Error During Platform Loading

NoSuchBucket errors may prevent the platform from loading or hinder login attempts. The application fails to initialize, blocking access to the platform dashboard.

**Root Cause**

Corrupted or outdated authentication data stored in the browser cache prevents the platform from loading correctly.

**Resolution**

1.  Navigate to the browser settings.
2.  Clear the browser cache and cookies.

After clearing the browser data, restart the browser and attempt to log in to verify if the platform loads successfully.

### Login Page Fails to Advance After Password Reset

Attempting to log in to Contentstack may fail when the login page does not proceed, even after a successful password reset and while the user profile remains in an active state.

**Root Cause**

Corrupted or incomplete organization associations prevent the login process from advancing correctly.

**Resolution**

1.  Contact the organization owner or administrator to request removal from the organization.
2.  Request a new invitation to the organization from the administrator.
3.  Accept the new invitation to re-establish the organization association.
4.  Attempt to log in to the Contentstack account.

After rejoining the organization, attempt to log in using account credentials.

If the login page advances and access is granted, the issue is resolved.

## Single Sign-On (SSO) & IdP Configuration

### Resolving SSO Login Requirement After Disabling Strict Mode

A message stating access is allowed only through SSO appears even after Strict Mode has been disabled, blocking login with credentials. This occurs when the system incorrectly mandates SSO access for non-SSO users.

**Root Cause**

A known UI issue prevents the "Allow Access without SSO" checkbox from appearing as expected when adding a user to an organization.

**Resolution**

1.  Navigate to the organization settings to add the user.
2.  Refresh the page while adding the user to make the checkbox visible.
3.  Locate the "Allow Access without SSO" checkbox that appears after the refresh.
4.  Select the "Allow Access without SSO" checkbox.
5.  Save the settings to allow the user to log in without SSO.

After saving the settings, attempt to log in using standard credentials. If the login is successful without an SSO redirect, the issue is resolved.

### Training Organization Missing After SSO Logi

Training organizations fail to appear in the organization dropdown after a successful SSO login.

**Root Cause**

A regional mismatch exists between the location of the training instance and the user's SSO login region, preventing the organization from being displayed.

**Resolution**

1.  Create a training instance in a region that aligns with the SSO login region.
2.  Use new email credentials to set up the instance.

After creating the instance in the correct region and logging in, check the organization list to verify if the training organization is visible.

### Login Failure Due to Missing or Incorrect SSO Details

Login attempts fail when the provided SSO details are missing or incorrect.

**Root Cause**

The login failure occurs because the correct SSO name for the organization has not been provided.

**Resolution**

1.  Contact the organization owner or admin to obtain the correct SSO name.
2.  Select "Log in via Email" to access the account using credentials.

After entering the correct SSO name or selecting the email login option, attempt to log in to verify if access is restored.

### Resolving Unexpected SSO Session Timeouts and Logouts

Unexpected daily logouts occur for SSO users regardless of Identity Provider session settings. Automatic logouts occur once the Contentstack SSO session timeout expires.

**Root Cause**

The SSO session timeout is controlled by Contentstack settings, which default to 12 hours and override the session duration set by the Identity Provider.

**Resolution**

1.  Access the SSO session timeout settings in Contentstack.
2.  Update the SSO session timeout value to a preferred duration between 1 and 24 hours.
3.  Note that each SSO login starts a new session; logging out and back in resets the session timer, but the session duration cannot exceed the configured limit.

After updating the timeout settings, verify if the session duration reflects the new configuration.

### Login Failure in SSO-Enabled Organizations via Credentials

Login attempts fail for SSO-enabled organizations even when "Strict SSO" is disabled. Despite the setting, the system displays an error message stating that access is restricted to SSO authentication only.

**Root Cause**

The "Allow Access Without SSO" configuration is not explicitly enabled for the specific user within the organization settings.

**Resolution**

1.  Access the **Organization User settings**.
2.  Explicitly enable the **Allow Access Without SSO** setting for the affected user.
3.  If the user still cannot access the platform, remove and re-invite the user to refresh their access permissions and SSO-related flags.

After updating the user settings or re-inviting the user, verify if the account can successfully authenticate without using SSO.

### Newly Invited SSO User Unable to Proceed Past Login Screen

Accessing Contentstack as a newly invited SSO user may fail at the login screen.

**Root Cause**

The user account is in a locked state, which prevents authentication even when the user has valid invitations and credentials.

**Resolution**

1.  Reset the login lock for the affected user.
2.  Ask the user to attempt to log in to Contentstack.

If the user successfully proceeds past the login screen, the issue is resolved.

### SSO Login Failure Due to Expired or Outdated Certificate

Attempting to log in via SSO as an organization owner may fail when the SSO certificate is not updated.

**Root Cause**

The SSO certificate has expired or is outdated, preventing successful authentication between the Identity Provider and Contentstack.

**Resolution**

1.  Navigate to the SSO configuration settings in Contentstack.
2.  Update the SSO certificate with the current valid certificate from the Identity Provider.
3.  Save the configuration changes.

After updating the SSO certificate, attempt to log in using SSO. If the login is successful, the issue is resolved.

### SSO Login Fails Due to an Incorrect SAML Email Attribute

The SSO Connection Test may fail during SAML configuration even when the certificate and URL are correctly set up.

**Root Cause**

An incorrect email attribute was being passed in the SAML assertion, causing the connection test to fail.

**Resolution**

1.  Review the SAML attribute mapping in the identity provider configuration.
    
2.  Update the email attribute to the correct value.
    
3.  Re-run the SSO Connection Test in Contentstack.
    

After correcting the attribute and re-running the test, verify that the SSO connection succeeds and that users can authenticate.

### SSO Login Fails Due to Unsupported Long-Form SAML Attribute Names

SSO configuration and testing may fail even when the certificate and URL are correctly uploaded.

**Root Cause**

Contentstack requires short attribute names (email, first\_name, last\_name) for SAML assertions. Long schema URNs (for example, http://schemas.xmlsoap.org/ws/2005/05/identity/claims/Email) are not supported.

**Resolution**

1.  Open the identity provider's application configuration.
    
2.  Replace any long schema URNs used for SAML attributes with the supported short names: email, first\_name, and last\_name.
    
3.  Save the updated configuration.
    

After updating the attribute names, retest SSO to confirm authentication completes successfully.

### SSO Login Fails Due to a Missing or Mismatched Email/NameID in the IdP

SSO login may fail without a clear error, even though the issue does not originate on the Contentstack side.

**Root Cause**

This behavior typically originates from the identity provider configuration. Common causes include: the user has no email address defined in the IdP, the email address configured in the IdP does not match the one used for authentication, or the NameID field in the IdP settings is not set to EmailAddress.

**Resolution**

1.  Confirm the affected user has an email address defined in the identity provider.
    
2.  Verify the email address in the IdP matches the one used during authentication.
    
3.  Confirm the NameID field in the IdP settings is set to EmailAddress.
    

After correcting the identity provider configuration, ask the user to retry SSO login to verify access is restored.

### SSO Login Fails With “Access Denied” Due to Corrupted IdP/Profile Mapping

A user may be unable to log in at all via SSO, receiving an “access denied” error, even though they belong to the correct Active Directory or identity provider groups and other users in the same group can log in without issue.

**Root Cause**

A corrupted user profile or a misconfigured IdP role mapping can block authentication for a specific user, even when their group membership is correct on the identity provider side.

**Resolution**

1.  Validate the affected user's identity provider group membership to confirm it is correct.
    
2.  Verify the IdP role mapping configuration for signs of misconfiguration.
    
3.  Clear browser cache or attempt login in an incognito window to rule out a client-side cause.
    
4.  If the error persists, remove the user from both the Contentstack groups and the identity provider, purge their profile and cache data, and re-add them to the appropriate groups to generate a fresh IdP mapping.
    

After re-provisioning the account, confirm the user can log in, authenticate via SSO, and access their assigned stacks.

### Safely Removing Users From Contentstack After IdP Deprovisioning

Users removed or deactivated in an identity provider such as Okta may still appear in Contentstack's user list.

**Root Cause**

Contentstack does not automatically remove a user's account when that user is deprovisioned in the identity provider; removal must be performed manually within Contentstack.

**Resolution**

1.  Confirm the user no longer exists in the identity provider and does not require Contentstack access.
    
2.  If the user holds stack ownership, reassign ownership to another user before proceeding.
    
3.  Delete the user directly within Contentstack.
    

Deleting the user this way does not affect the SSO configuration for remaining users, provided the user no longer exists in the IdP. Once deleted, the user loses all access to Contentstack.

### Cannot Stay Logged Into Multiple Organizations With Different SSO Configurations

Users who belong to two organizations with different SSO configurations may be unable to use the Org Switcher to move between both in the same browser session.

**Root Cause**

Contentstack manages sessions using browser cookies scoped to the application hostname (for example, app.contentstack.com). When two organizations use different SSO configurations but share the same hostname, only one active session is possible per browser at a time, so the Org Switcher cannot maintain simultaneous sessions across both.

**Resolution**

The Org Switcher does not support two concurrent SSO sessions on a shared hostname.

1.  Use separate browser sessions, such as a second browser or an incognito window, to access each organization at the same time if simultaneous access is required.
    
2.  Contact your Customer Success Manager to discuss a dedicated hostname or alternative configuration if this limitation affects regular workflows.
    

Confirm that each organization can be accessed individually, and that simultaneous access across both is possible using separate browser sessions.

### New Users Cannot Authenticate When Invited via the Contentstack UI in Strict-Mode SSO Organizations

New users can be provisioned and invited successfully, but are still unable to log in via SSO, while existing users in the same organization continue to log in without issue.

**Root Cause**

When an organization has SSO Strict Mode enabled, users invited directly through the Contentstack UI are provisioned for standard email/password access, which conflicts with Strict Mode's requirement that all access be governed by the identity provider. Users added this way cannot authenticate via SSO, while users originally provisioned through the IdP are unaffected.

**Resolution**

1.  Confirm whether the organization has SSO Strict Mode enabled.
    
2.  If so, provision the new user directly from the identity provider (for example, Okta or Microsoft Entra ID) side, rather than inviting them through the Contentstack UI.
    
3.  If email/password access is needed instead of SSO, have the Organization Owner disable Strict Mode and then re-invite the user with Allow Access without SSO enabled.
    

After provisioning the user through the identity provider, confirm they can log in successfully via SSO.

### SSO Access Denied Due to an Incorrect SAML Group or Role Attribute

Users may receive an “Access denied! You are not part of Contentstack” error during SSO login, or find that only some Okta/IdP groups can log in while others, especially newly created ones, cannot, even though all groups appear correctly provisioned.

**Root Cause**

In the confirmed cases, this was traced to the SAML attribute carrying group information: either the attribute was not named roles, as Contentstack requires, or the group values sent by the identity provider did not exactly match the IdP Role Identifier strings configured in the Contentstack IDP panel, including spacing and punctuation. Affected users were denied access even though they appeared correctly provisioned.

**Resolution**

1.  In the identity provider's SAML application, open the Attribute Statements / Group Attribute Statements configuration.
    
2.  Ensure the attribute that sends the user's groups is named roles.
    
3.  Confirm the group values being sent exactly match the IdP Role Identifier strings configured in the Contentstack IDP panel, including spacing and punctuation.
    
4.  Capture a fresh SAML response (for example, using a SAML tracer) to confirm it includes the expected group/role attribute.
    
5.  If mismatches remain for specific users, remove and re-add them to the group on the IdP side to trigger a fresh sync cycle.
    

After correcting the attribute name and group values, confirm the previously denied users or groups can authenticate successfully via SSO.

### SCIM-Assigned Roles Get Overwritten by IdP Role Mapping at Every Login

Users may be repeatedly downgraded to a lower-privilege role, such as Read-Only, immediately after login, despite having the correct role assigned in both Contentstack and the identity provider.

**Root Cause**

When both SCIM provisioning and IdP Role Mapping are enabled at the same time, the IdP role mapping re-evaluates and can overwrite the SCIM-assigned role every time a user logs in. This causes roles to silently revert, even though SCIM assigned the correct role in advance through group synchronization.

**Resolution**

1.  Confirm whether both SCIM provisioning and IdP Role Mapping are enabled for the organization.
    
2.  If so, disable IdP Role Mapping so that SCIM remains the single source of truth for role assignment and synchronization.
    
3.  Review the identity provider's group-to-role mappings for the affected users to confirm they are configured correctly.
    

After disabling IdP Role Mapping, confirm the user's role remains stable across multiple logins.

### Misleading “Failed Login Attempt” Email Notifications Sent to SSO Users

SSO-enabled users may receive an email about failed login attempts or a changed password, even though their account was never compromised and their SSO access continues to work normally.

**Root Cause**

This notification is triggered by multiple failed attempts on Contentstack's standard username/password login page, regardless of whether the account is actually configured for SSO. Since SSO-enabled accounts are authenticated entirely through the identity provider, Contentstack does not manage their password, so these notifications do not reflect any real impact to the account or its SSO access.

**Resolution**

1.  Confirm the account is configured for SSO, meaning authentication is handled entirely by the identity provider.
    
2.  Disregard the notification, since it does not indicate that the account or its SSO access has been affected.
    
3.  Continue logging in through the normal SSO flow to confirm access is unaffected.
    

After logging in via SSO, confirm access works normally despite having received the notification.

<!-- case:00060768 status:draft synced:false bucket:"Single Sign-On (SSO) & IdP Configuration" -->
### SSO Login Fails When Roles Attribute Missing With Role Mapping

Enabling SSO Role Mapping without including the required roles attribute in the SAML assertion may block SSO login for all users in the organization.

**Root Cause**

SSO Role Mapping requires a roles attribute containing an array of strings in the SAML assertion to map Identity Provider roles to Contentstack roles. When Role Mapping is enabled but this attribute is missing from the assertion, authentication fails for every user in the organization.

**Resolution**

1.  In the identity provider's SAML application, add a roles attribute to the SAML assertion, formatted as an array of strings.

2.  Map each IdP Role Identifier to the corresponding Contentstack role, such as a custom read-only Content Viewer role, in the Contentstack IDP panel.

3.  Save the updated SAML and IDP configuration.

4.  Have an affected user retry SSO login to confirm access is restored.

After adding the roles attribute and confirming the IdP Role Identifier mapping, have a user retry SSO login. If authentication completes successfully, the issue is resolved. Escalate with a fresh SAML response capture if login continues to fail.

<!-- end:00060768 -->

## Multi-Factor Authentication (2FA) & Security

### Two-Factor Authentication Login Failure Due to Expired Training Instance

Login attempts fail after entering a two-factor authentication verification code and clicking Verify. No error message is displayed, and access to the account is not granted.

**Root Cause**

The training instances associated with the account have expired, which prevents the login completion.

**Resolution**

1.  Access the appropriate link to create a new training instance.

After creating a new training instance, attempt to log in using the two-factor authentication process to verify if access is restored

### Resolving 2FA SMS Code Delivery Failure

Login attempts fail when the two-factor authentication code is not received via SMS. Authentication cannot be completed because the required verification code is not delivered.

**Root Cause**

Two-factor authentication codes fail to deliver via SMS, preventing the completion of the login process.

**Resolution**

1.  Install the Authy app on your mobile device.
2.  Switch the two-factor authentication method from SMS to app-based authentication.
3.  Configure the Authy app to receive authentication codes for the account.

After configuring the Authy app, enter the generated code into the login prompt to verify if access is restored.

### 2FA Authentication Failure Due to Authy Service Issue

Login attempts fail when an unexpected two-factor authentication requirement appears and verification codes are not received. Authentication cannot be completed, preventing access to the account.

**Root Cause**

A service issue with Authy prevents the delivery of multi-factor authentication codes required for the login process.

**Resolution**

1.  Contact Contentstack Support to request a temporary disablement of two-factor authentication for the account.
2.  Re-enable multi-factor authentication through the account security settings once the Authy service issue is resolved.

After the temporary disablement of 2FA, attempt to log in to verify if access is restored.

### Unexpected User Session Logouts

Unexpected session logouts may occur in Contentstack when security configurations such as Two-Factor Authentication are not enabled.

**Root Cause**

Missing security configurations, such as Two-Factor Authentication (2FA), can lead to unintended session termination or security-related drops.

**Resolution**

1.  Enable Two-Factor Authentication (2FA) for the affected user account.
2.  Monitor the account for any further unexpected logouts.

After enabling 2FA, monitor the session stability during platform use. If the user remains logged in without further interruptions, the issue is resolved.

### Regaining Access After Losing or Breaking Your MFA Device

Login is blocked when the device enrolled for two-factor authentication is lost, broken, or otherwise inaccessible, and no backup method is available.

**Root Cause**

Contentstack does not provide a self-service way to bypass multi-factor authentication when the enrolled device is unavailable. Disabling MFA on an account requires explicit approval from the Organization Owner.

**Resolution**

1.  Contact the Organization Owner to request approval to disable MFA on the affected account.
    
2.  Once approval is confirmed, Contentstack Support disables MFA for the account.
    
3.  Log in using the account's username and password now that MFA has been disabled.
    
4.  Set up MFA again on a new device if continued use of two-factor authentication is desired.
    

After MFA is disabled and login is confirmed, verify that a new authentication method can be configured successfully if needed.

### Resetting a User's MFA as an Organization Admin

Organization Admins may be unaware that MFA can be reset directly from the Organization Users list, and may escalate to Contentstack Support instead of using the self-service option already built into the product.

**Root Cause**

Resetting a user's MFA is a standard, self-service action available to anyone with Administration access, it does not require a separate feature to be enabled or a Support ticket.

**Resolution**

1.  Navigate to Administration (via the App Switcher), then open the Users tab.
    
2.  Click the vertical ellipses in the Actions column next to the affected user, and select Reset MFA.
    
3.  In the Reset Multi-Factor Authentication modal, click Proceed to confirm.
    
4.  The user receives an email with a link to reset their MFA configuration on a new device.
    

After the reset is triggered, confirm the user receives the reset-MFA email and can successfully reconfigure MFA on their device, without needing to contact Contentstack Support.

### MFA SMS Code Not Received Due to Browser Cache

A two-factor authentication SMS code may fail to arrive during login, even though the phone number on file is correct.

**Root Cause**

Corrupted or stale browser cache and cookies can interfere with the delivery or recognition of SMS-based verification codes during login.

**Resolution**

1.  Try logging in using an incognito or private browser window.
    
2.  If the issue persists, try a different browser.
    
3.  Clear the browser cache and cookies, then retry the login.
    

After clearing the cache or switching browsers, verify that the SMS code is received and that login completes successfully.

## Profile Updates & Email Changes

### Password Reset Email Not Received Due to Expired Training Instance

Login attempts fail and the Forgot Password option does not trigger a password reset email. Access to the account is not granted because the expected reset communication is not received.

**Root Cause**

The email address used for login is associated with an expired training instance, which prevents the password reset process from functioning.

**Resolution**

1.  Create a new training instance using a different email address.
2.  Create a new training instance using the same email address while selecting a different region instead of AWS NA.

After creating a new training instance, attempt to log in or trigger the password reset process to verify if access is restored.

### Updating User Email Addresses Following Domain Changes

Email address updates to a new domain fail when the email field is non-editable. This occurs because the platform does not allow direct modification of existing user email addresses.

**Root Cause**

User email addresses are immutable in Contentstack and cannot be modified once an account has been created.

**Resolution**

1.  Remove users with the old email domains from the organization.
2.  Re-invite users using their new email addresses.
3.  Reassign the necessary roles and permissions to the newly invited accounts.
4.  Configure alias support on the Identity Provider, such as Okta or Azure AD, if SSO is enabled.

After re-inviting the users and reassigning permissions, have the users log in with their new email addresses to verify if access is restored.

### Live Preview Fails to Load with Third-Party Authentication

Live Preview fails to load when the application uses a third-party authentication provider and redirection. Preview windows remain empty or fail to initialize because the authentication flow is blocked.

**Root Cause**

Live Preview does not support third-party OAuth authentication flows because iframes block the required redirects as per documented security limitations.

**Resolution**

1.  Verify if the application uses third-party OAuth authentication flows (such as Keycloak) that require redirection.
2.  Refer to the Live Preview limitations documentation to confirm unsupported authentication methods.
3.  Note that this restriction is expected behavior and cannot be bypassed using Content Security Policy (CSP) changes.

After reviewing the authentication flow and documentation, verify if removing the redirection requirement for the preview environment allows the preview to lo

## Organization & Stack Invitations

### Stack Invitation Acceptance Failure Due to Missing Organization Access

Stack invitations cannot be accepted when login credentials for the platform have not yet been established. Access to the specific stack is not granted until login credentials for the platform have been established.

**Root Cause**

Organization-level access and valid login credentials must be established before a user can accept invitations to individual stacks.

**Resolution**

1.  Obtain organization-level access to the platform.
2.  Log in through Okta.
3.  Accept the stack invitation once organization access is confirmed.

After obtaining organization access and logging in, check the stack list to verify if access is restored.

### Login Failure Due to Missing Organization Membership

Attempting to access Contentstack may fail during the login process.

**Root Cause**

The user account is not associated with any organization, preventing access to the platform.

**Resolution**

1.  Request an organization invitation from the relevant administrator.
2.  Accept the invitation to join the organization.
3.  Attempt to log in to Contentstack.

If the user successfully accesses the platform after joining the organization, the issue is resolved

### Demo Organization Not Visible in Dashboard

Accessing a demo organization may result in visibility issues when the organization does not appear in the dashboard and access emails are missing.

**Root Cause**

The user lacks formal ownership or an accepted invitation for the specific organization, preventing it from appearing in the user interface.

**Resolution**

1.  Contact Contentstack Support to request an organization ownership transfer email.
2.  Accept the ownership transfer invitation.

After accepting the ownership transfer, verify the visibility of the organization in the dropdown menu. If the organization appears as expected, the issue is resolved.

### Dashboard Loading Error When Accessing Organization Entries

Attempting to access entries within an organization may result in the dashboard failing to load and displaying a "Something went wrong" error.

**Root Cause**

Role-related inconsistencies in user permissions prevent the dashboard from syncing and loading correctly.

**Resolution**

1.  Contact the organization owner or administrator to refresh account permissions.
2.  Change the organization role from Member to Admin, then revert it to the original role (or vice versa if currently an Admin).
3.  Remove the user from the organization and re-add them with the correct role to resync access.

After re-adding the user and updating roles, attempt to access the organization entries. If the dashboard loads without error, the issue is resolved.

### Unable to Log In or Reset Password for Lytics

link

Logging in to Lytics or resetting account passwords may fail when using the standard login page or credentials.

**Root Cause**

The account requires authentication through a specific OAuth link rather than the standard login process.

**Resolution**

1.  Request the manual OAuth login link from Contentstack Support.
2.  Use the OAuth link instead of the standard login page to log in to Lytics.

After using the OAuth link, attempt to authenticate. If the login is successful, the issue is resolved.

### Restricted Stack Access for IdP-Managed Users

Stack access may be restricted and roles may be unassignable when SSO or Identity Provider management is enabled for an organization.

**Root Cause**

When SSO/IdP is enabled and managed externally, user roles and stack permissions must be synchronized through the Identity Provider rather than being manually updated within the Contentstack platform.

**Resolution**

1.  Verify the user is already part of the organization and has accepted the organization-level invitation.
2.  Coordinate with the internal IdP team to assign the appropriate roles and permissions via IdP groups for the required stack.
3.  Ensure the internal team creates and maps the necessary groups in the IdP for new stacks.
4.  Test stack access after the user has been assigned to the correct IdP groups.

After the IdP team updates the group assignments, attempt to access the specific stack in Contentstack. If the user can see the stack and perform actions aligned with their assigned role, the issue is resolved.

### Login Failure Due to Incorrect Region or Data Center Selection

Login attempts may fail or return incorrect-password errors when the wrong regional login URL is used (for example, an Azure-Europe link for an account hosted on AWS-Europe, or an EU link for an NA-hosted account), even when the credentials themselves are correct.

**Root Cause**

Contentstack credentials and SSO configurations are tied to the specific region and data center where the account was created (such as AWS NA, AWS EU, Azure EU, or GCP NA). Attempting to authenticate through a different region's URL causes the login to fail even when the credentials are correct. For more detail on how regions work, see the Contentstack documentation on regions (https://www.contentstack.com/docs/administration/about-regions).

**Resolution**

1.  Confirm which region and data center the organization is hosted in.
    
2.  Use the corresponding regional login URL (for example, https://eu-app.contentstack.com/#!/login for AWS EU, or https://gcp-na-app.contentstack.com/#!/login for GCP NA).
    
3.  Retry login or SSO authentication using the correct regional endpoint.
    

After switching to the correct regional login URL, attempt to log in again to verify that authentication completes without password or redirect errors.

### Dashboard Fails to Load or “Cannot Access Entry” Error Despite Admin Permissions

A user with confirmed administrator-level permissions may be able to log in but find that the stack dashboard fails to load, or that opening any entry returns a “cannot access entry” error stating the page is unavailable.

**Root Cause**

Failed network requests to the /extensions API can prevent the dashboard from rendering or entries from loading, even when the user's permissions and role are correctly configured.

**Resolution**

1.  Confirm the affected user has been granted the correct permissions and role within the stack.
    
2.  Have Contentstack Support remove the affected user from the organization.
    
3.  Have the organization admin re-add the user with the same role.
    

After re-adding the user, verify that the dashboard loads and that entries can be opened without the “cannot access entry” error.

### Unexpected Session Logouts Can Occur Even When Authentication Is Working Normally

A user may be logged out of Contentstack unexpectedly while editing, without any advance warning, even though nothing appears to be wrong with their account or credentials.

**Root Cause**

Contentstack manages authentication using access tokens and refresh tokens that work together to maintain the session in the background. Under normal conditions, the refresh token automatically renews the access token so the session continues without requiring the user to log in again. However, sessions can still be invalidated by factors such as browser security policies, network interruptions, extended inactivity, manual logout, or other security-related events, and both tokens expiring at the same time, while rare, remain possible.

**Resolution**

An occasional unexpected logout can happen even when authentication is otherwise functioning normally, due to browser- or network-level session invalidation rather than an account problem.

1.  As a best practice, save work periodically during long editing sessions, since a session is not guaranteed to persist indefinitely.
    
2.  If logouts become frequent under otherwise stable network and browser conditions, report the pattern, including browser, network conditions, and session duration, so it can be investigated further.
    

If logouts persist or increase in frequency, share these details so the behavior can be reviewed further.

## SCIM & Automated User Provisioning

### SCIM Provisioning Stops After API Token Deprecation

SCIM provisioning may stop functioning even though the associated SSO configuration continues to work normally.

**Root Cause**

The SCIM API token associated with the identity provider connection has been deprecated, halting provisioning independently of the SSO setup.

**Resolution**

1.  Navigate to Contentstack Marketplace > Manage Apps, and locate the app connection for your identity provider.
    
2.  Uninstall the existing identity provider app connection.
    
3.  Re-authenticate and reinstall the app to generate a new SCIM API token.
    
4.  Avoid using a deprecated identity provider app integration for new configurations going forward.
    

After reinstalling the app, confirm that SCIM provisioning resumes for new and existing users. This action does not affect the existing SSO configuration.

### SCIM/SSO Error Due to Incorrect Authorization URL

A SCIM-related error may appear while configuring SSO in certain regions, such as GCP NA.

**Root Cause**

The OAuth authorization URL used during setup was not constructed correctly for the account's region.

**Resolution**

1.  Refer to the Contentstack OAuth documentation for constructing the correct authorization URL.
    
2.  Update the SSO/SCIM configuration with the properly constructed authorization URL for the account's region.
    

After updating the authorization URL, retry the SCIM sync to verify the error no longer occurs.

### OAuth Authorization in Automate Workflows Breaks When Tied to a User Account

OAuth-based authorization used within Contentstack Automate workflows may stop working unexpectedly across all stacks, even though it had previously been functioning normally.

**Root Cause**

OAuth authorization in Automate is tied to the individual user account that originally authorized it, creating a dependency on that user's account state, such as account disablement or permission changes. A platform-level issue previously caused this OAuth authorization to stop working unexpectedly; that issue has since been fixed on the platform side.

**Resolution**

1.  As the more stable long-term approach, use Management Tokens instead of OAuth for Automate workflows. Management Tokens are not tied to an individual user account, which removes this dependency and reduces the risk of workflow failure due to user-related changes.
    
2.  If you are currently affected by an OAuth authorization failure of this kind, contact Contentstack Support to confirm your environment reflects the platform-side fix.
    

After switching to Management Tokens, or after confirming the platform fix is reflected in your environment, confirm Automate workflows run without interruption.

## Browser & Client-Specific Login Issuees

### “Next” Button Not Visible After Scanning the MFA QR Code Until the Browser Is Zoomed Out

While setting up two-factor authentication, a user may scan the QR code successfully but be unable to find or click the “Next” button needed to complete setup.

**Root Cause**

At certain browser zoom levels, the “Next” button on the MFA setup screen can render off-screen or hidden after the QR code is scanned, preventing the user from completing the setup step, even though the scan itself succeeded.

**Resolution**

1.  After scanning the QR code during MFA setup, if the “Next” button is not visible, zoom out the browser window.
    
2.  Click “Next” to complete MFA setup.
    

After zooming out and clicking “Next,” confirm MFA setup completes and login succeeds.

### Verification Code Not Received Because MFA Uses an Authenticator App, Not SMS or Email

A user may expect a verification code to arrive by email or SMS and be unable to log in when no such code appears.

**Root Cause**

When MFA is enabled on an account, the verification code must be generated by an authenticator app (such as Google Authenticator, Microsoft Authenticator, or Authy) configured during MFA setup. It is not sent by email or SMS.

**Resolution**

1.  Confirm MFA is enabled on the account.
    
2.  Open the authenticator app that was configured during MFA setup.
    
3.  Use the code currently displayed in the app, rather than waiting for an email or SMS code, to complete login.
    

After entering the app-generated code, confirm login succeeds.

### Blank Content Blocks and Login Failures Caused by Stale Session Token Caching

Multiple editorial users may experience login failures and blank content blocks within the CMS at the same time.

**Root Cause**

The behavior is consistent with a session or authentication token caching issue on the client side, where the browser fails to automatically refresh the cached session, resulting in login failures and content blocks that do not render.

**Resolution**

1.  Clear the browser cache and cookies.
    
2.  Log back in to Contentstack.
    

After clearing the cache and logging back in, confirm content blocks render correctly and login no longer fails. If the issue recurs at scale, capture a HAR file (from the browser's Network tab) before clearing the cache to help identify why the session failed to refresh automatically.