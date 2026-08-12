---
title: "CLI Troubleshooting Guides"
description: "Discover answers to common troubleshooting questions about CLI."
url: "https://www.contentstack.com/docs/headless-cms-cli-troubleshooting/faqs"
product: "Contentstack"
doc_type: "guide"
audience:
  - developers
  - admins
version: "current"
last_updated: "2026-07-28"
---

# CLI Troubleshooting Guides

## Authentication, Network & Node.js Environments

### Troubleshooting CLI Login Error with Node.js  link

CLI authentication fails with a "Login Error {}" response despite the web portal authentication succeeding.

**Root Cause**

A compatibility issue exists between the Contentstack CLI and Node.js versions 22.13.1 and 22.14.1, which causes authentication failures.

**Resolution**

1.  Verify your current Node.js version using the command node -v.
2.  Downgrade to Node.js 20.18.
3.  Re-attempt your CLI login.

CLI authentication completes successfully after downgrading to the supported Node.js version. After completing these steps, attempt to authenticate into the CLI again. If the issue persists, escalate with your CLI version and current environment details.

### Resolving Self-Signed Certificate Errors During CLI SSO Login

A "self-signed certificate in certificate chain" error occurs during CLI authentication via SSO, preventing successful login.

**Root Cause**

The error is caused by a failure in the environment-side trust path, typically resulting from corporate proxies, SSL inspection, or missing enterprise root Certificate Authorities (CAs).

**Resolution**

1.  Work with your internal IT or security team to add the enterprise root CA certificate to your system's trusted store.
2.  Alternatively, as a temporary workaround, disable SSL verification by running the command: npm config set strict-ssl false.

Authentication proceeds successfully once the certificate trust path is established or SSL verification is temporarily disabled. After completing these steps, attempt the CLI login again. If the issue persists, escalate with your system's security configuration details and the specific error output.

### Resolving Environment-Specific CLI Login Failures

CLI authentication fails despite following official documentation, indicating an environment-specific configuration issue.

**Root Cause**

The failure is caused by local configuration, network policies, or system-level restrictions specific to the machine or network environment.

**Resolution**

1.  Verify the CLI version and login method being used.
2.  Test the login on a different machine to isolate the issue to your specific environment.
3.  If login succeeds on another device, work with your internal IT team to review local firewall rules, proxy configurations, enterprise network restrictions, and system-level authentication blocks.

CLI login functions as expected once environment-level network and security restrictions are resolved. After completing these steps, attempt the CLI login again. If the issue persists, escalate with your system's network configuration details and any error logs generated during the authentication process.

### Troubleshooting CLI Execution Failures on Node.js 22.2.0+

CLI command execution failures occur when running Contentstack CLI on Node.js versions higher than 22.2.0.

**Root Cause**

Specific incompatibilities exist between the Contentstack CLI and Node.js versions exceeding 22.2.0, which prevent commands from executing.

**Resolution**

1.  Verify your current Node.js version by running node -v.
2.  If you are running a version higher than 22.2.0, downgrade to Node.js 22.2.0 or a stable Long Term Support (LTS) version below it.
3.  Subscribe to the Contentstack CLI changelog to monitor updates and compatibility fixes.

CLI commands execute successfully once your environment is configured to a compatible Node.js version. After completing these steps, re-run your CLI commands to verify functionality. If errors persist, ensure your CLI is up to date and check the release notes for any newer compatibility patches.

### Troubleshooting Authentication Errors During CLI Stack Operations

CLI commands fail with authentication errors during stack operations.

**Root Cause**

The failure is caused by an invalid, expired, revoked, or incorrectly generated authentication token that lacks the necessary permissions to execute the requested command.

**Resolution**

1.  Verify that your current Management Token or authentication token is valid and has not expired.
2.  Generate a new Management Token if you suspect the existing token is invalid, revoked, or lacks necessary permissions.
3.  Update your CLI configuration with the new token using csdx auth:tokens:add.
4.  Re-run the command to confirm successful authentication.

CLI commands execute successfully once a valid token with appropriate permissions is configured. After completing these steps, attempt your stack operations again to verify that the authentication error is resolved. If the issue persists, ensure that the newly generated token has the correct scope and permissions assigned within the stack settings.

### Troubleshooting CLI Login Failures Due to VPN Interference

CLI authentication fails despite correct regional and account configurations, due to network interference from VPNs.

**Root Cause**

The failure is caused by VPN interference, which blocks authentication traffic, prevents proper network pathing, or enforces policies that prevent the CLI from connecting to the authentication service.

**Resolution**

1.  Verify that your configured Contentstack region matches your account settings.
2.  Ensure your CLI is updated to the latest available version.
3.  If authentication fails, temporarily disable your VPN to rule out network path or policy-based traffic blocks.

CLI authentication proceeds as expected once the VPN is disabled or the network path is cleared of interference. After completing these steps, attempt the CLI login again to verify the fix. If login still fails, inspect your firewall or corporate security settings for further network traffic restrictions.

### Rate Limit Errors During cm:stacks:clone

Rate limit exceeded errors occurred during cm:stacks:clone, resulting in an incomplete clone.

**Root Cause**

Export and import requests during clone already retry automatically: up to 3 attempts, with a randomized 3-8 second delay, on 401, 408, 422, and 429 responses. A rate limit error means these retries were exhausted under sustained throttling, not that no retry was attempted. Clone has no checkpoint or resume mechanism, so once retries are exhausted the whole clone stops. Cloning a subset of locales is not supported; the type flag only chooses structure-only vs. structure-with-content. Proxy-related connection errors (ECONNREFUSED, ETIMEDOUT, ENOTFOUND) are not retried and can produce a failure that looks identical to an exhausted rate limit.

**Resolution**

1.  Review the output for the specific module where export or import failed; the error means retries were already exhausted.
    
2.  If fewer locales are needed, clone all locales, then manually remove the unwanted ones. There is no flag to clone a subset directly.
    
3.  Space out large clone operations or run them during lower API-traffic periods.
    
4.  If failures happen immediately rather than after several seconds, check for a proxy configuration; proxy connection errors are not retried.

### CLI Hides Log Output During Migration Runs

Console log output was not visible while a migration was running.

**Root Cause**

The migration command uses an interactive display that redraws progress in place in a terminal session. console.log output written during that time can be overwritten by the next redraw. This only happens in an interactive terminal; piped or redirected output switches the CLI to plain, non-redrawing mode automatically. Error-level entries are also written to migration-logs/error.logs regardless of terminal mode, but this does not capture arbitrary console.log calls.

**Resolution**

1.  Redirect the command's output to a file or run it in a non-interactive context, for example: csdx cm:stacks:migration --file-path <path> -k <api-key> > migration.log. This is the reliable fix, since it changes the output mode rather than racing the display.
    
2.  If redirection isn't an option, add a leading newline to console.log statements in the migration script, for example: console.log('\\nMigration started...'). This reduces, but does not eliminate, the chance of output being overwritten.
    
3.  Check migration-logs/error.logs in the working directory for error-level entries as a partial fallback; it does not capture custom console.log output.

### Taxonomy Export Fails with "Access Denied" Using a Management Token Alias

A taxonomy export command using a management-token alias failed with "Access denied. Please check your permissions."

**Root Cause**

