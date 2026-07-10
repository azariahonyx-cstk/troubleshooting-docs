---
title: "Webhook RSA-PSS Signature Verification Fails with Documented Salt Length 32"
slug: "webhook-rsa-pss-signature-verification-fails-salt-length-32"
pod: "General"
section: "Webhooks & External Integrations"
order: 1
meta_title: "Webhook RSA-PSS Signature Verification Fails with Salt Length 32 | Contentstack"
meta_description: "Webhook RSA-PSS signature verification can fail when using the documented default salt length of 32 in Java 21+/Spring Boot 4 environments. Learn the workaround."
status: "published"
source_case_id: "00058862"
contentstack_entry_uid: "blt3898d9637b6061b6"
migrated_from: null
migrated_on: null
---

# Webhook RSA-PSS Signature Verification Fails with Documented Salt Length 32

Webhook RSA-PSS signature verification fails when using the documented default salt length of 32, particularly in Java 21+/Spring Boot 4 environments.

## Root cause

Root cause was not documented in the source case. The resolution below addresses the reported symptom.

## Resolution

1. Explicitly set the RSA-PSS signature verification salt length to 222 instead of the documented default value of 32.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
