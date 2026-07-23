---
title: "BrandKit Assets Over 50MB Fail to Sync Silently"
slug: "brandkit-assets-over-50mb-fail-to-sync-silently"
pod: "BrandKit"
section: "API Delivery, GraphQL & Assets"
order: 1
meta_title: "BrandKit Assets Over 50MB Fail to Sync Silently | Contentstack"
meta_description: "BrandKit assets larger than 50MB can fail to sync into the asset library with no error shown. Learn the cause and how to raise the sync connector's upload size limit to fix it."
status: "published"
source_case_id: "00099003"
contentstack_parent_entry_uid: "blt65675af8d7e450b2"
contentstack_category_heading: "API Delivery, GraphQL & Assets"
migrated_from: null
migrated_on: null
---

# BrandKit Assets Over 50MB Fail to Sync Silently

BrandKit asset sync fails for files larger than 50MB, and no error is shown to indicate why the asset never appears in the stack's asset library.

## Root cause

The workspace's sync connector had a default upload size cap of 50MB that silently dropped larger files instead of returning an error, so no failure indication reached the user.

## Resolution

1. Raise the sync connector's upload size limit in its configuration settings.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
