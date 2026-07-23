---
title: "Personalize Traffic Not Splitting According to Configured Variant Weights"
slug: "personalize-traffic-not-splitting-according-to-variant-weights"
pod: "Personalize"
section: "Content Editing & UI Workflows"
order: 2
meta_title: "Personalize Traffic Not Splitting According to Configured Variant Weights | Contentstack"
meta_description: "Learn why a Personalize experience may send nearly all traffic to a single variant despite a configured weight split, and how a leftover audience-priority rule can cause it."
status: "published"
source_case_id: "00099020"
contentstack_parent_entry_uid: "blt42160a754b110d62"
contentstack_category_heading: "Content Editing & UI Workflows"
migrated_from: null
migrated_on: null
---

# Personalize Traffic Not Splitting According to Configured Variant Weights

Configuring a 50/50 traffic split between two variants in a Personalize experience may not distribute visitors evenly, with nearly all traffic going to only one variant.

## Root cause

The experience retained a leftover audience-priority rule from an earlier draft. This rule forced one variant for a broad audience segment, which took precedence over the configured weighted split for most visitors.

## Resolution

1. Remove the leftover audience-priority rule from the experience configuration.

## Verification

After completing these steps, confirm that traffic is distributing according to the configured variant weights (e.g., 50/50) across a broader sample of visitors. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
