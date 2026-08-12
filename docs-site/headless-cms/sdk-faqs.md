---
title: "SDK Troubleshooting Guides"
description: "Discover answers to common troubleshooting questions about SDK."
url: "https://www.contentstack.com/docs/headless-cms-sdk-troubleshooting/faqs"
product: "Contentstack"
doc_type: "guide"
audience:
  - developers
  - admins
version: "current"
last_updated: "2026-07-27"
---

# SDK Troubleshooting Guides

## Installation, Initialization & Environments

### Type Error During SDK Initialization or App Configuration

Initialization fails with type/runtime errors when config values have the wrong shape (for example, passing a string where an object is expected).

**Root Cause**  
Initialization parameters do not match the expected data types (e.g., passing stringified JSON instead of a raw object), or Marketplace app configuration schemas are misaligned with defined parameter shapes.

**Resolution**

1.  Validate the SDK initialization object against the SDK README/types.
2.  Ensure nested options (proxy/retry/cache/plugin options) are objects, not stringified JSON.
3.  For Marketplace apps, verify config schema matches app parameter definitions.

SDK initializes without exception and the first API call returns a 2xx JSON response. Escalate with a redacted config object and full stack trace if error persists.

### Node.js Version Incompatibility with CLI and SDK

Runtime/module parse errors can occur when project Node runtime is incompatible with package expectations.

**Root Cause**  
The project's Node.js runtime version falls outside the supported range of the specific SDK or CLI package, causing syntax errors or module parsing failures during execution.

**Resolution**

1.  Check node -v.
2.  Use an Active LTS Node version unless the specific SDK/CLI package documents different requirements.
3.  Reinstall dependencies after runtime switch.
4.  Avoid blanket downgrade guidance. Align Node version per package constraints in your lockfile/CI.

Install/import completes and sample SDK calls run without syntax/module loader errors.

### SDK Initialization Failures in SSR Frameworks (Next.js, Astro, Nuxt)

SSR builds/runtime can fail when browser-only assumptions leak into server execution paths.

**Root Cause**  
Browser-specific objects (like window or document) are referenced during server-side execution, or the SDK is initialized as a global singleton that cannot persist across stateless server requests.

**Resolution**

1.  Initialize SDK with contentstack.stack(...) in server-safe modules.
2.  Keep browser-only logic behind typeof window !== 'undefined' checks.
3.  Pass explicit environment/region in config for deterministic server behavior.
4.  Avoid older constructor/global-singleton patterns in SSR code.

Server render completes and fetch returns 2xx without window is not defined or similar runtime errors. Escalate with framework version and minimal initialization snippet.

### SDK Environment Variable Loading Failures in Node.js

The SDK fails to initialize or connect with "Undefined" values because it cannot successfully read the API Key or Token from local .env files.

**Root Cause**  
The SDK is imported or initialized before the application has finished loading .env files, or there is a naming mismatch between the system environment keys and the code.

**Resolution**

1.  Load env variables before any SDK initialization/import side effects.
2.  Match env key names exactly between .env and code.
3.  Restart runtime after changing .env.

Startup shows non-empty required env vars (redacted), and the first SDK call returns 2xx. Escalate with startup order snippet and SDK version if envs are present but init still fails.

### Javascript SDK "Buffer is not defined" Error in Browser Environments

Browser runtime errors occur when Node-only globals/modules are pulled into client bundles.

**Root Cause**  
The application is attempting to use Node.js-specific modules (like Buffer) in a client-side browser environment without the necessary polyfills or the use of a browser-safe SDK build.

**Resolution**

1.  Upgrade to the latest supported SDK/browser-safe package build.
2.  Remove Node-only imports from client-side bundles.
3.  Add polyfills only when upgrade/refactor is not immediately possible.

Browser flow completes without Buffer being defined, and SDK calls return expected data. Escalate with bundler config and import graph if error persists.

### SDK Installation Peer Dependency Version Conflicts

Installing the SDK results in a "Peer Dependency Conflict," preventing installation in projects using specific versions of React or Node.

