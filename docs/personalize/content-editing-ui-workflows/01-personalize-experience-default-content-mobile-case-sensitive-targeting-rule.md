---
title: "Personalize Experience Shows Default Content on Mobile Devices Due to Case-Sensitive Targeting Rule"
slug: "personalize-experience-default-content-mobile-case-sensitive-targeting-rule"
pod: "Personalize"
section: "Content Editing & UI Workflows"
order: 1
meta_title: "Personalize Experience Not Applying to Mobile Devices | Contentstack"
meta_description: "Learn why a Personalize targeting rule can fail to apply on mobile devices because of a case-sensitive mismatch between the rule value and the SDK-reported device type, and how to fix it."
status: "draft"
source_case_id: "00099016"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# Personalize Experience Shows Default Content on Mobile Devices Due to Case-Sensitive Targeting Rule

A Personalize experience may render correctly on desktop but always show default content on mobile devices, even when a mobile targeting rule is configured.

## Root cause

The experience's targeting rule used a device-type attribute value of "Mobile" (capitalized), while the SDK reported the device type in lowercase as "mobile". Because the comparison is case-sensitive, the rule never matched on mobile devices, so the experience fell back to default content.

## Resolution

1. Update the targeting rule's device-type attribute value to lowercase "mobile" so it matches the value the SDK actually sends.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.

<!-- diagnostic nudge -->
