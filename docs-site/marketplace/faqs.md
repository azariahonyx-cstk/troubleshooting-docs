---
title: "Marketplace Troubleshooting Guides"
description: "Discover answers to common troubleshooting questions about Marketplace."
url: "https://www.contentstack.com/docs/marketplace-troubleshooting/faqs"
product: "Contentstack"
doc_type: "guide"
audience:
  - developers
  - admins
version: "current"
last_updated: "2026-07-27"
---

# Marketplace Troubleshooting Guides

## App Installation & Configuration

### App Installation Fails with "Type Error" (Invalid JSON)

Users encounter a TypeError during the installation of Marketplace apps when the configuration parameters do not match the expected JSON schema. This often happens when a string is provided where a JSON object is required.

**Resolution**

1.  Review the app's configuration documentation for required field formats.
2.  Ensure that complex fields, such as proxies or custom headers, are wrapped in valid JSON curly braces {}.
3.  Validate your JSON input using an external linter before saving the app configuration.

**Verification**

The app saves successfully, and the "Installation Complete" message appears without console errors.

**Note**

If valid JSON still triggers a type error, provide the configuration snippet and the specific app name to the support team.

### Marketplace App Limits: "Maximum Apps Installed"

A "Limit Exceeded" error appears when trying to install a new app from the Marketplace.

**Resolution**

1.  Review your current **Subscription Plan** to see the allowed number of Marketplace app installations.
2.  Uninstall unused apps to free up slots for new installations.
3.  Contact your account manager if you require a limit increase for your organization.

The "Install" button becomes active after removing an existing app.

### Marketplace App "Save" Button is Disabled

Users cannot save changes to app configurations because the "Save" button remains greyed out.

**Resolution**

1.  Ensure all **Required Fields** (marked with a red asterisk) are filled.
2.  Check for validation errors in input fields, such as invalid URL formats or out-of-range numbers.
3.  Verify that you have "Admin" or "Owner" permissions for the stack.

The "Save" button becomes blue/active once all validation criteria are met.

### Missing App Settings After Re-installation

When an app is uninstalled and then re-installed, all previous configuration settings are lost.

**Resolution**

1.  This is expected behavior; app settings are stored per installation instance.
2.  Before uninstalling, manually back up any complex configuration JSON or API keys.
3.  Use the "Update" feature instead of "Uninstall/Reinstall" if you are just changing versions.

The new installation is configured using the backed-up settings.

## App Permissions & UI Visibility

### "Invalid API Key" Error in Public App Dashboard

A public app fails to load data, displaying an "Invalid API Key" error within its custom UI. This occurs when the app's internal token does not have permission for the specific stack or region.

**Resolution**

1.  Confirm the stack is in the same **Region** (US, EU, or Azure) as the app's registration.
2.  Check the **Stack Settings** to ensure the app has been granted "Read" permissions for the necessary content types.
3.  Re-install the app to refresh the automatically generated installation token.

The app dashboard populates with content from the stack successfully.

### App Sidebar Widget Not Displaying in Entry Editor

An installed sidebar app (e.g., SEO or Translation apps) does not appear in the entry editor sidebar for certain users.

**Resolution**

1.  Verify that the user's **Role** has "App Access" enabled in the Organization settings.
2.  Check the **App Configuration** to ensure it is assigned to the specific Content Type being edited.
3.  Refresh the browser to clear any cached UI states.

The app icon appears in the right-hand sidebar of the entry editor.

### Marketplace App Permissions: "403 Forbidden"

An app fails to perform actions (like updating an entry) and returns a 403 error, despite being installed.

**Resolution**

1.  Apps use **Management Tokens** with specific roles. Ensure the role assigned to the app during installation has "Write" access.
2.  If the app uses a **User Token**, ensure the user who installed the app has not been removed from the stack.
3.  Update the app's permissions in the **Stack > Settings > Apps** section.

The app successfully performs the restricted action (e.g., saving an entry).

### App UI Not Reflecting Localized Field Changes

A Marketplace app shows the same content across all locales, failing to reflect changes made in non-master languages.

**Resolution**

1.  Ensure the app's API queries include the locale parameter.
2.  The app must be configured to handle the specific locale code (e.g., ja-jp).
3.  Verify that the content has been published in the target locale.

Switching locales in the entry editor causes the app to display the corresponding localized data.

## Custom App Development & Extensions

### Implementing the Marketplace DateTimePicker component with input fields

