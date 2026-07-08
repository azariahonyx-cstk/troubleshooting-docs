---
title: "Polaris AI Feature \u2014 Capabilities, Credit Allocation, and Data Compliance Overview"
slug: "polaris-ai-feature-capabilities-credit-allocation-and-data-compliance-overview"
pod: "Marketplace - Public Apps"
section: "Content Editing & UI Workflows"
order: 1
meta_title: "Troubleshooting Content Editing & UI Workflows | Contentstack"
meta_description: "Common questions and guidance on using Polaris AI features, including capabilities, AI Credit allocation, and data compliance for Contentstack Marketplace apps."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "Marketplace - Public Apps (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Polaris AI Feature — Capabilities, Credit Allocation, and Data Compliance Overview

Questions about what the Polaris AI feature can do, how AI Credits are consumed, and whether customer content is shared or used for model training are common before enabling the feature for an organization.

## Root cause

Root cause was not documented in the source case. The resolution below addresses the reported symptom.

## Resolution

1. Use Cases: Content authors can use Polaris for drafting content, generating meta descriptions, creating social media snippets, and performing content gap analysis directly from within the entry editor. Developers can use Agent Builder for workflow automation, SEO audits, and approval trigger creation.
2. Pricing and Credit Allocation: Polaris is included in the Contentstack platform subscription — no separate license is required. AI Credit allocations vary by plan. Automate executions consume 150 credits each. Unused credits reset on the first day of each billing period and do not roll over. Contact your Customer Success Manager for your organization's specific allocation details and overage pricing.
3. Compliance and Data Handling: Prompts are stored in MongoDB with encryption at rest. Execution logs are retained for 90 days; prompt data in the analytics layer is retained for 60 days. Content is sent to the underlying LLM (OpenAI) for inference only — it is not used for model training.
4. Enabling Polaris: If Polaris is not yet enabled for your organization, contact Contentstack Support or your Customer Success Manager to initiate the activation process. Confirm the cloud provider (such as AWS or Azure) associated with your organization when requesting enablement.

## Verification

After completing these steps, confirm that Polaris is accessible from the entry editor and that AI Credit usage aligns with expectations. Escalate with your organization UID and a description of the specific capability or compliance concern if further clarification is needed from the Contentstack team.
