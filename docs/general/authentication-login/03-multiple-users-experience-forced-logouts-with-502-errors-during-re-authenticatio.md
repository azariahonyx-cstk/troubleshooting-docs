---
title: "Multiple Users Experience Forced Logouts with 502 Errors During Re-authentication"
slug: "multiple-users-experience-forced-logouts-with-502-errors-during-re-authenticatio"
pod: "General"
section: "Authentication & Login"
order: 3
meta_title: "Troubleshooting Authentication & Login | Contentstack"
meta_description: "Solutions for Partner Academy access failures, Support Portal connectivity issues on VPN networks, and forced logout incidents in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "General (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Multiple Users Experience Forced Logouts with 502 Errors During Re-authentication

Multiple users may be unexpectedly logged out of Contentstack and encounter a 502 Bad Gateway error when attempting to re-authenticate via an identity provider, with access restoring automatically after several minutes.

## Root cause

This behavior is caused by a specific traffic pattern that triggers a small number of complex, long-running queries against a particular dataset. The extended query execution time increases database response latency, creates request backlogs, and surfaces as intermittent 502 errors for users mid-session. The Contentstack platform has since addressed this by optimizing the affected queries, adding appropriate database indexes, and introducing backend query timeout controls to prevent similar occurrences.

## Resolution

1. Confirm that the forced logout and 502 error are affecting multiple users simultaneously — this behavior is indicative of a platform-level incident rather than an individual account issue.
2. Check the Contentstack Status Page at status.contentstack.com for any active or recently resolved incidents.
3. If an incident is not listed but the issue is widespread, contact Contentstack Support immediately and provide the following: the approximate start time of the forced logouts, the number of affected users, the organization UID, and any browser console errors or network logs captured during the 502 response.
4. Once the incident is resolved, users can log in again normally — no user-side configuration change is required to recover.

## Verification

After completing these steps, confirm that all affected users are able to log in successfully. If forced logouts with 502 errors recur after a platform incident has been resolved, escalate with session timestamps, a description of the behavior during re-authentication, and browser developer tool logs.