This message is the Management API's generic response for any HTTP 403, not a taxonomy- or version-specific error. Management-token aliases are a supported authentication method for taxonomy export. A 403 here is more often caused by the token lacking taxonomy read access or scope, the organization's plan not including taxonomies, the token predating taxonomy permissions on its role, or the alias pointing to a branch without taxonomy access, than by a CLI defect.

**Resolution**

1.  Confirm the management token's role includes taxonomy read access and that the token is scoped to the correct stack.
    
2.  Re-check the alias configuration with csdx auth:tokens to confirm it points at the intended stack and token.
    
3.  If permissions check out and a previous CLI version worked with no other change, downgrading (for example npm install -g @contentstack/cli@1.51.0) is a reasonable temporary workaround, not a confirmed fix.
    
4.  If the permissions check doesn't explain the failure, escalate to Contentstack support with the exact CLI version (csdx version), the full error response body, and the token's role and permissions.

### JavaScript Heap Out of Memory During Large Asset Migration

A large asset migration (roughly 5,354 assets across 554 folders, 5.53GB) consistently crashed at around 80% completion with a "JavaScript heap out of memory" error, even after raising the Node.js memory limit to 30GB.

**Root Cause**

Crashing well below a 30GB heap ceiling points to a memory-handling issue in the CLI's asset import process, not an under-provisioned heap. Default asset upload settings are already conservative (assetBatchLimit: 1, uploadAssetsConcurrency: 2, importFoldersConcurrency: 1). The import process loads the full list of assets and folder mappings into memory and keeps mapping data (asset-to-UID, URL, and folder maps) in memory for the life of the module's run; asset file bytes themselves are referenced by path rather than loaded into memory. The exact point at which memory use becomes unbounded has not been pinned down.

**Resolution**

1.  Build a custom upload script against the already-exported asset files instead of relying on the CLI's built-in asset import for this batch size.
    
2.  Limit request concurrency in the custom script to keep memory usage bounded.
    
3.  As a lighter alternative before a full custom script, try lowering assetBatchLimit, uploadAssetsConcurrency, and importFoldersConcurrency further via csdx cm:stacks:import --config <file>, and split the import into smaller runs. This has not been verified against this specific failure.

### Configuring a Custom Rate Limit for Bulk Publishing via CLI

CLI publishing limits were hit during large-scale bulk publish operations.

**Root Cause**

csdx config:set:rate-limit raises throughput for the CLI's core bulk publish commands (cm:entries:publish, cm:assets:publish, and related commands), which default to roughly 1 request per second. This must be configured for the organization before bulk publishing runs faster. It does not apply to the separate CLI Bulk Operations plugin (cm:stacks:bulk-entries / cm:stacks:bulk-assets), which controls its own throughput independently through rateLimit.requestsPerSecond and rateLimit.maxConcurrent in its own --config file.

**Resolution**

1.  Set a custom rate limit for the organization: csdx config:set:rate-limit --org <your\_org\_uid> --utilize <percentage> --limit-name bulkLimit. Start moderate and raise gradually.
    
2.  Confirm with csdx config:get:rate-limit. Reset to default with --default, or remove the custom configuration with csdx config:remove:rate-limit --org <your\_org\_uid>.
    
3.  If bulk publishing through the CLI Bulk Operations plugin instead, configure throughput through that command's own --config file (rateLimit.requestsPerSecond, rateLimit.maxConcurrent); config:set:rate-limit does not apply to it.
    
4.  If still rate-limited after raising the configured limit, request a plan-level rate limit increase from Contentstack, since no local configuration can exceed the organization's actual backend limit.

### CLI Stack Export Fails with "No Management Token Found on Given Alias"

CLI stack export failed with "No management token found on given alias" even though the token existed on the stack.

**Root Cause**

The token existed on the stack but was not registered in the CLI's local token store under that alias, so the CLI could not resolve it during export. This also occurs if the alias was later overwritten by a second auth:tokens:add call using the same alias with a different token, or if the alias was registered under a different CLI profile or user account than the one running the export. The token store is local to the machine and user profile, not read from the stack itself.

**Resolution**

1.  Register the token under the correct alias: csdx auth:tokens:add --management --alias <alias> --stack-api-key <stack\_api\_key> --token <management\_token>.
    
2.  Confirm registration: csdx auth:tokens.
    
3.  Re-run the export: csdx cm:stacks:export --stack-api-key <stack-api-key> --data-dir "<path>" --alias <alias>.

### Migration Tool Login Fails Due to Insufficient Org-Level Permissions

Login to the Contentstack migration tool failed, with no clear reason why access was being denied.

**Root Cause**

The migration tool requires Org-level Admin or Owner permissions. Admin access at the stack level alone, with only a Member role at the org level, blocks login. Logging in via the wrong region compounds the issue.

**Resolution**

1.  Ask your Org Admin or Owner to update your role to Admin or Owner at the organization level.
    
2.  Confirm you're logging in using the correct region for your organization (for example, AWS NA rather than Azure EU).
    
3.  Retry logging in to the migration tool.

### GUI Migration Tool Login Blocked by SSO Strict Mode

Login to the GUI migration tool was blocked because it requires a standard Contentstack username and password, and the organization uses SSO without a Contentstack password.

**Root Cause**

Organizations with SSO Strict Mode enabled prevent password-based logins entirely, which blocks access to the migration tool since it doesn't yet support SSO authentication.

**Resolution**

1.  Preferred: create a separate non-SSO user account with a standard password dedicated to migration tasks. This affects only that one account and doesn't change SSO enforcement for anyone else in the organization.
    
2.  Alternative, only if a separate account isn't workable: temporarily disable SSO Strict Mode so the user can set a standard password, then log in. This removes password-login enforcement organization-wide, not just for one user, so treat it as a temporary exception.
    
3.  If Strict Mode was disabled, re-enable it immediately once the migration work is complete.

## Migration, Cloning & Architecture

### Copy Content Types and Entries from One Stack to Another Using CLI Export/Import

The customer needed to copy content types and entry content from one stack to another and asked for the recommended approach to migrate content between stacks.

**Root Cause**

The supported approach is **CLI stack-to-stack migration**: export content from the **source** stack, then import it into the **target** stack. The customer needed confirmation of that pattern and a pointer to the canonical procedure rather than ad-hoc duplication of steps in the ticket.

**Resolution**

*   Explain at a high level that migration is handled with the **Contentstack CLI export → import** flow (with audit called out in the doc where relevant).
*   Redirect the customer to the [Migrate content between stacks using the CLI](/docs/headless-cms/migrate-content-between-stacks-using-the-cli) documentation for prerequisites, exact commands, and FAQs.

The target stack shows the expected **content types** and **entries**, and the customer confirms the migration matches what the guide describes for their scenario.

### Entry Version Numbers Mismatch After Stack Clone via Import/Export

After cloning a stack using CLI export/import, the customer observed that entry version numbers in the cloned stack did not match those in the original stack.

**Root Cause**

**Export/import recreates content** in the target stack; internal identifiers and version counters **often differ** from the source. That is expected when treating export/import as a **copy** workflow, not a byte-for-byte clone of all platform metadata.

**Resolution**

1.  Clarify that:
    *   export import recreates entries
    *   Original entry version history / sequencing is **not guaranteed** to match
2.  When stack-level cloning with richer parity is required, recommend **csdx cm:stacks:clone** (and validate the outcome in a non-production stack first).
3.  Do **not** promise identical version numbers unless verified for that customer’s workflow and CLI version.