**Root Cause**  
Version mismatches between the SDK’s requirements and the existing project dependencies (e.g., React or Node.js versions) prevent the package manager from resolving a stable dependency tree.

**Resolution**

Install failures often come from incorrect package names or incompatible dependency trees.

1.  Install correct SDK packages for the use case:
    *   @contentstack/delivery-sdk
    *   @contentstack/management
2.  Align Node and package manager versions with project/toolchain constraints.
3.  Resolve lockfile conflicts explicitly; use bypass flags only as a temporary debugging step.

npm i @contentstack/delivery-sdk  
npm i @contentstack/management

Packages install successfully and import without unresolved dependency conflicts. Escalate with lockfile excerpt, package manager version, and full install error output.

## Authentication, Regions & Networking

### SDK Authentication Failure Due to Invalid Token Type

SDK requests return 401 Unauthorized when a token type does not match the SDK/API being used (for example, using a CMA token with the Delivery SDK).

**Root Cause**

A mismatch exists between the API being called and the token provided, such as using a Management Token for Delivery API calls or a token from a different stack.

**Resolution**

1.  Use the correct token for the SDK:
    *   Delivery SDK -> Delivery Token
    *   Management SDK -> Management Token / Auth Token
2.  Confirm that the API key and token were generated from the same stack.
3.  For Delivery SDK calls, verify the token has access to the configured environment.

A fetch call returns 200 with a non-empty payload and no 401 response. Escalate if a token is active in UI but still rejected. Share stack UID, SDK package name/version, and request ID if available

### Management SDK 403 Error During Content Model Updates

Content type updates via CMA fail with 403 when the token role/scope/policy does not allow model changes.

**Root Cause**

The provided token lacks the necessary administrative permissions/roles to modify schemas, or the request originates from an IP address not included in the stack’s allowlist.

**Resolution**

1.  Ensure the token role has content model update permissions (typically admin-level).
2.  Confirm IP allowlist/policy permits the calling host.
3.  Validate stack limits or governance policies are not blocking changes.

update() returns 2xx, and schema changes appear in UI/API. Escalate if owner/admin role still receives 403; include request ID and sanitized payload.

### Missing "User-Agent" Header Blocking SDK Requests

Some corporate gateways block requests unless expected headers are present or match policy.

**Root Cause**

Corporate firewalls or security gateways are configured to drop requests that lack specific identification headers or custom security metadata.

**Resolution**

1.  Do not assume SDK omits identification headers by default.
2.  If policy requires extra headers, add approved custom headers in your request/plugin layer.
3.  Validate upstream proxies are not stripping headers before the request reaches Contentstack.
4.  Coordinate with network/security team on allowlist rules for SDK traffic.

Requests return 2xx, and WAF logs confirm expected headers/policy match. Escalate with sanitized gateway logs and request ID when blocked despite compliant headers.

### SDK Authentication Error for Non-US Region Stacks

Using default region/host against non-US stacks can produce auth/key mismatch symptoms.

**Root Cause**

The SDK is defaulting to the US region host while the target stack is hosted in a different region (e.g., EU or AU), causing a "Stack Not Found" or invalid key error.

**Resolution**

1.  Set explicit region in SDK initialization.
2.  Use valid region constants supported by the SDK (for example Region.EU, Region.AU, Region.AZURE\_NA, Region.AZURE\_EU, Region.GCP\_NA, Region.GCP\_EU in Delivery TS SDK).
3.  Ensure API key/token are from the same regional stack.

Region-configured calls return 200 from the correct regional host. Escalate if region is correct but key is still rejected; include stack UID, region, and request host.

### SDK Session Expiration for Private Stack Access

Scripts using the SDK with an **Authtoken** (user session) fail after a few hours, resulting in 401 Unauthorized as the session expires.

**Root Cause**

User-session Authtokens have a limited lifespan and expire, causing long-running background scripts to fail once the initial session token becomes invalid.

**Resolution**

Long-running scripts using user session auth can fail when session tokens expire.

