---
title: "Custom App URL Resolver Not Loading in Entry Editor"
slug: "custom-app-url-resolver-not-loading-in-entry-editor"
pod: "Launch"
section: "Custom Extensions, Live Preview & Analytics"
order: 2
meta_title: "Troubleshooting Custom Extensions & Live Preview in Launch | Contentstack"
meta_description: "Fix custom app URL resolver loading failures in Contentstack Launch."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "Launch Additions (Jun 28 2026)"
migrated_on: "2026-07-08"
---

# Custom App URL Resolver Not Loading in Entry Editor

A custom application's URL resolver fails to load when accessed within the Contentstack Entry Editor, resulting in a blank or non-functional panel where the app should appear.

## Root cause

Root cause was not documented in the source case. The observed behavior suggests the app may have been configured with a UI Location that conflicts with how the Entry Editor renders custom app panels.

## Resolution

1. Open your custom app configuration in the Contentstack Developer Hub.
2. Review the UI Locations assigned to the app and verify that the URL resolver is not assigned to a rendering location that conflicts with the Entry Editor (for example, an incorrectly registered sidebar extension type).
3. Update the UI Location configuration to match the intended rendering context for the URL resolver.
4. Open the browser developer console while loading the Entry Editor and review any errors produced during App SDK initialization.
5. Capture and share App SDK initialization errors or JavaScript console errors with Contentstack Support for further diagnosis.

## Verification

After completing these steps, reload the Entry Editor and verify that the custom app URL resolver panel loads correctly. Escalate with the App SDK initialization errors, your app configuration details (from Developer Hub), and a screen recording of the blank panel if the issue persists.
