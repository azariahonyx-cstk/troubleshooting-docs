---
title: "Unrecognized UID in Audit Logs Belongs to a Management Token"
slug: "unrecognized-uid-in-audit-logs-belongs-to-a-management-token"
pod: "AUTH"
section: "Authentication & Login"
order: 5
meta_title: "Troubleshooting Authentication & Login | Contentstack"
meta_description: "Solutions for SSO login failures, invitation acceptance issues, organization ownership transfers, account state problems, and Management Token identification in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "AUTH (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Unrecognized UID in Audit Logs Belongs to a Management Token

An audit log entry shows an unrecognized UID performing actions on a stack — such as modifying webhooks — but the UID cannot be matched to any user in the organization's user list.

## Root cause

UIDs that appear in audit logs but do not correspond to any user account may belong to Management Tokens rather than human users. Management Tokens are used by automated scripts, CI/CD pipelines, and API integrations to make programmatic changes to a stack. They appear in audit logs under their own UIDs rather than under a user name.

## Resolution

1. Note the unrecognized UID from the audit log entry, along with the stack UID and the timestamp of the action.
2. Review the Management Tokens configured for your stack by navigating to Settings > Tokens > Management Tokens in the affected stack.
3. Check whether any Management Token names correspond to the automated system or CI/CD integration that may have performed the action (such as a token named for a CLI or automation pipeline).
4. If the token cannot be identified through the self-service token list, contact Contentstack Support with the UID, the stack UID, and the timestamp to request identification of the token's origin, name, and permissions.

## Verification

After completing these steps, confirm the identity of the actor that made the changes. If the Management Token is unexpected or unauthorized, rotate or revoke it immediately from the Tokens settings page. Escalate with the stack UID and token creation details if further investigation is needed.
