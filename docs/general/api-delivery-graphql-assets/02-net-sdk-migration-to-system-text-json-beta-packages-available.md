---
title: ".NET SDK Migration to System.Text.Json \u2013 Beta Packages Available"
slug: "net-sdk-migration-to-system-text-json-beta-packages-available"
pod: "General"
section: "API Delivery, GraphQL & Assets"
order: 2
meta_title: "Troubleshooting API Delivery & Developer Tools | Contentstack"
meta_description: "Fix .NET SDK System.Text.Json migration issues and Contentstack MCP Server initialization failures in Slingshot."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "General Additions (Jun 28 2026)"
migrated_on: "2026-07-08"
---

# .NET SDK Migration to System.Text.Json – Beta Packages Available

Updating the Contentstack .NET SDKs to use System.Text.Json instead of Newtonsoft.Json requires migrating to the updated SDK versions. Beta packages are available for integration testing while the stable major version is being finalized.

## Root cause

Earlier versions of the Contentstack .NET SDKs relied on Newtonsoft.Json for JSON serialization. The updated beta versions replace this with System.Text.Json, requiring code changes to maintain compatibility.

## Resolution

1. Install and test the beta version of the SDK(s) relevant to your implementation from NuGet: Contentstack Utils .NET SDK contentstack.utils version 2.0.0-beta.1, Contentstack Delivery .NET SDK contentstack.csharp version 3.0.0-beta.1, and Contentstack Management .NET SDK contentstack.management.csharp version 1.0.0-beta.1.
2. Review the migration guides linked below for code changes required by each SDK.
3. Test the beta packages in a non-production environment and validate against your use cases.
4. Monitor the Contentstack release notes for the stable major version release announcement before upgrading production environments.

## Verification

After completing these steps, verify that your application compiles and runs correctly with the beta SDK and produces expected API results. Escalate with the error details and affected SDK version if you encounter compatibility issues during testing.

## See also

Migrate .NET Delivery SDK from Newtonsoft.Json to System.Text.Json — https://www.contentstack.com/docs/developers/sdks/content-delivery-sdk/dot-net/migrate-dotnet-delivery-sdk-from-newtonsoft.json-to-system.text.json | Migrate .NET Management SDK from Newtonsoft.Json to System.Text.Json — https://www.contentstack.com/docs/developers/sdks/content-management-sdk/dot-net/migrate-dotnet-management-sdk-from-newtonsoft.json-to-system.text.json
