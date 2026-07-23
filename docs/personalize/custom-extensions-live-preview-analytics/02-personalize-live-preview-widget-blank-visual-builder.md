---
title: "Personalize Live Preview Widget Shows Blank Panel in Visual Builder"
slug: "personalize-live-preview-widget-blank-visual-builder"
pod: "Personalize"
section: "Custom Extensions, Live Preview & Analytics"
order: 2
meta_title: "Personalize Live Preview Widget Not Loading in Visual Builder | Contentstack"
meta_description: "Learn why the Personalize live preview widget may show a blank panel in Visual Builder and how an ad-blocker extension can cause it, plus the fix."
status: "draft"
source_case_id: "00099009"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# Personalize Live Preview Widget Shows Blank Panel in Visual Builder

The Personalize live preview widget fails to load inside Visual Builder, displaying a blank panel with no error message.

## Root cause

An ad-blocker browser extension blocks the preview widget's script from loading because its URL pattern matches a common tracking-script signature.

## Resolution

1. Add the Personalize preview domain to your ad-blocker's allowlist.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
