---
title: "Node.js SDK Query Returns Empty Array for Entries That Exist in the CMS"
slug: "nodejs-sdk-query-empty-array-environment-mismatch"
pod: "SDK"
section: "Publishing, Releases & Environments"
order: 1
meta_title: "Node.js SDK Query Returns Empty Array Despite Existing Entries | Contentstack"
meta_description: "Learn why a Contentstack Node.js SDK query can return an empty array even when matching entries exist in the CMS, and how to fix it by aligning the query's environment parameter with the entry's published environment."
status: "draft"
source_case_id: "00099017"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# Node.js SDK Query Returns Empty Array for Entries That Exist in the CMS

Node.js SDK queries may return an empty array even though matching entries exist and are visible in the CMS UI, when the query's environment parameter does not match the environment where those entries are actually published.

## Root cause

The query was scoped to the "production" environment while the entries had only been published to "staging". Since the SDK only returns entries published to the specified environment, querying the wrong environment returns no results even though the entries exist and are visible in the CMS UI.

## Resolution

1. Update the SDK query's environment parameter to match the environment where the entries are actually published (e.g., "staging" instead of "production").

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.

<!-- diagnostic nudge -->