### Moving Deeply Referenced Entries Between Stacks (Multi-Level References)

The customer needed to migrate entries with three-level nested references (e.g., Questionnaire → Question Bundle → Question) from one stack to another.

**Root Cause**

Stack-to-stack moves with **deep reference graphs** usually require **ordered export/import** (parents before children) and/or multiple passes; the CLI does not offer a single “migrate entire nested graph with one flag” for arbitrary models. **Roadmap statements belong in product documentation**, not as a fixed KB claim—point customers to current docs or PM for feature status.

**Resolution**

1.  Set expectations: plan dependency order and validation, not one-click full automation for arbitrary depths.
2.  Manually export:
    *   Referenced content types
    *   All referenced entries
3.  Import them into the target stack in correct dependency order.
4.  Revalidate reference relationships after import.

Referenced entries must be manually validated in the target stack to ensure:

*   All referenced entries exist
*   Reference fields are correctly populated
*   No broken relationships remain

### CLI Guidance for GCP NA to EU Migration

Customers requested clarification on CLI usage while migrating from GCP NA to the EU region.

**Root Cause**

No CLI error occurred. The case involved clarifying the correct CLI workflow for region-based migration.

**Resolution**

1.  Explain export process from source region stack.
2.  Explain import process into target region stack.
3.  Confirm proper API keys and region endpoints are used.
4.  Ensure region-specific stack credentials are configured correctly before running CLI commands.

### Stack Cloning Attempted via Export/Import Breaks Internal References

Users attempted stack cloning using export/import, but internal references did not function correctly afterward. They also asked whether stack cloning is possible via the Content Management API (CMA).

**Root Cause**

Export/import **may not preserve every reference and linking edge case** the way a dedicated clone workflow does; outcomes depend on modules imported and order. **CMA does not expose a single “clone entire stack” API** comparable to cm:stacks:clone—practical stack copies are usually CLI export/import, clone, or custom automation.

**Resolution**

1.  Clarify that one-shot “clone stack” via CMA alone is not the standard pattern.
2.  Recommend **csdx cm:stacks:clone** when full stack replication is the goal; validate references after any path.

### Asset Duplication During Production to Development Migration

During migration from Production to Development:

*   Huge number of assets were duplicated
*   Assets were recreated instead of linked

**Root Cause**

Likely incorrect reference handling configuration during migration. Further investigation required CLI parameters and configuration, but no additional details were provided.

**Resolution**

1.  Request:
    *   CLI command used
    *   Migration configuration
    *   Reference handling flags
2.  Validate whether duplication resulted from full asset import instead of linking behavior.

### Schema / Content Model Changes (Tooling Expectations)

The customer raised a platform capability gap: they wanted **declarative, framework-style schema migrations** (similar to SQL migration tools) for every content model change, with low operational risk.

**Root Cause**

Contentstack does not ship a **single built-in “schema migration framework”** that auto-generates and applies arbitrary model diffs like some SQL tools. **Operational migrations still exist**: teams use **csdx cm:stacks:migration** (migration scripts), **export/import of modules**, **CMA/scripts**, and environment promotion—plus RTE-focused helpers such as **cm:entries:migrate-html-rte** where applicable.

**Resolution**

1.  Align expectations: plan migrations; use scripts and staging stacks.
2.  Apply safe model-change practices:
    *   Plan/document model changes before implementation.
    *   Maintain a manual version history of content models (exported JSON / change logs).
    *   Prefer creating new fields over renaming existing fields (deprecate old field gradually).
3.  For mandatory fields:
    *   Plan a population strategy (defaults, editor guidance, or scripted backfill).
4.  Use available tooling to reduce risk:
    *   **csdx cm:stacks:migration** for scripted stack changes
    *   CLI export/import of content models (backup replication across environments)
    *   CMA scripts to apply controlled schema updates and bulk updates to entries
5.  Always validate changes in non-production environments before production rollout.

### Workflow Cannot Push Content Between Stacks (Use CLI Export/Import)

The customer asked whether authors can push content from one stack to another automatically through a workflow stage transition (as part of workflow).

**Root Cause**

**Product behavior (workflows):** Contentstack workflows do not support cross-stack content migration as an action tied to stage transitions. Cross-stack transfer is outside workflow capabilities.

**Resolution**

1.  Confirm that workflow actions cannot migrate content between stacks.
2.  Recommend supported approaches for stack-to-stack migration:
    *   CLI export import utilities (contentstack-export / contentstack-import workflows)
    *   Custom scripts (for controlled migration automation if needed)
3.  Position this as the standard supported method for cross-stack migration workflows.

### Assets Not Appearing After Migration Unless Republished

After migrating content between branches, the customer reported that assets were not visible on the frontend unless entries were manually republished. This created the impression that publishing was required post-migration for assets to render correctly.

**Root Cause**

This was not a universal publishing requirement from Contentstack. Based on the case notes, the customer’s workflow assumed that migrated entries must be republished for assets to become available.

Support confirmed that **publishing entries was not required** for assets to be usable post-migration **in their scenario**, and provided a workaround to avoid an unnecessary republish cycle.

**Resolution**

1.  Review the customer’s post-migration workflow where entries are being republished purely to “make assets appear.”
2.  Apply the workaround shared in the case: **proceed without republishing entries**, since republish was not required to make assets available in that use case.
3.  Ask the customer to repeat their validation steps (asset rendering/use) without republishing, and confirm if the behavior is consistent.

Assets are usable/visible post-migration **without requiring manual republishing** of entries in the validated case, and the customer is able to proceed with migration activity without the republish step.

### Migration, Cloning & Architecture Branch Merge Consumes Excessive Memory and Time: Use the - no-revert Flag

Merging branches on a large stack with significant data differences consumed roughly 12GB of memory and took a long time to complete.

**Root Cause**

The --no-revert flag controls whether a revert (backup) branch is created, but that creation happens server-side, not in the local CLI process, so it's unlikely to directly drive memory usage on the machine running the CLI. Status polling after a merge starts at a 5-second delay and increases by 1 second per attempt up to a 60-second cap, making a lightweight request each time; this is also unlikely to meaningfully affect memory. The more likely driver is that the CLI computes and holds the full difference between the base and compare branches in memory before the merge runs, regardless of whether --no-revert is passed. For a large stack, this diff computation is what scales with memory use.

**Resolution**

1.  Add --no-revert to skip server-side backup-branch creation: csdx cm:branches:merge ... --no-revert. This reduces overall merge time and server-side load, but does not reduce the memory the CLI itself uses to hold the branch diff, since that happens either way.
    
2.  If memory is the primary concern rather than time, there is currently no flag to limit or paginate the diff computation. Merging more frequently in smaller increments, so each diff is smaller, is the more directly supported way to lower memory use for this step.
    

Skipping the revert branch also means there is no automatic backup to roll back to, so plan your own backup strategy before merging without it.

### Rate Limit Exceeded During Query-Based Migration Import

"Rate Limit Exceeded" errors occurred while importing entries during a query-based content migration, resulting in incomplete reference mapping.

**Root Cause**

The retry behavior is not import-specific: any command against the Management API retries up to 3 times on 401, 408, 422, and 429 responses, with a randomized 3-8 second delay. The default import concurrency of 5 governs three separate settings - importConcurrency, fetchConcurrency, and writeConcurrency - with importConcurrency responsible for entry and reference-mapping writes. There is no --concurrency flag; these settings can only be changed through an external configuration file passed to --config.

