---
title: "CLI Export Fails with \"Too Many Open Files\" Error on Large Stacks"
slug: "cli-export-fails-too-many-open-files-error-large-stacks"
pod: "General"
section: "API Delivery, GraphQL & Assets"
order: 4
meta_title: "CLI Export Fails with \"Too Many Open Files\" Error | Contentstack"
meta_description: "Learn why a CLI export of a large stack can fail with a \"too many open files\" error and how raising the system's file-descriptor limit resolves it."
status: "draft"
source_case_id: "00090005"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# CLI Export Fails with "Too Many Open Files" Error on Large Stacks

Exporting a large stack via the CLI may fail midway with a "too many open files" system error when the stack contains a high volume of assets.

## Root cause

The machine's default file-descriptor limit was exceeded by the export process while handling the stack's asset volume, causing the export to fail partway through.

## Resolution

1. Raise the system's file-descriptor limit on the machine running the CLI export.
2. Re-run the export.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
