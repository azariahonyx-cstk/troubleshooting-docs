---
title: "Custom Field Stops Persisting Data After App SDK Upgrade"
slug: "custom-field-stops-persisting-data-after-app-sdk-upgrade"
pod: "CMS - UI"
section: "Custom Extensions, Live Preview & Analytics"
order: 2
meta_title: "Troubleshooting Custom Extensions, Live Preview & Analytics | Contentstack"
meta_description: "Solutions for custom extension integration failures, App SDK regressions, and data persistence issues for custom UI Location fields in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - UI (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Custom Field Stops Persisting Data After App SDK Upgrade

A custom UI Location field that was working correctly may suddenly fail with a "Field not found" error after an App SDK version update, causing field values to stop being saved or displayed.

## Root cause

A regression was introduced in App SDK v2.4.0 that affects data persistence for custom fields in certain configurations. The regression causes the SDK to fail to correctly bind field state, resulting in the field becoming non-functional for data storage.

## Resolution

1. Check the App SDK version currently being consumed by your custom application by reviewing the application's package.json or dependency configuration.
2. If the installed version is v2.4.0, downgrade the App SDK to v2.3.0 by updating the dependency in your application's package configuration and redeploying.
3. Verify that the custom field resumes normal behavior — specifically that field values are correctly saved and displayed — after pinning to v2.3.0.
4. Monitor the Contentstack Marketplace or App SDK changelog for a release that addresses the v2.4.0 regression, and update to that version once it is available.

## Verification

After completing these steps, confirm that the custom field persists data correctly and that the "Field not found" error no longer appears. Escalate with the App SDK version, the custom app configuration details, the affected stack UID, and browser console errors if the issue persists after downgrading.
