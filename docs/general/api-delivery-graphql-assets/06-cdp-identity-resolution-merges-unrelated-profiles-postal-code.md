---
title: "CDP Identity Resolution Merges Unrelated Customer Profiles Sharing the Same Postal Code"
slug: "cdp-identity-resolution-merges-unrelated-profiles-postal-code"
pod: "General"
section: "API Delivery, GraphQL & Assets"
order: 6
meta_title: "CDP Identity Resolution Merges Unrelated Customer Profiles | Contentstack"
meta_description: "Learn why Contentstack CDP identity resolution may incorrectly merge unrelated customer profiles that share only a postal code, and how to fix it by tightening the matching ruleset."
status: "draft"
source_case_id: "00099001"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# CDP Identity Resolution Merges Unrelated Customer Profiles Sharing the Same Postal Code

CDP identity resolution may merge two genuinely different customer profiles into a single profile whenever they share the same postal code.

## Root cause

The identity-resolution rule set was configured to match on postal code alone as a fallback signal, which was too loose for the customer's customer base density.

## Resolution

1. Tighten the identity-resolution ruleset to require postal code plus at least one additional matching signal (email or phone) before merging profiles.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