**Do**

1.  Use management\_token for long-running, non-interactive server jobs.
2.  Keep auth mode explicit per workflow (management\_token, authtoken, or OAuth bearer).
3.  Handle 401 with a controlled re-auth/refresh path, then retry only safe/idempotent operations.
4.  Configure retry strategy for 429/5xx separately from authentication renewal.

**Don't**

1.  Don't run long background automation on user authtoken unless you own renewal logic.
2.  Don't assume a generic login() call automatically refreshes tokens in every SDK flow.
3.  Don't mix authorization and authtoken headers in the same request path.
4.  Don't retry 401 indefinitely without rotating or re-establishing credentials.

Long-running job completes without late-stage 401 failures, and any forced token rollover recovers via the defined re-auth path. Escalate with job duration, auth mode (management\_token/authtoken/OAuth), retry settings, and first 401 timestamp/request ID.

### Contentstack CLI "Login Failed" via SDK-based Auth Module

Users cannot log in to the CLI (csdx auth:login) despite using correct credentials, receiving an "Invalid Credentials" or "MFA Required" error.

**Root Cause**

Authentication fails due to incorrect region settings in the CLI config, or the user has failed to complete the required Multi-Factor Authentication (MFA) challenge.

**Resolution**

1.  Use csdx auth:login and complete the built-in MFA/OTP flow when prompted (or use --oauth for SSO flows).
2.  Confirm configured region before retrying auth (csdx config:get:region / csdx config:set:region).

csdx auth:login succeeds, csdx auth:whoami prints the logged-in email, and csdx config:get:region shows the expected region. Escalate through CLI support path with CLI version, exact login command used, region config output, and auth logs.

<!-- case:00059347 status:draft synced:false bucket:"Authentication, Regions & Networking" -->
### OAuth2 Token Requests Failing Due to Content-Type Mismatch

Calling a custom OAuth2 token endpoint (such as AWS Cognito) from an App SDK plugin may fail when the request uses the wrong Content-Type header.

**Root Cause**

The request was sent with `Content-Type: application/json` and a JSON-formatted body, but Cognito-style OAuth2 token endpoints expect `Content-Type: application/x-www-form-urlencoded`. The mismatched content type causes the token endpoint to reject or misinterpret the request.

**Resolution**

1.  Inspect the outgoing token request and confirm the Content-Type header being sent.
2.  Update the request to use `Content-Type: application/x-www-form-urlencoded` instead of `application/json`.
3.  Reformat the request body as URL-encoded form data (for example, `grant_type=client_credentials&scope=...`) instead of a JSON object.
4.  Retry the token request.

After updating the Content-Type header and body format, retry the OAuth2 token request. If the token endpoint returns a valid access token, the issue is resolved. Escalate with the exact request headers and response body if it persists.

<!-- end:00059347 -->

## Querying, References & Content Retrieval

### Identifying Unpublished Entries via Management SDK

Developers are unable to distinguish between "Draft" (unpublished) and "Published" entries when using the Management SDK for auditing or migration.

**Root Cause**

The Management SDK (CMA) returns all entries by default regardless of status; the publish\_details metadata must be explicitly requested and inspected to verify live status.

**Resolution**

1.  Fetch entries using CMA with include\_publish\_details: true.
2.  Inspect publish\_details in the response.
3.  Treat empty publish\_details (or version mismatch logic in your workflow) as unpublished/draft-like state.

Example:

const entry = await client  
.stack({ api\_key: process.env.CS\_API\_KEY })  
.contentType('blog')  
.entry('entry\_uid')  
.fetch({ include\_publish\_details: true });

The programmatic output correctly identifies which entries are live and which are drafts. Escalate if publish\_details are missing for entries known to be published. Provide Entry UID.

### SDK Query Parameter Mismatch (422 Unprocessable Entity)

The SDK returns a 422 Unprocessable Entity error when query methods (like filters or includes) use unsupported or misspelled parameters.

**Root Cause**

The query uses misspelled parameters, unsupported filter methods for a specific field type, or hidden characters that violate API validation rules.

