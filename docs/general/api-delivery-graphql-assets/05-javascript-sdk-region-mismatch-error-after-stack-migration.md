---
title: "JavaScript SDK Throws Region Mismatch Error After Migrating Stack to EU Region"
slug: "javascript-sdk-region-mismatch-error-after-stack-migration"
pod: "General"
section: "API Delivery, GraphQL & Assets"
order: 5
meta_title: "JavaScript SDK Region Mismatch Error After Stack Migration | Contentstack"
meta_description: "Learn why the JavaScript Delivery SDK throws a region mismatch error after migrating a stack to a new region, and how to fix it by updating the SDK's region configuration."
status: "published"
source_case_id: "00090004"
contentstack_parent_entry_uid: "blt126bd9f8c6e8e9bb"
contentstack_category_heading: "API Delivery, GraphQL & Assets"
migrated_from: null
migrated_on: null
---

# JavaScript SDK Throws Region Mismatch Error After Migrating Stack to EU Region

JavaScript Delivery SDK calls may fail with a region mismatch error after a stack is migrated to the EU region.

## Root cause

The SDK initialization code still referenced the default US region host, which no longer matched the stack's actual region after the migration.

## Resolution

1. Update the SDK's region configuration parameter in your initialization code to match your stack's actual region.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
