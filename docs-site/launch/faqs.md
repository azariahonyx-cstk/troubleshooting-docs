---
title: "Launch Troubleshooting Guides"
description: "Discover answers to common troubleshooting questions about Launch."
url: "https://www.contentstack.com/docs/launch-troubleshooting-guides/faqs"
product: "Contentstack"
doc_type: "guide"
audience:
  - developers
  - admins
version: "current"
last_updated: "2026-07-23"
---

# Launch Troubleshooting Guides

## Workspaces, Access & Admin

### Restoring Admin Access to Launch via Instance Keys

Users assigned the Admin role may find themselves unable to access or utilize Launch features within their instance. This prevents high-level users from managing projects or configurations.

**Root Cause**

Access to Launch is governed by instance-specific keys. If the Launch key for a specific instance is not enabled, the feature remains inaccessible regardless of the user's assigned role.

**Resolution**

Enable the Launch key for the affected instance. This restores visibility and functionality for all users with appropriate roles within that instance.

The issue is resolved when users with Admin roles can successfully view and interact with the Launch dashboard and its associated tools.

### Verifying and Confirming User Access to Launch

Accessing Contentstack Launch may appear restricted when a user is uncertain if permissions are enabled. This prevents users from beginning work within the Launch interface until access status is confirmed.

**Root Cause**

The user already had the required permissions and active access to the Launch environment, so no technical remediation was necessary.

**Resolution**

1.  Navigate to the Launch login page and attempt to sign in with your credentials.
2.  Verify that there are no authentication or permission error messages displayed during login.
3.  Check your user profile settings to ensure the Launch feature is visible in your organization.
4.  Confirm that you can access and view your projects within the Launch dashboard.

After completing the resolution steps, log in to the Launch interface and open a project. If you can successfully view the dashboard and interact with your projects, the issue is resolved.

### Permanently Deleting Projects in Contentstack Launch

Unable to locate the administrative settings required to permanently remove a project from the Contentstack Launch dashboard. This prevents the cleanup of unused or test environments and may lead to a cluttered project list.

**Root Cause**

The project deletion option is located within the project-specific settings and requires explicit confirmation, which can make it difficult for users to identify without specific guidance.

**Resolution**

1.  Log in to your Contentstack account and click the **Launch** icon from the App Switcher.
2.  From the Launch landing page, select the specific project you wish to delete.
3.  Click the **Settings** icon from the top panel or left navigation menu.
4.  In the **General** section, scroll down to the **Delete Project** area.
5.  Click the **Delete Project** button.
6.  In the confirmation modal that appears, type DELETE in the input field.
7.  Click the **Yes, Delete** button to permanently remove the project.

**Note:** This action is irreversible and will remove all domains and environments associated with the project.

After completing the deletion steps, return to the Launch main dashboard. If the deleted project no longer appears in your project list and all associated URLs are inactive, the issue is resolved.

### Environment Creation Limitations in Launch CLI

Attempts to create a new environment via the Launch Command Line Interface (CLI) fail because the functionality is currently restricted. This limitation requires an alternative workflow to establish new environments before they can be managed via terminal commands.

**Root Cause**

Creating new environments is currently a UI-only feature in Launch. While CLI support for this action is on the product roadmap, it is not supported in the current version of the tool.

**Resolution**

1.  Manually create the new environment through the Launch user interface.
2.  Once the environment is established in the UI, use the Launch CLI for subsequent tasks such as deployments and configuration management.
3.  Monitor official release notes for updates regarding expanded CLI capabilities for environment creation.

After manual creation in the UI, use the Launch CLI to list or manage the environment. The issue is resolved when the CLI successfully recognizes and interacts with the newly created environment.

### Resolving Launch Access and Provisioning Delays

Launch remains inaccessible within a Contentstack instance despite an active subscription, preventing the creation of new projects or environments.

**Root Cause**

Access to Launch is dependent on the completion of the provisioning process. This process is managed by a separate team (CSM/Provisioning) and falls outside the scope of technical support. Access may be paused if required administrative documentation or paperwork is outstanding.

**Resolution**

Ensure that all required administrative documentation and service agreements have been completed and submitted. Technical support cannot provision Launch; the request must be finalized by the Provisioning or Customer Success team once the paperwork is processed.

Attempt to access the Launch application from the App Selector. The issue is resolved when the Launch dashboard loads successfully and permits the creation of new projects.

## Git & Repository Integrations

### Connecting Launch Projects to Bitbucket Repositories

The absence of a configured connection between a Launch project and a Bitbucket Cloud repository prevents the establishment of automated deployment pipelines, requiring a guided setup of the necessary integration protocols and environment configurations.

**Root Cause**

Establishing a new project connection involves specific prerequisite steps, including organizational-level app installation and OAuth authorization.

**Resolution**

To integrate Bitbucket Cloud with Launch, you must complete the following configuration steps:

1.  **Install the Bitbucket Cloud Marketplace App**: Access the Contentstack Marketplace at the organization level to install the Bitbucket Cloud app, which establishes the necessary OAuth permissions for secure communication between the platforms.
2.  **Connect Bitbucket Cloud to Launch**: Create a new project within the Launch dashboard and select Bitbucket as your Git provider; this allows the platform to import your specific repository and branch for the initial deployment.
3.  **Configure and Deploy**: Define the project’s build commands and the output directory (e.g., dist or build) within the environment settings to ensure the platform correctly compiles and serves your source code.
4.  **Refer to Documentation**: Consult the official Contentstack Launch documentation for detailed troubleshooting and advanced environment variable configurations.

The issue is resolved when the user can successfully create the Launch project and confirm that the repository is connected and building correctly.

### Restoring GIT Connectivity via Repair Connection

Connectivity failures within the GIT integration disrupt automated deployment workflows, preventing the synchronization of repository updates with the Launch environment.

**Root Cause**

Generic integration issues between the platform and the GIT provider resulted in a loss of connectivity, though the specific underlying technical trigger was not identified in the logs.

**Resolution**

To restore the link between the source repository and Launch, follow these steps:

1.  **Initiate Reconnection**: Access the project's settings and initiate a reconnection with the GIT provider.
2.  **Repair Connection**: Utilize the "Repair Connection" tool to programmatically re-establish the integration and fix connectivity errors.
3.  **Confirm Status**: Verify that the integration is active and that the repository is once again communicating with the platform.

The issue is resolved when the GIT integration status returns to "Connected" and the user confirms that the case can be closed.

### Resolving Bitbucket Branch Retrieval Issues in Launch

The branch selection menu in Launch fails to populate when connecting to a Bitbucket repository. This prevents the selection of source branches, stalling the deployment configuration process.

**Root Cause**

This issue is typically caused by expired OAuth tokens, insufficient repository permissions, or browser-side session conflicts that block the integration from fetching the repository metadata.

**Resolution**

1.  Re-authenticate the Bitbucket integration within the Launch settings to refresh the connection.
2.  Verify that the Bitbucket account has the necessary permissions to access the specific repository and its branches.
3.  Ensure the OAuth token used for the integration has been granted the required scopes for repository read access.
4.  Use an Incognito browser window or clear the browser cache to rule out session-related display issues.

Access the project deployment or environment setup screen. The issue is resolved when the "Branch" dropdown menu successfully populates with the list of branches retrieved from the connected Bitbucket repository.

### Resolving High-Volume Log Delivery Failures Due to Endpoint Memory Pressure

A configured Log Target endpoint stops accepting logs from Launch, with millions of failed export attempts occurring over a short period. The receiving endpoint reports data being refused due to high memory usage.

**Root Cause**

An unusually high volume of log entries, in this case, caused by debug logging code that had been left active in a production environment—overwhelmed the memory capacity of the receiving log endpoint, causing it to refuse incoming data (commonly surfacing as a gRPC/Protobuf-level rejection).

**Resolution**

1.  Confirm with your Log Target endpoint’s monitoring whether it is experiencing memory pressure or explicitly refusing incoming data due to resource constraints.
    
2.  Review your application code for any debug or verbose logging that may have been inadvertently left enabled in production, generating excessive log volume.
    
3.  Remove or significantly reduce the debug logging identified, and deploy the fix to production.
    
4.  Monitor log volume and delivery success rates over the following hours to confirm the endpoint is no longer rejecting data.
    
5.  Consider implementing log level controls (e.g., environment-based log verbosity) to prevent debug-level logging from being active in production in the future.
    

The issue is resolved when log delivery to the configured endpoint resumes successfully and log volume returns to expected levels for production traffic.

### Analyzing Cache Miss Reports and 429 Rate-Limit Errors at the CDN Layer

A team requests a detailed analysis of cache misses on their Launch-hosted site, specifically to identify which URLs are contributing most to 429 (rate-limit) errors observed at the origin.

**Root Cause**

A high proportion of origin requests resulting in 429 responses typically indicates that a large share of traffic is bypassing the CDN cache and hitting rate-limited origin endpoints directly, often due to specific URL patterns, query parameters, or user agents that prevent effective caching.

**Resolution**

1.  Request a cache-miss and request-volume analysis from Contentstack Support, specifying the time window and the metric of interest (e.g., top URLs contributing to 429 responses).
    
2.  Review the resulting report, paying attention to whether the breakdown should be analyzed from the page/URL perspective rather than purely the API endpoint perspective, depending on what is actionable for your team.
    
3.  Identify the specific URL patterns or page types most responsible for cache misses and 429 errors.
    
4.  Implement caching improvements for the identified URL patterns, for example, by removing cache-busting query parameters, adjusting cache-control headers, or restructuring URLs to be more cache-friendly.
    
5.  Request a follow-up report after implementing changes to confirm a reduction in cache misses and 429 errors for the affected URLs.
    

The issue is resolved when the proportion of requests resulting in cache misses and 429 errors is significantly reduced for the identified high-impact URLs.

### Understanding Audit Log Retention and Custom Date Range Limits

A team needs clarity on how far back Audit Log entries can be retrieved within a Contentstack stack, in order to plan compliance or historical review activities.

**Root Cause**

This is a clarification of existing platform behavior rather than a defect. The default date range filters available in the Audit Log UI are limited to 1, 7, 15, and 30 days, but the Custom Date Range option does not enforce a strict limit, allowing retrieval of older logs where available.

**Resolution**

1.  Navigate to the Audit Log section under Settings within your Contentstack stack.
    
2.  Use the default date range filters (1, 7, 15, or 30 days) for standard recent-activity review.
    
3.  For older records, select the Custom Date Range option and specify the desired start and end dates, noting that older logs can be retrieved if still available in the system.
    
4.  Refer to the official Contentstack documentation on Audit Log retention for any updates to retention policy specifics relevant to your plan.
    

The issue is resolved once the team has clarity on the available date range options and can successfully retrieve the historical Audit Log data needed for their use case.

### Resolving GitHub 404 Errors During Non-Admin OAuth Authorization in Launch

When creating a new Launch project using “Import from Git repository” with a GitHub Enterprise account, a user who is not a GitHub organization admin completes the OAuth authorization request, but after the GitHub admin approves the app connection, refreshing the window shows a GitHub 404 page. The user cannot continue creating the Launch project, and restarting the flow leads to the same 404 error.

**Root Cause**

The Launch-to-GitHub connection flow for Enterprise GitHub accounts requires the user creating the Launch project to themselves hold GitHub organization admin permissions, or to be properly aligned with the OAuth and GitHub App installation flow’s permission requirements. A delegated approval flow (where a separate admin approves on behalf of a non-admin requester) can result in an incomplete connection state that surfaces as a 404 page.

**Resolution**

1.  Confirm whether the user attempting to create the Launch project holds GitHub organization admin permissions for the relevant GitHub Enterprise organization.
    
2.  If the user is not a GitHub organization admin, have a user who does hold that role create the Launch project and complete the GitHub OAuth and App installation flow directly.
    
3.  As an alternative that does not require GitHub organization admin permissions, use the file upload import method (via the Launch UI or the Contentstack CLI) instead of the Git repository import flow.
    
4.  If the Git-based import is required, retest in an incognito browser window to rule out session-related display issues, and provide a screen recording of the exact steps to Contentstack Support if the 404 persists.
    

The issue is resolved when the Launch project is successfully created, either by having a GitHub organization admin perform the Git-based import directly, or by using the file upload import method as a workaround.

### Fixing Missing Release Branches in the Launch Git Branch Selection Dropdown

Release branches (such as those using a release-\* naming prefix) exist in a connected GitHub repository but do not appear in the Launch UI’s branch selection dropdown when switching branches for an environment.

**Root Cause**

A synchronization gap between GitHub and the Launch UI’s branch selection logic caused certain branch naming patterns to be excluded from the dropdown, even though the branches existed in the repository and were otherwise accessible via the Launch API.

**Resolution**

1.  Confirm that the missing branches exist in the connected GitHub repository and follow the expected naming pattern (e.g., release-\*).
    
