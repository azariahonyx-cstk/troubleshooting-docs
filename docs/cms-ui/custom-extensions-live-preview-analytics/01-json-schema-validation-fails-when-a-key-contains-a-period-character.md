---
title: "JSON Schema Validation Fails When a Key Contains a Period Character"
slug: "json-schema-validation-fails-when-a-key-contains-a-period-character"
pod: "CMS - UI"
section: "Custom Extensions, Live Preview & Analytics"
order: 1
meta_title: "Troubleshooting Custom Extensions, Live Preview & Analytics | Contentstack"
meta_description: "Solutions for custom extension integration failures, App SDK regressions, and data persistence issues for custom UI Location fields in Contentstack."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - UI (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# JSON Schema Validation Fails When a Key Contains a Period Character

Integrating a third-party form schema that includes a key name containing a period (.) character may cause JSON key validation errors in Contentstack.

## Root cause

Contentstack's JSON validation requirements conflict with schema keys that contain a period (.) character. Period characters in key names can be interpreted as path separators in Contentstack's internal validation logic, causing the schema to fail validation. A known example is a schema key named widget.type, which triggers this conflict.

## Resolution

1. Inspect the JSON schema being integrated for any key names that contain a period (.) character.
2. Confirm whether the third-party form provider has released a version that prevents period characters from appearing in newly generated schema key names — if using a recent version, newly created schemas may already avoid this pattern.
3. For existing schemas that still contain period characters in key names, update or regenerate the schema using a provider version that does not produce keys with period characters, or manually rename the affected keys.
4. Re-test the integration after updating the schema to confirm the validation error is resolved.

## Verification

After completing these steps, verify that the form schema loads without validation errors. If the issue persists with a schema that does not contain period characters in key names, escalate with the full JSON schema, the stack UID, and any browser console errors.
