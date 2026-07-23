---
title: "BrandKit Sync Fails Silently for Assets Larger Than 50MB"
slug: "brandkit-sync-fails-assets-larger-than-50mb"
pod: "General"
section: "API Delivery, GraphQL & Assets"
order: 7
meta_title: "BrandKit Sync Fails for Assets Larger Than 50MB | Contentstack"
meta_description: "Assets larger than 50MB may fail to sync into BrandKit's asset library without any error message. Learn how to raise the sync connector's upload size limit to resolve it."
status: "draft"
source_case_id: "00099003"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# BrandKit Sync Fails Silently for Assets Larger Than 50MB

BrandKit assets larger than 50MB may fail to sync into the stack's asset library, with no error message shown to indicate the failure.

## Root cause

The workspace's sync connector enforced a default upload size cap of 50MB. Files exceeding this limit were silently dropped during sync instead of returning an error, so the failure was not visible to the user.

## Resolution

1. Raise the sync connector's upload size limit in its configuration settings to accommodate assets larger than 50MB.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