2.  As an interim workaround, use the Launch API directly to target the specific branch for deployment rather than relying on the UI dropdown.
    
3.  Report the issue to Contentstack Support with the organization UID, project name, and the specific branch names that are not appearing.
    
4.  Contentstack Engineering reviews the GitHub-to-Launch UI synchronization logic (including webhook and sync logs) and applies a fix for branch visibility.
    
5.  After the fix is deployed, verify in the Launch UI that the previously missing release branches now appear correctly in the branch selection dropdown.
    

The issue is resolved when all expected branches, including those with release-\* or similar naming patterns, appear correctly in the Launch UI’s branch selection dropdown, and the API-based workaround is no longer required.

## Builds & Deployments

### Troubleshooting Build Errors in Monorepo Deployments

Build failures can occur when attempting to deploy an application to Launch from a monorepo setup. The deployment fails during the build phase, preventing the application from going live.

**Root Cause**

Build failures in monorepos are often caused by missing shared dependencies in the configuration files or an incorrectly formatted build command that fails to target the specific project folder.

**Resolution**

1.  Ensure the build command correctly targets the intended project folder using the appropriate filter flags.
2.  Identify if any storefront files import logic from shared internal packages.
3.  Add any missing internal shared packages to the project's dependency list.

Check the **Deployment Logs** in the Launch dashboard for the new build attempt. If the build completes successfully and the "Deployment Succeeded" message appears, the issue is resolved.

### Fixing Deployment Failures Caused by Environment Variable Formatting

A deployment may succeed in one environment (such as Development) but fail in another (such as Staging) using the same code branch. These discrepancies often prevent specific environments from reflecting the latest updates.

**Root Cause**

Environment-specific build failures are frequently caused by improperly formatted environment variables, such as values containing unnecessary quotation marks or stray spaces that the build process cannot parse correctly.

**Resolution**

Inspect environment variable values for formatting errors. Remove any enclosing quotation marks or unnecessary spaces from the variable strings.

Monitor the build status of the Staging environment in the Launch dashboard. If the deployment completes successfully after the formatting changes, the issue is resolved.

### Resolving Zip Upload Failures for Specific Project-Level Admins

A specific user is unable to upload new zip files or create a new deployment in a Launch project, despite holding Admin access at the project level. Other users on the same project can upload without issue. The failure persists across browsers, in incognito mode, and even when re-uploading previously successful packages.

**Root Cause**

This was a platform bug in the new-deployment creation flow. The Project UID was not being passed correctly during the upload process, causing the system to validate permissions at the organization level instead of the project level. Users who were project-level Admins but only “Member” status at the organization level were incorrectly denied.

**Resolution**

1.  Confirm the affected user’s exact role at both the organization level and the specific Launch project level to rule out an actual permissions gap.
    
2.  If the user holds project-level Admin access but the upload still fails across browsers and incognito mode, report the issue to Contentstack Support with the Project UID, user email, and a description of the failure.
    
3.  Contentstack Engineering applies a fix ensuring the Project UID is correctly passed through the upload flow so that project-level Admin permissions are validated correctly.
    
4.  Once the fix is confirmed, have the affected user retry the zip upload and deployment creation to verify it now succeeds.
    

The issue is resolved when project-level Admins can successfully upload zip files and create deployments regardless of their organization-level role.

### Fixing Stale Build Delivery and ECONNRESET Errors During Dependency Installation

A Launch-hosted site intermittently serves outdated builds despite successful new deployments, alongside a higher-than-normal rate of build failures showing ECONNRESET errors during the dependency installation step.

**Root Cause**

Intermittent connection resets (ECONNRESET) during dependency installation destabilized the deployment workflow, occasionally leaving edge environments out of sync and continuing to serve a previously successful build instead of the latest one. In this case, an outdated version of the sharp image-processing library was a significant contributor to installation instability.

**Resolution**

1.  Review build logs for ECONNRESET errors occurring specifically during the dependency installation phase.
    
2.  Identify native or binary dependencies (such as sharp) in your package.json that are known to have installation stability issues in certain versions.
    
3.  Upgrade the affected dependency to a more recent, stable version (for example, sharp to ^0.33.5 or later).
    
4.  Redeploy the application and monitor subsequent builds for a reduction in ECONNRESET errors and stale-build delivery incidents.
    
5.  Continue monitoring over the following deployment cycles to confirm both build stability and consistent build delivery have been restored.
    

The issue is resolved when builds complete consistently without ECONNRESET errors and the live site reliably serves the most recently deployed build.

### Fixing CLI Installation Errors Caused by the --before Flag

Deploying through the @contentstack/cli using the --before=<date> flag fails in a CI/CD environment (such as Jenkins) with the error TypeError: withDisabledDeprecations is not a function. Installing the CLI without this flag does not reproduce the error.

**Root Cause**

The --before flag instructs npm to install the latest version of the package available before a given date. In this case, that resolution method installed a CLI version in a way that triggered an incompatibility with the installed Node.js version, surfacing as the withDisabledDeprecations error.

**Resolution**

1.  Identify the exact CLI version being installed via the --before flag by checking the npm install logs in your CI/CD pipeline.
    
2.  Replace the --before flag installation with an explicit version pin, for example: npm install @contentstack/cli@<version> --save-dev.
    
3.  Update your CI/CD pipeline configuration (e.g., Jenkinsfile) to use the explicit version installation instead of the date-based flag.
    
4.  Re-run the pipeline to confirm the deployment completes successfully without the withDisabledDeprecations error.
    
5.  If a newer Node.js version is available and appropriate for your project, consider upgrading as an additional long-term stability measure, though it is not required to resolve this specific error.
    

The issue is resolved when the CI/CD pipeline installs the Contentstack CLI successfully via an explicit version pin and deployments complete without the withDisabledDeprecations error.

### Resolving Deployment Failures Caused by a Missing Contentstack CLI in the Pipeline PATH

A deployment pipeline fails because it cannot locate the Contentstack CLI (cs or csdx command), indicating the CLI is either not installed or not accessible in the system PATH during pipeline execution.

**Root Cause**

The CLI was either missing from the pipeline’s build environment or installed in a location not included in the system PATH at execution time, causing the deployment script to fail when attempting to invoke CLI commands.

**Resolution**

1.  Verify whether the Contentstack CLI is installed as part of the pipeline’s dependency installation step by checking package.json and the pipeline configuration.
    
2.  Install the Contentstack CLI globally in the pipeline environment using npm install -g @contentstack/cli, and confirm the global npm bin directory is included in the PATH.
    
3.  As a more portable alternative that avoids PATH issues entirely, invoke the CLI using npx @contentstack/cli <command> rather than relying on a global install.
    
4.  Review package.json to confirm all required dependencies for the CLI and deployment scripts are correctly declared.
    
5.  Re-run the pipeline to confirm the CLI is now found and the deployment proceeds without PATH-related errors.
    

The issue is resolved when the pipeline successfully locates and invokes the Contentstack CLI, either via a correctly configured global install or via npx, and deployments complete without PATH errors.

### Resolving Cloud Functions Deployment Failures Caused by Container App Limits

A Cloud Functions deployment error occurs when deploying to a development or non-production environment, even when redeploying a previously successful build. In related cases, multiple environments (such as Integration, Stage, and Stage Canada) are left in a “failed state,” with server logs becoming inaccessible.

**Root Cause**

These failures were caused by the container app limit being reached on the production infrastructure underlying the organization’s Launch environments. This is a distinct root cause from environment-variable size limits, once the container app limit is reached at the infrastructure level, deployments across affected environments can fail or enter a failed state, even when the specific environment being deployed to is not itself production.

**Resolution**

1.  If a Cloud Functions deployment fails and the total environment variable size is confirmed to be within limits, consider whether a container app limit may have been reached at the infrastructure level rather than an application-side misconfiguration.
    
2.  Report the issue to Contentstack Support, including the affected project UID, the specific environments showing failures, and whether server logs have become inaccessible as a symptom.
    
3.  Contentstack Engineering investigates and addresses the container app limit on the affected production infrastructure.
    
4.  Once the limit issue is resolved on the platform side, retry deployments to the previously failing environments to confirm they now complete successfully and server logs are accessible again.
    

The issue is resolved when Cloud Functions deployments complete successfully across all affected environments and server logs are accessible, confirming the container app limit has been addressed.

<!-- case:00061478 status:draft synced:false bucket:"Builds & Deployments" -->
### Launch Deployment Fails With Error 109 Stack Not Found

Deploying a Launch project connected to a starter kit such as Veda may fail with a "We can't find that Stack" (error 109) message when the configured API key does not match the intended stack.

**Root Cause**

Error 109 occurs when the Contentstack API key configured in the Launch project's environment variables belongs to a different stack than the one intended for deployment, such as when partner and test instances use different stack API keys.

**Resolution**

1.  Open the Launch project's environment variable settings.

2.  Locate the Contentstack API key variable.

3.  Verify the API key corresponds to the correct stack for the target environment (partner vs. test instance).

4.  Update the API key value if it points to the wrong stack.

5.  Redeploy the project.

After redeploying with the corrected API key, confirm the build completes without the error 109 "We can't find that Stack" message. If the deployment succeeds, the issue is resolved. Escalate with the project ID and stack API key if error 109 persists.

<!-- end:00061478 -->

## Domains, DNS & SSL

### Validating Domain Ownership via CNAME Records

Incompatibility between the requested TXT record validation method and the specific environment workflow prevents successful domain ownership verification during the Go-Live process.

**Root Cause**

The domain validation workflow for certain edge configurations requires a CNAME record instead of a TXT record to successfully complete the Domain Control Validation (DCV) process.

**Resolution**

To validate domain ownership for the Launch project, the following DNS configuration must be implemented:

1.  **Identify Validation Type**: Confirm that the specific domain validation workflow requires a CNAME-based ACME challenge rather than a standard TXT record.
2.  **Configure CNAME Record**: Add a CNAME record at your authoritative DNS provider for the \_acme-challenge subdomain.
3.  **Point to Validation Endpoint**: Direct the CNAME record to the platform’s designated validation URL (e.g., \_acme-challenge.www.\[domain\].com CNAME www.\[domain\].com.\[unique-id\].dcv.cloudflare.com).
4.  **Refer to Documentation**: Consult the platform’s Go-Live instructions for the specific unique identifier and endpoint required for your custom domain.

The issue is resolved when the DNS configuration allows for proper domain validation and the SSL certificate provisions automatically.

### Serving Assets via Custom Domains

Standard asset delivery utilizes default platform domains, which may not align with organizational branding requirements. This necessitates a technical configuration to serve asset public URLs through a custom branded domain.

**Root Cause**

Default platform URLs are used for standard asset delivery. Masking these with a custom domain requires additional network configurations, such as DNS or proxy layers.

**Resolution**

Two supported approaches exist for serving assets via a custom domain:

1.  **Implement a Web Proxy**: Configure a web proxy server to act as an intermediary that rewrites asset requests to utilize the custom domain.
2.  **Reverse Proxy Setup**: Implement a reverse proxy configuration to direct traffic from the custom domain to the platform's asset origin.
3.  **Configure CNAME Record**: Establish a CNAME record at the authoritative DNS provider to map the custom domain to the platform's asset delivery endpoint.
4.  **Refer to Documentation**: Consult official guides for specific reverse proxy configuration logic and DNS mapping details.

The issue is resolved when asset public URLs successfully resolve and serve content through the configured custom domain.

### Managing SSL Provisioning and Redirections for Large Domain Sets

The inability to effectively provision SSL certificates and manage redirections across a large volume of domains can lead to site unavailability and certificate provisioning failures.

**Root Cause**

Attempting to manage a very large set of domains under a single service can exceed standard manageability thresholds, complicating the SSL SAN (Subject Alternative Name) update process and certificate issuance.

**Resolution**

1.  **Segment Domain Groups**: Split large sets of domains into smaller, manageable groups across separate services to facilitate better processing.
2.  **Configure Service Redirections**: Set up the necessary redirections between the split services to ensure all traffic points to the primary domain.
3.  **Implement CNAME Records**: Add the required CNAME records for each domain at the authoritative DNS provider to trigger validation.
4.  **Automate SSL Provisioning**: Once CNAMEs are verified, allow the platform to automatically provision certificates for the newly added domains.

The issue is resolved when all domains are successfully added, redirections are functional, and SSL certificates have provisioned automatically across both groups.

<!-- case:00060756 status:draft synced:true bucket:"Domains, DNS & SSL" -->
### SSL Certificate Stuck Inactive After Migrating From Fastly

Migrating a custom domain from a deprecated Fastly IP to the current Contentstack IP may leave the SSL certificate stuck in an inactive state.

**Root Cause**

