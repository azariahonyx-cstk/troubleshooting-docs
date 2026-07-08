---
title: "XTM Translation App Experiences Intermittent Delivery Failures on Large Batches"
slug: "xtm-translation-app-experiences-intermittent-delivery-failures-on-large-batches"
pod: "Marketplace - Public Apps"
section: "Webhooks & External Integrations"
order: 1
meta_title: "Troubleshooting Webhooks & External Integrations | Contentstack"
meta_description: "Solutions for Marketplace app delivery failures, authentication errors, and integration issues including XTM translation app and Trados connector problems in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "Marketplace - Public Apps (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# XTM Translation App Experiences Intermittent Delivery Failures on Large Batches

The XTM Marketplace integration may experience intermittent delivery failures when processing large batch translation jobs involving multiple entries across multiple languages, with approximately 1 in 25 deliveries failing without automatic retries.

## Root cause

Three contributing causes have been identified: (1) The app lacks a retry mechanism with exponential backoff for HTTP 429 (rate limit exceeded) and transient 5xx responses — large batches can exhaust the Management API write rate limit. (2) Translated strings may be pushed into Enum fields (Error 119), which reject values that do not exactly match the pre-configured enum options. (3) Occasional 401 Unauthorized errors occur during entry retrieval for specific locale branches during the delivery callback.

## Resolution

1. If a delivery failure occurs, log in to XTM and manually trigger a redelivery for the failed job from the XTM project interface.
2. For recurring failures, verify whether any of the translated content targets Enum fields — confirm that translated values exactly match the pre-configured enum options for those fields.
3. To enable a deeper investigation of a fresh failure, collect the following details during the next occurrence and provide them to Contentstack Support: Entry UID, date and exact timestamp when the translation was triggered, source locale, target locale(s), XTM Project ID, XTM Project Name, and any delivery, failure, or reopen timestamps.
4. Contentstack Support can use these details to trace the complete delivery flow through the logs and confirm the specific root cause for your batch configuration.

## Verification

After completing these steps, confirm that the redelivery completes successfully. If failures continue to recur at a high rate, escalate with the details listed in step 3, along with your stack UID and the XTM app version installed in your Marketplace.
