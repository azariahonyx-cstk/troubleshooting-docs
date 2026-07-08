---
title: "Live Preview Fails After Implementing Contentstack Live Preview with a CloudFront Failover Configuration"
slug: "live-preview-fails-after-implementing-contentstack-live-preview-with-a-cloudfron"
pod: "Launch"
section: "Custom Extensions, Live Preview & Analytics"
order: 1
meta_title: "Troubleshooting Custom Extensions, Live Preview & Analytics | Contentstack"
meta_description: "Solutions for Live Preview failures on Contentstack Launch, including CloudFront failover routing conflicts causing SDK errors and deployment queue issues."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "Launch (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Live Preview Fails After Implementing Contentstack Live Preview with a CloudFront Failover Configuration

Implementing Contentstack Live Preview on a Next.js project hosted on Contentstack Launch may result in deployments appearing stuck in a queued state and Live Preview loading inconsistently, with intermittent SDK-related errors in the browser console.

## Root cause

A CloudFront failover routing configuration using a failover cookie was causing Next.js static assets to be served from a backup S3 origin instead of the active staging origin during Live Preview sessions. This routing mismatch prevented the Live Preview SDK from loading correctly, resulting in Live Preview failures and intermittent errors. The issue is environment-specific and originates from the customer-managed routing configuration rather than the Contentstack platform itself.

## Resolution

1. Review your CloudFront distribution configuration and identify whether a failover routing rule or a failover cookie is in use for your staging environment.
2. Determine whether the failover behavior could redirect Contentstack Live Preview requests — specifically the fetching of Next.js static assets — to a secondary or backup origin.
3. Update the staging environment's CloudFront routing logic to bypass or exclude failover behavior specifically for requests associated with the Contentstack Live Preview flow.
4. Redeploy the application after updating the routing configuration.
5. Verify that Live Preview loads consistently and that no SDK-related errors appear in the browser console after the routing fix is applied.

## Verification

After completing these steps, confirm that Live Preview functions as expected across multiple page loads and content edits. If the issue persists after adjusting the CloudFront routing, escalate with your stack UID, the Launch environment name, the CloudFront distribution configuration details, and browser console error logs.
