---
title: "GraphQL Query Returns Null for Modular Block Field"
slug: "graphql-query-returns-null-modular-block-field"
pod: "SDK"
section: "API Delivery, GraphQL & Assets"
order: 2
meta_title: "GraphQL Query Returns Null for Modular Block Field | Contentstack"
meta_description: "A GraphQL query can return null for a modular block field when required fragment spreads for each block type are missing. Learn how to add the correct fragment spreads to resolve the field."
status: "draft"
source_case_id: "00099018"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# GraphQL Query Returns Null for Modular Block Field

A GraphQL query may return null for a modular block field even though the entry has content in that field.

## Root cause

The query was missing the required fragment spread for the modular block's specific block types, so the SDK couldn't resolve which fields to return.

## Resolution

1. Add the correct fragment spread for each block type used in the modular block field.
2. Confirm the query returns the expected content.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