**Resolution**

1.  Reduce import concurrency below the default of 5 using a configuration file, for example { "importConcurrency": 2 } passed as csdx cm:stacks:import --config <path/to/config.json> ....
    
2.  If rate limits affect modules other than entries, lower fetchConcurrency or writeConcurrency as well; these govern other modules' batching independently.
    
3.  If rate limits persist after reducing concurrency, request an increase to the organization's write limit.

### Import Content from a GitHub Repository Using the CLI Seed Command

Content needed to be imported directly from a GitHub repository into Contentstack.

**Root Cause**

The Seed command (csdx cm:stacks:seed) only imports content already in Contentstack's exported stack format, placed inside a folder named stack in the repository, with a GitHub Release created for it. The command downloads the latest release's tarball via the public GitHub API and runs it through the same import logic as cm:stacks:import. It reaches the GitHub REST API without an authentication header, so only public repositories work - no private repos or personal access tokens. It also fails if there's no stack folder or no published Release, even if the content itself is valid.

**Resolution**

1.  Export the source stack: csdx cm:stacks:export -A or csdx cm:stacks:export -a "management token".
    
2.  Create a public GitHub repository with a folder named stack inside it, and commit the exported content there.
    
3.  Create a GitHub Release on that repository - the Seed command downloads the latest release, not the latest commit.
    
4.  Run csdx cm:stacks:seed --repo "account/repository" to import. Use --stack-api-key for an existing stack, or --org and --stack-name to create a new one.

### Recommended Order for Migrating Content Types Between Stacks

The correct order for migrating content types and entries from one stack to another was unclear.

**Root Cause**

Migrating modules out of order can cause dependency failures, since content types may reference Marketplace App configurations or global fields that don't yet exist in the target stack. csdx cm:stacks:import applies the correct order automatically for a full import (no --module). That automatic sequencing is skipped when importing modules one at a time with --module, so the order must be followed manually in that case.

**Resolution**

1.  For per-module imports, follow this sequence: locales, environments, assets, taxonomies, extensions, Marketplace Apps, webhooks, global fields, content types, workflows, entries, labels, custom roles.
    
2.  Update and configure Marketplace Apps once imported, since content types import right after and may depend on their configuration.
    
3.  For a full import, running csdx cm:stacks:import without --module is sufficient - the CLI sequences modules internally.

### Migrating Entries Between Branches Using Migration Scripts

Entries needed to move from one branch to another within the same stack.

**Root Cause**

There's no single built-in "move branch" command. The migration script feature's built-in operations (creating or editing a content type or field) only cover content type and global field schema changes, not entries - moving entries requires a script that calls entry-level management operations directly. The --branch flag scopes a script to one branch, so a script copying entries between branches needs to open a second connection to the source branch itself.

**Resolution**

1.  Use migration scripts (csdx cm:stacks:migration) rather than looking for a built-in move-branch command.
    
2.  Refer to Contentstack's migration script documentation for structure and execution steps.
    
3.  Test against a non-production branch first before relying on it for production data.
    
4.  If the branch sync involves added or modified content types, run csdx cm:branches:merge first - it automatically generates ready-to-run entry migration scripts for the affected content types and prints the exact csdx cm:stacks:migration --multiple --file-path ... command to run them. This can be faster than writing a script from scratch when entry sync is tied to a content-type merge.

### Missing References After Export/Import or Clone: Resolving with Audit Fix

References were missing after export/import between stacks, and again after using the CLI clone command, with clone update failures showing no clear error messaging.

**Root Cause**

Entries reference other entries or content types by UID; if the referenced target doesn't exist in the target stack - deleted, not part of the exported module set, or pointing to a content type not in the field's reference\_to list - the reference breaks. cm:stacks:audit/cm:stacks:audit:fix (from @contentstack/cli-audit) check reference fields in the exported --data-dir folder, not the live target stack. cm:stacks:clone and cm:stacks:import both run this audit automatically before importing (unless --skip-audit is passed), which is why the same error class shows up across plain export/import and clone. A reference is flagged as broken the same way whether the target is fully missing or just not an allowed content type per reference\_to - and if a referenced module was excluded from export via --module/--content-types filters, the reference breaks purely from export scope, not data corruption.

**Resolution**

1.  Run csdx cm:stacks:audit:fix against the exported content directory (or let import/clone run it automatically).
    
2.  Import the corrected content into the target stack.
    
3.  Review the audit report at the printed path. Audit fix removes the invalid UID from the reference field rather than restoring the missing content - it prevents the import failure, not the underlying gap. If the referenced content should exist, locate or recreate it in the source data, then re-run the audit and import.

### Branch Merge Fails with Error Code 116 (Global Fields: Failed to Fetch Global Fields)

Merging branches failed with Error Code 116, "Global Fields: Failed to fetch global fields."

**Root Cause**

csdx cm:branches:merge doesn't implement merge logic itself - it sends a single API request and prints back whatever error comes from that call, including error 116. The only client-side error handling is a retry on HTTP 429 (rate limiting); the CLI does not inspect error code 116 specifically or evaluate field visibility rules on its own. The specific mechanism (an outdated field visibility rule migrating inconsistently between branches) is a stack/backend condition, not CLI behavior - the fix below is a confirmed workaround, but the CLI itself doesn't reveal why it works. Error 116 can surface from any transient failure fetching global fields during a merge, so it isn't necessarily specific to field visibility rules.

**Resolution**

1.  Review field visibility rules for global fields across the branches involved (a stack/content-type configuration step in the UI or Content Management API, not a CLI operation).
    
2.  Identify and manually remove the outdated field visibility rule in the main branch.
    
3.  Re-run csdx cm:branches:merge - it resends the request; the CLI doesn't retry or fix this automatically.

### Copying or Syncing Entries Between Branches (No Built-In Feature)

Copying or syncing entries, including localized versions and references, from one branch to another had no direct UI option.

**Root Cause**

There's no single built-in feature to copy or sync entries between branches outside manual UI actions. Bulk or reference-aware copying requires the Content Management API or the CLI, with custom scripting for localizations and references.

**Resolution**

1.  Single entry: copy manually via the UI, or use the Content Management API with a custom script to fetch each locale and recreate it in the target branch.
    
2.  Bulk copying: use the CLI to export from the source branch and import into the target branch - both cm:stacks:export and cm:stacks:import accept a --branch flag, so this is a genuinely supported flow. Alternatively, use the Content Management API with a custom script.
    
3.  Entries with references: copy referenced entries first, then the entries that reference them, using a UID-mapping table in a two-pass approach.
    
4.  If the entries belong to content types involved in a branch merge, csdx cm:branches:merge automatically generates ready-to-run entry migration scripts and prints the csdx cm:stacks:migration --multiple command to run them - the closest thing to a built-in entry-sync feature, though limited to content types involved in a merge.

### cm:branches:diff Shows a Field as Modified with No Visible UI Difference

Running cm:branches:diff to compare two branches showed a modification in a content type's field, but manually reviewing both branches in the UI showed no visible difference.

**Root Cause**

