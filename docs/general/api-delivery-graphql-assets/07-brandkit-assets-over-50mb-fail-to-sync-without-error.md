---
title: "BrandKit Assets Over 50MB Fail to Sync Without Error"
slug: "brandkit-assets-over-50mb-fail-to-sync-without-error"
pod: "General"
section: "API Delivery, GraphQL & Assets"
order: 7
meta_title: "BrandKit Assets Over 50MB Fail to Sync Without Error | Contentstack"
meta_description: "BrandKit assets larger than 50MB can silently fail to sync into the stack's asset library. Learn how to raise the sync connector's upload size limit to fix it."
status: "draft"
source_case_id: "00099003"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# BrandKit Assets Over 50MB Fail to Sync Without Error

Syncing BrandKit assets larger than 50MB into the stack's asset library may fail silently, with no error shown to the user.

## Root cause

The workspace's sync connector had a default upload size cap of 50MB that silently dropped larger files instead of returning an error.

## Resolution

1. Raise the sync connector's upload size limit in its configuration settings.

## Verification

After completing these steps, confirm that assets larger than 50MB sync successfully into the asset library. If the issue persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
