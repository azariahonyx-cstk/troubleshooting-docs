---
title: "Error 194 When Updating Stack Settings via Management API Using cURL"
slug: "error-194-when-updating-stack-settings-via-management-api-using-curl"
pod: "CMS - CDA(Rest)"
section: "API Delivery, GraphQL & Assets"
order: 1
meta_title: "Troubleshooting API Delivery, GraphQL & Assets | Contentstack"
meta_description: "Solutions for Management API errors including Error 194 stack settings update failures and cURL request formatting issues in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - CDA(Rest) (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Error 194 When Updating Stack Settings via Management API Using cURL

Attempting to update a stack setting such as enforce_unique_urls via the Contentstack Management API using a cURL command returns Error 194 (Validation Error) even when the request appears to be correctly structured.

## Root cause

Extra whitespace characters (spaces) present after the backslash line-continuation characters in a multi-line cURL command cause the request to be malformed. When spaces appear between the backslash and the newline, the shell does not treat the backslash as a line continuation, which breaks the request structure and results in a validation error from the API.

## Resolution

1. Review the cURL command being used to update the stack setting and inspect each line that ends with a backslash continuation character.
2. Ensure there are no spaces between the backslash character and the end of the line — the backslash must be the very last character before the newline for line continuation to work correctly.
3. Remove any trailing spaces after the backslash characters throughout the command.
4. Re-run the corrected cURL command and verify that the response returns a 200 status and that the stack setting has been updated as expected.

## Verification

After completing these steps, confirm the stack setting reflects the updated value by fetching the stack details via a GET request to the Management API. If the error persists after removing trailing spaces, escalate with the full cURL command (with API keys replaced by [your-API-key]), the stack UID, and the complete error response body.
