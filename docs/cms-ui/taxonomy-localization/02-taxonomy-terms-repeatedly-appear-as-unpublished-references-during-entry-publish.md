---
title: "Taxonomy Terms Repeatedly Appear as Unpublished References During Entry Publish"
slug: "taxonomy-terms-repeatedly-appear-as-unpublished-references-during-entry-publish"
pod: "CMS - UI"
section: "Taxonomy & Localization"
order: 2
meta_title: "Troubleshooting Taxonomy & Localization | Contentstack"
meta_description: "Solutions for taxonomy-related publish failures and localization issues when publishing entries to child locales in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - UI (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Taxonomy Terms Repeatedly Appear as Unpublished References During Entry Publish

Publishing an entry using the "Send with References" option may cause taxonomy terms to repeatedly appear as unpublished references, triggering unnecessary republish and CDN purge operations on every entry publish. Additionally, publishing localized entries may fail when a taxonomy field's publish validation requires terms to be explicitly localized to the target locale rather than falling back automatically from the master locale.

## Root cause

A platform enhancement introduced stricter validation for taxonomy references across locales. Taxonomy terms referenced in an entry must be explicitly localized to the target locale before publishing succeeds in that locale — delivery-side fallback (include_fallback=true) only applies at content delivery time, not at publish time. Separately, the "Send with References" publish flow by default includes taxonomy items and taxonomy terms as references, causing them to be automatically republished and CDN-purged whenever the related entry is published.

## Resolution

1. For publish failures in child locales: Navigate to the Taxonomy section, open the taxonomy referenced in the failing entry, select the relevant taxonomy terms, and localize them to the required target locale. Ensure both the taxonomy and its individual terms are localized before retrying the publish.
2. For taxonomy terms repeatedly appearing in "Send with References" operations: Contact Contentstack Support with your organization UID, stack UID, and a description of the repeated taxonomy publish behavior. Support can apply a backend configuration change to exclude taxonomy items and terms from the "Send with References" automatic publish flow for your organization.
3. After the backend configuration is applied, verify that taxonomy terms no longer appear in the referenced items list during subsequent entry publishes and that CDN purges are triggered only for intended content updates.

## Verification

After completing these steps, confirm that localized entries publish successfully and that taxonomy terms are excluded from automatic "Send with References" operations. Escalate with your stack UID, the taxonomy name, the affected locale codes, and publish queue error messages if the issue persists.
