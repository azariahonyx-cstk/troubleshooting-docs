---
title: "BrandKit Assets Don't Appear in the Entry Asset Picker"
slug: "brandkit-assets-not-appearing-in-asset-picker"
pod: "General"
section: "Content Editing & UI Workflows"
order: 2
meta_title: "BrandKit Assets Not Appearing in Asset Picker | Contentstack"
meta_description: "Learn why BrandKit assets may be visible in the BrandKit library but missing from the entry asset picker, and how linking the correct workspace to your stack resolves it."
status: "published"
source_case_id: "00090006"
contentstack_parent_entry_uid: "blt126bd9f8c6e8e9bb"
contentstack_category_heading: "Content Editing & UI Workflows"
migrated_from: null
migrated_on: null
---

# BrandKit Assets Don't Appear in the Entry Asset Picker

Accessing the entry asset picker may fail to display BrandKit assets even though those same assets are visible in the BrandKit library itself.

## Root cause

The assets were uploaded under a BrandKit workspace that was not yet linked to the stack being edited. Without that workspace-to-stack link, the asset picker cannot surface assets belonging to that workspace.

## Resolution

1. Link the correct BrandKit workspace to the stack under Settings.

## Verification

After completing these steps, confirm the BrandKit assets now appear in the entry asset picker. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
