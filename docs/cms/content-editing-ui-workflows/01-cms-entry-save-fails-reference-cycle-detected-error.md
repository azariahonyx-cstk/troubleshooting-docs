---
title: "CMS Entry Save Fails with \"Reference Cycle Detected\" Error"
slug: "cms-entry-save-fails-reference-cycle-detected-error"
pod: "CMS"
section: "Content Editing & UI Workflows"
order: 1
meta_title: "CMS Entry Save Fails with \"Reference Cycle Detected\" Error | Contentstack"
meta_description: "Saving an entry may fail with a reference cycle detected error when two entries reference each other through the same field. Learn how to restructure the reference to resolve it."
status: "published"
source_case_id: "00099014"
contentstack_parent_entry_uid: "blt930aa025508bb411"
contentstack_category_heading: "Content Editing & UI Workflows"
migrated_from: null
migrated_on: null
---

# CMS Entry Save Fails with "Reference Cycle Detected" Error

Saving an entry may fail with a "Reference cycle detected" error when two entries are linked to each other through the same reference field.

## Root cause

The content model allowed entry A to reference entry B and entry B to reference entry A through the same field, creating a circular reference. The CMS correctly refuses to save entries in this state.

## Resolution

1. Restructure the relationship to use a one-directional reference instead of a bidirectional one.
2. Handle the reverse link through a separate lookup field.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
