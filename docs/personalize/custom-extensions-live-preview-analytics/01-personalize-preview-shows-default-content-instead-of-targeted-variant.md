---
title: "Personalize Preview Displays Default Content Instead of Targeted Variant"
slug: "personalize-preview-shows-default-content-instead-of-targeted-variant"
pod: "Personalize"
section: "Custom Extensions, Live Preview & Analytics"
order: 1
meta_title: "Personalize Preview Displays Default Content Instead of Targeted Variant | Contentstack"
meta_description: "Personalize preview mode may show default content instead of a targeted variant due to a stale audience-context cookie. Learn how to clear the cookie and start a fresh preview session to resolve it."
status: "published"
source_case_id: "00099007"
contentstack_parent_entry_uid: "blt42160a754b110d62"
contentstack_category_heading: "Custom Extensions, Live Preview & Analytics"
migrated_from: null
migrated_on: null
---

# Personalize Preview Displays Default Content Instead of Targeted Variant

Personalize preview mode may display default content instead of the targeted variant, even when the preview audience matches the targeting rule.

## Root cause

The preview session was using a stale audience-context cookie that had been set before the targeting rule was last edited, causing the preview to continue rendering default content instead of reflecting the updated rule.

## Resolution

1. Clear the preview cookie in your browser.
2. Start a fresh preview session.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