**Resolution**

1.  Check the SDK method syntax; ensure you are using the correct helper methods (e.g., .includeCount() vs manually adding parameters).
2.  Verify that parameters like include\_fallback are supported for the specific content type.
3.  Ensure no trailing spaces or hidden characters exist in the parameter strings.

The query executes successfully and returns the expected count or localized content. Escalate if the same query works via cURL but fails via SDK. Provide the generated request URL.

### SDK 404 Error for Published Entries

Published entries can still return 404 when the environment/locale/region does not match the publish target.

**Root Cause**

The request is targeting a different environment or locale than the one where the entry was successfully published.

**Resolution**

1.  Confirm entry is published to the same environment used by SDK config.
2.  Ensure locale code matches exactly.
3.  Verify region/host alignment for the stack.

Entry fetch returns 200 and expected UID for requested environment/locale. Escalate with entry UID, environment, locale, and region used in request.

### SDK Reference Field Retrieval Returning Empty Arrays

Reference fields may return empty arrays/UID-only data when references are not explicitly expanded or not publish-aligned.

**Root Cause**

Reference fields are not explicitly expanded using .includeReference(), or the referenced entries have not been published to the target environment.

**Resolution**

1.  Use includeReference(...) for required reference fields.
2.  For nested refs, include dotted paths as needed.
3.  Verify referenced entries are published to the same environment/locale as the parent entry.

Response returns populated referenced objects (not empty arrays for valid linked data). Escalate with parent entry UID, reference field UID/path, and publish targets.

### Management SDK Failures to Retrieve Audit Metadata

Developers cannot programmatically access "Last Modified By" or "Owner" details via the SDK, as these are excluded from default responses for performance.

**Root Cause**

Metadata fields like "Owner" or "Last Modified By" are excluded from standard entry responses to optimize performance and must be requested via specific inclusion parameters.

**Resolution**

1.  Use CMA (not Delivery SDK) for metadata workflows.
2.  Fetch entry-level metadata through documented entry params:
    *   entry(uid).fetch({ include\_workflow: true, include\_publish\_details: true })
3.  Fetch action/user audit trail through stack audit-log APIs:
    *   stack.auditLog().fetchAll({ include\_count: true, limit, skip })
    *   stack.auditLog('log\_uid').fetch()
4.  Verify the token has read access for the stack objects being queried.

const entry = await client  
.stack({ api\_key: process.env.CS\_API\_KEY })  
.contentType('blog')  
.entry('entry\_uid')  
.fetch({ include\_workflow: true, include\_publish\_details: true });const logs = await client  
.stack({ api\_key: process.env.CS\_API\_KEY })  
.auditLog()  
.fetchAll({ include\_count: true, limit: 10, skip: 0 });

Entry fetch returns metadata fields (including workflow/publish context), and audit-log calls return actor/action records for the stack. Escalate with entry UID, audit-log request params, token type, and sample response payload if metadata is still missing.

### Localized Content Retrieval Defaults to Master Language

The SDK returns content in the master language even when a different locale is requested, or it returns a 404 if the locale is not properly specified.

**Root Cause**

The query does not explicitly define the .locale() parameter, or the requested locale code does not match the exact casing/format defined in the stack.

**Resolution**

1.  Use .locale('locale-code') on Delivery SDK queries/entry fetches.
2.  Confirm the target locale is enabled and published for the entry.
3.  Use exact locale code casing/format as defined in stack locales.

const localizedEntry = await stack  
.contentType('article')  
.entry('entry\_uid')  
.locale('fr-fr')  
.fetch();

Returned fields contain localized values (or expected fallback behavior if locale content is unavailable). Escalate with entry UID, locale code, and publish evidence when locale data is still missing.

### Global Field Data Missing from SDK JSON Response

Data contained within a Global Field is missing from the final SDK response, even though other entry fields are present.

**Root Cause**

The field is restricted by role-based permissions, or the global field schema was updated without re-publishing the affected entries.

**Resolution**