cm:branches:diff supports exactly two --format values: compact-text (the default) and detailed-text - there is no separate "summary" format. compact-text only lists which content types or global fields were added, deleted, or modified. detailed-text fetches a per-field comparison and renders field-level differences, a finer-grained diff than the coarse list. The CLI doesn't invent or compute extra metadata - it renders whatever the field-level comparison returns, which can include non-visual properties such as field order or internal attributes the standard schema UI doesn't render. Field reordering, or a difference in an attribute the comparison tracks but the UI doesn't display, can both produce this symptom.

**Resolution**

1.  When --format detailed-text reports a change with no visible UI difference, treat it as a field-level metadata difference rather than a CLI defect.
    
2.  If only the coarse added/deleted/modified list matters, use the default compact-text format (or omit --format entirely) instead of detailed-text.

### Cloning a Large Stack Runs Out of Disk Space

Cloning a large stack (entries and assets) consumed all available disk space and could not complete.

**Root Cause**

csdx cm:stacks:clone runs an export followed by an import, both executing locally through the same process as cm:stacks:export and cm:stacks:import. The export step writes the source stack's content types, entries, and assets to a local directory; only after that completes does the import step read the same directory and upload to the target stack, and the directory is deleted automatically once import finishes. For a large stack, the full set of entries and asset files must exist on local disk at once, which exhausts available space. Cloning via the Content Delivery or Content Management API directly isn't unsupported in the sense of the APIs being unavailable - clone already uses the Content Management API under the hood for both steps. What's actually missing is a streaming or in-memory clone path that skips writing to local disk before importing.

**Resolution**

1.  Confirm available local disk space before a large clone, or run it from a machine/volume with headroom for the full exported content.
    
2.  If entries and assets aren't needed, run csdx cm:stacks:clone --type a for structure-only cloning (all modules except entries and assets) - this is a supported flag, not a manual workaround, and avoids downloading asset files entirely.
    
3.  If both structure and content are needed but disk space is limited, clone structure with --type a first, then move entries and assets in smaller batches using cm:stacks:export/cm:stacks:import with --content-types or --branch filters.
    
4.  If none of the above works, replicate stack components manually as a last resort.

### Content Model Constraints - Title Field Cannot Be Made Non-Unique

Whether the title field on entries can be configured as non-unique was unclear.

**Root Cause**

The title field is unique by default and not configurable to allow non-unique values. This is enforced server-side as part of Contentstack's content model constraints, not by the CLI, so no CLI command, flag, or script can change or bypass it.

**Resolution**

No configuration change is available. If a non-unique display label is needed alongside a unique title, add a separate custom field for that purpose.

<!-- case:00059666 status:draft synced:false bucket:"Migration, Cloning & Architecture" -->
### cm:stacks:clone Hangs After "Audit Process Completed"

Cloning a stack with csdx cm:stacks:clone may stall indefinitely after the process displays "Audit process completed," never progressing to the import phase.

**Root Cause**

This is a known failure pattern in the clone workflow for certain stack configurations: the command completes the audit phase but hangs before it can start the import phase. Updating the CLI does not resolve it.

**Resolution**

1.  Export the source stack directly: csdx cm:stacks:export --stack-api-key [your-stack-uid] --data-dir <path>.
2.  Import the exported data into the destination stack: csdx cm:stacks:import --stack-api-key [your-stack-uid] --data-dir <path>.
3.  Use this two-step export/import approach in place of cm:stacks:clone - the import step does not run the audit phase, so it proceeds directly without the hang.

After completing the export and import steps, confirm the destination stack matches the source. If the clone completes without hanging at the audit phase, the issue is resolved. Escalate with your CLI version and stack configuration details if the export or import step itself fails.

<!-- end:00059666 -->

## Export/Import Commands & Data Formats

### CLI Import to New Locale Fails After Renaming Exported File

The customer wanted to import content into a new language (locale) and thought that simply renaming the exported content files would change their locale. However, after renaming the files, the import process failed. The customer asked for help to import content correctly into the intended new locale.

**Root Cause**

In this case, support observed an **incorrect locale identifier** (or mismatch with the stack’s configured locales) during the import workflow. Renaming files alone does not retarget locale. The failure was tied to locale configuration/format as used in the workflow, not necessarily a generic CLI defect.

**Resolution**

1.  Review the locale identifier the customer is using in the export/import workflow.
2.  Correct the locale format to match the stack’s configured locale format (the exact format used in the stack configuration).
3.  Re-run the import using the corrected locale format, following the same steps the customer was attempting.

The CLI import completes successfully after correcting the locale format, and the content is imported into the intended locale without error.

### CLI Import: Entries Imported but Assets Not Linked (Publish Failures)

Entries were imported successfully but failed to publish because linked assets were missing. Errors included:

Entry publishing failed. Please enter valid data.  
list\_no\_products\_found.images.0.image is a required field.

**Root Cause**

The import process included entries but did not include the **backup directory containing assets** (when assets are imported via the module/backup flow). As a result:

*   Entries were imported
*   Asset references existed
*   Actual asset files were not imported
*   Required asset fields failed validation during publish

**Resolution**

1.  Ensure the import directory includes:
    *   Entries
    *   Content types
    *   Assets (backup folder) per import flags (--module, --backup-dir as applicable)
2.  Re-run import including the full backup directory. Prefer long-form flags so behavior matches current CLI help, for example:

csdx cm:stacks:import --stack-api-key <stack-api-key> --data-dir "<path-to-export-data>" --module assets --backup-dir <backup-dir-name>

If a flag name differs on your install, run csdx cm:stacks:import --help and confirm with csdx --version.

1.  Retry publishing entries.

After including assets in the import process:

*   Entries publish successfully
*   Required image fields are populated
*   No publish validation errors occur

### Global Fields Import Fails: No Global Fields Found

Customer attempted to import global fields using:

csdx cm:stacks:import --stack-api-key <stack-api-key> --data-dir "<path-to-export-data>" --module global\-fields

Received error indicating no global fields were found.

**Root Cause**

The specified directory did not contain any global field definitions to import.

**Resolution**

1.  Verify directory structure.
2.  Confirm global-fields folder exists in export.
3.  Validate JSON files are present in target directory.
4.  Retry import.

No logs were received after follow-up.

Directory must contain valid global field definitions for import to succeed.

### Correct Command to Export Global Fields

Customers required the correct CLI command to export global fields.

**Root Cause**

Incorrect module parameter usage.

**Resolution**

Use:

csdx cm:stacks:export --stack-api-key <stack-api-key> --data-dir "path" --module global\-fields

Global fields export successfully to the specified directory.

### Bulk Content Download Before Account Termination (JSON/CSV)

Ahead of account termination, the customer requested a full export of their current content in **JSON/CSV** format for archiving and offboarding purposes.

**Root Cause**

This was not a CLI failure. The customer needed the correct, scalable method to export stack content in bulk prior to contract termination.

**Resolution**

1.  Confirm the scope of export needed (full stack content and/or specific modules like entries, assets, content types).
2.  For **full stack–style structured export**, use **csdx cm:stacks:export** (JSON/module folders as documented).
3.  For **CSV slices** (e.g. entries, taxonomies, users per command scope), use **csdx cm:export-to-csv** where it matches the need—**not** a drop-in replacement for entire-stack JSON export.
4.  Validate exported output locally to ensure completeness.

### CSV Import for Large Volume Content (CSV Not Natively Supported)

The customer explored whether they could import a large volume of entries using **CSV files**, beyond Contentstack’s standard **JSON import** capability.

**Root Cause**

