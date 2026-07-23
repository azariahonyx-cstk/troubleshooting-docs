---
title: "Academy Certificate Download Returns 403 Forbidden Error"
slug: "academy-certificate-download-403-error"
pod: "Academy"
section: "Authentication & Login"
order: 1
meta_title: "Academy Certificate Download Returns 403 Forbidden | Contentstack"
meta_description: "Learn why an Academy course-completion certificate download link may return a 403 Forbidden error and how to resolve it by regenerating the link under the correct org."
status: "draft"
source_case_id: "00099006"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# Academy Certificate Download Returns 403 Forbidden Error

Downloading an Academy course-completion certificate may return a 403 Forbidden error when the certificate link was generated while logged into a different Contentstack org than the one the enrollment belongs to.

## Root cause

The certificate link had been generated while logged into a different Contentstack org than the one the Academy enrollment was under, so the download request didn't match the enrollment's access scope.

## Resolution

1. Log out of the current Contentstack org.
2. Log back in under the org where the Academy enrollment is registered.
3. Regenerate the certificate link from the Academy dashboard.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
