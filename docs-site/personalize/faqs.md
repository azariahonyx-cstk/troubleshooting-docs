---
title: "Personalize Troubleshooting Guides"
description: "Discover answers to common troubleshooting questions about Personalize."
url: "https://www.contentstack.com/docs/personalize-troubleshooting/faqs"
product: "Contentstack"
doc_type: "guide"
audience:
  - developers
  - admins
version: "current"
last_updated: "2026-07-01"
---

# Personalize Troubleshooting Guides

## API & SDK Implementation

### Fixing Propagation Delay in Contentstack Personalize SDK

When using the Contentstack Personalize SDK, changes made to experiment variants in the dashboard do not reflect immediately on the frontend.

**Root Cause**

This is due to propagation delays inherent in the SDK's manifest delivery system. The SDK is designed for performance, which sometimes results in a slight delay for updates to reach the client side.

**Resolution**

If your use case requires immediate variant updates (real-time reflection), do not rely on the SDK's automated fetch. Instead, switch to using the Contentstack Personalize API for direct variant retrieval. The API bypasses the SDK's propagation window.

After switching from the SDK to the API, retrieve a recently updated variant. If the updated data is returned immediately and aligns with the expected scenario, the issue is resolved.

### Validation Errors When Creating Variant Groups via CMA API

Creating variant groups via CMA APIs in Personalize may result in specific validation errors, such as "name must be a string," when attempting to use unsupported POST requests. This prevents the automated creation of variants through the current API implementation.

**Root Cause**

The issue is caused by a system limitation where the variants endpoint within the CMA API currently only supports read operations (GET) and does not permit the creation of variants via the POST method.

**Resolution**

1.  Check the API request method to ensure it is not a POST request, as creating variants via API is not currently supported.
2.  Identify validation errors in the response, such as "name must be shorter than or equal to 200 characters", "name must be a string", or "name should not be empty", as indicators of an unsupported write attempt.
3.  Use the GET method exclusively to fetch existing variants from the endpoint.
4.  Manually create variants within the user interface until API write support is available.

After discontinuing the unsupported POST request and using the API only for fetching variants, check the API responses. If the validation errors no longer occur during read operations, the issue is resolved.

### 400 Bad Request Error Due to Missing Personalize Project ID

API calls to retrieve user attributes from Personalize may return a 400 Bad Request error. This prevents the system from fetching necessary user data, effectively blocking any personalization logic that relies on these attributes.

**Root Cause**

The issue is caused by a missing Project ID in the Personalize API request. When the integration is powered by Lytics, the API expects a valid Project ID to route the request; if this ID is not configured within the Lytics platform fields, it will not be passed in the outgoing request, resulting in an authentication or routing failure.

**Resolution**

1.  Inspect the failed API request and confirm if the project\_id parameter or header is missing or null.
2.  Navigate to the Lytics platform settings and locate the field designated for the Personalize Project ID.
3.  Update this field with the correct Project ID from the Contentstack Personalize dashboard.
4.  Save the configuration to ensure the ID is included in subsequent API calls.

After updating the Project ID in Lytics, re-trigger the API call to fetch user attributes. If the system returns a 200 OK response with the correct user data, the issue is resolved.

### Personalize SDK Returning Null Variants in Local Environments

Testing Personalize SDK integrations in a local development environment may result in variants failing to resolve, showing null in middleware logs. This prevents the validation of audience-based personalization rules (such as country-specific targeting) before deployment to a live server.

**Root Cause**

The issue is caused by the lack of valid geolocation data in local environments. Because Personalize relies on the user's IP address to determine audience membership for country-based segments, a localhost IP address cannot be resolved to a specific region. Consequently, the SDK cannot match the user to any country-targeted audience, resulting in a null variant response.

**Resolution**

1.  Check the middleware or SDK logs; if they display null variants while testing locally, verify if the audience rules rely on geolocation or IP-based data.
2.  Confirm that the middleware code and project configuration align with the standard implementation guides (e.g., Vercel-specific Next.js guide).
3.  Use a tool like ngrok to expose the local environment via a public URL or deploy the application to a staging/live environment (e.g., Vercel or Netlify) to test with real IP addresses.
4.  Perform manual testing by spoofing the country header in the request if the platform supports header-based overrides during development.

Deploy the application to a live URL and access it. If the Personalize SDK correctly identifies the user's country and returns the corresponding variant parameters, the implementation is verified as correct.

### Personalize UI Saved Values Not Visible After Platform Update

Saved personalization values may stop appearing in the Personalize UI even though the values are returned correctly when queried directly via the API. This discrepancy causes confusion about whether data has been saved successfully.

**Root Cause**

A security-related library upgrade that processes query parameters introduced a default limit on the number of query params that can be passed in a single request. Because the new limit was lower than the maximum number of rules allowed in an audience (100), requests with many rules were silently truncated, causing values to appear missing in the UI.

**Resolution**

1.  Verify the issue by querying the Personalize API directly. If values are returned via API but not displayed in the UI, the query param limit is the likely cause.
    
2.  Contact Contentstack Support and reference the query parameter processing library limit. Engineering must explicitly configure the limit to 100 to match the maximum audience rule count.
    
3.  Once the configuration is updated, reload the Personalize UI and confirm that all saved values are now visible.
    

After the fix is applied, values saved in the UI and retrieved via the API will be consistent. If the issue persists, check whether the number of audience rules exceeds 100, as this is the configured maximum.

### 403 Forbidden Errors on Personalize Manifest Endpoint

The Personalize manifest endpoint (/manifest) may return a high volume of 403 Forbidden responses, particularly during overnight hours. Users may suspect a platform change, rate limit, or authentication issue as the cause.

**Root Cause**

403 responses on the manifest endpoint are commonly caused by automated bot or crawler traffic (for example, ChatGPT bots, SeznamBot, or Website-info robots). DNS and CDN providers may automatically block unusual or high-frequency bot requests, resulting in 403 responses for those specific request origins. Legitimate user traffic is not affected.

**Resolution**

1.  Review your server logs or CDN analytics and filter requests by user agent. Identify whether the 403 responses are concentrated among known bot agents rather than real user sessions.
    
2.  Check your DNS provider or CDN configuration (for example, Cloudflare) to see if automated bot-blocking rules are active. These are expected and do not require changes.
    
3.  If legitimate user requests are also returning 403 errors, open a support case with Contentstack and share the specific user agents, IP ranges, and timestamps of affected requests for further investigation.
    
4.  Monitor the error rate over 24-48 hours. If bot traffic subsides, the 403 count will decrease accordingly.
    

If 403 errors drop significantly as bot activity decreases and real user traffic continues to succeed, the issue is confirmed as bot-related and no platform changes are required.