Using the DateTimePicker component in a custom extension may result in a missing input field or non-functional action buttons when manual integration is not performed. This prevents users from interacting with the picker or handling date and time values.

**Root Cause**

The DateTimePicker component does not provide a native input field or automatic button handlers, requiring manual configuration and pairing with separate UI elements.

**Resolution**

1.  Integrate a standard HTML input field manually into the extension code.
2.  Configure the input field to trigger the DateTimePicker modal upon interaction.
3.  Use separate DatePicker and TimePicker components if the application requires distinct date and time inputs.

After integrating the manual input field, click the field to verify the DateTimePicker modal opens.

If the onDone and onCancel buttons correctly process the input data, the manual integration is successful.

### Resolving infinite request loops in Marketplace boilerplate apps

Developing a custom app using the Marketplace boilerplate may trigger an infinite loop of requests on the App Configuration page. This prevents the configuration UI from loading or functioning correctly.

**Root Cause**

The installationData object is incorrectly included in the dependency array of a useEffect hook, causing the component to re-render and re-execute requests endlessly.

**Resolution**

1.  Open the AppConfigurationExtensionProvider.tsx file in the boilerplate source code.
2.  Locate the useEffect hook responsible for handling installation data or configuration requests.
3.  Remove installationData from the hook's dependency array.
4.  Redeploy the application to verify the fix.

After removing the dependency from the code, navigate to the App Configuration page of the custom app.

If the network tab shows a stable number of requests without an infinite loop, the render logic is corrected.

### Fixing syntax errors in DAM boilerplate app SDK initialization

Integrating a DAM boilerplate app may result in syntax errors during initialization when the target origin is not properly configured. This prevents the app from communicating with the Contentstack UI.

**Root Cause**

The application SDK uses a placeholder string for the target origin URL in its postMessage configuration, which the browser fails to validate as a legitimate domain.

**Resolution**