The domain's DNS still pointed to legacy Fastly infrastructure that is no longer in use, and the certificate required an updated Cloudflare DCV CNAME record instead of the legacy Fastly validation method.

**Resolution**

1.  Update the \_acme-challenge CNAME record for the domain to point to the Cloudflare DCV validation endpoint.

2.  Update the domain's A record to point to the current Contentstack IP address, available from Contentstack Support or your domain configuration.

3.  Allow DNS propagation to complete, then check the certificate status in the domain settings.

After updating the CNAME and A records, check the domain's SSL certificate status in Launch. If the certificate shows as Active, the issue is resolved. Escalate with your domain name and current DNS records if it remains stuck after propagation.

<!-- end:00060756 -->

### Configuring Custom Hostnames and Increasing Domain Limits

Subdomain traffic is failing to reach a Launch application despite having valid CNAME records in a DNS provider. Additionally, the user is unable to add the necessary domains to the Launch UI due to reaching a project-level limit.

**Root Cause**

Launch requires every domain intended to receive traffic to be explicitly registered as a "Custom Hostname" in the UI. Furthermore, projects have a default cap on the number of domains allowed, which requires manual intervention to increase.

**Resolution**

1.  Log in to the Launch dashboard and select your project.
2.  Go to **Settings** > **Domains** and click **Add Custom Hostname**.
3.  Enter the subdomains (e.g., blog.axonius.com) to link them to your application.
4.  If you receive an error stating the domain limit has been reached, contact Contentstack Support to request a limit increase.
5.  Once the limit is raised, complete the addition of the domains.
6.  Verify that your DNS CNAME records point to the correct Launch target.

After the domains are added and the limit is increased, navigate to the subdomains in a web browser. If the traffic is correctly routed to the Launch application without "Domain Not Found" or limit errors, the issue is resolved.

## Edge Functions & Frameworks

### Dynamic Data Fetching Limitations in Edge Functions

WinterCG runtime limitations prevent the direct fetching of dynamic data from Contentstack entries within a Launch Edge Function, causing failures when attempting to avoid hardcoded URLs in proxy configurations.

**Root Cause**

Launch Edge Functions operate within a restricted runtime environment that does not support the direct execution of certain SDK queries or external fetches intended for complex dynamic data retrieval.

**Resolution**

To handle dynamic URL routing or data retrieval within an Edge Function, implement the following workaround:

1.  **Create an API Route**: Develop a Next.js API route at the origin to fetch the required data from Contentstack using the JavaScript SDK.
2.  **Consume Data in Edge Function**: Configure the Edge Function to call the internal API route rather than querying the CMS directly.
3.  **Optimize with Caching**: Apply cache-control headers to the API response to improve performance and reduce origin load.
4.  **Implement Revalidation**: Utilize Contentstack Automate to trigger cache revalidation, ensuring the Edge Function has access to the most recent data without constant fetching.

The issue is resolved when the Edge Function successfully retrieves dynamic URLs through the intermediary API route without encountering runtime failures.

### Configuring Live Preview and Environment Variables in Astro Projects

Setting up Live Preview in Astro projects may fail when environment variables are handled incorrectly during SSR or SSG. This prevents users from viewing real-time content changes within the Live Preview interface.

**Root Cause**

Environment variables in Contentstack Launch are parsed upon ingestion, whereas local development environments typically treat these variables strictly as string values, leading to configuration mismatches.

**Resolution**

1.  Navigate to your Astro project configuration and verify how environment variables are being accessed for SSR and SSG.
2.  Adjust your code to account for the fact that Launch parses environment variables rather than treating them solely as strings.
3.  Review the implementation guide for Astro to ensure the Live Preview integration aligns with platform requirements.

After completing the resolution steps, open the Contentstack entry editor and initiate a Live Preview session for your Astro project. If the preview renders correctly and reflects your content changes, the issue is resolved.

### Resolving CSP Framing Restrictions in Custom Field Applications

A custom field application hosted on Launch fails to load within the Contentstack editor, displaying a Content Security Policy (CSP) error. This occurs because the browser refuses to frame the application URL, citing that an ancestor violates the frame-ancestors 'self' directive, particularly when users access the application via a VPN.

**Root Cause**

The application lacks a server-side framework (such as Next.js or Express) to modify response headers directly. By default, the CSP headers restrict the application from being embedded (framed) in external sites like the Contentstack UI.

**Resolution**

1.  Create a folder named functions at the root of your project.
2.  Inside this folder, add a file named \[proxy\].edge.js.
3.  Implement a handler function within \[proxy\].edge.js to modify the response headers.
4.  Use the Edge Function to explicitly set or update the Content Security Policy headers to allow the application to be embedded within Contentstack.
5.  Deploy the project; Contentstack Launch will automatically detect the new functions folder and apply the header modifications to all requests.
6.  If further clarification is needed on the function implementation, a technical call can be scheduled with the support team.

After the deployment is complete, navigate to the Contentstack entry that utilizes the custom field application. If the custom field application loads successfully within the Contentstack UI without being blocked by CSP restrictions, the issue is resolved.

### Errors while Running Elasticsearch Adapters in Launch

Deploying an Elasticsearch adapter via a webhook in Launch can result in 404 errors. While converting the adapter to an Edge Function may provide an immediate workaround, it introduces potential stability concerns due to runtime compatibility requirements.

**Root Cause**

Launch Edge Functions require code to be WinterCG-compliant. Some adapters or third-party libraries may not fully support this standard, leading to unexpected behavior or limited functionality during execution.

**Resolution**

1.  Use Launch Cloud Functions instead of Edge Functions for adapters that require a more robust Node.js environment or lack WinterCG compliance.
2.  Alternatively, implement a dedicated route within your application framework to handle the adapter's logic directly.
3.  Ensure that any code run within an Edge Function environment is verified for compatibility with the WinterCG standard.

Trigger the webhook or adapter logic and verify the response status. The issue is resolved when the 404 error is replaced by a successful data exchange and the function executes successfully in the logs.

## Performance, Network & Security Errors

### Compression and Caching for Client-Side Rendered (CSR) Apps

SEO auditing tools may report warnings regarding uncompressed static assets (such as .js and .css files) on production sites. These warnings indicate that assets are being served without compression, which can increase payload sizes and negatively impact site performance scores.

**Root Cause**

The behavior of asset compression in the hosting environment depends on the application architecture:

*   **Static Sites:** For projects hosted as purely static sites, the platform automatically applies compression (such as Gzip) to all assets.
*   **Next.js Applications:** In applications using the Next.js framework, the application itself is responsible for generating and serving static assets. Because these files are handled by the application code rather than the platform's default static hosting layer, compression is not applied by the platform automatically.

**Resolution**

1.  **Identify Architecture:** Determine if the project is a standard static site or a framework-based application like Next.js.
2.  **Configure Framework Compression:** If using Next.js, compression must be explicitly enabled within the Next.js configuration. This ensures that the application compresses the JavaScript and CSS files it serves, resolving SEO auditing warnings.
3.  **Static Site Default:** If the project is a purely static site, no additional action is required as compression is applied automatically by the platform.

### Identifying Service Outages Caused by CDN Provider Incidents

A hosted site becomes unreachable, causing downtime and requiring urgent clarification on whether the issue is platform-specific or related to external infrastructure.

**Root Cause**

Service disruptions can be caused by widespread outages at the Content Delivery Network (CDN) layer (such as Cloudflare). These incidents impact all sites and services routed through the affected provider's network.

**Resolution**

Monitor the official status pages of the platform and the CDN provider to identify active incidents. Communicate the status of the external outage to the affected parties and provide incident tracking links for real-time updates.

The issue is resolved when the CDN provider restores service and the hosted site becomes accessible again without further technical intervention.

### Resolving Slow Performance and Timeouts Caused by Origin 404 Errors

Accessing website redirects and production instances in Launch may experience significant delays and timeouts when a high volume of 404 errors occurs at the origin. This prevents accessing live site content and completing redirects within a functional timeframe.

**Root Cause**

A high volume of 404 errors from the application origin caused requests to bypass the CDN cache, subsequently overloading the server and leading to performance timeouts.

**Resolution**

1.  Investigate the application root cause, focusing on potential data retrieval issues from the CMS, database, or other sources.
2.  Add logging to your application to pinpoint the specific source of the 404 errors.
3.  Resolve the underlying application errors to stop the generation of 404 responses.
4.  Implement caching to reduce server load once the errors are resolved.
5.  Refer to the provided analytics report for a detailed list of URLs returning 404 errors.

After completing the resolution steps, navigate through the affected URLs and monitor server logs. If the site performs without timeouts and 404 errors are no longer bypassing the cache, the issue is resolved.

### Configuring Secure GRPC OTLP Endpoints for Launch Log Targets

Forwarding logs to an external destination in Launch may fail when the Log Target is incorrectly configured. This prevents accessing consolidated application and edge function logs within your preferred monitoring tool.

**Root Cause**

The Log Target configuration requires a secure GRPC OTLP endpoint to function; using an unsupported protocol or insecure endpoint prevents Launch from successfully forwarding log data.

**Resolution**

1.  Navigate to your Log Target settings in the Launch dashboard.
2.  Verify that the configured Log Target Endpoint is a secure GRPC OTLP endpoint.
3.  Update the endpoint URL and security settings to meet the GRPC OTLP requirements if they do not match.
4.  Check the "Server Logs" tab in the Launch interface to confirm that application logs are being generated internally.
5.  Ensure that your external log management tool is prepared to receive OTLP data from Launch.

After completing the resolution steps, trigger an action that generates logs (such as a site visit or a function execution) and check your external log destination. If both application logs and edge function logs appear in your designated log target, the issue is resolved.

### Resolving 502 and 524 Timeout Errors in Launch Applications

An application hosted on Launch intermittently displays a "502 A timeout occurred" page, preventing access to specific site paths even when traffic volume is low. This issue is typically characterized by high response times and application-level errors within Next.js logic, particularly on resource-heavy pages like "Contact Us."

**Root Cause**

The 502 error is triggered by upstream 524 timeouts, meaning the application is taking too long to respond to requests. This is often accompanied by 499 status codes, indicating that the client disconnected before the server could finish processing. In this specific case, application-level errors were identified on the "Contact Us" page, and high response times were linked to the Next.js application logic.

**Resolution**

1.  Review application performance to identify slow endpoints, particularly those related to server-side rendering or complex data fetching.
2.  Implement enhanced logging within the application to track response times and identify specific code blocks causing delays.
3.  Investigate application-level errors, specifically within the Next.js context on pages like "Contact Us," that may be contributing to processing overhead.
4.  Optimize backend logic to ensure responses are returned within standard gateway timeout limits.

Monitor the application's response behavior. The issue is resolved when the 524 and 499 status codes are replaced by successful 200 OK responses and the application consistently responds within the gateway’s timeout threshold.

### Whitelisting External Crawler IPs for SEO and Accessibility Audits

A website auditing tool is unable to crawl content hosted on Launch. This prevents the execution of pre-go-live scans used to ensure the site is properly indexed, optimized for SEO, and meets general accessibility standards.

**Root Cause**

Access restrictions are typically managed at the Content Delivery Network (CDN) layer (such as Cloudflare or CloudFront). Because the platform does not manage these perimeter security settings, external crawler IPs must be manually permitted at the CDN level.

**Resolution**

1.  Identify the specific IP address of the auditing tool's crawler.
2.  Access the configuration settings for the CDN or WAF used to manage the website's traffic.
3.  Add the crawler's IP address to the trusted whitelist or allowlist to permit the tool to bypass security restrictions.
4.  Once the configuration is updated, the auditing tool can proceed with the SEO and accessibility crawl.

The issue is resolved when the auditing tool successfully accesses the website pages and completes the scheduled scan without being blocked by security filters.

### Troubleshooting Intermittent Asset Loading and Connection Reset Errors

A website experiences intermittent application errors such as net::ERR\_INCOMPLETE\_CHUNKED\_ENCODING and net::ERR\_CONNECTION\_RESET. These errors prevent static assets from loading completely, even though the site remains functional on the default platform-provided domain.

**Root Cause**

When errors are restricted to a custom domain and not reproducible on the default domain, the root cause is typically located in intermediary network layers, such as a user-managed proxy, Netscaler, or load balancer.

**Resolution**

1.  Verify if the issue persists on the default platform domain.
2.  If the default domain is unaffected, investigate the configuration of any managed proxies or load balancers through which the custom domain traffic is routed.
3.  Review proxy and load balancer settings to ensure they are not prematurely terminating connections or mishandling chunked encoding.

The issue is resolved when static assets load consistently across all domains and the connection reset errors no longer appear during site navigation.

### Allowlisting Vendor IPs for Programmatic Access to Launch-Hosted Assets

A third-party vendor receives HTTP 403 errors when programmatically accessing Launch-hosted public assets (such as PDF files). The vendor believes their outbound IP addresses need to be allowlisted in order to access the site.