Contentstack does not provide a direct “CSV → Entries” native import workflow in the CLI the way **cm:stacks:import** uses exported JSON modules. CSV ingestion requires transformation or external tooling.

**Resolution**

1.  Confirm that native stack import format for cm:stacks:import is the **exported JSON module layout** (supported workflow).
2.  Provide supported alternative approaches for CSV-based datasets:
    *   Convert CSV → JSON, then use CLI import.
    *   Use a custom script to transform CSV rows into entry payloads and push via APIs.
    *   Use third-party integration platforms to orchestrate transformation import.
3.  Recommend against manual entry for large volumes due to scalability and error risk.

### Exporting Asset Metadata for a Specific Folder Using the CLI

Asset metadata for a specific folder could not be exported using the CLI.

**Root Cause**

CS Assets, Contentstack's space-based asset management system, is now generally available. CS Assets requires a logged-in session; a management token cannot read linked workspace settings and silently falls back to the legacy assets export. Folder-level filtering is not supported at export time in either path.

**Resolution**

1.  If CS Assets is not enabled on the stack, run the standard export; folder structure and folder association are included by default.
    
2.  If CS Assets is enabled, export using a logged-in session, not a management token, so the CLI can read the linked workspace settings.
    
3.  Filter the exported data locally by folder association, since export-time folder filtering is not supported.
    
4.  Alternatively, fetch assets via the [Content Management API](/docs/developers/apis/content-management-api) and filter by folder-related metadata.
    

Folder and asset metadata are available for both legacy and CS Assets stacks once the correct authentication method is used.

**Note:** [csdx cm:stacks:clone](/docs/developers/cli/clone-a-stack) does not export or import CS Assets space-based assets; use export/import instead if cloning a CS Assets-enabled stack.

### Recommended Module Order for Bulk CLI Export and Import

CLI-exported entries and assets could not be successfully re-imported into a stack.

**Root Cause**

Modules do need a specific order for dependencies to resolve (for example, assets must exist before entries import). cm:stacks:import enforces this automatically for a full import (no --module flag) via a fixed internal module order. Manual ordering only matters when modules are imported one at a time with --module; the CLI does not re-order anything in that case. If module order is correct and a bulk re-import still fails, check for missing or mismatched management token scopes, or conflicting UIDs on locales or content types already in the destination stack.

**Resolution**

1.  Install the CLI: npm install -g @contentstack/cli (requires Node.js 22 or later).
    
2.  Generate management tokens and confirm access rights on both stacks.
    
3.  Run the export using the source stack's API key.
    
4.  Run the import using the destination stack's token and API key, pointing to the same export directory.
    
5.  For a full import (no --module), the CLI already sequences modules correctly. For per-module imports, use this order: locales, environments, assets, taxonomies, extensions, marketplace-apps, webhooks, global-fields, content-types, workflows, entries, labels, custom-roles.

### CLI Export Hangs for Large Content Types with Nested References

Exporting a large content type (~85,000 records with references and arrays) using csdx cm:export-to-csv appeared to hang indefinitely.

**Root Cause**

export-to-csv is not deadlocked; it fetches entries one page at a time (100 per request, sequential, no concurrency) and flattens nested references and arrays into individual columns. All flattened rows accumulate in memory, and the CSV is written only once, after every page is fetched. For ~85,000 records, that's roughly 850 sequential calls with growing memory use and no per-page progress output beyond a static loader message, making a slow but progressing export look identical to a hang.

**Resolution**

1.  Use csdx cm:stacks:export to export in JSON format instead; it paginates the same way but writes each page to disk as it's fetched and reports progress per entry.
    
2.  Include all referenced content types explicitly with --content-types.
    
3.  Convert the exported JSON to CSV afterward with a script, if CSV is still required.

### Custom Fields, References, or Locales Not Imported Correctly: Use import-setup First

After a CLI import, a custom field (implemented via a Developer Hub app) wasn't populated, one content type's reference fields weren't linked, localized content imported as separate full entries, and running without a backup directory dropped fields from the content model.

**Root Cause**

Running import-setup first is the fix, and it works because of how the CLI resolves its working content directory, not because the backup directory only stores mapping metadata. Confirmed across four import modules (global-fields, content-types, entries, extensions): once a backup directory exists - either an existing one passed via --backup-dir, or a fresh one the CLI auto-creates by copying the entire --data-dir export folder - the CLI reassigns its internal working path to that backup directory for the rest of the run, and every module reads its actual schema and entry content from there, not from the original --data-dir. Without --backup-dir, a new backup directory is created from scratch on every run, so cross-module UID mappings never persist between runs; import-setup generates one and keeps it in place instead.

This explains three of the four reported symptoms directly: fields dropped from the content model when no backup directory was specified, and locale/reference handling that depends on those same mappings existing consistently across runs. It does not fully explain a fourth symptom on its own - after switching to --module entries, the field reappeared in the model but its data still didn't populate. That points to a separate dependency: a custom field backed by a Developer Hub app needs the app itself correctly installed and mapped in the destination stack before its data will populate and render correctly, independent of whether the CLI import step touches the schema. Importing marketplace apps first, before the content types and entries that depend on them, addresses this.

**Resolution**

1.  Run setup first to generate a persistent backup directory: csdx cm:stacks:import-setup -k <stack\_api\_key> -d ./export/main --module entries.
    
2.  Import Marketplace Apps used by custom fields before importing the content types or entries that depend on them, so the app is installed and mapped in the destination stack first: csdx cm:stacks:import -k <stack\_api\_key> -d ./export/main --backup-dir ./\_backup\_123 --module marketplace-apps.
    
3.  Then import using that same backup directory, so mappings and content persist instead of resetting: csdx cm:stacks:import -k <stack\_api\_key> -d ./export/main --backup-dir ./\_backup\_123 --replace-existing --module entries.
    

If localized entries still appear as separate full entries, confirm the master-locale entry finished importing and was mapped before other locales were processed. If a custom field's data still doesn't populate after the app is installed and mapped, or if it populates but doesn't render correctly, check the app's configuration directly in the destination stack - this can be a display/rendering issue in the destination environment rather than an import defect. If a field is missing from the export data itself (for example, added directly in the destination after export), no combination of import-setup or --backup-dir resolves that. (Reference-linking issues specific to one content type required separate investigation - see the following article on reference UID mismatches.)

### References Not Populated in Parent Entries After Import: Reference UID Mismatch

Reference fields inside a specific content type's entries were not linked in the parent entries after export/import, even though the referenced entries imported successfully.

**Root Cause**

cm:stacks:import resolves references in two passes: it first creates entries and records old-to-new UID mappings in the backup directory, then rewrites reference fields by looking up each referenced UID in that mapping. If a referenced entry's old UID isn't in the mapping when the second pass runs, the reference can't resolve. This commonly happens when the referenced content type was imported in a separate run using a different (or no) --backup-dir, so its mapping never lands in the same mapping file the parent entries' update pass reads, or when some referenced entries failed to import and were logged as failures instead of mapped.

**Resolution**

1.  Confirm the referenced entries were created successfully; check the failed-entries log in the --backup-dir folder for that content type.
    
2.  Confirm the UID mapping file under --backup-dir contains an entry for each referenced UID. If the two content types were imported with different backup directories, re-import both using the same --backup-dir so their mappings live in one file.
    