1.  Open the source code where the @contentstack/ui-extensions-sdk is initialized.
2.  Locate the configuration object or initialization function containing the target origin parameter.
3.  Replace the placeholder text "YOUR CUSTOM FIELD DOMAIN URL" with the specific Contentstack app domain URL (e.g., [app.contentstack.com](https://app.contentstack.com/)).
4.  Save the changes and rebuild the application.

After replacing the placeholder URL, open the DAM app within the Contentstack environment.

If the syntax error no longer appears in the console and the app loads correctly, the SDK is properly initialized.

### Resolving Global Field save failures and extension errors

Saving Global Field entries may fail with an error referencing a non-existent extension ID when specific experimental features are enabled. This prevents users from updating content model components.

**Root Cause**

The error is caused by a known defect in the Nested Global Fields feature, which incorrectly attempts to reference internal extension IDs that do not exist in the stack.

**Resolution**

1.  Navigate to the stack settings or contact support to access feature flags.
2.  Locate the "Nested Global Fields" enablement setting.
3.  Disable the feature to stop the system from referencing non-existent extension IDs.
4.  Attempt to save the Global Field entry again.

After disabling the Nested Global Fields feature, open a Global Field and attempt to save a change.

If the "Failed to update" error no longer appears, the reference mismatch is resolved.

### Configuring csdx CLI for regional GraphQL typing generation

Using the ts-gen plugin with the GraphQL flag may return an "API not available" error in specific regions like Azure EU. This prevents the generation of TypeScript typings for regional stacks.

**Root Cause**

The Contentstack CLI (csdx) defaults to the North American region unless explicitly configured, causing plugins to fail when communicating with regional endpoints.

**Resolution**

1.  Open a terminal or command prompt where the Contentstack CLI is installed.
2.  Execute the configuration command to set the region to your specific environment: csdx config:set:region AZURE-EU.
3.  Re-run the ts-gen command with the --api-type graphql flag.

After setting the CLI region, execute the ts-gen command again for the regional stack.

If the TypeScript typings are generated without the region availability error, the CLI configuration is correct.

### Trados project creation fails due to release field validation

Creating a project using the Trados integration may fail if the "Create Project" button remains disabled or returns a "Project Creation failed. Item not found in a release" error. This prevents users from initiating the translation workflow through the plugin.

**Root Cause**

The Trados plugin UI requires an existing release containing the source entries to satisfy validation requirements, even when a new release name is provided for the translated content.

**Resolution**

1.  Create a release within the Contentstack stack.
2.  Add all entries from the source locale intended for translation into the created release.
3.  Navigate to the Trados plugin dashboard.
4.  Select the release containing the source entries from the plugin dropdown menu.
5.  Enter a unique name for the translated release in the "Create Release" field.

After creating the source release and selecting it in the plugin, verify that the "Create Project" button is enabled. If the project is created successfully, the issue is resolved.

## Performance, Webhooks & Network Errors

### Webhook Failures for Marketplace Apps

Marketplace apps that rely on webhooks (e.g., Slack or Microsoft Teams notifications) stop sending updates.

**Resolution**

1.  Check the **Webhook Logs** in the Stack settings for failed delivery attempts.
2.  Verify that the app's target endpoint is not blocking Contentstack's IP addresses.
3.  Ensure the webhook status is set to "Enabled".

Trigger a test event (like an entry publish) and check if the app receives the notification.

### App Dashboard Slow Performance (High Latency)

Marketplace apps take a long time (up to 3 minutes) to load their dashboards.

**Resolution**

1.  Check the size of the data being requested; minimize deep reference nesting in the app's initial fetch.
2.  Verify the status of the app's external hosting provider (e.g., AWS, Vercel).
3.  Implement caching on the app's backend to reduce frequent API calls.

The app dashboard loads in under 5 seconds on subsequent refreshes

### "Bad Gateway" (502) Errors on Public App UI

A public app displays a "502 Bad Gateway" error instead of its dashboard.

**Resolution**

1.  This usually indicates the app's hosting server (outside of Contentstack) is down or crashing.
2.  Check the server logs for the app's hosting environment for memory or timeout errors.
3.  Ensure the server is capable of handling the current volume of requests.

The app UI loads after the hosting server is restarted or scaled.

### Marketplace App Assets Not Loading (HTTPS/SSL)

Images or styles within a Marketplace app fail to load, with browser errors regarding "Mixed Content".

**Resolution**

1.  All assets used by the app must be served over **HTTPS**.
2.  Verify that the hosting server has a valid SSL certificate.
3.  Check for hardcoded http:// links in the app's source code and update them to https://.

All app assets load without security warnings in the browser.

### Retrieving full entry data in translation webhook payloads

Receiving webhook notifications for translation events may result in missing translatable fields when payload settings are restricted. This prevents external systems from accessing the full entry content required for translation.

**Root Cause**

The "Concise Payload" configuration option is enabled, which limits the webhook response to a minimal set of metadata instead of the full entry body.

**Resolution**

1.  Navigate to the Webhook configuration page in the stack settings.
2.  Locate the specific webhook used for the translation workflow.
3.  Uncheck the "Concise Payload" checkbox to allow the transmission of the full entry details.

After disabling the concise payload option, trigger a translation event and inspect the webhook logs.

If the payload contains the full set of translatable fields, the configuration update is successful.

## Vendor-Specific Integrations

### Algolia App: "Index Not Found" During Configuration

When configuring the Algolia Marketplace app, the "Index" dropdown is empty or returns an error.

**Resolution**

1.  Verify the **Algolia API Key** and **Application ID** provided in the app settings.
2.  Ensure the API Key has "List Indices" permissions in the Algolia dashboard.
3.  Check if the index was recently created; it may take a few minutes to appear in the API response.

The dropdown correctly lists the available Algolia indices.

### Resolving language mismatches in RWS Trados Marketplace integration

Integrating RWS Trados in a stack may fail when the master language is set to a generic locale not supported by the vendor. This prevents the selection of source content for translation projects.

**Root Cause**

The third-party translation tool requires region-specific language variants (such as en-us) and does not recognize generic root locales (such as en).

**Resolution**

1.  Create a new regional language variant, such as English - United States (en-us), within the stack settings.
2.  Configure the generic master language (en) as the fallback for the newly created regional locale.
3.  Select the regional locale when initiating translation projects through the Trados app.

After creating the regional locale with a fallback, navigate to the Trados app and attempt to select the language.

If the language appears as an available option and allows project creation, the mismatch is resolved.

### Resolving project creation failures in the Trados integration

Creating a translation project in the Trados Marketplace app may fail with disabled buttons or "Item not found" errors when source entries are not properly grouped. This prevents the initiation of translation workflows for selected content.

**Root Cause**

The integration requires source entries to be associated with a specific Contentstack release that must be selected within the plugin UI to enable project validation.

**Resolution**

1.  Create a new release within the Contentstack stack.
2.  Add all entries from the source locale that require translation into this release.
3.  Navigate to the Trados plugin dashboard and select the created release from the dropdown menu.
4.  Enter a unique name for the target translated release in the "Create Release" field.

After selecting the source release and providing a target release name, check if the "Create Project" button becomes enabled.

If the project creation proceeds without "Item not found" errors, the release-based workflow is correctly configured.

### Resolving validation errors in Salesforce Commerce app configuration

Configuring the Salesforce Commerce Marketplace app may result in a disabled save button and "valid inputs" validation error when credentials are incomplete. This prevents the storage of integration settings within the stack.

**Root Cause**

The app performs real-time client-side validation, blocking the save action if required fields like Organization ID or Site ID are missing or if the Client ID does not match the Short Code.

**Resolution**

1.  Navigate to the Salesforce Commerce app configuration page.
2.  Enter all required fields: Client ID, Client Secret, Organization ID, Short Code, and Site ID.
3.  Ensure that the Client ID specifically corresponds to the Short Code provided by the Salesforce environment.
4.  Verify that the SLA key is set to private and generate a new secret if the current one is invalid.

After entering all required credentials correctly, hover over the Save button in the app configuration.

If the "testConfig" error message disappears and the Save button becomes clickable, the validation is satisfied.

### Resolving Duplicate site id errors in Salesforce Commerce

Adding a new configuration in the Salesforce Commerce connector may fail with a duplicate ID error when the same Site ID is reused. This prevents the setup of multiple environments within the same stack.

**Root Cause**

The connector enforces a strict uniqueness constraint on Site IDs, prohibiting the use of the same ID across different configurations even if they utilize different client IDs or environments.

**Resolution**

1.  Identify the existing configurations within the Salesforce Commerce app to see which Site IDs are currently in use.
2.  Contact the Salesforce Commerce Cloud (SFCC) administrator.
3.  Request the creation of unique Site IDs for each distinct environment (e.g., staging, production).
4.  Enter the new, unique Site ID in the configuration fields in Contentstack.

After obtaining a unique Site ID, attempt to save the new configuration in the Salesforce Commerce app.

If the "Duplicate site id" error does not appear and the configuration saves successfully, the unique ID requirement is met

### Resolving 40KB JSON field size errors in Shopify extensions

Integrating multiple Shopify stores may trigger a 40KB size limit error when syncing large product datasets to an entry. This prevents the saving of entries containing extensive third-party product metadata.

**Root Cause**

The error occurs because the integration attempts to store the entire Shopify product JSON payload in a single field, which exceeds Contentstack's strict system storage constraints.

**Resolution**

1.  Navigate to the configuration page of the Shopify custom field within the content type.
2.  Review the data mapping settings to identify the fields currently being synchronized.
3.  Select only the specific fields required for your implementation (e.g., product title, SKU, or price) instead of the full dataset.
4.  Save the field configuration to reduce the total payload size stored within the entry.

After limiting the stored fields, attempt to select a product from the Shopify store and save the entry.

If the entry saves successfully without a 40KB size error, the payload is correctly optimized for system limits.

<!-- case:00060653 status:draft synced:false bucket:"Vendor-Specific Integrations" -->
### Brightcove App Returns 400 or Credentials Error Selecting Video

Selecting a video through the Brightcove Marketplace app's custom field may return a 400 Bad Request error, or may fail to save with an "invalid or missing credentials" error when selecting a single video.

**Root Cause**

Both defects were introduced by the backend rollout of Brightcove Marketplace app v1.2.0, which reworked the video-request path logic. The 400 error occurred because the video ID was sent wrapped in stray brackets and commas instead of as a plain ID. The credentials error occurred because Brightcove's API returns a single object for one video ID but an array for multiple IDs, and the app was not handling that distinction correctly for single-video selection.

**Resolution**

1.  Confirm you are hitting this issue by checking whether video selection fails with a 400 error, or whether single-video selection specifically fails to save with an "invalid or missing credentials" error while multi-video selection works normally.

2.  Retry selecting a video. Contentstack engineering has deployed a fix for both the malformed video-request URL and the single-video selection handling in the Brightcove Marketplace app.

3.  Contact Contentstack Support with the Brightcove account ID and the video ID(s) being selected if the errors persist after retrying.

After retrying, confirm both single- and multi-video selection save successfully. If selection completes without errors, the issue is resolved. Escalate with the Brightcove account ID and video IDs if selection still fails.

<!-- end:00060653 -->