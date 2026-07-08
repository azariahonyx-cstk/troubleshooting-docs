---
title: "SSO Certificate Renewal Blocked When Original Organization Owner Has Left"
slug: "sso-certificate-renewal-blocked-when-original-organization-owner-has-left"
pod: "AUTH"
section: "Authentication & Login"
order: 2
meta_title: "Troubleshooting Authentication & Login | Contentstack"
meta_description: "Solutions for SSO login failures, invitation acceptance issues, organization ownership transfers, account state problems, and Management Token identification in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "AUTH (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# SSO Certificate Renewal Blocked When Original Organization Owner Has Left

Updating an expiring SSO certificate is not possible because access to SSO and Security Configuration settings is restricted to Organization Owners, and the original Organization Owner has left the organization.

## Root cause

Contentstack restricts access to SSO settings and Security Configuration to users with the Organization Owner role. When the original Organization Owner leaves and the role is not transferred beforehand, no existing user can access these settings.

## Resolution

1. Identify a user in the organization who should receive the Organization Owner role.
2. Contact Contentstack Support and request an organization ownership transfer, providing the current owner's details and the intended new owner's email address.
3. Once Support initiates the transfer, the designated user will receive a transfer request — accept the request to gain Organization Owner access.
4. After accepting the transfer, navigate to Settings > SSO to update the expiring certificate with the new certificate details.
5. Verify that SSO authentication continues to function correctly after updating the certificate.

## Verification

After completing these steps, confirm that SSO login works with the renewed certificate. If the ownership transfer or SSO update does not complete successfully, escalate with the organization UID, the new owner's email address, and the certificate expiry date.
