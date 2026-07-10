---
title: "IP Allowlist Blocks Legitimate Office Traffic After Office Relocation"
slug: "ip-allowlist-blocks-office-traffic-after-relocation"
pod: "General"
section: "Authentication & Login"
order: 4
meta_title: "IP Allowlist Blocking Office Traffic After Relocation | Contentstack"
meta_description: "Learn why an outdated IP allowlist entry can block an entire office from accessing a Contentstack stack after a physical move, and how to update the allowlist to restore access."
status: "draft"
source_case_id: "00090010"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# IP Allowlist Blocks Legitimate Office Traffic After Office Relocation

Accessing a stack may return an IP-restriction error for an entire team after a physical office relocation.

## Root cause

The stack's IP allowlist still referenced the old office's static IP range. Traffic from the new office location did not match any entry in the allowlist under Security settings, so requests were rejected.

## Resolution

1. Add the new office's IP range to the stack's IP allowlist under Security settings.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