Global field payload may appear missing due to model visibility, permission, or publish-state mismatch.

1.  Verify the global field is not hidden/restricted in the content model.
2.  Confirm token roles can access the field data.
3.  Re-publish content type/entries if model updates were recent.

Entry response includes expected global field object for the published target. Escalate with content type UID, field UID, and role/token details.

<!-- case:00059450 status:draft synced:false bucket:"Querying, References & Content Retrieval" -->
### Mixed-Locale Content on Nested Includes With Variants

Fetching an entry with nested included references and multiple variant parameters may return a mix of locales — variant fields resolve to a fallback locale while other fields correctly return the requested locale.

**Root Cause**

Two conflicting request settings caused this. Variant identifiers were being passed three different ways in the same request — a query parameter, a stack header, and the SDK's `.variants()` method — which conflicts. Separately, `include_fallback=true` was set even though the entry already existed in the requested locale; fallback only applies when localized content is genuinely missing, so setting it here mixed locale sources instead of resolving consistently.

**Resolution**

1.  Remove duplicate variant parameters from the request and pass variant identifiers using only the SDK's `.variants()` method.
2.  Remove `include_fallback=true` from the request if the entry already exists in the target locale — fallback is only needed for genuinely missing localized content.
3.  Retry fetching the entry with its nested includes and variant fields.

After correcting the variant parameter usage and removing the unnecessary fallback flag, retry the fetch. If all fields — including variant fields — consistently return the requested locale, the issue is resolved. Escalate with the exact request parameters and headers used if mixed-locale results persist.

<!-- end:00059450 -->

## Caching, Sync & Performance Limits

### SDK Timeout on Large Asset Content Fetching

Large payloads (many assets/references) can trigger request timeout failures.

**Root Cause**

Single requests attempting to fetch massive payloads (e.g., 100+ deep references) exceed the default network timeout limits of the SDK or environment.

**Resolution**

1.  Reduce payload size with pagination (limit/skip) and smaller batches.
2.  Increase SDK timeout only as needed for network conditions.
3.  Split deep data hydration into phased requests instead of one oversized query.

const result = await stack  
.contentType('article')  
.entry()  
.query()  
.limit(20)  
.skip(0)  
.find();

Paginated requests return 200 consistently with no timeout error. Escalate if timeouts persist on small paginated batches; include region, timeout setting, and stack UID.

### SDK Cache Synchronization Issues on Live Environments

Stale content appears when cache policy/persistence settings prioritize cache over freshness.

**Root Cause**

The SDK’s cache policy is set to prioritize local persistence (e.g., CACHE\_ELSE\_NETWORK) over real-time API data, causing the application to serve stale content.

**Resolution**

1.  Use modern cache policy configuration (cacheOptions.policy) for your freshness requirement.
2.  Prefer network-first patterns for dynamic/live content paths.
3.  Ensure persistence store TTL/maxAge and cache invalidation strategy are intentional.
4.  Remove guidance relying on legacy/non-standard cache clearing methods.

cacheOptions: {  
policy: Policy.NETWORK\_ELSE\_CACHE,  
persistenceStore: new PersistenceStore({ storeType: 'localStorage', maxAge: 3600000 })  
}

Recently updated entries return latest updated\_at/content after policy changes. Escalate with cache policy, persistence config, and timestamps of publish vs fetch.

### 429 Too Many Requests During SDK-Driven Bulk Operations

High-concurrency scripts hit platform/API rate limits and receive 429.

**Root Cause**

High-concurrency scripts exceed the platform’s rate limits by sending too many simultaneous requests without exponential backoff or throttling.

**Resolution**

1.  Use retry with exponential backoff in application logic.
2.  Reduce parallelism and batch requests.
3.  Use SDK-supported bulk operation endpoints/methods where applicable.
4.  In CMA JS flows, configure retry settings intentionally (retryOnError, retryLimit).

const client = contentstack.client({  
authtoken: process.env.CS\_AUTHTOKEN,  
retryOnError: true,  
retryLimit: 5  
});

