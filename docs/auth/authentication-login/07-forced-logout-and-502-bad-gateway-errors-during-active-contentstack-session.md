---
title: "Forced Logout and 502 Bad Gateway Errors During Active Contentstack Session"
slug: "forced-logout-and-502-bad-gateway-errors-during-active-contentstack-session"
pod: "AUTH"
section: "Authentication & Login"
order: 7
meta_title: "Troubleshooting Authentication & Login Issues | Contentstack"
meta_description: "Resolve loading spinner failures and forced logout 502 errors in Contentstack AUTH."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "AUTH Additions (Jun 28 2026)"
migrated_on: "2026-07-08"
---

# Forced Logout and 502 Bad Gateway Errors During Active Contentstack Session

Multiple users are simultaneously logged out of Contentstack unexpectedly and encounter a 502 Bad Gateway (openresty) error when attempting to re-authenticate. Access typically restores automatically within minutes.

## Root cause

This type of incident can be triggered by a specific traffic pattern that causes a small number of complex database queries to take significantly longer than expected, increasing response times and creating request backlogs that surface as 502 errors. Once the affected queries are optimized or the traffic pattern normalizes, the service recovers automatically.

## Resolution

1. Check status.contentstack.com immediately to determine whether an active platform incident is in progress.
2. If a status incident is confirmed, wait for the Contentstack engineering team to resolve the issue — service typically restores within minutes for traffic-triggered incidents.
3. Once service is restored, log in normally — no user-side action is required.
4. If forced logouts and 502 errors are recurring without a corresponding status page incident, contact Contentstack Support with: the approximate start time and duration of the disruption, the number of affected users, the hosting region (for example, Azure NA, AWS EU), the browser type and version, and screenshots or a screen recording of the error.

## Verification

After completing these steps, verify that login and session stability are restored. Escalate with the details above if the issue recurs outside of a documented status page incident.
