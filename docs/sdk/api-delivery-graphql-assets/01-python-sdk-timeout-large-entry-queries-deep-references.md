---
title: "Python SDK Times Out on Large Entry Queries with Deep Reference Chains"
slug: "python-sdk-timeout-large-entry-queries-deep-references"
pod: "SDK"
section: "API Delivery, GraphQL & Assets"
order: 1
meta_title: "Python SDK Times Out on Large Entry Queries | Contentstack"
meta_description: "Learn why Python SDK queries with deep reference chains can time out and how increasing the client timeout configuration resolves the issue."
status: "published"
source_case_id: "00099008"
contentstack_parent_entry_uid: "bltef47181f70dc4e80"
contentstack_category_heading: "API Delivery, GraphQL & Assets"
migrated_from: null
migrated_on: null
---

# Python SDK Times Out on Large Entry Queries with Deep Reference Chains

Python SDK queries fail with a timeout error when resolving entries that contain a large number of referenced fields.

## Root cause

The SDK client was initialized with the default 10-second timeout, which was too short for queries resolving deep reference chains.

## Resolution

1. Increase the SDK client's timeout configuration from the default 10 seconds to 30 seconds.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