**Root Cause**

Launch sits behind a CDN layer (such as Cloudflare) that can apply traffic filtering rules. When a third-party vendor’s requests originate from IP addresses not recognized by an existing allowlist or filtering rule, the CDN can return a 403 error even though the underlying content is intended to be publicly accessible.

**Resolution**

1.  Collect the exact outbound IP addresses used by the third-party vendor for their programmatic requests, including any new IPs introduced by infrastructure changes on their side.
    
2.  Identify the specific URLs being accessed and confirm whether they are intended to be publicly accessible without authentication.
    
3.  Submit the IP addresses to Contentstack Support or your internal CDN/WAF administrator to be added to the allowlist for the relevant Launch domain.
    
4.  After the allowlist update, have the vendor retest programmatic access to confirm the 403 errors are resolved.
    
5.  If issues persist after the initial allowlist update, provide additional request details (such as User-Agent string and CDN ray IDs) to help narrow down any remaining filtering rules affecting the vendor’s traffic.
    

The issue is resolved when the third-party vendor can programmatically access the intended Launch-hosted URLs without encountering 403 errors.

### Allowlisting the Default Launch Domain to Prevent DNS and Phishing Filter Blocks

End users experience DNS blocking or phishing warnings when accessing a Launch-hosted application through a custom domain. The warnings appear to originate from corporate DNS or security filters rather than from the application itself.

**Root Cause**

The default Launch domain pattern (\*.contentstackapps.com) had been flagged by one or more third-party security engines, likely due to prior abuse of similarly structured domains on shared hosting platforms. This flag can propagate into corporate DNS or security filtering products, blocking legitimate traffic to any site using the default domain, including via a custom domain that resolves through it.

**Resolution**

1.  Confirm the application follows web security best practices: serve over HTTPS, avoid unnecessary redirects, and do not load untrusted third-party scripts that could itself trigger security flags.
    
2.  As a workaround, advise affected end users or their IT departments to allowlist the default Launch domain (\*.contentstackapps.com) in their corporate DNS or security filtering product.
    
3.  Where possible, ensure your production traffic is served primarily through your custom domain rather than the default Launch domain, to reduce dependency on the flagged domain pattern.
    
4.  If the issue persists at scale, report the specific flagged domain pattern to Contentstack Support so it can be raised with the relevant security vendor for reputation review.
    

The issue is resolved when end users can access the application through the custom domain without triggering DNS blocking or phishing warnings, either through allowlisting or domain reputation remediation.

### Confirming Chunked Transfer Encoding Compatibility Between Launch and Upstream CDNs

A team using an upstream CDN such as Akamai in front of Launch needs to confirm whether the Launch origin supports Chunked Transfer Encoding (CTE), which is a prerequisite for certain CDN configurations.

**Root Cause**

This is a compatibility clarification rather than a defect. Launch deployments run on a Node.js/Next.js runtime that supports HTTP/1.1 streaming responses, which automatically use Transfer-Encoding: chunked when a response is streamed without a Content-Length header - meeting the standard prerequisite for CDNs that communicate with origins over HTTP/1.1 chunked encoding.

**Resolution**

1.  Confirm with your CDN provider’s documentation that their architecture uses HTTP/2 between the client and CDN, and HTTP/1.1 (with chunked transfer encoding as needed) between the CDN and the origin.
    
2.  No additional configuration is required on the Launch side, as the Node.js/Next.js runtime natively supports chunked transfer encoding for streamed responses.
    
3.  If specific endpoints are not streaming as expected, verify that the application code is not explicitly setting a Content-Length header where streaming behavior is intended.
    
4.  Test the upstream CDN configuration against the Launch origin to confirm chunked responses are handled correctly end-to-end.
    

The issue is resolved once it is confirmed that the Launch origin already meets the upstream CDN’s chunked transfer encoding prerequisite, with no platform-side changes required.

### Diagnosing 413 Payload Too Large Errors Caused by Cloud Provider Header Limits

A Launch-hosted application returns a 413 Payload Too Large error (sometimes shown as CF1001) when handling certain requests, particularly those carrying a large number of cookies or custom headers.

**Root Cause**

The 413 error is caused by request and header size limits enforced at the underlying cloud provider infrastructure level. These limits cannot be increased from the Contentstack side, as they are set by the infrastructure provider rather than by the Launch application layer.

**Resolution**

1.  Identify which requests are triggering the 413 error and inspect their total header size, with particular attention to cookies and any custom headers being set.
    
2.  Reduce the overall size of cookies sent with requests - for example, by trimming unnecessary cookie data, consolidating multiple cookies, or moving large values to server-side session storage instead of client-side cookies.
    
3.  Review any custom headers added by the application or intermediary services and remove or shorten any that are not strictly necessary.
    
4.  Retest the previously failing requests after reducing header size to confirm the 413 error no longer occurs.
    

The issue is resolved when requests complete successfully without triggering the 413 Payload Too Large error, having reduced the overall request header size below the cloud provider’s limit.

### Resolving 403 Errors During App Upload Due to Organization Admin Permission Requirements

A user with Stack Admin access attempts to upload a zip file to set up an app in Launch and encounters a “File upload failed” error. Closer inspection shows the underlying GraphQL request (createSignedUploadUrl) is returning a 403 Forbidden response.

**Root Cause**

App launch and upload functionality requires Organization Admin access, not just Stack Admin access. A user who is a Stack Admin but not an Organization Admin will be blocked at the createSignedUploadUrl step, since this operation is gated at the organization permission level.

**Resolution**

1.  Confirm the affected user’s role at both the Stack level and the Organization level within Contentstack.
    
2.  If the user holds Stack Admin access but not Organization Admin access, have an existing Organization Admin either grant the required role or perform the app upload on the user’s behalf.
    
3.  Once the user has Organization Admin access, retry the zip file upload and confirm the createSignedUploadUrl request succeeds.
    
4.  Document the permission requirement internally so future app upload requests from Stack-level users are routed to an Organization Admin without delay.
    

The issue is resolved when the user (or an Organization Admin acting on their behalf) can successfully upload the zip file and complete the app setup without encountering the 403 error.

<!-- case:00060727 status:draft synced:true bucket:"Performance, Network & Security Errors" -->
### Launch Cloud Function Times Out After 30 Seconds

Calling a Cloud Function synchronously from the frontend may return a 500-class error (for example CFOO5) when the function takes longer than 30 seconds to execute.

**Root Cause**

Launch Cloud Functions enforce a hard 30-second maximum execution timeout. A synchronous call that waits directly on a function taking 30 or more seconds to complete exceeds this ceiling, and the request fails with a 500-class error before the function can return a response.

**Resolution**

1.  Restructure the frontend-to-Cloud-Function integration to use an async start-and-poll pattern instead of a single synchronous call.

2.  Trigger the long-running function to start the work and return immediately.

3.  Poll a separate endpoint or status check on an interval until the function reports completion, then retrieve the result.

After switching to the async start-and-poll pattern, call the long-running function again and confirm the frontend no longer times out while waiting for a response. If the function completes and the result is retrieved successfully via polling, the issue is resolved. Escalate with the function's typical execution time and the error code observed if it persists.

<!-- end:00060727 -->

## Redirects & Routing

### Implementing 301 Redirect Management via Edge Functions

**Root Cause**

The launch.json-based redirect workflow requires direct file editing and a code deployment for every change, which is unsuitable for teams without developer access. Launch Edge Functions provide an alternative that allows redirect rules to be modeled and managed within Contentstack itself.

**Resolution**

1.  Model your redirect entries inside Contentstack as a content type that mirrors the structure of your existing launch.json redirect rules (source path, destination path, status code).
    
2.  Create a Launch Edge Function that fetches these redirect entries from the Contentstack Delivery API at request time.
    
3.  Implement caching within the Edge Function to avoid exceeding API rate limits on high-traffic sites. Store fetched redirect rules in memory or use cache-control headers on the API response.
    
4.  Use Contentstack Automate (webhooks) to trigger cache revalidation in the Edge Function whenever a redirect entry is published or updated, ensuring changes go live without requiring a redeployment.
    
5.  Deploy the updated project and validate that redirects resolve correctly via browser testing and HTTP status checks.
    

The issue is resolved when non-developer team members can update redirect rules by editing Contentstack entries, and the Edge Function serves the correct 301 responses without requiring a code push.

### Preserving Query Strings in Launch Edge URL Redirects

Query strings are not preserved when processing redirects configured in launch.json. This breaks analytics tracking parameters and campaign URLs that rely on query string values being forwarded to the destination.

**Root Cause**

The launch.json redirect configuration has limited support for query string handling. Using certain characters (such as ?) in the redirect definition can also cause deployment failures. Query string preservation requires logic that is beyond the capabilities of static launch.json rules.

**Resolution**

1.  Migrate the redirect logic from launch.json to a Launch Edge Function, which provides full programmatic control over request and response handling.
    
2.  Within the Edge Function, read the incoming request URL, extract the query string using the URL API, and append it to the destination URL before issuing the redirect response.
    
3.  Set the appropriate HTTP status code (e.g., 301 or 302) on the redirect response returned by the Edge Function.
    
4.  Deploy the project and test with URLs that include query parameters to confirm they are forwarded correctly to the destination.
    

The issue is resolved when redirected URLs correctly pass query strings to the destination, and no deployment failures occur from unsupported characters in the configuration.

### Fixing Next.js RSC Parameter Loss During CDN Redirects

A production site using Next.js on Launch experiences routing failures where the \_rsc parameter is stripped during CDN-level redirects. This breaks React Server Component (RSC) data fetching and causes partial or blank page renders.

**Root Cause**

Launch CDN redirect rules do not automatically preserve internal Next.js parameters such as \_rsc. When CDN-level rewrites or redirects occur, these parameters are dropped, disrupting the RSC payload request cycle that Next.js relies on for client-side navigation.

**Resolution**

1.  Update the rewrite or redirect logic in the Launch configuration or Edge Function to explicitly detect and preserve the \_rsc query parameter.
    
2.  As an alternative, implement a Launch Edge Function that intercepts requests containing \_rsc, strips the parameter before forwarding to the origin (to avoid double-processing), and ensures the response is returned correctly to the client.
    
3.  Review all existing CDN rewrite rules to confirm that no other Next.js internal parameters (such as \_next or \_\_nextjs\_) are being stripped.
    
4.  Redeploy and test client-side navigation flows to confirm RSC payloads load correctly without blank page renders.
    

The issue is resolved when all pages load correctly during client-side navigation and RSC data fetching errors no longer appear in the browser console or server logs.

### Configuring Single-Step Domain Redirects in Launch

