---
title: "Academy Course Progress Not Saving in Private/Incognito Browsing Mode"
slug: "academy-course-progress-not-saving-incognito-mode"
pod: "General"
section: "Authentication & Login"
order: 5
meta_title: "Academy Course Progress Not Saving in Incognito Mode | Contentstack"
meta_description: "Contentstack Academy course progress can reset between sessions when using a private or incognito browser window. Learn why this happens and how to fix it."
status: "draft"
source_case_id: "00090007"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# Academy Course Progress Not Saving in Private/Incognito Browsing Mode

Course progress in Contentstack Academy may reset between sessions when accessing the platform in a private or incognito browser window.

## Root cause

Progress tracking in Contentstack Academy relies on a cookie to persist state across sessions. Accessing the Academy in a private or incognito browser window prevents this progress-tracking cookie from persisting, which causes course progress to reset between sessions.

## Resolution

1. Exit the private/incognito browser window and access Contentstack Academy using a standard (non-private) browser session.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