3.  Follow Contentstack's [Update Missing Reference UIDs](/docs/headless-cms/update-missing-reference-uids) documentation: download the examples folder, and set mapper-path in config.json to the backup directory shown after a successful import (<path>/\_backup\_<number>/), with contentTypes listing the affected content type UIDs.
    
4.  Run the 05-Update-reference-entry-from-mapper script: csdx cm:stacks:migration --file-path ./05-Update-reference-entry-from-mapper.js --config-file ./config.json -k <stack\_ApiKey>.
    
5.  Validate the previously unlinked references now populate. If not, confirm the referenced entries still exist under the same UIDs recorded in the mapping - entries deleted and recreated outside the CLI won't match.

### Global Field Values Deleted During CLI Import: Two-Step Import Workaround

During a migration using cm:stacks:import with a backup directory from import-setup, a field inside a Global Field (implemented via a Marketplace App/Extension) was deleted from the destination stack's content model, affecting every content type that used the Global Field at once.

**Root Cause**

The CLI's import reads schema content, including global field definitions, from the backup directory once one exists for the run - not from the original --data-dir export folder directly, and not only mapping metadata as the checker feedback for this article claimed. If the backup directory's globalfields.json is missing a field that the destination stack's copy of that global field already has, and --replace-existing is used, the CLI performs a full schema replace for that global field using exactly what's in the backup directory, dropping the missing field everywhere the global field is used.

What isn't fully confirmed is why the field was missing from the backup directory's globalfields.json in the first place. The backup directory is a full copy made by import-setup at setup time, so a field genuinely absent from the source export would carry through as absent in the copy - that part is expected. What's unconfirmed is whether something in the setup or copy process itself can drop a field that was present in the original export data, or whether the field was already missing before import-setup ran (for example, because the field was added directly in the destination after export, or the source stack's app/extension wasn't fully synced at export time). This is the same category of custom-field dependency seen in the related import-setup article: a Marketplace App/Extension-backed field can go missing from schema data through paths the CLI import step itself doesn't control.

**Resolution**

1.  Import assets first: csdx cm:stacks:import ... --module=assets.
    
2.  Then import entries only: csdx cm:stacks:import ... --module=entries. Restricting to one module at a time means the global-fields import step never runs, so the existing global field schema in the destination is left untouched.
    
3.  If the global field schema needs editing directly, make the edit in the specific backup directory being used for that import run, before running with --replace-existing, and confirm you're pointing at that same directory rather than a newer one created by a fresh import-setup run - each import-setup run creates a new, separately-named backup directory copied fresh from the original export, so edits to an older one are silently bypassed.
    
4.  As a more direct fix for a full combined import: either drop --replace-existing (so existing global fields are never replaced) or confirm the export data used to build the backup directory actually contains the extension field before importing with --replace-existing - for example, by re-exporting from a source stack where the Marketplace App or Extension is confirmed installed.

### UI JSON Import Creates Only One Entry Even with Multiple Records in the File

Importing 500+ entries of the same content type using a single JSON file through the Contentstack UI's entry import option created only one empty entry.

**Root Cause**

This is expected behavior, not a bug. The Contentstack UI entry importer supports only a single entry per JSON file; it isn't designed for bulk multi-record import.

**Resolution**

1.  Use the Content Management API to programmatically create entries in bulk - the preferred approach for scalability.
    
2.  Alternatively, use the Contentstack CLI, which supports bulk import through a structured export/import format.

### Applications Renamed with a Suffix After Import (Duplicate Titles)

After importing a stack, all Marketplace app names had been renamed with an appended suffix, and many names were truncated.

**Root Cause**

When cm:stacks:import finds a Marketplace app name that already exists in the target stack, it generates a new name automatically: truncating the original (18 characters for the app name, up to 50 for UI location names) and appending a lozenge character (◈) followed by a numeric suffix, e.g. My App◈1. If a terminal or font can't render ◈, it falls back to a replacement character, which can look like "?1". This behavior is present in current CLI versions, not just an old release - there's no confirmation that upgrading alone changes it. Long names can also get truncated even without a naming conflict, once they're at or above the length threshold that triggers a suffix. Passing -y/--yes during import applies the suggested name automatically without the normal confirm/edit prompt.

**Resolution**

1.  Before importing, check the source stack for duplicate app titles and rename them to be unique, avoiding the conflict path entirely.
    
2.  Avoid -y when duplicate titles may be present, so the suggested name can be reviewed and edited via the interactive prompt.
    
3.  If a rename already happened, look for ◈ (it may render as "?" depending on terminal/font) followed by a number, and rename the app manually.
    
4.  Updating the CLI is general hygiene, but not confirmed to change this specific naming behavior, since it's present in current releases too.

### No Support for Custom Filtered Exports via CLI

A custom filtered view of entries could not be exported directly; only whole content types could be exported.

**Root Cause**

cm:stacks:export and cm:export-to-csv only select which content types to export, not which entries within one. The official Query Export Plugin (@contentstack/cli-cm-export-query) adds csdx cm:stacks:export-query, which exports content types matched by a query along with their dependencies and references. Only content-type-level queries are supported; there is no entry-level filtering within a content type, and asset-folder-level filtering is not supported either - all asset folders are always exported.

**Resolution**

1.  Install the plugin: csdx plugins:install @contentstack/cli-cm-export-query.
    
2.  Verify: csdx plugins.
    
3.  Run a query-based export, for example: csdx cm:stacks:export-query -a <alias> --query '{"modules":{"content-types":{"title":{"$in":\["Blog","Author"\]}}}}'. A query can also be stored in a JSON file and passed with --query ./my-query.json.
    
4.  Use --skip-references or --skip-dependencies to limit automatic dependency/reference export.
    
5.  For entry-level or folder-level filtering, export fully and filter the result afterward, since neither is supported by the query.

### Bulk Re-Publishing Already-Published Entries via CLI

It was unclear whether already-published entries for a content type could be bulk re-published on a given branch using the CLI, or whether SDK usage was required.

**Root Cause**

This is supported by the CLI today. The @contentstack/cli-bulk-operations plugin provides csdx cm:stacks:bulk-entries, installed separately from the base CLI. Its --operation publish path fetches matched entries and, when no --filter flag narrows the set (to draft, modified, unpublished, or non-localized entries), publishes every matched entry regardless of whether it was already published - which is exactly a bulk re-publish. A --branch flag (default main) scopes the operation directly.

**Resolution**

1.  Install the plugin: csdx plugins:install @contentstack/cli-bulk-operations.
    
2.  Verify: csdx cm:stacks:bulk-entries --help.
    
3.  Run: csdx cm:stacks:bulk-entries --operation publish --content-types <content\_type\_uid> --environments <environment\_name> --locales <locale\_code> --branch main -k <stack\_api\_key>.
    
4.  Confirm when prompted; the command lists matched entries before publishing.
    
5.  Review the summary output and log file (under the bulk-operation directory by default, or --bulk-operation-file) for failures.
    
6.  Retry only failed entries: csdx cm:stacks:bulk-entries --retry-failed ./bulk-operation.
    

If custom logic beyond these flags is needed, a Management SDK script (query entries, fetch publish details, re-publish) remains a valid alternative.

<!-- case:00059311 status:draft synced:false bucket:"Export/Import Commands & Data Formats" -->
### CLI Export-to-CSV Pagination Capped at 10 Records

Exporting users with csdx cm:export-to-csv may cap the export at exactly 10 records instead of retrieving the complete list, even after upgrading the CLI.