A domain redirect configuration results in a multi-step redirect chain (e.g., http://example.com → https://example.com → https://www.example.com) instead of a single direct redirect. Multi-step chains increase latency and may cause issues with certain browsers or SEO crawlers.

**Root Cause**

Default redirect configurations handle HTTP-to-HTTPS and non-www-to-www as separate steps. Without explicit single-step redirect configuration, the CDN or platform applies each rule sequentially, resulting in a redirect chain.

**Resolution**

1.  Define a single redirect rule that maps the non-secure, non-www root URL (e.g., http://example.com) directly to the final secure www destination (e.g., https://www.example.com).
    
2.  Configure the rule within your Launch Edge Function or launch.json so that both the protocol upgrade and subdomain normalization are handled in a single HTTP 301 response.
    
3.  Remove or disable any intermediate redirect rules that separately handle HTTP-to-HTTPS and non-www-to-www to prevent redirect chains from forming.
    
4.  Test the redirect chain using a tool such as curl --head or an online redirect checker to confirm that http://example.com resolves directly to https://www.example.com in a single hop.
    

The issue is resolved when the redirect chain collapses to a single step and the destination URL loads without intermediate redirects.

## Project & Account Management

### Transferring Ownership of a Launch Project

When a staff member who originally configured a Contentstack Launch project leaves the organization, the team needs to transfer project ownership and access to another user without losing project configurations or deployment history.

**Root Cause**

Launch project access is tied to user accounts within the Contentstack organization. Transferring ownership requires inviting the new owner, assigning the appropriate role, and removing the departing user—there is no single-click ownership transfer button.

**Resolution**

1.  Log in to Contentstack and navigate to your organization settings.
    
2.  Invite the new owner by adding them as a user to the organization with Owner or Admin permissions.
    
3.  Ensure the new user accepts the invitation and can access the relevant stack and Launch project.
    
4.  Remove the departing user from the stack and organization once ownership has been confirmed.
    
5.  Refer to the official Contentstack documentation on inviting users, removing users, and transferring stack ownership for detailed steps specific to your plan.
    

The issue is resolved when the new owner can access the Launch project, view all environments and deployment history, and perform administrative actions independently.

### Changing the Linked GitHub Repository for a Launch Project

A Launch project needs to be relinked to a different GitHub repository - for example, when a codebase is moved to a new organization or repository. The Launch UI does not expose a direct option to change the linked repository on an existing project.

**Root Cause**

Launch does not currently provide a self-service option to change the linked GitHub repository from within the project settings UI. The repository link is established at project creation, and changing it requires manual intervention by the Support team in coordination with the Launch team.

**Resolution**

1.  Contact Contentstack Support and provide the project UID, the current repository URL, and the new repository URL you wish to link.
    
2.  Support will coordinate with the Launch team to disconnect the existing GitHub connection and re-establish it pointing to the new repository.
    
3.  Once the update is applied, verify that the new repository is correctly linked by triggering a test deployment from the new source.
    
4.  Alternatively, if a new project can be created, set up a fresh Launch project connected to the new repository, migrate environment variables and domain configurations, and decommission the old project.
    

The issue is resolved when deployments trigger from the new repository and all build outputs match the expected source code.

### Resolving Node.js Version Reversion When Redeploying With Previous File Upload

After upgrading the Node.js version in package.json (e.g., from v18 to v22), new builds correctly use the updated version. However, when using the “Redeploy with previous file upload” option in Launch, the build reverts to the older Node.js version, even though the original file specified the newer version.

**Root Cause**

A bug in Launch’s version detection logic caused the platform to misread the Node.js version when redeploying from a cached file upload. This resulted in the build environment falling back to Node.js v18 regardless of the version specified in package.json.

**Resolution**

1.  Report the issue to Contentstack Support, providing the project UID, the package.json Node.js version specification, and the deployment IDs showing the incorrect version.
    
2.  The Launch engineering team will identify and apply a fix to the version detection logic.
    
3.  After the fix is confirmed, trigger a fresh deployment (not a redeploy from previous file upload) to verify that the correct Node.js version is used.
    
4.  Avoid using the “Redeploy with previous file upload” option until the fix has been confirmed in your environment.
    

The issue is resolved when both new builds and redeployments from previous file uploads correctly use the Node.js version specified in package.json.

### Resolving Projects Limit Reached Error in Launch

An error stating “Projects limit reached” appears when attempting to create or deploy a new Launch project. This prevents new projects from being added to the instance.

**Root Cause**

Contentstack Launch instances have a default maximum on the number of active projects. When the limit is reached, the platform prevents new project creation until existing projects are removed or the limit is increased.

**Resolution**

1.  Review your current Launch projects and identify any unused, test, or duplicate projects that can be safely deleted.
    
2.  Delete unnecessary projects by navigating to the project settings and using the Delete Project option (refer to the Permanently Deleting Projects article for detailed steps).
    
3.  If all existing projects are required and the limit needs to be increased, contact Contentstack Support with your organization ID and a description of your use case to request a limit increase.
    
4.  Once space is available or the limit is raised, retry creating or deploying the new project.
    

The issue is resolved when the new project is successfully created and deployments proceed without the “Projects limit reached” error.

### Resolving Access Limited Error for Non-Admin Users in Launch

A user attempting to access Contentstack Launch sees an “Access Limited” error and cannot view any Launch projects, even though they are a member of the organization.

**Root Cause**

Access to Launch projects requires organization-level Admin permissions. Users without this elevated role see a restricted view and cannot access project data. The error is not a technical failure, it reflects the user’s permission scope.

**Resolution**

1.  Confirm that the affected user does not hold the organization-level Admin role by reviewing the organization’s user list.
    
2.  Request that an existing organization Admin grants the user the required role level to access Launch.
    
3.  Once the permission change is applied, the user should log out and log back in to refresh their session.
    
4.  Verify that the user can now view and interact with the Launch dashboard and associated projects.
    

The issue is resolved when the user can access Launch projects without encountering the “Access Limited” error.

## Advanced Builds & Deployments

### Resolving Cloud Functions Deployment Errors

Deployments that include Cloud Functions consistently fail with a “Cloud functions deployment error” message, while deployments without Cloud Functions succeed. The error persists even after verifying package.json syntax and re-triggering the deployment.

**Root Cause**

Cloud Functions deployment errors can occur when the total size of environment variables set for the Cloud Function exceeds Launch’s 4 KB limit, or when the runtime encounters a transient platform-side issue. Exceeding the environment variable limit causes a silent failure during the Cloud Functions packaging step.

**Resolution**

1.  Check the total size of all environment variables configured for the affected Launch environment, particularly those used by Cloud Functions.
    
2.  If the combined size of environment variable keys and values exceeds 4 KB, move large values out of environment variables. Use an external secrets manager (such as AWS Secrets Manager or Azure Key Vault) and fetch the values at runtime within the function code.
    
3.  Alternatively, store large configuration payloads in a Contentstack entry and retrieve them via the Delivery API within the function.
    
4.  If the environment variable size is within the limit, wait a few minutes and retry the deployment, as transient platform issues can cause temporary Cloud Functions failures.
    
5.  If the error persists, contact Contentstack Support with the project UID, environment UID, and the full deployment log output.
    

The issue is resolved when the Cloud Functions deployment step completes successfully and the deployed function is reachable and responds correctly.

### Resolving ENOENT: No Such File or Directory Build Errors

A build or runtime process in Launch fails with an ENOENT: no such file or directory error. This typically appears in deployment logs when the application attempts to write cache files or temporary data to the file system.

**Root Cause**

The Launch build and runtime environment uses a read-only file system. Applications that attempt to write to directories outside of designated writable locations (such as /tmp) will encounter ENOENT errors. Next.js applications are a common source of this issue when default cache path configurations point to non-writable directories.

**Resolution**

1.  Identify the directory path referenced in the ENOENT error from the deployment or runtime log.
    
2.  Update the application configuration to redirect file writes to the /tmp directory, which is the only writable location available in the Launch environment.
    
3.  For Next.js applications, set the distDir or cacheHandler configuration to use /tmp/cache or a subdirectory within /tmp.
    
4.  Redeploy the application and confirm in the deployment logs that file write operations succeed without ENOENT errors.
    

The issue is resolved when the deployment and runtime logs are free of ENOENT errors and the application functions correctly in the Launch environment.

### Resolving JavaScript Heap Out-of-Memory Errors During Builds

A Launch build fails with a fatal error: Reached heap limit / Allocation failed - JavaScript heap out of memory. The error appears in deployment logs during the build step and prevents the deployment from completing.

**Root Cause**

The Node.js process used during the build exceeds the memory allocated to it. This is common in large Next.js or JavaScript applications with many pages, large dependency trees, or memory-intensive build steps such as static site generation with many routes. Node.js has a default heap size limit that can be exceeded during complex builds.

**Resolution**

1.  Increase the Node.js heap size by adding the NODE\_OPTIONS environment variable to your Launch environment with the value --max-old-space-size=<MB> (e.g., --max-old-space-size=4096 for 4 GB).
    
2.  Set this variable in the Launch UI under the environment’s environment variables section.
    
3.  Reduce the memory footprint of the build where possible by code splitting, reducing the number of pages generated at build time, or deferring static generation to runtime (ISR).
    
4.  Redeploy and monitor the build logs to confirm the heap error no longer appears.
    

The issue is resolved when the build completes successfully without memory allocation errors and the deployment proceeds to the live environment.

### Resolving Stuck or Queued Deployments in Launch

Deployments in a Launch project remain in a “Queued” state for an extended period without progressing to the build or deployment phase. Retrying or redeploying does not resolve the queue blockage.

**Root Cause**

Deployment queues can become blocked due to a previous failed or stuck deployment that did not release its queue slot, or due to a transient platform-side infrastructure issue on the Launch cluster. In some cases, a failed deployment leaves the queue in an inconsistent state that prevents subsequent deployments from starting.

**Resolution**

1.  Wait for 10–15 minutes to allow the queue to self-clear, as some transient queue states resolve automatically.
    
2.  Navigate to the Deployments section of the affected Launch environment and attempt a manual redeploy by clicking the Redeploy button on the most recent deployment.
    
3.  If the queue remains stuck after redeployment attempts, contact Contentstack Support with the project UID, environment UID, and the time the queue became stuck so that the Launch team can manually clear the queue.
    
4.  Once the queue is cleared, trigger a fresh deployment and monitor the deployment logs to confirm it progresses through the build and deployment stages.
    

The issue is resolved when the deployment exits the queued state, completes successfully, and the live environment reflects the intended changes.

### Fixing Deployment Failures Caused by SSH Key Formatting (CF001 Error)

A Launch deployment fails with a CF001 error or a “Deployment failed: Please try to redeploy the site” message. The error is often associated with SSH key configuration for private repository access or server-side deployment settings.

**Root Cause**

CF001 deployment errors can occur when an SSH private key has been pasted into the Launch environment variable field with incorrect formatting, specifically, missing or broken line breaks. The PEM format of SSH private keys requires precise line breaks, and a key pasted as a single line or with escaped newlines will be rejected during the deployment authentication step.

**Resolution**

1.  Navigate to the affected Launch environment settings and locate the SSH private key environment variable.
    
2.  Click the Form Edit mode (or equivalent multi-line input option) for the SSH key field rather than the standard single-line text input.
    
3.  Paste the SSH private key in Form Edit mode, ensuring that all line breaks within the PEM block are preserved correctly (each line of the key on its own row).
    
4.  Save the updated environment variable and trigger a new deployment.
    
5.  Monitor the deployment logs to confirm the SSH key is accepted and the deployment progresses past the authentication step.
    

The issue is resolved when the deployment completes successfully without CF001 errors and the live environment reflects the deployed changes.

### Resolving Empty Environment Variable Values Causing Stuck Updates

Updating an environment variable in a Launch project - for example, clearing its value to make it empty - causes the update process to get stuck without displaying an error message or completing. The environment variable update spinner runs indefinitely.

**Root Cause**

Launch does not support empty string values for environment variables. When a variable value is cleared and saved, the platform attempts to process an empty value, which causes the update operation to hang rather than returning a clear validation error.

**Resolution**

1.  If an environment variable is no longer needed, delete it entirely from the environment variables list rather than clearing its value.
    
2.  If a placeholder value is required, set a non-empty string (such as a space, a zero, or a placeholder like DISABLED) that the application can handle appropriately.
    
3.  If the update is already stuck, refresh the page to cancel the pending operation, then either delete the variable or set it to a non-empty value.
    

The issue is resolved when the environment variable is successfully deleted or updated to a valid non-empty value, and the Launch environment reflects the intended configuration.

## Node.js, Frameworks & Runtime

### Preparing for Node.js v18 Deprecation in Launch

Contentstack Launch is deprecating Node.js v18 support. After the deprecation date, any deployment or redeployment that targets Node.js v18 will fail. Existing live sites running on Node.js v18 will continue to serve traffic until they are next redeployed.

**Root Cause**

Node.js v18 has reached end-of-life and is no longer receiving security updates. Launch is removing support for deprecated runtime versions to maintain a secure build environment.

**Resolution**

1.  Identify all Launch projects currently running on Node.js v18 by reviewing the package.json engines field or the build log output that states the Node.js version in use.
    
2.  Update the Node.js version in package.json to a supported LTS version (such as v20 or v22) in the engines field: { "engines": { "node": ">=20" } }.
    
3.  Test the updated configuration locally and in a non-production Launch environment before promoting to production.
    
4.  Trigger a new deployment in each affected Launch environment to apply the Node.js version change.
    
5.  Monitor official Contentstack release notes for the exact deprecation date and confirm all projects are migrated before that date.
    

The issue is resolved when all Launch projects build and deploy successfully using a supported Node.js version, and no v18-related deprecation warnings appear in the deployment logs.

### Fixing Module Resolution Errors When Using Turbopack in Launch

A Launch deployment fails during the build phase with module not found or module resolution errors. The project builds successfully locally but fails in the Launch environment. The build command does not include the Turbopack flag.

**Root Cause**

When a Next.js project uses path aliases (configured via tsconfig.json or jsconfig.json) and Turbopack as the bundler, the build command must explicitly include the --turbo flag for Launch to resolve module paths correctly. Without this flag, the build environment may use a different resolution strategy that does not honor the path alias configuration.

**Resolution**

1.  Verify that path aliases are defined in tsconfig.json or jsconfig.json and that the project uses Turbopack as the bundler (indicated by next dev --turbo in local scripts).
    
2.  Update the Launch build command to include the --turbo flag: next build --turbo.
    
3.  Validate that the alias paths configured in tsconfig.json correspond to the actual directory structure within the build output directory.
    
4.  Trigger a new deployment with the updated build command and review the deployment logs to confirm module resolution succeeds.
    

The issue is resolved when the build completes without module resolution errors and the deployed application renders correctly in the Launch environment.

### Serving .well-known Files From a Monorepo Project in Launch

A project deployed from a monorepo needs to serve files from a .well-known directory (such as apple-app-site-association for universal linking). The files are placed at the monorepo root but are not accessible at the deployed domain.

**Root Cause**

Launch deploys content based on the build output of the specific site selected within the monorepo, not from the monorepo root. Files placed at the root of the repository are not included in the site’s build output and are therefore not served by Launch.

**Resolution**

1.  Place the .well-known directory and its files inside the public folder of the specific site being deployed (e.g., apps/my-site/public/.well-known/).
    
2.  The framework (e.g., Next.js) will automatically include files in the public directory in the build output and serve them at the root of the deployed domain.
    
3.  Confirm that the .well-known path is not excluded by any .gitignore or build ignore rules.
    
4.  Trigger a new deployment and verify that the .well-known files are accessible at https://your-domain.com/.well-known/apple-app-site-association or the relevant path.
    

The issue is resolved when the .well-known files are publicly accessible at the correct URL path on the deployed Launch domain.

### Resolving Serverless Function Webhook Timeout Errors (ECONNABORTED)

A webhook configured to trigger a Launch serverless function consistently fails with a timeout error (ECONNABORTED). The webhook logs show that requests are being sent but the function does not return a response within the expected timeframe.

**Root Cause**

Launch serverless function environments may expect a synchronous handler signature. When an async function is used without a synchronous wrapper, the runtime may not correctly await the response, causing the connection to time out before the function completes execution.

**Resolution**

1.  Wrap the async function logic inside a synchronous handler function that the Launch runtime can correctly invoke.
    
2.  Within the synchronous wrapper, call the async function and ensure the promise resolves before the handler exits, for example by using a callback or by structuring the wrapper to block until resolution.
    
3.  Test the function locally with a simulated webhook payload to confirm it responds within the expected timeout window.
    
4.  Redeploy and trigger the webhook again, checking the function logs to confirm a successful response is returned.
    

The issue is resolved when the webhook receives a successful HTTP response from the Launch function within the timeout threshold and ECONNABORTED errors no longer appear in the webhook logs.

## Caching, CDN & Content Delivery

### Implementing Dynamic Cache Priming on Launch

After a deployment, the CDN cache is empty and all requests are served from the origin until the cache is populated organically. For large sites, this creates a period of elevated origin load and slower response times for end users immediately after a release.

**Root Cause**

Launch does not natively provide an automated cache priming mechanism. After each deployment, the CDN cache starts fresh and is populated only as users request pages. Sites with many pages or high traffic sensitivity need a pre-warming step to avoid performance degradation post-deployment.

**Resolution**

1.  Create a pre-build script that fetches all page URL paths from the Contentstack Delivery API by querying the relevant content types.
    
2.  Write the fetched URLs into the launch.json file or a custom cache manifest as part of the prebuild step.
    
3.  Configure the prebuild step to run automatically before the main build command by adding it to the package.json scripts as: "prebuild": "node scripts/prime-cache.js".
    
4.  After deployment, the priming script can send HTTP GET requests to each URL to warm the CDN cache. Throttle the requests to avoid overloading the origin.
    
5.  Use Contentstack Automate to trigger a cache priming webhook on each publish event so that new or updated entries are automatically included in the next cache warm cycle.
    

The issue is resolved when post-deployment response times remain consistent and origin load does not spike after a new release due to a cold cache.

### Handling Cache Loss on Redeployment in Launch

A Launch project loses its locally cached data each time a new deployment is triggered. This is particularly disruptive for applications that build a content cache at startup and rely on it across requests, as each deployment resets the cache to zero.

**Root Cause**

Launch deployments run in ephemeral build environments. Each deployment creates a fresh instance, and any in-memory or local file system cache from the previous deployment is not carried forward. Local caches cannot persist across deployments in this architecture.

**Resolution**

1.  Move cache data to an external persistent store such as Redis, a database (e.g., MongoDB or PostgreSQL), or a cloud storage bucket (e.g., AWS S3 or Google Cloud Storage).
    
2.  Update the application to read from and write to the external cache store rather than the local file system or in-memory cache.
    
3.  On application startup, populate the external cache if it is empty, and serve from it on subsequent requests.
    
4.  Use Contentstack Automate webhooks to invalidate or refresh specific cache entries when content is published, rather than rebuilding the entire cache on each deployment.
    

The issue is resolved when cache data persists across deployments and the application does not incur a full cache rebuild cost after each release.

### Understanding CDN Revalidation Limitations for Query-Based or Pattern URLs

A Next.js site on Launch uses Contentstack Automate to trigger CDN cache revalidation when content is published. However, the revalidation only invalidates prefix-based URL patterns and does not support query string parameters or wildcard patterns. This causes stale content to be served for URLs with query strings after a content update.

**Root Cause**

Contentstack Automate’s CDN revalidation feature uses a prefix-based URL matching approach. It does not currently support query-aware or pattern-specific URL revalidation. URLs that include query strings (such as ?category=news) are not matched by prefix-only rules, so cache entries for those URLs are not invalidated when the trigger fires.

**Resolution**

1.  Accept that the current prefix-based approach is the supported method for CDN revalidation via Automate. Design URL structures to use path segments rather than query strings where cache invalidation is critical.
    
2.  For URLs that must use query strings, implement application-level cache control by setting short Cache-Control max-age headers on query-parameterized responses to reduce the window in which stale content is served.
    
3.  Alternatively, use Next.js ISR (Incremental Static Regeneration) with a short revalidation interval for pages that use query-parameterized data, so the CDN automatically refreshes stale content within a defined time window.
    
4.  Monitor Contentstack release notes for updates to the Automate CDN revalidation feature, as pattern-based and query-aware invalidation may be added in future releases.
    

The issue is resolved when content updates are reflected within an acceptable timeframe for all URL patterns, either through prefix invalidation, short cache TTLs, or ISR revalidation.

### Blocking Launch-Hosted Sites From Search Engine Indexing

Internal or staging Launch-hosted sites are appearing in Google search results. This can expose pre-production content, duplicate indexed pages, or reveal internal tools to the public.

**Root Cause**

If a Launch-hosted site is publicly accessible without authentication, search engine crawlers can discover and index it—especially if the domain is referenced in sitemaps, links, or social shares. There is no platform-level setting in Launch to block crawlers automatically for non-production environments.

**Resolution**

1.  Implement a Launch Edge Function that inspects the User-Agent header of incoming requests and returns a 403 response (or serves a robots.txt with Disallow: /) for known search engine crawler agents.
    
2.  Add a robots.txt file to the public directory of the site with Disallow: / to instruct crawlers not to index the site.
    
3.  Set the X-Robots-Tag: noindex, nofollow response header via the Edge Function for all responses to prevent indexing even if crawlers access the site.
    
4.  For staging environments, consider restricting access using HTTP Basic Authentication or IP allowlisting via the CDN to prevent unauthorized access entirely.
    

The issue is resolved when the Launch-hosted site no longer appears in new search engine index results and existing indexed pages are removed following a Search Console removal request or natural cache expiry.

### Understanding Launch CDN and WAF vs. Akamai Compatibility

An organization considering or currently using Akamai as a CDN or WAF layer on top of Contentstack Launch asks whether Akamai is supported or recommended as an additional network layer in front of Launch.

**Root Cause**

Launch includes a built-in CDN and Web Application Firewall (WAF). Placing a separate CDN or WAF such as Akamai in front of Launch creates a double-CDN architecture that can cause performance degradation, cache conflicts, and routing issues. The additional network layer is generally not recommended.

**Resolution**

1.  Rely on the built-in Launch CDN and WAF capabilities for content delivery, caching, and perimeter security, additional CDN layers are not needed and can be counterproductive.
    
2.  If your organization requires Akamai for other parts of the stack, work with your infrastructure team to ensure Akamai is not placed in front of Launch-hosted properties.
    
3.  If using Akamai in front of Launch is a hard requirement, contact Contentstack Support to discuss configuration constraints and potential compatibility issues before implementation.
    
4.  Review Launch documentation on CDN and WAF capabilities to understand what is provided natively before adding third-party network layers.
    

The issue is resolved when the network architecture is clarified and the Launch-hosted site performs correctly with the built-in CDN without additional intermediary layers.

### Fixing Slow Load Times Caused by no-store Cache-Control Headers

A Launch-hosted site experiences slow load times (30–60 seconds) and intermittent 5xx errors, primarily in certain browsers. The frequency of 5xx errors is too low to explain the performance issue on its own.

**Root Cause**

The application was sending cache-control headers such as no-store, max-age=0, and must-revalidate on responses. These directives prevent any caching and force every request to be processed by the origin server, significantly increasing load times under normal traffic.

**Resolution**

1.  Audit the cache-control headers currently being sent by the application across key page types (homepage, listing pages, detail pages).
    
2.  Identify which routes are unnecessarily using no-store, max-age=0, or must-revalidate when content does not change on every request.
    
3.  Implement an intermediate caching strategy with a short time-to-live (for example, 5–10 minutes) for pages where content updates are infrequent, rather than disabling caching entirely.
    
4.  Ensure a cache purge or revalidation workflow is triggered whenever content is updated from the CMS, so cached pages are refreshed promptly after publishing.
    
5.  Validate that the updated caching strategy does not interfere with other ongoing work (such as redirect logic or migration activities) before rolling it out broadly.
    
6.  Apply the caching strategy across the full site and monitor load times to confirm improvement.
    

The issue is resolved when page load times return to expected levels and the origin server no longer receives a disproportionate volume of uncached requests.

### Understanding Cache Revalidation Rate Limit Windows and Automation Thresholds

Teams using the Launch cache revalidation feature need clarity on how the rate limit “day” is defined (a fixed UTC day versus a rolling window), when the limit resets, and what the actual soft and hard automation thresholds are for their organization, especially when documentation or prior guidance appears inconsistent with observed behavior.

**Root Cause**

The cache revalidation rate limit uses a rolling 24-hour window rather than a fixed calendar day, each revalidation call counts against the limit for 24 hours from the moment it was triggered, and the reset time depends on when those specific requests were made. Automation soft and hard limits are configured per organization and may differ from generic figures previously communicated.

**Resolution**

1.  Confirm with Contentstack Support the exact soft and hard automation limits configured for your specific organization, as these can vary and may not match generic documentation figures.
    
2.  Understand that the cache revalidation limit operates on a rolling 24-hour window: each call remains counted against the limit for 24 hours from when it was made, not from a fixed daily reset time.
    
3.  Use the in-product notifications available in the Launch UI, which surface alerts at 80% of the limit and when the limit is reached, including the specific timestamp when the rate limit will reset.
    
4.  Monitor your organization’s automation usage against the confirmed soft and hard limits to proactively avoid hitting the threshold.
    
5.  If a separate connector-related issue (such as missing error feedback when a rate limit is exceeded) is also observed, track it as a distinct case rather than conflating it with the rate-limit definition question.
    

The issue is resolved when the team has accurate, organization-specific figures for the rate limit thresholds and understands the rolling-window reset behavior, with in-product notifications relied upon for ongoing visibility.

## Security, Compliance & Integrations

### Automating Launch Deployments via CI/CD With MFA-Enabled Accounts

A CI/CD pipeline (such as Azure DevOps) that deploys to Contentstack Launch using username and password authentication is blocked by multi-factor authentication (MFA). Manual MFA confirmation cannot be automated in a pipeline context, preventing fully automated deployments.

**Root Cause**

Username and password authentication for Launch CLI is subject to the same MFA enforcement applied to interactive user logins. Automated pipelines cannot complete the MFA challenge, causing the authentication step to fail. Two approaches exist depending on whether SSO Strict Mode is enabled on the organization.

**Resolution**

1.  Option 1 - TOTP-Based Authentication (applicable when SSO Strict Mode is _not_ enabled): Set the CONTENTSTACK\_MFA\_TOKEN environment variable in the CI/CD pipeline to a TOTP (Time-based One-Time Password) value generated by an authenticator app.
    
2.  This token must be refreshed each pipeline run as TOTP values expire every 30 seconds. Use a pipeline secret or dynamic token retrieval mechanism to automate this.
    
3.  Option 2 - Personal Access Token or OAuth (recommended for SSO-enabled organizations): Generate a Contentstack Personal Access Token (PAT) from your user profile settings.
    
4.  Configure the Launch CLI in the CI/CD pipeline to authenticate using the PAT instead of username and password.
    
5.  Store the PAT as a secure pipeline secret variable and pass it to the CLI via the appropriate flag or environment variable.
    
6.  Verify that the PAT has the required permissions to trigger deployments for the target Launch environment.
    

The issue is resolved when the CI/CD pipeline completes the Launch CLI authentication step without manual MFA intervention and deployments trigger automatically on each pipeline run.

### Understanding Launch’s Dynamic IP Architecture and Alternatives to Static IP Allowlisting

An organization needs to allowlist the IP addresses used by Contentstack Launch in their Cloudflare WAF or other network perimeter tools to ensure uninterrupted communication. The organization requests a static list of IPs from Contentstack Support.

**Root Cause**

Contentstack Launch does not maintain static or fixed IP addresses. The platform uses a dynamically scaling cloud infrastructure where IP addresses are assigned and released automatically. There is no fixed IP list that can be provided for allowlisting purposes, as the IPs change as the infrastructure scales.

**Resolution**

1.  Do not attempt to allowlist by IP address for Launch traffic, as the dynamic nature of the infrastructure means any list will become outdated quickly.
    
2.  Use identity-based security controls instead, such as API key validation, OAuth token verification, or request signing—to authenticate communication between your infrastructure and Launch.
    
3.  If your WAF requires source IP allowlisting and Launch is the origin, configure the WAF rule to allow traffic based on the hostname or domain rather than IP address.
    
4.  For Log Targets specifically, note that Launch Log Targets also use dynamic source IPs, configure the destination log system to accept connections from any IP and rely on authentication credentials (such as API keys or OTEL tokens) for security.
    

The issue is resolved when the network configuration uses identity-based controls rather than IP allowlisting, and communication between Launch and external systems is uninterrupted.

### Forwarding Launch Logs to Splunk via an OTEL Collector

A Launch Log Target configured to send logs directly to a Splunk Cloud HTTP Event Collector (HEC) endpoint fails because Splunk Cloud’s default HEC endpoint does not support the gRPC OTLP protocol required by Launch.

**Root Cause**

Launch Log Targets require a secure gRPC OTLP endpoint. Splunk Cloud’s standard HEC endpoint uses HTTP/HTTPS and is not OTLP-compatible. A direct Launch-to-Splunk connection is therefore not supported without an intermediary layer that translates between the two protocols.

**Resolution**

1.  Deploy an OpenTelemetry (OTEL) Collector as an intermediary service (e.g., on a cloud VM or container service).
    
2.  Configure the OTEL Collector to accept gRPC OTLP input on a secure endpoint.
    
3.  Set up an OTEL Splunk exporter in the Collector configuration to forward received logs to Splunk Cloud’s HEC endpoint.
    
4.  In the Launch Log Target settings, point the Log Target Endpoint to the OTEL Collector’s secure gRPC OTLP endpoint.
    
5.  Verify that logs appear in Splunk by triggering actions that generate log entries (such as a site visit or function execution) and checking the Splunk index.
    

The issue is resolved when application and edge function logs generated by Launch appear correctly in the configured Splunk index via the OTEL Collector.

### Reconnecting GitHub OAuth After Token Expiry or 403 Errors

Deployments from a GitHub-connected Launch project begin failing with 403 Forbidden errors. The GitHub integration status may show as disconnected or the deployment logs indicate an OAuth authentication failure.

**Root Cause**

GitHub OAuth tokens used by the Launch GitHub integration can expire or become invalidated—for example, when a GitHub organization admin revokes the token, the GitHub App permissions change, or the token exceeds its validity period. An expired or revoked token causes all deployment triggers from the affected repository to fail with authentication errors.

**Resolution**

1.  Navigate to the Launch project settings and initiate a GitHub reconnection by selecting the option to disconnect and reconnect the Git provider.
    
2.  As a GitHub Admin for the repository or organization, reinstall the Contentstack GitHub App by navigating to GitHub Settings > Applications > Installed GitHub Apps and reinstalling the Contentstack app.
    
3.  Complete the OAuth authorization flow in the Launch UI to generate a fresh token.
    
4.  Trigger a test deployment after reconnection to confirm the new OAuth token is accepted and deployments succeed.
    

The issue is resolved when the GitHub integration shows as connected, deployments trigger successfully from the repository, and 403 errors no longer appear in deployment logs.

### Handling External Security Vulnerability Reports for Launch-Hosted Domains

An EASM (External Attack Surface Management) tool flags vulnerabilities on a domain that the customer believes is hosted on Contentstack Launch. The customer requests Contentstack’s assistance in assessing or remedying the reported vulnerabilities.

**Root Cause**

EASM tools scan publicly accessible domains and may attribute vulnerabilities to Contentstack Launch based on DNS records or hosting patterns, even when the domain is not actually hosted on Launch. Misattribution is common when subdomains have mixed hosting environments.

**Resolution**

1.  Verify whether the flagged domain is actually hosted on Contentstack Launch by checking the Launch dashboard for a matching project and domain configuration.
    
2.  If the domain is not in Launch, inform the EASM tool owner that the vulnerabilities are not attributable to Contentstack Launch and advise them to investigate the actual hosting provider for that domain.
    
3.  If the domain is hosted on Launch, share the full EASM report with Contentstack Support so the Launch security team can assess the findings.
    
4.  Work with the Contentstack security team to implement any required remediations, such as updating TLS configuration, response headers, or CDN security settings.
    

The issue is resolved when the hosting of the affected domain is confirmed, and either the vulnerability is attributed to the correct provider or the Launch team has implemented the necessary security remediations.

## Apex Domains & Go-Live

### Adding Apex Domains to a Launch Project

An attempt to add an apex domain (e.g., example.com without the www prefix) to a Launch project through the UI fails or is not supported through the standard domain addition flow.

**Root Cause**

Apex domain configuration in Launch requires manual setup by the Launch team due to DNS constraints, apex domains cannot use CNAME records and instead require an A record pointing to a specific IP address provided by the platform. This configuration is not available through self-service in the Launch UI.

**Resolution**

1.  Contact Contentstack Support and request apex domain configuration, providing the domain name and the Launch project and environment UIDs.
    
2.  Support will engage the Launch team, who will provide the DNS A record (IP address) to which the apex domain should point.
    
3.  Update the DNS A record at your authoritative DNS provider to point the apex domain to the provided IP address (e.g., 151.101.66.137).
    
4.  The Launch team will complete the domain registration and SSL provisioning on their end.
    
5.  Verify the apex domain resolves correctly by accessing it in a browser and confirming that the SSL certificate is valid.
    

The issue is resolved when the apex domain resolves to the Launch application and the SSL certificate is provisioned and active.

### Eliminating Recurring TXT Record Updates Using Cloudflare Delegated DCV

TXT records used for SSL certificate domain control validation (DCV) must be updated manually each time the certificate renews. For organizations with many domains, this creates a recurring operational burden.

**Root Cause**

Standard TXT-based DCV requires a new unique TXT record value each time a certificate renews. Cloudflare’s Delegated Domain Control Validation (DCV) feature eliminates this by allowing the platform to complete DCV automatically using a CNAME delegation, removing the need for recurring manual TXT record updates.

**Resolution**

1.  At your authoritative DNS provider, add a CNAME record for the \_acme-challenge subdomain of each affected domain, pointing it to the Cloudflare DCV endpoint provided by the Launch team. Example: \_acme-challenge.www.example.com CNAME www.example.com.<unique-id>.dcv.cloudflare.com
    
2.  Contact Contentstack Support to obtain the specific unique-id value for your domain from the Launch team.
    
3.  Once the CNAME record is in place, Cloudflare will handle DCV automatically on each certificate renewal without requiring further manual TXT record changes.
    
4.  Verify that SSL certificates for the affected domains auto-renew without generating DCV validation errors in the Launch dashboard.
    

The issue is resolved when SSL certificates renew automatically and no manual TXT record updates are required at renewal time.

### Resolving Unsupported Protocol Errors Caused by Dots in Subdomains

A Launch-hosted domain returns an unsupported protocol error or fails to provision correctly when the subdomain contains a dot character (e.g., v2.staging.example.com as a single label).

**Root Cause**

Dots within a subdomain label (as opposed to dots separating subdomain levels) are not supported in Launch’s domain registration system. The platform interprets additional dots as subdomain level separators, which can cause routing, SSL provisioning, or validation errors.

**Resolution**

1.  Replace any dots within a subdomain label with hyphens. For example, change v2.staging to v2-staging.
    
2.  Update the domain in the Launch UI to use the hyphen-formatted subdomain.
    
3.  Update the corresponding DNS CNAME record at your DNS provider to use the new subdomain format.
    
4.  Verify that SSL provisioning completes and the domain resolves correctly after the change.
    

The issue is resolved when the updated subdomain (using hyphens instead of dots) is accessible over HTTPS without protocol or routing errors.

## API & Platform Behavior

### Empty JSON Response Bodies When statusCode Is Present in Small Payloads (Resolved Platform Issue)

API responses from Launch-hosted endpoints returned the correct HTTP status code, but the response body was empty whenever the payload included a “statusCode” field and contained fewer than approximately seven properties. This behavior was consistent across multiple endpoints and was identified as a recent regression.

**Root Cause**

This was a platform-level regression in how Launch serialized small JSON payloads that included a field named “statusCode.” The presence of this field combined with a low property count caused the response body to be dropped while the correct HTTP status code was still returned.

**Resolution**

1.  If you observe a request returning a correct HTTP status code (e.g., 200, 422) but an empty response body, check whether the payload includes a “statusCode” property and has fewer than approximately seven total properties, this combination matches the known regression pattern.
    
2.  Report the issue to Contentstack Support with sample request/response pairs and the affected endpoint so it can be confirmed against the known issue.
    
3.  This specific regression has already been fixed by the Launch engineering team and confirmed resolved by the reporting customer. No application-side workaround is required once your environment reflects the platform fix.
    
4.  If empty response bodies persist after the platform fix, treat it as a new issue rather than a recurrence of this one, and report it separately with full request/response details.
    

The issue is resolved on the platform side. Confirm your environment reflects the fix by sending a small payload containing a “statusCode” property and verifying the full JSON response body is returned.

### Fixing 403 FORBIDDEN_RESOURCE Errors Caused by an Incorrect Organization ID Parameter

Calls to the Launch API using a valid Authtoken consistently fail with a 403 Forbidden error tagged launch.FORBIDDEN\_RESOURCE, even though the authentication headers and Authtoken appear correct.

**Root Cause**

The request was passing an incorrect parameter name for the organization identifier. The Launch API requires the header to be named organization\_uid; using a different or malformed parameter name causes the platform to reject the request as unauthorized for the requested resource, even when the Authtoken itself is valid.

**Resolution**

1.  Review the headers being sent with the Launch API request and confirm the organization identifier is passed using the exact header name organization\_uid.
    
2.  Ensure the Authtoken header is also included and correctly formatted alongside the organization\_uid header.
    
3.  Update the API client or script to use the corrected header name and re-send the request.
    
4.  Confirm that the 403 FORBIDDEN\_RESOURCE error no longer appears and that the API returns the expected resource data.
    

The issue is resolved when Launch API calls authenticate successfully using the Authtoken and the correctly named organization\_uid header, with no further 403 errors.

### Scoping CDN Cache Revalidation to a Specific Path Using environmentId

When calling the Launch revalidate-cdn-cache endpoint with both a hostname and a cachePath parameter combined in the same request, the platform purges the entire hostname’s cache instead of limiting the purge to the specified path.

**Root Cause**

The Launch API supports only one revalidation strategy per request: cachePath, hostnames, or cacheTags. Combining hostnames and cachePath in the same payload is not supported and results in the broader hostname-level purge rather than the intended scoped purge.

**Resolution**

1.  To achieve scoped revalidation limited to a specific deployment, target the specific environmentId together with the required cachePath in the request, rather than combining hostnames with cachePath.
    
2.  This environmentId and cachePath combination limits the purge to the deployment associated with that environment, achieving the scoped behavior that combining hostnames and cachePath does not provide.
    
3.  If multiple revalidation strategies are required (for example, purging by both cacheTags and a specific path), make separate API calls for each strategy rather than attempting to combine them in a single request.
    
4.  Update any existing automation or scripts that currently combine hostnames and cachePath to instead use the environmentId and cachePath pattern for predictable, scoped purges.
    

The issue is resolved when cache revalidation calls using environmentId and cachePath correctly limit the purge to the intended deployment, without unintentionally invalidating the entire hostname cache.

### Resolving Intermittent API Connectivity Errors (ETIMEDOUT/ECONNREFUSED) From Launch Environments

Requests from a Launch-hosted application to the Content Delivery API intermittently fail with TCP-level errors such as ETIMEDOUT and ECONNREFUSED, generating alerts even though external API monitoring shows normal platform uptime.

**Root Cause**

Investigation showed the failures were primarily 500-level responses generated at the application layer rather than a platform-wide outage. Outbound connection handling in the hosting environment, combined with high concurrency, can produce intermittent TCP-level failures that surface as ETIMEDOUT or ECONNREFUSED at the client.

**Resolution**

1.  Review application logs to confirm whether the errors correlate with periods of high concurrency or specific deployment events.
    
2.  Enable HTTP/HTTPS keep-alive in your API client configuration to reduce the overhead of repeatedly establishing new TCP connections.
    
3.  Configure retry logic with exponential backoff and appropriate custom timeout settings in the Content Delivery API client to gracefully handle transient connection failures.
    
4.  Enforce IPv4 resolution in the application’s network configuration if dual-stack resolution is contributing to instability.
    
5.  Implement stale-while-revalidate caching so the application can continue serving a recent cached response while a fresh one is fetched in the background, reducing the impact of any individual failed request.
    
6.  Introduce request deduplication to avoid issuing multiple identical concurrent requests for the same data, which reduces unnecessary load during traffic spikes.
    
7.  Apply a concurrency cap on outbound API requests to prevent the application from overwhelming its own connection pool during periods of high concurrency.
    
8.  Monitor error rates after applying these changes to confirm a reduction in ETIMEDOUT and ECONNREFUSED occurrences, and roll the optimizations out to production as part of your regular release cycle once validated.
    

The issue is resolved when API requests from the Launch environment complete reliably under normal and high-concurrency conditions, with caching, deduplication, concurrency limits, and retry logic together absorbing any remaining transient failures.

### Resolving sync_token Undefined Errors in gatsby-source-contentstack

A site using gatsby-source-contentstack to fetch content fails during the build with the error TypeError: Cannot read properties of undefined (reading 'start'), traced back to an undefined sync\_token value.

**Root Cause**

The error was tied to the version of gatsby-source-contentstack in use. Changing the package version resolved the issue, though the source ticket does not document the specific internal mechanism that was at fault.

**Resolution**

1.  Check the currently installed version of gatsby-source-contentstack in your package.json.
    
2.  Change the package to a different version (the customer’s case was resolved by a version change, though the specific target version was not documented in the source ticket, testing the latest stable release is a reasonable starting point).
    
3.  Rebuild the site and confirm the TypeError no longer occurs and content syncs correctly.
    
4.  If the error persists after the version change, gather the specific package versions tested and report them to Contentstack Support along with the full error stack trace for further investigation.
    

The issue is resolved when the build completes successfully and content fetched via gatsby-source-contentstack syncs without the sync\_token-related errors.

### Resolving Recurring “Azure Container Does Not Exist” Errors After Failed Deployments

A Launch-hosted site repeatedly goes down with an “Azure container does NOT exist” error, occurring shortly after a failed deployment. The error had previously been reported and addressed, but recurred following a subsequent failed deployment.

**Root Cause**

When a deployment fails, the underlying container infrastructure could, in some cases, enter a state where the previous live container was already being torn down before the new one was confirmed healthy, resulting in a window where no valid container existed to serve traffic. This caused customer-facing downtime rather than a graceful fallback to the last known-good deployment.

**Resolution**

1.  Confirm the timing correlation between the failed deployment and the onset of the “Azure container does NOT exist” error by reviewing deployment logs and incident timestamps.
    
2.  Report the recurrence to Contentstack Support with the organization ID, the failed deployment ID, and the exact timestamps of failure and downtime.
    
3.  Contentstack Engineering implements platform-level safeguards to ensure a site does not enter a non-serving state due to a failed deployment, regardless of whether the failure is an application build error or an infrastructure-related issue.
    
4.  After the safeguard is deployed, monitor subsequent deployments (including any that fail) to confirm the live site remains available rather than entering the container-not-found state.
    
5.  If ETIMEDOUT-related deployment failures continue to occur as a separate but related issue, track them under a dedicated case for ongoing resolution.
    

The issue is resolved when failed deployments no longer cause customer-facing downtime, with the platform retaining the last successful container until a new deployment is confirmed.

### Clarifying npm Version Downgrade Warnings in Build Logs

Build logs for a Launch deployment show a message indicating an npm version downgrade, raising concern that this is causing build failures or deployment issues.

**Root Cause**

In this case, the npm version message in the build log was an informational notice rather than the actual cause of the build failure. The real build issues were resolved separately through dependency overrides, and the npm message did not require any corrective action on its own.

**Resolution**

1.  Read the full npm version message in the build log carefully to distinguish between an informational notice and an actual error or failure condition.
    
2.  If genuine build failures are present alongside the npm message, investigate those independently, for example, by reviewing dependency version conflicts and applying overrides in package.json where needed.
    
3.  Apply any necessary dependency overrides to resolve genuine build issues, separate from the npm version notice.
    
4.  Redeploy and confirm that builds complete successfully, and that the npm version message (if it still appears) does not correspond to an actual failure.
    

The issue is resolved when deployments complete successfully and the team understands that an npm version notice in build logs is not inherently indicative of a deployment failure.

### Handling Production Regressions After Platform-Initiated Node.js Runtime Upgrades

Following a platform-initiated upgrade of the Node.js runtime (for example, from v22 to v24), a Launch-hosted application experiences production regressions despite builds and deployments completing successfully. Symptoms include failures in Chromium-based PDF generation and filesystem errors (ENOENT and EROFS) when the application attempts to write to its build cache directory.

**Root Cause**

Two distinct issues surfaced from the runtime upgrade: first, Chromium-based functionality failed due to a missing system-level dependency (libnspr4.so) in the newer Node.js runtime image. Second, filesystem errors occurred because Launch environments operate on a read-only filesystem across all Node.js versions, with only the /tmp directory writable—a behavior that was likely already present but became more apparent or differently triggered after the upgrade.

**Resolution**

1.  For Chromium-related failures, temporarily pin the application to the previous stable Node.js version by specifying it in the engines field of package.json (e.g., "node": "22.x") while the missing dependency is investigated by the platform team.
    
2.  For filesystem errors, update the application configuration to redirect all cache writes to the /tmp directory - for example, by setting NEXT\_CACHE\_DIR=/tmp/.next/cache for Next.js applications.
    
3.  Audit the application for any other file write operations that target directories outside of /tmp, and redirect those as well.
    
4.  Share details of your Chromium setup (such as the specific library or headless browser configuration in use) with Contentstack Support to assist in resolving the missing dependency on the platform side.
    
5.  Monitor for platform updates addressing the missing Chromium dependency, and plan to remove the Node.js version pin once confirmed resolved.
    

The issue is resolved when Chromium-based functionality operates correctly (either via the version pin or a platform-side dependency fix) and all application file writes succeed by targeting only the /tmp directory.

## Application Performance & Resource Management

### Diagnosing CPU and Memory Exhaustion on Long-Running Launch Containers

A Launch-hosted application becomes unstable or experiences repeated downtime, with CPU and memory utilization climbing toward 100%. The instability may not have been visible previously because frequent redeployments were effectively resetting the application containers.

**Root Cause**

This is application-specific resource consumption behavior, not a platform-level fault. When redeployment frequency decreases—for example, after resolving an unrelated deployment issue, containers run for longer uninterrupted periods, exposing underlying memory leaks or unbounded resource growth that redeployments had been masking. The absence of caching on the site can also contribute to sustained high resource usage.

**Resolution**

1.  Review CPU and memory utilization graphs for the affected environment to confirm a gradual climb toward 100% over time rather than a sudden spike.
    
2.  As an immediate mitigation, increase the allocated CPU and memory for the affected environment (for example, from 1 vCPU/2 GiB to 2 vCPU/4 GiB) to provide headroom while a permanent fix is implemented.
    
3.  If utilization continues to climb even after the resource increase, configure scheduled force restarts (for example, hourly) as an interim mitigation to reset accumulated memory usage.
    
4.  Investigate the application code for memory leaks, unbounded caches, or repeated allocations that are not being garbage collected.
    
5.  Implement caching at the application or CDN layer to reduce the volume of requests that require full server-side processing, lowering sustained CPU and memory load.
    

The issue is resolved when CPU and memory utilization remain stable over extended periods without requiring scheduled restarts, and the application no longer experiences instability-related downtime.

### Diagnosing Third-Party Script Render Blocking on Launch-Hosted Pages

Specific pages on a Launch-hosted site experience 15–30 second initial load times with partial rendering. Third-party widgets (such as chat or virtual sales assistant scripts) fail to populate, leaving the page in a frozen state where only static elements are visible.

**Root Cause**

The delay was reproducible outside of the Launch environment, confirming the root cause as internal application logic and third-party script loading behavior rather than a Launch platform issue. Synchronous or blocking script loading patterns for third-party widgets can hold up page rendering significantly.

**Resolution**

1.  Reproduce the slow load and partial rendering behavior in a local development environment to confirm the issue is application-level rather than platform-level.
    
2.  Identify which third-party scripts are loaded synchronously or block the main render thread during page load.
    
3.  Update the script loading strategy to use async or defer attributes, or load third-party widgets after the main content has rendered (for example, using a loading strategy like Next.js’s next/script with an appropriate strategy prop).
    
4.  Test the updated loading strategy to confirm that hero content and primary UI render immediately while third-party widgets populate progressively without blocking the page.
    
5.  Deploy the fix and monitor real-user load time metrics to confirm the 15–30 second delay is eliminated.
    

The issue is resolved when affected pages render primary content immediately and third-party widgets populate without causing a frozen or partially rendered page state.

### Investigating SSR Response Time Differences Between Launch and Other Hosting Providers

A team comparing server-side rendering (SSR) performance between Contentstack Launch and another hosting provider (such as Vercel) observes page component resolution times exceeding 2 seconds on Launch for the same codebase, which cannot be replicated on the comparison platform.

**Root Cause**

Comparative load testing using simulated traffic confirmed the latency difference was an expected result of geographic hosting variation. If the comparison platform’s instance is hosted in a region geographically closer to the test traffic than the Launch deployment region, the additional network distance accounts for the millisecond-level differences observed.

**Resolution**

1.  Confirm the hosting region for both the Launch deployment and the comparison platform deployment.
    
2.  Run comparative load tests using a tool such as k6, simulating traffic from a location consistent with your actual user base, rather than relying on anecdotal browser testing alone.
    
3.  If a significant regional latency gap is identified, evaluate whether Launch supports deployment in a region closer to your primary user base, and request a region change through Contentstack Support if needed.
    
4.  Re-run the comparative load test after any regional adjustment to confirm response times have improved.
    

The issue is resolved when the observed latency difference is understood to be a function of geographic hosting distance, and (if applicable) the deployment region is adjusted to better match the target user base.

## Live Logs and Server Logs

### Server Logs Is Empty or Shows Fewer Logs Than Expected

The Server Logs view displays no entries, or displays fewer log entries than you expect for the selected period.

**Root Cause**

This typically occurs when the active Timeframe filter does not cover the period the logs were generated in, when the Source filter (Origin or Edge) excludes the relevant log source, when a Search filter is unintentionally narrowing the results, or when the deployment has not produced any output yet.

**Resolution**

1.  Confirm the Timeframe filter covers the period during which the entries were generated.
    
2.  Confirm at least one Source (Origin or Edge) is enabled.
    
3.  Check whether you have applied a Search filter, and remove it if it isn't needed.
    
4.  If the deployment is running, start a Live Log Capture session to confirm that the application is producing output.

### Live Logs Remain on "Waiting for live logs…" With No Entries

A Live Log Capture session starts and stays active, but the view continues to show "Waiting for live logs…" with no entries appearing.

**Root Cause**

The session itself is active and working correctly, but the application has not yet generated any output for it to display. In some cases, an active Source filter can also exclude the entries that are being produced.

**Resolution**

1.  Send a request to your deployment to trigger log generation.
    
2.  If entries still do not appear, verify the Source filter is not excluding them.

### New Entries Do Not Appear After a Refresh

New log entries do not appear in the Server Logs list after a browser or page refresh, even when recent activity is expected.

**Root Cause**

Server Logs do not auto-refresh. A browser or page refresh does not fetch new entries automatically; fetching newer entries requires an explicit in-product action.

**Resolution**

1.  Click Load new logs at the bottom of the list, or use Refresh in the toolbar, to fetch newer entries.
    
2.  For continuous, real-time updates instead of manual refreshing, use Live Log Capture.

### A Load or Refresh Returns an Error

Loading or refreshing Server Logs returns an error state instead of the expected log entries.

**Root Cause**

This is generally a transient issue and displays as a distinct error state rather than as an empty list. Persistent errors may indicate the deployment itself is no longer active.

**Resolution**

1.  Retry after a few seconds; transient errors resolve on their own in most cases.
    
2.  If the error persists, verify the deployment is still active.
    
3.  Try Live Log Capture as an alternative to loading historical Server Logs.

### Logs Older Than 24 Hours Are Needed

Server Logs limits look-back to **24 hours**. Entries older than this window are not available in-product.

**Root Cause**

The in-product Server Logs view limits look-back at **24 hours**. Launch does not retain logs older than this window.

**Resolution**

1.  Configure a Log Target to forward logs to a third-party monitoring service so the third-party service retains them beyond the **24-hour** window.
    

Refer to the [Log Targets](/docs/developers/launch/log-targets) documentation for setup details.