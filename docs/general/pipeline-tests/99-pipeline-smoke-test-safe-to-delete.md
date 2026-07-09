---
title: "Pipeline Smoke Test Article - Safe to Delete"
slug: "pipeline-smoke-test-safe-to-delete"
pod: "General"
section: "Pipeline Tests"
order: 99
meta_title: "Pipeline Smoke Test | Contentstack"
meta_description: "Dummy article used to verify the docs publishing pipeline end to end. Not customer content."
status: "draft"
source_case_id: null
contentstack_entry_uid: null
migrated_from: null
migrated_on: null
---

# Pipeline Smoke Test Article - Safe to Delete

This is a dummy article created to verify the GitHub-to-Contentstack publishing pipeline. It exercises the same path a real generated article will take: branch, PR, CI validation, merge, and publish workflow.

## Root cause

Not applicable. This article exists only to test the pipeline (TD-5299).

## Resolution

1. Open a pull request containing this article and confirm the Validate articles workflow passes.
2. Merge the pull request to main.
3. Confirm the Publish to Contentstack workflow runs in dry-run mode and logs the entry payload it would send.
4. Delete this article once the test is complete.

## Verification

After completing these steps, the Actions tab shows a green Validate run on the PR and a green dry-run Publish run on main. No Contentstack entry is created while PUBLISH_LIVE is unset.