Note: if Personalize is completely unresponsive rather than returning 403 errors, check the Contentstack Status Page (https://www.contentstackstatus.com) as the first step before beginning any SDK or configuration debugging. Platform incidents are posted there in real time.

### Personalize Management API Authentication: OAuth Token Required

Requests to the Personalize Management API return a "Failed to Fetch" or "Unable to Retrieve Data" error when using a Content Management Token (CMT) for authentication. This blocks programmatic access to Personalize resources.

**Root Cause**

The Personalize Management API does not support Content Management Tokens. It requires either an OAuth token or an authtoken for all API requests. Using an unsupported token type results in an authentication failure.

**Resolution**

1.  Confirm the authentication method currently in use. If a Content Management Token is being passed in the request headers, this is the cause of the failure.
    
2.  Generate an OAuth token by following the Contentstack OAuth documentation. Alternatively, use the authtoken associated with a valid Contentstack account.
    
3.  Update all API requests to pass the correct token in the Authorization header.
    
4.  Retry the request and confirm a successful response is returned.
    

Refer to the Personalize Management API documentation for full details on supported authentication methods: https://www.contentstack.com/docs/personalize/

### Short UID Not Supported as API Query Parameter for Experience or Variant Retrieval

Attempting to retrieve a specific Experience or Variant by passing its Short UID as a query parameter in the Contentstack API does not return the expected result. This prevents developers from using Short UIDs as identifiers in API-driven workflows.

**Root Cause**

Short UIDs are not supported as direct query parameters in the Contentstack API. This is a current API design limitation and not a product defect.

**Resolution**

1.  Replace Short UIDs with full UIDs or slug-based identifiers when querying Experiences or Variants via the API.
    
2.  If your application has already stored Short UIDs, build a mapping layer in your backend that translates Short UIDs to full UIDs or slugs before making API calls.
    
3.  To retrieve variant content, use the Contentstack Delivery SDK or CDA and specify variant aliases rather than relying on Short UID-based querying.
    
4.  Store full UIDs or slugs as the primary identifiers in your application architecture to avoid this limitation going forward.
    

Once full UIDs or slugs are used in API requests, Experiences and Variants will be retrieved as expected.

### Management API: Variant Updates Require the Versions Endpoint

Attempting to update variant fields via the /experiences/{experience\_uid} endpoint in the Personalize Management API results in validation errors or the changes not being applied. This prevents programmatic management of variant content.

**Root Cause**

The /experiences/{experience\_uid} endpoint only supports updating experience-level fields. It does not support updating variant-specific fields. A separate versions endpoint must be used for variant updates.

**Resolution**

1.  Review your API request and confirm whether the fields being updated are experience-level or variant-level. Experience name, status, and configuration belong to the experiences endpoint; variant content and rules belong to the versions endpoint.
    
2.  Update your API calls to target the correct versions endpoint for any variant field updates.
    
3.  If your implementation uses Lytics audiences in the variant configuration, pass external Lytics audience IDs using the lyticsAudiences field rather than the audiences field to ensure correct resolution.
    
4.  Test the updated API call and confirm the variant fields are saved and returned correctly.
    

After switching to the versions endpoint and using the correct field names, variant updates will be applied successfully.

### Personalize API Long Response Times and Intermittent Failures

Connections to Contentstack Personalize endpoints (/user-attributes and /manifest) may experience response times ranging from 1 to 10 seconds, with intermittent failures across all containers in an integration. This can degrade application performance and reliability.

**Root Cause**

Isolated latency spikes on Personalize endpoints are typically caused by brief traffic bursts or normal network variability rather than a persistent platform issue. Platform-side p95 latency for /user-attributes is approximately 380 ms and for /manifest approximately 149 ms. Requests exceeding 1 second typically represent less than 0.2% of traffic.

**Resolution**

1.  Check whether the high latency is consistent or isolated. Review Contentstack's status page for any active incidents before investigating your own infrastructure.
    
2.  Implement /user-attributes calls as fire-and-forget requests so they do not block critical application workflows. These calls update user data asynchronously and do not need to be awaited before rendering content.
    
3.  Add retry logic and fallback mechanisms to /manifest calls to handle occasional latency spikes gracefully without impacting the user experience.
    
4.  Review your container or serverless environment's connection settings. Ensure HTTP keep-alive is enabled to avoid TCP handshake overhead on each request.
    
5.  If sustained high latency persists beyond what is explained by traffic bursts, open a support case and provide the affected Project ID, endpoint URLs, timestamps, and sample request/response logs.
    

After implementing fire-and-forget patterns for /user-attributes and retry logic for /manifest, isolated latency spikes will no longer cause visible failures in the application.

### Personalize Not Working in QA Environment (Edge API)

Personalization appears to function correctly in a local development environment but fails in a QA application environment. The /manifest endpoint returns unexpected results or variants are not applied as expected.

**Root Cause**

The Personalize /manifest endpoint is publicly accessible and does not require IP allowlisting. If personalization works locally but not in QA, the issue is typically caused by a misconfiguration in the QA application setup rather than a platform restriction.

**Resolution**

1.  Confirm that the QA environment URL is correctly configured and accessible. An unreachable QA endpoint will prevent the Personalize SDK from operating.
    
2.  Verify there is no IP allowlisting or firewall rule in the QA environment that would block outbound requests to Personalize endpoints.
    
3.  Check whether the Personalize SDK initialization code in the QA environment is identical to the working local configuration. Ensure environment variables such as the Project UID are correctly set for QA.
    
4.  Review Cloudflare or CDN security event logs to confirm no rules are blocking network calls from the QA environment.
    
5.  Isolate the issue by making a direct cURL request to the /manifest endpoint from the QA environment and inspecting the response.
    

If a direct cURL request to /manifest returns the correct response from the QA environment, the issue is in the application-level setup rather than the platform. Review SDK initialization order and environment configuration.

### Unexpected 404 on /user-attributes and /api/telemetry/event Endpoints

A 404 error appears on the Personalize Edge /user-attributes endpoint on page load, even though the application is not making explicit GET or PATCH calls to that endpoint. A separate 404 on POST /api/telemetry/event may also be observed in the same environment.

**Root Cause**

The /user-attributes call is triggered automatically by certain Contentstack packages — in particular, the Live Preview Utils package (@contentstack/live-preview-utils) and Lytics jstag integration — rather than by explicit developer code. If the Personalize project UID is not correctly configured in the jstag settings within Lytics, the outbound PATCH /user-attributes request will fail with a 400 or 404 because the platform cannot route the request to the correct project. The /api/telemetry/event 404 is typically a separate, non-critical call made by SDK packages for internal diagnostics and does not affect personalization delivery.

**Resolution**

1.  Open browser developer tools, navigate to the Network tab, and filter for requests to the personalize-edge.contentstack.com domain. Identify which package or script is initiating the /user-attributes call.
    
2.  If Lytics is installed on the site, navigate to the Lytics dashboard and verify that the Contentstack Personalize project UID is correctly entered in the jstag configuration settings. A missing or incorrect project UID is the most common cause of this 404.
    
3.  If Lytics is not in use, check whether the @contentstack/live-preview-utils package is initialised with the correct project UID and environment settings.
    
4.  For the /api/telemetry/event 404: confirm whether this endpoint is required by your implementation. If the 404 has no visible effect on personalization behaviour, it can be treated as a non-critical SDK diagnostic call. If it is blocking a workflow, open a support case and share a HAR file capturing the full request/response.
    
5.  After correcting the project UID configuration, reload the page and confirm that /user-attributes returns a 200 response and that personalization behaves as expected.
    

If the 404 persists after verifying the project UID and package configuration, open a support case with your Project UID, the full request URL, response headers, and a HAR file if available. Do not share HAR files containing authentication tokens without redacting sensitive values first.

## Experiences & Variant Delivery

### Personalized Module Variants Missing in Alternate Branches

Personalized module variants may appear missing when switching from the main branch to an alternate branch. This behavior prevents testing personalized modules in non-main environments.

**Root Cause**

This is a product limitation. Variant groups, variants, and entry variants are exclusively supported on the main branch and are not cloned when new branches are created.

**Resolution**

1.  Configure all variant groups, variants, and entry variants exclusively on the main branch.
2.  Note that these elements will not be present when a new branch is created.
3.  Refer to the official documentation regarding entry variant limitations for further details on branch-specific support.

Navigate to the main branch to verify variant visibility. If variants appear there but not in derived branches, the behavior is confirmed as expected.

### Locked Variant Distribution in Active A/B Split Tests

Ending an A/B split test to promote a winning variant can be difficult because the variant distribution sliders remain locked, even if the test is paused.

**Root Cause**

System locks on variant distribution are a deliberate safeguard once an experiment is live. This ensures test results remain statistically valid by preventing mid-test adjustments that would skew data.

**Resolution**

1.  Recognize that distribution sliders are non-functional while a test is running or paused.
2.  Identify the winning variant based on current analytics.
3.  Create a new draft of the personalized experience to override the locked settings.
4.  Direct 100% of the traffic to the winning variant within the new draft to "promote" the winner.
5.  Manually copy the winning content into the main baseline entry if it is intended to replace the original version permanently.

Publish the new draft with 100% traffic directed to the winner. If the winning content is consistently served to all users, the issue is resolved.

### Geolocation Variants Failing to Activate in Personalize

Personalization variants based on "Geolocation - Country" conditions may fail to activate, resulting in a null status in personalization logs and the delivery of default content.

**Root Cause**

This is typically caused by limitations in the third-party IP geolocation database. If a user's IP address cannot be correctly mapped to a specific country in the external database, the location trigger fails to resolve.

**Resolution**

1.  Review personalization logs to confirm if geolocation variants return a null status while other variants activate correctly.
2.  Use a VPN during testing to provide a verified IP address associated with the target country.
3.  Test on a mobile device, as mobile networks often provide more consistent geolocation data.
4.  Perform manual testing via GraphQL by explicitly passing the regional condition (e.g., country: "US") in the query to bypass automatic resolution.

Check personalization logs after using a VPN or hardcoded GraphQL parameter. If the variant status changes from null to active (e.g., 3\_1), the configuration is correct, and the failure is confirmed as a database-resolution issue.

### Lytics Experience Pop-up Failing to Appear on Live Pages

A Lytics Experience (such as a notification or pop-up) may be visible in the preview environment but fail to appear on live pages, often accompanied by a "Bad Request" error.

**Root Cause**

The request sent to the personalization edge API is missing the PROJECT\_UID header. Without the x-cs-personalize-project-uid header during a PATCH request to the /user-attributes endpoint, the system returns an error and blocks the experience.

**Resolution**

1.  Open browser developer tools and inspect the **Network** tab for failed requests to personalize-edge.contentstack.com.
2.  Look for the error message: personalize.USER\_ATTRIBUTES.PROJECT\_UID\_HEADER\_NOT\_SET.
3.  Update the implementation to ensure the required Project UID is included in all personalization-related request headers.
4.  Verify the experience is correctly activated in the Lytics dashboard and targeted to the correct URL.

Navigate to the target live page after ensuring the Project UID header is correctly set. If the intended pop-up appears as expected, the issue is resolved.

### A/B Test Conversion Numbers Not Incrementing Correctly

Conversion numbers in a Personalize A/B test do not consistently increment even when conversion events are successfully triggered. This causes inaccurate test results and prevents reliable evaluation of variant performance.

**Root Cause**

The issue occurs in hybrid Next.js implementations where the Personalize SDK is initialized on the server side (SSR) but conversion events are triggered on the client side. This architectural split creates a User ID mismatch: the server-generated session ID differs from the client session, so the system cannot attribute client-side conversions to server-side impressions within the required 30-day attribution window. Race conditions between SDK initialization and event firing compound the problem.

**Resolution**

1.  Audit your SDK initialization code. Identify whether the SDK is being initialized in both server and client contexts.
    
2.  Move SDK initialization entirely to the client side using a Global Context Provider pattern. A custom hook (for example, usePersonalize) should manage the SDK instance and prevent redundant re-initialization across component renders.
    
3.  Ensure the User ID is generated and persisted consistently on the client side so that impression and conversion events share the same session context.
    
4.  Use the publish\_details field from the entry JSON to identify which variant was served. This simplifies variant filtering without requiring additional API calls.
    
5.  After migrating to a fully client-side SDK initialization, trigger an impression and then a conversion event and confirm that the conversion count increments in the Personalize analytics dashboard.
    

Once SDK initialization is consolidated on the client side, impression and conversion events will share a consistent User ID and conversions will be accurately attributed.

### Asset Data Returns Null for Variant Entries Using Image Preset Picker

When an asset is attached to a variant entry using the Image Preset Picker Marketplace extension inside a global field, the CDA response returns null for that asset. The same asset attached using a standard file field returns correctly.

**Root Cause**

This was a known platform bug specific to the combination of the Image Preset Picker Marketplace extension, global fields, and personalization variant entries. The issue was reproduced internally and tracked in engineering. Re-saving and re-publishing the entry did not resolve the issue prior to the fix.

**Resolution**

1.  If you encounter null asset data for variant entries using the Image Preset Picker in a global field, verify that your Contentstack environment is running the latest platform version, as a fix has been deployed.
    
2.  As a temporary workaround while awaiting the fix, replace the Image Preset Picker field with a standard file field to attach the asset, which returns correctly in the CDA response.
    
3.  After the fix is confirmed as deployed in your region, re-test the variant entry with the Image Preset Picker in a global field to confirm asset data is returned correctly.
    

If null asset data persists after the platform fix is deployed, open a support case with your Stack UID, Content Type UID, and Entry UID for further investigation.

### Variant Does Not Belong Error Blocking Save and Publish

While editing an experiment page in Personalize, a "Variant Doesn't Belong" error appears after a minor update. This error prevents saving or publishing any variants, including the control, and also blocks exporting. All variant editing actions are blocked until the issue is resolved.

**Root Cause**

This is a backend inconsistency or stuck state that can occur when an editing operation leaves a variant in an invalid relationship with the parent experience. The error is a platform-side bug rather than a user configuration issue.

**Resolution**

1.  Stop attempting to save or publish variants, as repeated failed attempts will not resolve the stuck state.
    
2.  Open a support case with Contentstack and provide the affected Project UID, Experience UID, and the exact error message text.
    
3.  Engineering will review the backend state for the affected experience and apply a fix to restore the correct variant-to-experience relationship.
    
4.  Once the fix is applied, attempt to edit and publish the affected variants to confirm the error no longer appears.
    

This issue is resolved at the platform level by engineering. Contact Contentstack Support immediately when the error appears to minimize disruption to your live personalization setup.

### Entry Variants Not Working — Entry Variants Not Enabled

Personalization variants appear to be set up correctly but do not function as expected. Content is not personalised and variant configurations seem to have no effect.

**Root Cause**

Entry variants must be explicitly enabled in the Personalize project settings before they can be used. If this setting has not been activated, variant configurations will not be applied regardless of audience or experience configuration.

**Resolution**

1.  Navigate to your Personalize project settings.
    
2.  Locate the Entry Variants toggle and ensure it is enabled.
    
3.  Save the settings and return to the experience configuration.
    
4.  Verify that the variant entries are correctly linked to the relevant content entries and audiences.
    

After enabling entry variants, re-test the experience to confirm that the correct variant content is served to the targeted audience.

### cs-personalize Cookies Showing Multiple Variants

Browser cookies set by Contentstack Personalize (cs-personalize) contain multiple variant entries such as "4:0; 6:0; c:0" across different experiences. Users may be unsure whether this is expected behavior or a tracking error, and may be relying on cookies to determine which variant was actually displayed on a page.

**Root Cause**

The /manifest endpoint evaluates all active experiences for a user at runtime and returns variants for each applicable experience simultaneously. Cookies reflect all evaluated and active experiences, not just the one tied to the current page render. This is expected behavior and not a bug.

**Resolution**

1.  Do not rely on cs-personalize cookies to determine which variant was actually shown on a given page. Cookies reflect all experiences evaluated at manifest resolution time, not just what was rendered.
    
2.  To accurately track which variant was rendered, use the Content Delivery API (CDA) response. Extract the publish\_details.variants field from the entry response, which contains the actual variant aliases applied to the content that was returned.
    
3.  Trigger impression and conversion tracking events using the variant aliases extracted from publish\_details.variants, not from cookie values.
    
4.  Refer to the official impression tracking documentation for the recommended implementation pattern: https://www.contentstack.com/docs/personalize/dynamically-track-variant-impressions
    

Using publish\_details.variants from the CDA response ensures that tracking reflects exactly what was displayed to the user, preventing inflated or incorrect attribution.

### Personalizing Content with Contentstack Studio Components

In a React-based setup using Contentstack Studio, component properties do not support entry-level variants. This creates an apparent limitation where personalization cannot be linked directly to Studio-authored components, and authors cannot preview different personalization variants while composing in Studio.

**Root Cause**

Studio component properties are intentionally agnostic to personalization. Personalization (variants and audience targeting) is managed separately through the Visual Editor, not within Studio component definitions.

**Resolution**

1.  Do not implement variant logic inside Studio component definitions. Keep components agnostic — they should only map to the content schema.
    
2.  Manage all personalization configuration (variant groups, audiences, experiences) through the Personalize Visual Editor.
    
3.  At runtime, use the Personalize SDK to fetch the active variant alias for the current user.
    
4.  Pass the active variant alias to the useCompositionData hook. This ensures the correct personalized content is delivered automatically without requiring variant logic inside components.
    
5.  Use the Visual Editor (not Studio) to author, manage, and preview personalized experiences across different audience segments.
    

This architecture keeps Studio focused on page composition and structure while the Visual Editor handles all personalization logic, enabling both authoring flexibility and correct variant delivery.

### Conversions Not Displayed in Personalize Analytics Graph

The Personalize analytics dashboard does not display conversion data for an active A/B test, even though conversion events are being triggered correctly. The graph appears empty or shows zero conversions.

**Root Cause**

Conversions may not appear in the analytics graph when the selected date range in the dashboard does not cover the period in which the conversion events were registered. Filtering the view to a single day is a common cause of missing data.

**Resolution**

1.  Open the Personalize analytics dashboard for the affected experience.
    
2.  Verify the date range filter. Expand it to cover the full duration of the A/B test rather than a single day.
    
3.  Confirm the event name used in your conversion trigger matches the event name configured in the experience. A mismatch in event names (for example, click\_any\_insight vs a differently named event) will prevent conversions from being attributed.
    
4.  If conversions are still not appearing after adjusting the date range and verifying event names, open a support case with your Project ID, Experience ID, and the event name used, so backend logs can be checked to confirm whether events are being received.
    

If backend logs confirm that conversion events are registered but the dashboard still shows zero, the issue may require a platform-side investigation. Contact Contentstack Support with the above details.

### Variant "Not in Plan" When Using Non-Main Branch

Variants appear inaccessible or show a "not in plan" message when a user is working in a non-main branch of a Contentstack stack. Personalization variant configurations that were created on the main branch do not appear in other branches.

**Root Cause**

Variant groups, variants, and entry variants are supported exclusively on the main branch and are not cloned when new branches are created. This is a product limitation, not a configuration error.

**Resolution**

1.  Switch to the main branch of your stack to access variant configurations.
    
2.  Confirm that all personalization setup — including variant groups, variants, and entry variants — is performed exclusively on the main branch.
    
3.  Do not attempt to recreate variant configurations on non-main branches, as this is not supported.
    
4.  For testing purposes, use the main branch with appropriate environment or release configurations.
    

After switching to the main branch, variant configurations will be accessible and personalization will function as expected.

### Variants Fail After Recreating or Copying Entries

Personalization stops working after a user deletes and re-adds variants in a project, or after copying and pasting entries that contain variant references. Errors such as "The Variant 'cs01f9918869240cb0' does not belong to the Content Type 'multi\_teaser'" appear, or the Delivery API returns null for assets or embedded data that render correctly in Live Preview.

**Root Cause**

When variants are deleted and recreated, the platform generates new variant UIDs. Existing entries may still reference the old, now-invalid variant IDs — causing a mismatch that blocks personalization. Similarly, when entries are copied, variant references embedded in the copied content may point to UIDs that are no longer valid in the current project context, resulting in null responses from the Delivery API.

**Resolution**

1.  Identify the affected entry in the Contentstack CMS. Navigate to the entry's variant field and remove the current variant selection — this clears the stale reference.
    
2.  Re-select the correct variants from the updated list. The new variant UIDs will be written to the entry, replacing the stale references.
    
3.  Save and publish the entry, then verify that personalization is applied correctly.
    
4.  If the error persists after re-selecting variants, check the content type's Variant field configuration. If the field still references deleted variant groups, reconfigure it to point to the current variant group.
    
5.  As a last resort, create a new entry from scratch to ensure a clean variant mapping with no legacy references.
    
6.  For copy/paste errors where the Delivery API returns null for assets or embedded data: share comparative API responses (with and without the Personalize variant header), the Entry UID, Content Type UID, Variant UID, locale, environment, and asset publication status with Contentstack Support for further investigation.
    

If none of the above steps resolve the issue, open a support case. Provide the Project UID, Experience UID, Content Type UID, the exact error message, and — for copy/paste cases — redacted JSON responses showing the null values.

### Visual Experience Preview Not Refreshing When Audience Is Changed

In the Visual Experience editor, changing the selected audience in the preview pane does not update the displayed variants. The preview continues to show the same content regardless of which audience is selected. Direct API calls to the Personalize manifest may also return null variants when Lytics audiences are used in this context.

**Root Cause**

This issue has two related causes. First, the Live Preview SDK initialisation may be missing the required mode: 'builder' setting, which is needed for the Visual Experience editor to correctly override audience membership during preview. Without this setting, the preview environment cannot signal to the Personalize SDK that it should evaluate audience overrides interactively. Second, Lytics audiences may not be considered in manifest calculation when used for overriding audience membership in the Visual Experience context — this was a platform-level bug that has since been addressed with a fix pushed to production.

**Resolution**

1.  Review your Live Preview SDK initialisation code. Confirm that the init method includes mode: 'builder' in the configuration object. Without this setting, the Visual Experience editor cannot correctly override audience membership for preview purposes.
    
2.  Update the init call to include the mode setting and redeploy. Example: ContentstackLivePreview.init({ mode: 'builder', ... })
    
3.  After updating the init method, return to the Visual Experience editor, switch between audiences in the preview pane, and confirm that the displayed variants update accordingly.
    
4.  If variants are still null when calling the Personalize manifest directly with Lytics audiences after the init fix, verify that your environment is on the latest platform version, as the underlying Lytics manifest calculation fix has been deployed to production.
    
5.  If the issue persists in your specific environment, open a support case and reference the mode: 'builder' configuration and the Lytics audience manifest issue. Include your SDK version, Project UID, and a sample manifest API response.
    

Confirm the fix by switching audiences in the Visual Experience preview and verifying that the correct variant content is displayed for each audience selection.

## Lytics CDP & Integrations

### Lytics Login Failure for Users With Member Role

Accessing Lytics may fail for users who are assigned a Member role at the organization level within Contentstack. This prevents successful login to the Lytics platform despite the user being added to the Data Activation Layer (DAL).

**Root Cause**

The issue is caused by a permission restriction where the "Member" organization role does not provide sufficient privileges for standard Lytics authentication.

**Resolution**

1.  Check the user's organization-level role to determine if it is set to "Member".
2.  Coordinate with the Lytics engineering team to generate a manual OAuth login link for the affected user.
3.  Use the generated OAuth link to facilitate the initial login process.

After providing the OAuth link, attempt to log in to the Lytics platform. If the user successfully accesses the dashboard, the issue is resolved.

### Viewing Behavior and Interest Scores in Lytics Browser Extension

Exposing behavior and interest scores in the Lytics browser extension may require manual field mapping within the Public API settings. This prevents the real-time validation of user interest data during development and testing.

**Root Cause**

The issue is caused by the default Public API field configuration, which does not include behavioral and interest data points for external visibility in the Dev Tool extension.

**Resolution**

1.  Navigate to the Lytics Public API field configuration settings.
2.  Add the specific fields for behavior and interest scores to the allowed Public API fields list.
3.  Refresh the Lytics browser extension to sync the updated field permissions.
4.  Check the Dev Tool interface to ensure the scores are now visible.

After updating the Public API field configuration, open the Lytics browser extension on a tracked page. If the behavior and interest scores are displayed correctly within the extension interface, the issue is resolved.

### Field Mapping Requirements in Lytics CDP

Determining whether specific fields require manual mapping in Lytics CDP may be unclear when transitioning between standard integrations and custom data sources. This prevents the confident configuration of data ingestion streams without knowing which fields are automated by default.

**Root Cause**

Standardized integrations come with pre-configured default mappings to ensure immediate compatibility, whereas custom sources (like CSV uploads or custom APIs) do not have a predictable schema, making manual mapping necessary.

**Resolution**

*   Check if the data is being ingested through a standard stream like salesforce\_accounts, which utilizes default mappings.
*   Verify if the data source is a custom import to determine if manual mapping is required.
*   Use **Schema Copilot** to automatically suggest and define field mappings for non-standard data sources.
*   Refer to official Lytics documentation for a complete list of default fields and mapping behaviors for built-in integrations.

### Lytics Audiences Not Reflecting in Cookies During SSR Implementation

Implementing personalization in a Server-Side Rendering (SSR) environment may fail when Lytics audiences do not correctly appear in browser cookies. This prevents Personalize from identifying user segments, causing the site to display default content.

**Root Cause**

The issue is caused by a failure in the Lytics segment assignment process, where the user profile is not successfully associated with the target audience at the CDP level. Because the segmentation data never reaches the browser cookies, the downstream Personalize engine cannot trigger variant rules.

**Resolution**

1.  Check the Lytics dashboard to verify if the test user is successfully being added to the intended segment.
2.  Verify the Edge function and proxy configuration to ensure data is passing correctly between the server and the Lytics API.
3.  If the user does not appear in the Lytics segment, escalate the issue to the Lytics support team via a specialized Zendesk ticket.
4.  Provide the development domain and specific cookie screenshots to the Lytics team to facilitate troubleshooting.

### Retrieving Historical Event Data for Analytics Via Lytics

Using the Stream Events API to perform historical data analysis may result in incomplete data sets, as the endpoint typically returns only a small number of the most recent events. This prevents users from identifying long-term trends.

**Root Cause**

The issue is caused by a functional limitation of the Stream Events API, which is optimized for real-time validation and stream health monitoring rather than serving as a query engine for historical data.

**Resolution**

1.  Identify if the requirement is for real-time debugging or long-term historical analytics.
2.  If historical analysis is required, do not rely on the GET /v2/stream/{name}/events endpoint.
3.  Configure a data export to a warehouse such as **Google BigQuery** using Lytics' built-in integrations.
4.  Utilize the data warehouse's native SQL or querying tools to run analytics on the stored event data.
5.  Refer to the Lytics BigQuery documentation to set up the automated event dump.

### API Returns Null for activeVariantShortUid When Using Lytics Audiences

The Contentstack Personalize API returns null for activeVariantShortUid when Lytics-based audience conditions are in use. This blocks personalization testing and prevents variant evaluation from functioning correctly.

**Root Cause**

The null response is caused by missing audience slugs in the x-live-attributes request header. When Lytics audience conditions are used, the header must include the correct slug for each Lytics audience to allow the system to evaluate audience membership. Without valid slugs, audience conditions cannot be matched and the API returns null for the active variant.

**Resolution**

1.  Open browser developer tools or your API client and inspect the request header for the failing API call. Check whether x-live-attributes contains audience slugs for all Lytics-based audiences used in the experience.
    
2.  Navigate to the Lytics dashboard and retrieve the correct slug for each audience used in the experience configuration.
    
3.  Update your API request or cURL command to include the correct audience slugs in the x-live-attributes header.
    
4.  Retry the API call and confirm that activeVariantShortUid is now returned with a non-null value.
    

After passing the correct audience slugs in x-live-attributes, the API will correctly evaluate audience membership and return the active variant. If the issue persists after updating slugs, verify that the audience configuration in Lytics is active and that the slugs match exactly.

### Object/Map Type Attributes Not Supported in Personalize

Attempting to create a custom attribute in Personalize with an object or map type to target variants based on complex Lytics data (such as a date or nested key-value structure) results in an error or the attribute not being available for variant targeting. This blocks use cases that require gating content based on structured user attributes.

**Root Cause**

Contentstack Personalize does not support object-type attributes. Additionally, variants must be linked to audiences — they cannot be targeted directly off a raw attribute value. The intended data must be sent as a scalar key-value pair and evaluated through a Lytics audience before it can drive variant selection.

**Resolution**

1.  Instead of sending the attribute as a complex object, send it as a key-value scalar pair using the jstag.send() method. For example, send an unlocked\_until date as a plain date-type value rather than a nested object.
    
2.  In the Lytics dashboard, create a field and mapping for the new scalar attribute.
    
3.  Create a Lytics audience based on the attribute value. For example, define an audience for users where unlocked\_until is before Today to identify users with active access.
    
4.  In Personalize, create a Segmented Experience with a single variant linked to that Lytics audience. Users in the audience receive the gated variant; all other users receive the fallback content.
    
5.  For multiple gated pages or URL-based use cases, repeat the above steps with separate key-value pairs, field mappings, and audiences for each page or condition.
    

Refer to the Lytics Fields & Mappings documentation for details on creating custom fields and audience definitions.

### S3 Ingestion Minimum Scheduling Interval Is One Hour

Organizations using S3 ingestion to synchronize profile data into Contentstack Personalize (via Lytics) require near-real-time data freshness but are limited to a minimum scheduling interval of one hour. Shorter intervals of 15 or 30 minutes are not currently available through the standard configuration.

**Root Cause**

The minimum supported scheduling interval for S3 ingestion in Lytics is one hour. Sub-hourly scheduling is not currently a supported configuration option for this ingestion method.

**Resolution**

1.  If hourly ingestion is insufficient for your use case, contact Contentstack Support and raise a request to explore sub-hourly S3 ingestion options. This request will be escalated to the Lytics team for assessment.
    
2.  As an interim approach, consider aggregating profile updates into a single hourly batch to maximize the relevance of each ingestion run.
    
3.  Evaluate whether the Lytics Attribute API or Cloud Connect can be used to push attribute updates on a more frequent or event-driven basis, bypassing the S3 scheduling constraint for time-sensitive data.
    
4.  For near-real-time attribute updates tied to specific user events, use the Personalize Edge API (PATCH /user-attributes) to push individual attribute changes as they occur, rather than relying on scheduled batch ingestion.
    

Sub-hourly S3 scheduling is a platform enhancement under consideration. Check with Contentstack Support for the current status of this capability.

### Pre-Computing and Bulk-Syncing User Attributes into Personalize

Organizations that calculate user attributes offline or in batch (not in real-time) need to sync these pre-computed values into Contentstack Personalize before a user starts an active session. There is uncertainty about whether a batch API or server-side mechanism exists for this use case.

**Root Cause**

This is an architectural question rather than a bug. "Data in Contentstack Personalize" is stored and managed via Lytics. Syncing attributes to Lytics automatically makes them available to Personalize. Separately, the Personalize Edge API supports a request-time pattern for setting attributes per user session.

**Resolution**

1.  To pre-load user attributes before a session, sync the data directly into Lytics rather than using the Personalize Edge API. Data synced to Lytics is automatically available to Personalize.
    
2.  Use Lytics Cloud Connect or the Lytics Attribute API to perform bulk attribute imports. These tools support server-side and scheduled data pushes without requiring an active user session.
    
3.  If you are using the request-time pattern (PUT /user-attributes followed by GET /manifest), be aware that a race condition is theoretically possible. To mitigate this, ensure attributes are set before the manifest request is made, and treat the /user-attributes call as a prerequisite step in your request flow.
    
4.  Note that the Personalize Edge API is scheduled for deprecation in favor of a Lytics-first data model. Begin transitioning attribute management to Lytics to ensure long-term compatibility.
    

For bulk pre-computed attribute scenarios, Lytics Cloud Connect or the Attribute API is the recommended approach. Contact Contentstack Support for guidance on configuring the correct Lytics ingestion method for your data architecture.

### Country-Based Audience Count Discrepancy Compared to Other Analytics Tools

The audience count for a country-based Personalize segment appears significantly lower than the equivalent metric in a third-party analytics platform such as Google Analytics or Adobe Analytics. The audience conditions appear to be configured correctly using the country attribute.

**Root Cause**

Discrepancies between Personalize audience counts and external analytics tools are typically caused by differences in how each platform resolves geolocation data. Personalize derives country information from the visitor's IP address using an integrated geolocation database. If an IP address cannot be accurately mapped to a country in that database, the visitor will not be attributed to the country-based audience, resulting in lower counts compared to tools that use different resolution methods.

**Resolution**

1.  Verify the audience conditions in Personalize to confirm the country attribute is configured correctly and is not filtering out valid traffic unintentionally.
    
2.  Use a VPN set to the target country and test whether you are correctly placed into the country-based audience. A successful match confirms the audience condition is working for resolvable IP addresses.
    
3.  Acknowledge that perfect parity between Personalize audience counts and external analytics tools is not expected, as each platform uses different data sources and geolocation resolution methods.
    
4.  If the discrepancy is significantly larger than expected (for example, more than 20-30%), open a support case with your Project UID, Experience UID, the specific audience condition, and a sample of request logs showing the country attribute values being passed.
    

Geolocation-based audience discrepancies are expected to some degree. If the miss rate is outside acceptable bounds for your use case, consider supplementing IP-based geolocation with an explicit country attribute passed from your own infrastructure (for example, from a CDN header such as Cloudflare-IPCountry).

### Data & Insights (Lytics) Audience Unavailable

When working in Personalize, you may encounter one of the following error messages:

*   Some Lytics audiences are unavailable. Active experiences may not behave as expected.
*   Linked audience(s) from Data & Insights (Lytics) are unavailable.

These errors indicate that one or more Lytics audiences referenced in your Personalize experiences can no longer be resolved.

**Root Cause**

This error occurs for one of two reasons:

*   **Missing DAL connection:** The Personalize project is no longer connected to an active Data Activation Layer (DAL), so audiences cannot sync from Lytics.
*   **Audience deleted in Lytics:** The audience referenced in the experience was removed from the Lytics dashboard.

**Resolution**

1.  Navigate to **Org Admin** settings, open the **Data Activation Layer** section, and click **Edit** on your DAL connection. Click **Test Connection** to verify it is active. If the connection is broken, reconnect your Personalize project to the correct DAL.
2.  Log in to your Lytics dashboard and navigate to **Using Profiles > Audiences**. Search for the audience referenced in the affected experience.
3.  If the audience is missing, either recreate it in Lytics and relink it in Personalize, or replace it with another active audience.
4.  Once the correct audience is in place, resolve the experience based on its current state:
    *   **Draft:** Edit the existing draft to point to the new or replacement audience.
    *   **Paused:** Create a new draft with the correct audience before reactivating the experience.
    *   **Active:** Pause the experience, create a new draft linked to the correct audience, then reactivate.

## Visual Builder & Preview

### Unable to Edit Entries in Visual Builder

Editing entries within the Visual Builder interface may fail to function correctly. This issue prevents users from restoring or using full editing capabilities while working in the interface.

**Root Cause**

This is typically caused by a version mismatch in the initialization method. Using an outdated version of the Live Preview SDK leads to compatibility failures within the Visual Builder.

**Resolution**

1.  Update the Live Preview SDK to the latest available version.
2.  Verify that the init method in your code is aligned with the current implementation requirements.

After updating the SDK and the init method, open the Visual Builder and attempt to edit an entry. If the editing functionality works as expected, the issue is resolved.

### Non-interactive Elements in Shared Preview Links

When loading a shared preview link, interactive page elements—such as accordions, modals, or links—may become non-functional. This prevents stakeholders from fully testing the user experience within the preview context.

**Root Cause**

This issue is generally caused by external environment or public link (publink) configurations that interfere with client-side script execution, rather than a defect within Contentstack.

**Resolution**

1.  Verify if the shared URL is a valid public link and ensure it is loading successfully.
2.  Coordinate with your development team to ensure the sandbox environment is configured to support interactive elements.
3.  Check the preview link access settings to ensure all required scripts and styles are permitted to load.

Navigate to the shared preview link and attempt to trigger an interactive element, such as a modal. If these elements function correctly, the issue is resolved.

### Visual Builder Experiences Failing to Apply Due to CDA Personalization Limits

Active experiences created in the Visual Builder may fail to apply to a live website if the project exceeds the established personalization limits within the Content Delivery API (CDA). This results in only top-priority variants being displayed, while others are ignored during delivery.

**Root Cause**

The CDA has a hard cap on the number of active experiences allowed per request. Every experience passed in a request counts toward this limit (previously set to 5), regardless of whether a specific entry has a personalized variant defined for it. When a project contains more experiences than this cap, the additional variants are not rendered.

**Resolution**

1.  Review your project configuration to determine the total number of active experiences requested via the CDA.
2.  Confirm if the total number of experiences exceeds the current system limit of 5.
3.  Submit a request to Contentstack support to increase the personalization limit for your specific project (e.g., increasing the limit to 10).

Once the limit has been increased, reload the target page. If all active experiences are correctly evaluated and visible on the site and within the Visual Builder, the issue is resolved.

## Platform Settings & Permissions

### Unable to Access Data Activation Layer in Stack Settings

Users may find that they cannot access the Data Activation Layer (DAL) within individual stack settings, even if the feature is enabled for the account. This prevents the configuration of data activation features.

**Root Cause**

The Data Activation Layer is an organization-level configuration rather than a stack-level setting. The issue typically arises from a misunderstanding of the feature hierarchy.

**Resolution**

1.  Navigate to the **Organization Admin** settings instead of individual stack settings.
2.  Locate the **Data Activation Layer** section within the organization-level configuration menu.
3.  Verify that the necessary permissions are active at the organization level to view the feature.

After navigating to the Organization Admin settings, check for the Data Activation Layer option. If the feature is visible and accessible in this location, the issue is resolved.

### Difficulty Activating Data Layer Without Launch Project Selection

Activating the Data Layer in Personalize may appear to require a Launch project selection, even when using external tools like Google Tag Manager. This prevents setup completion if Launch is not part of the tech stack.

**Root Cause**

This issue is caused by client-side caching.

**Resolution**

1.  Check the current browser cache and clear it to ensure the latest interface state is loaded.
2.  Attempt to activate the Data Layer without selecting a Launch project to verify if the requirement persists.
3.  Coordinate a troubleshooting call to observe the behavior in real-time if the interface does not allow progression.

After clearing the client-side cache, navigate to the Data Layer activation screen. If the Data Layer can be activated without selecting a Launch project, the issue is resolved.

### Authentication Failure for Certification Portal Access

Accessing the Data & Insights Practitioner Certification portal may fail if the user's account is not correctly associated with an active Contentstack Organization. This prevents practitioners from completing certification milestones despite having valid Partner Hub credentials.

**Root Cause**

The issue is caused by a missing Organization (ORG) association. Even with access to external partner tools, the certification portal requires the user to be a member of a registered Organization within the Contentstack ecosystem to validate identity and permissions.

**Resolution**

1.  Check if the user is attempting to use Partner Hub credentials on the certification portal without being linked to an ORG.
2.  Verify the user's account status in the internal system to see if they are a member of any active Organization.
3.  If no Organization is found, advise the user to contact their internal Organization administrator to be added as a member.
4.  If the user is the primary contact for a new organization, initiate the standard onboarding or invitation process to establish the Organization link.

### Role Restriction Error When Accessing Data & Insights Tab

Users assigned to the "Member" role at the organization level may be blocked from accessing the Data & Insights (D&I) tab within Personalize. This results in a "role restriction" error, preventing users from viewing audience analytics.

**Root Cause**

The issue is caused by insufficient role privileges. The standard "Organization Member" role does not include the necessary permissions by default to authenticate into the integrated Lytics environment that powers Data & Insights.

**Resolution**

1.  Confirm the user is encountering a "role restriction" error when attempting to access the Data & Insights tab.
2.  Verify the user is assigned the "Member" role at the organization level.
3.  Coordinate with the Lytics engineering or support team to generate a manual OAuth login link specifically for the affected user.
4.  Provide the generated OAuth link to the user to bypass the standard UI authentication restriction.

Provide the user with the OAuth link and ask them to attempt access. If the user successfully reaches the Data & Insights dashboard, the issue is resolved.

### Conditional Rules Failing to Hide File Field Options

Configuring conditional rules in Personalize may fail to hide specific options, such as "transparent background," when field-level validations are active. This prevents the enforcement of UI logic intended to restrict choices based on a selected variant.

**Root Cause**

The issue is caused by a system limitation where active validations on a file field interfere with the ability of conditional rules to hide or modify available options.

**Resolution**

1.  Navigate to the content type or field settings and temporarily remove all validations from the affected file field.
2.  Create and save the conditional rule intended to hide options for the specific variant.
3.  Re-enable the previously removed field-level validations.
4.  Verify that the rule remains active and functional after the validations are restored.

After temporarily removing validations and setting the rule, navigate to the entry editor and select the target variant. If the specific file field options are successfully hidden while validations are active, the issue is resolved.

### Cannot Access Personalize Feature - Org Admin Rights Required

A user is unable to access the Contentstack Personalize feature despite being a member of the organization. Personalize does not appear or is inaccessible from the user's account.

**Root Cause**

Access to Contentstack Personalize requires organization admin or owner rights. Regular organization member roles do not grant access to the feature.

**Resolution**

1.  Verify the user's current role in the Contentstack organization settings. If the role is "Member" rather than "Admin" or "Owner," the user will not be able to access Personalize.
    
2.  Request that an existing organization admin or owner elevate the user's role to admin, or add the user as a collaborator on the specific Personalize project.
    
3.  Once the role is updated, ask the user to log out and log back in, then navigate to the Personalize section to confirm access.
    

Organization admins and owners have full access to Personalize. Collaborators added to a specific project can view and work within that project. Members without either role will not see or be able to access Personalize.

### Unable to Create Personalize Projects - Must Be Org Admin or Owner

A user is unable to create a new Personalize project despite having access to the Personalize section. The create action is not available or results in a permission error.

**Root Cause**

Creating a Personalize project requires organization admin or owner rights. Users who are collaborators on an existing project can view it but cannot create new projects. Regular members cannot create or view Personalize projects.

**Resolution**

1.  Confirm the user's role within the Contentstack organization. Project creation requires the admin or owner role.
    
2.  If the user needs to create projects, an existing admin or owner must promote the user's role in the organization settings.
    
3.  If the user only needs to view or contribute to an existing project, an org admin can add them as a collaborator on that specific project without changing their organization role.
    
4.  After the role or collaborator status is updated, the user should refresh the Personalize dashboard and verify that the create project option is now available.
    

Role changes in Contentstack take effect immediately. The user does not need to wait for a cache refresh, but logging out and back in ensures the updated permissions are reflected.

### Cannot Create Personalize Project - Organization Project Limit Reached

A user with the correct admin or owner permissions is unable to create a new Personalize project. All prerequisites appear to be in place but project creation fails or the option is unavailable.

**Root Cause**

Each Contentstack organization has a maximum limit on the number of Personalize projects that can be created. Attempts to create additional projects beyond this limit will fail. The default limit may be set to a low number (for example, 1 or 2 projects) and must be increased by Contentstack Support.

**Resolution**

1.  Confirm that the user attempting to create the project has organization admin or owner rights. Rule out a permissions issue before escalating the project limit.
    
2.  Count the current number of active Personalize projects in the organization. If the number equals or exceeds the configured limit, project creation will be blocked.
    
3.  Open a support case with Contentstack and request an increase to the Personalize project limit for your organization. Include your Organization UID and the desired new limit.
    
4.  Once the limit has been increased, retry project creation from an admin or owner account.
    

Project limit increases are applied at the organization level by Contentstack Support. There is no self-service option for adjusting this limit.

## External CDN & Architecture

### Variant Resolution Broken When External CDN (Akamai) Sits in Front of Launch

When an external CDN such as Akamai is placed in front of Contentstack Launch, personalized variant resolution may not work as expected. Experience splits (for example, 33/33/33 A/B distributions) do not behave correctly because cached content is served without re-evaluating the Personalize SDK per visitor.

**Root Cause**

The documented Contentstack Launch + Personalize architecture assumes that Launch's Edge Proxy runs the Personalize Edge SDK before any personalized HTML or API response is returned. When Akamai caches the response after the first request and serves it to subsequent visitors, the Personalize SDK is not re-executed per visitor — so variant selection does not occur for cached requests. Using a Vary header affects cache keys only and does not cause the Personalize SDK to execute.

**Resolution**

1.  Prefer using Contentstack Launch as the delivery edge for all hostnames serving personalized pages. Avoid placing a second CDN in front of Launch for personalized routes where possible.
    
2.  If Akamai must remain in front of Launch, do not cache personalized routes at Akamai. Apply Cache-Control: no-store on HTML responses for personalized pages and on any personalized API responses. Ensure Akamai is configured to honour origin cache-control headers for these routes.
    
3.  Static assets (images, stylesheets, scripts) can still be cached aggressively at Akamai — apply no-cache policies only to routes that serve personalized content.
    
4.  If you require per-visitor variant evaluation at the Akamai layer, explore Akamai EdgeWorkers as a custom solution. Note that EdgeWorkers are a customer-owned design and Contentstack does not provide a supported integration for this pattern. Professional Services can be engaged if needed.
    
5.  Confirm the final architecture with your team and reopen the support case if additional clarification is required.
    

The safest and most supported architecture for Personalize is using Contentstack Launch as the sole edge delivery layer. CDN bypass rules for personalized routes are the recommended interim solution when a second CDN cannot be removed.

### Geolocation Country Code Not Accessible via Personalize SDK at Runtime

A developer needs to access the visitor's resolved country code at runtime in a Next.js application to pass it as a parameter to an external API call. Contentstack Personalize is already configured with location-based targeting (Country/Region/City) but the SDK does not appear to expose the resolved geolocation value programmatically.

**Root Cause**

Contentstack Personalize uses geolocation data internally for audience evaluation only. The resolved country code is not exposed via the Personalize SDK for external consumption at runtime. The SDK provides variant delivery, not raw geolocation data.

**Resolution**

1.  Do not rely on the Personalize SDK to expose geolocation data for non-audience use cases. The SDK is not designed for this purpose.
    
2.  Implement independent geolocation resolution in your Next.js application. The recommended approaches are:
    

*   Use the Cloudflare-IPCountry request header if your application is deployed behind Cloudflare. This header contains the two-letter country code resolved by Cloudflare's network and is available at the edge.
    
*   Use the x-vercel-ip-country header if deploying on Vercel. This header is automatically populated by Vercel's infrastructure.
    
*   Integrate a third-party geolocation API (for example, MaxMind GeoIP2 or ip-api.com) within your Next.js middleware or API route to resolve the country code server-side before rendering.
    

3\. Pass the resolved country code from your chosen geolocation source to the external API call as required by your implementation.

Using a CDN or infrastructure-level geolocation header is the most performant approach for Next.js applications, as the country code is resolved at the network edge without an additional API call.

## Webhooks & External Integrations

<!-- case:00061371 status:draft synced:false bucket:"Webhooks & External Integrations" -->
### Configuring Webhooks to Trigger on Variant Publish Events

Publishing updates to a variant entry may not trigger downstream webhook-driven processes, even when publishing the equivalent base entry does trigger them.

**Root Cause**

Variant publish and unpublish events use separate webhook channels from the base entry's publish and unpublish channels. A webhook configured only for base entry events does not fire for variant-only updates.

**Resolution**

1.  Open the webhook configuration and review which publish/unpublish channels are currently selected.

2.  Add the variant-specific publish/unpublish channels alongside the existing base entry channels, scoped at the content type or entry level so all variants within that scope are covered.

3.  Save the webhook configuration.

After adding the variant publish/unpublish channels to the webhook, publish an update to a variant entry. If the webhook now fires as expected, the issue is resolved. Escalate with the webhook UID and content type UID if variant-only updates still don't trigger it.

<!-- end:00061371 -->