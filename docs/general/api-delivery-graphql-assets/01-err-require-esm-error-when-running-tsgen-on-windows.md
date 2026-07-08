---
title: "ERR_REQUIRE_ESM Error When Running tsgen on Windows"
slug: "err-require-esm-error-when-running-tsgen-on-windows"
pod: "General"
section: "API Delivery, GraphQL & Assets"
order: 1
meta_title: "Troubleshooting API Delivery, GraphQL & Assets | Contentstack"
meta_description: "Solutions for Contentstack CLI errors including ERR_REQUIRE_ESM module compatibility issues when running tsgen on Windows systems."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "General (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# ERR_REQUIRE_ESM Error When Running tsgen on Windows

Running npm run tsgen on a Windows system throws an ERR_REQUIRE_ESM error, preventing TypeScript type definition generation from completing.

## Root cause

The error occurs because an outdated version of the Contentstack CLI bundles an ES Module (ESM) version of the uuid package that is incompatible with the CommonJS require() call in @contentstack/cli-utilities. This incompatibility surfaces on Windows when the CLI version is not up to date.

## Resolution

1. Check the currently installed version of the tsgen plugin by running csdx plugins and locating the @contentstack/cli-tsgen entry.
2. Update the tsgen plugin to the latest version by running: csdx plugins:install @contentstack/cli-tsgen@latest
3. Verify the installed version shows v4.7.0 or higher after the update.
4. If updating the plugin alone does not resolve the issue, perform a full CLI reinstall: uninstall the existing Contentstack CLI, clear any related npm cache entries, and reinstall the CLI using the official installation instructions from the Contentstack documentation.
5. After the update or reinstall, run npm run tsgen again to confirm the ERR_REQUIRE_ESM error is resolved.

## Verification

After completing these steps, confirm that the tsgen command completes successfully and generates the expected TypeScript type definitions. Escalate with the CLI version, the Node.js version, the Windows OS version, and the full error output if the error persists after updating to the latest CLI version.
