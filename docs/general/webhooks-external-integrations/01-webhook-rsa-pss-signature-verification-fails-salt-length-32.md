---
title: "Webhook RSA-PSS Signature Verification Fails With Documented Salt Length of 32"
slug: "webhook-rsa-pss-signature-verification-fails-salt-length-32"
pod: "General"
section: "Webhooks & External Integrations"
order: 1
meta_title: "Webhook RSA-PSS Signature Verification Fails With Salt Length 32 | Contentstack"
meta_description: "RSA-PSS verification of Contentstack webhook signatures can fail when using the documented default salt length of 32 bytes. Learn the correct salt length to use and how to fix verification failures in Java and other RSA-PSS implementations."
status: "draft"
source_case_id: "00058862"
contentstack_entry_uid: null
migrated_from: null
migrated_on: null
---

# Webhook RSA-PSS Signature Verification Fails With Documented Salt Length of 32

Verifying a Contentstack webhook payload signature with RSA-PSS using the documented default salt length of 32 can fail. This has been observed when implementing verification in a Java 21+ / Spring Boot 4 environment.

## Root cause

Root cause was not documented in the source case. The resolution below addresses the reported symptom. During troubleshooting, explicitly setting the PSS salt length to 222 instead of the documented default of 32 resolved the verification failure. This discrepancy has been reported to Contentstack's documentation and engineering teams, who are reviewing the documented default salt length.

## Resolution

1. When verifying the webhook signature, do not hardcode the RSA-PSS salt length to 32.
2. Configure your PSS verification parameters to use a salt length of 222 instead.
3. Locate the explicit salt-length parameter used by your PSS verification implementation and set it to 222 rather than relying on the default.
4. Re-run signature verification against a known webhook payload and its corresponding signature header to confirm the change resolves the failure.

## Verification

After completing these steps, resend or replay a webhook payload and confirm that signature verification succeeds using the salt length of 222 rather than 32. If verification still fails, capture the exact salt length your code is using and escalate with that detail plus a sample payload and signature header.
