---
title: "Webhook RSA-PSS Signature Verification Fails Using Documented Salt Length of 32"
slug: "webhook-rsa-pss-signature-verification-fails-salt-length-32"
pod: "General"
section: "Webhooks & External Integrations"
order: 1
meta_title: "Webhook RSA-PSS Signature Verification Fails With Salt Length 32 | Contentstack"
meta_description: "Contentstack webhook signature verification using RSA-PSS with the documented salt length of 32 can fail, especially on Java 21+ and Spring Boot 4. Learn the correct salt length to use and how to fix verification."
status: "draft"
source_case_id: "00058862"
contentstack_entry_uid: null
migrated_from: null
migrated_on: null
---

# Webhook RSA-PSS Signature Verification Fails Using Documented Salt Length of 32

Verifying Contentstack webhook payload signatures with RSA-PSS using the documented default salt length of 32 can fail, particularly in Java 21+ / Spring Boot 4 environments where the cryptography provider strictly validates PSS parameters.

## Root cause

Root cause was not documented in detail in the source case beyond the empirical finding below. The resolution addresses the reported symptom: the actual RSA-PSS salt length used to sign the webhook payload does not match the salt length of 32 published in the documentation. For a 2048-bit RSA signing key with a SHA-256 digest, the maximum salt length permitted under the PKCS#1 v2.2 PSS scheme (RSA modulus size in bytes minus hash length minus 2) works out to 222 bytes. Some cryptography libraries compute or tolerate the salt length flexibly during verification, but Java 21+ and Spring Boot 4's default providers require the exact salt length used at signing time, so hard-coding the documented value of 32 causes verification to fail.

## Resolution

1. In your webhook signature verification code, configure RSA-PSS verification to use a salt length of 222 bytes instead of the documented value of 32.
2. In Java, build the verification parameters explicitly rather than relying on defaults, for example: `new PSSParameterSpec("SHA-256", "MGF1", MGF1ParameterSpec.SHA256, 222, 1)`.
3. Re-run signature verification against a known webhook payload and confirm it now succeeds.
4. If your signing key size is not 2048 bits, recompute the correct salt length as `(modulusSizeInBytes - hashLengthInBytes - 2)` and use that value instead of 222.

## Verification

After completing these steps, trigger a test webhook delivery and confirm the signature verification code completes without throwing an exception or rejecting the payload. If verification still fails, escalate with the RSA key size and hash algorithm used for signing, along with your JDK and Spring Boot versions, so the discrepancy can be reproduced.