**Root Cause**

The pagination fix for this command resides in a sub-plugin rather than the core CLI. A standard npm update does not force npm to replace a sub-plugin if the top-level CLI version is already considered valid, so the fix does not pull down correctly through a regular update.

**Resolution**

1.  Completely uninstall the existing CLI package: npm uninstall -g @contentstack/cli.
2.  Freshly install the package to force-fetch all latest sub-plugins: npm install -g @contentstack/cli.
3.  Re-run csdx cm:export-to-csv and confirm the full record list is exported.

After performing a clean reinstall, re-run the export command. If it returns the complete list of records rather than capping at 10, the issue is resolved. Escalate with your CLI and sub-plugin versions if it persists.

<!-- end:00059311 -->

## TypeScript Generation (TSGen) & Plugins

### csdx tsgen GraphQL Type Generation Fails with Empty Logs

The csdx tsgen command failed to generate GraphQL types, returning a generic "unable to generate GQL types" response.

Executed Code:

csdx tsgen -a "<delivery\_token\_alias>" -o "contentstack/generated.d.ts" --api-type graphql -p CTS --include-system-fields

Response:

unable to generate GQL types

Error logs were empty.

**Root Cause**

*   tsgen comes from the **contentstack-cli-tsgen** plugin—make sure it’s installed and up-to-date.
*   Common issues:
    *   Plugin or version mismatch
    *   Wrong alias or stack
    *   Problems with GraphQL/schema
*   For --api-type graphql, **you must use a delivery token** (management tokens don’t work).
*   The error “unable to generate GQL types” usually comes from **@contentstack/types-generator**, which may not provide detailed error logs—empty log files don’t mean a single root cause.
*   Always check these areas if logs are empty:
    *   plugin status
    *   token type
    *   Authentication
    *   Region
    *   Schema setup

**Resolution**

1.  Confirm contentstack-cli-tsgen is installed and current: csdx plugins:install contentstack-cli-tsgen (or update plugins per docs).
2.  Verify the token alias with csdx auth:tokens: for GraphQL generation, use a **delivery** token alias, and ensure **environment** (and **branch**, if applicable) match the stack.
3.  Review GraphQL-related schema and stack configuration.
4.  Retry csdx tsgen after corrections.

After addressing plugin/config/schema issues in the case, tsgen successfully generated the .d.ts file without error.

### TSGen Output Shows _version Instead of Types

While generating TypeScript types, the user may observe incorrect output: the generated types showed the last \_version number (or otherwise looked sparse or wrong) instead of expected property type definitions.

**Root Cause**

**Verified case:** Reinstalling/updating the **contentstack-cli-tsgen** plugin resolved the symptom.

**Other common causes:** csdx tsgen resolves the stack only from the **delivery token alias** (-a / --token-alias); there is no separate stack flag. Generation is delegated to **@contentstack/types-generator** (REST content types by default, or GraphQL when --api-type graphql is used). Any of the following can produce odd, minimal, or metadata-heavy output:

*   **Wrong alias / stack / environment** - alias points at a different stack, environment, or token than intended.
*   **Token type** - REST generation expects a **delivery** token; GraphQL mode **requires** delivery (management tokens are rejected for GraphQL).
*   **Wrong branch** - content types differ per branch; omitting --branch uses the default branch schema.
*   **Region / host mismatch** - CLI login region or CDA host not aligned with where the stack lives.
*   **CLI / plugin / generator version skew** - outdated plugin or CLI vs current @contentstack/types-generator behavior.
*   **Schema / validation** - some content types skipped (partial generation); output can look incomplete.
*   **Invalid generated interface names** - content type UIDs that do not yield valid TypeScript identifiers (mitigate with -p prefix).
*   **REST vs GraphQL** - comparing expectations across modes; GraphQL output shape differs from REST.

**Resolution**

Apply the scenario that matches the customer setup (often more than one check is needed).

1.  **Wrong stack, alias, or environment**
    
    *   Run csdx auth:tokens and confirm alias, API key, **environment**, and **delivery** token for the intended stack.
    *   Re-add the token if needed, then re-run:
    
    csdx tsgen -a "<correct\_delivery\_alias>" -o ./types/generated.d.ts
2.  **Management token instead of delivery**
    
    *   Use a **delivery** token alias for the target stack and environment.
    *   For GraphQL typings:
    
    csdx tsgen -a "<alias>" -o ./types/graphql.d.ts --api-type graphql
    *   Optional namespace: add --namespace "YourNamespace".
3.  **Wrong branch**csdx tsgen -a "<alias>" -o ./types/generated.d.ts --branch "<branch\_uid>"
4.  **Region / stack mismatch**
    *   Confirm stack region in the Contentstack UI matches CLI login context (for example csdx config:get:region or csdx config:get:proxy when relevant; run csdx config --help for other get commands / auth docs for your CLI version).
    *   Re-authenticate for the correct region, then run TSGen again.
5.  **CLI vs plugin vs generator version skew**csdx --version  
    csdx plugins  
    csdx plugins:update contentstack-cli-tsgen
    *   If issues persist: csdx plugins:uninstall contentstack-cli-tsgen then csdx plugins:install contentstack-cli-tsgen.
6.  **Schema / content type issues (partial generation)**
    *   Read CLI output for skipped content types or “partial schema” messaging; fix content model / global field issues in the stack, then re-run.
7.  **Invalid interface / content type UID names**csdx tsgen -a "<alias>" -o ./types/generated.d.ts -p "I"
8.  **REST vs GraphQL**
    *   Default is **REST** (content-type interfaces). Use --api-type graphql only when GraphQL typings are required; do not expect the same file shape as REST.
9.  **Plugin install / corruption (verified fix)**csdx plugins:install contentstack-cli-tsgen
10.  **Re-run and validate**
     *   Re-run the customer’s exact csdx tsgen command (same flags as CI if applicable).
         *   Open the output file and confirm custom fields appear on interfaces.
         *   If \_version is **expected** as a modeled system field, use --include-system-fields (REST) so system fields are included explicitly.

**Verified case:** After installing or updating contentstack-cli-tsgen, the generated types showed correct property type definitions and the customer confirmed resolution.

**General:** After the matching fix above, generated output should reflect the intended stack, environment, and branch; interfaces should include expected custom fields, not only system metadata (unless --include-system-fields was intentionally used).

<!-- case:00059390 status:draft synced:false bucket:"TypeScript Generation (TSGen) & Plugins" -->
### tsgen ERR_REQUIRE_ESM Error on Windows

Running npm run tsgen on Windows may fail with an ERR_REQUIRE_ESM error, even when following the standard tsgen setup.

**Root Cause**

The uuid module bundled with an outdated version of the Contentstack CLI ships as a newer ES Module version that is incompatible with the CommonJS require() call used internally by @contentstack/cli-utilities.

**Resolution**

1.  Update the tsgen plugin to the latest version: csdx plugins:install @contentstack/cli-tsgen@latest.
2.  Confirm the installed version is v4.7.0 or higher.
3.  If the error persists, perform a clean reinstall of the CLI on Windows and re-verify the uuid module version for compatibility.
4.  Re-run npm run tsgen.

After updating the tsgen plugin and confirming the version, re-run npm run tsgen. If the command completes without an ERR_REQUIRE_ESM error, the issue is resolved. Escalate with your CLI version and OS details if it persists.

<!-- end:00059390 -->