---
title: "BrandKit Sync Fails Silently for Assets Larger Than 50MB"
slug: "brandkit-sync-fails-assets-larger-than-50mb"
pod: "General"
section: "API Delivery, GraphQL & Assets"
order: 7
meta_title: "BrandKit Sync Fails for Assets Larger Than 50MB | Contentstack"
meta_description: "BrandKit assets larger than 50MB may fail to sync into the asset library without any error message. Raise the sync connector's upload size limit to resolve it."
status: "draft"
source_case_id: "00099003"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# BrandKit Sync Fails Silently for Assets Larger Than 50MB

BrandKit assets larger than 50MB may fail to sync into the stack's asset library without displaying an error, making the sync appear successful even though some files never arrive.

## Root cause

The workspace's sync connector had a default upload size cap of 50MB that silently dropped larger files instead of erroring, so no failure was surfaced to the user.

## Resolution

1. Raise the sync connector's upload size limit in its configuration settings.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
