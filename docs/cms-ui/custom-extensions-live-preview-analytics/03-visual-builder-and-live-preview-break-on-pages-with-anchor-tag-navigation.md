---
title: "Visual Builder and Live Preview Break on Pages with Anchor Tag Navigation"
slug: "visual-builder-and-live-preview-break-on-pages-with-anchor-tag-navigation"
pod: "CMS - UI"
section: "Custom Extensions, Live Preview & Analytics"
order: 3
meta_title: "Troubleshooting Custom Extensions & Live Preview | Contentstack"
meta_description: "Fix Visual Builder failures caused by anchor tags, and understand limitations with dynamically generated pages in Contentstack Live Preview and Visual Editor."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - UI Additions (Jun 28 2026)"
migrated_on: "2026-07-08"
---

# Visual Builder and Live Preview Break on Pages with Anchor Tag Navigation

Accessing a page within the Contentstack Visual Builder or Live Preview that uses anchor tag links (for example, a href="#section-id") for in-page navigation may cause the preview session to break, navigate away unexpectedly, or lose the current editing context.

## Root cause

Root cause was not documented in the source case. The observed behavior indicates that the Visual Builder and Live Preview intercept navigation events at the browser level. Anchor tag navigation within the same page may be interpreted as a full page navigation request, disrupting the preview session context.

## Resolution

1. Identify which pages in your application use anchor tags for in-page navigation (scroll-to-section links).
2. Test Visual Builder on pages without anchor tag navigation to confirm the preview loads and functions correctly on those pages.
3. If your application requires anchor tag navigation on pages used with Visual Builder, consider using JavaScript-based smooth-scroll implementations that do not trigger full navigation events.
4. Note that dynamically generated pages rendered at runtime from an external API and not stored as individual Contentstack entries are not supported in the Visual Editor — only pages that correspond to actual CMS entries can be edited in context.
5. If the issue occurs on pages without anchor tags, capture a screen recording of the error along with a HAR file and browser console logs.

## Verification

After completing these steps, confirm that Visual Builder maintains the editing context without breaking. Escalate with a screen recording, HAR file, a description of your routing setup, and whether the affected pages use anchor tag navigation if the issue persists.
