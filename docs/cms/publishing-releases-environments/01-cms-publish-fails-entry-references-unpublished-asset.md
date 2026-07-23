---
title: "CMS Publish Fails Silently When Entry References an Unpublished Asset"
slug: "cms-publish-fails-entry-references-unpublished-asset"
pod: "CMS"
section: "Publishing, Releases & Environments"
order: 1
meta_title: "CMS Publish Fails Silently When Entry References an Unpublished Asset | Contentstack"
meta_description: "An entry may fail to publish without a clear error when it references an unpublished image asset. Learn how to identify the unpublished asset and resolve the publish failure."
status: "draft"
source_case_id: "00099015"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# CMS Publish Fails Silently When Entry References an Unpublished Asset

Publishing an entry may fail without a clear error message when the entry references an image asset that hasn't been published yet.

## Root cause

The CMS silently blocks publishing entries that reference unpublished assets, without surfacing which asset was the cause.

## Resolution

1. Check each referenced asset's publish status individually to identify the unpublished asset.
2. Publish that asset first.
3. Confirm the entry publishes successfully afterward.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.

<!-- diagnostic nudge -->
