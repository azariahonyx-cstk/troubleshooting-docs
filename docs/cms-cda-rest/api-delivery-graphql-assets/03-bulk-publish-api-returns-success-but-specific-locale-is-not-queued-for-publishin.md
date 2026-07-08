---
title: "Bulk Publish API Returns Success But Specific Locale Is Not Queued for Publishing"
slug: "bulk-publish-api-returns-success-but-specific-locale-is-not-queued-for-publishin"
pod: "CMS - CDA(Rest)"
section: "API Delivery, GraphQL & Assets"
order: 3
meta_title: "Troubleshooting API Delivery, GraphQL & Assets | Contentstack"
meta_description: "Fix include_fallback locale behavior and Bulk Publish API version mismatches in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - CDA(Rest) Additions (Jun 28 2026)"
migrated_on: "2026-07-08"
---

# Bulk Publish API Returns Success But Specific Locale Is Not Queued for Publishing

Using the Bulk Publish API to publish entries returns a success response, but one or more specific locales (for example, en-us) do not appear in the publish queue or are not published to the target environment.

## Root cause

Root cause was not fully resolved in the source case. An identified contributing factor is sending "version": 0 in the Bulk Publish API request payload while the entry's actual current version is 1 or higher. A version mismatch between the request payload and the actual entry version may cause certain locales to be silently excluded from the bulk publish operation.

## Resolution

1. Review your Bulk Publish API request payload and verify the version value for each entry.
2. Retrieve the current version of the entry using the Management API: GET /v3/content_types/[your-content-type-uid]/entries/[your-entry-uid].
3. Update your Bulk Publish request to use the correct version number matching the actual entry version.
4. Re-run the Bulk Publish request and check the response to confirm the affected locale is now included in the publish queue.
5. If the issue persists, capture the complete API request payload, the full API response body, the affected entry UID, locale, and version number used.

## Verification

After completing these steps, verify that the affected locale appears as published in the target environment. Escalate with the request payload, response body, entry UID, locale, and version number if the locale continues to be excluded from the publish queue.
