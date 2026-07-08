---
title: "Unpublished Locale Returns Content When include_fallback Is Enabled"
slug: "unpublished-locale-returns-content-when-include-fallback-is-enabled"
pod: "CMS - CDA(Rest)"
section: "API Delivery, GraphQL & Assets"
order: 2
meta_title: "Troubleshooting API Delivery, GraphQL & Assets | Contentstack"
meta_description: "Fix include_fallback locale behavior and Bulk Publish API version mismatches in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - CDA(Rest) Additions (Jun 28 2026)"
migrated_on: "2026-07-08"
---

# Unpublished Locale Returns Content When include_fallback Is Enabled

Fetching entries for a locale that has not been explicitly published returns content instead of a 404 error when the include_fallback parameter is included in the API request.

## Root cause

When include_fallback=true is passed in a CDA request, Contentstack walks up the fallback chain and returns content from the nearest available published locale (typically the master locale) when the requested locale has no published content. Additionally, child locale entries automatically inherit master locale data when a master locale entry is first created, so they may appear populated even if no locale-specific publishing has occurred.

## Resolution

1. Review your CDA API request and check the value of the include_fallback parameter.
2. To return content only for explicitly published locales, set include_fallback=false — a 404 response will be returned if the requested locale has not been published.
3. To preserve fallback behavior (returning master locale content for unpublished child locales), keep include_fallback=true.
4. Use the locale parameter alongside include_fallback to control which locale's data is fetched.
5. Review your locale fallback hierarchy in Settings > Languages if you need to adjust which locale acts as the fallback parent.

## Verification

After completing these steps, test your API requests for both published and unpublished locales to confirm the behavior matches your expectations. Escalate with the full request URL, response payload, and your stack's locale hierarchy if the behavior differs from the documented specification.
