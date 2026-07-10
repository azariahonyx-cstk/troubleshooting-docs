---
title: "CDP Audience Segment Updates Delayed 4-6 Hours in Destination Connector"
slug: "cdp-segment-sync-delayed-batch-vs-streaming-connector-mode"
pod: "General"
section: "Webhooks & External Integrations"
order: 2
meta_title: "CDP Segment Sync Delayed by Hours | Contentstack"
meta_description: "Learn why CDP audience segment updates may take hours to sync to a destination activation channel and how switching the connector to streaming sync resolves the delay."
status: "draft"
source_case_id: "00090003"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# CDP Audience Segment Updates Delayed 4-6 Hours in Destination Connector

CDP audience segment updates may take 4-6 hours to reflect in a connected activation channel instead of syncing in near-real-time.

## Root cause

The destination connector was configured for daily batch sync rather than streaming sync.

## Resolution

1. Switch the destination connector's sync mode from batch to streaming.

## Verification

After completing these steps, confirm that segment updates begin reflecting in the destination channel within minutes rather than hours. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