Bulk workflow completes successfully without terminal 429 failures. Escalate if 429 appears at low request volume; share request rate, source IP, and stack UID.

### Handling "Entry Deleted" Errors During SDK Sync API Calls

The SDK's Sync API returns an error or stops processing when it encounters a deletion event in the sync queue.

**Root Cause**

The application logic fails to distinguish between entry updates and entry\_deleted event types in the Sync API response, leading to processing errors for non-existent UIDs.

**Resolution**

Sync consumers break when deletion events are treated like normal entry payloads.

Use one of the following supported patterns based on your sync architecture:

1.  **Client-side event switch (default):**
    *   Process all syncData.items by item.type
    *   Remove local records for entry\_deleted
2.  **Server-filtered delete sync jobs:**
    *   Run stack.sync({ type: 'entry\_deleted' }) for cleanup-focused workers
3.  **Tokened incremental strategy (recommended at scale):**
    *   Drain batches with pagination\_token
    *   Persist and continue with sync\_token for delta runs
    *   Apply delete events before any re-fetch/re-hydration logic

const syncData = await stack.sync({ syncToken: lastSyncToken });  
for (const item of syncData.items) {  
if (item.type === 'entry\_deleted') {  
// remove from local store  
}  
}  
  
// Example server-filtered delete run:  
const deletedOnly = await stack.sync({ type: 'entry\_deleted' });

Sync completes with 200, delete events are consumed without exceptions, and local state no longer contains deleted entry UIDs after reconciliation. Escalate with sync mode used (full/mixed/deleted-only), sync\_token/pagination\_token, failing item payload, and local-store reconciliation logs.

## Asset Transformations & UI Rendering

### SDK Asset URL Transformation Parameters Not Applying

Developers attempt to resize an asset using SDK helper methods (e.g., .width(200)), but the resulting URL does not contain the transformation parameters.

**Root Cause**

Transformation methods are being chained on the URL string directly rather than using the ImageTransform class required by modern SDK versions to generate valid query parameters.

**Resolution**

Legacy chaining assumptions can generate unchanged URLs when transformation objects are not applied correctly.

1.  Build transform instructions with ImageTransform.
2.  Apply transformation through the SDK URL transform API.
3.  Confirm the asset is an image and not a non-transformable file type.

import { ImageTransform, Format } from '@contentstack/delivery-sdk';  
const transform = new ImageTransform().resize({ width: 200 }).format(Format.PJPG);  
const transformedUrl = assetUrl.transform(transform);

The generated URL contains expected transform parameters (for example width=200) and transformed asset loads. Escalate with original URL, transformed URL, and asset MIME type.

### Raw Markdown Returned Instead of HTML in SDK Output

Content from Markdown fields is returned as raw Markdown syntax in the SDK response, leading to formatting issues on the live site.

**Root Cause**

Contentstack APIs return raw data (Markdown or JSON RTE) to maintain a headless architecture; the responsibility of parsing and rendering this data lies with the frontend application.

**Resolution**

SDK responses intentionally return raw markdown content; HTML rendering is application responsibility.

1.  Classify the field first:
    *   **Markdown field** -> expect raw markdown string from SDK.
    *   **JSON RTE field** -> expect structured JSON, not pre-rendered HTML.
2.  For JSON RTE content that includes embedded entries/assets, fetch with SDK query helpers such as .includeEmbeddedItems().
3.  For reference fields used in render paths, include linked content using .includeReference(...) where needed.
4.  Render in the application layer:
    *   Markdown -> parse with your app’s markdown renderer.
    *   JSON RTE -> render through your rich-text renderer/component pipeline.
5.  Sanitize final HTML output according to frontend security policy before DOM injection.
6.  If output is still raw, verify the UI render path is not escaping HTML as plain text.

API response returns raw markdown/JSON RTE as expected, and frontend render output shows formatted HTML with embedded items resolved where configured. Escalate with field type (Markdown vs JSON RTE), sample payload, query helper usage (includeEmbeddedItems/includeReference), and renderer configuration.