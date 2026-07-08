---
title: "Contentstack Support Portal Access Fails with a Connection Error on VPN Networks"
slug: "contentstack-support-portal-access-fails-with-a-connection-error-on-vpn-networks"
pod: "General"
section: "Authentication & Login"
order: 2
meta_title: "Troubleshooting Authentication & Login | Contentstack"
meta_description: "Solutions for Partner Academy access failures, Support Portal connectivity issues on VPN networks, and forced logout incidents in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "General (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Contentstack Support Portal Access Fails with a Connection Error on VPN Networks

Accessing the Contentstack Support Portal and selecting any login option may result in an immediate redirect to an error page rather than a successful login screen, with a net::ERR_CONNECTION_CLOSED error visible in the browser's developer console. The issue may affect multiple users across different VPN configurations simultaneously.

## Root cause

Root cause was not documented in the source case. The resolution below addresses the reported symptom. The behavior has been observed when connecting through specific VPN solutions and is caused by a conflict between certain VPN network configurations and the backend infrastructure serving the Support Portal. Access has been confirmed to work consistently on non-VPN connections.

## Resolution

1. Disconnect from the VPN and attempt to access the Contentstack Support Portal again to confirm whether the issue is VPN-specific.
2. If access succeeds without VPN, confirm whether your organization's VPN policy permits access to the Support Portal URL — the VPN may be blocking or interfering with the connection.
3. If the Support Portal must be accessed while on VPN, contact your network or IT team to review whether the VPN routing configuration is compatible with the Support Portal's connection requirements.
4. If the issue persists even without VPN, or if it affects all users simultaneously, contact Contentstack Support directly via email to report the connectivity issue and provide the error message, the affected URL, the VPN client name and version, and the approximate number of affected users.

## Verification

After completing these steps, confirm that Support Portal access is restored. If the issue resolves without VPN but cannot be resolved on VPN, work with your IT team to adjust the routing rules. Escalate with browser console error logs, VPN client details, and the affected user count if the issue appears platform-wide.
