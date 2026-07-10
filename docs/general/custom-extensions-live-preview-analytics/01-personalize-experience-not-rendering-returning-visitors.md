---
title: "Personalize Experience Not Rendering for Returning Visitors"
slug: "personalize-experience-not-rendering-returning-visitors"
pod: "General"
section: "Custom Extensions, Live Preview & Analytics"
order: 1
meta_title: "Personalize Experience Not Rendering for Returning Visitors | Contentstack"
meta_description: "Personalize experiences may render for first-time visitors but fail for returning visitors when third-party cookies are blocked by default. Learn how to fix the cookie-consent configuration to restore identity resolution."
status: "draft"
source_case_id: "00090002"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# Personalize Experience Not Rendering for Returning Visitors

Personalize experiences render correctly for first-time visitors but fail to render for returning visitors on the same device.

## Root cause

The site's cookie-consent configuration blocked third-party cookies by default. This caused the Personalize identity-resolution cookie to be dropped between sessions, so Personalize could not recognize the visitor as a returning user on subsequent visits.

## Resolution

1. Update your cookie-consent configuration to allow the Personalize first-party cookie category by default.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
