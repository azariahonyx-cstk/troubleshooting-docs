---
title: "BrandKit Assets Over 50MB Fail to Sync Silently Without an Error"
slug: "brandkit-assets-over-50mb-fail-to-sync-silently"
pod: "General"
section: "API Delivery, GraphQL & Assets"
order: 7
meta_title: "BrandKit Sync Failing for Assets Larger Than 50MB | Contentstack"
meta_description: "Learn why BrandKit assets larger than 50MB may fail to sync into the stack's asset library without an error, and how to raise the connector's upload size limit to resolve it."
status: "draft"
source_case_id: "00099003"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# BrandKit Assets Over 50MB Fail to Sync Silently Without an Error

BrandKit assets larger than 50MB may fail to sync into the stack's asset library, with no error message displayed to indicate the failure.

## Root cause

The workspace's sync connector had a default upload size cap of 50MB that silently dropped larger files instead of returning an error.

## Resolution

1. Raise the upload size limit in the sync connector's configuration settings to accommodate assets larger than 50MB.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
