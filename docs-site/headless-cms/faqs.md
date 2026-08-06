---
title: "Headless CMS Troubleshooting Guides"
description: "Discover answers to common troubleshooting questions about Headless CMS."
url: "https://www.contentstack.com/docs/headless-cms-troubleshooting/faqs"
product: "Contentstack"
doc_type: "guide"
audience:
  - developers
  - admins
version: "current"
last_updated: "2026-07-27"
---

# Headless CMS Troubleshooting Guides

## Content Editing & UI Workflows

### Cannot Modify a Historical Entry Version (Versioning Behavior)

When attempting to update a previously saved version of an entry, the system does not allow direct modification of that historical version. Any changes made through the CMS UI or Content Management API result in the creation of a new latest version instead of altering the selected older version.

**Root Cause** 

Contentstack enforces immutable versioning by design.

*   Each time an entry is updated, a new version is created.
    
*   Historical versions are retained as read-only snapshots for audit and rollback purposes.
    
*   The Content Management API (CMA) and CMS UI only allow updates to the current/latest entry state.
    
*   Older versions cannot be edited directly to preserve content integrity and version history accuracy.
    

This behavior ensures traceability, audit compliance, and content recovery safety.

**Resolution**

Do not attempt to edit historical versions directly. If content from an older version is required:

*   Use the **Version History** feature in the CMS UI.
    
*   Select the required version and choose **Restore** (this creates a new latest version based on that snapshot).
    

**For API-based workflows:**

*   Retrieve the latest entry version via CMA.
    
*   Apply updates to the current version only.
    
*   Allow the system to generate the next version automatically.
    

Check the entry version number before making changes and perform an update via CMS UI or CMA.

**Confirm:**

*   A new version number is generated.
    
*   The previous historical version remains unchanged.
    
*   The updated content exists only in the new latest version.

### Entry Version Warning Showing Older Version

Warnings such as “Published before localization” or indicators of older versions appear even after publishing.

**Root Cause**

A Release stores a snapshot of specific entry versions. Publishing a newer version outside the Release does not automatically update the Release reference.

**Resolution**

1.  Open the affected Release.
2.  Update the entries to their latest versions.
3.  Deploy.

Open the Release and confirm that all referenced entries use the latest version and that the warning is no longer displayed.

### Managing Concurrent Entry Edits Without Merge Functionality

Multiple contributors working on the same entry may overwrite each other's changes because the platform does not support merging entry versions. This prevents the simultaneous consolidation of updates from different users into a single version.

**Root Cause**

The platform's versioning architecture is designed for linear tracking and does not include a native merge feature.

**Resolution**

1.  Use Workflows to manage the progression of entry edits and handoffs between users.
2.  Add Field Notes to provide context or instructions to other contributors.
3.  Coordinate with team members to ensure only one user is editing a specific entry version at a time.

After implementing a workflow-based editing process, check the version history of an entry. If updates are saved sequentially without data loss from overwrites, the coordination strategy is effective.

### Cross-section card drag-and-drop not supported in CMS UI"

Reordering card components in the CMS UI may be restricted to the section in which they are placed. This prevents moving individual cards directly from one section to another via drag-and-drop.

**Root Cause**

The current drag-and-drop functionality only supports reordering elements within a single section.

**Resolution**

1.  Move cards within their specific section using the drag handles.
2.  Reorder entire sections if the project requires moving a group of components.
3.  Refer to the product team to submit a feature enhancement request for cross-section dragging.

After attempting to drag a card within its parent section, check the vertical order. If the card moves within its section but cannot be dropped into a different section, the behavior is expected.

### Date Field Time Settings Reset During Entry Save

Saving an entry in the CMS may cause the time settings in a date field to reset or shift from the originally entered values. This prevents maintaining a fixed time independent of the user's local timezone.

**Root Cause**

The date field automatically adjusts its value to follow the current local timezone of the user performing the save operation.

**Resolution**

1.  Verify the local timezone settings of the user account performing the entry save.
2.  Ensure team members are aware that saved times reflect the local timezone of the last editor.
3.  Refer to upcoming product enhancements for improved handling of fixed timezone settings.

After entering a specific time and saving the entry, check the date field value. If the time displays an adjustment consistent with the local timezone, the behavior is operating as currently designed.

### UID Conflicts During Content Migration to a New Stack

Content migration to a new stack fails with errors indicating UID uniqueness conflicts. A content type field UID matches an existing field name, or a global field import fails due to a naming collision.

**Root Cause**

Contentstack enforces unique UIDs for fields within a content type and globally for global fields. During migration, if a field UID in the source stack conflicts with an existing field or global field UID in the target stack, the import fails. Common causes include: a content type has a field with the same UID as a global field already present in the target, or two fields within the same content type share a UID.

**Resolution**

1.  Review the migration error log to identify which UIDs are conflicting.
    
2.  Rename conflicting field UIDs in the source content type before re-exporting.
    
3.  Ensure global field UIDs are unique across the target stack before importing.
    
4.  If the UID collision is between a field and a global field, rename one to resolve the conflict and update any references accordingly.
    
5.  Re-run the migration after resolving all UID conflicts.
    

After resolving UID conflicts, re-run the import. If the migration completes without uniqueness errors, all UIDs are compatible with the target stack.

### Required Field Validation Errors When Updating Translated Entries via CMA

A translation connector or API-based workflow fails to push updated translated entries back to Contentstack. The CMA returns required field validation errors even though all required fields appear to be populated.

**Root Cause**

The validation error typically occurs because the file field value in the update payload is structured incorrectly. The translation connector may be passing the full asset object from the original Get Entry response instead of the required simplified format (asset UID only). Other required field validation errors can occur when the payload is missing field keys that are required by the content type schema.

**Resolution**

1.  Review the update payload and verify that all required fields are included with valid values.
    
2.  For file fields specifically, ensure only the asset UID is passed: { "uid": "<asset\_uid>" }
    
3.  For reference fields, ensure only the entry UID and content type are included, not the full resolved reference object.
    
4.  Test the corrected payload against a single entry before running the full translation batch.
    

After correcting the payload structure, re-run the update for a single translated entry. If it succeeds without validation errors, apply the fix to the full translation workflow.

### Entry Import vs. Create Entry API - Understanding the Overwrite Flag

The overwrite flag behavior during CMA entry import is unclear. It is uncertain whether import will overwrite existing entries or create duplicates, and how it differs from the Create Entry API.

**Root Cause**

The CMA import endpoint and the Create Entry API are distinct operations with different behaviors. The overwrite flag in the import endpoint controls whether existing entries with matching UIDs are overwritten. Without overwrite=true, importing an entry with an existing UID will either fail or create a new entry, depending on the content type's uniqueness constraints

**Resolution**

*   CMA Import endpoint: imports entries in bulk from a JSON export. Use overwrite=true in the request to replace existing entries that share the same UID. Without overwrite, duplicate entries may be created or conflicts may occur.
    
*   Create Entry API (POST /v3/content\_types/{uid}/entries): creates a new entry each time it is called, regardless of whether an entry with the same title or content already exists. It does not accept an overwrite flag.
    
*   To update an existing entry via API, use the Update Entry (PUT) endpoint with the entry's UID.
    

Choose the appropriate API based on the use case: use Import with overwrite=true for bulk migration scenarios, and use the Update Entry API for targeted entry updates.

### Field Display Name and UID Blank in Content Type - Missing field_metadata

Fields in a content type display blank names and UIDs in the CMS UI. The fields exist in the schema but their display values are not visible.

**Root Cause**

The field\_metadata property is missing from the field definitions in the content type schema. This property is required for the CMS to render field display names and other UI-level metadata. When it is absent or has invalid values, the fields appear blank in the interface.

**Resolution**

1.  Retrieve the content type schema via the CMA: GET /v3/content\_types/{content\_type\_uid}
    
2.  Identify fields where the field\_metadata key is missing or empty.
    
3.  Add the field\_metadata key with appropriate default values to each affected field. At minimum, include: { "field\_metadata": { "description": "", "default\_value": "" } }
    
4.  Update the content type schema via: PUT /v3/content\_types/{content\_type\_uid} with the corrected schema.
    
5.  Reload the CMS UI and confirm the field display names are now visible.
    

After updating the schema with the field\_metadata key, reload the content type in the CMS. If field display names are now visible, the metadata has been correctly added.

### Changing a Field Data Type - Correct Process to Avoid Data Loss

A customer wants to change an existing field's data type (for example, from Number to String). It is unclear whether this can be done directly and what the impact on existing content will be.

**Root Cause**

Directly changing a field's data type in Contentstack is not supported and will result in irreversible data loss. The existing data stored in the original field type cannot be automatically converted to the new type and will be permanently deleted.

**Resolution**

1.  Create a new field with the desired data type (for example, a new String field).
    
2.  Write a script using the CMA to fetch all entries, read the value from the original Number field, and write it to the new String field.
    
3.  Verify that all entries have been migrated correctly by spot-checking a sample of entries.
    
4.  Once migration is confirmed, deprecate the original field (optionally remove it from the UI without deleting it immediately to allow a rollback window).
    
5.  After full validation, delete the original field if it is no longer needed
    

After completing the migration script and verifying entry data, confirm that the new String field contains the expected values for all entries before removing the original field.

### Unique Title Constraint Blocks Content Migration - Disable via CMA

A content migration from a custom CMS fails because the target Contentstack content type enforces a unique title constraint. Source content contains duplicate titles that cannot be imported.

**Root Cause**

By default, the title field in Contentstack content types has unique=true, which prevents multiple entries from sharing the same title. The CMS UI does not expose an option to disable this uniqueness constraint. During migration, duplicate titles from the source system trigger validation failures.

**Resolution**

1.  Use the CMA to update the content type schema and set unique=false on the title field: PUT /v3/content\_types/{content\_type\_uid} with the updated schema where the title field has: { "unique": false }
    
2.  Re-run the migration import after applying this change.
    
3.  Optionally restore unique=true after the migration is complete if uniqueness should be enforced going forward.
    

After setting unique=false and re-running the import, confirm that entries with duplicate titles are created successfully. Restore the uniqueness constraint after migration if required.

### PUT Request Sent to Wrong Branch - Missing Branch Header

A CMA PUT request intended for a specific branch is applied to the main branch instead. The entry update appears on main rather than the intended target branch.

**Root Cause**

The CMA defaults all requests to the main branch when no branch header is included. Without explicitly specifying the branch in the request header, every CMA operation targets main, regardless of any branch context in the UI or the calling application.

**Resolution**

1.  Add the branch header to all CMA requests that should target a specific branch: branch: <branch\_uid>
    
2.  Verify the branch UID by listing available branches: GET /v3/stacks/branches
    
3.  Re-run the PUT request with the branch header included and confirm the update is applied to the correct branch.
    

After adding the branch header, execute the PUT request and verify the entry is updated in the correct branch, not in main.

### Restoring Deleted Entries via CMA Script

Entries have been accidentally deleted from a stack. The customer needs to restore them and wants to know whether deleted entries can be published after restoration.

**Root Cause**

Contentstack does not provide a native UI-based entry restoration feature. Deleted entries can be recovered by recreating them via the CMA using data from a backup or audit log. Once recreated, they are new entries and publish normally through the standard workflow.

**Resolution**

1.  Retrieve the entry data from a backup source (for example, a previously exported JSON file, a staging stack, or a source-of-truth external system).
    
2.  Use the CMA Create Entry endpoint (POST /v3/content\_types/{uid}/entries) to recreate each deleted entry with the original content.
    
3.  If the original entry UID must be preserved, include the uid field in the create payload.
    
4.  After recreating the entries, publish them through the standard publish workflow.
    

After recreating the entries and publishing them, verify they appear correctly in the target environment via the CDA.

### Bulk Editing Multiple Entries via a Single CMA Call Is Not Supported

A request is made to update multiple entries simultaneously using a single CMA API call. No documentation appears to cover bulk entry updates in one request.

**Root Cause**

Bulk editing of entry content via a single CMA call is not currently supported. The CMA's bulk operations endpoint supports bulk publish, unpublish, and delete, but not bulk content updates (changing field values across multiple entries simultaneously).

**Resolution**

1.  Fetch all required entries using the CMA GET entries endpoint (with pagination if needed).
    
2.  Modify the desired field values in the response payload for each entry.
    
3.  Loop through the entries and send a separate PUT /v3/content\_types/{uid}/entries/{entry\_uid} request for each one.
    
4.  Implement rate limiting and retry logic in the loop to stay within CMA rate limits.
    

After implementing the per-entry update loop, run it against a small batch first to confirm the updates are applied correctly before running it at full scale.

### Which Locale to Pass in the CMA Update API - Entry Locale vs. Input Parameter Locale

There is confusion about which locale value should be passed in a CMA update API call: the locale of the entry being updated, or the locale from an input parameter in the workflow. Passing the wrong locale causes unexpected behavior or errors.

**Root Cause**

The locale parameter in a CMA update request determines which locale version of the entry is being updated. Passing the wrong locale either creates or modifies the wrong locale version of the entry, or fails validation if the specified locale does not exist for that entry.

**Resolution**

1.  Always pass the locale of the specific entry version you intend to update.
    
2.  If updating the master locale version, pass the master locale code (for example, en-us).
    
3.  If updating a localized version, pass the exact locale code of that localized version (for example, fr-fr, de-de).
    
4.  Do not pass the input parameter locale from an external system unless it has been validated against the locales configured in the Contentstack stack.
    
5.  To confirm which locales exist for an entry, call: GET /v3/content\_types/{uid}/entries/{entry\_uid}/locales before updating.
    

After confirming the correct locale code and updating the request, re-run the CMA update. If the correct locale version of the entry is updated, the locale parameter is now correctly specified.

### Workflow Status Per Entry Version Not Available via API

A customer wants to retrieve the complete version history of an entry along with the workflow status for each version. No API endpoint appears to provide this combination of data.

**Root Cause**

Contentstack does not provide workflow status per individual version through the API. The API returns the current workflow stage of the entry, not a history of stages across versions. This data is not natively persisted in a queryable per-version format.

**Resolution**

The following workarounds can be used to build a workflow history:

1.  Use the Audit Log API (GET /v3/audit-logs) to retrieve workflow stage change events, which include the user, timestamp, and new stage for each change. Cross-reference with version numbers to reconstruct a workflow history.
    
2.  Configure a webhook to fire on workflow stage change events. Capture and store the payload (which includes entry UID, version, and new stage) in an external system to build a persistent per-version workflow history.
    
3.  For ongoing tracking, log workflow status at the point of each version update in the external system.
    

After setting up the webhook listener or integrating the Audit Log API, validate that workflow stage change events are correctly captured and linked to the corresponding entry version.

### Admin Users Bypass Workflow Stage Rules: Expected Behavior

An admin user is able to change an entry's workflow stage despite strict transition rules being configured that should prevent that move. The workflow constraints appear to be ignored for this user.

**Root Cause**

This is expected behavior by design. Organization owners, stack owners, and stack admins automatically bypass all workflow constraints, including stage transition rules and access restrictions. Elevated admin permissions are intentionally exempt from editorial workflow controls to ensure admins can always manage content regardless of workflow state.

**Resolution**

No fix or configuration change is available to apply workflow constraints to organization or stack admins. To manage this by design:

1.  Ensure that users who must be subject to workflow constraints are assigned standard roles (not owner or admin roles).
    
2.  Create dedicated content editor roles with the appropriate permissions that are not exempt from workflow rules.
    
3.  Document the admin bypass behavior for the team so editors understand why admins can make transitions that standard users cannot.
    

Workflow stage rules will be enforced correctly for non-admin users. Only organization owners, stack owners, and stack admins bypass these constraints.

### Management Token Cannot Change Workflow Stage When Role Restrictions Are Set

A CMA request to change a workflow stage using a management token returns an access denied error. The same operation works when using a user auth token.

**Root Cause**

Workflow stage transitions with role restrictions require the transition to be performed by a user who holds the required role. A management token is not associated with a user role — it is a stack-level credential without user identity. When role restrictions are applied to a workflow stage, the CMA validates the requester's role, and a management token cannot satisfy this check.

**Resolution**

Two options are available:

1.  Option A - Use a user auth token: Generate an auth token from a user account that holds the required role for the workflow transition. Use this auth token instead of the management token for workflow stage change requests.
    
2.  Option B - Remove role restrictions: If user identity is not required for the transition, remove the role restriction from the workflow stage configuration. This allows management tokens to perform the transition
    

After applying the chosen approach, re-run the workflow stage change request. If the transition succeeds without an access denied error, the authorization requirement is satisfied.

### 422 Error on Workflow Stage Change Endpoint - Entry Requires Initial Stage First

A CMA request to the workflow stage change endpoint returns a 422 error. The entry exists and the workflow is configured correctly, but the stage transition fails.

**Root Cause**

The /workflow endpoint can only transition an entry between workflow stages if the entry already has an initial workflow stage assigned. If the entry was created without a workflow stage (for example, programmatically via API without setting a stage), it has no current stage and the transition endpoint cannot operate on it.

**Resolution**

1.  First, assign the initial workflow stage to the entry using the Entry Update API (PUT /v3/content\_types/{uid}/entries/{entry\_uid}). Include the workflow stage in the update payload: { "entry": { "\_workflow": { "uid": "<initial\_stage\_uid>" } } }
    
2.  After the initial stage is set, use the workflow stage change endpoint to perform subsequent transitions.
    

After setting the initial stage via the Entry Update API, retry the workflow stage change endpoint. If the transition completes without a 422 error, the entry now has a valid starting stage.

### Rich Text Editor Field Behavior: Empty Default JSON vs. Null RTE Blocks

Rich Text Editor (RTE) fields can appear to return unexpected values in GraphQL responses. This section covers two distinct RTE behaviors that are commonly confused:

**Scenario A: Empty RTE Field Returns Default JSON Instead of Null**

An empty RTE field does not return null in the GraphQL response. Instead, it returns a default JSON structure even when no content has been entered. This behavior differs from plain text fields, which return null when empty.

**Root Cause**

RTE fields are initialized with a default JSON structure to ensure consistent and valid output for the front-end rendering layer. This approach maintains compatibility with rich text rendering libraries that expect a defined JSON schema even for empty content. Returning an empty JSON structure rather than null is intentional behavior to prevent rendering errors.

**Resolution**

This is expected platform behavior and cannot be changed. To handle empty RTE fields in the front-end application:

1.  Check whether the returned JSON structure represents an empty document (for example, an empty paragraph node) rather than checking for null.
    
2.  Implement a client-side utility function that evaluates the RTE JSON structure and treats it as empty when it contains no meaningful content.
    
3.  Do not rely on null checks for RTE fields; use content checks against the JSON structure instead.
    

**Scenario B: RTE Blocks Return Blank or Null Despite Content Being Present**

RTE Blocks appear blank or return null when queried via GraphQL or the Content Delivery API, even though content is visible in the CMS editor.

**Root Cause**

This can occur when the RTE field’s internal data state is stale or was not correctly committed during the last save. The CMS UI may display content that has not been fully persisted or indexed for delivery.

**Resolution**

1.  Open the affected entry in the CMS.
    
2.  Make a minor edit to the RTE field - for example, add a space or retype a character - and save the entry.
    
3.  Publish the entry to the target environment.
    
4.  Re-run the GraphQL or CDA query and confirm the RTE content is now returned correctly.
    

Use Scenario A guidance if the RTE field is intentionally empty and the application needs to detect that state. Use Scenario B guidance if the RTE field contains content in the CMS but returns blank or null in the API response.

After applying the relevant fix, query the entry again. If the RTE field returns the expected content or the empty state is correctly handled in the application, the issue is resolved.

### Entry Version History Limited to 30 Versions - Full History Not Visible

The Contentstack UI displays a maximum of 30 versions for an entry, even though the entry has been saved and updated many more times. Older versions beyond the 30-version display limit are not accessible.

**Root Cause**

A backend configuration that controls how publish statuses are displayed across entry versions was not enabled for the affected organization. When this configuration is disabled, the version history display is capped at a lower threshold, making it appear as though older versions do not exist.

**Resolution**

1.  Contact Contentstack Support and report that entry version history is limited to 30 versions. Provide the stack API key and an example entry UID.
    
2.  Engineering will enable the backend configuration to restore full version history visibility.
    
3.  After the configuration is enabled, reload the entry in the CMS UI and confirm that all versions beyond 30 are now visible.
    

After the fix, verify the full version history is accessible for the affected entry and that versions can be compared and restored as expected.

### ‘Saved By’ Shows Incorrect User in Entry Version History

The ‘Saved By’ field in an entry’s version history displays a user who is not the person expected to have made the change. Editors report seeing unexpected names or user IDs in the version history.

**Root Cause**

The ‘Saved By’ field reflects the user who saved the entry version, not the user who published it. If an entry is saved by one user and later published by another, the version history shows the saver’s identity - not the publisher’s. Additionally, automated processes (API calls, CLI operations, or automation scripts) that save entries will show their associated user identity or service account.

**Resolution**

1.  Distinguish between the saver and the publisher: ‘Saved By’ in version history = the user who saved that version; the publishing record in the audit log = the user who triggered the publish.
    
2.  To identify the user behind a specific updated\_by UID shown in version history, call the Users API: GET /v3/users/{user\_uid} (requires a management token).
    
3.  Review the Audit Log (Settings > Audit Log) for the entry to see both save and publish events with their associated users and timestamps.
    
4.  For discrepancies caused by automated processes, review which service accounts or automation configurations have write access to the affected entries.
    

After cross-referencing the updated\_by UID with the Users API, confirm the identity of the user who saved the version and whether the change was manual or automated.

### Entry Version Missing From History and Audit Log - Silent Revision Failure

A specific version of an entry (for example, version v4) is confirmed to have been published to production, but it does not appear in the version history dropdown or in the audit log. The version appears to have been deleted or never created.

**Root Cause**

Investigation confirmed the version was successfully created and published to production. However, due to a silent failure at the time of creation, the version was not recorded in the revisions collection - the internal store that powers version history and audit log display. The version existed and functioned correctly in live content. The absence from version history and audit logs is caused by the revision record never being written, not by any deletion action.

**Resolution**

1.  Contact Contentstack Support and provide the entry UID, the missing version number, and the stack API key. Engineering can inspect the revisions collection to confirm whether the version record exists.
    
2.  Do not attempt to recreate or overwrite the missing version - the live content is correct. The issue is limited to the history display layer.
    
3.  If the missing version is needed for audit or compliance purposes, Engineering can provide a backend confirmation that the version was created and published at the reported time.
    

After Engineering investigates, confirm whether the revision record can be restored to the history view, or accept the Engineering-provided confirmation as the audit record for the missing version.

### Variant Entry Data Corruption - Component Misbehavior from Modular Block Duplication

A variant entry exhibits unexpected component behavior: modular blocks convert to different types unexpectedly, data sources are reset without user action, and previously deleted items reappear within the entry. The issue is blocking a project go-live.

**Root Cause**

The corruption was caused by a bug in the duplication logic of modular blocks when applied to variant entries. The duplication process incorrectly shared or re-used block data between the base entry and the variant, causing component conversion, data source resets, and reappearance of items that had been deleted in the variant context.

**Resolution**

A platform fix was deployed to correct the modular block duplication logic for variant entries. No further action is required for stacks affected by this bug after the fix is applied.

1.  If similar symptoms appear (components converting types, deleted items reappearing, data source resets in variant entries), contact Contentstack Support immediately with the affected variant UID, entry UID, and stack API key.
    
2.  Do not attempt to manually re-delete the reappearing items or re-configure components - this may compound the data state.
    
3.  After the fix is confirmed, re-verify the variant entry content to ensure all components are in their expected state and no data corruption remains.
    

After the platform fix, open the affected variant entry and confirm that components display correctly, deleted items do not reappear, and data sources are stable.

### Unique Validation Not Enforced Inside Multiple Group Fields

A Group field marked as Multiple has fields inside it (such as key and value) with the Unique property enabled. Despite the unique constraint, duplicate key/value pairs can still be saved within the same entry.

**Root Cause**

The Unique validation for fields within a Multiple Group operates at the entry level, not at the group-item level. This means Contentstack checks whether the value is unique across all entries in the content type - it does not check whether the value appears more than once within the multiple group instances inside a single entry. Duplicate items within the same entry’s group instances are therefore permitted by design.

**Resolution**

Native uniqueness enforcement within a Multiple Group’s items is not supported. Alternatives:

1.  Implement client-side validation in the editorial workflow or a UI extension that checks for duplicate items within the group before saving.
    
2.  Use a custom App SDK extension on the field to perform real-time duplicate detection within the group instances as editors add items.
    
3.  If unique group items are a strict business requirement, consider restructuring the data model: use a JSON custom field or a modular block where the uniqueness can be enforced programmatically via a webhook or automation.
    

After implementing the client-side or extension-based validation, confirm that editors receive a clear message when attempting to save duplicate group items.

### Restoring Accidentally Deleted Entries and Taxonomy Terms

A large number of entries or taxonomy terms were accidentally deleted - for example, by a misconfigured integration script - and need to be restored. The affected content is now missing from the CMS.

**Root Cause**

When entries or taxonomy terms are deleted, they are moved to the Trash (Bin) and retained for a platform-defined retention period before permanent deletion. During this window, they can be restored programmatically.

**Resolution**

**Restoring deleted entries from Trash:**

1.  Retrieve deleted entries from the Bin: GET https://app.contentstack.com/#!/stacks/{stack\_api\_key}/recycle-bin (UI) or via the CMA: GET /v3/trash (Management API Trash endpoint).
    
2.  Restore individual entries: POST /v3/trash/{entry\_uid}/restore.
    
3.  For bulk restoration of many entries, use the Trash API in a script: fetch all deleted entry UIDs and iterate with restore calls.
    

**Restoring accidentally removed taxonomy terms:**

1.  If terms were removed from entries (not the taxonomy itself deleted), use the CMA to re-add taxonomy terms to affected entries: PUT /v3/content\_types/{uid}/entries/{entry\_uid} with the corrected taxonomy data.
    
2.  If terms were deleted from the taxonomy, contact Contentstack Support - taxonomy term deletion may require backend restoration if the terms are no longer in the Trash.
    
3.  For large-scale restorations (600+ entries), contact Contentstack Support and provide the list of affected entry UIDs and the Stack API key. Engineering can assist with bulk restoration.
    

After restoration, verify a sample of entries are correctly restored and contain the expected data.

Important: Contentstack does not provide a bulk rollback endpoint for restoring multiple deleted entries in a single API call. Each entry must be restored individually using: PUT /v3/content\_types/{content\_type\_uid}/entries/{entry\_uid}/restore?deleted=true with the entry locale in the request body. For large-scale restorations, script this call iteratively across all affected entry UIDs rather than expecting a single bulk operation.

### Bulk JSON Import via UI Creates ‘Untitled’ Entries Without Populating Fields

Attempting a bulk entry import through the Contentstack UI using a JSON file results in entries being created as ‘Untitled’ with no fields populated. The import appears to succeed but the entries are empty.

**Root Cause**

The Contentstack UI does not support bulk entry creation via JSON import. The UI import function is designed for configuration data (content types, global fields, etc.), not for populating entry fields from JSON. When a JSON entry structure is uploaded through the UI import, it creates shell entries without mapping the JSON fields to entry field values.

**Resolution**

1.  Use the Contentstack CLI for bulk entry import: cs cm:stacks:import --stack-api-key {key} --data-dir {path} - this correctly maps JSON data to entry fields.
    
2.  Alternatively, use the CMA to create entries programmatically: POST /v3/content\_types/{uid}/entries with the entry data in the request body.
    
3.  Delete the ‘Untitled’ entries created by the failed UI import before running the CLI or CMA import to avoid duplicates.
    

After importing via CLI or CMA, verify that a sample of entries contain the expected field values and can be published successfully.

### Workflows Disabled After CLI Import/Export Between Branches

Workflows are intermittently disabled with an error stating ‘no content type selected’, even though content types were previously assigned to the workflow. The issue occurs specifically after CLI import/export operations used to migrate data between branches.

**Root Cause**

During CLI import operations, content type UIDs in the workflow configuration can become detached if the UIDs differ between the source and target branches. The CLI import restores the workflow schema but does not re-bind the content type references when the UIDs are mismatched or the content types do not yet exist in the target branch at import time. The workflow is created but its content type associations are empty.

**Resolution**

1.  After a CLI import, navigate to Settings > Workflows in the target branch and open each workflow.
    
2.  Re-add the required content types to each workflow stage that shows ‘no content type selected’.
    
3.  Save the workflow configuration.
    
4.  To prevent recurrence, import content types before workflows in the CLI import sequence, ensuring content type UIDs exist in the target branch before the workflow configuration references them.
    
5.  If using automated CLI migrations, add a post-import verification step that checks workflow configurations and re-applies content type assignments if they are missing.
    

After re-adding content types to the workflow configuration, verify that workflow stage transitions function correctly and editorial users are assigned to the correct stages.

### Prevent Self-Approval’ Setting Not Working

The ‘Prevent self-approval’ setting is configured on a publish rule, but users with direct publish permission to production can still publish entries without going through an approval step. The self-approval prevention appears to have no effect.

**Root Cause**

The ‘Prevent self-approval’ setting only applies when an approval step is enforced by the workflow. If the workflow does not have a stage that requires approval before the publish rule is triggered, there is nothing to prevent self-approval of - the user is publishing directly, not approving their own request. The setting is irrelevant when no approval step exists in the publishing flow.

**Resolution**

1.  Review the workflow configuration. Confirm whether a stage is configured that requires approval before publishing to the target environment.
    
2.  If no approval stage exists, add one: create a workflow stage (for example, ‘Pending Approval’) that must be completed before content can be published to production. Assign approvers to this stage.
    
3.  Enable ‘Prevent self-approval’ on the publish rule in conjunction with the approval stage. This prevents the original author from approving their own content at that stage.
    
4.  Assign the approval permission to a different user or role from the one that originally creates or edits entries.
    

After adding an approval stage and re-enabling ‘Prevent self-approval’, verify that authors cannot approve their own publish requests and must wait for a designated approver.

### Disabling a Publish Rule - Behavior and Scope

An administrator wants to temporarily disable a publish rule without deleting it. They cannot find a disabled toggle - only a delete option is visible. They also need to confirm whether the publish rule applies to all environments or only the specified one.

**Root Cause**

Publish rules in Contentstack do not have a standalone enable/disable toggle separate from deletion. The way to disable a publish rule is to disable the workflow it is associated with. When a workflow is disabled, all publish rules tied to that workflow are also disabled. Additionally, publish rules are scoped per environment: a rule configured for the ‘Live’ environment applies only to that environment, leaving all other environments (such as staging) unaffected.

**Resolution**

1.  To disable a publish rule without deleting it: navigate to Settings > Workflows, open the workflow the publish rule is associated with, and disable the workflow using the toggle. This disables the workflow and all its publish rules.
    
2.  To re-enable, toggle the workflow back on.
    
3.  Regarding environment scope: if a publish rule specifies ‘Live’ as the environment, users can still publish to all other environments (staging, dev, etc.) without restriction. The rule only enforces its conditions when publishing to ‘Live’.
    

After disabling the workflow, confirm that users can publish freely to non-production environments and that the production-environment restrictions no longer apply.

### Bulk Publish and Unpublish Failing With ‘Invalid Entry’ Error

Bulk publish and unpublish operations fail with an ‘Invalid entry’ error, despite the entries being valid when published individually. The bulk job log shows ‘Untitled’ entries in the failure list. Individually publishing the same entries succeeds.

**Root Cause**

This was a platform-level bug in the new publishing flow. The bulk publish/unpublish path was failing to correctly resolve entry versions during the validation step, causing valid entries to be flagged as invalid. The ‘Untitled’ display in the job log was a consequence of the entry resolution failure, not an indication that the entries were actually untitled or invalid.

**Resolution**

A platform fix has been deployed. No configuration change is required.

1.  After the fix deployment, retry the bulk publish or unpublish operation that was previously failing.
    
2.  If the ‘Invalid entry’ error persists after the fix is confirmed deployed, contact Contentstack Support with the affected entry UIDs, the stack API key, and the bulk job ID from the failed operation.
    

After the fix, confirm that bulk publish and unpublish operations complete successfully for the previously failing entries.

### Auto Draft Feature Causing Unexpected Draft Creation on Entry Open

After enabling the Auto Draft (Auto-Save) Early Access feature, drafts are automatically created whenever any editor opens an entry, even without making changes. This disrupts the editorial workflow and is causing unexpected publish issues in the newsroom.

**Root Cause**

The Auto Draft Early Access feature creates a draft automatically when an entry is opened for editing. In some configurations or with certain workflow setups, this behavior was overly aggressive - creating drafts even for read-only views or in environments where the feature’s interaction with existing publish flows was not yet fully validated.

**Resolution**

1.  Disable the Auto Draft feature to restore normal workflow behavior: navigate to Settings > Early Access Features and toggle Auto Draft off.
    
2.  After disabling, confirm that opening an entry no longer creates an automatic draft.
    
3.  Before re-enabling Auto Draft in future, test it on a non-production stack to validate its interaction with existing workflows and publish rules.
    
4.  Contact Contentstack Support to report the specific disruptive behavior observed - this feedback helps improve the feature before general release.
    

After disabling Auto Draft, verify that editors can open entries without triggering unexpected drafts and that the publishing workflow returns to normal.

### Searching Entries for Exact http:// URLs - Using CMA Regex Query

An administrator needs to find all entries containing http:// links (as opposed to https://) for a security or migration audit. The CMS UI search returns both http:// and https:// results because it does not support exact protocol matching.

**Root Cause**

The Contentstack UI search does not support exact-match queries for URL protocol prefixes. The UI’s text search treats http and https as similar strings. Precise pattern-based searching requires the CMA with a $regex query operator.

**Resolution**

1.  Use the CMA with a $regex query to find entries containing http:// (without the ‘s’):
    
2.  GET /v3/content\_types/{uid}/entries?query={“field\_uid”:{“$regex”:“^http://”}}
    
3.  For a broader search across all text/URL fields, run the regex query per content type and per field UID.
    
4.  Use a management token for these CMA requests. Dedicated management tokens scoped to read-only operations are recommended for audit queries.
    
5.  Collect the matching entry UIDs and update them programmatically using the CMA PUT endpoint to replace http:// with https://.
    

After running the regex query, verify the result set contains only entries with http:// (not https://) and confirm the update script correctly replaces the protocol prefix in all affected entries.

### WYSIWYG HTML Mismatch Between CMS UI and Delivery API Response

The HTML content in a WYSIWYG field displayed in the Contentstack UI does not match the HTML returned by the Delivery API, even though the entry is at the same version. The mismatch occurs consistently on a specific entry and environment.

**Root Cause**

This is a data desync issue at the platform level where the HTML content stored for delivery is out of sync with the content stored for the CMS UI rendering layer. This can occur due to a data processing anomaly during a save or publish operation. The fix requires a platform-level data repair.

**Resolution**

1.  Re-save the affected entry (without content changes) to trigger a re-write of the delivery data.
    
2.  Re-publish the entry to propagate the corrected content to the delivery layer.
    
3.  Fetch the entry via the CDA and confirm the HTML now matches the CMS UI representation.
    
4.  If the mismatch persists after re-saving and re-publishing, contact Contentstack Support with the entry UID, environment, and stack details for a platform-level data repair.
    

After re-saving and re-publishing the entry, verify the WYSIWYG HTML in the CDA response matches the content visible in the CMS UI.

### ‘Something Went Wrong’ Error When Accessing the Dashboard or Entries

Users encounter a ‘Something went wrong’ error when navigating to the Contentstack dashboard, the entry list, or individual entries. Other users on the same stack may not be affected.

**Root Cause**

This error is typically caused by one of the following: a stale browser session, corrupted local cache or cookies, or a desynchronized user permission state in the authorization cache. In some cases it is triggered by a recent platform deployment that a specific browser session has not refreshed.

**Resolution**

1.  Clear browser cache and cookies and reload the page.
    
2.  Open Contentstack in a new incognito or private browsing window.
    
3.  If the error persists for a specific user, ask the Organization Owner to remove the user from the organization and re-add them. This re-syncs their permission state.
    
4.  If the error appears after a platform deployment, Engineering may need to revert the release. Contact Contentstack Support with the stack details and timestamps.
    

After clearing cache or re-adding the user, navigate to the affected page. If it loads correctly, the session or permission state has been refreshed.

### All Contentstack UI Pages Fail to Load - Browser-Specific Issue

All Contentstack UI pages - entries, assets, and content models - fail to load for a specific user. The issue persists in incognito mode and after clearing the cache, but only in one browser.

**Root Cause**

A browser incompatibility, corrupted browser installation, or conflicting browser extension is preventing the Contentstack UI from rendering. This is not a platform issue when it affects only one browser.

**Resolution**

1.  Test the same URL in a different browser (for example, switch from Chrome to Firefox or Edge).
    
2.  If the alternative browser works, the issue is isolated to the original browser.
    
3.  Update or reinstall the problematic browser.
    
4.  Disable browser extensions one by one to identify if an extension is causing the conflict.
    

After switching browsers or reinstalling, confirm that all UI pages load correctly.

### Dashboard Not Loading and Entries Cannot Be Opened

A user can see the entry list but cannot open any individual entry. Clicking an entry shows the ‘Something went wrong’ error. The dashboard also fails to load for the same user.

**Root Cause**

The user’s authorization state has become stale or desynchronized, typically due to a Redis cache issue in the authorization layer. This can occur after role changes, SSO sync events, or organization permission updates.

**Resolution**

1.  Ask the Organization Owner or Admin to switch the user’s organization role from Member to Admin and back to Member (or the reverse if they are currently an Admin). This forces a permission re-sync.
    
2.  Alternatively, remove the user from the organization entirely and re-add them with the correct role.
    
3.  After the role change, ask the user to log out, clear their browser cache, and log back in.
    

After the role toggle or re-add, confirm the user can access the dashboard and open entries without errors.

### UI Not Responsive or Broken After a Platform Deployment

The Contentstack UI becomes unresponsive, shows visual glitches, or fails to load pages for some users immediately after a platform update or deployment. Other users may be unaffected.

**Root Cause**

A cached version of the previous JavaScript bundle is being served from the browser cache after a UI revamp or feature flag rollout. The old cached scripts conflict with the newly deployed code, causing rendering failures for users whose browsers cached the previous version.

**Resolution**

1.  Ask affected users to perform a hard refresh (Ctrl+Shift+R on Windows, Cmd+Shift+R on Mac) or clear browser cache and reload.
    
2.  Alternatively, open Contentstack in an incognito window, which bypasses the cache.
    
3.  If clearing cache does not resolve the issue and multiple users are affected, contact Contentstack Support. Engineering may need to revert the deployment.
    

After clearing cache or switching to incognito, confirm the UI loads and functions as expected.

### Entries Not Visible When Switching to a Branch - UI Cache Issue

When navigating to a specific branch in the entry list, no entries are visible even though the branch contains content. Refreshing the page does not help. Switching to another branch and back resolves the display temporarily.

**Root Cause**

This is a UI-level caching inconsistency. The entry list view retains a stale cache from a previous branch session. No data loss has occurred - the entries exist and are accessible via the API.

**Resolution**

1.  Navigate away from the empty branch view to another branch or stack.
    
2.  Return to the original branch and verify entries now appear.
    
3.  If the issue persists, clear the browser cache and reload.
    

After navigating away and returning, confirm that entries in the branch are now visible in the list view.

### HTML Comments in HTML RTE Not Persisting

HTML comments added in the HTML RTE mode disappear when the entry is saved. The expected behavior of commenting out code using <!– --> syntax does not work.

**Root Cause**

HTML commenting within the RTE has never been an officially supported feature. The RTE processes and sanitizes HTML on save, removing markup that does not conform to its supported element set. HTML comment syntax (<!– -->) falls outside the supported markup and is stripped.

**Resolution**

This is expected platform behavior. To store developer notes or conditionally toggle content:

1.  Use a separate text field in the content type specifically for internal notes.
    
2.  For conditional content toggling, use field visibility rules or separate fields rather than HTML comments.
    

HTML comments cannot be reliably stored in the RTE. Use alternate content type fields for notes or metadata.

### Embedding Objects and Assets in HTML RTE

The HTML RTE does not appear to support embedding entries or assets directly from the editor, while the JSON RTE supports this functionality. Customers assume the HTML RTE cannot embed objects.

**Root Cause**

The HTML RTE does support embedding objects, but the feature must be explicitly enabled. It is disabled by default and requires activation through the RTE’s Advanced Settings.

**Resolution**

1.  Open the content type in the Content Type Builder.
    
2.  Click on the HTML RTE field to open its properties.
    
3.  Navigate to Advanced Settings > Custom and enable the Embed toggle.
    
4.  Save the content type. Editors can now embed entries and assets directly within the HTML RTE.
    

After enabling the Embed toggle, open an entry and confirm the embed option is available in the HTML RTE toolbar.

### JSON RTE Embed Entries Not Appearing - Content Type Requires URL Field

When attempting to embed an entry link in the JSON RTE, no entries appear in the selection dialog. The content types exist but their entries cannot be selected for embedding.

**Root Cause**

For a content type’s entries to be selectable for embedding as links in the JSON RTE, the content type must include a URL field. Without a URL field, the JSON RTE cannot determine where the embedded entry links to and excludes those entries from the embed selection.

**Resolution**

1.  Open the content type whose entries should be embeddable in the Content Type Builder.
    
2.  Add a URL field to the content type.
    
3.  Save the content type.
    
4.  Reload the JSON RTE entry and attempt to embed a link again - entries from the updated content type should now appear.
    

After adding the URL field to the content type, confirm the entries appear as selectable options in the JSON RTE embed link dialog.

### RTE Always Wraps Content in <p> Tags - Expected Behavior

All content entered in the RTE is wrapped in <p> tags in the API response, even for single-line text. This causes issues with frontend rendering code that does not expect paragraph wrappers.

**Root Cause**

The RTE enforces <p> tag wrapping to ensure HTML standards compliance. Block-level elements must be wrapped in appropriate container tags for valid HTML structure. This is intentional behavior.

**Resolution**

Two approaches are available:

1.  Strip <p> tags programmatically on the frontend before rendering, using a utility function that removes the wrapping tags.
    
2.  Switch to the JSON RTE for the affected field, which provides a structured JSON output that gives the frontend full control over rendering, including the ability to render content without enforced paragraph wrappers.
    

Choose based on whether the use case benefits from structured JSON (use JSON RTE) or needs the simplest possible fix (strip tags on frontend).

### Custom Font Sizes in the Rich Text Editor

Editors want to apply custom font sizes in the RTE beyond the default heading and paragraph options. No font size control appears in the editor toolbar.

**Root Cause**

The standard RTE does not include a font size selector by default. Custom font sizes are available through the Fonts Marketplace app.

**Resolution**

1.  Navigate to the Contentstack Marketplace and install the Fonts app.
    
2.  Configure the Fonts app with the desired font sizes and attach it to the relevant stacks.
    
3.  Once configured, the font size controls become available within the RTE for editors.
    

After installing and configuring the Fonts app, confirm that font size options appear in the RTE toolbar.

### <style> Tags Being Stripped from RTE Content

CSS inside <style> tags entered in the RTE is removed when the entry is saved. The same workflow works in another stack, suggesting an inconsistency in configuration.

**Root Cause**

The RTE strips <style> tags by default as part of HTML sanitization. The other stack where this works has the sys\_rte\_allowed\_tags stack variable configured to explicitly allow style tags. Without this configuration, <style> tags are removed on save.

**Resolution**

1.  Use the CMA to update the stack settings and allow style tags:
    
2.  PUT /v3/stacks with body: { “stack”: { “stack\_variables”: { “sys\_rte\_allowed\_tags”: “style,script,figure” } } }
    
3.  Verify the setting is applied by calling GET /v3/stacks and checking the stack\_variables in the response.
    

After updating the stack settings, enter CSS in <style> tags in the RTE and save the entry. Confirm the styles are preserved in the saved entry content.

### Bulk Search for Hyperlink Href Values in JSON RTE Not Working

Using the Bulk Operations search to find and replace hyperlink href values within JSON RTE content does not return results. Plain text searches work correctly.

**Root Cause**

The Bulk Operations search and replace function operates on the visible field values - the text displayed within the RTE. It does not search through internal structured data such as hyperlink URL attributes within the JSON RTE’s data model. Hyperlink URLs are stored as internal reference fields, not as plain text values.

**Resolution**

This is expected behavior based on the JSON RTE data architecture. For bulk hyperlink URL updates:

1.  Use the CMA to fetch entries and parse the JSON RTE structure programmatically.
    
2.  Identify and update the href values within the JSON structure using a script.
    
3.  Update the entries via the CMA update endpoint with the corrected JSON RTE content.
    

After scripting the JSON RTE update, verify the hyperlink URLs are correctly replaced in the affected entries by fetching them via the CDA.

### Table Formatting Inconsistent Across Environments

Tables that appear correctly inside the Contentstack editor display with different sizes or lose dimension attributes when rendered in a testing or production environment.

**Root Cause**

Table dimension attributes may be stripped or inconsistently preserved depending on the HTML structure used. Non-standard or incomplete table markup can result in attributes being dropped during HTML processing.

**Resolution**

1.  Use a recommended HTML table structure that includes explicit width attributes and proper <table>, <colgroup>, <tr>, <th>, and <td> elements.
    
2.  Avoid using inline style properties for dimensions; use width and height attributes directly on the table elements.
    
3.  Apply the corrected structure to the affected entries and republish.
    

After updating the table markup to follow the recommended structure, verify that table dimensions are consistent between the CMS editor and the rendered frontend environment.

### Migrating HTML Code View Content to JSON RTE

A customer uses raw HTML in the HTML RTE’s Code View mode and needs to migrate this content to the JSON RTE. The JSON RTE does not have a Code View equivalent.

**Root Cause**

The JSON RTE is built on a structured JSON architecture and cannot support raw HTML editing. Code View in the HTML RTE allows arbitrary HTML that does not map directly to the JSON RTE’s node-based structure.

**Resolution**

1.  For storing HTML code snippets or widgets, use a Custom Block in the JSON RTE, which allows embedding structured custom elements.
    
2.  For small inline HTML fragments, use Inline Custom Elements within the JSON RTE.
    
3.  For bulk migration of HTML RTE content to JSON RTE, use a programmatic approach: fetch entries via the CMA, convert HTML to JSON RTE structure using the @contentstack/json-rte-serializer library, and update entries via the CMA.
    
4.  For complex HTML that cannot be converted, consider keeping the HTML RTE for that content type rather than forcing migration to JSON RTE.
    

After selecting the appropriate migration approach, verify that the migrated content renders correctly in the frontend using the JSON RTE output.

### Default Dropdown Values Not Applied to Existing Entries

After updating a content type to add default values to dropdown fields, the defaults do not populate in existing entries. Only new entries receive the default values.

**Root Cause**

Default field values in Contentstack are applied only to entries created after the defaults are configured. Existing entries already have a saved state and are not retroactively updated with new default values when the content type is modified.

**Resolution**

This is expected behavior. For existing entries:

1.  Use a CMA script to fetch all existing entries that are missing the default value, set the field value programmatically, and update the entries via the CMA.
    
2.  Alternatively, manually open each affected entry and save it - if the field is blank, the default will populate on save.
    

After applying the default values to existing entries (programmatically or manually), verify that all entries contain the expected default field values.

### Global Fields Cannot Reference Another Global Field

A customer wants to create a structure where a Global Field references another Global Field (for example, a FeaturedCard global field referencing a MediaAsset global field). The relationship cannot be established.

**Root Cause**

Global Fields in Contentstack do not support direct references to other Global Fields. A Global Field can only be referenced from within a Content Type or as a block within a Modular Block - not by another Global Field.

**Resolution**

The following workarounds are available:

1.  Convert the referenced global field into a regular Content Type. Entries of that content type can then be referenced from within the parent Global Field using a Reference field.
    
2.  Replicate the fields from the nested global field directly into the parent Global Field if the structure is simple enough.
    
3.  Create a connector Content Type that brings together the fields from both global structures, used wherever the combined structure is needed.
    

After restructuring using one of the above approaches, verify the content type schema works as expected and entries can be created with the correct field relationships.

### Global Field Cannot Be Added Inside a Modular Block

A customer wants to add a Global Field inside a Modular Block but is unable to do so in the content type editor.

**Root Cause**

Global Fields in Contentstack can only be added as standalone blocks within a Modular Block - they cannot be nested inside another block type within the Modular Block. The Global Field appears as its own full block in the Modular Block structure, not as a nested sub-field.

**Resolution**

1.  Add the Global Field as a standalone block directly in the Modular Block configuration - do not attempt to nest it inside another block.
    
2.  If deeper nesting is required, use a Reference Content Type approach: create the nested structure as a regular content type and reference it from within the Modular Block.
    

After adding the Global Field as a standalone block in the Modular Block, verify editors can select and populate it in entries.

### Non-Localized Fields Cannot Be Configured Inside a Non-Localized Modular Block

After setting a modular block to non-localized, the option to mark individual fields inside the block as non-localizable disappears. This is unexpected behavior.

**Root Cause**

This is expected behavior by design. When a modular block is configured as non-localized, all fields within it automatically inherit the non-localized status. Setting individual fields within the block as non-localizable is therefore redundant - it is implied by the block-level configuration. The UI removes the per-field option to reflect this inherited state.

**Resolution**

No action is required. All fields within a non-localized modular block are automatically non-localized. If specific fields within the block need to be localizable while others are not, the modular block itself should not be set to non-localized - instead, configure non-localizable at the individual field level.

### Taxonomy Fields Cannot Be Added to Global Fields or Inside Components

A customer receives an error or finds no option when trying to add a Taxonomy field inside a Global Field or a Modular Block component. Taxonomy fields can only be added at the top level of a content type.

**Root Cause**

Taxonomy fields are designed to be top-level fields within a content type by platform architecture. Nesting taxonomy fields inside Global Fields or Modular Blocks is not currently supported.

**Resolution**

Two workarounds are available:

1.  Reference-based workaround: Create a custom ‘Taxonomy Node’ content type that has a Taxonomy field at the top level. Add a Reference field inside the Global Field or Modular Block that references this Taxonomy Node content type. Editors select taxonomy terms through referenced entries.
    
2.  Select field workaround: For simpler, flat taxonomies, replace the Taxonomy field with a Select field containing the taxonomy values as options. This is suitable for small, static term sets that don’t require hierarchical querying.
    

After implementing the chosen workaround, verified editors can assign taxonomy-like values within the Global Field or Modular Block.

### Content Type Count on Dashboard Does Not Match Main Branch

The Content Type count displayed on the Stack dashboard does not match the number of content types visible when navigating to the main branch.

**Root Cause**

The Stack dashboard displays the total count of content types across all branches in the stack, not just the main branch. If additional branches contain extra content types that do not exist in main, the dashboard total will be higher than the main branch count.

**Resolution**

This is expected behavior. To see the content type count for a specific branch, navigate to that branch directly and view the content types from within that branch context. No corrective action is needed.

### Publish Error When Entry Has More Than 20 Modular Blocks

Publishing entries containing more than 20 modular blocks fails with a generic error (genericError.maxInstance). Entries with 20 or fewer blocks publish successfully.

**Root Cause**

A backend configuration limit key controls the maximum number of modular block instances allowed per entry. When this key is set to a threshold below the actual number of blocks in the entry, publishing is blocked. This is a stack-level backend configuration, not a UI-accessible setting.

**Resolution**

1.  Contact Contentstack Support and report the error along with the stack API key.
    
2.  Request that Engineering review and re-enable or increase the modular block maximum threshold for the affected stack.
    
3.  After the backend fix is applied, retry publishing the affected entries.
    

After engineering applies the configuration fix, attempt to publish entries with more than 20 modular blocks and confirm they publish without the genericError.maxInstance error.

### Modifying a Field UID Causes Data Loss

A customer asks whether it is safe to rename a field UID after content has been created. They want to restructure their content model without losing existing data.

**Root Cause**

Renaming a field UID in Contentstack is not recommended and will result in data loss. Entries store field values keyed by the field UID. When a UID is changed, the entry data stored under the old UID becomes inaccessible - it is not automatically migrated to the new UID. The field will appear empty for all existing entries.

**Resolution**

1.  Do not rename field UIDs on content types that contain existing entry data.
    
2.  If renaming is necessary, use the safe migration approach: create a new field with the desired UID, migrate data from the old field to the new field using a CMA script, verify the migration, and then delete the old field.
    
3.  For new content types with no data, UIDs can be renamed freely before any entries are created.
    

If a UID rename has already been performed and data is missing, recreate the field with the original UID - if the original data was not overwritten, it may still be retrievable under the original UID.

### Reference Field Cannot Have a Maximum Entry Limit Configured

A customer tries to set a maximum entry limit on a Reference field to restrict how many entries editors can select. The option does not appear to be available for Reference fields, though documentation suggests it should be.

**Root Cause**

Setting a maximum value limit on Reference fields is a known limitation currently tracked internally (JIRA UE-4241). While this feature is available for other field types, it has not been implemented for Reference fields. The documentation reference is inaccurate.

**Resolution**

At this time, maximum entry limits cannot be configured for Reference fields. As a workaround:

1.  Use a Modular Block instead of a Reference field if maximum instances need to be enforced - Modular Blocks support minimum and maximum instance settings.
    
2.  Implement frontend validation to restrict the number of selected references if the UI constraint is not available.
    
3.  Contact Contentstack Support to register interest in this feature so it can be prioritized in future releases.

### Deleted or Renamed Global Field Data Persists in Entries - Schema Refresh Required

After deleting a field from a global field or renaming it, the old field data continues to appear in existing entries. Alternatively, adding a new global field to a content type fails with a ‘reference doesn’t exist’ error, or the content type cannot be saved after a global field change.

**Root Cause**

When a global field is modified - by deleting a field, renaming a field, or changing referenced content types - the change is not automatically propagated to all content types or entries that reference that global field. The schema reference cache becomes stale. This causes entries to retain old field data and content types to fail validation against the outdated schema.

**Resolution**

1.  Navigate to the affected Global Field in the CMS (Settings > Global Fields).
    
2.  Open the Global Field and save it - even without making any visible changes. This triggers a schema refresh that propagates the current field structure to all referencing content types.
    
3.  If a content type shows a ‘reference doesn’t exist’ error, open the Global Field, remove the stale reference, and re-save. Then re-add the Global Field to the content type.
    
4.  For entries that still show old deleted field data, re-save the affected entries to force schema revalidation.
    

After re-saving the Global Field and affected entries, confirm the old field data is no longer returned in the API response and the content type saves without reference errors.

### Only One Taxonomy Field Allowed Per Content Type

A customer asks whether it is possible to add more than one taxonomy field to a single content type. They want to classify entries using multiple independent taxonomy structures (for example, one for Topic and one for Region).

**Root Cause**

Contentstack currently supports only one taxonomy field per content type. The taxonomy field is treated similarly to the Tags or URL field - it is a classification field with a single instance limit per content type. This is a current platform constraint.

**Resolution**

As a workaround:

1.  Use taxonomy\_uid within the single taxonomy field to differentiate between multiple taxonomy structures. The field can contain terms from multiple taxonomies, distinguished by their taxonomy\_uid in the API response.
    
2.  Alternatively, use a Reference field pointing to a dedicated ‘Tag Node’ content type for additional classification axes where strict taxonomy tree behavior is not required.
    
3.  Contact Contentstack Support to submit an enhancement request for multiple taxonomy field support per content type.
    

After implementing the workaround, verify that entries can be classified across multiple taxonomies using the single taxonomy field with multiple taxonomy\_uid values.

### Field Visibility Rule ‘Any’ Condition Behaving as ‘All’ - Engineering Fix Applied

Field Visibility Rules configured with the ‘Any’ condition type are not working as expected. Fields remain hidden even when one of the conditions is satisfied. The system treats all conditions as mandatory instead of requiring only one.

**Root Cause**

This was a confirmed platform bug where the FVR logic evaluation incorrectly applied AND logic for the ‘Any’ rule type instead of OR logic. Rules configured with ‘Any’ should show a field when at least one condition is met; instead, all conditions had to be satisfied simultaneously.

**Resolution**

Engineering has applied a fix restoring correct logic - ‘Any’ now applies OR and ‘All’ applies AND. No configuration change is required.

1.  If rules still behave incorrectly after the fix, delete the existing FVR configuration and re-add it to force a schema refresh.
    
2.  To re-add: navigate to the field settings, remove the current FVR configuration, save, then re-add with the correct conditions.
    
3.  If the issue persists, contact Contentstack Support with the content type UID and field UID.
    

After re-adding the rules, confirm that a field becomes visible when any one condition is met, and remains hidden only when none of the conditions are satisfied.

### Field Visibility Rules Not Working When Parent Field Has Multiple = true

Field visibility rules work correctly when a Group or Global Field’s Multiple setting is false, but stop functioning when Multiple is set to true. Conditional field display does not apply regardless of rule configuration.

**Root Cause**

This is a known platform limitation. The FVR engine supports sub-field references within Group or Global Fields only when the parent field is not marked as Multiple. When Multiple = true, the engine cannot evaluate conditions across multiple instances, so rules do not apply.

**Resolution**

1.  Set Multiple to false on the parent field if the multiple-instance requirement can be relaxed.
    
2.  Alternatively, expose all sub-fields without conditional visibility and use clear field labels or help text to guide editors on which fields apply in each scenario.
    
3.  Submit an enhancement request through Contentstack Support to extend FVR support to Multiple parent fields.
    

This is a documented platform limitation. No workaround currently enables FVR inside a Multiple Group or Multiple Global Field.

### Unable to Delete or Modify Empty Field Visibility Rules

Field visibility rules created without conditions (empty rules) cannot be deleted or modified in the content type editor. The empty rule blocks further content type saves.

**Root Cause**

Empty rules - created without condition values - can become locked in the schema if the editor was closed before the rule was completed or if the rule was partially saved. The UI may not expose a delete action for empty rules in certain states.

**Resolution**

1.  Export the content type schema via the CMA: GET /v3/content\_types/{content\_type\_uid}
    
2.  Locate and remove the empty rule entry from the field visibility configuration in the JSON.
    
3.  Update the content type via the CMA with the cleaned schema: PUT /v3/content\_types/{content\_type\_uid}
    
4.  Reload the content type in the CMS UI and confirm the empty rule no longer appears.
    

After updating the schema via CMA, open the content type and confirm field visibility rules can now be modified and saved without errors.

### Field Visibility Rules Are Not Supported Inside Global Fields

A customer wants to conditionally show or hide fields within a Global Field based on a dropdown selection inside the same Global Field. Field visibility rules cannot be applied within Global Field structures.

**Root Cause**

Field Visibility Rules are not supported within Global Fields. The FVR engine applies at the content type level, not within the reusable Global Field structure. This is a current platform limitation.

**Resolution**

1.  Expose all fields without visibility rules and use field labels or help text to guide editors on which fields to populate per scenario.
    
2.  Replace the Global Field with a dedicated content type containing the conditional fields. Content types support FVR fully, allowing conditional display based on selections within the same entry.
    

After implementing the workaround, confirm editors can identify which fields to use in each scenario through guidance text or through FVR applied at content type level.

### Taxonomy API Response Does Not Include Parent/Child Hierarchy

When fetching entries that have a Taxonomy field, the API response contains only the taxonomy\_uid and term\_uid - not the full parent/child hierarchy. Displaying the taxonomy path (for example, Battery > Battery Charging) requires additional lookups.

**Root Cause**

Entry-level API responses return taxonomy data as flat UID references by design. The full hierarchical path is not embedded in the entry response. To retrieve hierarchical data, the Taxonomy Terms endpoints must be queried separately.

**Resolution**

1.  Query the taxonomy terms endpoint to retrieve the full term hierarchy: GET /v3/taxonomies/{taxonomy\_uid}/terms
    
2.  Build a local lookup map of term\_uid to its parent/child relationships.
    
3.  Use this map to resolve the hierarchical path from the UIDs returned in entry responses.
    
4.  Alternatively, use GraphQL, which can resolve taxonomy term names and paths inline within an entry query.
    

After building the taxonomy lookup map, confirm that full hierarchical paths can be resolved from the entry-level taxonomy UIDs.

### Column Views in Entry List Not Persisting

Changes made to column layout in the entry list view - adding, removing, or reordering columns - revert to the previous state when navigating away from the page.

**Root Cause**

Column layout changes must be explicitly saved into a Named View to persist. Simply modifying the columns and navigating away does not auto-save the configuration. The view must be saved or updated after making column changes.

**Resolution**

1.  After adjusting the column layout in the entry list, click Save View or Update View to persist the column configuration.
    
2.  For new column configurations, use Save As New View and give the view a name.
    
3.  Select the saved view from the Views menu to load the persistent column configuration on future visits.
    

After saving the view, navigate away and return to the entry list. Confirm the column configuration is preserved.

### Enforce a Structured Tag Library for Content Editors

A team wants editors to choose tags from an approved list rather than entering arbitrary text in the Tags field. A controlled, typeahead-style tag library is needed.

**Root Cause**

The native Tags field accepts free-text input and provides typeahead suggestions for previously used tags, but does not enforce selection from a fixed list. To enforce a controlled vocabulary, additional approaches are needed.

**Resolution**

Three options are available with varying enforcement levels:

1.  Native Tags field with suggestions (lowest enforcement): the Tags field will suggest previously used tags in typeahead, but editors can still enter new values. Requires editorial discipline.
    
2.  Reference-based tag content type (highest enforcement): create a ‘Tag’ content type with a required Title field. Use a Reference field in place of the Tags field. Editors can only select from existing Tag entries, fully enforcing the controlled vocabulary.
    
3.  Custom field via Apps Framework (full control): build a custom field extension that displays a controlled tag selector backed by a Tag content type or external source. Editors see only approved tags and cannot enter free text.
    

After implementing the chosen approach, confirm editors can only select from the approved tag list and cannot add unsanctioned tags.

### Entry Version Limits and Version Number Reset

A customer asks whether entries have a maximum version limit, whether version numbers can be reset, and whether high version counts could cause issues with automated updates.

**Root Cause**

Contentstack does not impose a hard maximum on entry versions. Entries can accumulate many versions over time without hitting a platform-enforced limit. Version numbers increment sequentially and cannot be reset or rolled back to a lower number - though editors can switch to viewing an older version using the version dropdown.

**Resolution**

*   No hard maximum on entry versions: entries can have many versions without platform-level restrictions.
    
*   Version number reset not supported: version numbers always increment and cannot be reset while preserving content.
    
*   Automations and high version counts: automated scripts that frequently save entries will accumulate versions quickly, but this does not cause functional issues. For housekeeping, consider limiting automated saves to meaningful changes only.
    
*   To view an older version: use the version dropdown in the entry editor to switch between versions for review.
    

No action is required unless version accumulation becomes a storage concern. Contact Contentstack Support if there are specific version management requirements.

### BLT IDs or User IDs Appearing in Entry Version History Instead of Names

The version history of an entry displays a BLT ID or a Contentstack user UID instead of the user’s name in the ‘Created By’ or ‘Modified By’ fields. This makes it impossible to identify who made a specific change.

**Root Cause**

This is expected behavior when the user associated with the action has been removed from the Contentstack organization. Once a user profile is deleted, the system can no longer resolve their UID to a display name. The entry retains the UID as a historical identifier but the user profile no longer exists to provide the name.

**Resolution**

This is expected platform behavior and cannot be reversed once the user has been deleted. To identify historical activity:

1.  Use the Audit Log API to retrieve action records by user UID: GET /v3/audit-logs - the response includes the user UID and action details, which can be cross-referenced with any external records of the deleted user’s UID.
    
2.  To prevent this issue going forward, avoid deleting user accounts from the organization while retaining entries they have modified. Instead, remove the user from stacks while preserving their organization membership if auditability is important.
    

The audit log retains historical records including the UID of users who are no longer active, enabling partial traceability even after account deletion.

### Entry Publish Fails with Missing Required Field - Modular Block Minimum Instance Misconfiguration

Publishing an entry fails with a Missing Required Field error. No validation error is visible in the entry UI during save or publish. The error only appears in the publish queue.

**Root Cause**

The modular block within the content type has a minimum instance configuration set to 1, requiring at least one block instance to be present for the entry to be valid. When the entry does not include an instance of that modular block, the missing required field validation triggers at publish time. The UI does not surface this validation error during entry editing because the constraint check is applied at publish rather than save.

**Resolution**

1.  Navigate to the content type schema in the CMS and locate the modular block field showing the validation error.
    
2.  Open the field settings and change the minimum instance value from 1 to 0 if the block is not always required.
    
3.  Save the content type schema.
    
4.  Retry publishing the affected entry and confirm it succeeds without the Missing Required Field error.
    

After updating the minimum instance configuration, attempt to publish the entry again. If publishing succeeds without validation errors, the constraint has been corrected.

### Entry Access Blocked by autodraft=true Parameter - Code 194 Error

Users are unable to access entries in the Contentstack CMS. The error returned is code 194: ‘not allowed to access draft feature’. The issue affects all users on the stack.

**Root Cause**

The autodraft=true query parameter is being included in API requests for entry access. This parameter is part of the Auto Draft Early Access feature. When included, it triggers a code 194 error because the stack’s organization does not have the Early Access feature enabled, or it was enabled and then caused unexpected behavior in the production environment.

**Resolution**

1.  Navigate to Settings > Early Access Features and disable the Auto Draft (Auto-Save) feature if it is enabled.
    
2.  Clear browser cache and hard refresh the page (Ctrl+Shift+R / Cmd+Shift+R).
    
3.  If the issue persists after disabling the feature, contact Contentstack Support with the stack API key and the code 194 error details.
    

After disabling Auto Draft and clearing cache, attempt to access entries and confirm code 194 no longer appears and entries load correctly.

### ‘Something Went Wrong’ or Blank Screen Errors in the CMS

Multiple users across different roles and browsers encounter a ‘Something went wrong’ error or blank screen when accessing the Contentstack CMS. The issue may be widespread across an organization.

**Root Cause**

This error can be caused by: a stale browser cache serving outdated JavaScript assets after a platform deployment, a platform-level incident affecting the UI layer, or the Auto Draft Early Access feature creating unexpected behavior that blocks entry access.

**Resolution**

1.  Clear browser cache and cookies, then perform a hard refresh (Ctrl+Shift+R or Cmd+Shift+R).
    
2.  Open Contentstack in an incognito/private browsing window to rule out cache and extension issues.
    
3.  Check the Contentstack Status Page (status.contentstack.com) for any active incidents.
    
4.  If the Auto Draft Early Access feature is enabled, disable it via Settings > Early Access Features - this is a known cause of ‘You are not allowed’ and ‘Something went wrong’ errors across all roles.
    
5.  If the issue affects multiple users simultaneously and persists after cache clear, escalate to Contentstack Support with the time of onset and affected stack details.
    

After clearing cache or disabling Auto Draft, confirm entries load correctly for all affected users.

### Field UID ‘tags’ Conflicts with System Reserved Keyword

A single-line text field with UID ‘tags’ does not appear in the entry editor, or filling it with a value makes the entire entry inaccessible. The field was created and appears in the content type schema.

**Root Cause**

‘tags’ is a reserved system keyword in Contentstack used for the native Tags metadata field. Creating a custom field with the UID ‘tags’ conflicts with the system-level Tags field. The UI cannot render both and may hide the custom field or cause instability in the entry editor.

**Resolution**

1.  Open the content type in the Content Type Builder.
    
2.  Locate the field with UID ‘tags’ and change its UID to a non-reserved value (for example, ‘article\_tags’, ‘custom\_tags’, or ‘tag\_list’).
    
3.  Save the content type.
    
4.  Open affected entries and confirm the field now appears and accepts input without making the entry inaccessible.
    

Other reserved field UIDs to avoid: title, uid, locale, created\_at, updated\_at, created\_by, updated\_by, publish\_details. Using these as custom field UIDs will cause unpredictable behavior.

### Newly Created Entries or Content Types Not Visible in the UI

An entry or content type is created successfully via the API or UI, but does not appear in the entry list or content type list. The item is accessible via API but invisible in the CMS UI.

**Root Cause**

Newly created items are indexed asynchronously in the search layer that powers the CMS list views. Under high-load conditions, this indexing can lag, causing the item to appear in the API (which reads directly from the primary database) but not in the UI (which reads from the search index).

**Resolution**

1.  Wait 1-2 minutes and refresh the page - indexing typically completes quickly.
    
2.  If the item is still not visible after several minutes, try a hard refresh (Ctrl+Shift+R / Cmd+Shift+R).
    
3.  If the issue persists across multiple users and browsers, contact Contentstack Support. Engineering can trigger a manual index refresh for the affected stack.
    

After the index refresh, confirm the newly created entry or content type appears in the CMS list view.

### Ghost Entries Visible in UI After Successful Deletion

Deleted entries continue to appear in the entry list on a specific branch. API queries confirm the entries no longer exist, but they remain visible in the CMS UI.

**Root Cause**

This is a search index inconsistency. When an entry is deleted, the primary database is updated immediately, but the search index may retain stale records. This creates ghost entries that are visible in the UI but do not exist in the API or backend.

**Resolution**

1.  Confirm the entries are truly deleted by fetching them via the CMA: GET /v3/content\_types/{uid}/entries/{entry\_uid} - a 404 confirms deletion.
    
2.  Contact Contentstack Support and provide the stack API key, branch name, and UIDs of the ghost entries. Engineering will run a search index migration to remove the stale records.
    
3.  Do not attempt to re-delete the ghost entries - they do not exist in the backend and the delete call will fail.
    

After the index migration, reload the entry list and confirm ghost entries are no longer visible.

### ‘URL Not Unique’ Error When Saving - Deleted Entry Holds the URL

Attempting to save an entry returns a ‘value is not unique’ or ‘URL not unique’ error. No other visible entry appears to use that URL.

**Root Cause**

Soft-deleted entries in the Trash continue to hold their URL values until permanently deleted or restored. The system enforces URL uniqueness including against Trash entries.

**Resolution**

1.  Check the Trash/Bin for deleted entries with the conflicting URL via the UI Trash section or GET /v3/trash via the CMA.
    
2.  If a deleted entry with the same URL is found in Trash, either restore and republish it (then delete it properly) or permanently delete it from Trash.
    
3.  If no deleted entry is found, contact Contentstack Support with the entry UID and stack API key. Engineering will investigate whether a stale uniqueness lock exists.
    
4.  Best practice: always unpublish an entry before deleting it to ensure clean removal of all database references.
    

After clearing the stale uniqueness reference, retry saving the entry and confirm it saves without the uniqueness error.

### Entry Search Uses OR Logic - High Volume of Unrelated Results

Searching for entries by multiple keywords returns a large volume of results including multilingual variants and unrelated entries. The expected behavior is to filter by all keywords simultaneously.

**Root Cause**

The default entry search uses OR logic - it returns entries matching any of the provided terms. This is by design.

**Resolution**

1.  Use the Advanced Search (Global Search) feature instead of the basic search bar. Advanced Search supports structured queries with AND conditions between multiple filter criteria.
    
2.  In Advanced Search, create filter conditions for each keyword or field value separately and combine them to narrow results progressively.
    
3.  For programmatic exact-match lookups, use the CMA with a specific query: GET /v3/content\_types/{uid}/entries?query={“field\_uid”:“exact\_value”} which applies strict equality matching.
    

After switching to Advanced Search with multiple AND conditions, confirm the results are narrowed to entries matching all specified criteria.

### CSV Export Fails With ‘File Unavailable’ Despite ‘Export Completed’ Message

A user attempts to export filtered entries from the Entries view as a CSV file. The export process starts, shows ‘processing’, then displays ‘Export Completed’ - but the browser reports ‘file failure - file unavailable’ and no CSV or ZIP file is downloaded. The Network tab shows a 200 status code but the response is JSON rather than a file.

**Root Cause**

This was a bug in the Search Export functionality. The search-grpc service was not returning the correct document set when the requesting user had a custom role with restricted permissions, causing the export file generation to fail silently. The UI reported success but no file was generated on the backend.

**Resolution**

A platform fix has been deployed. CSV export from the Entries view now works correctly for users with custom roles.

1.  If the export still fails after the fix deployment, contact Contentstack Support with the stack API key, the custom role configuration, and the filter criteria used in the export.
    
2.  As a workaround before the fix: use a higher-privileged role (Developer or Admin) to perform the export, or use the CMA to fetch and export entries programmatically.
    

After the fix, apply filters to the Entries view, trigger a CSV export, and confirm the file downloads successfully without a ‘file unavailable’ error.

### RTE Reorders HTML Tags and Inserts Unexpected Non-Breaking Spaces

The Rich Text Editor reorders nested HTML tags (swapping <strong> and <sup> positions) and automatically inserts non-breaking spaces (&nbsp;). The output HTML differs from what was entered.

**Root Cause**

Two separate issues: (1) a confirmed platform bug where <strong> and <sup> tags were reordered during edits - an engineering fix has been deployed; (2) &nbsp; insertion is expected RTE behavior for block structure and cursor stability.

**Resolution**

1.  For tag reordering: the fix has been deployed. If reordering still occurs, contact Contentstack Support with the specific tag combination and reproduction steps.
    
2.  For &nbsp; insertion: strip these characters on the frontend before rendering if they cause visual issues.
    
3.  For the extra <p>&nbsp;</p> appearing above images: remove via the HTML view in the editor, or apply p:empty { display: none } CSS on the frontend.
    

After the fix deployment, verify that <strong>/<sup> tag ordering is preserved when editing entries containing both tags.

### Cannot Paste Bullet Content from Microsoft Word into HTML RTE

Editorial users cannot copy and paste bullet lists from a Microsoft Word document into the HTML Rich Text Editor. The paste operation does not preserve the list structure.

**Root Cause**

Microsoft Word uses a proprietary clipboard format. The HTML RTE does not fully parse Word’s clipboard format and drops bullet/list structure during paste. This is a known limitation of browser-based RTEs.

**Resolution**

1.  Paste into a plain text editor (Notepad or TextEdit in plain text mode) first to strip all Word formatting, then paste from there into the RTE.
    
2.  Alternatively, use the RTE’s own list formatting tools to recreate the bullet structure after pasting the plain text.
    
3.  For teams frequently copying from Word, consider using the JSON RTE which has better handling for structured content imports.
    

After stripping Word formatting before pasting, confirm the text pastes correctly into the HTML RTE without losing content.

### Non-Breaking Spaces Inserted After Pasting from Microsoft Word Online

Content pasted from Microsoft Word Online into the RTE causes unexpected line breaks on the published website. Inspection shows &nbsp; characters between words.

**Root Cause**

Microsoft Word Online inserts &nbsp; characters at copy time to preserve word spacing. When pasted into the RTE, these are preserved and can cause line-break issues in narrow containers.

**Resolution**

1.  Strip &nbsp; characters from RTE content on the frontend before rendering - replace with regular spaces.
    
2.  Alternatively, paste via an intermediate plain text editor to strip the non-breaking spaces before reaching the RTE.
    
3.  For bulk cleanup, use the CMA to fetch entries, apply regex replacement (&nbsp; to space), and update entries programmatically.
    

After implementing frontend stripping or the plain text paste workflow, verify that published content no longer shows unexpected line breaks from &nbsp; characters.

### Code Block Formatting Lost in JSON RTE - VS Code ‘Copy with Syntax Highlighting’

When pasting code copied from VS Code or Cursor into a JSON RTE Code Snippet block, the formatted code appears as a continuous paragraph without syntax structure.

**Root Cause**

VS Code includes hidden formatting metadata when ‘Copy with Syntax Highlighting’ is enabled. This clipboard metadata interferes with the JSON RTE’s parsing of pasted code.

**Resolution**

1.  In VS Code, disable ‘Copy with Syntax Highlighting’: Settings > search for ‘editor.copyWithSyntaxHighlighting’ and set it to false.
    
2.  After disabling the setting, copy and paste the code again into the JSON RTE Code Snippet block.
    
3.  Alternatively, paste into a plain text editor first to strip all formatting metadata, then copy from there into the RTE.
    

After disabling ‘Copy with Syntax Highlighting’, paste code into the Code Snippet block and confirm it renders as structured code without collapsing into a paragraph.

### Onclick and JavaScript Attributes Stripped from Anchor Tags in RTE

nchor tags with onclick attributes entered in the HTML RTE are stripped when switching between HTML and Design views.

**Root Cause**

This is expected behavior. The RTE applies HTML sanitization that removes inline JavaScript event handlers including onclick for XSS security reasons. This cannot be disabled.

**Resolution**

1.  Use CSS classes or data attributes instead of inline onclick: add class=“trigger-modal” or data-action=“open-modal” to the anchor tag and attach the JavaScript handler via external scripts that query these selectors.
    
2.  Use the JSON RTE’s custom block capability to create structured components that the frontend renders with the required JavaScript behavior.
    

After moving event handling to external CSS selectors or data attributes, verify the behavior triggers correctly on the frontend without requiring inline JavaScript in RTE content.

### Duplicate UID Error in Group Field with JSON RTE After Adding Multiple Instances

A Multiple Group field containing a JSON RTE field returns a duplicate UID error when more than one group instance is added. Saving or publishing fails.

**Root Cause**

An extra empty schema: \[\] array in the JSON RTE field configuration within the Group causes a UID conflict when multiple instances are created.

**Resolution**

1.  Fetch the content type schema via CMA: GET /v3/content\_types/{uid} and look for a duplicate empty schema array in the JSON RTE field configuration.
    
2.  Remove the duplicate empty schema: \[\] entry from the JSON RTE field configuration using the CMA: PUT /v3/content\_types/{uid} with the corrected field configuration.
    
3.  After fixing the schema, re-save affected entries and confirm multiple group instances can be added and saved without the duplicate UID error.
    

After correcting the JSON RTE field configuration, add two or more instances of the Multiple Group and confirm it saves and publishes without errors.

### JSON RTE Field Exceeds 30KB Size Limit

Saving an entry returns an error indicating the JSON RTE field has exceeded the 30KB size limit. The field contains large amounts of structured content including tables.

**Root Cause**

Each JSON RTE field has a maximum of 30KB. Tables with many rows, nested formatting, and inline metadata grow significantly in JSON representation. The 30KB counts the full serialized JSON, not visible character count.

**Resolution**

1.  Move large tables to a Reference field pointing to a dedicated ‘Table’ content type, separating table data from the RTE field.
    
2.  Split long content across multiple JSON RTE fields, or across multiple entries linked by references.
    
3.  Reduce nested formatting - excessive bold, italic, and inline style metadata contributes to JSON size.
    

After restructuring, verify the entry saves without the 30KB limit error and the frontend renders the complete content correctly.

### JSON RTE Plugin Block Elements Stripped After Save or Reload

Custom block elements created by JSON RTE plugins (including Contentstack’s out-of-the-box info panel extension) are stripped from the field when the entry is saved and reloaded.

**Root Cause**

This was a platform-level bug in how plugin-generated content was being persisted and reloaded in the JSON RTE - the persistence logic had a gap that dropped plugin-specific block types during serialization.

**Resolution**

A platform fix has been deployed. Plugin-based content in the JSON RTE is now correctly persisted and reloaded.

1.  If plugin block elements are still being stripped after the fix, contact Contentstack Support with the plugin name, block type, and steps to reproduce.
    
2.  As a temporary workaround: use the JSON RTE’s standard block types rather than plugin-created custom blocks where content persistence is critical.
    

After the fix deployment, create a test entry with a plugin-generated block, save and reload, and confirm the block content is preserved.

### JSON RTE Content Not Displaying - Imported JSON Keys Do Not Match Field UID

A JSON RTE field appears empty after content was imported. The data exists in the entry JSON but the field does not render.

**Root Cause**

The JSON RTE field stores content using its field UID as the key. If the imported JSON uses a different key, the field cannot find its data and renders empty.

**Resolution**

1.  Fetch the content type schema: GET /v3/content\_types/{uid} and identify the exact UID of the JSON RTE field.
    
2.  Compare the field UID against the keys used in the imported entry JSON.
    
3.  If keys differ, update the entry JSON to use the correct field UID: PUT /v3/content\_types/{uid}/entries/{entry\_uid} with the corrected JSON structure.
    

After correcting the JSON key to match the field UID, confirm the JSON RTE field renders the imported content and the entry can be saved and published.

### JSON RTE Field Blank, Fails to Load, or Content Disappears - Multiple Causes

The JSON Rich Text Editor field appears completely blank, does not load (stuck on a skeleton), or content briefly appears and then disappears. The issue affects multiple users across browsers and private sessions. In some cases the browser console shows a Minified React error #310.

**Root Cause**

This symptom has several distinct root causes that produce the same visible behavior:

*   Malformed JSON structure in a localized entry: if the entry’s JSON RTE data contains an invalid JSON structure (for example, from a translation service like GlobalLink TransPerfect writing malformed JSON), the field cannot parse and render the content.
    
*   React hook error #310 from large entries: when a JSON RTE field in a very large entry is opened, a React ‘Rendered more hooks than during the previous render’ error (Minified React #310) is thrown by the DiscussionHOC component in the Contentstack bundle. This crashes the RTE field rendering.
    
*   Plugin interference: multiple plugins enabled on the same JSON RTE field (such as image preset and audience plugins) can conflict with each other or with the host RTE, causing blank or disappearing content.
    
*   JavaScript disabled in browser context: if the entry page loads with JavaScript partially disabled or blocked, the RTE component shows ‘You need to enable JavaScript to run this app’ and the table/content does not render.
    

**Resolution**

**For malformed JSON structure:**

1.  Identify the affected entry and locale. Use the CMA to fetch the raw entry JSON: GET /v3/content\_types/{uid}/entries/{entry\_uid}?locale={locale}
    
2.  Inspect the JSON RTE field’s data for malformed structures. Common issues include mismatched brackets, invalid UTF-8 characters, or incomplete serialization from translation tools.
    
3.  Fix the JSON structure manually via CMA PUT and re-save the entry. If the content was generated by a translation service, report the issue to the integration provider.
    

**For React hook error #310 on large entries:**

1.  The error is triggered by opening a very large entry. As a workaround, split the entry’s content into smaller entries or reduce the number of fields visible simultaneously.
    
2.  Contact Contentstack Support if the error is consistent - Engineering can investigate the DiscussionHOC hook count issue.
    

**For plugin interference:**

1.  Disable plugins on the JSON RTE field one at a time in the field configuration to identify the conflicting plugin.
    
2.  Contact Contentstack Support if the conflict is between Contentstack’s own plugins.
    

**For JavaScript-related rendering issues:**

1.  Clear browser cache and hard refresh. Test in incognito mode and a different browser.
    
2.  Disable browser extensions that may be blocking scripts.
    

After identifying the specific root cause from the above patterns, apply the matching resolution and verify the JSON RTE field renders content correctly.

### Links Disappearing or Anchor Tags Wrapped in <p> Tags in RTE

Hyperlinks entered in the Rich Text Editor disappear when switching between HTML and Design views, or anchor tags are automatically wrapped in <p> tags, breaking the intended HTML structure.

**Root Cause**

The RTE enforces block-level structure. Inline elements such as anchor tags (<a>) must be contained within a block-level element. If a link is entered at the top level without a surrounding block element, the RTE either removes it on view switch or automatically wraps it in a <p> tag to comply with HTML standards. This is expected RTE behavior for structural compliance.

**Resolution**

1.  When adding a hyperlink in the HTML view, ensure the anchor tag is always inside a block-level element: <p><a href=“…”>Link text</a></p>
    
2.  For links that keep disappearing: switch to HTML view, wrap the <a> tag inside a <p> tag, and switch back to Design view. The link will persist.
    
3.  For anchor tags being automatically wrapped in <p>: this is expected behavior and ensures valid HTML structure. Apply the <p> tag explicitly rather than relying on the RTE to do it automatically, as placement may vary.
    

After wrapping the anchor tag inside a <p> block element, confirm the link persists when switching between HTML and Design views.

### Cannot Add Fields to Content Type - 500 Field Limit Reached

A user is unable to add new fields to a content type. Field additions silently fail.

**Root Cause**

Contentstack enforces a maximum of 500 fields per content type, counting all fields at every nesting level: top-level, inside Groups, inside Modular Block schemas, and from Global Fields.

**Resolution**

1.  Review the content type’s total field count - complex schemas accumulate counts quickly.
    
2.  Refactor: move reusable field groups to Global Fields, or split the content type into a parent type with reference fields pointing to sub-types.
    
3.  Remove unused or deprecated fields.
    

After reducing the field count below 500, verify new fields can be added and the content type saves.

### Empty Modular Block Instance Not Saved - Expected Behavior

When a modular block instance is added but no field values are entered, the block disappears after page reload.

**Root Cause**

This is expected behavior. Contentstack requires at least one field within the block to contain a value before it is persisted. An empty block is considered a no-op and is discarded on reload.

**Resolution**

This behavior is by design. To retain a modular block instance, populate at least one field before saving. If a block must be saved in a ‘blank’ state, add a placeholder field (such as a boolean or select with a default value) that is always populated automatically.

### Validated Fields Cannot Be Target Fields in Field Visibility Rules

Adding Regex validation to a sub-field inside a Global Field causes the parent group to become invisible when Field Visibility Rules are applied.

**Root Cause**

This is expected behavior. Fields with validation constraints cannot be used as target fields in Field Visibility Rules. This applies even within Groups or Global Fields.

**Resolution**

1.  Use a non-validated control field (such as a Select or Boolean) as the source of the visibility condition.
    
2.  Apply validation to the conditionally shown field, but use the non-validated control field as the FVR target.
    

After restructuring to use a non-validated control field, confirm dependent fields show and hide correctly based on the control field’s value.

### FVR Save Error When Configuring More Than 5 Conditions

Configuring a Field Visibility Rule with more than 5 SHOW or HIDE conditions causes a save error after the 5th condition is added.

**Root Cause**

Contentstack enforces a maximum of 5 conditions per Field Visibility Rule. A fix was deployed to provide a clearer error message, but the 5-condition limit remains.

**Resolution**

1.  Keep each individual Field Visibility Rule to a maximum of 5 conditions.
    
2.  To implement logic requiring more than 5 conditions, split across multiple fields or use a Select control field with compound values mapping to multiple show/hide scenarios.
    
3.  Contact Contentstack Support to submit an enhancement request if more conditions are needed.
    

After reducing the rule to 5 or fewer conditions, confirm the Field Visibility Rule saves and functions as expected.

### Nested Global Fields Inside Modular Blocks - Feature Flag Required

A customer wants to use a Global Field inside an existing block of a Modular Block. This option is not available in the UI.

**Root Cause**

Nesting Global Fields inside individual blocks of a Modular Block is an Early Access feature not enabled by default for all organizations.

**Resolution**

1.  Contact Contentstack Support and request enablement of the Nested Global Field feature, providing the Organization ID.
    
2.  After enablement, navigate to the Modular Block schema in the Content Type Builder and confirm the option to add a Global Field inside an existing block is now available.
    

After the feature is enabled, add a Global Field to a Modular Block block definition and verify it renders correctly in entry instances.

### Cannot Copy Content Type - Invalid FVR Referencing Deleted Field UIDs

Duplicating a content type fails with an error. The content type appears to have correctly configured fields, and manual inspection does not immediately reveal the problem.

**Root Cause**

The content type has Field Visibility Rules (FVR) - either directly or inherited via a Global Field - that reference field UIDs or dropdown values that no longer exist. When the content type was modified (fields deleted or renamed, or dropdown options changed), the FVR configurations were not updated to match. The duplication process validates the full schema including FVR targets, and encounters references to non-existent fields.

**Resolution**

1.  Navigate to the content type in the Content Type Builder and open the Field Visibility Rules for each field.
    
2.  Look for any rule that references a field UID that no longer exists in the schema (these may appear as empty dropdowns or ‘undefined’ values).
    
3.  If the FVR is on a field inside a Global Field, open the Global Field and review its FVR configurations - fixing the rule in the Global Field propagates the fix to all content types using it.
    
4.  Update each invalid FVR to use valid, existing field UIDs and dropdown values.
    
5.  Save the content type (or Global Field) and retry the duplication.
    

After updating the FVR to reference only currently existing fields and values, retry duplicating the content type and confirm it completes successfully.

### Branch Isolation Failure - Content Type Changes Leaking Across Branches

Changes made to a content type in a test branch are incorrectly applied to the main branch. This unexpected behavior led to a significant purge of CDN content, disrupting production data integrity.

**Root Cause**

This was a critical platform-level bug in the branch isolation mechanism. Under specific conditions, schema changes made in one branch were being propagated to other branches, violating the expected branch isolation contract. This caused unintended content type modifications in branches that should not have been affected.

**Resolution**

A platform fix has been deployed to correct the branch isolation failure. Schema changes made in one branch no longer propagate to other branches.

1.  After the fix is deployed, verify branch isolation by making a test change to a content type in a non-main branch and confirming it does not appear in the main branch.
    
2.  If branch isolation issues are still observed after the fix, contact Contentstack Support immediately with the affected branch names, stack API key, and a description of what changed unexpectedly.
    
3.  Review and restore any production content type schemas that were incorrectly modified due to this bug. Use the content type version history or a pre-bug backup to identify the correct schema state.
    

After verifying the fix, confirm that branch isolation is functioning correctly by independently modifying a content type field in each branch and verifying the changes remain isolated.

### Date/Time Field Not Responding - DST Crash in Australian Time Zone

Date and time fields in the entry editor stop responding or become unclickable. Date picker dropdowns open briefly and disappear. Specific to Australian Eastern Time during DST transitions.

**Root Cause**

A confirmed platform bug in main.js where Sydney’s DST flag was missing, causing an infinite update loop in timezone-aware components during DST transitions, crashing the date field UI.

**Resolution**

A platform fix has been deployed to correct DST handling for Sydney and affected Australian time zones.

1.  Clear browser cache and hard refresh after the fix is deployed.
    
2.  If date/time fields are still unresponsive after the fix, contact Contentstack Support with the affected stack, time zone, and a screen recording.
    

After the fix deployment, confirm date/time fields respond correctly to clicks and dates can be selected and saved.

### Social Embed Option Disappeared From JSON RTE

The social embed button in the JSON RTE is no longer visible for certain content types. It was previously working.

**Root Cause**

The social embed option requires the Social Embed feature to be enabled at the field level. When a content type is restructured or duplicated, the social embed configuration may not carry over correctly.

**Resolution**

1.  Open the content type in the Content Type Builder and navigate to the affected JSON RTE field.
    
2.  Click the field to open its configuration, navigate to Advanced > Custom settings.
    
3.  Enable the Social Embed toggle.
    
4.  Save the content type and confirm the social embed option now appears in the JSON RTE toolbar.
    

After enabling the Social Embed toggle, verify the option appears in the JSON RTE for editors.

<!-- case:00060538 status:draft synced:false bucket:"Content Editing & UI Workflows" -->
### Mixed Arabic/Latin Text Displays Left-to-Right in Multi Line Textbox

Entering mixed Arabic and Latin text into a Multi Line Textbox field may render left-to-right (LTR) instead of right-to-left (RTL), even when most of the content is Arabic.

**Root Cause**

The Multi Line Textbox is a plain text field, so Contentstack does not explicitly control its text direction. The browser applies the Unicode Bidirectional Algorithm instead, which determines RTL versus LTR based on the first strong directional character in the field. When a Latin character appears before any Arabic character, the browser resolves the entire field as LTR.

**Resolution**

1.  Insert a Unicode Right-to-Left Mark (U+200F) as the first character in the field value. This is a zero-width, non-printing character and does not affect the visible content.

2.  Save and publish the entry.

After inserting the RTL mark, reload the entry and confirm the field renders right-to-left. If the direction displays correctly, the issue is resolved. Escalate with the field UID and a sample of the affected text if the mark does not force RTL rendering.

<!-- end:00060538 -->

## Publishing, Releases, Environments and Operations

### Referenced Entry Not Publishing with Parent Entry

Referenced entries are not automatically published unless they are already live at the time the parent entry is published.

**Root Cause**

During scheduled publishing, dependencies are resolved at publish time. If a referenced entry is not live in the same environment when the parent entry publishes, it is not included automatically.

**Resolution**

1.  Identify all referenced entries in the parent entry.
2.  Schedule the referenced entries to publish first.
3.  Schedule the parent entry to publish a few minutes later.

After the scheduled publish completes, open the parent entry and confirm that all referenced entries are published and visible in the target environment.

For more information, refer to [Working with Nested Reference Publishing](/docs/headless-cms/working-with-nested-reference-publishing) documentation.

### Bulk “Add to Release” Operations Stuck or Failing

Bulk “Add to Release” operations may remain in a queued status for an extended period or fail to complete. This behavior is identified as a platform limitation when the system experiences high concurrent load on bulk processing services.

**Root Cause**

High demand on background processing services can delay or block task execution.

*   **Symptoms**: Operations may show a "queued" status for an extended time without progressing.
*   **Partial Success**: Partial success can occur where only a subset of the selected entries are successfully added before the process stalls, if one or more selected entries do not meet the publishing requirements.
*   **Retry Safety**: It is generally safe to retry the operation if it remains stuck, as the system will identify existing Release members and avoid duplicates.

**Resolution**

*   **Stagger Operations**: Avoid triggering excessive concurrent bulk actions across the same stack to reduce service contention.
*   **Retry Strategy**: Monitor the task status; if the operation remains queued significantly past expected limits, retry the action after platform load has stabilized.
*   **Batch Sizing**: Reduce the number of entries per individual "Add to Release" action to ensure faster completion times.

The operation is confirmed successful once all selected entries appear within the target Release and the task status in the background activity log marks as "Completed".

### Accessing nested reference publishing in Bulk Operations

Performing nested reference publishing in the Bulk Operations App may fail to show the “publish with references” option. This prevents publishing entries together with their nested references using the app.

**Root Cause**

The Bulk Operations App does not support the “Send with References” feature.

**Resolution**

1.  Navigate to the Entries UI and use the Bulk Publish option for nested reference publishing.
2.  Publish referenced entries separately if continuing to use the Bulk Operations App.

After navigating to the Entries UI, attempt to use the Bulk Publish feature. If the “publish with references” option is available, the correct publishing method is active.

### Impact of renaming environments on API and tool configurations

Renaming an environment in the CMS UI may cause connectivity issues in APIs, SDKs, and the CLI when the new name is not updated. This prevents external tools from accessing the renamed environment.

**Root Cause**

Environment name changes affect all code or tooling references to that environment, although API tokens remain valid.

**Resolution**

1.  Update the environment name in all API calls, SDK configurations, and CLI usage to reflect the new name.

After updating the environment name in the relevant code or tools, execute a test request. If the request connects successfully to the renamed environment, the updates are correct.

### Bulk API Shows Complete But Entries Published to Only One Environment

A Bulk API publish job returns a success or complete status, but the published entries only appear in one of the two intended environments (for example, staging instead of both staging and development).

**Root Cause**

The Bulk API was functioning correctly. The issue was in the implementation — the API request payload was not consistently including both environments in the publish target. When the payload specifies only one environment, the API publishes to that environment and returns complete, which is accurate for the request it received.

**Resolution**

1.  Review the Bulk API request payload and confirm that both target environments are included in the environments array of the publish request body.
    

**Example structure:** { "entries": \[...\], "locales": \[...\], "environments": \["staging", "development"\] }

1.  Test the corrected payload for a single entry before running the full bulk operation.
    
2.  Re-run the bulk publish with the corrected payload and verify the entries appear in both environments.
    

After correcting the environments array in the payload, re-run the bulk publish. If entries appear in both environments after the job completes, the payload is now correct.

### Release Deployment Fails with "Field Not Marked as Multiple" Error

A release deployment fails with an error stating that a field is not marked as multiple. The same entry can be published directly from the CMS without any error, making the release-specific failure confusing.

**Root Cause**

The multiple flag is set on the extension for the field but is not set on the field definition within the content type schema. Direct publishing may not enforce the schema validation as strictly as release deployment, which performs a full schema compliance check before deploying. The mismatch between the extension's multiple setting and the content type field definition causes the deployment to fail.

**Resolution**

1.  Navigate to the content type in the CMS and locate the affected field.
    
2.  In the field settings, enable the multiple flag on the field itself to match the extension's configuration.
    
3.  Save the updated content type schema.
    
4.  Re-add the entry to the release if required and attempt the deployment again.
    

After correcting the multiple flag on the field definition, re-run the release deployment. If the deployment completes without the validation error, the schema mismatch is resolved.

### Entries Cannot Be Added to a Release - Stuck in In-Queue State

Bulk Add to Release operations fail with entries stuck in an in-queue state in the bulk task queue. The issue affects multiple users and blocks release workflows.

**Root Cause**

This is a platform-level capacity issue where the bulk-action processing pods are overwhelmed by concurrent Add to Release requests, particularly when Marketplace Integration jobs are also running simultaneously. Insufficient pod capacity causes the queue to back up.

**Resolution**

1.  Contact Contentstack Support and report the stack details and the in-queue bulk task UIDs.
    
2.  Engineering can scale the bulk-action processing pods to clear the backlog and resume processing.
    
3.  As a workaround while the queue is clearing, add entries to releases in smaller batches with pauses between batches.
    
4.  Avoid running large Add to Release operations simultaneously with other bulk operations (bulk delete, global field updates) to reduce pod contention.
    

After engineering scales the processing capacity, monitor the bulk task queue. If entries transition from in-queue to processing and complete, the capacity issue is resolved.

### Scheduled Publish Overridden by a Manual Publish on the Same Entry

An editor schedules a future publish for one field of an entry. Another editor manually publishes the same entry before the scheduled time. The scheduled publish still fires at the set time, but now publishes an outdated or unexpected version.

**Root Cause**

This is expected behavior. Each publish action, whether manual or scheduled publishes the full current state of the entry at the time of execution. A manual publish does not cancel a scheduled publish. When the scheduled publish fires, it publishes whatever version of the entry is current at that time, which may include or overwrite the manually published changes depending on the sequence of edits.

**Resolution**

There is no configuration or permission setting to prevent a manual publish from affecting a scheduled publish on the same entry. Recommended workflow practices:

1.  Coordinate publish activities between editors working on the same entry to prevent conflicts.
    
2.  Cancel the scheduled publish explicitly if a manual publish has made it redundant — navigate to the scheduled publish in the CMS and delete the schedule.
    
3.  Use Releases for controlled publishing workflows where multiple entries are coordinated and published together at a specific time.
    

Teams working on the same entry should communicate before publishing to avoid unintended overrides of scheduled content.

### Scheduled Publish vs. Releases - When to Use Each

Basic scheduled publish is used to queue entries for future publishing. However, when the entry is updated after the schedule is set, it is unclear whether the updated or original version will be published at the scheduled time.

**Root Cause**

The basic Schedule Publish feature publishes the entry at the scheduled time, but what it publishes depends on the latest saved version at that time, not a snapshot taken at scheduling. This can lead to unexpected results if the entry is modified after scheduling. Releases address this by providing a snapshot-based workflow.

**Resolution**

1.  For content that may be updated between scheduling and publish time, use Releases instead of basic scheduled publish.
    
2.  Releases allow you to group entries, review exactly what will be published, and deploy the release at a scheduled time.
    
3.  If an entry in a Release is updated before the release is deployed, the release will publish the latest version — this is intentional and predictable.
    
4.  Use basic scheduled publish only for simple, single-entry scenarios where no edits are expected between scheduling and publish time.
    

After switching time-sensitive multi-entry workflows to Releases, confirm that deployments publish the expected version of each entry.

### CLI Migration Accidentally Ran on Main Branch - Restoring Deleted Fields

A CLI migration intended for a non-main branch using the --branch flag was executed on the main branch due to a misconfiguration. Fields were deleted from content types and content may have been lost.

**Root Cause**

The CLI migration ran on the main branch because the branch specification was not correctly applied or the migration script defaulted to main. Once fields are deleted from a content type, the associated content data is also removed. However, if the content type itself still exists, recreating the deleted fields with the same UIDs can restore access to the original data.

**Resolution**

1.  Identify all deleted fields by reviewing the audit log for the affected content type.
    
2.  Recreate each deleted field using the CMA or CMS UI, using exactly the same field UIDs as the original fields.
    
3.  After recreating the fields, verify whether the original content data is restored by fetching affected entries.
    
4.  To prevent recurrence, test all CLI migrations on a dedicated branch and verify the --branch flag is correctly set before running on any production branch.
    

After recreating the fields with identical UIDs, fetch the affected entries and confirm the content data is accessible. If the content is restored, the field recreation has succeeded.

### Hundreds of Entries Failing Release Publish Due to Missing Modular Block Metadata

A large number of entries in a release fail to publish. Re-saving entries manually without changes fixes the error, but manually re-saving hundreds of entries is not practical.

**Root Cause**

The entries are missing the required \_metadata.uid field for one or more nested modular blocks. This metadata is auto-generated when an entry is saved through the CMS. Entries created or modified programmatically (for example, via API or migration scripts) may not have this metadata populated. The release publish validation requires this metadata and fails when it is absent.

**Resolution**

1.  Use the CMA API to programmatically fetch and re-save each affected entry. A re-save without content changes is sufficient to trigger the metadata regeneration.
    
2.  Script the re-save using the following approach:
    
    *   Fetch each entry UID from the release using the Releases API.
        
    *   For each UID, perform a GET then a PUT (update) to the entry with the same payload to force a re-save.
        
3.  After re-saving all affected entries, re-attempt the release publish and confirm entries are now deploy-ready.
    

After scripting the bulk re-save, check the release deployment status. If entries transition from error to deploy-ready and the release publishes successfully, the metadata regeneration is complete.

### Scheduling Publish for a Parent Entry That Has Referenced Entries

A parent entry is scheduled for future publish, but referenced child entries are not included in the scheduled publish. When the scheduled publish fires, the parent is published but the referenced entries remain at their previous state, causing content inconsistencies.

**Root Cause**

When scheduling a publish for a parent entry, referenced entries are not automatically included in the schedule unless they are explicitly added. Scheduling only the parent publishes the parent entry at the set time, but referenced entries retain their current published version. If referenced entries have unpublished changes, those changes will not go live with the scheduled parent publish.

**Resolution**

1.  When scheduling a publish for a parent entry that references other entries, include all referenced entries in the scheduled publish.
    
2.  In the CMS UI, use the Publish with References option when scheduling to automatically include referenced entries in the publish action.
    
3.  Via the CMA, include all referenced entry UIDs explicitly in the publish request payload alongside the parent entry.
    
4.  Alternatively, use Releases to group the parent and all referenced entries together and schedule the release deployment, which ensures all entries are published atomically at the scheduled time
    

After including referenced entries in the scheduled publish or Release, verify at the scheduled time that both the parent and all referenced entries reflect the latest published version.

### Publish Rules Ignored During Bulk Publish with References - Resolved Bug

When a parent entry is published using the Send with References bulk publish option, the publish rules for associated child entries are not enforced. Child entries are published to languages and environments where the publishing user does not have the required permissions.

**Root Cause**

This was a confirmed platform bug where the bulk publish with references operation bypassed workflow publish rule validation for child entries. The publish rules were correctly enforced for direct publishes, but not when referenced entries were published as part of a Send with References bulk action.

**Resolution**

This issue has been resolved by the Contentstack engineering team. Publish rules are now correctly enforced for child entries during bulk publish with references operations. No configuration change is required

1.  If you encounter publish rule bypass behavior during bulk publish with references after this fix, contact Contentstack Support with the affected entry UIDs and publish action details for investigation.
    
2.  Ensure that publish rules and role permissions are correctly configured in Settings > Workflows for the relevant content types and environments.
    

After the fix is applied, attempt a bulk publish with references for entries that have restrictive publish rules. If child entries are correctly blocked or routed based on publish rules, the fix is in effect.

### include_publish_details Returns Empty in CMA Response

CMA API calls using include\_publish\_details=true return an empty or null publish\_details field, even though entries are confirmed as published. The issue appears on EU stacks but entries are visible in the CDA.

**Root Cause**

A backend inconsistency in how publish details are stored per locale causes the CMA to fail to retrieve them for certain entries. The data exists but is not correctly indexed for retrieval. Re-saving all locales of the affected entries forces a re-write of the publish details index, resolving the retrieval issue.

**Resolution**

1.  Identify all locales for the affected entries.
    
2.  Open each entry, switch to each locale, and perform a save without content changes.
    
3.  For large numbers of entries, use a CMA script to fetch each entry per locale and re-save using PUT /v3/content\_types/{uid}/entries/{entry\_uid}?locale={locale}.
    
4.  After re-saving, re-run the include\_publish\_details=true request and confirm the publish\_details field is now populated.
    

After re-saving all locales, verify the CMA response includes publish\_details with the correct environment and publish timestamp for each locale.

### api_version: 3.2 Header Routes All Publishes to Bulk Queue

Publish requests sent with the api\_version: 3.2 header are being routed to the Bulk Publish Queue and returning a job\_id. The same requests without the header process immediately through the Single Publish Queue. The Bulk Publish Queue is already heavily loaded, causing further delays.

**Root Cause**

This is expected behavior in API version 3.2. The 3.2 version routes all publish operations through the Bulk Publish Queue, regardless of whether the entry is localized. This change was introduced to standardize publish processing. The queue delay is a consequence of using the newer API version.

**Resolution**

1.  If immediate publishing is required and bulk queue load is a concern, omit the api\_version: 3.2 header to route the request through the Single Publish Queue.
    
2.  If api\_version: 3.2 is needed for other behavioral changes it introduces, implement polling logic against the returned job\_id to track publish completion rather than expecting a synchronous response.
    
3.  Use GET /v3/bulk/jobs/{job\_id} to poll job status until it reaches ‘complete’ or ‘failed’.
    
4.  Monitor the Bulk Publish Queue load before using 3.2 in high-frequency publishing workflows to avoid compounding queue delays.
    

After selecting the appropriate API version for the use case, confirm publish operations complete correctly and queue load is within acceptable bounds.

### Bulk Publish Fails from Entry List Page but Works from Individual Entry Editor

Attempting to bulk publish entries from the Entry List page fails, while publishing the same entries individually from the entry editor succeeds. The issue occurs primarily on non-main branches after downporting content from the main branch.

**Root Cause**

This is a platform-level bug in the descendants validation logic for bulk publish operations in non-main branches. The bulk publish path applies a stricter descendant reference check than the individual entry publish path, causing valid entries to fail bulk publication if the branch context is not correctly resolved.

**Resolution**

1.  As an immediate workaround, publish affected entries individually from the entry editor.
    
2.  Contact Contentstack Support with the affected branch name, stack API key, and entry UIDs. Engineering will investigate the branch-context issue.
    
3.  After the platform fix is applied, retry the bulk publish from the Entry List page and confirm entries publish successfully.
    

After the engineering fix, verify bulk publish from the Entry List page completes without errors for entries on non-main branches.

### Publish Modal Shows Endless Loading Spinner on 422 Error

Clicking Publish on an entry triggers a continuous loading state in the publish modal. No error message appears in the UI. The publish operation does not complete. Network inspection shows the backend returning a 422 response.

**Root Cause**

The publish modal does not surface 422 error messages from the API response, leaving editors without feedback on why the publish failed. The 422 typically indicates a validation failure - an invalid or missing required field, a schema constraint violation, or a reference resolution issue.

**Resolution**

1.  Open the browser’s developer tools and navigate to the Network tab.
    
2.  Attempt the publish and identify the failing API request (typically a POST to /v3/bulk/publish or similar).
    
3.  Inspect the response body of the 422 request for the specific error message and error\_code.
    
4.  Common causes: a required field is empty, a field value fails a regex or length constraint, or a referenced entry has missing mandatory fields. Address the specific validation error surfaced in the response.
    
5.  After fixing the underlying validation issue, re-attempt the publish and confirm it completes without the spinner.
    

If the 422 error reason is unclear, contact Contentstack Support with the entry UID, content type, and the raw 422 response body for investigation.

Note: The same silent 422 pattern applies in Visual Experience (Visual Builder). If clicking Publish in the Visual Experience interface produces an ‘Invalid Input’ error without further detail, the root cause is also a 422 validation failure from the underlying API. Inspect the network response for the specific validation message (for example, a third-party component such as Commercetools Product Finder may be generating the invalid payload). The fix in those cases comes from the component or extension responsible for the invalid input.

### Entry Cannot Publish - Ghost Taxonomy Field No Longer in Content Type

An entry fails to publish with a ‘missing required field’ error referencing a taxonomy field. However, inspection of the content type shows the taxonomy field no longer exists - it was removed previously. The entry appears to still expect the deleted field.

**Root Cause**

When a field is removed from a content type, the change is applied to the schema but not retroactively cleaned from existing entry data. If the field was marked as required at the time of its removal, or if the entry’s data structure was not refreshed after the content type change, the entry may still carry a reference to the deleted field in its internal metadata, causing publish validation to fail.

**Resolution**

1.  Open the affected entry in the CMS editor.
    
2.  Perform a save without content changes. This triggers a schema revalidation and clears stale field references from the entry’s internal structure.
    
3.  Attempt to publish again. If the error persists, export the entry JSON via the CMA and inspect the data for any reference to the deleted field UID.
    
4.  If a stale field reference is found in the entry JSON, remove it programmatically using the CMA PUT endpoint and re-save.
    
5.  If the issue affects multiple entries, use a CMA script to identify entries with the ghost field reference and re-save each one.
    

After re-saving the entry and clearing the stale field reference, confirm the entry publishes without the missing required field error.

### Cannot Publish Localized Entries After Taxonomy Field Changed to Non-Localizable

After changing a taxonomy field from localizable to non-localizable across 40+ content types, localized entries fail to publish. Errors show ‘missing required field’ or the entries remain in an inconsistent state.

**Root Cause**

Changing a field’s localizable status after entries have been created creates a data state mismatch. Localized entries already have locale-specific values stored for the field. When the field is changed to non-localizable, the system expects the value to come from the master locale only, but the localized versions may have stale or conflicting data that prevents publish validation from passing.

**Resolution**

1.  Contact Contentstack Support and provide the affected content type UIDs, the field UID that was changed, and a sample of failing entry UIDs. Engineering will assess the data state.
    
2.  For each affected localized entry, open it in the CMS editor under each locale, verify the field state, and re-save to trigger schema revalidation.
    
3.  If the field is required and the master locale value is not propagating to localized entries, confirm the field value is set in the master locale and re-save the master locale entry first, then re-save localized entries.
    
4.  For large-scale remediation, use a CMA script to re-save all affected localized entries after the master locale is confirmed correct.
    

After resolving the data state mismatch, verify that localized entries publish successfully and the correct (master locale) non-localizable field value is reflected in all locale variants.

### Release Unpublish Stuck in ‘In Progress’ - Never Completes

A release triggered for unpublishing content has been stuck in ‘In Progress’ state for an extended period. Entries included in the release remain published on live environments despite the release being in progress.

**Root Cause**

Release deployments can become stuck when the release processing job encounters a failure mid-execution that does not cleanly roll back or transition to a failed state. This leaves the release in a locked ‘In Progress’ state that prevents new deployments and leaves entries in their current published state.

**Resolution**

1.  Contact Contentstack Support immediately and provide the release UID, stack API key, and the time the release was triggered.
    
2.  Engineering will inspect the release job state and forcefully complete or retry the stuck deployment.
    
3.  If entries need to be unpublished urgently while the release is stuck, use the CMA bulk unpublish endpoint as a direct workaround: POST /v3/bulk/unpublish with the specific entry UIDs and environments.
    
4.  After the release is resolved, verify the entries are correctly unpublished and the release shows a completed state.
    

If the release deployment continues to fail after retry, consider recreating the release with the same entries and re-deploying.

### Release Stuck in Locked State - Retry Deployment

A release repeatedly fails to deploy and appears in a locked state. Previous deployment attempts have failed in the release history. The release cannot be re-triggered from the UI.

**Root Cause**

Release deployments can enter a locked state when a previous deployment attempt failed partway through and did not correctly release its lock. Subsequent retry attempts are blocked until the lock is cleared.

**Resolution**

1.  Review the release deployment history in the Releases section for any failed attempts and their error details.
    
2.  Wait briefly and attempt to retry the deployment from the UI - in some cases the lock clears on its own.
    
3.  If the lock does not clear, contact Contentstack Support with the release UID and stack details. Engineering can manually clear the lock and allow a fresh deployment attempt.
    
4.  During a call with Support, review the deployment and network logs to validate the release item count and confirm the deployment can proceed.
    

After the lock is cleared, retry the deployment and confirm the release completes successfully and entries are published or unpublished as intended.

### Publishing Dialog Prompts Re-Publishing Already-Published References in Non-Localized Locales

The publish dialog incorrectly shows already-published reference entries as needing republishing when publishing a specific entry in non-localized locales. This creates unnecessary re-publish operations and editorial confusion.

**Root Cause**

This is a platform-level bug specific to certain entries where the publishing dialog’s reference resolution logic for non-localized locales incorrectly flags already-published references as pending. The behavior was identified as data-specific - other entries using the same references do not exhibit the issue.

**Resolution**

1.  Contact Contentstack Support with the affected entry UID and content type. Engineering will investigate whether data corruption or a stale reference state is causing the incorrect flag.
    
2.  As a workaround, proceed with the publish - republishing already-published references does not cause data loss and is safe. The entries simply receive a new publish timestamp.
    
3.  After the platform fix is applied, confirm the publish dialog no longer prompts unnecessary re-publishing of already-published references.
    

After the fix, attempt a publish of the affected entry and confirm the dialog shows only genuinely unpublished references as pending.

### Scheduling Conflicts - Editing a Live Entry With a Pending Scheduled Publish or Unpublish

An editor needs to make emergency changes to a live entry that already has a pending scheduled publish or unpublish action. They are unsure how editing the live entry will interact with the pending schedule.

**Root Cause**

Contentstack handles scheduled actions and live edits as separate version-based operations. Understanding the interaction requires knowing which version each action targets.

**Resolution**

**Scenario: Entry is live (published). A scheduled publish exists for a future version.**

Editing and publishing the live entry immediately creates a new version and publishes it. The scheduled action will publish the version it was set against - if that version is now older than the current live version, the scheduled publish may overwrite the current live content when it fires. Cancel the scheduled action before making immediate changes if this is a concern.

**Scenario: Entry is live. A scheduled unpublish exists.**

Editing and saving the entry does not cancel the scheduled unpublish. When the scheduled time arrives, the entry will be unpublished regardless of any edits made. If the entry should remain live after the scheduled time, cancel the scheduled unpublish before making edits.

**Scenario: Entry is not yet published. A scheduled publish exists.**

Edits made before the scheduled publish time will be part of the version that publishes at the scheduled time, provided the entry is saved before the schedule fires. Saving after the schedule fires will create a new version that is not scheduled.

1.  Always review the scheduled actions on an entry (visible in the entry’s schedule panel) before making emergency edits.
    
2.  If the emergency change should override a pending schedule, cancel the schedule first, make the change, and re-schedule if needed.
    

Confirm the desired content is live after the emergency edit by checking the entry’s publish status and verifying the correct version is shown in the published environment.

### Publish with References’ - Cannot Be Disabled, and Can Silently Skip Already-Published Entries

This article covers two related but distinct issues with the platform’s ‘Publish with References’ behavior.

**Scenario A - Cannot Be Disabled**

A customer wants to suppress or disable the ‘Publish with References’ behavior so that publishing an entry does not trigger cascading publish operations on all referenced entries. They are also looking to identify publish-with-references events in webhook payloads or Automate action logs.

**Root Cause**

‘Publish with References’ is a platform-enforced behavior in the standard publishing workflow. There is no built-in setting or API parameter to disable or suppress it. Contentstack processes the referenced entry publishes as multiple individual publish events internally, rather than exposing a distinct flag or attribute. As a result, this option is not available as a distinguishable event in webhook payloads or Automate Hub action logs.

**Resolution**

As there is no native disable option, the following approaches can control the behavior:

1.  Publish entries individually using the CMA single-entry publish endpoint rather than the UI ‘Publish with References’ flow. The CMA publish endpoint does not automatically resolve and publish referenced entries unless explicitly instructed.
    
2.  In webhook-receiving logic, filter events by entry UID to distinguish which entries were explicitly published versus which were pulled in as references.
    
3.  Use Releases as the publishing mechanism - Releases give explicit control over which entries are included in a deployment without automatically pulling in unrequested references.
    
4.  If the goal is to prevent editors from accidentally publishing referenced entries, configure Publish Rules to require approval before production publishes, giving an approver visibility into what is being published.
    

After adopting one of the above approaches, confirm that publishing operations affect only the intended entries.

**Scenario B - Silently Skips a Previously Published Entry**

Using ‘Publish with References’ to publish a parent entry results in a referenced module being skipped rather than published. The module was previously published but has since been updated. The publish queue shows the module as ‘Skipped’.

**Root Cause**

The ‘Publish with References’ operation skips referenced entries that were already published under the same version and state. If the referenced module was previously published and the system considers the current version as already live (even if the module has been updated), the publish step is skipped. This occurs when the module was published with the same version number as the current draft version.

**Resolution**

1.  Open the skipped referenced entry (module) and make a minor save (even without content changes) to increment its version number.
    
2.  Re-publish the module directly from the entry editor.
    
3.  Then re-publish the parent entry using ‘Publish with References’ to include the now-updated module.
    
4.  Alternatively, use a Release to group the parent entry and all referenced modules, which provides more granular control over what is included in each publish action.
    

After saving and re-publishing the skipped module, confirm it is included in the next ‘Publish with References’ operation and appears as published in the target environment.

### Required Field Validation Bypassed During Bulk Publish - Platform Bug Fixed

Entries with unpopulated required fields (specifically images and single-line text fields) are successfully published via bulk publish operations. The required field validation that normally blocks individual entry publish does not apply during bulk publish.

**Root Cause**

This was a platform-level bug where the required field validation was not being consistently enforced across both individual and bulk publish workflows. Entries that would correctly fail validation when published individually were bypassing the same validation during bulk publish operations.

**Resolution**

A platform fix has been deployed. Required field validation is now consistently enforced across both individual entry publish and bulk publish workflows. No configuration change is required.

1.  If entries with missing required fields were successfully published before the fix, review and re-publish affected entries after populating the required fields to ensure the published content is valid.
    
2.  To audit which entries were published with missing required fields, query the CDA for the affected content type and check for entries where the required field is null or empty.
    

After the platform fix, attempt a bulk publish with an entry that has an empty required field and confirm the operation correctly fails with a validation error.

### Rolling Back a Release by Bulk-Unpublishing Released Entries

A release has been deployed and the customer needs to roll it back - effectively undoing the publish of all entries included in the release. There is no native ‘rollback’ button on a deployed release.

**Root Cause**

Contentstack does not provide a one-click rollback mechanism for deployed releases. Rollback must be performed by explicitly unpublishing the entries that were deployed in the release.

**Resolution**

**From the Entries List page (UI):**

1.  Navigate to the Entries section in the stack.
    
2.  Use filters or search to identify and select the entries that were part of the released deployment.
    
3.  Use the checkboxes to select all affected entries.
    
4.  Click Unpublish from the floating action panel and select the target environments.
    

**Programmatically via CMA (recommended for large releases):**

1.  Retrieve the list of entry UIDs from the release: GET /v3/releases/{release\_uid}/items
    
2.  Use the CMA bulk unpublish endpoint: POST /v3/bulk/unpublish with the array of entry UIDs and target environments.
    
3.  Poll the returned job\_id to confirm all entries are unpublished.
    

After the rollback, verify a sample of the released entries are no longer accessible via the CDA and that the environment reflects the pre-release content state.

### 403 Error on Publish Modal Descendants API in Non-Master Locales

The publish modal displays a spinner or 403 error when attempting to publish entries in non-master locales. The issue affects entries in specific stacks and appears only for certain locale combinations.

**Root Cause**

The 403 error on the publishing modal’s descendants API is caused by a deleted locale UID being referenced in the query. When a locale is deleted from a stack, its localeUid may remain as a reference in certain entry metadata. When the publish modal attempts to fetch descendants for that locale, the query fails with a 403 because the localeUid no longer exists.

**Resolution**

A platform fix has been deployed. The descendants query now only fetches entries where deleted\_at is false, preventing the 403 error from being triggered by deleted locale references. No action is required for stacks affected by this bug after the fix is applied.

1.  If the 403 error persists after the fix deployment, contact Contentstack Support with the affected stack API key, entry UID, and the locale combination that triggers the error.
    
2.  As a workaround before the fix is available: publish the entry via the CMA directly, bypassing the publish modal: POST /v3/bulk/publish with the entry UID and target locale and environments specified in the request body.
    

After the fix is applied, open the publish modal for an entry in a non-master locale and confirm the descendants list loads without a 403 error or spinner.

### New Branch Not Appearing in UI After Creation

A newly created branch does not appear in the Contentstack UI several hours after creation. Branch creation jobs disappear from the Bulk Task Queue without confirming success or providing error logs.

**Root Cause**

This was previously caused by infrastructure bottlenecks (GCP search service / Elasticsearch capacity) combined with a UI bug where long-running branch creation tasks dropped off the Bulk Task Queue before completing, even though the branch was still being created in the background. Contentstack has since remediated the infrastructure bottleneck through search service scaling and the Branch Parallelization plan; branch creation times for large stacks have stabilized to a 45–60 minute window. Retrying creation while the original job is still running produces a ‘branch already exists’ error.

**Resolution**

1.  Wait 45–60 minutes before assuming branch creation has failed. This is the expected window for large-stack branch creation following Contentstack’s infrastructure improvements.
    
2.  Check whether the branch already exists by navigating to Settings > Branches and refreshing the page.
    
3.  Do not retry branch creation if the job appeared to disappear - check first whether the branch was silently created. Retrying will produce a ‘branch already exists’ error if creation is completed.
    
4.  If the branch genuinely did not create after several hours, contact Contentstack Support with the stack API key and the time the creation was initiated. Engineering can check the background job status.
    

After confirming the branch exists, verify it contains the expected content by navigating to it and checking a known content type.

### Branch Merge Reports Success but Leaves Broken Global Field References

A branch merge operation reports success but the target branch is left in an inconsistent state. Global field references are broken, field rule changes were not applied, and entries show red-outlined blocks in the CMS editor.

**Root Cause**

The merge process completes at the schema level without fully normalizing or rebinding global field dependencies. When global fields are updated in the source branch and merged, the merge operation applies field rule changes but does not re-resolve the global field references in the target branch’s entries, leaving orphaned or stale references.

**Resolution**

1.  Contact Contentstack Support immediately and provide the source branch, target branch, stack API key, and the time of the merge. Engineering will assess the inconsistent state.
    
2.  As a diagnostic step, open affected entries in the target branch and check whether the red-outlined blocks correspond to specific global fields.
    
3.  Do not delete and recreate the global fields manually - this can compound data loss.
    
4.  Engineering will apply a targeted fix to normalize global field bindings in the target branch without requiring a full re-merge.
    
5.  After the fix, re-save affected entries to trigger schema revalidation and confirm the red-outlined blocks are resolved.
    

After Engineering resolves the reference normalization, verify a sample of affected entries display correctly and the global field references load without errors.

### Bulk Publish Jobs Stuck in ‘In Progress’ or ‘In Queue’ Status

This article covers two related but distinct causes of bulk publish jobs appearing stuck in ‘In Progress’ or ‘In Queue’ status.

**Scenario A - Status Tracking Bug (Entries Actually Published)**

Bulk publish jobs initiated via the API with publish\_all\_localized=true appear stuck in ‘In Progress’ or ‘In Queue’ status indefinitely. Entries are actually published successfully in the background, but the job status never updates to ‘Complete’ in the UI or API.

**Root Cause**

This is a platform-level bug in the job status tracking for bulk publish operations with the publish\_all\_localized=true parameter. The background publish process completes successfully, but the job management layer fails to update the status to reflect completion. This makes it impossible to programmatically confirm success or failure from the job status API.

**Resolution**

1.  Verify that entries are actually published by querying the CDA for the affected entries and checking their published status directly, rather than relying on the job status.
    
2.  Contact Contentstack Support and provide the stuck job IDs. Engineering can investigate and apply a fix to the job status tracking system.
    
3.  As a workaround for job monitoring, implement a post-job verification step that checks the publish status of a sample of entries via the CDA rather than relying on the job status endpoint.
    

After the platform fix is applied, confirm that new bulk publish jobs with publish\_all\_localized=true show ‘Complete’ status correctly in the UI and API.

**Scenario B - Job Stuck with No Cancel Option (Processing Error, Not Status-Tracking)**

A bulk publish job has been in ‘In-Progress’ for an extended period with no UI Cancel option, and - unlike Scenario A - the underlying publish itself has not completed.

**Root Cause**

Bulk publish jobs can become stuck when the processing service encounters an error that leaves the job in a partial state without transitioning to ‘failed’. The Cancel option only appears for actively queued jobs.

**Resolution**

1.  Use the Retry Jobs API to attempt to clear or retry the stuck job: POST /v3/bulk/jobs/{job\_id}/retry.
    
2.  If the Retry API does not resolve the state, contact Contentstack Support with the stuck job ID and stack API key. Engineering can force-transition the job to a failed state.
    
3.  After the job state is cleared, retry the bulk publish operation.
    

After clearing the stuck job, confirm new bulk publish operations complete correctly.

### Localized Entry Release Version Mismatch - Single Locale Selection Sets Version for All

When adding a localized entry to a Release, selecting a single locale version (with a lower version number) and then adding other locales causes all selected locales to inherit the version of the initially selected locale. This results in older content versions being included in the Release for some locales.

**Root Cause**

The Release item addition logic uses the version of the first selected locale as the version reference when multiple locales are added together in certain selection sequences. When all locales are selected simultaneously (multi-select), each locale correctly retains its own latest version. However, when a single locale is selected first and then other locales are added, the version of the initial selection is applied to all.

**Resolution**

1.  When adding localized entries to a Release, select all locales simultaneously (multi-select) in a single operation rather than selecting one locale first and then adding others.
    
2.  After adding entries to a Release, review the Release items list to verify each locale shows the expected (latest) version number before deploying.
    
3.  If incorrect versions were already added, remove the affected entries from the Release and re-add them using the multi-select approach.
    

After using multi-select for locale addition, verify in the Release items list that each locale shows its own correct latest version number, not the version of the initially selected locale.

### Publish Rules Only Apply to Unpublished Entries

Publish rules configured for a production environment are not enforced when an editor re-publishes an entry that was already published at a previous workflow stage. The re-publish bypasses the configured restrictions.

**Root Cause**

Publish rules in Contentstack apply only when an entry is being published for the first time (moving from an unpublished state). If an entry is already published and an editor simply changes the workflow stage and re-publishes the same version, the publish rules do not re-evaluate - the entry is treated as an update to an already-live item, not a new publish action.

**Resolution**

This is expected behavior. To enforce rules on every publish action:

1.  Configure workflows so that publishing to production always requires a version increment (new save before publish).
    
2.  Use Releases as a controlled publishing channel, which enforces a structured approval and deployment process.
    
3.  Educate editors on the distinction between new publishes (rule-enforced) and re-publishes of existing versions (not rule-enforced).
    

For use cases that require rules on every publish action regardless of prior state, submit an enhancement request through Contentstack Support.

### Scheduled Publish Not Consistently Including Referenced Entries

When a parent entry is scheduled for future publication, the referenced child entries do not consistently publish at the scheduled time. The parent publishes but referenced entries may remain at their previous state.

**Root Cause**

Scheduling a parent entry does not automatically include referenced entries in the same scheduled publish job unless they are explicitly added. When referenced entries are not included, they remain at their current published version when the parent publishes.

**Resolution**

1.  When scheduling the parent entry, include all referenced entries in the same scheduled publish job.
    
2.  In the CMS UI, use the Publish with References option during scheduling to automatically include referenced entries.
    
3.  For the most reliable approach, schedule the referenced entries first (a few minutes earlier), then schedule the parent entry. This guarantees referenced entries are live before the parent publishes.
    
4.  Use Releases to group parent and referenced entries together and schedule the release deployment as an atomic operation.
    

After scheduling both the referenced entries and parent entry (referenced first), verify at the scheduled time that all entries are published with the correct versions.

### Multiple Versions of the Same Entry Scheduled for the Same Time

Versions 10, 11, and 12 of the same entry are all scheduled to publish at the same time. Inconsistent ordering is observed during testing and it is unclear which version will be live.

**Root Cause**

When multiple versions of the same entry are scheduled for an identical timestamp, the publish jobs execute in parallel. Parallel execution is non-deterministic - there is no guaranteed ordering. Whichever job completes last will be the version that appears live.

**Resolution**

1.  Before scheduling a new version, cancel all previously scheduled publishes for the same entry.
    
2.  Schedule only the intended latest version for the target time.
    
3.  To cancel existing scheduled publishes, navigate to the entry and remove any pending schedule from the scheduled publish panel.
    

After canceling previous schedules and scheduling only the intended version, verify that the correct version goes live at the scheduled time.

### ‘Published Before Localization’ Warning in Entry Publish Status

A warning reading ‘Published before localization’ appears under the entry’s publish status tab, even though the entry has been published to multiple environments. The warning remains despite subsequent published actions.

**Root Cause**

The warning appears when the entry has been published to an environment before it was ever localized for a newly added language. Until the entry is explicitly opened and saved in that locale - which creates the localized version - the warning persists. Publishing from the master locale does not resolve the warning for the new locale.

**Resolution**

1.  Open the affected entry in the CMS.
    
2.  Switch to the locale that shows the ‘Published before localization’ warning.
    
3.  Open and save the entry in that locale (even without making changes). This creates the localized version and clears the warning.
    
4.  If the locale should continue to inherit from the master locale rather than having its own localized version, the warning will reappear after the next master locale publish. This is expected behavior for master-only entries.
    

After saving the entry in the affected locale, check the publish status tab. If the ‘Published before localization’ warning is gone, the entry is now correctly localized.

### Workflow Status Mismatch Between Entry View and Entry List

An entry shows a status of ‘Approved’ when opened individually in the editor and across all locales, but the entry list still shows it as ‘Review’. The discrepancy causes confusion about whether the entry is ready to publish.

**Root Cause**

The entry list UI may not immediately reflect localized workflow stage updates. The backend workflow state is correctly updated, and publishing will proceed without issues based on the actual workflow state - not the stale list view.

**Resolution**

This is a known UI refresh lag in the entry list. To resolve:

1.  Refresh the entry list page to force the UI to reload the latest workflow states.
    
2.  Publishing can proceed safely - the backend workflow state (visible in the entry editor) is the authoritative state.
    

After refreshing the entry list, confirm the workflow status shown matches the status visible within the entry editor.

### URL Prefix Only Applies to Newly Created Entries

A URL prefix is configured in the content type’s URL field settings (for example, /insights-hub/). The prefix works for newly created entries but does not update existing entries that already have URLs.

**Root Cause**

URL prefix configuration applies to entries created after the prefix is configured. Existing entries retain their previously generated URL and are not automatically updated when the prefix is changed. This is by design to prevent unintended URL changes to live content.

**Resolution**

1.  For existing entries, manually update the URL field in each entry to include the new prefix.
    
2.  For large volumes of existing entries, use a CMA script to fetch all entries, update the URL field programmatically, and push the updates back.
    
3.  Going forward, all new entries created after the prefix was configured will automatically receive the prefix.
    

After updating existing entry URLs, verify that all entries (old and new) have the correct prefix by checking their URL fields.

### Publish Status Showing ‘Not Published’ Despite Successful Publish Queue

After publishing an entry, the Publish Status in the entry list and editor continues to display ‘Not published’ for an unusually long time. Additional publish attempts during this window are ignored. Other users are also affected.

**Root Cause**

In the reported case, the entry was published successfully and was visible on the live site, but the Publish Status indicator continued to show ‘Not published’ for an extended period before self-resolving with no corrective action applied. No specific cause was confirmed. This is a known, self-resolving symptom pattern - the entry is correctly published on the backend, and the delay appears to be in the status display rather than the publish action itself.

**Resolution**

1.  Wait briefly and refresh the page - the status will update once the asynchronous propagation completes.
    
2.  Do not submit additional publish attempts during the delay window. Multiple re-publishes of the same entry are queued but the delay is in the status display, not the publish action itself.
    
3.  If the status does not update after 10–15 minutes, contact Contentstack Support with the entry UID, stack, environment, and timestamp of the publish action for investigation.
    

After refreshing the page following a short wait, confirm the Publish Status updates to reflect the correct published state.

### Users Receiving Unexpected Publish Approval Emails

A user receives an email requesting them to grant permission or approve a publish action, but the email was not intended for them. They want to understand why they are receiving these notifications.

**Root Cause**

Publish approval emails are sent to all users listed as approvers in the publish rule for the relevant content type and environment. If a user’s email was added to the approvers list - intentionally or by mistake - they will receive approval request emails for every publish action that triggers that rule, even if they are not actively involved in the workflow.

**Resolution**

1.  Contact the stack Owner or Admin and ask them to review the publish rule configuration in Settings > Workflows.
    
2.  Locate the publish rule sending the approval emails and review the list of configured approvers.
    
3.  Remove any incorrectly added email addresses from the approvers list.
    
4.  Save the updated publish rule.
    

After updating the approvers list, confirm the affected user no longer receives publish approval emails for that rule.

### Environment Renaming - Safe for Tokens but Requires Code Updates

A team wants to rename the ‘dev’ environment to ‘preview’. They are concerned this will invalidate API tokens or break existing configurations.

**Root Cause**

Renaming an environment in the UI does not affect delivery tokens, management tokens, or API keys - these reference the environment by its internal identifier, not its display name. However, anywhere the environment name is referenced as a string in application code, SDK configurations, or tooling (such as deploy scripts, environment variables, or content queries), those references must be updated manually.

**Resolution**

1.  Rename the environment in Settings > Environments - this will not break existing tokens.
    
2.  Update any hardcoded environment name references in application code, SDK initialization, and CI/CD pipelines from ‘dev’ to ‘preview’.
    
3.  Update environment variables on all hosting platforms (for example, Vercel, Netlify) that reference the environment name.
    
4.  Test API calls after renaming to confirm content delivery is working with the updated environment name.
    

After renaming and updating all code references, confirm that the application fetches and publishes content correctly using the renamed environment.

### Production Site Showing Content from a Different Branch (Branch Token Isolation)

The production website intermittently displays content from a non-production branch (for example, an acceptance or staging branch). The issue occurs despite the production application always querying using branch: main.

**Root Cause**

Branch isolation in Contentstack CDN works as designed - CDN caching cannot mix branch data. The root cause in this scenario is that both production and acceptance environments are using the same delivery token, which is not restricted to a specific branch. Without branch-scoped tokens, a single token can return content from any branch, and CDN cache entries may be served across environments if the same token and URL structure is shared.

**Resolution**

1.  Create separate, branch-restricted delivery tokens for each environment: a Production token restricted to branch: main, and an Acceptance token restricted to branch: acceptance (or equivalent).
    
2.  Update the production application to use only the production-scoped delivery token.
    
3.  Update the acceptance application to use only the acceptance-scoped token.
    
4.  Ensure no shared tokens are used across production and non-production environments.
    

After implementing branch-restricted tokens, verify by querying the production endpoint - only content from the main branch should be returned, regardless of cache state.

### Entry in a Release Not Updated After Release Publish - Already Published Entry Skipped

After publishing a release, one entry does not update its publish status in the target environment, even though all other entries in the release are published correctly.

**Root Cause**

If an entry included in a release is already published at the same version in the target environment, the release publish process skips it because no change is detected. The entry is considered already up to date and is not re-published. This can cause confusion when the intent is to force a re-publish regardless of the current state.

**Resolution**

1.  Check the publish queue in the CMS to confirm the status of the skipped entry and verify the reason it was not updated.
    
2.  If the entry needs to be re-published regardless, open the entry, make a minor save (even without content changes to create a new version), include the new version in the release, and publish again.
    
3.  Alternatively, publish the entry directly from the entry editor outside of the release to force a refresh.
    

After re-publishing the entry (either through the release with a new version or directly), confirm the entry’s publish status in the target environment reflects the latest version.

### Scheduled Publishing Not Triggering - Job Scheduler Service Hang

Scheduled publishing stops working across an organization. Both single and bulk scheduled publishers fail to trigger at their configured time.

**Root Cause**

This is a platform-level incident. The job scheduler service can become stuck due to a service hang in the pod, preventing all queued messages from being processed across multiple organizations in the affected region.

**Resolution**

1.  Check the Contentstack Status Page (status.contentstack.com) to confirm whether an incident has been identified.
    
2.  Contact Contentstack Support immediately, providing the affected stack details, region, and estimated start time.
    
3.  Engineering will identify and restart the stuck scheduler pod.
    
4.  After the fix, verify that past-due scheduled jobs are processed or re-schedule them manually.
    

After the scheduler service is restored, confirm that newly scheduled publish jobs trigger at the correct time.

### Unschedule Request Failing With ‘job_id is Required’

Attempting to cancel a scheduled publish via the Unschedule API returns ‘job\_id is required’. The scheduled publish exists but cannot be canceled.

**Root Cause**

The scheduled job was created without a job\_id reference because the nestedSinglePublishing feature flag is not enabled. Without this flag, the scheduling system does not properly associate job IDs with individual publish actions.

**Resolution**

1.  Contact Contentstack Support and request enablement of the nestedSinglePublishing feature flag for the affected stack.
    
2.  After the flag is enabled, retry the unschedule operation. New scheduled jobs created after enablement will correctly receive job IDs.
    

After enabling nestedSinglePublishing, confirm that new scheduled releases can be successfully canceled using the Unschedule API.

### Third-Level Nested References Not Published - Intermediate Entry Skipped

Publishing a parent entry with references does not publish third-level nested entries. The intermediate second-level entry is already published and skipped, which also skips its references.

**Root Cause**

‘Publish with References’ skips already-published entries. When the intermediate entry is skipped, the system does not recurse into its references, leaving third-level entries unpublished.

**Resolution**

1.  For deep nesting (3+ levels), publish from the deepest level upward: publish third-level entries first, then intermediate entries, then the top-level parent.
    
2.  Use a Release to group all entries at all levels for a coordinated single deployment.
    
3.  For automation, use the CMA bulk publish endpoint with the complete list of entry UIDs across all levels.
    

After publishing from the deepest level upward, verifying the parent entry resolves all reference data correctly in the CDA response.

### Publishing Fails Due to Mandatory JSON RTE Field Left Blank

Publishing an entry fails with a missing mandatory field error. All visible fields appear populated but the error persists.

**Root Cause**

A JSON RTE field is mandatory in the schema but appears empty in the entry. Common causes: the field was added as mandatory after the entry was created; the field is inside a modular block that was not scrolled to; or the field was cleared during editing.

**Resolution**

1.  Open the browser developer tools and attempt the publish to see the specific field UID in the 422 error response.
    
2.  Use browser search or manually scroll through all fields and modular blocks to locate the flagged JSON RTE field.
    
3.  Add at least minimal placeholder content to the mandatory JSON RTE field, or mark the field as non-mandatory if it should be optional.
    

After filling the mandatory JSON RTE field, confirm the entry is published successfully to all target environments.

### Scheduled Publish for Variant Shows ‘Publish Failed’ in UI Despite Queue Success

A scheduled publish job for a variant entry shows as completed in the Publish Queue, but the entry UI shows ‘publish failed’. The content appears correctly on the live environment.

**Root Cause**

This is a status synchronization issue. The Publish Queue correctly tracks the job lifecycle, but the entry-level variant publish status display has a UI-side lag - it does not correctly receive the completed status update. The actual publish succeeded.

**Resolution**

1.  Verify the actual publish outcome by querying the CDA for the variant - if the correct content is served, the publish was successful.
    
2.  Contact Contentstack Support with the variant entry UID, scheduled job ID, and stack details for investigation.
    

After the platform fix, schedule a test variant publish and confirm the UI status badge correctly reflects the queue’s completed state.

### Publishing Status Takes 15+ Seconds to Load on High-Volume Stacks

The Publish Status panel and version history take 15+ seconds to load for stacks with many environments (15+) and languages (14+).

**Root Cause**

The new Publish Status and Version History interface fetches status data for all environments and languages simultaneously. For stacks with many combinations, this generates a large number of parallel queries causing significant latency.

**Resolution**

1.  Contact Contentstack Support and request enablement of the ‘disablePublishStatusV2’ configuration key for the affected organization.
    
2.  This reverts the organization to the legacy Publish Status interface which uses a faster data loading pattern.
    

After the key is enabled, reload an entry with many locales and environments and confirm the Publish Status panel loads within a normal timeframe.

### Published Entry Not Reflecting on Live Site - Old Version Persisting

A team publishes an updated version of an entry (for example, V6) but the live site continues to serve the old version (V5). The publish operation shows as successful in the UI and the release includes the correct version, but the content does not change on the frontend.

**Root Cause**

This can occur when the entry’s internal state has a discrepancy between the saved version and the version being pushed to the delivery layer. The publish appears to succeed because the entry exists and meets schema validation, but the delivery layer does not register a meaningful change from its current state.

**Resolution**

1.  Re-save the entry to create a new version (even without making content changes) - open the entry, click Save, and confirm a new version number is created.
    
2.  Publish the newly created version.
    
3.  If the entry was published via a Release, confirm the new version is included in the Release items - older versions in a Release are not automatically replaced when a new version is saved.
    
4.  After publishing the new version, add a cache-busting query parameter to the live URL to confirm the new content is being served: append ?cb=timestamp to force a fresh CDN fetch.
    

After re-saving and republishing, verify the live site serves the updated content version.

### Publish Fails With ‘Required Fields Missing’ Despite All Fields Appearing Populated

Publishing an entry returns an error suggesting required fields are missing. The team reviews all fields in the entry editor but cannot identify any empty mandatory fields. The issue persists across multiple publish attempts.

**Root Cause**

The most common cause is a JSON RTE field containing invalid content that is not visible to editors. For example, a space character in an invalid position within the JSON RTE’s internal data structure causes the API’s publish validation to fail with a required-field-style error, even though the field appears populated in the editor. This can happen after content is pasted from an external source or generated by a translation integration.

**Resolution**

1.  Open the browser developer tools and inspect the network response for the failed publish API call. The 422 response body will specify the exact field UID and the nature of the validation failure.
    
2.  For JSON RTE fields flagged in the error: open the affected field and re-enter the content from scratch, or switch to HTML view and remove any invisible characters or malformed markup.
    
3.  Export the entry JSON via the CMA: GET /v3/content\_types/{uid}/entries/{entry\_uid} and inspect the JSON RTE field’s data structure for unexpected characters, null values, or invalid nesting.
    
4.  If the invalid content was introduced by a translation service, work with the integration provider to ensure their output conforms to the Contentstack JSON RTE schema.
    

After correcting or re-entering the JSON RTE content, retry publishing. If the entry publishes successfully, the invalid content was the cause.

### Publish and Unpublish Buttons Persist After Role Permission Change - Entry Editor Not Auto-Refreshing

After a user’s role permissions are updated (for example, removing publish access), the Publish and Unpublish buttons remain visible in the entry editor for that user without a page refresh. The user can see buttons that suggest they have permissions they no longer hold.

**Root Cause**

The entry editor UI does not automatically refresh its permission state after role changes are applied. The buttons displayed in the editor reflect the permissions loaded when the page was last loaded - not the current server-side permission state. This is expected behavior. The display is cosmetic only: server-side validation is always applied when a publish or unpublish action is actually attempted.

**Resolution**

This is expected behavior and not a security issue. The actual permission check is always performed server-side when the publish/unpublish action is triggered. The visible buttons are cached from the last page load.

1.  To update the button state immediately: ask the affected user to reload the entry page. The buttons will reflect the current role permissions after reload.
    
2.  Communicate to editors that button visibility may lag behind role changes and a page reload is needed to see the updated state.
    

After reloading the entry page, confirm the Publish and Unpublish buttons are no longer visible for the user whose permissions were revoked.

<!-- case:00060730 status:draft synced:false bucket:"Publishing, Releases, Environments and Operations" -->
### Release Shows Successful Deployment but Content Reverts

Deploying a Release may show a successful status while the published content fails to reach the target environment, with the content reverting after redeployment.

**Root Cause**

The root cause was identified as two teams editing and publishing the same entries at the same time, producing conflicting data that caused the apparent revert after deployment.

**Resolution**

1.  Check whether multiple teams or users published changes to the same entries at or near the same time as the Release deployment.

2.  Coordinate publishing so that only one team edits and publishes a given set of entries within the same Release window.

3.  Redeploy the Release after confirming no conflicting edits are in progress.

After coordinating publishing and redeploying the Release, confirm the target environment reflects the expected content without reverting. If the content persists as published, the issue is resolved. Escalate with the Release name and the affected entry UIDs if the content continues to revert.

<!-- end:00060730 -->

## API Delivery, GraphQL & Assets

### Referenced Entries Not Included in CDA Response

Referenced entry fields or names do not appear in the Content Delivery API (CDA) response when fetching entries.

**Root Cause**

The Delivery API does not automatically expand reference fields. Referenced entries must be explicitly included using the appropriate inclusion parameters.

Common causes include:

*   Missing include\[\] parameter in REST (CDA) requests
*   Missing nested reference selection in GraphQL queries
*   Referenced entries not published in the requested environment
*   Locale mismatch between the parent and referenced entry

If inclusion is not configured correctly, only the reference UID is returned.

**Resolution**

For REST (CDA):

*   Use the include\[\] parameter to expand referenced fields.
*   Specify include\_depth if nested references are required.

For GraphQL:

*   Explicitly query nested reference fields in the selection set.

Additionally:

*   Confirm referenced entries are published.
*   Verify environment and locale alignment.

Re-run the request with proper inclusion parameters and confirm that referenced entry fields are expanded in the API response.

### Missing referenced entry details in API responses

Retrieving content via the API may return incomplete data for referenced entries even when include parameters are used. This prevents developers from accessing nested or linked content within a single request.

**Root Cause**

The include\_all configuration is not enabled for the specific stack, limiting the ability to retrieve all referenced details.

**Resolution**

1.  Enable the include\_all feature for the stack settings to allow full reference retrieval.
2.  Ensure the API request parameters explicitly specify the references to be included.

After the include\_all feature is enabled, execute the API request for an entry with references. If the JSON response contains the full details of the referenced entries, the feature is active.

### Asset Metadata (Dimensions) Missing in API Response

Image width and height values are not included in the Delivery API response, even though they appear in the UI.

**Root Cause**

The Delivery API does not return asset dimensions by default to optimize response size. The include\_dimension=true query parameter must be explicitly provided.

**Resolution**

*   Add include\_dimension=true to the Delivery API request.
*   Re-fetch the entry or asset.

The API response includes width and height under the asset metadata.

### CDA 422 Error Due to Reference Resolution Limit (100)

A Delivery API request fails with a 422 Unprocessable Entity error indicating that the number of resolved references exceeds the allowed limit.

**Root Cause**

The Content Delivery API enforces a strict maximum of 100 resolved references per request, including nested references. When the total number of expanded references exceeds this limit, the API returns a 422 validation error.

This commonly occurs when:

*   Using include\_all=true
*   Using high include\_depth values
*   Querying entries with deeply nested reference structures

**Resolution**

*   Reduce include\_depth where possible.
*   Avoid include\_all unless necessary.
*   Split large requests into multiple smaller requests.
*   Merge results client-side if needed.

After reducing reference expansion, the API request completes successfully without triggering the 422 error.

### Missing fields in REST API entry response

Retrieving content via the REST API may return incomplete data when querying an older version of an entry. This prevents viewing fields like overview or table\_of\_contents that are visible in the Entry UI.

**Root Cause**

The requested entry version does not contain the specific fields added in later versions of the content.

**Resolution**

1.  Verify the version number of the entry being requested in the API call.
2.  Query the latest version of the entry to ensure all fields are included in the response.
3.  Compare the API output against the Entry UI to identify version discrepancies.

After updating the API request to target the latest version, execute the GET request. If the missing fields appear in the response, the content is correctly synchronized.

### Missing tags in Delivery API locale responses

Querying entry data for specific locales via the Delivery API may result in missing tag fields. This prevents localized content from displaying tags that have been added to the latest version of the entry.

**Root Cause**

The API request is targeting an older version of the entry that was saved before the tags or fields were implemented.

**Resolution**

1.  Navigate to the Entry UI and verify the latest version number for the affected locale.
2.  Update the Delivery API query parameters to target the latest version of the entry.
3.  Ensure the fields exist in the specific version being requested.

After adjusting the query to the latest version, perform a new API call for the affected locale. If the tags appear in the JSON response, the data discrepancy is resolved.

### GraphQL returns master content despite fallback_locale being disabled

Querying entries via GraphQL may return master locale content even if the fallback\_locale parameter is set to false. This prevents users from receiving an empty response or error when content does not exist in the requested locale.

**Root Cause**

The entry exists and is published in the master locale but has not been localized for the specific language being requested in the query.

**Resolution**

1.  Localize the entry for the specific target language within the CMS.
2.  Publish the localized version of the entry to the desired environment.
3.  Ensure the query targets the correct locale where the localized content resides.

After localizing and publishing the entry, execute the GraphQL query again with fallback\_locale: false. If the localized content appears instead of the master locale data, the configuration is correct.

### Resolving slow stack performance caused by large assets

Managing entries in the stack may experience significant delays and slow response times when the stack contains very large assets. This prevents efficient content management and increases API response latency.

**Root Cause**

Extremely large asset sizes, ranging from 100MB to 1.5GB, are causing high response times during delivery operations.

**Resolution**

1.  Review CDA logs to identify specific assets causing high latency.
2.  Reduce the file size of assets currently stored in the stack.
3.  Implement caching strategies to decrease the load on the origin server.

After optimizing asset sizes and implementing caching, monitor the stack response times in the logs. If the response times return to normal operating levels, the performance bottleneck is cleared.

### RESPONSE_SIZE_TOO_BIG - GraphQL Response Exceeds 7MB Limit

The GraphQL Explorer or API returns the following error even though the query appears to request a reasonable amount of data:

{ “error”: { “message”: “Response size was too big. Maximum response size allowed is 7MB”, “code”: “RESPONSE\_SIZE\_TOO\_BIG”, “hint”: “Try making smaller queries or reduce the response size by using ‘limit’ arguments.” } }

**Root Cause**

Contentstack enforces a 7MB maximum on GraphQL response payloads. This limit exists to protect platform performance. The limit is evaluated against the full serialized JSON response - including all resolved references, nested fields, and asset metadata. Queries that request many entries with deeply nested references or large text fields commonly exceed this threshold even when the individual entry count appears small. The API returns an HTTP 503 status code along with the RESPONSE\_SIZE\_TOO\_BIG error code when this limit is exceeded.

**Resolution**

1.  Add a limit argument to the top-level query to reduce the number of entries returned per request. For example: allBlogPost(limit: 10)
    
2.  Remove fields from the selection set that are not strictly needed for the use case, especially deeply nested reference chains and large Rich Text fields.
    
3.  Split a single large query into multiple smaller queries, each targeting a subset of the content.
    
4.  Use pagination - combine limit with skip to page through results incrementally rather than fetching all entries in one request.
    
5.  For asset-heavy queries, consider fetching asset UIDs only and resolving asset metadata in separate calls.
    

After reducing the query scope, re-run it in the GraphQL Explorer. If the RESPONSE\_SIZE\_TOO\_BIG error no longer appears and results are returned, the response is now within the 7MB limit.

### GraphQL Returns 400 Errors Across Multiple Regions With No Configuration Change

GraphQL Delivery API requests begin returning unexpected HTTP 400 status code errors in production. The issue affects multiple regions simultaneously (for example, both US and EU). No changes were made on the customer side before the errors began.

**Root Cause**

When 400 errors appear simultaneously across multiple regions without any customer-side configuration change, the root cause is typically a platform-level infrastructure issue - such as a misconfiguration in the GraphQL service, a deployment that introduced a regression, or a DNS/routing issue. This is not caused by the query structure or the delivery token, and it resolves after Contentstack engineering performs a rollback or applies a platform-level fix.

**Resolution**

1.  Confirm the error is not caused by a recent query change or token expiry by testing with a simple known-good query (for example, fetching a single entry with minimal fields).
    
2.  Check the Contentstack Status Page (status.contentstack.com) for any active incidents affecting the GraphQL API.
    
3.  If no active incident is listed but the error persists across regions, contact Contentstack Support immediately with: the affected stack API key, the regions where the error is observed, the approximate start time, and a sample failing request.
    
4.  Engineering will investigate the platform-level cause and apply a fix. No configuration change is required on the customer side.
    

After the engineering fix is applied, re-test the previously failing GraphQL request. If it returns a valid response, the platform-level issue has been resolved.

### GraphQL Latency Spikes - Response Times Rising to Multiple Seconds

GraphQL API response times increase from milliseconds to several seconds with no changes to the query, stack configuration, or network setup. The latency spike is consistent and observed via monitoring probes across multiple requests.

**Root Cause**

Sudden, unexplained latency spikes in the GraphQL endpoint (graphql.contentstack.com) without any customer-side change indicate a platform-level issue, such as resource contention on shared infrastructure, CDN routing instability, or degraded performance in the GraphQL processing layer. These incidents are identified and resolved by Contentstack’s engineering and infrastructure teams.

**Resolution**

1.  Check the Contentstack Status Page (status.contentstack.com) for any active performance incidents.
    
2.  If no incident is listed but latency remains elevated, contact Contentstack Support and provide: the affected endpoint, the regions experiencing latency, the approximate start time of the increase, and monitoring probe data or response time samples.
    
3.  No configuration changes are required on the customer side for platform-level latency incidents.
    
4.  As a temporary measure during a latency spike, implement timeout handling and retry logic in the application so that individual slow responses do not cause cascading failures.
    

After Contentstack resolves the underlying infrastructure issue, response times will return to normal. Confirm by testing a standard query and verifying the response time is within the expected range.

### Path Field Returns null for Specific Entries - Not All Entries in the Same Content Type

The GraphQL API returns the path field as null (or omits it entirely) for certain entries within a content type, while the same field is correctly populated and returned for other entries of the same type. There is no obvious difference in how the affected entries were created.

**Root Cause**

This issue is caused by a data inconsistency at the entry level - the path field data for specific entries was not correctly persisted or indexed in the delivery layer. This is not a schema issue or a query issue; the field is defined correctly in the content type. The inconsistency affects only specific entry UIDs and requires a backend data fix applied by the Contentstack CDA team.

**Resolution**

1.  Identify the affected entry UIDs by querying the GraphQL API and comparing the results - entries where path is null while other entries of the same type return a value.
    
2.  Contact Contentstack Support and provide the affected entry UIDs and the stack API key.
    
3.  The CDA team will investigate the data inconsistency for the affected entries and apply the appropriate backend fix.
    
4.  After the fix is applied, re-query the affected entries and confirm the path field is now returned correctly.
    

This issue does not require content republishing or configuration changes. After the backend fix is confirmed by Support, verify by fetching the affected entries and checking the path field value.

### Modular Block UID Not Available in GraphQL Schema

The REST Delivery API returns a uid field for modular block instances within an entry, but the same uid is not available when querying via the GraphQL API. Teams relying on the block UID for client-side rendering or block identification cannot retrieve it through GraphQL.

**Root Cause**

The UID associated with modular block instances is an internal identifier used by the Contentstack platform for block positioning and management purposes. Because this identifier is not part of the content type schema, it is intentionally not exposed in the GraphQL schema. The GraphQL API only surfaces fields that are defined in the content type schema. REST returns this field as an implementation detail of the JSON structure, but GraphQL enforces strict schema compliance.

**Resolution**

This is expected behavior by design. The modular block instance UID is not available via GraphQL and cannot be queried through the schema.

1.  If client-side block identification is required, add a dedicated identifier field (for example, a text or short uid field) to the modular block definition in the content type schema. Populate this field in entries to provide a stable, schema-defined identifier accessible via both REST and GraphQL.
    
2.  If the internal block UID is essential for the use case, use the REST Delivery API instead of GraphQL for queries that require this field.
    

After adding a schema-defined identifier field to the modular block, verify it is accessible in the GraphQL Explorer and returned correctly in the query response.

### Content Type with Numeric-Only Name Fails GraphQL Queries

Querying a content type through GraphQL fails when the content type UID or name consists entirely of numeric characters. The query does not return results, and an error is returned from the GraphQL endpoint.

**Root Cause**

GraphQL enforces strict naming conventions for schema types. Type names must begin with a letter or underscore (\[\_a-zA-Z\]) and cannot start with or consist solely of numeric characters. When a content type is named with only numbers, it violates GraphQL’s schema naming rules and cannot be represented as a valid type in the generated schema.

**Resolution**

1.  Navigate to the Content Type settings in the CMS.
    
2.  Rename the content type UID and display name to a value that begins with a letter or underscore.
    
3.  Save the updated content type.
    
4.  Retry the GraphQL query using the updated content type name.
    

After renaming the content type, execute the GraphQL query again. If the query returns results without a naming error, the content type name is now schema-compliant.

### GraphQL Schema Error: Names Must Start with [_a-zA-Z]

GraphQL queries fail with an error message such as: “Names must start with \[\_a-zA-Z\] but ‘03VisaPanel’ does not.” This error prevents the field or content type from being included in the GraphQL schema.

**Root Cause**

GraphQL schema generation enforces that all type and field names conform to the identifier naming standard: they must begin with a letter (a–z, A–Z) or underscore (\_). Field UIDs or content type identifiers that begin with a number or contain special characters violate this convention and cause schema build failures.

**Resolution**

1.  Identify the field UID or content type name referenced in the error message.
    
2.  Rename the field UID or content type to begin with a letter or underscore. For example, rename “03VisaPanel” to “visa\_panel\_03” or “visaPanel03”.
    
3.  Save the content type and allow the GraphQL schema to regenerate.
    
4.  Re-run the query in the GraphQL Explorer or API client.
    

After renaming, confirm the schema no longer includes the naming error and the content type or field is accessible via GraphQL.

### SCHEMA_BUILD_ERROR Caused by Field UID Conflicts with Internal GraphQL Types

The GraphQL Explorer displays SCHEMA\_BUILD\_ERROR messages when running queries. The error is tied to a specific content type or field UID that conflicts with a reserved or internally generated GraphQL type name.

**Root Cause**

Contentstack auto-generates GraphQL types based on content type and field UIDs. When a UID such as link\_Where is used, it collides with system-internal GraphQL type names (for example, types used for where-clause filtering). This collision causes the schema build to fail.

**Resolution**

1.  Identify the content type or field UID mentioned in the SCHEMA\_BUILD\_ERROR.
    
2.  Rename the conflicting UID to avoid collision with system-internal GraphQL types. Examples of safe alternatives: change “link\_Where” to “custom\_link” or “my\_link\_type”.
    
3.  Save the content type and allow the schema to regenerate.
    
4.  Reload the GraphQL Explorer and confirm the SCHEMA\_BUILD\_ERROR is no longer present.
    

After renaming the field or content type UID, open the GraphQL Explorer. If queries execute without a SCHEMA\_BUILD\_ERROR, the conflict has been resolved.

### Global Fields Not Appearing in GraphQL Explorer or Schema Introspection

Global fields configured in the CMS do not appear in the GraphQL Explorer schema or are not returned during schema introspection. Developers cannot query global field data via GraphQL despite the fields being visible in the CMS.

**Root Cause**

Global fields may temporarily not appear in the GraphQL schema due to a schema cache that has not yet refreshed, or because the global field has not been fully propagated to the GraphQL layer. In most cases the fields are present in the schema and become visible after a short propagation delay or page refresh.

**Resolution**

1.  Wait briefly and refresh the GraphQL Explorer to allow schema propagation to complete.
    
2.  Re-run the schema introspection query to confirm whether the global fields are now present.
    
3.  If fields remain missing, verify the global field is correctly referenced within a content type in the CMS.
    
4.  If the issue persists, contact Contentstack Support and request internal schema validation for the affected stack.
    

After refreshing the GraphQL Explorer, run an introspection query. If global fields appear in the returned schema, the propagation has completed successfully.

### Expected all_author Field Not Found in GraphQL Schema

The GraphQL schema documentation references an all\_author field, but the field cannot be found or queried in the target stack’s GraphQL environment. Queries using all\_author return an error or produce no results.

**Root Cause**

GraphQL schema types are generated dynamically based on content types present in the stack. The all\_author field is only generated if a content type with the UID “author” exists in the stack. If no such content type exists, the corresponding GraphQL type and field are not created.

**Resolution**

1.  Verify whether a content type with the UID “author” exists in the stack.
    
2.  If the content type does not exist, create it or confirm the correct UID of the content type intended for author data.
    
3.  Refresh the GraphQL Explorer to regenerate the schema after any content type changes.
    
4.  Re-run the query using the correct generated field name based on the actual content type UID.
    

After confirming or creating the content type with the correct UID, reload the GraphQL Explorer. If the corresponding field appears in the schema, the content type is correctly linked.

### GraphQL Error After Removing a Field from a Content Type

After removing a field from a content type, a GraphQL query that previously referenced that field now returns an error. The query fails even though the content type itself still exists.

**Root Cause**

When a field is removed from a content type, it is also removed from the GraphQL schema. Any existing query that references the removed field becomes invalid because the field no longer exists in the schema. This is expected GraphQL behavior - the schema is the source of truth for valid query fields.

**Resolution**

1.  Update the GraphQL query to remove the reference to the deleted field.
    
2.  If the field data is still required, restore the field in the content type via the CMS before re-running the query.
    
3.  Validate the updated query against the current schema using the GraphQL Explorer before deploying.
    

After updating the query, execute it in the GraphQL Explorer. If the query runs without errors, the field reference has been correctly removed or the schema has been restored.

### MAX_RESOLVER_COST_EXCEEDED Error in GraphQL Queries

GraphQL queries fail with a MAX\_RESOLVER\_COST\_EXCEEDED error even when the expected number of returned results is small. The platform rejects the query before execution based on estimated query cost.

**Root Cause**

Contentstack applies strict query cost limits to protect platform stability. These limits are evaluated based on worst-case expansion of the query, not actual returned data:

*   Maximum documents: 7,500
    
*   Maximum resolver cost: 20
    
*   Maximum reference depth: 3 levels
    

When a query structure theoretically could expand to exceed these limits - even if the actual dataset is small - the platform rejects it. Queries with multiple nested references, high include depth, or broad filters are most commonly affected.

**Resolution**

1.  Reduce the number of nested reference levels in the query to stay within the 3-level maximum.
    
2.  Break complex queries into multiple smaller queries targeting specific content types or fields.
    
3.  Avoid querying all fields across deeply nested structures in a single request.
    
4.  Use pagination (limit and skip) to reduce the theoretical document count per query.
    

After restructuring the query to reduce resolver cost and depth, re-run it in the GraphQL Explorer. If the query executes without a MAX\_RESOLVER\_COST\_EXCEEDED error, the query is within platform limits.

### MAX_DOCUMENT_LIMIT_EXCEEDED and Platform Limits Cannot Be Raised

GraphQL queries fail with a MAX\_DOCUMENT\_LIMIT\_EXCEEDED error. Requests to increase the default limit (7,500 documents) or the resolver cost cap beyond platform thresholds are not fulfilled.

**Root Cause**

Contentstack enforces fixed platform-level limits on GraphQL queries to ensure performance and stability across all customers. These limits are not configurable beyond predefined thresholds and cannot be raised on request:

*   Default document limit: 7,500
    
*   Default resolver cost cap: 20
    

Complex navigation structures, deeply nested content types, or queries that expand across many references commonly trigger these limits.

**Resolution**

1.  Restructure queries to fetch data in smaller, targeted chunks instead of one large query.
    
2.  Preprocess or flatten content structures where possible to reduce query depth and expansion.
    
3.  Use client-side aggregation to combine results from multiple smaller queries.
    
4.  Consider caching frequently accessed query results to reduce repeated large query execution.
    

After restructuring the queries, confirm that each individual request stays within the document and resolver cost limits. If queries complete without limit errors, the restructuring is effective.

### Enabling Deeper Nested Reference Filtering with gql_max_reference_depth

GraphQL queries that attempt to filter nested references beyond the default depth limit fail or return incomplete results. The default reference depth configuration does not support the level of nesting required by the query.

**Root Cause**

Contentstack’s GraphQL API has a default maximum reference depth limit. For use cases that require deeper nested reference filtering, the gql\_max\_reference\_depth configuration must be explicitly enabled for the organization by the Contentstack support or solutions team.

**Resolution**

1.  Contact Contentstack Support or your Solutions Architect and request that the gql\_max\_reference\_depth configuration be enabled for your organization.
    
2.  After enablement, update the GraphQL query to utilize deeper nested reference filtering.
    
3.  Verify behavior by running the updated query and confirming that nested references are returned correctly.
    

After the configuration is enabled, re-run the nested reference query. If the expected nested reference data is returned without errors, the depth configuration is active.

### GraphQL 422 Error Due to Invalid Branch Key in Requests

GraphQL API requests return a 422 Unprocessable Entity error. The requests appear structurally valid but are consistently rejected by the API.

**Root Cause**

A 422 error in this context is caused by invalid or non-existent branch keys included in the GraphQL request headers or query parameters. When the branch key referenced in the request does not match any existing branch in the stack, the API rejects the request with a 422 error.

**Resolution**

1.  Inspect the GraphQL request headers and query parameters to identify the branch key being sent.
    
2.  Verify that the branch key corresponds to an existing, active branch in the Contentstack stack.
    
3.  Correct or remove the invalid branch key from the request.
    
4.  Re-run the request and confirm that the 422 error no longer occurs.
    

After updating the branch key to a valid value, re-execute the GraphQL request. If the request completes with a 2xx response, the branch key is valid.

### Intermittent 520 Errors Caused by Host Header in GraphQL Requests

GraphQL requests intermittently return HTTP 520 errors. The errors occur specifically when the Host header is explicitly included in the request, while requests without the Host header succeed.

**Root Cause**

When the Host header is explicitly set in the GraphQL request, it interferes with Cloudflare’s routing logic. Cloudflare uses the Host header to determine the backend destination; a manually set or incorrect Host header causes misrouting at the CDN layer, resulting in 520 origin connection errors.

**Resolution**

1.  Remove the manually set Host header from the GraphQL request configuration.
    
2.  Allow the HTTP client to set the Host header automatically based on the request URL.
    
3.  If the Host header is required by the client’s network configuration, contact Contentstack Support. A backend fix can be implemented to bypass Cloudflare routing for the affected traffic pattern.
    

After removing the explicit Host header, re-run the GraphQL request. If responses are returned with a 2xx status code and the 520 errors no longer occur, the routing issue is resolved.

### WAF Blocking Large or Alias-Heavy GraphQL Queries with 404 DOWNSTREAM_SERVICE_ERROR

A GraphQL query consistently fails with a 404 DOWNSTREAM\_SERVICE\_ERROR in the production environment, while the same query works correctly in the GraphQL Explorer. The query is large, contains many aliases, or both.

**Root Cause**

A Web Application Firewall (WAF) rule on the customer’s domain is blocking large or alias-heavy GraphQL queries. WAF rules designed to prevent abuse may treat complex GraphQL query patterns as suspicious and block them before they reach the Contentstack origin, returning a 404 error.

**Resolution**

1.  Contact Contentstack Support and report the 404 DOWNSTREAM\_SERVICE\_ERROR along with a sample of the failing query.
    
2.  Support will review WAF configuration for the affected domain and update the rules to allow valid complex GraphQL queries.
    
3.  As a temporary measure, reduce query complexity by splitting large queries or removing aliases where possible.
    
4.  After the WAF configuration is updated, re-run the original query and confirm it succeeds.
    

After the WAF rules are adjusted, execute the affected query in the production environment. If the query completes without a DOWNSTREAM\_SERVICE\_ERROR, the WAF is no longer blocking the request.

### Application Fails After GraphQL Request Due to Client-Side Firewall

An application fails or returns unexpected errors after sending a GraphQL request to Contentstack. The Contentstack API itself is functioning correctly and no errors appear on the platform side.

**Root Cause**

The failure originates on the client side, not Contentstack. A corporate or network-level firewall is blocking outbound requests to the Contentstack GraphQL endpoint or blocking the response from being received by the application.

**Resolution**

1.  Test the GraphQL request directly from a tool such as Postman or cURL to confirm the Contentstack API is responding correctly.
    
2.  If the direct test succeeds but the application fails, investigate the network and firewall configuration of the environment where the application is running.
    
3.  Work with the network team to allow outbound HTTPS traffic to Contentstack GraphQL endpoints.
    
4.  Confirm no proxy or VPN is intercepting and blocking the GraphQL traffic.
    

After adjusting the firewall configuration, retry the request from the application. If the application receives a valid GraphQL response, the network restriction has been resolved.

### GraphQL SSL Error: Unable to Get Local Issuer Certificate

GraphQL API requests fail with an SSL error: “unable to get local issuer certificate.” The error occurs on the client side and prevents any successful connection to the Contentstack GraphQL endpoint.

**Root Cause**

This error is client-side and is not caused by a change on Contentstack’s infrastructure. Common causes include:

*   A corporate proxy that intercepts HTTPS traffic and presents its own certificate, which the client does not trust
    
*   An outdated version of Node.js or the HTTP client library with an incomplete or outdated CA certificate bundle
    
*   Missing or improperly configured CA certificates in the runtime environment
    

**Resolution**

1.  Test the request using cURL to isolate whether the issue is environment-specific: curl -v https://graphql.contentstack.com
    
2.  Update Node.js to the latest stable version to ensure the CA certificate bundle is current.
    
3.  If a corporate proxy is in use, obtain the proxy’s CA certificate and add it to the trusted certificate store of the runtime environment.
    

After updating the runtime environment and CA certificates, retry the GraphQL request. If the SSL error no longer appears and the connection succeeds, the certificate trust chain is correctly configured.

### How to Provide Access Token in the GraphQL Explorer

Queries run in the GraphQL Explorer fail due to authorization errors. It is unclear where to input the access\_token to authenticate requests within the Explorer interface.

**Root Cause**

The GraphQL Explorer requires an access token to authenticate API requests. The token must be supplied through the Explorer’s HTTP headers configuration panel, not as a query parameter or inline in the query.

**Resolution**

1.  Open the Contentstack GraphQL Explorer from the stack dashboard.
    
2.  Locate the HTTP Headers panel (typically at the bottom of the Explorer interface).
    
3.  Add the authorization header in the following format: { “access\_token”: “your\_delivery\_token\_here” }
    
4.  Run the query. The Explorer will include the token in all subsequent requests.
    

After adding the access\_token to the HTTP Headers panel, re-run the query. If the query returns results without an authorization error, the token is correctly configured.

### GraphQL Works in Postman but Fails in Apollo Studio Due to Duplicate Content-Type Header

GraphQL queries execute successfully in Postman but fail when the same query and credentials are used in Apollo Studio or Apollo Sandbox. The requests return errors or are rejected.

**Root Cause**

Apollo Studio and Apollo Sandbox automatically add a Content-Type: application/json header to all GraphQL requests. When users manually add the same header in the request configuration, a duplicate Content-Type header is sent. This causes the request to be rejected by the server.

**Resolution**

1.  In Apollo Studio or Apollo Sandbox, navigate to the request headers configuration.
    
2.  Remove any manually added Content-Type: application/json header, as Apollo adds this automatically.
    
3.  Retain only the authorization and access token headers.
    
4.  Re-run the query and confirm it succeeds.
    

After removing the duplicate Content-Type header, re-run the GraphQL query in Apollo Studio. If the query returns results, the header conflict has been resolved.

### Apollo GraphQL Documentation References Incorrect Endpoint URI with /explore

GraphQL implementation based on Apollo documentation fails because the documented URI format includes an /explore path suffix that does not work when used programmatically.

**Root Cause**

The /explore path is the browser-based GraphQL Explorer interface URL, not the API endpoint URL. Using the /explore URI in code or API clients results in requests reaching the wrong destination. The correct GraphQL API endpoint does not include /explore.

**Resolution**

1.  Use the correct GraphQL endpoint format without the /explore suffix. The standard format is: https://graphql.contentstack.com/stacks/{api\_key}
    
2.  Update all code, SDK configuration, and API client settings to use the correct endpoint format.
    
3.  Refer to the official Contentstack GraphQL documentation for the authoritative endpoint format.
    

After updating the endpoint URL in the application, re-run the GraphQL request. If the request connects and returns data, the correct endpoint is now in use.

### GraphQL Explorer Shows No Schema on QA or UAT Branches

The GraphQL Explorer displays no schema and returns errors when accessing QA or UAT branches. The main branch works correctly under the same credentials.

**Root Cause**

The GraphQL token being used does not have access permissions for the QA or UAT branch. Branch-specific access must be explicitly granted to the delivery token. A token configured only for the main branch cannot access other branches, causing the Explorer to show an empty schema for those branches.

**Resolution**

1.  Navigate to Settings > Tokens in the Contentstack dashboard.
    
2.  Select the delivery token being used for GraphQL access.
    
3.  Verify that the token includes access permissions for the QA and UAT branches.
    
4.  If the token does not have branch access, update the token’s permissions or create a new token scoped to the required branches.
    
5.  Reload the GraphQL Explorer and confirm the schema is now available for the QA and UAT branches.
    

After updating the token permissions, reload the GraphQL Explorer for the affected branches. If the schema appears and queries execute correctly, the token now has the required branch access.

### Exporting GraphQL Schema as a .graphql File

There is no built-in export button in the GraphQL Explorer to download the schema as a .graphql file. Developers need the full schema definition for tooling, code generation, or offline reference.

**Root Cause**

The Contentstack GraphQL Explorer does not natively support exporting the schema as a downloadable .graphql file. However, the full schema can be retrieved programmatically using a GraphQL introspection query, which is the standard approach for schema extraction.

**Resolution**

1.  Run a full GraphQL introspection query against the stack’s GraphQL endpoint to retrieve the complete schema definition.
    
2.  Use a tool such as get-graphql-schema, graphql-codegen, or Apollo CLI to convert the introspection JSON result into a .graphql SDL file.
    
3.  Save the output as a .graphql file for use in development tooling, type generation, or documentation.
    

After running the introspection query and converting the output, open the generated .graphql file and verify that it contains the expected type definitions and queries. If the schema is complete, the export has succeeded.

### gql_regex Feature Not Available for Organization

The gql\_regex option is not available or functional in the GraphQL Explorer or API for the organization. Regex-based filtering in GraphQL queries does not work even when the syntax is correct.

**Root Cause**

The gql\_regex feature is not enabled by default for all organizations. It must be explicitly enabled at the organization level by the Contentstack support team. Additionally, after the feature is enabled, content types must be re-saved to refresh the GraphQL schema and make the regex capability active.

**Resolution**

1.  Contact Contentstack Support and request that the gql\_regex feature be enabled for your organization.
    
2.  After receiving confirmation that the feature is enabled, navigate to the affected content types in the CMS.
    
3.  Re-save each affected content type (even without changes) to trigger a schema refresh.
    
4.  Re-run the GraphQL query using the regex filter and confirm the expected results are returned.
    

After enabling the feature and re-saving the content types, execute a GraphQL query with a regex filter. If results match the regex pattern, the feature is active for the organization.

### GraphQL Returns Null for Unpublished or Deleted References

GraphQL responses return null values or empty arrays for reference fields even though references are configured in the entries. The references exist in the CMS but do not appear in the GraphQL response.

**Root Cause**

Contentstack’s GraphQL API intentionally returns only published referenced entries. If a referenced entry is unpublished, in draft state, or has been deleted, GraphQL will return null or an empty array for that reference field. This is by design to ensure the Delivery API only surfaces live, published content.

**Resolution**

1.  Identify which referenced entries are returning null in the GraphQL response.
    
2.  Navigate to those entries in the CMS and verify their publish status in the target environment.
    
3.  Publish any entries that are in draft or unpublished state.
    
4.  Re-run the GraphQL query and confirm that the previously null reference fields now return data.
    

After publishing the referenced entries, execute the GraphQL query again. If the previously null fields now return data, the references are live and being resolved correctly.

### Images Not Appearing in GraphQL Asset Queries

GraphQL queries for assets or entries containing image references return no results or empty arrays for image fields. The images exist in the CMS but are not visible in the query response.

**Root Cause**

GraphQL only returns published assets. Images that exist in the CMS but have not been published to the target environment are not included in the Delivery API response, even if they are visible in the CMS UI.

**Resolution**

1.  Navigate to the Assets section in the CMS.
    
2.  Identify the assets referenced in the failing GraphQL query.
    
3.  Publish the assets to the target environment.
    
4.  Re-run the GraphQL query and confirm that the images now appear in the response.
    

After publishing the assets, execute the GraphQL query. If image data is returned in the response, the assets are now live in the target environment.

### GraphQL all_assets Query Returns Empty Array Despite Assets Existing

A GraphQL query using all\_assets { items { system { … } } } returns an empty array even though assets are visible in the CMS and the API call returns a 200 status.

**Root Cause**

The GraphQL query returns an empty result when either of the following conditions is true:

*   The delivery token used in the request does not have access to the environment being queried
    
*   No assets have been published to the environment specified in the query
    

The API returns a 200 with an empty array rather than an error, which can make the root cause difficult to identify.

**Resolution**

1.  Verify the delivery token’s environment access in Settings > Tokens and ensure the token has access to the target environment.
    
2.  Confirm that at least one asset has been published to the environment referenced in the query.
    
3.  If using the default environment, ensure the delivery token explicitly includes that environment.
    
4.  Re-run the query after verifying token permissions and asset publish status.
    

After confirming the token has environment access and assets are published, execute the all\_assets query. If assets are returned in the response, the token and environment configuration are correct.

### GraphQL Error When Fetching Nested Modular Blocks at the Second Level

GraphQL queries fail when attempting to retrieve nested modular blocks at the second level of nesting. The CMS structure is valid and the REST API returns the expected data, but GraphQL fails specifically on the nested modular block.

**Root Cause**

Querying nested modular blocks (modular blocks within modular blocks) via GraphQL requires specific query structuring that differs from REST API access patterns. Incorrect query structure for the second-level modular block type causes the GraphQL request to fail.

**Resolution**

1.  Review the GraphQL query for the nested modular block and ensure the selection set correctly targets the second-level block type using inline fragments.
    
2.  Use GraphQL inline fragments (… on BlockTypeName) to specify the fields for each modular block type at each nesting level.
    
3.  Validate the query structure in the GraphQL Explorer before running it in the application.
    
4.  If the query structure appears correct but the error persists, contact Contentstack Support and request a troubleshooting session to validate the specific query and schema interaction.
    

After updating the query to use correct inline fragments for the nested modular block type, re-run it in the GraphQL Explorer. If the nested modular block data is returned, the query structure is correct.

### GraphQL Requests Count Toward API Usage Quota

There is uncertainty about whether GraphQL API requests delivered through the Contentstack CDN count toward the API usage quota. Usage metrics appear higher than expected.

**Root Cause**

GraphQL requests run through the Content Delivery API (CDA) and are counted toward the API usage quota, regardless of whether they are served from the CDN cache or hit the origin. Each GraphQL request - cached or otherwise - is recorded as an API call for quota purposes.

**Resolution**

1.  Review API usage metrics in the Contentstack dashboard under Organization settings to understand current consumption patterns.
    
2.  Implement query-level caching in the front-end application to avoid repeated identical GraphQL requests.
    
3.  Use the CDN effectively by structuring queries that can be cached (avoid highly dynamic, user-specific queries for cacheable content).
    
4.  If usage consistently exceeds plan limits, contact the Contentstack account team to review quota allocations.
    

After implementing caching and reviewing usage patterns, monitor the API usage dashboard over a rolling window. If usage decreases to expected levels, the caching strategy is reducing redundant API calls.

### Bandwidth and API Overages Without Application Errors

Bandwidth and API usage are significantly over contracted limits (in some cases 6x or more), yet no errors are visible in the application. The overage is not accompanied by noticeable performance degradation.

**Root Cause**

High usage can occur without triggering errors as long as the traffic is being served successfully. Common causes of unexpected overages include:

*   Increased consumption from CDN and Images API endpoints
    
*   High-resolution or unoptimized assets being served repeatedly
    
*   Bots, crawlers, or unintended traffic patterns hitting the delivery endpoints
    
*   A spike in legitimate end-user traffic or new integration workflows
    

**Resolution**

1.  Review historical usage trends in the Contentstack dashboard to identify when the overage began and which endpoints are driving the increase.
    
2.  Analyze CDN and Images endpoint consumption specifically, as these commonly drive bandwidth overages.
    
3.  Audit asset sizes and implement image optimization or resizing to reduce per-request bandwidth.
    
4.  Check for unexpected bot traffic or crawler activity hitting the delivery endpoints.
    
5.  Contact the Contentstack account team to review overage charges and discuss plan adjustments if increased usage is legitimate and expected to continue.
    

After identifying the traffic source and implementing optimization, monitor bandwidth and API metrics for a 7-day period. If consumption returns to within contracted limits, the optimization measures are effective.

### GraphQL CDN Caching Inconsistencies

GraphQL requests return inconsistent results or do not behave as expected due to CDN caching. Some requests return stale data while others hit the origin unnecessarily.

**Root Cause**

CDN caching for GraphQL requests depends on how the CDN hashing mechanism is configured. If the hashing configuration does not correctly account for the query body, variables, or headers, requests may be incorrectly grouped into the same cache key or bypassed entirely.

**Resolution**

1.  Contact Contentstack Support if you observe consistent caching anomalies such as stale data or unexpected cache misses.
    
2.  Support will review the CDN hashing configuration for the affected stack and adjust it to ensure requests with different query bodies or variables are cached independently.
    
3.  In the meantime, append a cache-busting query string parameter to force fresh requests where stale data is critical.
    

After the CDN hashing configuration is adjusted, re-run the affected GraphQL queries. If responses are now consistent and correctly reflect the latest published content, the caching issue is resolved.

### GraphQL Taxonomy Search Not Returning Expected Results

A GraphQL taxonomy search query returns unexpected or empty results despite the taxonomy being correctly configured in the CMS.

**Root Cause**

GraphQL taxonomy search results can be affected by a stale cache at the delivery token or entry level. If the taxonomy or entries were recently created or modified, the cache may not have updated to reflect the latest state.

**Resolution**

1.  Navigate to Settings > Tokens and re-save the delivery token used in the GraphQL query (without making changes) to force a cache refresh.
    
2.  Re-save the affected entries or taxonomy terms in the CMS to trigger a cache invalidation.
    
3.  If caching is suspected at the CDN layer, append a unique query string parameter to the request to bypass the cache: ?cb=<random\_value>
    
4.  Re-run the taxonomy search query and confirm results now match expectations.
    

After re-saving the token and entries, execute the taxonomy search query again. If the expected taxonomy results are returned, the cache has been successfully refreshed.

### GraphQL Introspection Cannot Be Disabled in Contentstack

A request to disable GraphQL introspection in production - either for security hardening or to prevent schema exposure - cannot be fulfilled. Contentstack does not provide a configuration option to disable introspection.

**Root Cause**

Contentstack does not support disabling GraphQL introspection. Introspection queries are treated equivalently to GET Content Types API requests. There is no separate control to disable introspection independently from other API access. This is a platform design decision.

**Resolution**

Since introspection cannot be disabled, consider the following security mitigations:

1.  Ensure delivery tokens are scoped to the minimum required environments and branches.
    
2.  Do not expose management API keys or tokens in client-facing code.
    
3.  Apply rate limiting on the network or infrastructure layer to restrict the volume of introspection queries from external sources.
    

Introspection access is equivalent to GET Content Types access. If schema exposure is a concern, focus on delivery token scoping and network-level controls rather than attempting to disable introspection at the platform level.

### Retrieving Variant Content in GraphQL for Personalization

After configuring personalization and variants in the CMS, there is no variant filter available in the GraphQL Explorer’s where clause. Variant-specific content cannot be retrieved through the standard GraphQL query interface.

**Root Cause**

Variant filters for personalized content are not available in the GraphQL Explorer interface. Personalization variant retrieval is not supported through the standard where clause in GraphQL queries.

**Resolution**

1.  Use a direct API request (REST or GraphQL) and include the variant information in a special HTTP header instead of the query parameters.
    
2.  Refer to the Contentstack Personalization documentation for the correct header name and format required to retrieve variant-specific content.
    
3.  Implement the header-based variant retrieval in the application code rather than relying on the GraphQL Explorer interface.
    

After adding the required variant header to the API request, verify that the response returns the expected variant version of the content. If the variant-specific content is returned, the header configuration is correct.

### Intermittent Null Entry IDs Resolved by Rotating the Production Delivery Token

Production GraphQL API responses intermittently return null for entry IDs with the error “Failed to fetch item – Object not found.” The issue occurs only in the production environment and not in staging or development.

**Root Cause**

Intermittent authentication or token-related inconsistencies can cause the API to fail to resolve entries correctly, returning null IDs. Token rotation - generating a new delivery token - resolves stale token states that may accumulate over time in production environments.

**Resolution**

1.  Navigate to Settings > Tokens in the Contentstack dashboard.
    
2.  Regenerate or rotate the production delivery token.
    
3.  Update the application configuration to use the new delivery token.
    
4.  Re-run the affected GraphQL queries and confirm that entry IDs are returned correctly without null values.
    

After rotating the delivery token and updating the application, execute the previously failing queries in production. If entry IDs are returned consistently without null values, the token rotation has resolved the inconsistency.

### Cache Headers for CDN Optimization - Adding s-maxage

Performance testing reveals CDN cache MISS responses for repeated requests. Repeated API calls are reaching the origin, causing latency and contributing to 429 rate limit errors. Cache-Control headers are not set or are set only for browser caching.

**Root Cause**

Without s-maxage in the Cache-Control header, CDN edge nodes do not cache API responses. The max-age directive controls browser-side caching only. Without explicit CDN caching instructions, every request passes through to the origin, multiplying traffic and increasing the risk of rate limiting under load.

**Resolution**

1.  Add Cache-Control: s-maxage=86400 to responses intended for CDN caching. The s-maxage directive instructs CDN and shared caches to store the response for the specified duration (86400 seconds = 24 hours).
    
2.  Retain max-age for browser-side caching if the application also needs client caching.
    
3.  After adding the header, redeploy the application or use the Launch cache revalidation option to clear existing CDN cache and begin serving the new cached responses.
    
4.  Re-run the load test after the header update. Monitor CDN cache HIT vs MISS rates to confirm caching is now effective.
    

After deploying with s-maxage headers, confirm that repeated requests return CDN cache HITs in the response headers and that the origin request rate decreases proportionally.

### include[] Path Broken After Content Type Schema Update

An include\[\] parameter that correctly resolved a nested reference stops working after a content type schema update. The API returns incomplete data or ignores the include path entirely.

**Root Cause**

The include\[\] path is evaluated against the current content type schema. When a schema is updated - for example, a reference field is moved, renamed, or restructured within a group or modular block - the include path that previously worked no longer matches the updated schema. The API silently ignores include paths that do not resolve to a valid reference field.

**Resolution**

1.  After a content type schema update, review all include\[\] paths in the application against the updated schema.
    
2.  Fetch the current content type schema: GET /v3/content\_types/{uid} to inspect the field UID structure and confirm the correct path.
    
3.  Update the include\[\] path to reflect the new field structure. For example, if a reference field moved from section\_config.items.ref to section\_config.carousel.items.ref, update the path accordingly.
    
4.  Test the updated include\[\] path with a single entry before deploying the change to production.
    

After updating the include path to match the current schema, confirm the referenced entry data is returned in the API response.

### include_all_depth Is Only Valid on the CDA - Not CMA

The include\_all\_depth parameter is added to an API request but has no effect. The nested references are not resolved to the expected depth.

**Root Cause**

The include\_all and include\_all\_depth parameters are only supported by the Content Delivery API (CDA). When these parameters are used with the Content Management API (CMA) endpoint, they are silently ignored. This is a common source of confusion when requests are inadvertently routed to the wrong endpoint.

**Resolution**

1.  Confirm the request is using the CDA endpoint: cdn.contentstack.io (or the appropriate regional CDA host) and not the CMA endpoint: api.contentstack.io.
    
2.  Include both include\_all=true and include\_all\_depth={n} in the CDA request:
    
3.  Example: GET https://cdn.contentstack.io/v3/content\_types/{uid}/entries/{entry\_uid}?environment=production&include\_all=true&include\_all\_depth=2
    
4.  Note: the 100-reference cumulative limit applies across all resolved levels. See Issue 3 below for guidance on staying within this limit.
    

After confirming the request targets the CDA endpoint and includes both parameters, verify that referenced entries are returned at the expected depth.

### 422 Error - include_all=true Causes Recursive Resolution Beyond 100 References

The API returns a 422 error with the message ‘should not be greater than 100’ when using include\_all=true, even though there are fewer than 100 referenced entries at the first level. The error appears intermittent or only for certain entries.

**Root Cause**

The 100-reference limit is cumulative across all resolved depth levels, not per level. When include\_all=true is used, the API recursively resolves all references at every level. A content type with 10 first-level references, each pointing to 5 second-level references, can produce 60 resolved references in total - exceeding the limit for entries with deeper or broader reference trees. Additionally, 422 errors on include\[\] can also be triggered by invalid locale parameter formats in the same request.

**Resolution**

1.  Switch from include\_all=true to explicit include\[\] paths that resolve only the specific references needed.
    
2.  Use include\_all\_depth=1 or =2 rather than allowing unlimited recursive resolution, and verify the total resolved reference count stays under 100.
    
3.  For content types with deep or wide reference structures, split the request: fetch the top-level entry first, then fetch referenced entries in separate calls using their UIDs.
    
4.  Verify the locale parameter format is correct if 422 errors are not consistently triggered by include\_all. Valid format examples: en-us, fr-fr. Invalid: en\_US, de\_DE (underscore notation is not accepted).
    

After switching to explicit include\[\] paths and verifying the locale format, confirm the 422 error no longer occurs for the affected entries.

### 422 Error - 100 Reference Include Limit Cannot Be Increased

A request to increase the 100-reference include limit to 150–200 is made. The application’s content structure genuinely requires resolving more than 100 references in a single call. The same ‘include should not be greater than 100’ error can also surface on the CMA (not just the CDA) - for example, on entries where a Group field combines a Boolean field with a Reference field - because the 100-reference count applies to the total resolved references in the response, regardless of endpoint.

**Root Cause**

The 100-reference limit for include\[\] and include\_all is a hard platform constraint imposed due to the high computational cost of resolving reference trees at scale. It applies to both the CDA and the CMA and cannot be increased at the organization or account level.

**Resolution**

1.  Restructure the application to fetch deep reference chains in multiple requests: first call resolves the top-level entry with the first set of references; subsequent calls resolve each referenced entry’s nested references individually.
    
2.  Merge the results client-side to reconstruct the full data structure before rendering.
    
3.  For CMA requests hitting this error on a Group field with a Boolean + Reference combination, reduce the include depth or scope to keep the total resolved reference count within the limit.
    
4.  Consider using GraphQL for complex reference structures - GraphQL’s explicit field selection can retrieve specific nested fields without triggering the 100-reference counting mechanism.
    
5.  If the content model can be simplified (for example, by flattening some nested reference chains into inline fields), this can reduce the number of references that need resolving per request.
    

After splitting the request into multiple calls and merging results client-side, verify the full content structure is correctly assembled and the application renders as expected.

### Global Field Schema Missing from getContentType API Response

The schema for a nested Global Field is missing from getContentType API responses and from the GraphQL Explorer. The Global Field is referenced within another Global Field, and its schema appears empty in the API response despite appearing correctly in the Contentstack UI.

**Root Cause**

Nested Global Field schemas can suffer from schema caching inconsistencies, where the outer Global Field’s schema does not reflect the inner Global Field’s current structure. This occurs when the inner Global Field is updated but the outer Global Field’s schema cache is not refreshed.

**Resolution**

1.  Open the outer Global Field in the CMS and re-save it without making any changes. This forces a schema refresh that propagates the inner Global Field’s current structure.
    
2.  If the issue persists, open both the inner and outer Global Fields and re-save each one.
    
3.  After re-saving, fetch the content type schema again via the API and confirm the nested Global Field schema is now included in the response.
    
4.  If the schema remains empty after re-saving, contact Contentstack Support with the Global Field UIDs and stack API key for investigation.
    

After re-saving the affected Global Fields, fetch the content type and confirm the nested Global Field schema is populated correctly in the API response.

### Reference Count Discrepancy Between UI and Content Management API

A reference field shows 19 linked entries in the Contentstack UI but the CMA API returns only 17 matching entries. Two entries appear with an unexpected content type UID in the API response.

**Root Cause**

The discrepancy occurs when some referenced entries belong to a content type that has been renamed or modified since the references were created. The UI resolves the display name dynamically, showing the current content type name. The CMA returns the actual stored content type UID at the time of reference creation, which may not match the current content type UID after a rename.

**Resolution**

1.  Identify the two entries with the unexpected content type UID from the API response.
    
2.  Open those entries in the CMS and re-save them to update the stored content type reference to the current UID.
    
3.  Re-fetch the reference field via the CMA and confirm all 19 entries now return with the correct and consistent content type UID.
    

After re-saving the affected entries, verify the reference field count matches between the CMS UI and the CMA API response.

### 400 Error for Valid Locale Parameter - Re-save Delivery Token to Fix

API requests with a specific locale code (for example, de-de) intermittently fail with a 400 error. The same request works when tested from a different environment or tool. The issue is not consistently reproducible.

**Root Cause**

The delivery token configuration may have become out of sync with the stack’s branch or environment scope. This can occur after a branch scope change or environment update that was not propagated correctly to the delivery token’s state. The result is intermittent validation failures for otherwise valid locale parameters.

**Resolution**

1.  Navigate to Settings > Tokens in the Contentstack dashboard.
    
2.  Open the affected delivery token and re-save it without making any changes. This forces the token configuration to resync with the current branch and environment scope.
    
3.  Re-run the previously failing request with the locale parameter and confirm it no longer returns a 400 error.
    

Re-saving the delivery token resolves the configuration desync. No code or API request changes are required.

### Error 109 - Invalid API Key When Using the Wrong Regional Endpoint

API calls return error code 109: ‘api\_key is not valid’ or ‘We can’t find that Stack’ despite using the correct API key. The stack exists and is accessible via the Contentstack UI.

**Root Cause**

Error 109 occurs when the request is sent to a regional CDA endpoint that does not host the stack. Contentstack infrastructure is region-specific. A stack provisioned on Azure EU must be accessed via the Azure EU CDN endpoint. Using the standard AWS NA endpoint for an Azure-hosted stack produces a 109 error because the stack does not exist in that region’s database.

**Resolution**

1.  Identify the cloud provider and region for the stack from the dashboard URL or stack settings.
    
2.  Update the CDA base URL to the correct regional endpoint:
    

*   AWS NA: cdn.contentstack.io
    
*   AWS EU: eu-cdn.contentstack.com
    
*   Azure NA: azure-na-cdn.contentstack.com
    
*   Azure EU: azure-eu-cdn.contentstack.com
    

1.  Update the API host in SDK configurations, environment variables, and any hardcoded URLs.
    
2.  Re-run the API call and confirm the stack is found and a valid response is returned.
    

After updating to the correct regional endpoint, confirm the 109 error no longer appears and the API returns content from the correct stack.

### 500 Internal Server Error from Taxonomy Queries - CMA Endpoint with Delivery Token

A CDA request using a delivery token (access\_token) to a taxonomy-related endpoint returns a 500 Internal Server Error. The same token works correctly for non-taxonomy endpoints.

**Root Cause**

The request is being sent to the CMA API endpoint (api.contentstack.io) using a delivery token. The CMA requires a management token or auth token - passing a delivery token to the CMA produces unexpected behavior including 500 errors. Delivery tokens are only valid for CDA endpoints (cdn.contentstack.io and its regional equivalents).

**Resolution**

1.  Confirm the endpoint being called. For content delivery use cases, use the CDA endpoint (cdn.contentstack.io or regional equivalent) with the delivery token (access\_token header).
    
2.  If the use case requires CMA access (for example, fetching unpublished entries or schema data), use the CMA endpoint (api.contentstack.io) with a management token or auth token.
    
3.  Never use a delivery token on the CMA endpoint - this configuration is not supported.
    

After switching to the correct endpoint and token combination, re-run the request and confirm a valid response is returned.

### 500 Errors from Malformed sort Field Payload

The CDA returns intermittent 500 Internal Server Errors for certain endpoints. Investigation shows the errors are consistently triggered at the origin (not the CDN) for a specific set of requests.

**Root Cause**

500 errors at the origin level are triggered by malformed payloads in the sort field parameter. When the sort query parameter contains an invalid value (for example, an unsupported field name, incorrect format, or an unexpected data type), the origin server fails to process the request and returns a 500.

**Resolution**

1.  Review the sort parameter in the failing requests. Valid sort values are field UIDs (for example, created\_at, updated\_at, or a custom field UID).
    
2.  Test the request without the sort parameter to confirm the 500 disappears, isolating the sort field as the cause.
    
3.  Correct the sort parameter to use a valid, indexed field UID.
    

**Note:** the CDA does not support multi-field sorting. Only a single sort parameter is accepted per request.

After correcting the sort parameter, re-run the request and confirm the 500 error no longer occurs.

### Error 141 - CDA Query with Nested Field Dot Notation

A CDA query with a filter on a nested field using dot notation returns error 141: ‘Failed to fetch entries. Please try again with valid parameters.’ The query format appears correct.

**Root Cause**

The error occurs because the filter is attempting to query a nested field path (for example, category.category) but the field is defined as a reference or group, which is not directly queryable using simple dot notation in a JSON query string. The CDA query parser rejects the path as invalid. Reference fields must be queried using their specific query operator (for example, $in with the referenced entry UID), not a value equality filter on a nested path.

**Resolution**

1.  For filtering on a reference field’s value, use the $in operator with the referenced entry UID instead of the nested field value.
    
2.  For filtering on an inner field of a group field, use the full dot-notation path within the query JSON object, encoded correctly in the URL.
    
3.  Example for reference field: query={“category.uid”:{“$in”:\[“blt12345”\]}} rather than query={“category.category”:“value”}.
    
4.  Test the corrected query format in the GraphQL Explorer or via cURL before integrating into the application.
    

After correcting the query format, re-run the request and confirm entries are returned without error 141.

### 422 Errors - Invalid Locale Format and Invalid Include Paths

CDA requests return 422 Unprocessable Entity errors. Analysis of error logs shows 422s across a large volume of requests, with the majority concentrated in a short burst window.

**Root Cause**

422 errors in CDA requests are typically caused by one of two issues: (a) invalid locale parameter format - for example, using underscore notation (en\_US, de\_DE) instead of hyphen notation (en-us, de-de); or (b) invalid include\[\] paths that do not resolve to a valid reference field in the content type schema. Both are validation failures that the API rejects before processing.

**Resolution**

1.  Review the locale parameter in failing requests. Use hyphen notation: en-us, fr-fr, de-de. Underscore formats (en\_US) are not accepted.
    
2.  Review all include\[\] path values against the current content type schema. Paths that reference deleted, renamed, or restructured fields produce 422 errors.
    
3.  If 422s appear in high-volume bursts from a specific time period, examine whether a deployment or automation introduced a new locale format or changed reference paths.
    
4.  Check the 422 error response body for details - the errors object typically specifies which parameter is invalid.
    

After correcting locale formats and include\[\] paths, re-deploy and monitor for 422 errors. The error rate should return to near-zero once all invalid parameters are corrected.

### Entries Missing from API Query Results - url as Top-Level Parameter

An API query intended to filter entries by a URL field returns all entries (up to the default 100 limit) instead of the specific entry matching the URL. The URL filter appears to be ignored.

**Root Cause**

The URL filter is being passed as a top-level query parameter (for example, url=/about) rather than inside the query JSON object. The CDA only processes field filters when they are included within the query JSON parameter. Top-level parameters that are not recognized by the API are silently ignored, causing the API to return the default result set without filtering.

**Resolution**

1.  Move the URL filter inside the query JSON object: query={“url”:“/about”}
    
2.  Correctly URL-encode the query parameter when including it in the request URL.
    
3.  Test the corrected query with a known URL value and confirm the correct single entry is returned.
    
4.  If filtering by the URL field, ensure the field is named url (the system URL field) or use the exact field UID for custom URL fields.
    

After moving the filter inside the query JSON object, confirm the API returns only the entry matching the specified URL.

### Unexpected _validations Property Appearing in CDA Responses

CDA API responses contain an unexpected \_validations property that was not present in previous responses. The customer is unsure whether this is expected behavior or a bug.

**Root Cause**

The \_validations property appeared due to an internal validation feature that was enabled for a limited set of customers during testing and was unintentionally exposed in the CDA response payload. This is not a documented CDA field and its presence in responses is a platform-level error.

**Resolution**

1.  Contact Contentstack Support and report the presence of \_validations in the CDA response, providing the affected stack API key and a sample response.
    
2.  Engineering will deploy a fix to remove the property from CDA responses for the affected stack.
    
3.  After the fix is deployed, re-publish affected entries if the property still appears (re-publishing triggers a delivery data refresh).
    
4.  In the meantime, update any response parsing or TypeScript interfaces to treat \_validations as an optional unknown field to prevent type errors.
    

After the engineering fix is deployed and entries are re-published, fetch the affected entries and confirm \_validations no longer appears in the CDA response.

### Intermittent 502 Latency Spikes via SDK - CDN Edge Delays

Production applications using the TypeScript Delivery SDK experience intermittent latency spikes (up to 60+ seconds) and occasional 502 errors. The stack itself appears stable and direct cURL tests show normal response times.

**Root Cause**

The latency is caused by CDN edge-level delays, not by the origin server. CDN edge nodes can experience transient congestion or routing issues that cause requests to wait longer than normal at the edge before receiving a response. The SDK wraps the CDN call, making the delay appear as SDK-level slowness. The origin processes the request within normal bounds (around 1–2 seconds) but the CDN layer adds the additional delay.

**Resolution**

1.  Implement a client-side timeout in the SDK configuration. Set a reasonable timeout (for example, 10 seconds) so requests that stall at the edge fail fast and can be retried rather than waiting indefinitely.
    
2.  Implement retry logic with exponential backoff for requests that exceed the timeout threshold.
    
3.  If sustained latency spikes are observed, contact Contentstack Support and provide the time window, affected region, and stack details. CDN engineering can investigate edge routing issues.
    
4.  Monitor the CDN layer by measuring response time at both the network level and the SDK level to distinguish edge delays from origin delays.
    

After configuring a client-side timeout, confirm that requests stalling at the CDN edge fail within the timeout window and are retried successfully.

### ECONNRESET - Connection Reset Before Response Received

Applications receive ECONNRESET errors (connection reset by peer) when fetching content from the Contentstack CDA. The error indicates the server-side connection was closed before the full response was delivered.

**Root Cause**

ECONNRESET errors are network-layer failures, not CDA errors. The TCP connection is unexpectedly closed before the response is fully transmitted. Common causes include: network path instability between the application and the CDN edge, a proxy or load balancer with an aggressive connection timeout, an upstream CDN or network device closing idle or slow connections, or the CDN rotating the IP address mid-connection during a certificate renewal.

**Resolution**

1.  Implement retry logic with exponential backoff specifically for ECONNRESET errors. These are typically transient and succeed on retry.
    
2.  Check whether a proxy, VPN, or load balancer sits between the application and the Contentstack CDN. Review its connection timeout and keepalive settings.
    
3.  If ECONNRESET errors are correlated with specific CDN IP addresses, check whether CDN IP reassignment is the cause (see Issue 6 below).
    
4.  Contact Contentstack Support with the time window, frequency of occurrences, and the network path being used (direct to CDN vs via proxy) for CDN-level investigation.
    

After implementing retry logic, confirm that ECONNRESET errors result in successful retries rather than failed requests. Monitor the frequency of retries to assess whether the underlying network issue needs further investigation.

### ETIMEDOUT Errors on Contentstack Launch Domain

Applications hosted on Contentstack Launch experience intermittent ETIMEDOUT errors when fetching page entries. The errors occur on consecutive days and affect specific URL paths.

**Root Cause**

ETIMEDOUT errors from a Launch domain indicate the connection attempt to the Contentstack CDA timed out before establishing a connection. This is typically caused by a CDN edge issue, a platform-level service degradation, or an overloaded query that takes too long to process.

**Resolution**

1.  Check the Contentstack Status Page (status.contentstack.com) for any active incidents during the observed timeframe.
    
2.  Review the specific API queries generating ETIMEDOUT errors for complexity - queries with deep reference chains or large result sets can time out under load.
    
3.  Simplify or paginate the affected queries to reduce per-request processing time.
    
4.  Implement timeout handling and retry logic in the application so ETIMEDOUT errors trigger a retry rather than a permanent failure.
    
5.  If ETIMEDOUT errors persist without an active platform incident, contact Contentstack Support with sample failing request URLs and the time window.
    

After simplifying queries and implementing retry logic, confirm ETIMEDOUT errors no longer cause permanent page load failures.

### SSL Certificate Errors After CDN Migration to Cloudflare

After a CDN migration, all subdomains of a custom domain return SSL certificate errors. Users receive SSL handshake failure messages and content cannot be delivered.

**Root Cause**

SSL certificate errors after a CDN migration to Cloudflare are typically caused by an incomplete certificate chain or misconfigured intermediate certificates on Cloudflare. During the CDN migration, the certificate provisioning process may not have completed correctly, leaving the intermediate certificate chain broken. This causes SSL handshake failures for all clients that do not already have the root certificate cached.

**Resolution**

1.  Contact Contentstack Support and report the SSL certificate errors, providing the affected domain(s) and a sample SSL error message.
    
2.  The CDA team will investigate the certificate chain on Cloudflare and re-issue or correct the intermediate certificate configuration.
    
3.  To verify the issue, use an SSL certificate checker tool (such as SSL Labs) to inspect the certificate chain for the affected domain.
    
4.  Do not attempt to manually modify DNS or certificate settings during investigation, as this can compound the issue.
    

After the certificate chain is corrected, verify using an SSL checker that the full chain is complete and test content delivery on the affected domain.

### DNS Returning Only AAAA (IPv6) Records After CDN Migration - IPv4 Services Affected

After a CDN migration, a custom domain that previously returned IPv4 (A) records in DNS lookups now returns only IPv6 (AAAA) records in some regions. Services that do not support IPv6 fail to connect.

**Root Cause**

During the CDN migration to Cloudflare, Cloudflare’s DNS resolution in certain regions may prioritize IPv6 over IPv4 or return only AAAA records. Services that exclusively use IPv4 stacks cannot connect to AAAA-only responses, causing connection failures in those regions.

**Resolution**

1.  Contact Contentstack Support and report the DNS behavior, specifying the affected domain, region, and that only AAAA records are being returned.
    
2.  The CDA and infrastructure team will work with the CDN provider to ensure both A and AAAA records are returned (dual-stack configuration).
    
3.  As an immediate mitigation for IPv4-only services, configure the service to prefer IPv4 resolution or implement a fallback DNS resolver that returns A records.
    

After the CDN DNS configuration is corrected to return dual-stack records, verify using DNS lookup tools from the affected region that both A and AAAA records are returned for the domain.

### CDN IP Reassignment After Certificate Renewal Causes Image Loading Failures

Images that were loading correctly begin failing after a period of time. Investigation reveals that CDN IP addresses changed during a certificate renewal or domain re-verification process, causing previously cached IP addresses or firewall rules to become stale.

**Root Cause**

CDN providers like Cloudflare and Fastly may reassign IP addresses to a domain during certificate renewal or domain re-verification processes. This is a CDN provider-level behavior that Contentstack cannot prevent. When IP addresses change, any firewall rules or client-side IP caches that had the old addresses will block or fail to connect to the new addresses.

**Resolution**

There is no guaranteed way to prevent CDN IP reassignment - this is a CDN provider behavior. Mitigation strategies:

1.  Do not whitelist CDN IP addresses by specific IP value. Instead, whitelist by domain name using DNS-based firewall rules, which automatically resolve to the current IPs.
    
2.  If IP-based whitelisting is required (for example, in legacy firewall configurations), establish a process to review and update CDN IP lists periodically and after any certificate renewal events.
    
3.  Subscribe to CDN provider status pages and IP change announcements to proactively update firewall rules before changes take effect.
    

After updating firewall rules to reflect the new CDN IPs, verify image loading is restored by testing affected asset URLs from the impacted network environment.

### include_all_depth Not Working in JavaScript Delivery SDK

Fetching deeply nested referenced entries using include\_all\_depth works correctly when calling the Contentstack REST API directly, but the same depth configuration does not produce nested results when using the JavaScript Delivery SDK.

**Root Cause**

The JavaScript Delivery SDK requires the include\_all\_depth parameter to be added explicitly via the .addParam() method. Without this, the SDK defaults to a shallow reference fetch and does not honor depth values passed through other means.

**Resolution**

1.  Add the include\_all\_depth parameter using the SDK’s .addParam() method:
    
2.  Example: Query.addParam(‘include\_all\_depth’, 3); - where 3 is the desired depth level.
    
3.  Ensure include\_all is also set to true alongside include\_all\_depth.
    
4.  Re-run the query and verify that nested referenced entries are returned at the specified depth.
    

Note: The 100-reference cumulative limit still applies across all resolved levels. If the total resolved references across all depth levels exceeds 100, the request will fail with a 422 error. Reduce depth or reference count if this occurs.

After adding the parameter, execute the SDK query and confirm that referenced entries at the target depth are present in the response.

### include_all and include_depth Are Not Supported in the Content Management API

Attempts to use include\_all or include\_depth parameters in Content Management API (CMA) requests to fetch referenced entry details do not return the expected nested content, even though the same parameters work correctly in CDA calls.

**Root Cause**

The include\_all and include\_depth parameters are exclusive to the Content Delivery API (CDA). They are not supported in the Content Management API (CMA) by design. The CMA is intended for content creation, update, and management operations, not for resolving deep reference hierarchies in delivery responses.

**Resolution**

1.  Use the CDA endpoint (cdn.contentstack.io) instead of the CMA endpoint when fetching entries with nested references.
    
2.  Pass the include\_all=true and include\_depth parameters in CDA requests to resolve referenced entries.
    
3.  If the CMA must be used (for example, to fetch draft or unpublished content), retrieve referenced entry UIDs from the CMA response and make separate CDA or CMA calls for each referenced entry.
    

After switching to the CDA endpoint with the include\_all parameter, confirm that the API response contains the expanded referenced entry data.

### Fetching Only Specific Fields from Referenced Entries Using the SDK

When fetching entries through the SDK using .includeReference(), the full content of referenced entries is returned. There is no apparent way to limit the response to only specific fields within referenced entries, leading to oversized responses.

**Root Cause**

The SDK’s .includeReference() method fetches the complete referenced entry by default. To limit the fields returned for referenced entries, the .only() method must be used in combination with field-specific parameters to specify which fields to include in the response.

**Resolution**

1.  Chain .only() after .includeReference() in the SDK query to specify the fields required from the referenced entry.
    
2.  Pass the reference field name and an array of the desired sub-fields as parameters to .only().
    
3.  Example structure: Query.includeReference(‘author’).only(‘author’, \[‘name’, ‘bio’\]).find()
    
4.  Test the query to confirm only the specified fields are returned within the referenced entry object.
    

After implementing .only(), execute the query and verify that referenced entries in the response contain only the specified fields, reducing the response payload size.

### 422 Error When Querying Nested Reference Fields - Use Field UID, Not Entry UID

A CDA request returns a 422 error when attempting to filter on a nested reference field. The query structure places entry UIDs directly inside the filter parameter instead of resolving the reference field first.

**Root Cause**

When querying nested reference fields in the Delivery API, the filter must reference the field UID of the nested reference, not the UID of the referenced entry. Passing entry UIDs directly into nested query parameters produces an invalid query structure that the API rejects with a 422 error.

**Resolution**

1.  Identify the field UID of the reference field within the content type (not the UID of the referenced entry).
    
2.  Structure the query filter using the field UID path, for example: query\[reference\_field\_uid\]\[entry\_uid\]\[$in\]\[\]=value
    
3.  Refer to the Contentstack documentation for Reference Search (Equals) for the correct query parameter format.
    
4.  Test the corrected query and confirm a valid response is returned.
    

After correcting the query structure to use field UIDs, re-run the request. If the API returns a valid response without a 422 error, the query syntax is correct.

### ECONNRESET Errors When Fetching Nested Content with .includeReference

Intermittent network socket disconnection errors (ECONNRESET) occur when fetching entries with nested content using the CDA SDK’s .includeReference method. The errors are inconsistent - some complex pages fail while others with similar structure succeed.

**Root Cause**

ECONNRESET errors in this context are client-side network socket disconnections, not CDA errors. They can be triggered by network instability, proxy timeouts, or connection pool exhaustion when the client makes many simultaneous or large reference-resolution requests. Contentstack CDA responses are valid and complete; the connection is being dropped on the client or intermediate network layer.

**Resolution**

1.  Implement retry logic with exponential backoff around .includeReference calls to handle transient network failures.
    
2.  Reduce the number of concurrent reference resolution requests by batching or sequencing complex page fetches.
    
3.  Review network and proxy configuration for connection timeout settings and increase them if requests are being terminated prematurely.
    
4.  If the issue is environment-specific (for example, only on a deployment platform like Netlify or Vercel), validate the networking configuration of that environment.
    
5.  Update the .includeReference implementation to use the minimum required depth to reduce response size and connection duration.
    

After implementing retry logic and reviewing the network configuration, run the affected queries again. If ECONNRESET errors no longer occur consistently, the connection handling has been stabilized.

### Sorting on Nested or Referenced Fields Not Supported in CDA SDK

Attempts to sort entries by fields inside a referenced entry using .orderByAscending() or .orderByDescending() in the CDA SDK do not produce the expected sort order. Sorting on top-level fields like created\_at works correctly, but sorting on reference paths such as title\_reference.release\_date returns unsorted or incorrect results.

**Root Cause**

The Delivery API’s orderByAscending and orderByDescending parameters only support sorting on fields that belong directly to the queried content type (top-level fields). Sorting on nested paths within referenced entries is not supported, even when include\_all or deeper reference resolution is applied.

**Resolution**

1.  Fetch entries without the sort parameter and perform sorting client-side after retrieving and resolving all referenced data.
    
2.  If server-side sorting is required, restructure the content model to promote the sort field to a top-level field on the queried content type.
    
3.  For use cases requiring complex sorting across referenced types, consider using GraphQL, which allows more flexible query and sort composition.
    

After applying client-side sorting or restructuring the content model, verify that the returned entries are ordered as expected.

### 422 Error - “include should not be greater than 100” When Using include_all

A CDA request using include\_all=true or include\_all\_depth returns a 422 error with the message: “include should not be greater than 100”. The expectation is that the entry has fewer than 100 linked entries, so the limit appears to be hit unexpectedly.

**Root Cause**

The 100-reference limit is cumulative across all resolved reference levels, not per level. When include\_all=true is used, the API resolves every reference at every depth. Even if each level has a small number of references, the total count across all levels can exceed 100 quickly. For example, 5 references at level 1, each pointing to 5 entries at level 2, each with 5 at level 3, produces 155 total resolved references - well above the limit. The 422 error is expected and enforced to protect platform stability.

**Resolution**

1.  Reduce the reference depth by lowering the include\_all\_depth value. Start at depth 1 and increase incrementally until the 100-reference threshold is approached.
    
2.  Reduce the number of referenced entries per level in the content model where possible.
    
3.  Split the query into multiple smaller requests: fetch the top-level entry first, then fetch referenced entries separately using their UIDs.
    
4.  Merge the results client-side to reconstruct the full data structure.
    
5.  Apply filters or pagination on referenced fields to limit how many references are resolved per request.
    

After restructuring the query to reduce total resolved references below 100, re-run the request. If the 422 error no longer appears, the cumulative reference count is within the limit.

### Cached Requests Are Still Counted in Product Analytics

Product Analytics shows API requests for assets and entries even when responses are served from the CDN cache. The expectation is that cached responses should not increment the API usage count.

**Root Cause**

Product Analytics logs every request that reaches Contentstack endpoints - including CDN, Images API, GraphQL, and Assets - regardless of whether the response is served from cache or origin. Cache hits are still recorded as API calls because the request is processed by the CDN layer, which is part of Contentstack infrastructure.

**Resolution**

This is expected behavior. Cached requests do count toward API usage metrics and cannot be excluded from Product Analytics. To reduce overall API usage counts:

1.  Maximize cache hit rates by structuring requests to be cache-friendly (consistent URLs, minimal query string variation).
    
2.  Implement application-level or CDN-level caching upstream of Contentstack to avoid repeated requests for the same content.
    

After improving cache hit rates, monitor Product Analytics to confirm that total request counts decrease as more responses are served from the application cache.

### CDN Cache Not Updating After Changes to a Custom JSON Global Field

After updating an entry through a Custom JSON field that references a global field, the changes are not reflected in the live site. The CDN continues to serve stale content even after the update is confirmed in the CMS.

**Root Cause**

When a global field is updated through a custom JSON field, the CDN cache may not be automatically purged. The cache purge is triggered by a publish event on the parent entry. If the update path does not trigger a standard publish event, the CDN retains the cached version of the content.

**Resolution**

1.  After updating the entry via the Custom JSON field, explicitly publish the parent entry to trigger a CDN cache purge.
    
2.  If the entry is referenced by other entries, publish those as well to propagate the cache invalidation.
    
3.  Refer to the Contentstack CDN Cache Management documentation for guidance on revalidation workflows for global fields and custom extensions.
    

After publishing the parent entry, request the affected URL and confirm the response reflects the updated content.

### 401 Error When Using eu-assets.contentstack.com Endpoint

Attempts to retrieve assets using the eu-assets.contentstack.com endpoint return a 401 Unauthorized error. The same assets are accessible via other URLs.

**Root Cause**

The eu-assets.contentstack.com endpoint is not intended for CDN-based asset delivery. It is an internal or legacy endpoint that requires authentication and is not the correct URL for retrieving assets in the EU region.

**Resolution**

1.  Replace eu-assets.contentstack.com with eu-images.contentstack.com in all asset request URLs.
    
2.  The eu-images.contentstack.com endpoint is the correct CDN-based asset delivery URL for EU region stacks.
    
3.  Update any hardcoded URLs, SDK configurations, or integration settings that reference the incorrect endpoint.
    

After updating to the correct endpoint, request an asset URL using eu-images.contentstack.com and confirm a 200 response is returned with the expected asset content.

### Latest Published Entry Not Showing on Live Site - Client-Side Caching

The live site displays an older version of a published entry instead of the latest published version. Direct API calls (via cURL or Postman) return the correct latest version, confirming the CDA is serving the right content.

**Root Cause**

The discrepancy is caused by caching on the client side or at the front-end hosting layer, not by Contentstack. When the CDA API returns the correct latest version but the rendered site shows stale content, an intermediate cache (browser cache, CDN on the hosting platform, or front-end framework cache) is serving the older version.

**Resolution**

1.  Verify the CDA response directly using cURL or Postman. If the correct version is returned, the issue is not with Contentstack.
    
2.  Clear the front-end hosting platform’s cache (for example, Vercel, Netlify, or a custom CDN).
    
3.  Clear browser cache and test in an incognito window to rule out browser-level caching.
    
4.  Review the front-end application’s caching strategy and ensure published content invalidates the relevant cache on deploy or on a configurable TTL.
    

After clearing the client-side cache, reload the live site and confirm the latest published entry version is now displayed.

### CDA Serving Stale Content - Fastly Cache Not Purged

Published content changes are not reflected on the live site even after waiting beyond the expected cache refresh window. The CDA continues to return an older version of the entry. The issue resolves only after manual intervention.

**Root Cause**

The Fastly CDN layer used by Contentstack did not purge the cached version of the content following the publish event. In this scenario, the origin (Contentstack) holds the correct updated content but Fastly continues serving the stale cached response. This is a platform-level caching anomaly requiring engineering intervention.

**Resolution**

1.  Contact Contentstack Support and report the affected entry UID, environment, and the timestamp of the publish event.
    
2.  Support will escalate to the CDA engineering team, who can force a Fastly cache purge for the affected content.
    
3.  As an interim measure, append a unique cache-busting query parameter to the request URL (for example, ?cb=<timestamp>) to force a cache miss and retrieve fresh content directly from the origin.
    

After the Fastly cache is purged by engineering, request the affected URL without cache-busting parameters and confirm the latest content is returned.

### CDN Cache Refresh Timing After Publish and Unpublish Actions

After publishing or unpublishing content, there is an observable delay before the change is reflected in API responses. The expected behavior and timing of CDN cache refresh is unclear.

**Root Cause**

Contentstack automatically triggers a CDN cache purge when a publish, unpublish, or delete action occurs. The first request after the purge hits the origin server to retrieve the fresh content, and subsequent requests are served from the refreshed CDN cache. The time between the publish action and full CDN propagation is typically near-instant but may take a short period during high-load conditions.

**Resolution**

1.  Allow a brief propagation window after publishing before expecting the change to be universally reflected across all CDN nodes.
    
2.  If content is not updating after an extended period, verify the publish was successful by checking the publish queue in the CMS.
    
3.  For time-sensitive deployments, use cache-busting parameters in test requests to confirm the origin is returning updated content before CDN propagation completes.
    
4.  Note: There is no public API available for manually triggering a CDN cache clear. Cache purges are automatic on publish, unpublish, and delete events.
    

After publishing, wait for the propagation window and request the URL without cache-busting parameters. If the updated content is returned, the CDN has propagated the change.

### no-cache Directive Not Preventing CDN from Serving Stale Responses

Using a Cache-Control: no-cache header in API requests does not prevent the CDN from serving cached responses. Stale or inconsistent data continues to be returned despite the no-cache directive.

**Root Cause**

The no-cache directive instructs the CDN to revalidate cached content with the origin before serving it, but it does not prevent the CDN from storing the response. Under certain conditions, a CDN may interpret no-cache as permission to serve a stored response if revalidation is deferred or unavailable. The no-store directive is the correct directive to fully prevent caching and storage of a response.

**Resolution**

1.  Replace Cache-Control: no-cache with Cache-Control: no-store in requests where caching must be fully disabled.
    
2.  The no-store directive instructs the CDN and all intermediate caches not to store any version of the response, ensuring every request retrieves fresh content from the origin.
    
3.  Refer to the Contentstack CDN documentation for details on supported Cache-Control directives and their behavior within the Contentstack delivery infrastructure.
    

After switching to no-store, send the same request multiple times and confirm that each response reflects the latest origin data without CDN-served variations.

### High Percentage of API Calls Going to Origin Instead of CDN Cache

Approximately 30% or more of API calls are reaching the Contentstack origin server instead of being served from the CDN cache. This increases origin load and response latency.

**Root Cause**

A high origin hit rate is typically caused by the development or staging environment being configured to bypass CDN caching, or by cache-busting query parameters being appended to requests. Development environments often fetch content directly from origin by design to ensure fresh content during active development, which naturally produces a higher origin traffic proportion.

**Resolution**

1.  Review the environment configuration for all applications making CDA requests. Development environments may intentionally bypass the CDN and do not need optimization.
    
2.  For production environments, ensure requests use consistent, cacheable URL structures without dynamic query strings that create unique cache keys per request.
    
3.  Review any middleware, proxy configurations, or front-end caching settings that may be forwarding requests to origin unnecessarily.
    
4.  Monitor origin vs CDN hit ratios in Product Analytics after configuration changes.
    

After reviewing and correcting the configuration, monitor the origin hit rate. A well-configured production environment should have a CDN hit rate well above 70%.

### Error 109 - API Key Invalid or Stack Not Found (Wrong Regional Host)

API calls return the error: “We can’t find that Stack. Please try again.” with error\_code 109. The API key appears correct but the error persists.

**Root Cause**

Error 109 is returned when the API request is directed to a regional endpoint that does not host the stack. Contentstack infrastructure is region-specific (AWS NA, AWS EU, Azure NA, Azure EU, GCP EU, etc.). When the SDK or API client uses the default or wrong regional host, it cannot locate stacks that reside in a different region.

**Resolution**

1.  Identify the region in which the stack was created (visible in the Contentstack dashboard URL or stack settings).
    
2.  Update the SDK configuration to use the correct regional host. For example, for Azure NA: Stack.setHost(‘azure-na-api.contentstack.com’)
    
3.  For direct API calls, ensure the base URL matches the stack’s region. Examples:
    

*   AWS NA: cdn.contentstack.io
    
*   AWS EU: eu-cdn.contentstack.com
    
*   Azure NA: azure-na-cdn.contentstack.com
    
*   Azure EU: azure-eu-cdn.contentstack.com
    

1.  Re-run the request after updating the host and confirm a valid response is returned.
    

After correcting the regional host, execute the API call and confirm the stack is found and the response is returned without error 109.

### 401 Errors Caused by Using a Preview Token Instead of a Delivery Token

Intermittent 401 Unauthorized errors appear on CDA requests. The token appears valid because it works for some requests but fails on others.

**Root Cause**

The token being used is a preview token, not a delivery token. Preview tokens are valid for Preview API requests but are not authorized for the standard CDA (cdn.contentstack.io) endpoints. When a preview token is used on a delivery endpoint, the API returns a 401 error because the token type does not match the endpoint’s authorization requirements.

**Resolution**

1.  Review the token configured in the application or SDK and confirm its type in Settings > Tokens.
    
2.  If the token is a Preview Token, replace it with a Delivery Token scoped to the correct environment.
    
3.  Ensure that delivery tokens and preview tokens are never interchanged - use delivery tokens for CDA production requests and preview tokens only for Preview API requests.
    

After replacing the preview token with the correct delivery token, re-run the affected CDA requests and confirm that 401 errors no longer occur.

### 412 Precondition Failed - Stack Not Found After Wrong Regional Base URL

After activating a Contentstack instance and running the starter kit, a Precondition Failed error is returned with the message: “We can’t find the stack.” The API key and credentials appear correct.

**Root Cause**

The starter kit or application is configured with a base URL pointing to the wrong cloud region. For example, an instance provisioned on Azure is being accessed using the AWS base URL. Each Contentstack cloud region uses a distinct base URL, and using a mismatched URL causes the stack lookup to fail with a 412 error.

**Resolution**

1.  Identify the cloud region for the Contentstack instance (AWS NA, Azure NA, AWS EU, Azure EU, etc.) from the dashboard or provisioning confirmation.
    
2.  Update the base URL in the starter kit or application configuration to match the correct region. For example, for Azure NA the API base URL is azure-na-api.contentstack.com.
    
3.  Refer to the Contentstack region-specific documentation for the correct base URLs for each region.
    

After updating the base URL to the correct regional endpoint, re-run the starter kit and confirm that the stack is found and API calls return successfully.

### 422 Error on Image URL - Malformed Query String with Multiple Question Marks

Dynamically generated image URLs return 422 errors while static image URLs work correctly. The URLs appear similar but the dynamic version consistently fails.

**Root Cause**

The dynamic URL is malformed because multiple ? characters are present in the query string. This occurs when parameters are appended incorrectly - for example, adding ?environment=production after a URL that already contains ?auto=webp results in two separate query strings, which is invalid URL syntax. The server cannot parse the malformed URL and returns a 422 error.

**Resolution**

1.  Ensure that the first parameter in the URL uses ? and all subsequent parameters use &.
    
2.  Correct example: https://images.contentstack.io/v3/assets/{uid}/{asset}?auto=webp&environment=production&quality=80
    
3.  Incorrect example (two ? characters): https://images.contentstack.io/v3/assets/{uid}/{asset}?auto=webp?environment=production
    
4.  Review dynamic URL construction logic in the application code and validate that parameter concatenation always uses & after the first ?.
    

After correcting the URL construction logic, test a dynamically generated image URL and confirm a 200 response is returned with the expected image.

### 422 Errors Caused by Incorrect Locale Configuration

CDA requests return 422 Unprocessable Entity errors in production. The requests appear structurally valid and the same configuration worked previously.

**Root Cause**

The 422 errors are caused by an invalid or incorrectly formatted locale value being passed in the API request. If the locale code does not match any locale configured in the stack, the API returns 422 because it cannot process the request against an unrecognized locale.

**Resolution**

1.  Review the locale parameter in the failing API requests and confirm it matches a locale code configured in the stack (Settings > Languages).
    
2.  Check for typos, incorrect case, or locale codes that have been removed from the stack configuration.
    
3.  Test the request with a known valid locale (for example, en-us) to confirm the 422 error is locale-specific.
    
4.  Correct the locale value in the application configuration and re-deploy.
    

After correcting the locale value, re-run the API request and confirm a valid response is returned without a 422 error.

### Deleted Field Still Appearing in API Responses After Branch Schema Update

A field deleted from a content type in one branch (for example, main) continues to appear in API responses when querying other branches (for example, production) or when the entry is fetched directly.

**Root Cause**

Content type schema changes, including field deletions, are branch-specific in Contentstack. Deleting a field in one branch does not automatically remove it from other branches. The field and its data persist in branches where the schema has not been updated, so the API continues to return the field for those branches.

**Resolution**

1.  Apply or merge the schema change (field deletion) to all branches where the field should be removed.
    
2.  After updating the schema in each branch, verify the content type no longer includes the deleted field.
    
3.  Re-run the API request against each branch and confirm the deleted field is no longer present in the response.
    

After updating the schema across all relevant branches, execute the API call and confirm the deleted field does not appear in any branch’s response.

### API Calls Return Mismatched _version Values for List vs Single Entry Requests

Fetching a list of entries via the CDA returns different \_version values compared to fetching the same entry individually. The same entry appears to have a different version depending on which request is used.

**Root Cause**

The list request is being made without an access token (delivery token), causing the request to return unauthenticated results, which may reflect a different or default version of the entry. The single-entry request includes the access token and therefore returns the correct, authenticated version. Different authentication states can produce different responses for the same entry.

**Resolution**

1.  Add the correct delivery access token to the headers of the list request: access\_token: <your\_delivery\_token>
    
2.  Ensure all API requests - both list and single-entry - include the access token and target the same environment.
    
3.  Re-run both requests and confirm that the \_version values are now consistent.
    

After adding the access token to the list request, compare the \_version values from the list and single-entry responses. If they now match, the authentication mismatch has been resolved.

### Error Code 118 - Content Type Not Found

API calls to fetch entries for a specific content type return Error Code 118 with the message Content Type not found. The content type appears to exist in the CMS.

**Root Cause**

Error 118 is returned when the content type UID referenced in the API request is invalid, inaccessible, or not available in the queried environment. Common causes include:

*   The content type UID in the URL does not match the actual UID in the stack (case-sensitive mismatch or typo)
    
*   The content type exists in a different branch or environment than the one being queried
    
*   The delivery token being used does not have access to the environment containing the content type
    
*   The API key being used does not correspond to the stack containing the content type
    

**Resolution**

1.  Verify the content type UID exactly as it appears in the CMS (Settings > Content Types). UIDs are case-sensitive.
    
2.  Confirm the delivery token has access to the target environment.
    
3.  Confirm the API key matches the stack containing the content type.
    
4.  Ensure the request is targeting the correct branch if branches are in use.
    

After correcting the content type UID, token, and environment configuration, re-run the API request and confirm a valid response is returned without error 118.

### SDK Not Reflecting Published Entry Updates - Wrong SDK Import

Entry updates are visible via CMA, direct CDA calls, and cURL, but changes are not reflected in the application when using the TypeScript or JavaScript SDK. The SDK appears to be fetching stale or incorrect data.

**Root Cause**

The application is using an incorrect or mismatched SDK import. For example, importing the Content Management SDK when the Delivery SDK is required, or using an import path that points to a cached or incorrectly resolved module. This causes the SDK to query a different endpoint or use incorrect credentials, returning outdated or mismatched data.

**Resolution**

1.  Verify the SDK import statement in the application code. For delivery use cases, ensure the import is from the Contentstack Delivery SDK, not the Management SDK.
    
2.  Correct delivery SDK import example: import Contentstack from ‘@contentstack/delivery-sdk’
    
3.  Confirm the SDK is initialized with the correct API key, delivery token, and environment.
    
4.  Clear the module cache (npm cache clean --force or equivalent) and reinstall dependencies if the import appears correct but the issue persists.
    

After correcting the SDK import, re-run the application query and confirm that the latest published entry data is returned.

### CORS 405 Preflight Error on the Content Delivery API

A browser-based application fails to fetch content from the Contentstack Delivery API. The browser reports a CORS error and the network inspector shows the OPTIONS preflight request receiving a 405 Method Not Allowed response, which prevents the actual GET request from executing.

**Root Cause**

A 405 error on the CORS preflight OPTIONS request indicates that the Delivery API endpoint is not returning the required CORS headers (Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers) in the OPTIONS response. This is a platform-level issue where the endpoint’s CORS configuration is incomplete or incorrectly handling preflight requests from the requesting origin.

**Resolution**

1.  Confirm the error is a CORS preflight failure by inspecting the browser’s network tab. Look for an OPTIONS request to the Delivery API URL that returns 405.
    
2.  Contact Contentstack Support and report the affected endpoint URL, the requesting origin (the domain making the browser request), and the environment.
    
3.  Engineering will identify and correct the CORS header configuration for the affected endpoint.
    
4.  As a short-term workaround, route Delivery API requests through a server-side proxy that adds the required CORS headers before the response reaches the browser. This avoids the browser making the preflight request directly to the Contentstack endpoint.
    

After engineering resolves the CORS configuration, retry the browser-based request. If the OPTIONS preflight request returns a 200 or 204 with the required Access-Control-Allow-\* headers and the subsequent GET request succeeds, the CORS issue is resolved.

### Empty Single Line Text Field Returns Empty String, Not undefined

When a Single Line Text field is left empty in an entry and the entry is fetched via the CDA, the field is returned as an empty string (““) in the response instead of being absent or returning undefined. This differs from the expectation that an empty field would be omitted.

**Root Cause**

Empty Single Line Text fields are intentionally stored and returned as empty strings by the Contentstack CDA. This ensures a consistent, predictable response structure where all declared fields in the content type schema are always present in the API response, regardless of whether content has been entered. Returning “” instead of omitting the field prevents null reference errors in front-end applications that expect the field to always exist.

**Resolution**

This is expected platform behavior and is not a bug. To handle empty Single Line Text fields in the application:

1.  Check for empty string (““) rather than null or undefined when evaluating whether a Single Line Text field has content.
    
2.  Implement a utility function that normalizes empty strings to null or undefined if the application requires that distinction.
    
3.  Do not rely on field absence as a signal for empty content - use explicit empty string checks instead.
    

After updating the application’s field evaluation logic to check for empty strings, confirm that empty Single Line Text fields are correctly identified and handled without runtime errors.

### Fetching created_by and updated_by for Content Types via API

There is no direct field on content type API responses for the creator or last modifier details. The created\_by and updated\_by information is needed for programmatic user management or audit purposes.

**Root Cause**

The CMA does not include created\_by and updated\_by fields on content type API responses. This information is recorded in the audit log rather than in the content type schema response.

**Resolution**

1.  Use the Contentstack Audit Log API to retrieve creator and modifier details for content types. The audit log records create and update events with the associated user information.
    
2.  Call GET /v3/audit-logs with appropriate filters to retrieve content type activity.
    
3.  For last-login and user management use cases, export users from Organization Settings > Users as a CSV file, which includes the Last Login field. Filter the CSV to identify inactive users.
    

After querying the Audit Log API, confirm that the creator and modifier details for content types are present in the response.

### Version Field Absent from Entry Response When Global Fields Are Present

The version field (\_version) is present in the API response when fetching a global field independently, but is absent from the entry response when the entry contains that global field.

**Root Cause**

The version field in Contentstack represents the version of the top-level object being fetched. When fetching an entry that includes a global field, the \_version in the response reflects the entry’s version, not the global field’s version. The global field itself does not independently contribute a version number to the parent entry response - its version is only visible when the global field is fetched directly.

**Resolution**

1.  To retrieve the version of the global field itself, fetch it directly via the global fields API endpoint.
    
2.  To retrieve the version of the entry, use the standard entry fetch endpoint - the \_version field in the entry response reflects the entry’s version.
    
3.  If the intent is to track changes to global fields embedded within entries, use the Audit Log API to view modification history.
    

After fetching the global field directly, confirm that the \_version field is present in the response and reflects the expected version number.

### Using the only[] Parameter to Simplify Delivery-to-Management API Conversion

Entries retrieved from the Delivery API require extensive manual restructuring before they can be used in Management API update requests. The response includes fields and metadata that the Management API does not accept or requires in a different format.

**Root Cause**

The Delivery API and Management API return and accept different response structures by design. The Delivery API includes resolved references, environment metadata, and flattened fields that are not part of the Management API’s update schema. Fetching the full entry from the Delivery API and passing it directly to the Management API without restructuring produces errors.

**Resolution**

1.  Use the only\[\] parameter in the Delivery API request to fetch only the specific fields required for the Management API update, reducing the need for manual restructuring.
    
2.  Example: GET /v3/content\_types/{uid}/entries/{entry\_uid}?only\[BASE\]\[\]=title&only\[BASE\]\[\]=description
    
3.  Alternatively, fetch the entry via the CMA (Management API) using a management token to retrieve it in the native management schema, which is directly compatible with update requests.
    

**Note - Excluding Metadata Fields (updated\_by, updated\_at, created\_by, etc.)**

If the goal is to receive cleaner API responses without system metadata fields (such as updated\_by, updated\_at, created\_by, created\_at, \_version), the REST API does not support excluding these fields natively. However, GraphQL provides a direct solution: because GraphQL uses explicit field selection, metadata fields can simply be omitted from the query selection set and will not appear in the response. This also eliminates the need for long URL query strings when selecting specific fields.

After using the only\[\] parameter or switching to a CMA fetch, confirm that the response structure requires minimal transformation before being used in a Management API update call.

### Regex Queries Work in CMA but Fail in CDA

A regex-based query filter works correctly when executed against the Content Management API but returns an error or no results when the same query is run against the Content Delivery API.

**Root Cause**

The CMA had a regex validation bypass enabled, which allowed unsafe or complex regex patterns. The CDA enforces strict validation of regex patterns and requires them to be safe (non-catastrophic) regex expressions. Patterns that bypass CMA validation may fail CDA validation. The bypass was disabled to protect CDA performance and stability.

**Resolution**

1.  Review the regex pattern used in the query and ensure it is a safe, well-bounded expression (no catastrophic backtracking potential).
    
2.  Test the updated regex pattern against the CDA endpoint.
    
3.  Avoid using open-ended quantifiers (such as .\* or .+) without anchors in regex filters, as these are more likely to be rejected by CDA validation.
    
4.  If safe regex patterns are required for the use case but are being rejected, contact Contentstack Support to review the specific pattern.
    

After updating the regex to a safe pattern, re-run the CDA query and confirm that results are returned without a validation error.

### Querying Entries by Taxonomy Terms via the Delivery API

There is no clear guidance on how to filter or retrieve entries based on specific taxonomy terms using the CDA REST API.

**Root Cause**

Taxonomy-based filtering is available in the CDA but requires the correct query parameter syntax to target taxonomy terms. The query structure differs from standard field-based filtering.

**Resolution**

1.  Use the taxonomies.term\_uid query parameter in the CDA request to filter entries by a specific taxonomy term.
    
2.  Example: GET /v3/content\_types/{uid}/entries?query={“taxonomies.term\_uid”:{“$in”:\[“term\_uid\_value”\]}}
    
3.  Refer to the Contentstack Taxonomy documentation for the full list of supported query operators for taxonomy filtering.
    
4.  Combine taxonomy filters with other query parameters as needed using standard and/or operators.
    

After applying the taxonomy term filter, execute the API request and confirm that only entries tagged with the specified taxonomy term are returned.

### Modular Block Order Differs Between CDA Response and CMS UI

The order of modular blocks returned by the Content Delivery API does not match the order displayed in the Contentstack CMS entry editor. The CDA response appears to sort or reorder blocks differently.

**Root Cause**

The CDA API may not preserve the exact UI-defined order of modular blocks in all response scenarios. The CMA API response preserves the modular block order as defined in the entry editor.

**Resolution**

1.  Use the CMA API instead of the CDA API when modular block order is critical to the application.
    
2.  Authenticate the CMA request with a management token and fetch the entry via: GET /v3/content\_types/{uid}/entries/{entry\_uid} with the management token in the headers.
    
3.  The CMA response preserves the modular block sequence as defined in the CMS UI.
    
4.  If using the CDA is required, implement client-side sorting based on an explicit order field added to each modular block in the content model.
    

After switching to the CMA API for the modular block fetch, compare the response order with the CMS UI. If the order matches, the CMA is correctly preserving the block sequence.

### Reducing API Call Count and Improving Delivery Performance

API usage significantly exceeds expected limits. The application is generating a high volume of CDA calls and guidance is needed on how to reduce consumption without impacting content delivery.

**Root Cause**

High API call counts are commonly caused by inefficient content modeling, redundant requests, deeply nested reference resolution on every page load, and lack of caching at the application layer.

**Resolution**

*   Use GraphQL instead of REST for queries requiring specific field selection, reducing over-fetching. Be mindful of the 8,192-byte GraphQL query size limit.
    
*   For REST, use the only\[\] parameter to fetch only required fields and reduce response payload.
    
*   Flatten deep reference chains in the content model where possible to reduce include\_depth requirements per request.
    
*   Paginate large datasets using limit and skip rather than fetching all entries in a single large request.
    
*   Implement server-side or edge caching to serve repeated identical queries from cache rather than making a new CDA call each time.
    
*   Review the Product Analytics dashboard (accessible to Org Owners and Admins) to identify the highest-traffic endpoints and content types, then target optimizations accordingly.
    
*   For static site generation, pre-fetch and cache all required content at build time to reduce runtime API calls.
    

After implementing caching and query optimization, monitor API usage in Product Analytics over a 7-day window. If total call counts decrease toward expected levels, the optimizations are effective.

### $exists:false Queries Are Significantly Slower Than $exists:true

CDA queries using $exists: false on a field (for example, hero\_video) have significantly higher response times compared to queries using $exists: true on the same field. The performance difference is consistent.

**Root Cause**

Queries using $exists: false require a full collection scan to identify entries where the field is absent, because the absence of a field cannot be indexed in the same way as its presence. $exists: true queries can leverage an index on the field, making them fast. The $exists: false condition cannot benefit from the field index, resulting in much higher query execution time on large datasets.

**Resolution**

1.  Add additional indexed field filters to the $exists: false query to reduce the scan scope. For example, filter on a content type or status field that is indexed, in addition to the $exists condition.
    
2.  Alternatively, add a dedicated boolean field (for example, has\_hero\_video: false) to the content model. Set this field explicitly when creating or updating entries. The boolean field can be indexed and queried with $exists: true, achieving the same result with better performance.
    
3.  If the performance issue is severe and the content model cannot be changed, contact Contentstack Support and request that the specific field be added to the index for the stack.
    

After adding the additional filter or the dedicated boolean field, re-run the query and measure the response time. If the latency is reduced to a level comparable to $exists: true queries, the optimization is effective.

### Contentstack Assets Are Indexed by Google Search

PDF files, images, and other assets uploaded to Contentstack are appearing in Google search results. The assets are publicly accessible via their direct URLs, which allows search engines to discover and index them.

**Root Cause**

Contentstack asset URLs are publicly accessible by default once an asset is uploaded, regardless of its publish status. If asset URLs are embedded in publicly accessible pages, shared externally, or discovered via sitemaps, search engine crawlers can index them. Contentstack does not apply noindex headers or robots restrictions to assets by default.

**Resolution**

To prevent asset indexing going forward:

1.  Implement secure asset URLs by enabling token-based access for assets in the stack settings. This makes direct URL access require authentication, preventing public crawler access.
    
2.  Serve assets through a custom domain with appropriate robots.txt rules and X-Robots-Tag: noindex headers to instruct crawlers not to index the asset URLs.
    
3.  Remove all publicly accessible links to assets that should not be indexed.
    
4.  To de-index already indexed assets, use the Google Search Console URL Removal tool to request de-indexing of specific asset URLs.
    

After implementing token-based asset access, confirm that unauthenticated requests to asset URLs return 401 errors, preventing public crawler access.

### Custom Domain CDN (Akamai) Returning 404 for Asset Paths - Host Header Misconfiguration

Assets requested via a custom Akamai CDN domain return 404 errors for all asset paths (/v3/assets/\*). Direct requests to the Contentstack origin return 200 OK, confirming the assets exist and are accessible.

**Root Cause**

Akamai is forwarding an incorrect Host header to the Contentstack origin. When the Host header contains the customer’s custom domain instead of the Contentstack CDN domain, the Contentstack origin cannot match the request to the correct stack and returns 404. The Akamai property’s origin configuration is also misconfigured, pointing to the wrong origin hostname.

**Resolution**

1.  In the Akamai property settings, update the Origin Hostname to the correct Contentstack CDN domain: images.contentstack.io (or eu-images.contentstack.com for EU region stacks).
    
2.  Set the Forward Host Header in Akamai to Origin Hostname to ensure the correct Host header is forwarded to Contentstack.
    
3.  Do not use the customer’s custom domain as the value forwarded in the Host header to the Contentstack origin.
    
4.  After updating the Akamai configuration, test a direct asset request through the custom domain and confirm a 200 response is returned.
    

After correcting the Akamai origin hostname and Host header forwarding settings, request an asset via the custom domain. If a 200 response is returned with the expected asset content, the configuration is correct.

### CDA Always Returns Single-Value Fields as Arrays

The Content Delivery API returns certain fields as arrays in the JSON response even when the field contains only a single value. This is unexpected for developers who anticipate a scalar value for single-entry fields.

**Root Cause**

This is intentional system design. The Contentstack CDA returns fields as arrays to ensure a consistent and predictable response structure across all locales and content variations. A field that contains one value in one locale may contain multiple values in another locale (for example, a multi-select or reference field). Using arrays for all such fields ensures the application code does not need to handle both scalar and array types for the same field depending on the locale or content state.

**Resolution**

This is expected platform behavior and cannot be changed. To handle single-value array fields in the application:

1.  Access the value using array index notation: field\[0\] to retrieve the first (and typically only) element.
    
2.  Implement a normalization utility that checks whether a field is a single-item array and extracts the scalar value where needed.
    
3.  Design application code to consistently treat these fields as arrays regardless of the number of values, which is the safest and most future-proof approach.
    

After updating the application to access field values using array notation, confirm that the expected values are retrieved correctly without type errors.

### Intermittent 429 Rate Limit Errors in Serverless and Launch Architectures

A website hosted on Contentstack Launch or a serverless platform (such as Vercel or Netlify) returns intermittent HTTP 429 Too Many Requests errors from the GraphQL API. The errors appear during deployments, content updates, or when multiple visitors trigger server-side rendering simultaneously. Because the environment is stateless and scales horizontally, standard rate limit management approaches that rely on shared in-memory state do not work.

**Root Cause**

Serverless and edge function architectures create multiple isolated execution contexts (function instances) simultaneously. Each context makes independent GraphQL requests without awareness of how many requests the other instances are sending. The aggregate request volume across all concurrent instances can easily exceed the organization’s GraphQL rate limit (typically 80–200 requests per second), even when each individual instance appears to be making a modest number of calls. This is compounded during deployments when cache warming triggers many simultaneous requests.

**Resolution**

**Short-term: Reduce request volume during high-concurrency events**

1.  Implement ISR (Incremental Static Regeneration) or static generation for content that does not change frequently. Pre-building pages at deploy time eliminates runtime GraphQL calls for those routes. Note: ISR is a Next.js-specific feature - other frameworks have equivalent static or deferred generation patterns (for example, Gatsby’s deferred static generation, Nuxt’s static target, or Astro’s static output mode). Apply the equivalent pattern for your framework.
    
2.  Add response caching at the CDN layer (Contentstack’s built-in CDN caches GraphQL responses for identical queries). Ensure query structure is consistent so cache hits are maximised rather than each instance generating a unique cache-busting request.
    
3.  During planned deployments, stagger the cache warming process - use a throttled crawler or regeneration script that paces requests rather than triggering all pages simultaneously.
    

**Medium-term: Manage concurrency at the application layer**

1.  Implement a token bucket or leaky bucket rate limiter using a shared external store (such as Redis, Upstash Redis, or a Cloudflare KV store) that all serverless instances can read and write to. This creates a global request counter that prevents the aggregate rate from exceeding the limit.
    
2.  Alternatively, route all GraphQL requests through a single lightweight API layer (a dedicated server or durable compute instance) that centralises rate limit enforcement before forwarding requests to Contentstack.
    

**Long-term: Reduce total request count**

1.  Review the site architecture to identify which pages truly need server-side GraphQL calls and which can be served from a static or ISR build.
    
2.  Consolidate multiple GraphQL queries per page into fewer, broader queries to reduce the total number of API calls per page render.
    
3.  Contact Contentstack Support to request a rate limit review if the architecture genuinely requires higher throughput than the current limit allows.
    

After implementing ISR or centralized rate limiting, monitor the GraphQL error rate during the next deployment and content update cycle. If 429 errors cease or are significantly reduced, the rate limiting strategy is effective.

### ‘Network Request Failed’ Error With No HTTP Status Code

GraphQL API calls from a browser-based or server-rendered application return a ‘Network request failed’ error with no HTTP status code. The error indicates the request never completed rather than receiving an error response from Contentstack.

**Root Cause**

A ‘Network request failed’ pattern with no HTTP status code means the HTTP connection was not established or was interrupted before a response was received. This is a client-side or network-side failure, not a Contentstack API error. Common causes include:

*   CORS preflight failure: the browser’s OPTIONS preflight request is blocked or returns an unexpected response, preventing the actual GraphQL request from being sent.
    
*   DNS resolution failure: the hostname graphql.contentstack.com cannot be resolved in the execution environment (common in corporate networks, VPCs, or custom DNS configurations).
    
*   TLS/SSL handshake failure: the client cannot establish a secure connection due to certificate validation errors, an outdated CA bundle, or a TLS version mismatch.
    
*   Network-level blocking: a corporate firewall, proxy, or VPN intercepts or drops outbound HTTPS requests to Contentstack endpoints.
    
*   Request timeout: the connection attempt times out before a response is received, often in serverless environments with short execution windows.
    

**Resolution**

**Step 1 - Isolate the failure type**

1.  Test the GraphQL endpoint directly using cURL from the same environment where the failure occurs: curl -v -X POST https://graphql.contentstack.com/stacks/{api\_key} -H ‘Content-Type: application/json’ -d ‘{“query”:“{\_\_typename}”}’
    
2.  If cURL succeeds but the application fails, the issue is in the application’s HTTP client configuration (CORS, proxy, or TLS settings), not in the network.
    
3.  If cURL also fails, the issue is at the network level (DNS, firewall, or VPN).
    

**Step 2 - CORS (browser-based applications)**

1.  Open the browser’s developer tools and check the Network tab for a failed OPTIONS preflight request to the GraphQL endpoint.
    
2.  Verify that the request is being made to the correct regional GraphQL URL and that no proxy is altering the request headers.
    
3.  If CORS headers are missing from the preflight response, contact Contentstack Support - CORS configuration for the GraphQL endpoint may need to be updated.
    

**Step 3 - DNS resolution (server-side or VPC environments)**

1.  Run nslookup graphql.contentstack.com or dig graphql.contentstack.com from within the execution environment to confirm DNS resolution is working.
    
2.  If DNS fails, add a DNS override or configure a custom DNS resolver that can reach public DNS. Check VPC or corporate network DNS policies.
    

**Step 4 - TLS/SSL issues**

1.  Check whether the runtime environment has an up-to-date CA certificate bundle. For Node.js, update to a recent LTS version to ensure the CA bundle is current.
    
2.  If a corporate proxy performs SSL inspection, add the proxy’s CA certificate to the trusted certificate store.
    

After identifying and resolving the network-level cause, re-run the GraphQL request and confirm a valid response is returned.

### GraphQL Explorer UI Issues - Scroll, Disappearing Components, Interaction Disruptions

The Contentstack GraphQL Explorer in the dashboard exhibits UI instability: scroll functionality is inconsistent or stops working, certain UI components disappear during interaction, and general usability is disrupted, making it difficult to build and test queries.

**Root Cause**

GraphQL Explorer UI issues are typically caused by one of the following: a browser-specific rendering incompatibility, a browser extension interfering with the Explorer’s JavaScript, a cached version of the Explorer’s assets that conflicts with a recent platform update, or a platform-level bug in the Explorer interface that requires an engineering fix.

**Resolution**

1.  Clear the browser cache (Ctrl+Shift+Delete or equivalent) and reload the GraphQL Explorer.
    
2.  Open the Explorer in a new incognito or private browsing window to rule out browser extension interference.
    
3.  Test in a different browser. If the Explorer works in one browser but not another, the issue is browser-specific.
    
4.  Disable browser extensions one by one to identify if an extension (such as an ad blocker, dark mode extension, or developer tool) is interfering with the Explorer.
    
5.  If the issue persists across browsers and in incognito mode, contact Contentstack Support and provide a screen recording or screenshots of the specific UI behavior, the browser version, and the operating system. Engineering will investigate whether a platform-level fix is required.
    

After clearing the cache and testing in incognito mode, confirm whether the GraphQL Explorer loads and functions correctly. If it does, a browser cache or extension was the cause.

### relative_urls=true Has No Effect on Content Delivery API Asset Requests

The relative\_urls=true query parameter is added to a Content Delivery API (CDA) request for Get All Assets or Get a Single Asset. Despite being included, the url field continues to return a full absolute URL starting with https://. The parameter appears to have no effect.

**Root Cause**

The relative\_urls=true parameter is supported only in the Content Management API (CMA), not in the Content Delivery API (CDA). When the parameter is passed in a CDA request, it is silently ignored - the CDA always returns absolute URLs for asset fields. This was previously documented incorrectly and the Contentstack documentation has since been updated to clarify that relative\_urls is a CMA-only parameter.

**Resolution**

There is no supported way to retrieve relative asset URLs from the Content Delivery API. To work with relative URLs for assets:

1.  If relative URLs are needed for asset management or internal tooling, use the Content Management API (CMA) with a management token and include relative\_urls=true in the CMA request.
    
2.  If the use case is front-end rendering, extract the relative path client-side by stripping the domain from the absolute URL returned by the CDA. For example: new URL(absoluteUrl).pathname
    
3.  Do not rely on relative\_urls=true in CDA requests - the parameter has no effect and the absolute URL will always be returned.
    

After switching to the CMA for asset requests (if relative URLs are required), confirm the url field returns a relative path. For front-end use cases, apply client-side URL path extraction from the absolute URL returned by the CDA.

### Inconsistency Between GraphQL Delivery API and GraphQL Live Preview Responses

The same GraphQL query returns different data when executed against the standard GraphQL Delivery API versus the GraphQL Live Preview API. Specifically, nested child objects or referenced content that appears in the standard delivery response is missing or empty in the Live Preview response.

**Root Cause**

The GraphQL Live Preview API and the standard GraphQL Delivery API use different data resolution mechanisms. The Live Preview API fetches the draft state of the requested entry but does not always resolve deeply nested referenced entries in the same way as the Delivery API. Specifically:

*   The Live Preview API resolves the top-level entry in its draft state, but referenced child entries are resolved from the delivery layer, not the draft layer.
    
*   If a child entry has not been published (or has only recently been published without cache propagation), it may not be available in the resolution path used by the Live Preview API.
    
*   The Live Preview API also has known limitations with certain nested structures compared to the full delivery GraphQL schema.
    

**Resolution**

1.  Verify that all referenced child entries are published to the target environment. Unpublished child entries will not be resolved in either the delivery or live preview response.
    
2.  After publishing child entries, clear any cached state and re-run the Live Preview query to confirm the nested data appears.
    
3.  If child entries are published but still missing in the Live Preview response, contact Contentstack Support and provide: the GraphQL query, the top-level entry UID, the missing child entry UIDs, and the Live Preview token being used.
    
4.  As a workaround, if the missing data is not in draft state (it is already published and visible in the standard delivery response), use the standard Delivery API response for the affected nested fields rather than re-fetching through the Live Preview endpoint.
    

After publishing all referenced child entries and re-running the Live Preview query, confirm that nested data is now returned consistently between the Delivery API and Live Preview API responses.

### personalize.AUDIENCES.RULE_COUNT_EXCEEDED Error in GraphQL

A GraphQL request returns the error personalize.AUDIENCES.RULE\_COUNT\_EXCEEDED. The error prevents audience-based personalization rules from being applied and causes GraphQL queries that use personalization to fail.

**Root Cause**

This error occurs when the number of rules configured within a Personalize audience exceeds the organization’s personalizeRulesPerAudience limit. The default limit is 50 rules per audience. When the number of configured rules reaches or exceeds this threshold, new rules cannot be added and existing personalization queries that attempt to evaluate audiences with excessive rules return this error.

**Resolution**

1.  Review the Personalize project configuration and identify audiences that have a large number of rules configured.
    
2.  Where possible, consolidate or simplify audience rules to stay within the current limit.
    
3.  If consolidation is not feasible and the use case genuinely requires more than 50 rules per audience, contact Contentstack Support and provide: the Personalize project ID and the stack API key. Request an increase to the personalizeRulesPerAudience limit. The maximum supported limit is 100 rules per audience.
    
4.  After the limit is increased by Support, verify the personalization rules are applied correctly by re-running the affected GraphQL query.
    

After the limit increase is applied, re-run the GraphQL query that was returning the error. If the query executes successfully and returns personalized content, the audience rule limit has been resolved.

<!-- case:00060720 status:draft synced:false bucket:"API Delivery, GraphQL & Assets" -->
### Descending Sort Places Lowercase Values Before Uppercase

Sorting entries in descending order by a text field may place values beginning with lowercase characters before values beginning with uppercase characters, appearing out of alphabetical order.

**Root Cause**

Descending sort is case-sensitive and orders values by character code rather than human alphabetical order. Because lowercase characters have higher character values than uppercase characters, entries starting with lowercase letters can appear before uppercase entries in descending order.

**Resolution**

1.  Check whether the sorted field contains a mix of uppercase and lowercase starting characters.

2.  Maintain a consistent casing convention for the field's values if alphabetical ordering is required.

3.  Alternatively, perform a case-insensitive sort at the application level after retrieving the entries.

After applying a consistent casing convention or sorting case-insensitively at the application level, confirm the entries display in the expected alphabetical order. If the ordering matches expectations, the issue is resolved. Escalate with the field UID and a sample of the affected values if the ordering still appears incorrect.

<!-- end:00060720 -->

## Webhooks & External Integrations

### Entry Publish Failed - Webhook Not Triggered as a Result

A common misconception is that webhooks fail to trigger during the publishing process. However, if the publishing event itself is blocked, often due to validation errors in referenced entries, the webhook event never occurs and therefore cannot fire. This should be framed as a publishing failure rather than a webhook malfunction.

**Root Cause**

The primary cause is that the Entry Publish Failed. Specifically:

*   **Incomplete Referenced Entries**: Referenced entries with missing mandatory fields or validation errors block the parent entry from publishing.
*   **Event Suppression**: Because webhooks trigger only when an event (like a successful publish) actually occurs, a blocked publish means the trigger event never happens.

**Resolution**

*   **Identify Publishing Blockers**: Check the publishing logs to confirm if the entry failed due to validation errors in referenced content.
*   **Fix Mandatory Fields**: Navigate to the referenced entries and ensure all mandatory fields are correctly populated.
*   **Expand Referenced Entries**: Verify all levels of nested references to ensure no sub-entry is blocking the chain.
*   **Retry Publishing**: Once references are corrected, re-attempt to publish the parent entry.

The webhook fires successfully once the publishing event is officially recorded in the system.

### Webhook Delivery Fails Due to IP Whitelisting or Network Restrictions

Webhook endpoints do not receive requests after an event is triggered.

**Root Cause**

Firewall, IP allowlists, or network restrictions block incoming requests from Contentstack webhook IP addresses.

**Resolution**

*   Allowlist the official Contentstack webhook IP addresses. Refer to the documentation.
*   Verify firewall and security group rules. Ensure inbound HTTPS (port 443) traffic from Contentstack IP ranges is permitted.
*   **Confirm endpoint response behavior:** Ensure the webhook endpoint returns a 2xx HTTP status code for successful requests.
*   Review server logs:
    *   Check application/server logs for rejected or blocked IP addresses.
    *   Look for 403, 401, or connection timeout entries.

Trigger a test webhook event.

**Confirm:**

*   The endpoint receives the request.
*   The endpoint returns a 2xx response.
*   No IP-based rejection appears in server logs.
*   The webhook remains in an active state in the CMS.

### Webhooks Disabled Automatically Due to Endpoint Failures

Webhooks are automatically disabled after repeated failures (e.g., multiple non-2xx responses). Failures include timeouts, 5xx responses, and unreachable endpoints.

**Root Cause**

Circuit breaker behavior disables unhealthy webhooks to protect the platform.

**Resolution**

*   Manually re-enable the webhook.
*   Configure email notifications for future alerts.

The webhook remains active after recovery.

### Excessive Webhook Traffic Causes 429 Errors

Webhook executions fail with **HTTP 429** responses when Contentstack attempts to deliver events to the configured endpoint.

**Root Cause**

In this case, the 429 is returned by the customer’s receiving system, not by Contentstack. This typically happens when the receiving endpoint enforces its own rate limits, retry loops cause traffic spikes, or multiple webhooks fire simultaneously (bulk publish, branch merge, etc.).

**Resolution**

*   Review webhook execution logs.
*   Check receiving system rate limits.
*   Implement:
    *   Idempotency handling
    *   Queue-based processing
    *   Throttling on the receiving system
*   Avoid webhook recursion or retry storms.

Confirm if:

*   Webhook delivery logs show successful (2xx) responses.
*   No further 429 responses from receiving endpoint.
*   No excessive retry attempts.

### Webhook Authentication Configuration Confusion

Uncertainty around whether to use Basic Auth or OAuth for webhook authentication.

**Root Cause**

Multiple authentication options can cause configuration confusion.

**Resolution**

*   Select the appropriate authentication method.
*   Disable Basic Auth if it is not required.

Webhook authentication works as configured.

### Integrating Contentstack with Adobe Experience Manager

Integrating Contentstack with Adobe Experience Manager (AEM) in the CMS may require a custom approach when an out-of-the-box connector is missing. This prevents the use of a native public connector for migration or integration.

**Root Cause**

A dedicated out-of-the-box AEM connector is not available on the public site.

**Resolution**

1.  Refer to the official AEM-to-Contentstack migration PDF for guidance.
2.  Utilize custom scripts and APIs to implement a migration or integration approach.

After reviewing the migration PDF and scripts, attempt to configure the custom integration. If the integration successfully connects the platforms, the custom approach is functional.

### Contentstack Webhook IP Addresses by Region

Webhook requests sent from Contentstack are rejected or blocked by the receiving server’s firewall. The server administrator needs to know which IP addresses to whitelist to allow inbound webhook traffic.

**Root Cause**

Contentstack sends all webhook requests from a fixed set of outbound IP addresses per cloud region. When a receiving server has a firewall or network access control list, these IPs must be explicitly allowed. If the IPs are not whitelisted, webhook requests will be refused at the network level.

**Resolution**

Whitelist the appropriate IPs for your stack’s cloud region. Contact Contentstack Support to obtain the current IP list for your specific region, as IP ranges are subject to change. The currently documented IPs by region are:

*   AWS NA: 52.35.1.58, 52.35.48.83, 52.27.91.224
    
*   AWS EU: Obtain from Contentstack Support - ASN details are not shared but full IP ranges are available on request
    
*   Azure NA: 20.98.104.159, 20.115.208.50 (note: 20.3.15.152 is no longer active and should be removed)
    
*   Azure EU: Obtain from Contentstack Support
    

Note: Contentstack does not publish ASN details. Whitelist by specific IP address, not by ASN.

1.  Add the applicable IP addresses to the inbound allow list in your firewall or network access control configuration.
    
2.  After updating the firewall, trigger a test webhook event and confirm the request is received by the endpoint.
    
3.  If new IPs are issued in future, contact Contentstack Support to obtain the updated list.
    

After updating the whitelist, trigger a test publish event and verify the webhook payload is received at the endpoint without a connection refused or blocked response.

### Webhook Requests Blocked Despite Correct IPs Being Whitelisted

Webhook requests continue to be refused even after the IP addresses provided by Contentstack Support have been added to the firewall. The customer has confirmed the IPs are whitelisted.

**Root Cause**

The most common cause is a mismatch between the whitelisted IPs and the actual outbound IPs Contentstack is currently using. If the stack was provisioned on a different cloud provider or region than assumed, the wrong regional IP set may have been whitelisted. Additionally, an outdated NAT outbound IP (for example, the now-inactive Azure NA IP 20.3.15.152) may still be configured.

**Resolution**

1.  Confirm the cloud region for your stack from the Contentstack dashboard URL or stack settings.
    
2.  Re-request the IP list from Contentstack Support, specifying the stack’s exact cloud provider and region, to ensure you have the current active IPs.
    
3.  Remove any deprecated IPs from the whitelist (for example, 20.3.15.152 for Azure NA).
    
4.  Add the newly confirmed IPs and retest the webhook.
    
5.  Inspect server-side firewall logs to confirm whether the rejected requests are originating from the whitelisted IPs or from a different address.
    

After updating to the correct and current IP set, trigger a test webhook and confirm the request passes through the firewall without rejection.

### Outdated NAT Outbound IP Causing 429 Errors on Webhook Endpoint

A high volume of 429 Too Many Requests errors appears on the webhook endpoint. Webhook delivery is failing at scale and the receiving server is rate-limiting the requests.

**Root Cause**

The customer’s webhook receiving system was rate-limiting requests originating from an outdated NAT outbound IP. Because the outdated IP was not in the customer’s allowed list, the server treated these requests as unauthorized traffic and applied aggressive rate limiting. The outbound IP Contentstack was using had changed and the webhook configuration on the customer’s side had not been updated to reflect this.

**Resolution**

1.  Contact Contentstack Support and request the current active outbound IP addresses for your region.
    
2.  Remove any outdated IPs from your firewall allowlist and add the current ones.
    
3.  Verify that no additional rate-limiting rules are targeting the Contentstack IP range beyond standard firewall allow/deny rules.
    
4.  After updating, monitor the webhook logs for 429 errors and confirm they cease.
    

After updating the allowlist with the current IPs, trigger a series of webhook events and confirm requests are received without 429 responses.

### Securing Firewall-Protected Endpoints That Receive Webhook Traffic

A webhook endpoint is behind a strict firewall (for example, triggering an Azure Function) that requires static IP ranges or trusted header-based filtering before allowing inbound traffic. The customer needs to know how to secure webhook delivery without blocking legitimate requests.

**Root Cause**

Firewall-restricted webhook endpoints require either IP-based or header-based verification to accept webhook traffic. Contentstack provides both mechanisms to support these scenarios.

**Resolution**

Contentstack supports the following mechanisms for securing webhook delivery to firewall-protected endpoints:

1.  IP whitelisting: whitelist the static outbound IP addresses for your region (see Issue 1 above) in the firewall or network access control list.
    
2.  Request signature header: every webhook request includes the X-Contentstack-Request-Signature header, which contains an RSASSA-PSS signature. The receiving endpoint can verify this header against the Contentstack public key to confirm authenticity.
    
3.  Custom headers: configure custom request headers in the webhook settings to include a shared secret or token that the receiving endpoint can validate.
    
4.  Authentication methods: configure Basic Auth, Bearer Token, or OAuth 2.0 Client Credentials in the webhook settings to authenticate requests at the application layer.
    

Use a combination of IP whitelisting (for network-level trust) and request signature verification or authentication headers (for application-level trust) for defense-in-depth webhook security.

### Configuring Webhook Authentication - Basic Auth, Bearer Token, and OAuth 2.0

Guidance is needed on the available webhook authentication methods in Contentstack, how to configure each, and when to use each option.

**Root Cause**

Contentstack supports three authentication methods for webhook requests in addition to unauthenticated (None) delivery. Each method serves different security and integration requirements.

**Resolution**

**Basic Auth:**

Attach a username and password to every webhook request. Configure in the webhook settings by selecting Basic Auth and entering credentials. The receiving endpoint validates the credentials on each request.

**Bearer Token:**

Attach a static bearer token in the Authorization header of each webhook request. Configure in the webhook settings by selecting Bearer Token and entering the token value. Suitable for endpoints that accept static API keys.

**OAuth 2.0 Client Credentials:**

Contentstack fetches an access token from a configured token endpoint and includes it in webhook requests. When the token expires and the endpoint returns a 401 with the correct WWW-Authenticate header, Contentstack automatically refreshes the token. OAuth 2.0 must be enabled for the organization - contact Contentstack Support to request enablement. Commercial details must be confirmed with your Customer Success Manager.

**None:**

No authentication header is included. Use this when the endpoint handles security through IP whitelisting or request signature verification instead.

After configuring the chosen authentication method, trigger a test webhook and verify the endpoint receives the request with the correct authorization credentials.

### OAuth 2.0 Webhook Token Not Refreshing - Requires Correct 401 Response Format

A webhook configured with OAuth 2.0 initially works correctly but later becomes disabled. Investigation reveals that Contentstack is continuing to use an expired access token rather than fetching a new one, causing all subsequent webhook deliveries to fail.

**Root Cause**

Contentstack follows the OAuth 2.0 standard for token refresh triggering. To signal that an access token has expired and a new one should be requested, the endpoint must return a 401 Unauthorized response that includes a WWW-Authenticate header with the value error=“invalid\_token”. If this header is absent from the 401 response, Contentstack does not recognize the 401 as a token expiry signal and does not trigger a refresh. The webhook continues to fail with the expired token until it is disabled by the circuit breaker.

**Resolution**

1.  Update the webhook-receiving endpoint or its authentication middleware to return the following header alongside a 401 response when the token is expired:
    
2.  WWW-Authenticate: Bearer realm=“example”, error=“invalid\_token”, error\_description=“The access token expired”
    
3.  Ensure the error=“invalid\_token” value is present - this is the specific signal Contentstack uses to trigger a token refresh.
    
4.  After updating the endpoint, re-enable the disabled webhook and trigger a test event. Verify the token refresh occurs correctly when the token expires.
    

After the endpoint is updated to return the correct WWW-Authenticate header on 401 responses, trigger a webhook call with an expired token. If Contentstack successfully refreshes the token and the webhook delivers correctly, the refresh flow is working.

### Webhook Appears to Require Basic Auth - How to Disable It

After a webhook configuration change, webhooks appear to require Basic Auth credentials, causing delivery failures for endpoints that do not use authentication. The expectation is that authentication is optional.

**Root Cause**

Basic Auth (and other authentication methods) in Contentstack webhook configuration are optional. If Basic Auth is selected and credentials are partially entered or left blank, the webhook save may fail or the auth method may appear required. This confusion arises from the UI presenting authentication fields when Basic Auth is selected.

**Resolution**

1.  Open the webhook configuration in the Contentstack dashboard.
    
2.  Navigate to the Authentication Method section.
    
3.  Select None to disable authentication entirely.
    
4.  Save the webhook configuration.
    

After setting Authentication Method to None and saving, trigger a test webhook and confirm delivery succeeds without any authentication header being required by the endpoint.

### Webhook Signature Verification Failing - Correct Implementation Approach

Webhook signature verification fails during implementation. The X-Contentstack-Request-Signature header value does not match the computed signature, despite seemingly correct public key loading and RSASSA-PSS parameters.

**Root Cause**

Webhook signature verification uses RSASSA-PSS with specific parameters. Implementation failures typically result from one of the following: incorrect base64 decoding of the signature header in certain execution environments (such as Cloudflare Workers), using the wrong hash algorithm or salt length in the PSS parameters, or processing the request body incorrectly before verification.

**Resolution**

The correct verification approach varies by runtime. Key requirements common to all implementations:

*   Algorithm: RSASSA-PSS with SHA-256 digest
    
*   Salt length: match the digest length (MGF1 with SHA-256)
    
*   Input: the raw request body bytes - do not parse or transform before verification
    
*   Key format: PEM-encoded RSA public key from Contentstack webhook settings
    

1.  For Java (Spring with BouncyCastle): use PSSSigner with SHA256withRSAandMGF1. Ensure the public key is loaded correctly and the signature is decoded from base64 before passing to the signer. Contact Contentstack Support for a tested Java code sample if the implementation continues to fail.
    
2.  For Node.js: use the built-in crypto module - crypto.createVerify(‘RSA-SHA256’) with RSA\_PKCS1\_PSS\_PADDING and saltLength set to crypto.constants.RSA\_PSS\_SALTLEN\_DIGEST.
    
3.  For Cloudflare Workers: the standard atob() base64 decoder may not handle all base64 variants correctly. Use a Uint8Array-based decoder or the SubtleCrypto API instead.
    

After implementing the correct verification logic, send a test webhook and confirm the signature verification succeeds for the received payload.

### mTLS (Certificate-Based OAuth) Not Supported - Use a Proxy

A customer needs Contentstack webhooks to deliver to an endpoint that requires OAuth 2.0 with mutual TLS (mTLS) / certificate-based authentication. It is unclear whether Contentstack supports this setup.

**Root Cause**

Contentstack webhooks support OAuth 2.0 Client Credentials flow for token-based authentication, but mutual TLS (mTLS) - where the client must present a certificate alongside OAuth credentials - is not directly supported. The webhook delivery system does not manage client certificates.

**Resolution**

1.  Deploy a lightweight proxy or serverless function (such as AWS Lambda, Azure Functions, or Google Cloud Functions) between Contentstack and the mTLS-protected endpoint.
    
2.  Configure Contentstack to send webhooks to the proxy endpoint using standard OAuth 2.0 or Bearer Token authentication.
    
3.  The proxy function receives the webhook, handles the mTLS handshake using the required client certificate, and forwards the payload to the protected endpoint.
    
4.  If the mTLS endpoint is public (not behind a private network), consider whether IP whitelisting combined with request signature verification provides sufficient security without mTLS.
    

After deploying the proxy, configure Contentstack to target the proxy endpoint and trigger a test webhook. If the payload reaches the mTLS-protected endpoint successfully, the proxy is correctly bridging the authentication requirements.

### Webhook Automatically Disabled - Circuit Breaker Behavior

A webhook is automatically disabled without warning. The notification endpoint was temporarily unreachable, but the webhook remains disabled even after the endpoint comes back online. This causes cache inconsistencies or missed content events.

**Root Cause**

Contentstack implements a circuit breaker pattern for webhook reliability. When a webhook endpoint repeatedly fails to respond (for example, with 5xx errors or timeouts), Contentstack automatically disables the webhook to prevent further failed delivery attempts and to protect the platform from sustained load against an unavailable endpoint. Once disabled, the webhook does not automatically re-enable when the endpoint recovers - it requires manual re-activation.

**Resolution**

1.  Resolve the underlying issue causing the endpoint to fail (for example, fix the endpoint timeout, restore service availability, or correct authentication configuration).
    
2.  Navigate to Settings > Webhooks in the Contentstack dashboard.
    
3.  Locate the disabled webhook (shown with a disabled status indicator).
    
4.  Re-enable the webhook by toggling it back to active.
    
5.  Trigger a test webhook delivery to confirm the endpoint is now responding correctly.
    

Note: Content published while the webhook was disabled will not automatically trigger a retry. If the downstream system needs to process missed events, re-publish the affected entries after re-enabling the webhook.

Note: Webhook execution logs in the Contentstack dashboard can lag behind actual delivery. If the endpoint is confirming receipt of requests but the Logs section shows no new executions, the webhook may be in a disabled state or the log display has not yet refreshed. Confirm the webhook’s active/disabled status before concluding that delivery has failed.

### Configuring Email Notifications for Webhook Disablement

When a webhook is disabled by the circuit breaker, there is no immediate alert. Editors and developers discover the issue only after content fails to reach downstream systems. A mechanism is needed to proactively notify the team when a webhook is disabled.

**Root Cause**

Contentstack automatically sends email notifications when a webhook is disabled by the circuit breaker, but the notification email address must be explicitly configured in the webhook settings. If no email is configured, no notification is sent.

**Resolution**

1.  Open the webhook configuration in the Contentstack dashboard.
    
2.  Locate the Notification Email field in the webhook settings.
    
3.  Enter the email address (or addresses) of the team members who should be notified when the webhook is disabled.
    
4.  Save the webhook configuration.
    

After configuring the notification email, disable and re-enable the webhook in test mode to confirm the email notification is delivered. Note that Slack notifications are not natively supported - for Slack alerting, configure a webhook to a Slack-to-email bridge or implement a custom monitoring solution using the webhook execution logs API.

Note: Proactive monitoring of webhook health before the circuit breaker triggers is not natively available in Contentstack. The circuit breaker only fires after a threshold of failures has already occurred. For pre-failure alerting, use the following approaches:

*   Monitor your receiving endpoint’s error logs and set up alerts on the endpoint side for 5xx responses.
    
*   Use AWS CloudWatch, Azure Monitor, or equivalent infrastructure-level tooling to alert on HTTP failure rates from the endpoint.
    
*   Implement a custom health-check script that periodically queries the Contentstack webhook execution logs API and alerts on recent failures before they accumulate to the circuit breaker threshold.

### Reasons a Webhook Gets Disabled - Reference Guide

Webhooks are getting disabled unexpectedly on a stack. The team needs a clear understanding of all conditions that cause automatic disablement and what to do in each case.

**Root Cause**

Contentstack disables a webhook automatically under the following conditions:

*   Repeated endpoint failures: the endpoint consistently returns 5xx errors or connection timeouts across multiple consecutive delivery attempts.
    
*   Authentication failures: the endpoint consistently returns 401 or 403 responses, indicating the authentication credentials are invalid or expired (and cannot be refreshed via the OAuth flow).
    
*   Unhealthy endpoint: the endpoint URL is unreachable or returns unexpected responses that indicate it is no longer healthy.
    
*   Rate limit exceeded: persistent 429 Too Many Requests responses from the endpoint cause the circuit breaker to trip.
    

**Resolution**

1.  Check the webhook execution logs in the Contentstack dashboard to identify the specific error code returned by the endpoint before disablement.
    
2.  Resolve the root cause: fix the endpoint, update credentials, reduce delivery frequency, or correct the configuration.
    
3.  Re-enable the webhook manually from Settings > Webhooks.
    
4.  Configure a notification email to receive alerts for future disablement events.
    
5.  Re-publish any content that was missed during the disablement window if the downstream system requires it.
    

After resolving the root cause and re-enabling, trigger a test webhook and confirm the endpoint responds with a 200 OK status.

### Cannot Save a Webhook - Missing Mandatory Fields or Incomplete Authentication

Clicking Save in the webhook configuration UI does nothing. No confirmation is shown and no error message appears. The webhook cannot be created or updated.

**Root Cause**

The most common cause is incomplete or invalid authentication configuration. If Basic Auth is selected as the authentication method but valid credentials are not provided, or if another authentication method is selected without completing its required fields, the webhook form prevents saving without surfacing an obvious error message.

**Resolution**

1.  Review all fields in the webhook configuration for completeness, paying particular attention to the Authentication Method section.
    
2.  If Basic Auth is selected, ensure both the username and password fields are populated with valid values.
    
3.  If no authentication is needed, change the Authentication Method to None.
    
4.  Check that the notification URL is correctly formatted and begins with https://.
    
5.  After completing all required fields, attempt to save again.
    

After correcting the authentication configuration, attempt to save the webhook. If the save succeeds and a confirmation is shown, the required fields are now complete.

### Algolia Webhook Disabled After an App Update - Re-enable and Republish

After a Contentstack Algolia app update, content published or updated since the update is not being indexed in Algolia. The Algolia webhook was automatically disabled as part of the update process.

**Root Cause**

During certain Contentstack Algolia app updates, the associated webhook is automatically disabled to prevent partial or inconsistent indexing during the update. Content events that fire while the webhook is disabled are not forwarded to Algolia and are not automatically retried.

**Resolution**

1.  Navigate to the Algolia app configuration page in Contentstack (Marketplace > Installed Apps > Algolia).
    
2.  Locate the webhook configuration and re-enable the webhook.
    
3.  Identify all entries that were published or updated during the period the webhook was disabled.
    
4.  Republish those entries to regenerate the webhook events and restore Algolia indexing for the missed content.
    
5.  Confirm that real-time indexing is functioning by publishing a new entry and verifying it appears in Algolia.
    

After re-enabling the webhook and republishing affected entries, confirm new and republished content appears in Algolia search results as expected.

### Webhook Not Relayed - Referenced Entries Have Unfilled Mandatory Fields

Publishing a parent entry does not relay the webhook event, even though the parent entry’s fields are all filled. The publish action appears to stall and no webhook payload is sent.

**Root Cause**

Contentstack validates all referenced entries when a parent entry is published. If any referenced entry has unfilled mandatory fields, the parent entry’s publish action is blocked even if the parent’s own fields are complete. The webhook is not triggered because the publish never completes.

**Resolution**

1.  Open the parent entry and expand all referenced entry sections within it.
    
2.  Look for orange alert symbols (warning indicators) on any referenced entry fields - these indicate unfilled mandatory fields.
    
3.  Navigate to each flagged referenced entry and complete the missing mandatory fields.
    
4.  Republish the referenced entries individually.
    
5.  Return to the parent entry and publish it again. The webhook should now trigger.
    

After filling and publishing all referenced entries, attempt to publish the parent entry. If the webhook fires and the payload is received at the endpoint, the referenced entry validation is now passing.

### Variant Workflow Changes Not Triggering Webhook Events

Testing a translation webhook setup reveals that variant workflow stage changes do not trigger webhook events. It is unclear whether this is expected behavior or a configuration issue.

**Root Cause**

Contentstack webhooks do support variant-related events, but the webhook must be explicitly configured to listen for variant events. If the webhook is configured only for standard entry events (create, update, publish), variant workflow events will not trigger it.

**Resolution**

1.  Open the webhook configuration in the Contentstack dashboard.
    
2.  Under the Events section, ensure that the Variants event type is selected in addition to any standard entry events.
    
3.  Refer to the Contentstack Webhook Events documentation for the full list of supported variant-related event types and their payload formats.
    
4.  Save the updated webhook configuration.
    
5.  Trigger a variant workflow stage change and confirm the webhook event fires with the expected payload.
    

After updating the webhook event configuration to include variant events, change a variant’s workflow stage and verify the webhook payload is received at the endpoint.

### Webhook Payload Missing Updated Fields After Content Type Change

A field was removed from a content type. After the change, a third-party integration that receives webhook payloads begins failing because the payload structure has changed or the integration no longer receives correct entry data.

**Root Cause**

When a content type field is removed, existing entries retain their data under the old field UID in the database. However, the webhook payload reflects the entry’s current schema. Entries that were not re-saved after the content type change may carry a stale version. The downstream integration receives a payload that no longer matches what it expects. Re-saving entries increments their version and causes the webhook to deliver the updated payload structure.

**Resolution**

1.  After modifying a content type (removing, renaming, or adding fields), re-save all affected entries - even without content changes - to increment their version and update the payload structure.
    
2.  Notify downstream integration teams of the content type change so they can update their payload processing logic.
    
3.  If the field removal was unintentional, recreate the field with the same UID to restore the data. See the relevant CMA documentation for field recreation.
    

After re-saving the affected entries, trigger a test publish and confirm the webhook payload includes the updated entry structure matching the current content type schema.

### Multi-Environment Publish Webhook Returns Wrong or Duplicate Environment Data

When publishing an entry to multiple environments simultaneously (for example, production, staging, and QA), the webhook payload returns incorrect or duplicated environment data. Routing logic downstream fails because the environment field in the payload does not match expectations.

**Root Cause**

The webhook is configured with a Channels condition that restricts event delivery to a specific environment (for example, staging only). When publishing to multiple environments, only the staging events are relayed, making it appear as if only staging was updated. Other environments do not generate webhook events because they are excluded by the Channels configuration.

**Resolution**

1.  Open the webhook configuration and review the Channels section.
    
2.  If the webhook should fire for all environments, remove the environment-specific Channels restriction or add all required environments to the Channels condition.
    
3.  If environment-specific routing is required, create separate webhooks per environment - each scoped to a specific environment in the Channels condition.
    
4.  Save the updated webhook configuration and re-test a multi-environment publish.
    

After updating the Channels configuration, publish an entry to all target environments and confirm that separate webhook events are generated for each environment with the correct environment data in the payload.

### Webhook Fires Repeatedly in a Loop When Updating Multi-Locale Entries

A webhook is configured to update a specific field (for example, campaign ID) whenever an entry is published. When the entry is published across multiple locales, the webhook triggers once per locale, and each trigger causes another update, creating a recursive loop.

**Root Cause**

The campaign ID field is localizable. When it is updated via the webhook for one locale, it creates a new version of the entry in that locale, which triggers the webhook again - causing a recursive chain across all locales. Because the field is not shared across locales, each locale requires a separate update, multiplying the webhook execution count.

**Resolution**

1.  Make the campaign ID (or equivalent trigger field) non-localizable. A non-localizable field has a single value shared across all locales - setting it once in the master locale automatically applies to all locales, eliminating the need for per-locale updates.
    
2.  Navigate to the content type and edit the field settings.
    
3.  Enable the Non-localizable option on the field.
    
4.  Save the content type. Future webhook-triggered updates to this field will only fire once regardless of how many locales are published.
    

After making the field non-localizable, trigger a multi-locale publish and confirm the webhook fires only once (from the master locale update) rather than once per locale.

### Webhook Delays After Large Bulk Publish - Queue Backlog

Webhooks stop triggering or are significantly delayed after a large bulk publish operation. Waiting a long time eventually restores normal webhook delivery.

**Root Cause**

Contentstack’s webhook system processes events with a concurrency limit. A large bulk publish generates a high volume of webhook events simultaneously. When the number of queued events exceeds the concurrency limit, the queue builds up and subsequent webhooks are delayed until earlier events are processed. The publish itself completes correctly - only the webhook delivery is delayed.

**Resolution**

1.  If delivery is critically delayed and events are piling up, temporarily disable the affected webhook to allow the existing queue to drain.
    
2.  Re-enable the webhook after the queue has cleared.
    
3.  For ongoing workloads, avoid triggering large bulk publishes (thousands of entries simultaneously) during peak hours. Stagger bulk operations to reduce webhook queue pressure.
    
4.  If webhook delivery delays recur consistently with large bulk publishes, contact Contentstack Support to investigate queue scaling for your organization.
    

After the queue drains and the webhook is re-enabled, confirm that new publish events trigger webhook delivery within the expected time window.

### Webhook Not Triggering Due to Platform Resource Constraints

Webhooks stop firing for publish and unpublish events without any configuration change. The issue begins at a specific time and affects all webhooks across the stack.

**Root Cause**

Contentstack’s webhook infrastructure operates as a shared system. Temporary resource spikes (such as pod crashes or memory pressure) can cause webhook processing to stall or fail platform-wide. This is a platform-level issue, not a stack configuration problem, and requires engineering intervention to resolve.

**Resolution**

1.  Contact Contentstack Support and report that webhooks have stopped firing, providing the approximate start time and affected stack details.
    
2.  Engineering will investigate the webhook pod health and scale resources as needed to restore processing.
    
3.  No configuration changes are required on the customer side.
    
4.  After Engineering confirms the fix, trigger a test publish and verify the webhook fires correctly.
    

After Engineering resolves the platform resource constraint, trigger a publish event and confirm the webhook delivers within the normal expected timeframe.

### Webhook Not Triggering for Larger Entries

Webhooks trigger correctly for smaller entries but fail silently for certain entries with larger payloads. The issue is not consistent across all content types and began appearing after a specific date.

**Root Cause**

Entries with particularly large payload sizes can exceed internal size thresholds in the webhook processing system, causing those events to be dropped silently. This is a platform-level defect that requires an engineering fix.

**Resolution**

1.  Contact Contentstack Support and provide the affected entry UIDs and content types.
    
2.  Engineering will investigate and apply a fix to the webhook processing pipeline to handle the affected payload sizes.
    
3.  After the fix is confirmed, re-publish the affected entries to generate new webhook events.
    

After the engineering fix is applied, publish one of the previously affected large entries and confirm the webhook fires and the payload is delivered to the endpoint.

### Field-Specific Webhook Triggers Not Supported

A customer wants to trigger a webhook only when a specific field (such as the URL field) changes in an entry update, rather than on every entry update regardless of which field changed.

**Root Cause**

Contentstack webhooks do not currently support field-level trigger conditions. Entry-level webhooks fire on the defined event (create, update, publish, etc.) for the entire entry, regardless of which fields changed within that entry. Filtering by specific field changes is not natively configurable.

**Resolution**

1.  Configure the webhook to fire on the entry update event as normal.
    
2.  In the webhook receiving endpoint or middleware, compare the updated entry payload against the previously stored version of the entry to detect whether the specific field of interest has changed.
    
3.  Process the event only if the field-level comparison indicates a change in the field; discard it otherwise.
    
4.  Cache or store the previous entry state (for example, using the entry version number or a persisted copy) to enable the comparison.
    

This is a known product limitation. An enhancement request for native field-specific trigger conditions can be submitted through Contentstack Support.

### Webhook Conditions Only Support OR Logic - Cannot Exclude a Content Type

A webhook needs to fire for all content types except one test-only type. The webhook configuration UI only supports OR conditions - there is no built-in exclusion or AND logic to skip a specific content type.

**Root Cause**

Contentstack webhook conditions use OR logic - each configured condition is an additional trigger, not a filter-by-exclusion. There is no AND logic or NOT condition available in the webhook configuration to exclude a specific content type. Selecting multiple content types means the webhook fires for any of them.

**Resolution**

1.  In the webhook configuration, manually select every content type except the test-only type. This is the most straightforward approach for a limited number of content types.
    
2.  Alternatively, configure the webhook without content type restrictions (fire for all content types) and implement exclusion logic in the webhook receiving endpoint: check the content\_type.uid field in the payload and discard events from the test content type.
    

Receiver-side filtering is the recommended approach when complex exclusion logic is required, as it provides full control over event handling without being constrained by the webhook configuration UI.

### Webhook Payload Cannot Be Customized for Third-Party APIs

A customer needs to send webhook events to a third-party API (such as GitHub) that requires a specific payload format. The Contentstack webhook payload format does not match the required format.

**Root Cause**

Contentstack webhook payloads are fixed in structure and cannot be customized or transformed within the platform. The payload always follows the Contentstack webhook schema for the given event type.

**Resolution**

1.  Deploy a lightweight middleware service between Contentstack and the third-party API. Options include AWS Lambda, Azure Functions, Google Cloud Functions, or a dedicated microservice.
    
2.  Configure the Contentstack webhook to deliver to the middleware endpoint.
    
3.  The middleware receives the Contentstack payload, transforms it into the required format for the third-party API, and forwards it.
    
4.  The middleware can also handle any authentication, signing, or retry logic required by the third-party service.
    

After deploying the middleware and updating the webhook endpoint, trigger a test event and verify the payload arrives at the third-party API in the correct format.

### Additional Headers Cannot Be Added to Webhook Requests

A customer needs to inject specific HTTP headers (beyond the standard Contentstack headers) into webhook requests. The webhook configuration does not appear to support this.

**Root Cause**

Contentstack webhooks support configuring authentication-related headers (Basic Auth, Bearer Token, OAuth 2.0) and custom headers through the webhook settings. However, there is a limit on the type and number of headers that can be injected, and server-level headers tied to the underlying connection mechanism cannot be modified.

**Resolution**

For adding custom headers:

1.  In the webhook configuration, use the Custom Headers section to add key-value pairs for additional headers needed by the endpoint.
    
2.  If the required header type is not supported natively (for example, system-level or connection headers), use a middleware proxy to add the required headers before forwarding the request to the final endpoint.
    

After adding custom headers in the webhook configuration, trigger a test event and inspect the received request at the endpoint to confirm the custom headers are present.

### updated_by Field Missing from Concise Webhook Payload

The updated\_by user field is absent from the webhook payload. User attribution data is needed to log who triggered a content event.

**Root Cause**

The concise webhook payload format is designed to be minimal and efficient. It intentionally excludes user-related fields such as updated\_by and created\_by to reduce payload size. This is by design and is not a bug.

**Resolution**

1.  Switch the webhook payload format from Concise to Full in the webhook settings.
    
2.  The full payload includes user attribution fields such as updated\_by and created\_by, providing complete metadata about who triggered the event.
    
3.  Note that the full payload is significantly larger than the concise format - ensure the receiving endpoint can handle the increased payload size.
    

After switching to the full payload format, trigger a test event and confirm the updated\_by field is present in the received payload.

### Distinguishing Release Deploy Webhooks from Single Entry Publish Webhooks

A customer needs to differentiate between webhook payloads triggered by a release deployment and those triggered by a direct single-entry publish outside of a release. The payload structure appears similar.

**Root Cause**

Contentstack generates distinct webhook event types for release deployments versus individual entry publishes. These events have different structures and identifiers that allow downstream systems to distinguish between them.

**Resolution**

1.  For release deployments, configure the webhook to listen for the Release Deployed event type. The payload for this event includes release-level details (release UID, release name) and an array of all deployed entries.
    
2.  For individual entry publishes, the webhook payload uses the standard entry publish event type and contains only the single entry’s data.
    
3.  In the receiving endpoint, check the event type field in the webhook payload header or body to determine whether the event originated from a release or a direct publish.
    

After configuring the Release Deployed event type in the webhook, deploy a release and confirm the payload includes the release UID and the list of deployed entries, distinguishing it from single-entry publish payloads.

### URL Field Missing from entry_variant Webhook Payload

The URL field is absent from the webhook payload when the module is entry\_variant. The URL is needed by the receiving system for cache-clearing operations but cannot be found in the variant publish payload.

**Root Cause**

This is expected behavior based on Contentstack’s webhook design. For base entry publishes (module: “entry”), the webhook includes the full canonical entry object including the URL field. For variant publishes (module: “entry\_variant”), the webhook contains only a partial payload that does not include the canonical URL field. Variants are supplemental content overlays on top of a base entry, so the URL belongs to the base entry.

**Resolution**

1.  When receiving an entry\_variant webhook event, extract the entry\_uid from the variant payload.
    
2.  Use the entry\_uid to make a separate CDA or CMA API call to fetch the base entry and retrieve its URL field.
    
3.  Use the retrieved URL for cache-clearing or other operations that require the canonical entry URL.
    

After implementing the base entry lookup step for entry\_variant events, trigger a variant publish and confirm the URL is successfully retrieved from the base entry API call.

### Listening for Taxonomy Create and Update Events via Webhooks

A customer wants to use webhooks to be notified when taxonomy terms are created or updated, and to retrieve the full taxonomy hierarchy programmatically when an event fires.

**Root Cause**

Taxonomy create and update events are supported in Contentstack webhooks and can be configured to trigger on taxonomy-related actions. Taxonomy term hierarchy is accessible via the Taxonomy API, which is the recommended approach for retrieving hierarchical structure after a webhook event fires.

**Resolution**

1.  In the webhook configuration, select the Taxonomy event type to listen for create and update actions on taxonomy terms.
    
2.  The webhook payload will include the taxonomy UID and term details for the triggering event.
    
3.  To retrieve the full taxonomy hierarchy programmatically after receiving the event, call: GET /v3/taxonomies/{taxonomy\_uid}/terms - this returns all terms and their parent-child relationships.
    
4.  Refer to the Contentstack Taxonomy API documentation for filtering and pagination options when working with large taxonomy trees.
    

After configuring the taxonomy webhook event, create or update a taxonomy term and verify the webhook is triggered with the expected payload containing the taxonomy and term details.

### Webhook Responses Delayed - Shared Infrastructure and Auto-Scaling

Webhooks are taking significantly longer than usual to deliver - delays of several minutes instead of seconds. The issue is intermittent and appears to resolve over time without any configuration change.

**Root Cause**

Contentstack’s webhook infrastructure is a shared system across all organizations. During periods of unusually high platform load (for example, widespread bulk publishes or infrastructure events), webhook processing may be temporarily throttled while auto-scaling provisions additional capacity. The delay is not caused by the customer’s webhook configuration and requires no action on their side.

**Resolution**

1.  Monitor the webhook execution logs in the dashboard to confirm events are queued and not failing.
    
2.  If the delay is consistent and exceeds 10–15 minutes, contact Contentstack Support with the approximate start time and affected stack and region details.
    
3.  Do not disable and re-enable the webhook during a temporary delay - this can cause events to be dropped from the queue.
    
4.  For time-sensitive delivery requirements, implement a retry mechanism in the receiving endpoint that can handle delayed delivery gracefully.
    

After the auto-scaling resolves, confirm that new webhook events are delivered within the normal expected window.

### Excessive Webhook Traffic Causing 429 Rate Limit Errors

A large number of HTTP 429 Too Many Requests errors appear in the webhook logs. The volume of webhook events being generated far exceeds what is expected from normal content publishing activity.

**Root Cause**

429 errors on the webhook system indicate that either: (a) the receiving endpoint is rate-limiting inbound requests from Contentstack, or (b) a misconfigured webhook, automated script, or integration is generating an unexpectedly high volume of webhook events (for example, a recursive loop, an unthrottled bulk operation, or a broken automation repeatedly re-triggering events).

**Resolution**

1.  Review the webhook execution logs to identify the volume and frequency of events and which content types or entries are generating the most traffic.
    
2.  Identify any automated workflows, CLI operations, or third-party integrations that may be triggering excessive publish or update events.
    
3.  If a recursive loop is identified (for example, a webhook triggers an update that re-triggers the webhook), break the loop by making the relevant field non-localizable, adding a payload check to skip no-op updates, or disabling the webhook temporarily.
    
4.  If the receiving endpoint is rate-limiting the requests, implement a queue-based receiver that can handle webhook events asynchronously without hitting endpoint rate limits.
    
5.  After identifying and fixing the source of excess events, re-enable or restore the webhook and monitor traffic levels.
    

After correcting the misconfiguration or loop, monitor the webhook execution logs for 24 hours. If 429 errors cease and the event volume returns to expected levels, the root cause has been resolved.

### Webhook Publish Event Looping

A webhook configured to fire on entry publish is causing entries to be published in a continuous loop. Each webhook-triggered action causes another publish event, which re-triggers the webhook.

**Root Cause**

A publish event webhook that triggers a CMA update or publish operation on the same entry creates a recursive cycle: publish → webhook → CMA update → publish → webhook. This pattern is especially common when a webhook is used to set or update a field value after publish (for example, setting a campaign ID or last-modified timestamp).

**Resolution**

1.  Implement a loop-prevention check in the webhook receiver: compare the field value being set against the current value. If they are equal, skip the CMA update to avoid re-triggering the publish.
    
2.  Make the field being updated by the webhook non-localizable, which ensures it is set globally in a single operation rather than per-locale, reducing the number of webhook triggers.
    
3.  Add a custom header to webhook-triggered CMA requests. In the webhook receiver, check for this header - if the request was triggered by a webhook, skip the re-publish.
    
4.  Consider using the Automate Hub instead of a direct CMA call, as Automate has built-in idempotency and loop-detection mechanisms.
    

After implementing loop-prevention logic, trigger a single publish and confirm the webhook fires once and does not cause additional publish events.

### Cloudflare Rules or Cache Settings Blocking Webhook Delivery

A webhook that was previously working stops delivering events. Investigation reveals the endpoint is reachable but Contentstack requests are being blocked. The issue is resolved after making changes to Cloudflare settings.

**Root Cause**

Cloudflare’s Web Application Firewall (WAF) rules, cache policies, or IP reputation filters can block inbound webhook requests from Contentstack. This can occur after a Cloudflare configuration change, a Cloudflare WAF rule update, or when Contentstack’s outbound IP addresses are treated as suspicious by a Cloudflare security rule.

**Resolution**

1.  Log in to the Cloudflare dashboard and review the firewall events log for blocked requests originating from Contentstack’s IP addresses.
    
2.  Create a Cloudflare WAF allow rule for Contentstack’s outbound IP addresses to exempt webhook traffic from WAF blocking.
    
3.  If caching is applied to the webhook endpoint URL, add a Cache Rule to bypass caching for the webhook endpoint path.
    
4.  Ensure the webhook endpoint path is not subject to Cloudflare’s DDoS protection rules that may throttle POST requests.
    

After updating the Cloudflare rules to allow Contentstack’s IPs and bypass caching on the webhook endpoint, trigger a test webhook and confirm delivery succeeds.

### Contentstack Webhook Outbound IP Addresses for Whitelisting

A receiving server’s firewall or network access control is blocking inbound webhook requests from Contentstack. The server administrator needs the current outbound IP addresses to add to the allowlist.

**Root Cause**

Contentstack sends all webhook requests from a fixed set of outbound IP addresses per cloud region. Firewall rules must explicitly permit these IPs before webhook traffic can reach the endpoint.

**Resolution**

The current confirmed outbound IP addresses for the AWS North America region are:

*   52.35.1.58
    
*   52.35.48.83
    
*   52.27.91.224
    

IMPORTANT - Verify before publishing: the IP addresses above are sourced from support case data and may not reflect the current active set. Before publishing this article, confirm the current IP list with Contentstack Support or from the official Contentstack webhook documentation. IP ranges can change, and publishing outdated IPs will cause customers to misconfigure their firewalls.

For other regions (AWS EU, Azure NA, Azure EU), contact Contentstack Support and specify the cloud provider and region for the stack. IP addresses are confirmed to be stable - if the IPs above are not returning traffic, verify the correct regional endpoint is being used rather than assuming the IPs have changed.

1.  Add the applicable IP addresses to the inbound allow list in the firewall or network ACL.
    
2.  After updating the firewall, trigger a test webhook event and confirm the request is received at the endpoint.
    
3.  If IPs change in future (Contentstack will communicate this), update the allowlist accordingly. Contact Contentstack Support to confirm the current list before making any changes.
    

After updating the allowlist, trigger a test publish event and verify the webhook payload is received without a connection refused or blocked response.

### Webhook Requests Blocked by UCEPROTECT RBL - Third-Party Blacklist

Webhook requests from Contentstack are being blocked at the receiving server’s network layer. Investigation reveals the Contentstack IP addresses are listed on the UCEPROTECT Real-time Blackhole List (RBL) used by the network or mail gateway.

**Root Cause**

UCEPROTECT operates as a commercial pay-to-delist service. IP address blocks are based on automated detection criteria that can include shared infrastructure neighbors - meaning legitimate IP addresses on shared subnets can be listed without any abuse originating from those IPs. Cloudflare and other CDN/network providers have flagged UCEPROTECT as an unreliable blocklist due to this model.

**Resolution**

1.  Advise the network or security team to review whether UCEPROTECT is an appropriate RBL for their use case. Cloudflare explicitly recommends that organizations consider alternative providers for blacklist validation due to UCEPROTECT’s pay-to-delist model.
    
2.  As an immediate workaround: add the specific Contentstack webhook IP addresses to an explicit allowlist at the application or firewall level, which overrides the RBL block for those known-good IPs.
    
3.  If using Cloudflare WAF, create a WAF exception or allowlist rule for the Contentstack IP addresses to bypass the RBL check.
    
4.  If the business is unable to change the RBL configuration, contact Contentstack Support for alternative outbound routing options.
    

After adding Contentstack IPs to the explicit allowlist, trigger a test webhook and confirm the request bypasses the RBL block and reaches the endpoint.

### Webhook Calls Failing After SSL Certificate Renewal - Certificate Chain Issue

Webhook calls from Contentstack began failing shortly after an SSL certificate was renewed on the receiving server. The endpoint is accessible via the browser but Contentstack webhook requests return certificate errors.

**Root Cause**

Contentstack validates SSL certificates against publicly recognized Certificate Authorities (CAs). When a certificate is renewed, the renewal process occasionally results in an incomplete or incorrect certificate chain being served. The most common issue is an intermediate certificate being missing from the chain, causing Contentstack’s webhook delivery system to reject the handshake even though browsers may accept it (browsers often cache intermediate certificates locally).

**Resolution**

1.  Verify the complete certificate chain is being served correctly. Use an SSL checker tool (such as SSL Labs at ssllabs.com/ssltest) to inspect the certificate chain for the webhook endpoint URL.
    
2.  Ensure the certificate chain includes: the end-entity (leaf) certificate, all intermediate certificates, and the root CA certificate in the correct order.
    
3.  Update the server configuration (nginx, Apache, or load balancer) to include the full intermediate certificate bundle alongside the leaf certificate.
    
4.  Ensure the certificate is issued by a publicly recognized CA (such as DigiCert, Let’s Encrypt, Sectigo, or similar). Self-signed certificates are not trusted by Contentstack.
    
5.  After updating the certificate chain, trigger a test webhook and confirm delivery succeeds.
    

After correcting the certificate chain, verify using SSL Labs that the chain is complete and then confirm webhook delivery succeeds in the Contentstack webhook execution logs.

### X.509 Certificate-Based Authentication (mTLS) Not Supported for Webhooks

A customer integrating Contentstack webhooks with an API gateway that requires mutual TLS (mTLS) / X.509 client certificate authentication asks whether Contentstack can present a client certificate during the TLS handshake for outbound webhook calls.

**Root Cause**

Contentstack webhooks support token-based and OAuth 2.0 authentication methods for securing outbound webhook requests. Mutual TLS - where Contentstack would present a client X.509 certificate during the TLS handshake - is not currently supported. The webhook delivery infrastructure does not manage or present client certificates.

**Resolution**

Since mTLS is not natively supported, the following alternative security approaches are available:

1.  Proxy-based mTLS: deploy a lightweight proxy or serverless function (AWS Lambda, Azure Functions, or a dedicated proxy) between Contentstack and the mTLS-protected API gateway. Contentstack delivers the webhook to the proxy using Bearer Token or OAuth 2.0 authentication. The proxy then handles the mTLS handshake and forwards the payload to the API gateway.
    
2.  IP allowlisting: restrict the API gateway’s inbound rules to accept requests only from Contentstack’s known outbound IP addresses. This provides network-level authentication without requiring client certificates.
    
3.  Request signature verification: Contentstack includes an X-Contentstack-Request-Signature header on every webhook. The API gateway can verify this RSASSA-PSS signature using Contentstack’s public key to confirm the request originated from Contentstack.
    
4.  OAuth 2.0 Client Credentials: if the API gateway supports token-based auth, use Contentstack’s OAuth 2.0 webhook authentication to exchange client credentials for an access token per request.
    

The proxy-based approach is the most common solution for environments that mandate mTLS. After deploying the proxy, configure Contentstack to target the proxy endpoint and confirm the webhook payload reaches the mTLS-protected API gateway.

### Webhook Trigger Filters Not Supported - Implement Receiver-Side Filtering

A customer wants to configure a webhook to fire only when a specific field in an entry changes, or only when entries of a specific content type match a custom attribute. They expect a filter configuration in the webhook settings.

**Root Cause**

Contentstack webhook conditions support filtering by event type (create, publish, unpublish, delete), content type, environment (via Channels), and locale. Field-level or attribute-based trigger filtering - where the webhook fires only if a specific field value meets a condition - is not currently supported within the Contentstack webhook configuration.

**Resolution**

1.  Configure the webhook to fire on the appropriate event type and content type as a baseline filter.
    
2.  In the webhook receiver (your application endpoint, Lambda, or middleware), inspect the incoming payload and implement the custom filter logic: compare field values, check for specific attributes, or evaluate conditions against the payload data before deciding whether to process the event.
    
3.  To filter by field changes, compare the current field value in the payload against the previously stored value (fetched from a cache, database, or the Contentstack API) and discard the event if the field of interest has not changed.
    
4.  Use the webhook’s Channels condition to scope delivery to specific environments, and use the content type filter to narrow to relevant content types - combining these built-in filters reduces unnecessary events before the receiver applies custom logic.
    

Receiver-side filtering is the recommended pattern for all filtering requirements beyond what the webhook configuration natively supports. This approach gives full control over event processing logic without platform constraints.

### Webhook Not Triggering a Single Event for Multi-Environment Publish - Use the Job Channel

A customer configures a webhook for entry publish events but does not receive a single unified notification when an entry is published to multiple environments simultaneously. Instead, they either receive multiple events (one per environment) or no events at all.

**Root Cause**

Contentstack does not send a single combined webhook event for a publish action that targets multiple environments simultaneously. Each environment publish generates its own individual event, and the webhook fires per environment. If a single summary notification is needed for a multi-environment publish operation, the Channels filter on the webhook must be configured appropriately, or the job channel must be used.

**Resolution**

1.  To receive a single summary notification for a bulk or multi-environment publish operation, configure the webhook to subscribe to the Job channel. The job channel delivers a summary notification for the overall publish operation after it completes, rather than one event per environment.
    
2.  From the job summary payload, make a follow-up API call to fetch the detailed information for the specific entries and environments that were published.
    
3.  If per-environment granularity is needed (rather than a summary), configure separate webhooks scoped to each environment using the Channels condition in the webhook settings.
    

After subscribing to the job channel, trigger a multi-environment publish and confirm a single summary notification is received rather than multiple per-environment events.

### Webhook Retry Behavior - 10 Retries Before Auto-Disablement

A customer wants to understand how many times Contentstack retries a failed webhook before disabling it, and whether the retry interval can be configured.

**Root Cause**

Contentstack implements a circuit breaker pattern for webhook reliability. When a webhook endpoint returns failure responses (5xx errors, 401 Unauthorized, or connection timeouts), Contentstack retries the delivery up to 10 times before automatically disabling the webhook as a safeguard. The retry interval uses an exponential backoff pattern.

**Resolution**

*   Retry count: up to 10 retry attempts before the webhook is automatically disabled.
    
*   Retry triggers: 5xx server errors, 401 Unauthorized responses, and connection timeouts.
    
*   Retry interval: exponential backoff - the interval between retries increases with each attempt.
    
*   Configurable: the retry count and interval are not configurable. They are platform-enforced defaults.
    
*   After 10 failures: the webhook is automatically disabled and must be manually re-enabled from Settings > Webhooks after the endpoint issue is resolved.
    

To receive proactive notification when a webhook is disabled after retry exhaustion, configure the ‘Email Addresses to Notify’ field in the webhook settings.

### No Email Notification When Webhook Is Auto-Disabled - Configure Notification Email

A webhook was automatically disabled by the circuit breaker after the endpoint became unhealthy, but no one on the team was notified. The issue was discovered only after downstream systems stopped receiving events.

**Root Cause**

Contentstack has a built-in mechanism to send email notifications when a webhook is disabled by the circuit breaker, but the notification email addresses must be explicitly configured in the webhook settings. If no email is configured, no notification is sent when the webhook auto-disables.

**Resolution**

1.  Navigate to Settings > Webhooks in the Contentstack dashboard.
    
2.  Open the webhook configuration for each critical webhook.
    
3.  Locate the ‘Email Addresses to Notify’ field and enter the email addresses of team members who should be alerted when the webhook is disabled.
    
4.  Save the webhook configuration.
    
5.  To test: manually disable the webhook and re-enable it to confirm the notification email configuration is working (or trigger a test disable through a failing endpoint).
    

After configuring notification emails, confirm the team receives an alert the next time the circuit breaker auto-disables the webhook, enabling faster response and recovery.

### Multiple Webhooks Going Unhealthy - Endpoint Timeouts

Multiple webhooks on a production stack become unhealthy simultaneously. Re-enabling them provides temporary recovery before timeouts return. The webhook execution logs show consistent endpoint timeouts.

**Root Cause**

Engineering review of logs confirmed the root cause was the webhook endpoint processing being too slow relative to Contentstack’s delivery timeout threshold. When the receiving endpoint takes too long to respond, Contentstack records the delivery as a timeout failure. After repeated timeouts, the circuit breaker disables the webhook. On re-enable, the endpoint briefly accepts requests before slowing down again, creating a cycle of re-enable and re-disable.

**Resolution**

**Optimize the webhook receiver for fast acknowledgment:**

1.  Return a 200 OK response immediately upon receiving the webhook, before any processing logic runs. Store the payload in a queue (AWS SQS, Redis, RabbitMQ, or similar) and process it asynchronously.
    
2.  Review the endpoint’s processing time. Any synchronous operation (database writes, API calls to third parties, cache invalidations) performed before the 200 response is returned adds to the response time.
    
3.  If the endpoint is hitting Contentstack’s timeout threshold even with fast acknowledgment, contact Contentstack Support to confirm the configured timeout value and whether it can be extended for the specific integration.
    

**Monitor endpoint health proactively:**

1.  Set up external health monitoring (AWS CloudWatch, Datadog, or equivalent) on the webhook endpoint to alert before Contentstack’s circuit breaker trips.
    
2.  Configure the ‘Email Addresses to Notify’ field in the webhook settings to receive immediate notification when Contentstack auto-disables the webhook.
    

After optimizing the receiver to return 200 immediately and process asynchronously, re-enable the webhooks and monitor the execution logs. If timeouts cease and the webhooks remain healthy, the response time optimization was sufficient.

### Webhook Delay of 20–30 Minutes After Bulk Publish - Queue Pressure

Webhook events for a bulk publish job (for example, 10 entries published simultaneously) arrive at the receiving endpoint 20–30 minutes after the publish action completed. The delay impacts downstream systems that depend on real-time event processing.

**Root Cause**

Contentstack’s webhook system processes events with a concurrency limit. When a bulk publish generates a high volume of webhook events across multiple organizations simultaneously (shared infrastructure), the webhook processing queue builds up. Events are delivered in order, but slower if the queue is under pressure. For the specific bulk publish case, concurrent webhook queue load from other organizations in the region was identified as the primary cause of the 20–30 minute delay.

**Resolution**

1.  For time-sensitive downstream systems: implement retry logic and a timeout-based fallback in the receiving system that can detect missed or delayed events and poll the Contentstack CDA or CMA for the latest content state if an expected event hasn’t arrived within a tolerance window.
    
2.  For large bulk publishes: consider splitting the bulk operation into smaller sequential batches (for example, 5–10 entries at a time with a brief pause between batches) to reduce the spike in webhook events generated at a single point in time.
    
3.  If sustained webhook delays are impacting production operations, contact Contentstack Support and provide the time window, bulk job details, and the delay observed. Engineering can investigate queue health for the specific region.
    
4.  Monitor webhook delivery times via the execution logs in the Contentstack dashboard to establish a baseline and detect anomalies proactively.
    

After implementing the fallback polling strategy for time-sensitive systems, confirm that downstream processes continue correctly even when webhook delivery is delayed.

### system_action: GLOBAL_FIELD_UPDATE in Webhook Payload - Expected Behavior

A webhook payload for a specific entry contains the attribute system\_action: “GLOBAL\_FIELD\_UPDATE” while similar webhook events for other entries do not contain this attribute. The customer is unsure why this value is appearing.

**Root Cause**

The system\_action: “GLOBAL\_FIELD\_UPDATE” attribute is set in the webhook payload when a Global Field used within a Content Type is updated. When a Global Field’s schema is modified and saved, Contentstack propagates the schema change to all Content Types that reference the Global Field. During this propagation, the system internally updates the affected entries and sets the system\_action flag to GLOBAL\_FIELD\_UPDATE to indicate that the event was triggered by a Global Field update rather than a direct editorial action on the entry itself.

**Resolution**

This is expected, documented behavior. No action is required. To handle this in the webhook receiver:

1.  Check the system\_action field in the webhook payload before processing. If system\_action is GLOBAL\_FIELD\_UPDATE, the event was triggered by a Global Field schema change propagation rather than a direct user edit or publish action.
    
2.  Decide in the receiver whether to process or skip events with system\_action: GLOBAL\_FIELD\_UPDATE based on the use case. For cache invalidation workflows, these events may still warrant a cache purge. For audit or change-tracking workflows, these events should be labeled distinctly from user-initiated changes.
    
3.  If GLOBAL\_FIELD\_UPDATE events are being triggered unexpectedly (for example, without any recent Global Field changes), contact Contentstack Support with the entry UID and the timestamp of the event for investigation.
    

After updating the receiver logic to handle system\_action: GLOBAL\_FIELD\_UPDATE, confirm that the webhook processing correctly categorizes and routes these events separately from user-initiated content events.

### Webhooks Do Not Consume Delivery API Rate Limits

A customer asks whether webhook triggers consume their Delivery API rate limit. They are concerned that a high volume of webhook events (from publish, unpublish, delete, and workflow operations) will push their application toward the Delivery API rate limit.

**Root Cause**

Webhooks are processed internally by the Contentstack platform and do not consume the Delivery API rate limit. Each webhook trigger counts as a Management API operation internally, but the outbound webhook delivery itself is a separate system from the Delivery API rate limit budget.

**Resolution**

To clarify webhook rate limit behavior:

*   Webhooks do not consume Delivery API rate limits simply by existing or firing.
    
*   The outbound webhook delivery (Contentstack sending the HTTP POST to the endpoint) does not count against the CDA or CMA rate limit.
    
*   High webhook volumes do contribute to overall system load. Very high volumes of events (for example, from a runaway automation making thousands of CMA PUT requests per hour) can create webhook queue pressure and affect delivery latency.
    
*   If a webhook receiver makes Contentstack API calls upon receiving events (for example, fetching the updated entry from the CDA), those API calls do count against the Delivery API rate limit. Monitor those calls and apply caching to reduce unnecessary lookups.
    

If a webhook is continuously triggering due to a high volume of API updates (for example, an automation making many CMA PUT requests), review the automation’s logic to reduce unnecessary updates rather than treating it as a rate limit issue.

### Exporting Webhook Execution Logs - No Native S3 Integration

A customer wants to export webhook execution logs and audit logs to an S3 bucket for long-term storage and monitoring. They ask whether Contentstack provides an S3 destination or similar log export capability.

**Root Cause**

Contentstack does not currently provide a native integration to export webhook execution logs or audit logs directly to an external storage destination such as Amazon S3, Google Cloud Storage, or Azure Blob Storage. Log export is not available as a built-in platform feature.

**Resolution**

1.  Use the Contentstack webhook execution logs API to programmatically retrieve logs. The API returns a list of webhook execution records including event type, payload, response code, timestamp, and delivery status.
    
2.  Schedule a periodic job (AWS Lambda, cron, or similar) to call the logs API and write the results to S3 or your preferred log storage.
    
3.  For audit logs specifically, use the Contentstack Audit Log API: GET /v3/audit-logs - this returns organization-level activity records that can be periodically exported.
    
4.  If real-time log streaming is required, configure your webhook receiver to log all inbound webhook payloads to your preferred observability platform (Datadog, Splunk, CloudWatch) as they arrive, rather than relying on Contentstack’s log export.
    

After setting up a scheduled log export script, confirm that webhook execution records are correctly written to S3 with the required fields and that the script handles pagination for large log volumes.

### Webhook Sync ‘Socket Hang Up’ Error - Upgrade sync-core SDK

A DataSync or webhook sync receiver encounters the error: sync-core Error \[check\] Error: socket hang up. The webhook receiver stops working after this error and requires a manual restart to recover. There is no automatic reconnection after a socket error.

**Root Cause**

The socket hang up error is caused by a connection disruption between the sync-core SDK and the Contentstack sync service. In affected versions of the sync-core SDK, a socket hang up does not trigger automatic reconnection, requiring a manual service restart. A fix has been released in a more recent version of the SDK.

**Resolution**

1.  Upgrade to the latest version of the sync-core SDK. The fix for the socket hang up reconnection issue is included in the release - check the sync-core SDK changelog for the specific version that includes the fix.
    
2.  After upgrading, verify that a simulated socket disconnection (for example, a brief network interruption) triggers automatic reconnection without requiring a manual restart.
    
3.  Implement a process supervisor (such as PM2 for Node.js, systemd, or a Kubernetes restart policy) as an additional safety net to automatically restart the sync-core process if it terminates unexpectedly.
    

After upgrading the SDK and confirming automatic reconnection, monitor the sync receiver for 24 hours to confirm the socket hang up no longer requires manual intervention.

<!-- case:00060794 status:draft synced:false bucket:"Webhooks & External Integrations" -->
### Webhook Executions Not Triggering After Entries Are Published

Webhook executions may stop triggering after publishing entries, with the publish queue also failing to process as expected.

**Root Cause**

An indexing configuration mismatch caused some indexes to be automatically created with incorrect mappings, resulting in repeated processing attempts and a backlog in the publish queue that prevented webhook executions from firing.

**Resolution**

1.  Confirm that entries are publishing successfully but configured webhooks are not executing, and that the publish queue shows a growing backlog.

2.  Gather the stack API key and sample cURL requests for Get Entry, Webhook Executions, and Publish Queue for the affected entries.

3.  Contact Contentstack Support with these details so the indexing configuration can be checked and the affected indexes recreated with correct mappings.

After Contentstack Support recreates the affected indexes, publish an entry and confirm the publish queue clears without a backlog and the webhook executes as expected. Escalate with the stack API key and the affected entry UIDs if webhook executions still fail to trigger.

<!-- end:00060794 -->

## Custom Extensions, Live Preview & Analytics

### Resolving null User-Agent values in usage reporting

Usage metrics in the dashboard may display "null" for device or browser categories when processing API requests. This prevents accurate reporting and attribution of traffic to specific platforms or devices.

**Root Cause**

The calling client or integration script is not sending a User-Agent header in the HTTP request.

**Resolution**

1.  Review all direct HTTP integrations, custom scripts, or backend services making API calls.
2.  Ensure every request includes a valid and descriptive User-Agent header.
3.  Verify that asset-heavy flows are not bypassing header configurations.

After updating the scripts to include a User-Agent header, monitor the usage logs or dashboard. If the "null" values are replaced by the specified User-Agent strings, the reporting discrepancy is resolved.

### Customizing visibility behavior for DateTimePicker component

Integrating the DateTimePicker component in a custom UI may result in the popup being visible simultaneously with the input field. This prevents achieving a "click-to-show" behavior similar to standard text inputs.

**Root Cause**

The DateTimePicker component does not include a native configuration to toggle visibility only on user interaction.

**Resolution**

1.  Implement a state variable in the front-end code to manage visibility.
2.  Use the onFocus event of the input field to set the state to show the picker.
3.  Use the onBlur event of the input field to set the state to hide the picker.
4.  Render the DateTimePicker component conditionally based on the state variable.

After implementing the conditional logic, click on the date input field in the application. If the popup UI appears only upon clicking the field and disappears on blur, the implementation is correct.

### Resolving client-side exceptions in Live Preview

Enabling Live Preview in the CMS may result in a client-side exception error when new global fields are added. This prevents the real-time rendering of content changes in the preview pane.

**Root Cause**

A TypeError occurs when the front-end application code attempts to render new global field data that is not yet supported by the existing implementation.

**Resolution**

1.  Inspect the browser console to identify the specific field causing the TypeError.
2.  Verify that the Live Preview SDK is correctly integrated and configured with valid API keys and delivery tokens.
3.  Ensure the Preview URL in stack settings is correct.
4.  Update the front-end code to handle the data structure of the newly added global field.
5.  Clear browser cache and reload the preview window.
6.  Refer to the official Live Preview documentation for complete front-end integration guidance.

After updating the front-end code to handle the new field structure, open the Live Preview window. If the preview renders without an application error, the issue is resolved.

### CORS Error When Accessing the Preview GraphQL Endpoint

A CORS (Cross-Origin Resource Sharing) error occurs when attempting to access the Preview GraphQL endpoint from a browser-based application. The request is blocked due to a missing or incorrect CORS header in the response.

**Root Cause**

CORS errors on the Preview GraphQL endpoint typically occur when the request origin is not included in the allowed origins configured for the stack or when environment-specific configuration details are missing from the request. The Preview endpoint may have additional requirements compared to the standard Delivery endpoint.

**Resolution**

1.  Confirm the request origin (the domain making the browser-side request) matches what is configured in the Contentstack stack settings.
    
2.  Verify the environment specified in the request corresponds to a valid, active environment in the stack.
    
3.  Ensure the correct Preview API token is being used and that it has access to the target environment.
    
4.  If the CORS issue persists after verifying configuration, contact Contentstack Support with the request origin, environment details, and a sample request for further investigation.
    

After verifying and correcting the origin and environment configuration, retry the browser-based request to the Preview GraphQL endpoint. If the CORS error no longer appears, the origin is now permitted.

### GraphQL Preview Endpoint Does Not Support Taxonomy Queries or Nested Where Filtering

Queries that work on the main GraphQL endpoint - particularly those using taxonomy fields or where filtering on nested collection fields - fail or return errors when run against the GraphQL Preview endpoint.

**Root Cause**

The GraphQL Preview endpoint has known feature limitations compared to the main Delivery GraphQL endpoint. Specifically:

*   Taxonomy field queries are not supported on the Preview endpoint
    
*   The where argument for filtering is only available on top-level queries; nested collection filtering is not supported
    

This is a known platform limitation, not a bug or misconfiguration.

**Resolution**

1.  For taxonomy queries, use the main GraphQL Delivery endpoint rather than the Preview endpoint.
    
2.  For nested where filtering, restructure queries to apply filters at the top level where possible.
    
3.  If Preview-specific testing of these features is required, apply post-fetch filtering on the client side after retrieving data via the Preview endpoint.
    

After redirecting taxonomy and nested filter queries to the main GraphQL endpoint, confirm the queries return expected results. If responses are correct, the limitation has been appropriately worked around.

### Live Preview Blank Screen with GraphQL: Object Not Extensible Error

Enabling Live Preview in a Next.js setup with GraphQL results in a blank screen. A runtime error appears stating that a property could not be added because the object is not extensible.

**Root Cause**

The Live Preview SDK’s addEditableTags function attempts to add properties to the GraphQL entry object. If the object returned by GraphQL is frozen or sealed (non-extensible), JavaScript prevents property addition and throws a TypeError. This commonly occurs with GraphQL clients that return immutable response objects.

**Resolution**

1.  Before passing the GraphQL entry object to addEditableTags, create a deep clone of the object to ensure it is mutable.
    
2.  Use a utility such as cloneDeep from the lodash library or JSON.parse(JSON.stringify(entry)) to produce a plain, extensible copy of the entry data.
    
3.  Pass the cloned object to addEditableTags instead of the original GraphQL response object.
    
4.  Verify the Live Preview SDK is correctly configured with valid API keys and the preview URL is set in the stack settings.
    

After implementing the deep clone before addEditableTags, reload the Live Preview window. If the preview renders without a blank screen or runtime error, the frozen object issue is resolved.

### CMS Analytics Shows More Content Types Than Expected Due to Branch Counts

The Stack Dashboard shows a content type count (for example, 333) that far exceeds the actual number of unique content types in the stack (for example, 50). The inflated count is approaching the plan limit, raising billing concerns.

**Root Cause**

CMS Analytics counts content types across all branches in the stack, not just the main branch. Each branch contributes its own copy of the content types to the total count. A stack with 50 unique content types spread across 6 branches shows 300 in Analytics (50 × 6). This aggregated number is used for Analytics display purposes and reflects the total addressable content type count across the entire stack.

**Resolution**

This behavior is by design and does not necessarily indicate a billing problem. Clarify with Contentstack whether plan limits are enforced per-branch or based on unique content types across all branches:

1.  Contact your Customer Success Manager or Contentstack Support to clarify how content type limits are counted for billing in your specific plan.
    
2.  To reduce the count if needed: delete unused branches that are no longer needed, which removes their content type copies from the total count.
    
3.  Note: the main branch content type count is the authoritative number for editorial purposes. The aggregated count in Analytics is for platform-wide monitoring.
    

After discussing the counting methodology with your CSM, confirm whether any action is needed to stay within plan limits.

### Automation ‘Get All Terms’ Returns Empty - Taxonomy Dropdown Not Populated

The Automate Hub ‘Get All Terms (V2)’ action returns no taxonomy values. Although taxonomies exist in the stack and the automation has full authorization access, the ‘Select Taxonomy’ dropdown is empty and automation execution returns blank results. This breaks automations that compile taxonomy values and push data to downstream systems such as Algolia.

**Root Cause**

This was a platform-level bug in the Get All Terms (V2) action in the Automate Hub. A scoping issue caused the action to fail to retrieve taxonomy data despite correct authorization and taxonomy configuration.

**Resolution**

A hotfix was deployed to resolve the issue. The Get All Terms (V2) action should now correctly return taxonomy values.

1.  After the fix deployment, open the affected automation and re-test the Get All Terms (V2) action. If the taxonomy dropdown now populates and execution returns the expected terms, the fix is in effect.
    
2.  If the dropdown remains empty after the fix, try removing and re-adding the Get All Terms action step in the automation to force a refresh of the action’s configuration.
    
3.  If the issue persists, contact Contentstack Support and provide the automation ID, the affected taxonomy UID, and the stack API key.
    

After the fix, verify the full automation runs end-to-end and downstream systems (such as Algolia) receive the correct taxonomy data.

### Using the Preview API Directly Without the Live Preview SDK

A developer attempts to use the Contentstack Preview API from an internal tooling environment outside of the Contentstack editor. They are providing the preview\_token and preview\_timestamp headers but struggling to provide the live\_preview hash. They also need to access future-dated (scheduled) content.

**Root Cause**

Two separate Preview features are relevant here, and they require different approaches: (1) Live Preview returns draft/unpublished content and requires a live\_preview hash generated by the Live Preview SDK from an active editor session. The hash cannot be generated independently outside of the Contentstack editor iframe. (2) Timeline Preview returns future-dated content (entries scheduled for a future publish date) and is accessed via the Preview API using the preview\_token and preview\_timestamp headers - no live\_preview hash is required.

**Resolution**

**For accessing draft content from an internal tool:**

1.  Use the Content Management API (CMA) with a management token instead of the Preview API. The CMA returns the latest saved version of entries, including unpublished drafts, without requiring the live\_preview hash.
    
2.  Alternatively, use the Preview API only within the Contentstack editor context where the Live Preview SDK generates the hash automatically.
    

**For accessing future-dated (scheduled) content:**

1.  Use the Timeline Preview endpoint with the preview\_token and preview\_timestamp headers. Set preview\_timestamp to the ISO date of the future date you want to preview.
    
2.  The live\_preview header is not required for Timeline Preview - only preview\_token and preview\_timestamp are needed.
    

After selecting the correct approach - CMA for drafts, Timeline Preview API for future-dated content - confirm the expected content is returned without requiring the live\_preview hash.

### Bandwidth Spike Investigation - Using Top URLs Analytics

An unexpected increase in bandwidth usage is observed without a corresponding increase in visitor numbers. The cause is unclear and the customer needs to identify which assets or endpoints are driving the usage.

**Root Cause**

Bandwidth spikes without visitor growth are typically caused by a small number of large assets being requested at high frequency, or by external traffic (bots, scrapers, or unauthorized embedding) hitting asset URLs. The Contentstack Product Analytics dashboard provides tools to identify the source.

**Resolution**

1.  Navigate to Product Analytics in the Contentstack dashboard and open the Top URLs section.
    
2.  Sort by bandwidth to identify which asset or API URLs are consuming the most bandwidth. A small number of URLs driving disproportionate bandwidth indicates the root cause.
    
3.  Review the top asset URLs for large file sizes (for example, unoptimized MP4 videos or high-resolution images). Apply image optimization parameters (quality, resize, auto=webp) to reduce per-request bandwidth.
    
4.  If the top URLs correspond to assets not embedded in your own site, check for unauthorized external embedding and enable Secure Public URLs to prevent third-party sites from accessing assets.
    
5.  For video assets, consider serving MP4 files from a dedicated video CDN or streaming service rather than from Contentstack, to avoid bandwidth costs for progressive download.
    

After identifying high-bandwidth URLs and applying optimizations or access restrictions, monitor the bandwidth trend over the following 24–48 hours to confirm the spike has been addressed.

### Live Preview SDK Initialization - Common Configuration Errors

Live Preview fails to initialize or does not update content when editing. Common errors include ‘stackSdk.live\_preview is an invalid key’, the preview pane not reflecting changes, or missing network requests to the preview endpoint.

**Root Cause**

The most common causes are: incorrect SDK initialization structure, the enable flag missing or set to false, required parameters (preview token, app host, host) absent, or the init() call placed in a server-rendered context where it cannot execute.

**Resolution**

1.  Ensure the SDK initialization is structured correctly. The live\_preview configuration must be nested correctly in the stack initialization - not as a top-level key.
    
2.  Include all required fields: enable: true, preview\_token, host, app\_host, and environment.
    
3.  For Next.js App Router: move ContentstackLivePreview.init() into a dedicated Client Component (add ‘use client’ at the top) rather than inside app/layout.jsx. Live Preview must run in a browser context.
    
4.  Add debug: true during setup to surface configuration details in the browser console.
    
5.  Ensure the SDK initialization fires before any GetEntry API calls in the page lifecycle.
    

After correcting the initialization structure and verifying all required parameters, reload the preview pane and confirm that content updates in the editor are reflected in real time.

### Preview Token Feature Not Visible in UI

The Preview Token option is absent from the Tokens section in stack settings. Admin and Developer users cannot see or create Preview Tokens.

**Root Cause**

The Preview Token (previewTokens) feature is not enabled by default for all organizations. It must be enabled at the organization level by Contentstack Support.

**Resolution**

1.  Contact Contentstack Support and request enablement of the previewTokens feature for the organization.
    
2.  Provide the Organization ID and region in the request.
    
3.  After Support confirms enablement, navigate to Settings > Tokens and verify the Preview Token option is now visible.
    

After enablement, confirm Preview Tokens can be created and used for Live Preview initialization.

### Management Token Exposed in Client-Side Code - Use preview_token Instead

During a Live Preview implementation, the management token is visible in browser developer tools when inspecting the network requests or environment variables on the client side.

**Root Cause**

An older Live Preview SDK version requires using a management token in the Live Preview configuration. Newer versions of the SDK support the preview\_token, which is specifically designed for safe client-side use and does not expose management-level access.

**Resolution**

1.  Upgrade the Live Preview SDK to the latest version that supports preview\_token.
    
2.  Replace the management token in the Live Preview configuration with the preview\_token.
    
3.  Generate a Preview Token in Settings > Tokens and use it in the SDK initialization.
    
4.  Remove the management token from all client-side code and environment variables.
    

After switching to preview\_token, inspect the network requests in browser developer tools and confirm the management token is no longer visible.

### Visual Builder Shows ‘Entry Not Found’ on First Selection

In Visual Builder, clicking an entry for the first time shows an ‘Entry not found’ error. The entry only loads correctly after selecting it a second time.

**Root Cause**

A trailing forward slash in the environment URL configuration causes Visual Builder to fail to resolve the entry on the first attempt. Removing the trailing slash allows the entry to load correctly on the first selection.

**Resolution**

1.  Navigate to stack Settings > Environments and select the affected environment.
    
2.  Remove any trailing slash from the base URL for that environment.
    
3.  Save the environment configuration.
    
4.  Reload Visual Builder and confirm entries load correctly on the first selection.
    

After removing the trailing slash, select an entry in Visual Builder and confirm it loads without an ‘Entry not found’ error.

### Live Preview Returns Error 901 - Delivery Token Missing Branch Permission

Live Preview fails with error code 901: ‘Access denied. You have insufficient permissions to perform operation on this branch alias.’

**Root Cause**

The delivery token used for Live Preview does not have access to the branch (or branch alias) being previewed. When a branch alias such as ‘production’ is used, the delivery token must be explicitly granted access to that branch or alias.

**Resolution**

1.  Navigate to Settings > Tokens and select the delivery token used for Live Preview.
    
2.  Update the token’s branch permissions to include the branch or branch alias referenced in the Live Preview configuration.
    
3.  Save the updated token and reload the Live Preview session.
    

After updating the token permissions, restart the Live Preview session. If error 901 no longer appears and content loads correctly, the branch access is now granted.

### Live Preview Not Working in Next.js SSR - SDK Initialization

Live Preview does not update content in a Next.js application using SSR. The SDK initialization appears correct but the preview pane shows stale or unresponsive content.

**Root Cause**

In Next.js SSR environments, the Live Preview SDK must run in a browser context. Placing ContentstackLivePreview.init() inside server-rendered files (such as app/layout.jsx without the ‘use client’ directive) means the SDK never initializes in the browser, so Live Preview cannot receive editor messages.

**Resolution**

1.  Create a dedicated Client Component file (for example, LivePreviewInit.tsx) and add ‘use client’ at the top.
    
2.  Move ContentstackLivePreview.init() with all required parameters into this Client Component.
    
3.  Import and render the Client Component in app/layout.jsx.
    
4.  Ensure preview token, host, and environment are passed correctly in the init configuration.
    

After moving the initialization to a Client Component, reload the page in the editor preview pane. If content updates in the editor are reflected in real time, the initialization is correctly placed.

### Live Preview Not Initialized on All Pages - Only Works on Homepage

Live Preview functions correctly on the homepage but does not work on other pages of the application. Editing content for non-homepage entries has no effect on the preview.

**Root Cause**

ContentstackLivePreview.init() is only called in the homepage component or layout, not globally. For Live Preview to work on all pages - including error pages and 404 pages - the SDK must be initialized on every page of the application.

**Resolution**

1.  Move ContentstackLivePreview.init() to the global layout file (for example, \_app.tsx in Pages Router or app/layout.tsx in App Router) so it executes on every page load.
    
2.  For App Router, ensure it is inside a Client Component as described above.
    
3.  Include initialization even on error pages and 404 pages to prevent tracker errors on those routes.
    

After moving initialization to the global layout, navigate to a non-homepage entry in the editor and confirm the preview updates correctly.

### Live Preview Not Supported with GraphQL

A customer attempts to implement Live Preview using GraphQL queries. The preview does not load draft or unpublished content, and integration guidance is unclear.

**Root Cause**

Live Preview requires a live\_preview hash to be passed with every request to retrieve draft content. The GraphQL API cannot process the live\_preview hash parameter in the same way as the REST API. This makes standard Live Preview integration incompatible with direct GraphQL usage.

**Resolution**

For GraphQL-based implementations:

1.  Use the Live Preview Utils SDK to generate the live\_preview hash from the editor session.
    
2.  Pass both the live\_preview hash and the preview\_token in the GraphQL request headers.
    
3.  Listen for content updates using the SDK’s onEntryChange callback and re-fetch the GraphQL query with the updated hash.
    
4.  Refer to the Contentstack Live Preview with GraphQL documentation for the correct header format and query structure.
    

After implementing the hash-passing pattern in GraphQL headers, confirm that draft content changes in the editor are reflected in the preview response.

### ‘Please Create Tracker Before Starting Live Preview Session’ Error

Live Preview returns the error: ‘Please create tracker before starting live preview session’ (error code 382). The error appears intermittently or consistently during preview sessions.

**Root Cause**

This error occurs when: the Live Preview SDK is not initialized before a GetEntry API call executes, the live\_preview hash passed in the request is invalid or mismatched, or the SDK configuration is missing required fields (enable: true, preview\_token, host, app\_host).

**Resolution**

1.  Verify that ContentstackLivePreview.init() is called before any getEntry or API calls on every page.
    
2.  Ensure enable: true is set in the initialization configuration.
    
3.  Include all required configuration values: preview\_token, host, and app\_host.
    
4.  Add debug: true to the init configuration to log configuration details and identify missing fields.
    
5.  If using branches, verify the preview is configured for the correct branch matching the content being edited.
    

After verifying the initialization order and configuration, reload the Live Preview session. If the error no longer appears and content updates correctly, the tracker is now being created in the correct order.

### Live Preview Edit Button Uses Branch Alias Instead of Actual Branch

When clicking the Edit button in Live Preview, the generated URL references a branch alias (for example, prod\_alias) instead of the actual branch name (for example, main). This causes a ‘branch not found’ error when the link is opened.

**Root Cause**

The Live Preview SDK constructs Edit URLs using the stack\_details value provided during initialization. If prod\_alias is passed as the branch identifier in stack\_details, the SDK uses it verbatim in Edit URLs. Branch alias resolution is not supported in Live Preview Edit URLs - only actual branch UIDs are valid.

**Resolution**

1.  Update the Live Preview SDK initialization to pass the actual branch UID (for example, main) in the stack\_details object instead of the branch alias.
    
2.  Remove any alias references from the branch configuration in the Live Preview init call.
    

After updating the branch reference, click the Edit button in Live Preview and confirm the generated URL correctly references the actual branch and opens the entry in the editor.

### ‘Live Preview Service Not Enabled’ Error Despite Live Preview Being Configured

After configuring Live Preview, error messages appear stating the Live Preview service is not enabled in the stack. The stack has Live Preview turned on but the error persists.

**Root Cause**

This error appears when the stack is using the legacy Live Preview setup and has not yet migrated to Contentstack’s new Preview service. The new Preview service is required for features such as Timeline Preview and Visual Builder. The legacy SDK and new Preview service are not directly interchangeable.

**Resolution**

1.  Migration to the new Preview service is optional - the legacy Live Preview setup will continue to function for basic preview use cases.
    
2.  To resolve the error and gain access to Timeline Preview and Visual Builder, follow the Live Preview Migration Guide to upgrade to the new Preview service.
    
3.  After migrating, update the SDK initialization to use the new configuration format and preview\_token instead of the management token.
    
4.  Refer to the corrected Live Preview Onboarding and Troubleshooting Guide provided by Contentstack Support for the updated setup steps.
    

After completing the migration, reload the Live Preview session and confirm the service-not-enabled error no longer appears and preview features work as expected.

### Unpublished or Draft Content Not Visible in Live Preview

Live Preview does not show unpublished or draft content. When editors make changes and try to preview them, the preview renders the last published version rather than the draft state.

**Root Cause**

ContentstackLivePreview.init() must be called on every page - including error pages and 404 pages - for the Live Preview session to be active and capable of returning draft content. If the init() call is missing on a page, the SDK falls back to the standard CDA, which returns only published content.

**Resolution**

1.  Ensure ContentstackLivePreview.init() is called in the global layout or on every page of the application, not just the homepage or specific routes.
    
2.  Verify the enable: true flag is set in the initialization and the correct preview\_token and environment are provided.
    
3.  When the Live Preview session is active, the SDK automatically fetches draft content. When accessed normally outside a preview session, the SDK returns only published content - this is the expected dual behavior.
    

After adding the init() call to all pages, navigate to an unpublished entry in the editor and open Live Preview. If draft content is visible in the preview pane, the initialization is correctly applied globally.

### Live Preview Cannot Show Scheduled (Future-Dated) Content

Editors want to use Live Preview to see how content scheduled for a future publish date will appear on the site before it goes live. Live Preview does not appear to support previewing scheduled content.

**Root Cause**

Live Preview is designed to preview the current draft and unpublished state of entries. It does not support previewing content at a future scheduled publish date. The feature renders what the entry looks like now, not how it will look after a future publish action completes.

**Resolution**

Scheduled content preview is not supported in Live Preview. Available alternatives:

1.  Use Releases to group future-dated content and review it as a set before scheduling the release deployment.
    
2.  Create a dedicated staging environment and manually publish the scheduled content there to preview the future state.
    
3.  Use the Timeline feature (available with the new Preview service) to step through published versions of content over time.
    

Document this limitation for editorial teams so they understand that Live Preview reflects current draft state, not future scheduled state.

### addEditableTags TypeScript Type Mismatch with CLI-Generated Models

TypeScript type validation fails when calling addEditableTags() with CLI-generated entry models. The error indicates a type incompatibility between the generated types and the types expected by addEditableTags.

**Root Cause**

CLI-generated models include SystemFields in the type definition. The addEditableTags function expects the entry object to include a uid property, but TypeScript cannot confirm this at compile time because SystemFields may not always expose uid in the type signature.

**Resolution**

1.  Add a runtime check before calling addEditableTags to verify the uid property exists: if (‘uid’ in entry) { … }
    
2.  After the runtime check, apply a type assertion to satisfy TypeScript: addEditableTags(entry as EntryEmbeds, ‘content\_type\_uid’)
    
3.  This approach maintains type safety without modifying generated code or utility definitions.
    

After implementing the runtime check and type assertion, confirm TypeScript compilation succeeds and addEditableTags applies edit tags correctly to the entry.

### Live Edit Tags Must Be Applied to Raw Contentstack Response

The Live Preview Edit button does not function when clicking on components in the preview. Edit icons appear but clicking them does not open the correct field in the editor.

**Root Cause**

addEditableTags must be called on the raw Contentstack API response object, not on a transformed or reshaped version of the data. If data is restructured before addEditableTags is called, the data-cslp attributes are generated incorrectly and cannot be mapped back to the correct fields.

**Resolution**

1.  Call addEditableTags on the entry object directly as returned by the Contentstack SDK or API, before any transformation or mapping.
    
2.  Do not hardcode data-cslp attribute values - they must be derived dynamically from the raw entry structure.
    
3.  If using a deep clone before addEditableTags (for example, to handle frozen GraphQL response objects), ensure the clone is a plain, extensible object.
    

After applying addEditableTags to the raw entry response, click a component in the Live Preview pane. If the correct field opens in the editor, the tags are correctly mapped.

### Referenced Sub-Entries Appear Empty in Live Preview for a Specific Locale

When previewing a parent entry (for example, a homepage) in a specific locale such as pt-pt, referenced sub-entries appear empty in the preview even though they have content in the master locale.

**Root Cause**

Live Preview does not support automatic locale fallback for referenced entries. If a referenced sub-entry has not been localized for the previewed locale, Live Preview returns empty content for that reference - it does not fall back to the master locale automatically, unlike the standard CDA.

**Resolution**

1.  Localize all referenced sub-entries for the locale being previewed.
    
2.  Remove or update references to deleted sub-entries to prevent empty slots in the preview.
    
3.  Ensure the front-end application’s Live Preview fetch logic explicitly handles missing referenced entries to prevent rendering failures.
    

After localizing the referenced entries, reload the Live Preview for the affected locale and confirm sub-entries now render with the expected content.

### QuotaExceededError in Live Preview - localStorage Quota

A QuotaExceededError appears in the browser console during a Live Preview session. The error references localStorage and occurs within an iframe environment.

**Root Cause**

The Contentstack Delivery SDK uses localStorage to cache frequently accessed content for performance. Browser storage quotas apply per origin domain and are unaffected by iframe embedding. When the localStorage quota for the Contentstack domain is exhausted, the error is triggered.

**Resolution**

1.  Open browser developer tools and navigate to Application > Storage to inspect localStorage usage for the Contentstack domain.
    
2.  Clear the localStorage for the Contentstack domain to free up space.
    
3.  If the issue recurs, consider reducing the amount of data cached by the SDK or implementing a periodic cache cleanup in the application.
    

After clearing localStorage, reload the Live Preview session and confirm the QuotaExceededError no longer appears in the console.

### Visual Builder Popup Empty for Rich Text Fields

In Visual Builder, clicking the Edit button on a rich text field opens a popup that is completely empty. The rich text content is visible and correct in the right-hand editor panel, but the inline edit popup shows nothing.

**Root Cause**

The data-csl-value attribute for the rich text field contains escaped HTML rather than raw HTML. Visual Builder requires the data-csl-value to contain unescaped, raw HTML. If the front-end framework escapes the HTML before rendering the attribute, the popup cannot parse the content.

**Resolution**

1.  Ensure the data-csl-value attribute contains raw, unescaped HTML.
    
2.  Confirm that the Live Preview SDK is initialized in builder mode for Visual Builder sessions.
    
3.  Verify the front-end framework is not escaping the HTML value when spreading tag attributes (for example, in React: <div {…entry.$?.body ?? {}} dangerouslySetInnerHTML={{…}} />).
    
4.  Use the correct tag spreading syntax to ensure data-cslp and data-csl-value are set without HTML escaping.
    

After correcting the data-csl-value to contain raw HTML, click the Edit button on the rich text field in Visual Builder. If the popup displays the content correctly, the attribute value is now unescaped.

### Live Preview CSP Block Errors

Content Security Policy (CSP) block errors appear in the browser console when using Live Preview. The errors prevent the preview iframe from loading or communicating with the editor.

**Root Cause**

The application’s CSP headers do not include the Contentstack app domains required for Live Preview to function. The preview iframe communicates via postMessage between the Contentstack editor (app.contentstack.com) and the preview application. If the CSP blocks frame-ancestors, connect-src, or frame-src for Contentstack domains, the preview fails.

**Resolution**

1.  Review the application’s Content Security Policy headers.
    
2.  Add the following Contentstack domains to the appropriate CSP directives:
    

*   frame-ancestors: app.contentstack.com, eu-app.contentstack.com (and other regional variants)
    
*   connect-src: \*.contentstack.com, \*.contentstack.io
    

1.  If the application is served via a CDN or reverse proxy, update the CSP there as well.
    
2.  After updating the CSP, reload the Live Preview session and confirm no CSP block errors appear in the console.
    

After updating the Content Security Policy to allow Contentstack domains, reload the preview. If Live Preview loads without CSP errors and the editor communicates with the preview, the policy is correctly configured.

### Live Preview Hash - Required on Every Request and Cannot Be Reused

A developer asks why the live\_preview hash must be included on every API request during a Live Preview session, whether it can be cached or reused across entries, and how long it remains valid.

**Root Cause**

The live\_preview hash represents the exact editor session state at the time of the request, including draft and unpublished changes specific to that editor’s session. Because the hash is perishable and session-specific, it cannot be reused across sessions, users, or entry fetches.

**Resolution**

*   The hash must be included in every API request during a Live Preview session to ensure the response reflects the editor’s current draft state.
    
*   The hash cannot be reused across different editor sessions or users - each session generates a unique hash.
    
*   Prefetching or caching preview responses is limited because the hash changes with each edit action.
    
*   Implement the onEntryChange callback from the Live Preview SDK to detect when content changes and re-fetch with the latest hash.
    

Design the Live Preview data-fetching logic to always retrieve the current hash from the SDK before making API calls, rather than caching or reusing a previously obtained hash.

### Live Preview Mode Must Be Set to ‘builder’ for Preview Share Link Comments

When using the Preview Share Link feature, users cannot add comments on the shared preview. The comment functionality does not appear or is non-functional.

**Root Cause**

Preview Share requires the Live Preview SDK to be initialized in builder mode. If the mode is set conditionally based on query parameters rather than always set to builder, the Preview Share Link feature will not receive the correct mode and comment functionality will fail.

**Resolution**

1.  Update the Live Preview SDK initialization to always set mode to ‘builder’ - do not make this conditional on query parameters.
    
2.  Ensure the SDK is initialized with the correct Preview API configuration alongside the builder mode setting.
    

After setting mode: ‘builder’ unconditionally in the SDK initialization, reload the Preview Share Link and confirm that comment functionality is available and operational.

### Analytics Dashboard Access - Only Organization Owners and Admins

A user with stack-level Admin, Content Manager, and Developer roles cannot access the Analytics dashboard. The Analytics tab is not visible for that user.

**Root Cause**

Analytics access in Contentstack is restricted to Organization-level Owners and Admins only. Stack-level roles - regardless of their permission level - do not grant access to the Organization Analytics dashboard.

**Resolution**

1.  If the user requires Analytics access, assign them the Organization Admin or Organization Owner role at the organization level.
    
2.  If full Organization Admin access is not appropriate, note that stack-level Analytics access is not separately configurable - this is a platform limitation.
    

After assigning the Organization Admin role, ask the user to log out and back in, then confirm the Analytics dashboard is accessible.

### 404 Error When Calling Brand Kit or Gen AI API - Wrong HTTP Method

An API call to the Brand Kit API or Gen AI API returns a 404 error or unexpected response data despite using the correct endpoint URL, variables, and authentication headers.

**Root Cause**

The API call is using the wrong HTTP method. The Brand Kit API requires POST requests, not GET. Similarly, the Gen AI API requires GET, not POST. Using the incorrect method causes the server to return 404 (method not found) or unexpected response data.

**Resolution**

1.  Review the Contentstack API documentation for the specific endpoint to confirm the required HTTP method.
    
2.  For the Brand Kit API: switch the request method to POST.
    
3.  For the Gen AI API: switch the request method to GET.
    
4.  Retain all existing headers and body parameters and re-run the request with the correct method.
    

After updating the HTTP method, re-run the API call and confirm a valid response is returned without a 404 error.

### Visual Builder Requires Live Preview Implementation First

A customer attempts to use Visual Builder but cannot access it, or sees errors when navigating to the Visual Editor. They believe it is a platform bug.

**Root Cause**

Visual Builder requires Live Preview to be configured and implemented in the front-end application. Visual Builder communicates with the front-end through the Live Preview connection. Without Live Preview, Visual Builder has no channel to render or edit content.

**Resolution**

1.  Implement Live Preview first: install the @contentstack/live-preview-utils SDK, configure ContentstackLivePreview.init() with the correct stack credentials, and deploy the application with the preview endpoint accessible.
    
2.  Configure the Live Preview URL in Settings > Live Preview to point to the preview deployment.
    
3.  Once Live Preview works and entries load in the preview pane, Visual Builder becomes accessible from the entry editor.
    

After Live Preview is fully implemented, navigate to an entry and click Open Visual Builder to confirm the builder loads and fields are editable inline.

### ‘Invalid Input’ Error When Adding Snippet Blocks in Visual Builder

Users encounter an ‘Invalid Input’ error when adding snippet blocks through Visual Builder Forms, even before content is added to the new block.

**Root Cause**

The error occurs when reference field values are added directly via Visual Builder Forms without the reference being pre-populated inside the entry first. Without a pre-existing value, the form cannot construct a valid CSLP tag path, causing the invalid input error.

**Resolution**

1.  Before using Visual Builder to add or edit a reference field, open the entry in the standard entry editor and add at least one value to the reference field.
    
2.  Save the entry.
    
3.  Now open Visual Builder - the pre-populated reference field will allow further additions without the Invalid Input error.
    

After pre-populating the reference field in the entry editor, open Visual Builder and confirm snippet blocks can be added without the Invalid Input error.

### ‘Invalid CSLP Tag’ Error for Fields in Referenced Entries

Visual Builder throws an ‘Invalid CSLP tag’ error when editing fields within referenced entries. Fields in the parent content type work correctly.

**Root Cause**

The error is caused by path discontinuity. When fields are nested inside a referenced content type via a template/wrapper structure, Visual Builder attempts to construct the CSLP tag path but the path includes a reference boundary that is not correctly traversed.

**Resolution**

1.  Ensure addEditableTags() is called on referenced entry objects individually, not just on the parent entry.
    
2.  For nested reference structures, call addEditableTags on each resolved reference’s data object at the correct depth level.
    
3.  Confirm the CSLP tag attributes contain the full path from the root entry, including the reference field UID and the referenced entry’s UID.
    

After ensuring addEditableTags is applied at each reference level, reload Visual Builder and confirm fields in referenced entries are editable without Invalid CSLP tag errors.

### Japanese and Chinese Text Causes Line Breaks and Cursor Jumps in Visual Builder

Typing Japanese or Chinese characters in Visual Builder snippet fields causes text to break onto a new line, cursor jumps, or character duplication.

**Root Cause**

This is a known IME (Input Method Editor) input composition issue. During the composition phase, Visual Builder’s field event handling incorrectly processes composition events as final input, causing premature line breaks and cursor jumps.

**Resolution**

1.  As a workaround: compose Japanese or Chinese text in a separate text editor first, then copy and paste the completed text into the Visual Builder field.
    
2.  Alternatively, use the standard entry editor (not Visual Builder) for content in Japanese or Chinese locales.
    
3.  Contact Contentstack Support to check the current fix status for IME composition in Visual Builder.
    

After applying the copy-paste workaround, confirm content in Japanese or Chinese is entered correctly without duplication or cursor issues.

### UI Extension Not Triggering When Entry Is Saved from Visual Builder

A UI extension that updates a group field when an entry is saved works correctly from the standard entry editor but does not trigger when saving via Visual Builder.

**Root Cause**

Visual Builder’s save operation uses a different code path than the standard entry editor save. Extensions listening to editor-specific lifecycle events may not receive signals from Visual Builder’s save mechanism.

**Resolution**

1.  Review the extension code to use App SDK lifecycle hooks rather than editor-specific event listeners.
    
2.  Use ContentstackSDK.entry.onSave() if available in the App SDK version being used.
    
3.  If the extension cannot be adapted, implement the logic as a webhook instead - webhooks fire on save/publish events regardless of which authoring surface triggered the action.
    

After adapting the extension to use App SDK lifecycle hooks, test saving from both the standard entry editor and Visual Builder. Confirm the group field updates in both cases.

### Live Edit Tags Not Working with GraphQL - addEditableTags on Connection Structure

addEditableTags() does not work when entry data comes from a GraphQL response. Edit icons do not appear on the frontend.

**Root Cause**

GraphQL responses use a connection structure: connection > edges > node. When this structure is passed directly into addEditableTags(), the function cannot traverse the nested layers to generate CSLP tag paths.

**Resolution**

1.  Before calling addEditableTags(), extract the entry node from the GraphQL response: const entry = response.data.allContentType.edges\[0\].node
    
2.  Pass the extracted node (the flat entry object) to addEditableTags() rather than the full GraphQL response.
    
3.  Ensure addEditableTags() receives the raw, unmodified entry node object.
    

After extracting the node before calling addEditableTags(), reload in Live Preview mode and confirm edit icons appear correctly on all editable fields.

### Save and Publish Buttons Not Visible in Visual Editor on Small Screens

When using the Visual Editor on a laptop or smaller screen, the Save and Publish buttons are not visible. They render correctly on external monitors.

**Root Cause**

On smaller screen widths (typically below 1440px), the Visual Editor’s top action bar does not correctly adjust its layout, causing action buttons to overflow beyond the visible area.

**Resolution**

1.  Zoom out the browser to 80-90% (Ctrl+- or Cmd+-) to reveal the action bar buttons.
    
2.  Use an external monitor at a higher resolution.
    
3.  Use keyboard shortcut Ctrl+S / Cmd+S to save without using the button.
    

After zooming out the browser, confirm Save and Publish buttons are visible and functional in the Visual Editor.

### Visual Builder Scroll Locked on Initial Load - Cookie Consent Popover

When opening Visual Builder, the page is stuck on initial load and users are unable to scroll down. The scroll appears completely locked, preventing interaction with the page content.

**Root Cause**

A cookie authorization popover or consent banner on the preview site is causing the scroll to remain locked even after it is dismissed. The popover intercepts scroll events at the page level and Visual Builder’s iframe cannot unlock the scroll after the popover state changes.

**Resolution**

1.  Dismiss the cookie consent banner immediately when Visual Builder first loads. Once dismissed, scroll should be restored.
    
2.  If the scroll remains locked after dismissal, refresh the Visual Builder session.
    
3.  To prevent this recurring: configure the preview site to suppress cookie consent popovers when loaded in the context of Visual Builder (for example, detect the Contentstack live\_preview query parameter and skip the consent UI).
    
4.  Alternatively, pre-accept the cookie consent in the browser before opening Visual Builder, so the popover does not appear.
    

After dismissing the cookie popover and refreshing if needed, confirm Visual Builder loads with full scroll functionality and all content sections are accessible.

### ‘Invalid Input’ in Visual Experience From Default Value Fields or Custom Integration Fields

An ‘Invalid Input’ error occurs in Visual Experience. In one pattern, entry creation fails in Visual Experience for a content type when fields have default values configured. In another pattern, the error occurs when interacting with Bynder or similar custom integration asset fields even without modifying them.

**Root Cause**

Two distinct root causes produce the same Invalid Input error:

*   Default value initialization failure (JIRA VB-1457): Visual Experience encounters a failure while processing undefined data during the initialization of fields with default values. This is a platform bug.
    
*   Custom integration field regression: recent platform fixes inadvertently affected how certain third-party integration fields (such as Bynder asset picker) pass their data through Visual Experience’s form layer. Fields that were previously working began returning Invalid Input after the fix.
    

**Resolution**

**For default value initialization failures:**

1.  A platform fix has been deployed (JIRA VB-1457). Entry creation in Visual Experience should now work correctly for content types with default value fields.
    
2.  If the error persists after the fix, contact Contentstack Support with the content type UID and the specific fields that have default values.
    

**For custom integration field regressions (Bynder, etc.):**

1.  Contact Contentstack Support and report the Invalid Input error with the integration name, the specific field type, and a description of the actions that trigger it.
    
2.  As a workaround: use the standard entry editor instead of Visual Experience for entries containing the affected integration fields until the regression is resolved.
    

After the relevant platform fix is deployed, confirm entry creation and editing in Visual Experience work without Invalid Input errors for both default value fields and custom integration fields.

### Visual Builder Not Supported for Anchor-Tag Navigation and Non-Entry Dynamic Pages

Visual Builder / Live Preview does not work correctly for pages that use anchor tag-based navigation (#section links) or for dynamically generated pages that do not exist as standalone entries in Contentstack (for example, pages rendered from a template entry with data populated from external integrations).

**Root Cause**

Visual Builder is designed to edit content entries that exist as standalone entries in Contentstack. Two unsupported scenarios: (1) anchor tag navigation - Visual Builder does not support in-page scroll navigation via hash (#) URLs; the LP session uses the base URL and cannot track anchor positions. (2) Non-entry dynamic pages - pages rendered programmatically from templates using external data sources (CVent, APIs, etc.) do not have a corresponding Contentstack entry for Visual Builder to edit.

**Resolution**

These are known platform limitations for Visual Builder:

1.  For anchor-tag navigation pages: use the standard entry editor to make content changes, then verify the result on the published page. Visual Builder cannot navigate to specific anchor sections.
    
2.  For dynamic template pages without standalone entries: consider restructuring so each unique page has its own entry in Contentstack. If this is not feasible, use the entry editor for template content changes and preview using the standard delivery URL.
    
3.  Contact Contentstack Support to register interest in anchor navigation support and non-entry page support for Visual Builder - these are tracked for future roadmap consideration.
    

After understanding the limitations, confirm the editorial team uses the appropriate authoring surface (Visual Builder for standalone entry pages, entry editor for anchor-nav and dynamic template pages).

### Live Preview Not Loading Ads - iframe Restrictions

Live Preview fails to render certain content (particularly ads or embedded third-party widgets) in the preview pane. The content loads correctly on the published site.

**Root Cause**

Google Ads and many third-party providers explicitly block rendering inside iframes. Since Live Preview loads in an embedded iframe, ad content is blocked by the provider’s X-Frame-Options or frame-ancestors CSP directives.

**Resolution**

1.  Enable the ‘Live Preview outside iframe’ feature in the stack settings. This opens Live Preview in a separate browser tab rather than an embedded iframe, bypassing iframe restrictions.
    
2.  Navigate to Settings > Live Preview and toggle the ‘Open in new tab’ or ‘Outside iframe’ option if available.
    
3.  Contact Contentstack Support to enable the LivePreview outside iframe feature if the toggle is not visible.
    

After enabling Live Preview outside iframe, confirm that ad content renders correctly in the preview and editorial workflows are unblocked.

### Live Preview Blocked by Vercel Deployment Protection - 401 Error

Live Preview returns a 401 Unauthorized error when attempting to load a preview URL hosted on Vercel. The preview works on localhost but not on the Vercel deployment.

**Root Cause**

Vercel Deployment Protection requires authentication before serving pages. When Contentstack’s Live Preview attempts to load the URL, the authentication cookie is not present, causing a 401. Vercel may also set X-Frame-Options: DENY.

**Resolution**

1.  In Vercel Project Settings > Deployment Protection, create a Protection Bypass Secret.
    
2.  Add the bypass secret as a query parameter to the Live Preview base URL in Contentstack: https://your-preview.vercel.app?x-vercel-protection-bypass={your-secret}
    
3.  Alternatively, configure Vercel to allow Contentstack app domains in trusted origins for the deployment protection bypass.
    
4.  If X-Frame-Options is blocking iframe embedding, enable ‘Open Live Preview in new tab’ to avoid the iframe requirement.
    

After configuring the bypass secret, reload Live Preview and confirm content loads without a 401 error.

### Live Edit Button Appearing in Production Environment

The Live Preview edit button (#cslp-tooltip) appears on the production website even though Live Preview is not configured for production.

**Root Cause**

The production build is including the full Live Preview SDK rather than the lightweight build, so Visual Builder components - including the edit button (#cslp-tooltip) - are bundled and injected into the production DOM even when a Live Preview token is not defined.

**Resolution**

1.  Set the PURGE\_PREVIEW\_SDK=true environment flag in .env.production (for Next.js projects using @contentstack/live-preview-utils). This swaps in the lightweight SDK build, which excludes Live Preview and Visual Builder components - including the edit button - from the production bundle.
    
2.  Rebuild and redeploy the production environment after adding the flag.
    
3.  If the edit button or Visual Builder code persists in the production bundle/DOM after correctly applying PURGE\_PREVIEW\_SDK=true, this is a known SDK-bundling issue rather than a configuration mistake. Confirm you are on the latest SDK version, and if the issue persists, contact Contentstack Support with your @contentstack/live-preview-utils version and a description of the persisting behavior.
    

After redeploying with the flag applied, confirm the edit button overlay no longer appears in production and, if it does, escalate to Support rather than assuming a coding error.

### ‘Preview Service Not Enabled’ Error Despite Live Preview Being Configured

After configuring Live Preview, the preview pane shows ‘Preview Service Not Enabled’. The stack has Live Preview enabled in settings.

**Root Cause**

This error appears when the application opens with the live\_preview hash in the URL, but is not sending requests that include this hash to the preview host. The SDK is not correctly intercepting and modifying API requests to include the live\_preview parameter.

**Resolution**

1.  Verify ContentstackLivePreview.init() includes: host, app\_host, enable: true, and preview\_token.
    
2.  Ensure data-fetching calls use the Contentstack SDK (not raw fetch/axios) so Live Preview SDK can intercept them to include the live\_preview hash.
    
3.  In Next.js, ensure the SDK is initialized in a Client Component (with ‘use client’) so it runs in the browser context.
    
4.  Add debug: true to init() to output hash interception status to the browser console.
    

After verifying SDK initialization and SDK-based data fetching, reload the preview and confirm the ‘Preview Service Not Enabled’ message is replaced by the correct entry preview.

### Live Preview Blank or Partial for Custom Roles - Missing Environment Permissions

Live Preview works correctly for Admin and Developer users but shows a blank or partial preview for custom role users.

**Root Cause**

Custom roles require explicit environment access permissions for Live Preview. If the custom role does not have access to the preview environment, Live Preview API calls return 401/403 and the preview pane cannot load content.

**Resolution**

1.  Navigate to Settings > Roles and Permissions and open the custom role configuration.
    
2.  Under Environments, add the preview environment to the allowed environments for this role.
    
3.  If using a preview token for Live Preview, ensure the preview token also has access to the correct environment.
    
4.  Save the role and ask the affected user to log out and back in.
    

After adding the preview environment to the custom role, log in as the affected user and confirm Live Preview renders content correctly.

### Live Preview Base URL Switches Locale When Preview Panel Opens

The en-us base URL unexpectedly switches to another locale as soon as the Live Preview panel opens. Consistent even in incognito mode.

**Root Cause**

The lpUrlLocaleWise configuration controls which URL to use per locale. If this configuration maps the current locale to a different environment URL, the base URL changes when the SDK applies locale-based URL routing.

**Resolution**

1.  Check localStorage for the lpUrlLocaleWise value in browser developer tools to inspect the current locale-to-URL mapping.
    
2.  Review the ContentstackLivePreview.init() configuration for the livePreviewEntry URL mapping - confirm the en-us locale is not incorrectly mapped.
    
3.  Ensure the staging environment has separately configured URL mappings rather than sharing with dev.
    

After correcting the locale-to-URL mapping, open the preview panel and confirm the base URL remains correct for the content locale.

### Changes Not Reflecting After Save and Publish in Live Preview

Changes made to entries are not reflected in Live Preview after saving and publishing. The editor panel shows updated content but the preview shows the old version.

**Root Cause**

Causes include: the onEntryChange callback not being registered, the Contentstack SDK not being used for data fetching, or CDN/application-level caching serving old content to the preview URL.

**Resolution**

1.  Register the onEntryChange callback: ContentstackLivePreview.onEntryChange(() => { /\* re-fetch entry and update state \*/ }). This fires whenever the editor saves a change.
    
2.  Ensure all data fetching in the preview context uses the Contentstack SDK so the live\_preview hash is included in requests.
    
3.  For cached ISR routes in Next.js, ensure preview mode bypasses the ISR cache.
    

After registering onEntryChange and verifying SDK data fetching, make a change in the editor, save, and confirm the preview updates within a few seconds.

### Live Preview ‘Open in New Tab’ Auto-Closes and Reopens in Side Panel

When clicking ‘Open in new tab’ for Live Preview, the new tab automatically closes after a few seconds and the preview reverts to the side panel. Reproducible across browsers and incognito sessions.

**Root Cause**

This is a known platform bug. A lifecycle detection issue causes the newly opened tab to be detected as disconnected from the editor session, triggering an automatic close and fallback to the side panel.

**Resolution**

1.  Contact Contentstack Support and report the issue with browser version, OS, and region.
    
2.  As a workaround: copy the Live Preview URL from the tab before it closes, paste it into a new browser tab, and refresh manually.
    
3.  If the Live Preview outside iframe feature is available, enable it - this uses a different tab-opening mechanism without the auto-close.
    

After the platform fix is deployed, confirm that opening Live Preview in a new tab maintains the editor connection for the full session.

### Live Preview Default Environment Is Stack-Wide, Not Branch-Specific

The Live Preview Default Environment setting is shared across all branches in the stack. Changing the preview environment in one branch (for example, dev) automatically updates it for all other branches (including main), causing ‘requested tracker was created for the main branch’ errors in the dev branch.

**Root Cause**

The Live Preview Default Environment setting is a stack-level configuration, not a branch-level one. There is currently no way to configure different default preview environments per branch within the same stack. When the setting is updated in any branch context, it applies globally to the entire stack.

**Resolution**

This is a current platform limitation. Available workarounds:

1.  Configure the default environment to the one used by the most critical branch (typically main/production) and accept that other branches will need to manually select the correct environment when opening Live Preview.
    
2.  When switching to a branch for editing, manually update the active preview environment in the Live Preview settings before starting the session. Remember to switch it back after.
    
3.  If branch-specific preview environments are critical for the workflow, contact Contentstack Support to submit an enhancement request for per-branch Live Preview environment configuration.
    

After establishing a consistent convention for which environment to set as the default, communicate the manual switching steps to the editorial team to avoid tracker mismatch errors.

### Preview API Returns Partial Data for Non-Localized Referenced Entries

Preview API endpoints (rest-preview or graphql-preview) return partial data for referenced entries that are not localized in the requested locale. Only reference metadata (uid, content\_type\_uid) is returned rather than the full entry data. The same entries return full data via the standard CDN delivery endpoint.

**Root Cause**

The preview endpoint does not automatically apply locale fallback behavior to referenced entries. When a referenced entry has not been localized in the requested locale (for example, en-us), the preview endpoint returns only the stub reference metadata rather than falling back to the master locale. This behavior differs from the CDN delivery endpoint which applies configured locale fallback automatically.

**Resolution**

1.  Add the fallback\_locale parameter explicitly to the GraphQL preview query. For example: allPage(fallback\_locale: true) { … }
    
2.  For REST preview calls, include the fallback\_locale=true query parameter in the preview request URL.
    
3.  Ensure referenced entries that should appear in preview are either (a) localized in the requested locale, or (b) the query includes fallback\_locale to enable automatic fallback to the master locale.
    

After adding the fallback\_locale parameter, re-run the preview query and confirm that non-localized referenced entries return their full data by falling back to the master locale.

### Analytics Dashboard Error for Date Ranges Over 90 Days

The Analytics Dashboard returns an error when a date range exceeding two months is selected.

**Root Cause**

The Analytics Dashboard has a 90-day maximum limit for a single date range query. When the selected range exceeds 90 days, the underlying query fails and the dashboard component throws an error. This is a platform constraint, not a bug.

**Resolution**

1.  Select date ranges of 90 days or less in the Analytics Dashboard.
    
2.  To analyze a period longer than 90 days, split into multiple 90-day queries and combine the data manually or via the Analytics API.
    

After adjusting the date range to 90 days or less, confirm the Analytics Dashboard loads data correctly.

### Analytics Dashboard TB to Byte Conversion Discrepancy

The Analytics Dashboard terabyte values do not match when users manually convert the exported byte values using the binary standard (1 TiB = 1,099,511,627,776 bytes).

**Root Cause**

Contentstack Analytics uses the decimal (SI) standard: 1 TB = 1,000,000,000,000 bytes. The binary standard (1 TiB = 1,099,511,627,776 bytes) produces an apparent discrepancy of approximately 9.95%.

**Resolution**

No action required - the values are correct. Use decimal conversion when comparing Contentstack Analytics figures:

*   1 TB = 1,000 GB = 1,000,000,000,000 bytes (decimal / SI standard)
    
*   1 TiB = 1,024 GiB = 1,099,511,627,776 bytes (binary / IEC standard)
    

Contentstack uses decimal (SI) units. Exported byte values divided by 1,000,000,000,000 will match the terabyte values shown in the dashboard.

<!-- case:00059438 status:draft synced:true bucket:"Custom Extensions, Live Preview & Analytics" -->
### RTE Editing in Nested Fields Throws onFocus TypeError

Rich Text Editor content nested inside Reference or Global fields may throw a console error (Uncaught TypeError: e.onFocus is not a function) in Visual Experience when edits are applied.

**Root Cause**

Contentstack's content type resolution logic did not correctly handle Rich Text Editor fields nested inside Reference or Global field structures within Visual Experience, causing the onFocus handler reference to be undefined and the edit to throw a TypeError.

**Resolution**

1.  Upgrade to Live Preview SDK v4.4.5 or a later version, which contains a permanent fix for this content type resolution issue.

After upgrading, attempt to edit Rich Text Editor content nested inside a Reference or Global field in Visual Experience. If the edit applies without the "e.onFocus is not a function" console error, the issue is resolved. Escalate with the console error output and current SDK version if it persists.

<!-- end:00059438 -->

<!-- case:00058802 status:draft synced:false bucket:"Custom Extensions, Live Preview & Analytics" -->
### Live Preview Not Updating in SSR Applications

Configuring Live Preview in a server-side rendered (SSR) application may fail to reflect entry changes on initial load or when edits are made.

**Root Cause**

The onEntryChange callback was gated behind a livePreviewReady condition and wrapped in a setTimeout, preventing it from firing on initial load. In addition, the SSR implementation did not call stack.livePreviewQuery(req.query) on the server for every request, so the required Live Preview parameters were never explicitly set or cleared.

**Resolution**

1.  Remove any condition (such as checking livePreviewReady) that prevents onEntryChange from firing on initial page load.

2.  Remove the setTimeout wrapper around the Live Preview initialization and callback flow so it executes immediately when the component mounts.

3.  Call stack.livePreviewQuery(req.query) on the server for every request, in both preview and non-preview flows, so Live Preview parameters are set or cleared correctly.

4.  Confirm onEntryChange triggers both on initial load and when edits are made in the entry editor.

After redeploying with these changes, open the entry in edit mode and confirm both the initial page load and subsequent edits reflect in Live Preview. If updates render immediately without requiring a manual refresh, the issue is resolved. Escalate with your SDK version and SSR framework details if it persists.

<!-- end:00058802 -->

## Authentication, Tokens & Access

### API User Session Breaks When Using Two-Factor Authentication

API user sessions fail or break when the account has two-factor authentication (2FA) enabled. CMA calls that require organization-level access return errors or cannot be authenticated.

**Root Cause**

Two-factor authentication adds an interactive step to the login flow that is not well-suited to unattended automation. While the login API does support a 2FA challenge step (tfa\_token), completing this interactively in an automated workflow is not practical, causing session failures for unattended API-driven processes.

**Resolution**

1.  Create a dedicated service account without 2FA enabled specifically for API and automation use.
    
2.  Generate an auth token using that service account's credentials via the user session (login) API.
    
3.  Use this auth token for all CMA calls requiring organization-level access.
    
4.  Restrict the service account's permissions to only the access required for the automation to follow the principle of least privilege.
    

After setting up the service account and generating its auth token, re-run the CMA calls. If they succeed without session breaks, the 2FA conflict is resolved.

### CMA Returns Empty Stack List After SSO Is Enabled

After enabling Single Sign-On (SSO) for the organization, CMA calls to Get All Stacks return an empty array even though stacks exist and are accessible via the UI.

**Root Cause**

For SSO-enabled organizations, the CMA requires the organization\_uid to be included as a header in API requests. Without this header, the API cannot scope the request to the correct organization and returns an empty result.

**Resolution**

1.  Retrieve the organization UID from the Contentstack dashboard (Organization Settings).
    
2.  Add the organization\_uid header to all CMA requests: organization\_uid: <your\_org\_uid>
    
3.  Re-run the Get All Stacks call with the header included and confirm the correct stack list is returned.
    

After adding the organization\_uid header, execute the Get All Stacks API call. If the response contains the expected stacks, the SSO scoping is correctly configured

### SSO Users Cannot Generate Auth Tokens via Basic Credentials in Postman

An SSO-enabled user is unable to generate an auth token using basic username and password credentials in Postman. The login attempt fails and no token is returned.

**Root Cause**

SSO users authenticate through the identity provider (IdP), not through Contentstack's native credential system. Standard credential-based auth token generation via the login API is not available for SSO-only accounts. Additionally, certain Postman configurations (such as proxy settings or certificate handling) can interfere with the SSO authentication flow.

**Resolution**

1.  Use a non-SSO service account (a Contentstack-native user) to generate auth tokens programmatically for API and Postman use.
    
2.  If the SSO user must authenticate, use the Contentstack UI to generate a temporary auth token via the browser-based SSO flow and paste it into Postman manually.
    
3.  Review Postman's proxy and SSL certificate settings to ensure they are not intercepting or modifying the SSO redirect flow.
    

After switching to a non-SSO service account or obtaining a browser-generated token, re-run the Postman request. If authentication succeeds and an auth token is returned, the credential issue is resolved.

### Account Locked Out - Unable to Generate Auth Token

A user is unable to sign in to Contentstack without SSO and therefore cannot generate an auth token. The account is locked and login attempts consistently fail.

**Root Cause**

Repeated failed login attempts trigger an automatic account lock as a security measure. Once locked, the account cannot be accessed until the lock is reset by Contentstack Support.

**Resolution**

1.  Contact Contentstack Support and request an account lock reset for the affected user account.
    
2.  Once Support resets the lock, attempt login again with correct credentials.
    
3.  After successfully logging in, generate the required auth token via the user session (login) API or the Contentstack UI.
    

After the account lock is reset, log in and confirm an auth token can be generated successfully.

### Management Token Will Not Be Deprecated - Clarification on Preview Token

There is concern that the management token will be deprecated and replaced by the Preview token. Teams building automations on the CMA want assurance about its continued availability.

**CLARIFICATION**

The management token is not being deprecated. The Contentstack UI itself relies on the CMA for most of its operations. The Preview token is a separate credential introduced specifically to support Live Preview and Visual Builder features — it is not a replacement for the management token.

For clarity:

*   The management token does not expire unless an explicit expiry date is set at creation.
    
*   The Preview token is used only for Live Preview and Visual Builder integrations.
    
*   Automations, migrations, and integrations built on the CMA can continue operating without changes.
    

Teams can continue building on the CMA with confidence. Any future deprecation notices will be communicated in advance through official Contentstack channels.

### 401 Error on /v3/stacks Using a Stack-Level Management Token

A CMA request to GET /v3/stacks returns a 401 Unauthorized error when authenticated with a stack-level management token.

**Root Cause**

/v3/stacks is an organization-level endpoint. It returns the list of stacks associated with the authenticated user's organization. A stack-level management token is scoped to a single stack and does not have the organization-level authority required by this endpoint.

**Resolution**

1.  Generate a user auth token via the login (user-session) API: POST /v3/user-session with the user's credentials.
    
2.  Include the auth token in the request header as authtoken: <your\_auth\_token>.
    
3.  For SSO-enabled organizations, also include the organization\_uid header.
    
4.  Re-run the GET /v3/stacks request with the auth token and confirm the stack list is returned.
    

After replacing the management token with an auth token, execute the /v3/stacks request. If stacks are returned in the response, the correct authentication method is in use.

### Retrieve Entry Data Without Publishing - Use the CMA

A developer needs to access entry content including drafts and unpublished versions programmatically, without needing to publish entries first.

**Root Cause**

The Content Delivery API (CDA) only serves published content. To access entries in any state - including drafts, unpublished versions, and entries in any workflow stage - the Content Management API (CMA) must be used with a management token.

**Resolution**

1.  Use the CMA entry endpoint: GET /v3/content\_types/{uid}/entries/{entry\_uid} with a management token in the api\_key and authorization (management token) headers.
    
2.  To retrieve all entries regardless of publish state: GET /v3/content\_types/{uid}/entries with the management token.
    
3.  The CMA response includes all entry versions and their current state. Add include\_publish\_details=true to also retrieve publish status information.
    
4.  Ensure the management token has access to the correct branch if the stack uses branches.
    

After switching to the CMA, confirm the response includes unpublished entries and draft content as expected.

### Launch API Returns 403 Forbidden - org_id Required

A Launch API request authenticated with a valid authtoken returns a 403 Forbidden error with the message ‘launch.FORBIDDEN\_RESOURCE’. The authtoken is freshly generated and valid for other CMA calls.

**Root Cause**

The Launch API requires both the authtoken and the org\_id to be passed in the request. Unlike standard CMA endpoints which infer the organization from the authtoken context, the Launch API uses the org\_id to scope access to the correct Launch project. Omitting the org\_id results in a 403 regardless of authtoken validity.

**Resolution**

1.  Add the organization\_uid header (or the x-cs-org-uid header, depending on the endpoint) to the Launch API request alongside the authtoken.
    
2.  The org\_id can be found in the Contentstack dashboard under Account Settings > Organizations, or by calling GET /v3/organizations with the authtoken.
    
3.  Example: curl ‘https://azure-eu-launch-api.contentstack.com/projects’ -H ‘authtoken: <token>’ -H ‘organization\_uid: <org\_id>’
    
4.  Retry the request with the org\_id included and confirm a 200 response is returned.
    

After adding the org\_id to the request, verify the Launch API returns the expected project list or resource without a 403 error.

### Management Token Limit - Requesting an Increase

A stack has reached the maximum number of management tokens permitted under the current plan. Additional tokens are needed for new automation integrations.

**Root Cause**

Management tokens have a plan-level limit that constrains how many can be created per stack. This limit is designed to prevent unbounded token proliferation, which would make access management difficult and increase security surface area.

**Resolution**

1.  Review existing management tokens (Settings > Tokens > Management Tokens) and remove any that are no longer in use. Inactive tokens from old integrations are a common source of limit exhaustion.
    
2.  If additional tokens are genuinely needed beyond the current limit, contact your Customer Success Manager. Increasing the management token limit may have commercial implications depending on the plan.
    
3.  When requesting the increase, provide: the Organization ID, the stack API key, the current token count, and the expected total number of tokens needed.
    

After clearing unused tokens or receiving a limit increase, confirm new management tokens can be created and the desired integration is functional.

### Management Token Cannot Be Scoped to Specific Content Types

A customer wants to restrict a management token to a specific content type or subset of resources to reduce the risk if the token is exposed. They want to limit what the token can do within an automation.

**Root Cause**

Management tokens in Contentstack are stack-level credentials. They can be scoped to branches and environment aliases, but cannot be restricted to specific content types, entries, or fields. Any management token with access to a branch has read and write access to all content types and entries on that branch.

**Resolution**

There is no native way to scope management tokens to specific content types. Available risk reduction strategies:

1.  Create dedicated branches for high-privilege automations and issue management tokens scoped to those branches only. This isolates automation access to a specific branch rather than the full stack.
    
2.  Rotate management tokens frequently and use short-lived tokens where the automation framework supports it.
    
3.  Audit management token usage via the Audit Log to detect unexpected operations.
    
4.  For UI-extension-based operations, use App SDK proxied requests (see Issue 7) which run under the logged-in user’s permissions rather than a standalone management token.
    

After implementing branch-scoped tokens and token rotation practices, review the Audit Log to confirm automated operations are correctly attributed to the expected tokens.

### Error 105 - Organization API Calls Rejected With Strict SSO

An API call to an organization-level endpoint returns Error 105 even though the authtoken is valid for stack-level calls. The organization has Strict SSO enabled.

**Root Cause**

With Strict SSO enabled, Contentstack rejects standard email/password authtokens for organization-level API calls. The SSO enforcement requires all organization-level requests to be authenticated via the SSO flow. Service accounts that use password-based login cannot generate authtokens that pass organization-level validation under Strict SSO.

**Resolution**

1.  Enable the User Email Whitelist feature for the service account email addresses that need to make organization-level API calls. This feature allows specific accounts to use password-based login (via the CMA Login API) while still having their authtokens accepted by organization-level APIs, even when Strict SSO is enabled.
    
2.  To add an email to the whitelist, contact Contentstack Support with the Organization ID and the service account email addresses to whitelist.
    
3.  After whitelisting, the service account can authenticate via POST /v3/user-session (CMA Login API) and use the returned authtoken for organization-level calls.
    

After whitelisting the service account email, confirm that organization-level API calls return 200 responses rather than Error 105.

### CMA Workflows API Returns Auth Error - Postman Authorization Header Conflict

A CMA API call to retrieve workflows returns an authentication error similar to ‘you cannot do that unless you are logged in’, even though the api\_key and management token are correct. The same call works correctly when run via cURL.

**Root Cause**

The issue is caused by Postman’s Authorization tab. When Postman’s Authorization is set to any type other than ‘No Auth’, Postman generates and injects its own Authorization header into the request. This injected header overwrites or conflicts with the manual authorization header (containing the management token) that was added in the Headers tab. The result is that the management token is either duplicated or replaced by an empty or invalid value.

**Resolution**

1.  In Postman, navigate to the Authorization tab for the request and set the type to No Auth.
    
2.  Add the management token manually in the Headers tab: key = authorization, value = {management\_token}.
    
3.  Also add the api\_key header: key = api\_key, value = {stack\_api\_key}.
    
4.  Re-send the request and confirm the workflows are returned correctly.
    

After setting Postman’s Authorization to No Auth and adding headers manually, confirm the CMA call returns the expected workflow list without authentication errors.

### App SDK for CMA-Style Operations in UI Extensions

A developer building a Contentstack UI extension or marketplace app needs to perform CMA-style operations (such as asset search or entry lookups) without embedding a management token in client-side code.

**Root Cause**

Embedding management tokens in client-side extensions is a security risk - the token would be visible to any user inspecting the extension’s code. The App SDK provides a secure, proxied method for extensions to make CMA-style requests that execute under the logged-in user’s permissions and session, without exposing tokens.

**Resolution**

1.  Use the App SDK’s window.opener.postMessage or the stack.ContentType().Entry() SDK methods to make requests. These are proxied through the Contentstack App SDK, which uses the logged-in user’s session and permissions.
    
2.  For asset search: use the App SDK’s stack.Asset().Query().where() methods to search assets under the logged-in user’s access.
    
3.  For entry lookups: use stack.ContentType(uid).Entry(entryUid).fetch() within the extension to retrieve entry data without a management token.
    
4.  Refer to the Contentstack App SDK documentation for the full list of supported CMA-proxied operations available to UI extensions and marketplace apps.
    

After implementing App SDK proxied requests, confirm that CMA-style operations work without a management token being embedded in the extension code.

### Global Field Not Updating via CMA - Missing https:// in Base URL

CMA requests to update a global field appear to succeed (returning a 200 response) but the global field does not change in Contentstack. The field values remain at their previous state after the request.

**Root Cause**

The request was being made to a non-HTTPS base URL (for example, http:// instead of https://). Without the HTTPS protocol, the request may not reach the correct CMA endpoint. In some configurations, the http:// request silently succeeds at the network level but does not reach the CMA handler, resulting in a no-op.

**Resolution**

1.  Verify the base URL in the API request uses https://:
    
2.  Correct: https://api.contentstack.io/v3/global\_fields/{uid}
    
3.  Incorrect: http://api.contentstack.io/v3/global\_fields/{uid} or api.contentstack.io/v3/global\_fields/{uid}
    
4.  Update all CMA requests in the integration to use https:// and retry the global field update.
    

After correcting the base URL to https://, confirm the PUT request updates the global field and the change is reflected in the Contentstack CMS UI.

### Finding Users by user_ID - Users API

An administrator needs to look up the name or email of a user given only their user UID (for example, from an entry’s created\_by or updated\_by field). The CMS UI does not provide a UID-based user search.

**Root Cause**

The Contentstack CMS UI does not support searching users by UID. User UID to identity mapping must be done programmatically via the CMA Users API.

**Resolution**

1.  Use the CMA Users API to resolve a user UID to user details: GET /v3/users/{user\_uid} - requires a management token or authtoken.
    
2.  For bulk lookup of multiple user UIDs, iterate over the list and call the endpoint for each UID.
    
3.  Alternatively, fetch all users in the organization: GET /v3/organizations/{org\_uid}/users - this returns a full list of users with their UIDs, names, and email addresses, which can be used to build a local lookup map.
    

After building the UID-to-user lookup map, confirm that all relevant user UIDs from entry metadata can be resolved to names or email addresses.

### Management Tokens Cannot Perform Workflow Transitions With Role-Based Restrictions

An automated background process using a management token needs to publish content while respecting the workflow and publish restrictions configured for specific user roles. Management token-based publishes bypass these restrictions and go through regardless of the workflow state.

**Root Cause**

Management tokens are stack-level credentials that do not carry user identity or role context. Workflow stage transitions and publish rule restrictions are enforced based on the role and identity of the user performing the action. Because management tokens have no user identity, the system cannot evaluate which workflow stages or publish restrictions apply - resulting in the token either bypassing restrictions or returning a 141 Access Denied error when strict workflow enforcement is applied.

**Resolution**

1.  If workflow enforcement must be respected by the automation, use an authtoken generated by logging in as a specific service account user (via POST /v3/user-session). Assign that service account the appropriate role in Contentstack so workflow stage restrictions apply to it.
    
2.  For organizations with Strict SSO, use the User Email Whitelist feature (see Authentication Issue 5) to allow the service account to generate authtokens while SSO is active.
    
3.  If the automation must use a management token and the 141 error is being triggered: confirm whether the workflow stage the entry is in allows the target publish action. Management tokens can trigger publishes but only when the entry’s current workflow stage permits it.
    

After switching to a role-assigned service account authtoken, verify that the automation respects workflow stage transitions and publish rule restrictions as intended.

### Restricting Users from Publishing to a Production Environment

An administrator wants to prevent certain users from publishing to the production environment. A custom role has been created but users are still seeing incorrect environments or are able to bypass the restriction.

**Root Cause**

Environment publishing restrictions are enforced through Publish Rules, not directly through custom role permissions. A common confusion is attempting to restrict production publishing via custom role environment access settings, rather than configuring a Publish Rule that requires approval before publishing to the production environment.

**Resolution**

1.  Navigate to Settings > Workflows and create or update a Publish Rule that governs the production environment.
    
2.  In the Publish Rule, set ‘Allowed Roles’ or ‘Approval Required’ conditions that restrict direct publishing to production. For example, require approval from a designated senior editor or admin role.
    
3.  Assign the custom role to users who should not publish directly to production. These users will be subject to the Publish Rule restrictions.
    
4.  Test by logging in as a user with the custom role and attempting to publish to production - the Publish Rule should block direct publish and require approval.
    

After configuring the Publish Rule for the production environment, verify that restricted users cannot bypass it and that the approval flow works as expected for production publishes.

### Delivery Token Exposed in Frontend Application Bundle - Rotate Immediately

A delivery token is discovered to be exposed in the frontend application bundle - visible to anyone who inspects the application’s JavaScript code. This is a security risk.

**Root Cause**

Delivery tokens embedded in frontend code or hardcoded in client-side JavaScript bundles are publicly accessible to any user who inspects the application source. While delivery tokens are designed for read-only content delivery (not write operations), an exposed token allows unauthorized parties to access all published content in the stack, potentially including content not yet published publicly.

**Resolution**

1.  Rotate the exposed delivery token immediately: navigate to Settings > Tokens, locate the compromised token, and regenerate or delete it. Create a new token to replace it.
    
2.  Update the application configuration to use the new token.
    
3.  For frontend applications, avoid embedding delivery tokens directly in client-side code. Instead, proxy delivery API requests through a server-side endpoint that adds the token server-side before forwarding to Contentstack.
    
4.  For server-side rendering (SSR) or static site generation (SSG) frameworks, ensure the token is stored in server-side environment variables and never bundled into the client-side output.
    

After rotating the token and updating the application, confirm that the old token no longer returns data (it should return a 401 or 404) and that the new token functions correctly.

### Role Permissions Not Taking Effect - Permission Cache Desync

A user’s role and permissions are correctly configured but actions they should be allowed to perform - such as editing entries or accessing certain sections - are still blocked. The UI behaves as if an older permission set is active.

**Root Cause**

User role and permission data is cached in Redis for performance. If a role update does not propagate correctly to the cache, the old permission set continues to govern the user’s actions. This can occur after role changes, multi-role assignment updates, or SSO sync events.

**Resolution**

1.  Ask an Organization Owner or Admin to temporarily change the affected user’s role and then revert it. This triggers a cache refresh.
    
2.  Alternatively, remove the user from the stack and re-add them, which forces a full permission state rebuild.
    
3.  Ask the user to log out and log back in after the role change.
    

After the role toggle or re-add, ask the user to attempt the previously blocked action. If it succeeds, the permission cache has been refreshed.

### ‘Insufficient Permission’ Error When Publishing After Role Assignment

A user with a Developer role and access to all environments receives an ‘insufficient permission’ error when attempting to publish entries. The role appears correctly configured in the dashboard.

**Root Cause**

This is a permission mapping desync. When a user’s role is changed or re-assigned, the permission mapping may not immediately take effect. Removing and re-adding the user to the stack forces the permission mapping to rebuild correctly.

**Resolution**

1.  Ask the stack Owner or Admin to remove the affected user from the stack.
    
2.  Re-add the user to the stack with the same role.
    
3.  Ask the user to log out and log back in.
    
4.  Test publishing to confirm the error is resolved.
    

After removing and re-adding the user, confirm they can publish entries without an insufficient permission error.

### Hiding Content Models from the Sidebar for a Specific Role

A customer wants to hide the Content Models section from the left sidebar for users assigned the Developer role, without changing their other permissions.

**Root Cause**

The Developer role is a default system role in Contentstack. Default system roles cannot be modified to restrict sidebar visibility. Only custom roles support granular permission configuration.

**Resolution**

1.  Create a new custom role with the same permissions as the Developer role.
    
2.  In the custom role settings, remove or restrict access to Content Models.
    
3.  Assign users who should not see Content Models to the new custom role instead of the default Developer role.
    

After assigning the custom role, confirm that the Content Models section is no longer visible in the sidebar for those users.

### Restricting Specific Fields for All Users Using Field-Level Permissions

An administrator wants to restrict certain fields so that all users - regardless of role - cannot edit them. Field-level restrictions appear to require role-by-role configuration.

**Root Cause**

Field-level access restrictions in Contentstack are configured within custom roles under Roles and Permissions. Fields can be restricted globally across all content types within a role, or per content type. Each role that should have the restriction must be configured individually.

**Resolution**

1.  Navigate to Settings > Roles and Permissions and select the role to be restricted.
    
2.  Under the Content Types section, locate the field to restrict and configure its permission as read-only or hidden.
    
3.  To apply the restriction across all content types, use the global field restriction setting rather than configuring each content type individually.
    
4.  Repeat for each role that should have the restriction applied.
    

After saving the role configuration, log in as a user with the restricted role and confirm the targeted fields are not editable.

### Assigning Multiple Roles with Different Language Permissions

A team wants to give content managers access to specific locales only - for example, one user manages English, another manages German. Multiple roles with different language permissions need to be assigned to users.

**Root Cause**

Contentstack supports language-specific permissions within custom roles. Users can be assigned multiple roles simultaneously, and language permissions from non-conflicting roles combine. If roles have overlapping permission scopes, the more permissive role may override the more restrictive one.

**Resolution**

1.  Create a custom role for each language group (for example, a German Content Manager role with Create, Read, Update, and Delete access scoped to de-de).
    
2.  Assign users the appropriate language-scoped role.
    
3.  If a user needs access to multiple languages, assign multiple language-specific roles to them.
    
4.  Monitor for overriding behavior when roles share similar permission scopes - the more permissive role will take precedence.
    

After assigning language-specific roles, confirm users can only access and edit entries in their permitted locales.

### Stack Owner Cannot Publish to Production - Not Added as Approver

A stack owner is unable to publish entries to the production environment. The publish action is blocked despite their elevated role.

**Root Cause**

A publish rule configured for the production environment restricts publishing approvals to a specific set of users (for example, Administrators only). If the stack owner is not explicitly listed as an approver in the publish rule, they are blocked from publishing - even as a stack owner.

**Resolution**

1.  Navigate to Settings > Workflows and locate the publish rule governing the production environment.
    
2.  Add the affected user (stack owner) to the list of approvers in the rule.
    
3.  Save the updated publish rule.
    
4.  Test publishing again to confirm access is restored.
    

After updating the publish rule, confirm the stack owner can publish entries to production without being blocked.

### Custom Role Editors Cannot See Newly Created Taxonomies

Editors with a custom role that grants full access to specific content types can see existing taxonomies but cannot see newly created ones. Admin users see all taxonomies.

**Root Cause**

Taxonomy visibility for custom roles requires explicit permission grants for each taxonomy. When a new taxonomy is created, it is not automatically added to the permissions of existing custom roles. Each new taxonomy must be explicitly permitted in the role settings.

**Resolution**

1.  Navigate to Settings > Roles and Permissions and select the affected custom role.
    
2.  Under the Taxonomies section, add explicit access to the newly created taxonomy.
    
3.  Save the updated role.
    
4.  Ask editors to log out and back in for the permission change to take effect.
    

After updating the role, confirm that editors can see and interact with the new taxonomy.

### Restricted Content Type Still Appears When Creating New Entries

A user assigned a custom role that should not allow creating entries for a specific content type (for example, ‘Ad’) still sees that content type as an option when creating new entries.

**Root Cause**

The role has a blanket Create permission enabled under ‘All Entries of Content Types’, which overrides the individual content type restriction. Contentstack evaluates the broadest matching permission, so the general permission takes precedence over the per-type exclusion.

**Resolution**

1.  Navigate to the role settings and remove the Create permission from ‘All Entries of Content Types’.
    
2.  Explicitly add Create permissions only for the individual content types that should be accessible.
    
3.  Ensure the excluded content type (for example, ‘Ad’) is not included in the individual list.
    
4.  Save and test by logging in as the affected user.
    

After updating the role, confirm that the excluded content type no longer appears as an option when the user creates new entries.

### Deleting a Role Only Removes That Role’s Permissions

An administrator is unsure whether deleting a role will affect all permissions for users assigned that role, including permissions from their other roles.

**Root Cause**

In Contentstack, deleting a role removes only the permissions associated with that specific role from the users it was assigned to. Other roles assigned to the same users remain intact and their permissions are unaffected.

**Resolution**

When deleting a role, the warning message refers only to the removal of that role’s permissions. Users who have additional roles will retain all permissions from their remaining roles. Review users assigned to the role before deletion to confirm they will retain the necessary access through their other roles.

### Field-Level Permissions Inside Modular Blocks Are Not Supported

A customer wants to restrict access to specific fields nested inside a modular block using Roles and Permissions. The expected granular control does not appear to be available.

**Root Cause**

Field-level permission control for fields nested inside modular blocks is not supported in the current version of Contentstack. Permissions can be configured at the content type and top-level field levels, but not for individual fields within modular block types.

**Resolution**

As an alternative, use content type-level permissions to restrict access to entire content types that contain the sensitive modular block fields. Contact Contentstack Support to submit an enhancement request if granular modular block field-level permissions are a business requirement.

### Reference Field Not Visible Despite Being Enabled in Field-Level Permissions

A reference field is enabled in the role’s field-level permissions but does not appear for users with that role. The field is visible to Admin users.

**Root Cause**

A reference field that points to multiple content types requires the role to have access to each of the referenced content types. If a user does not have read access to one or more of the content types referenced by the field, the field will not be visible.

**Resolution**

1.  Review which content types are referenced by the field.
    
2.  In the role settings, grant Read (or higher) access to all content types referenced by the field.
    
3.  Save the updated role and confirm with the user that the field is now visible.
    

After updating the role to include access to all referenced content types, confirm the reference field appears correctly for users with that role.

### Read-Only Role That Can View Publish Status Without Publishing

A team needs a role that provides read-only access to stack content but still allows users to view which environments an entry is published to - without any ability to publish or modify entries.

**Root Cause**

Publish status visibility is tied to environment access within the role. Granting environment access at the Read level shows publish status without enabling publish or unpublish actions.

**Resolution**

1.  Create or edit the read-only role in Settings > Roles and Permissions.
    
2.  Under Entries and Assets, grant Read permissions only.
    
3.  Assign the relevant environments to the role so publish status is visible for those environments.
    
4.  Do not enable any Publish or Unpublish permissions.
    

After configuring the role, confirm that users can view the publish status (environment badges) on entries but cannot initiate any publish or unpublish actions.

### Authorization Errors When Uploading or Publishing Assets for Content Manager Role

Team members with the Content Manager or Content Editor roles receive authorization errors when uploading or publishing assets, while users with the Developer role can perform the same actions without issues.

**Root Cause**

The Content Manager and Content Editor roles are missing the Upload Assets and/or Publish Assets permissions, or do not have permission grants for the relevant environments.

**Resolution**

1.  Navigate to Settings > Roles and Permissions and select the Content Manager or Content Editor role.
    
2.  Enable the Upload Assets permission under the Assets section.
    
3.  Enable the Publish Assets permission for the required environments.
    
4.  Save the updated role and ask affected users to retry the action.
    

After updating the role permissions, confirm affected users can upload and publish assets without authorization errors.

### Workflow Settings Not Visible to Org Owner - Must Be Stack Owner

An Org Owner cannot see or access workflow settings within a specific stack, even with full organization access.

**Root Cause**

In Contentstack, certain configuration areas - including Workflow settings - are only visible to users who hold the Stack Owner role for that specific stack. Org Owner access alone is insufficient for stack-level settings. Each role operates at a different scope.

**Resolution**

1.  Have the current Stack Owner assign the requesting user as a Stack Owner for the specific stack.
    
2.  Once assigned as Stack Owner, the user will have full visibility into and control over Workflow settings.
    

After the user is assigned Stack Owner, navigate to Settings > Workflows in the affected stack and confirm the settings section is now visible.

### Taxonomy Tagging Now Requires Explicit Taxonomy Permissions

Users who previously could tag entries with taxonomy terms now encounter errors or cannot see taxonomy terms after a platform update.

**Root Cause**

A platform update changed the permission model. Previously, users with entry edit access could tag taxonomy terms without separate taxonomy permissions. Now explicit taxonomy permissions are required.

**Resolution**

1.  Navigate to Settings > Roles and Permissions and open the custom role configuration.
    
2.  Under Taxonomies, add the specific taxonomies the role should be able to apply to entries. Grant ‘Read’ access to allow tagging without full management permissions.
    
3.  Avoid granting ‘All Taxonomies’ with full permissions unless the role should also create and modify taxonomy structures.
    
4.  Save the role and ask affected users to log out and back in.
    

After adding taxonomy Read permissions, confirm affected users can view and apply taxonomy terms without permission errors.

### ‘Unlocalize’ Button Not Visible for a Specific Locale

An editor cannot see the ‘Unlocalize’ button for a specific localized entry. The option is visible for other locales and other users.

**Root Cause**

The visibility of the Unlocalize button is tied to the ‘Delete Entry’ permission. The unlocalize operation removes the locale-specific version, which is functionally a deletion. Without Delete Entry permission, the button is hidden.

**Resolution**

1.  Navigate to Settings > Roles and Permissions and review the custom role assigned to the affected user.
    
2.  Enable the Delete Entry permission for the relevant content type in the role.
    
3.  If enabling Delete Entry globally is inappropriate, create a separate role with Delete permission scoped only to the relevant content type and assign it alongside the existing role.
    

After adding the Delete Entry permission, confirm the Unlocalize button appears for the affected user.

### Referenced Content Type Not Accessible - Role Missing Access

Client users encounter: ‘The referenced content type(s) do not exist or are not accessible’ when viewing a specific entry. The entry works for users with higher permissions.

**Root Cause**

The user’s role does not have Read access to the referenced content type. Contentstack enforces content type access at the role level.

**Resolution**

1.  Navigate to Settings > Roles and Permissions and open the affected role.
    
2.  Under Content Types, add the inaccessible content type and grant at least Read access.
    
3.  For read-only reference resolution (no edits needed), grant Read-only to allow the reference to resolve without permitting modifications.
    
4.  Save the role and ask affected users to log out and back in.
    

After updating the role, reload the affected entry and confirm the referenced content type resolves without the access error.

### ‘UID Should Be Unique’ When Creating a Child Taxonomy Term

Creating a child taxonomy term returns a ‘UID should be unique’ error even though there are no visible child terms with that UID under the parent.

**Root Cause**

Taxonomy term UIDs must be unique across the entire taxonomy - not just within the same parent level. If a term with the same UID exists anywhere else in the taxonomy tree, a new term cannot be created with that UID.

**Resolution**

1.  Search the entire taxonomy for any existing term with the same UID: GET /v3/taxonomies/{taxonomy\_uid}/terms via the CMA.
    
2.  If the conflicting term is unnecessary, delete it before creating the new term.
    
3.  If both terms need to exist, choose a different UID for the new term (for example, append the parent path to make it unique).
    

After resolving the UID conflict, retry creating the child term and confirm it is created successfully under the intended parent.

### Accidentally Deleted Taxonomy - Restore from Trash Within 14 Days

A user accidentally deleted a required taxonomy. The taxonomy is no longer visible but is needed for active content.

**Root Cause**

Deleted taxonomies are retained in the Trash for up to 14 days before permanent deletion. Within this window, restoration is possible.

**Resolution**

1.  Navigate to the Trash section in Contentstack and search for the deleted taxonomy.
    
2.  Restore the taxonomy from Trash within the 14-day retention window.
    
3.  If the 14-day window has passed, contact Contentstack Support immediately to escalate for a backend restore attempt.
    
4.  After restoring, verify that entries previously tagged with the taxonomy’s terms still show correct associations.
    

After the taxonomy is restored, open a test entry and confirm taxonomy terms are correctly assigned and visible.

### Taxonomy Import to New Stack Silently Fails - Missing Locales and Environments

Exporting taxonomies from one stack and importing into another appears to succeed but no taxonomy data appears in the target stack.

**Root Cause**

Taxonomies have dependencies on locales and environments. If the target stack does not have the same locales and environments as the source stack, the taxonomy import silently fails to associate correctly.

**Resolution**

1.  Before importing, ensure the target stack has the same locales as the source: Settings > Languages.
    
2.  Ensure the target stack has the required environments configured: Settings > Environments.
    
3.  After adding the required locales and environments, re-attempt the taxonomy import.
    
4.  If the import still silently fails, contact Contentstack Support with the import file and target stack details.
    

After configuring required locales and environments, import the taxonomy and verify terms and hierarchy appear correctly.

### Taxonomy-Based Role Restriction Blocks Save Without a Clear UI Error

Users with a custom role that has taxonomy-based restrictions are blocked from saving entries that include restricted taxonomy terms. The backend correctly rejects the save, but the UI does not clearly communicate which taxonomy term is restricted or why the save failed.

**Root Cause**

Contentstack correctly prevents users from saving entries with taxonomy terms they are not authorized to apply. However, the error surfaced to the user in the UI was generic - not clearly indicating which taxonomy term caused the save failure. An engineering fix has been deployed that updates the UI to better reflect restricted taxonomy terms (by displaying them differently in the selection interface rather than allowing selection and failing on save).

**Resolution**

A platform fix has been deployed to improve the UI experience for taxonomy-based restrictions. Restricted terms are now surfaced differently in the entry editor so editors know before attempting to save.

1.  If editors are still encountering unclear save failures related to taxonomy permissions, review the custom role’s taxonomy access settings and confirm the role has Read access only to the permitted taxonomies.
    
2.  After the fix, verify that attempting to apply a restricted taxonomy term either (a) prevents selection entirely, or (b) shows a clear error on save indicating which term is restricted and why.
    

After the fix deployment, open an entry as a role-restricted user and confirm that restricted taxonomy terms are visually identifiable and that save failures show actionable error messages.

### Taxonomy Term Deletion Removes Term from All Entries Silently - No Webhook or Audit Event

When a taxonomy term is deleted from Contentstack, it is automatically removed from all entries that had that term assigned. No webhook event is triggered for those entries, and no audit log record captures the previous term associations. It is impossible to identify which entries were affected.

**Root Cause**

This is expected platform behavior. Taxonomy term deletion cascades to remove the term from all entry associations immediately. Contentstack does not emit per-entry webhooks or audit events for the cascade removal - only the taxonomy deletion event itself may be logged. This is a known limitation of the taxonomy deletion lifecycle.

**Resolution**

This is a documented platform limitation. To mitigate the impact:

1.  Before deleting a taxonomy term, use the CMA to identify all entries currently associated with that term: GET /v3/content\_types/{uid}/entries?query={“taxonomies.term\_uid”:“{term\_uid}”} - run this query for each content type to build a complete list.
    
2.  Save the list of affected entries before deletion so you know which entries need review after the term is removed.
    
3.  Consider using the Automate Hub to set up a pre-deletion workflow that captures term associations before allowing deletion.
    
4.  Contact Contentstack Support to submit an enhancement request for webhook events on taxonomy term cascade removals.
    

After documenting affected entries before deletion, confirm the taxonomy term is removed from all expected entries via CDA query and that no unintended entries were affected.

### Taxonomy Field Display Order in Entry Editor Doesn’t Match Selection Order

After selecting taxonomy terms in a specific order in the entry editor, the displayed order of terms in the taxonomy field does not match the order in which they were selected. The Content Delivery API correctly captures the selection order, but the UI display is inconsistent.

**Root Cause**

This is a UI display bug. The entry editor’s taxonomy field component renders terms in a different order than the sequence in which they were selected. The underlying data is stored and returned by the CDA in the correct selection order - the discrepancy is cosmetic and limited to the editor display.

**Resolution**

An engineering fix has been deployed to correct the taxonomy term display order in the entry editor. The editor should now reflect the selection order consistent with the CDA output.

1.  If the display order is still inconsistent after the fix deployment, contact Contentstack Support with the content type UID and a screen recording showing the ordering discrepancy.
    
2.  In the meantime, verify the correct order via the CDA and trust the API output for downstream rendering - the data is correct even if the editor display was inconsistent.
    

After the fix deployment, select taxonomy terms in a specific order and confirm the entry editor displays them in the same sequence as the CDA returns them.

<!-- case:00050794 status:draft synced:false bucket:"Authentication, Tokens & Access" -->
### Roles Created via CMA Don't Display Correctly in the UI

Creating a role through the Content Management API may result in the role details failing to load in the Contentstack UI, even though the role was created successfully.

**Root Cause**

The request payload for roles created programmatically was missing the sub_acl key inside the content_types module, which caused the UI to fail when rendering the role's permission details.

**Resolution**

1.  Confirm the role was created via the CMA and that its details fail to load or render in the Contentstack UI.

2.  Retry loading the role details. A platform fix for the missing sub_acl key has been deployed and resolves this for both new and previously created roles.

3.  Contact Contentstack Support with the role UID and stack API key if the role details still fail to load after retrying.

After retrying, open the affected role in the Contentstack UI and confirm the Content Type Management permissions display correctly. If the role details load as expected, the issue is resolved. Escalate with the role UID and stack API key if it persists.

<!-- end:00050794 -->

## CMA Rate Limiting & 429 Errors

### 429 Errors in Launch Logs Caused by Incorrect API_HOST Variable

A Contentstack Launch-hosted application generates 429 errors in its logs. The application is not intentionally making CMA calls, yet the errors point to CMA rate limit exhaustion.

**Root Cause**

The application's environment variable API\_HOST is set to api.contentstack.io, which is the CMA endpoint, instead of the CDA endpoint (cdn.contentstack.io). As a result, what should be CDA delivery calls are incorrectly routed to the CMA, exhausting the CMA rate limit and returning 429 errors.

**Resolution**

1.  Review the application's environment variables in the Contentstack Launch configuration.
    
2.  Locate the API\_HOST variable and correct its value from api.contentstack.io to cdn.contentstack.io (or the appropriate regional CDA endpoint).
    
3.  Redeploy the application with the corrected environment variable.
    
4.  Monitor the Launch logs after redeployment to confirm 429 errors no longer appear.
    

After correcting the API\_HOST variable and redeploying, check the application logs. If CMA 429 errors no longer occur, the requests are now correctly routed to the CDA endpoint.

### 429 Errors During Bulk Delete and Bulk Publish Despite Adding Delays

Bulk delete and bulk publish CMA operations return 429 errors even though the requests stay within the 10-UID-per-request limit and a 1-second delay is added between requests.

**Root Cause**

The CMA rate limit is enforced on call frequency, not on the number of UIDs per request. A 1-second delay between requests may still produce more than 20 POST/PUT/DELETE calls per second when requests are sent from multiple threads or processes simultaneously. The limit for CMA POST/PUT/DELETE operations is 20 requests per second.

**Resolution**

1.  Increase the delay between bulk operation requests to ensure the total call rate stays below 20 requests per second.
    
2.  If multiple threads or parallel processes are sending bulk requests, implement a shared throttle across all processes, not just per-thread delays.
    
3.  Use exponential backoff: when a 429 is received, wait and retry rather than failing the job immediately.
    
4.  Process bulk operations sequentially rather than in parallel where possible.
    

After increasing the delay and implementing throttling, re-run the bulk operation. If 429 errors no longer occur, the request rate is within the CMA limit.

### CMA Rate Limit Increase Request Process

A customer is receiving 429 errors on CMA requests and wants to increase the CMA rate limit. It is unclear whether this can be done via a support ticket.

**Root Cause**

CMA rate limit increases are commercial decisions that involve changes to the organization's plan. Support cannot unilaterally increase CMA rate limits, these requests must be handled by the Customer Success Manager (CSM) who manages the account's commercial agreement.

**Resolution**

1.  Contact your assigned Customer Success Manager and request a CMA rate limit increase, specifying the current limit and the target limit needed.
    
2.  While awaiting the increase, implement the following best practices to reduce CMA usage:
    
    *   Reduce concurrent requests; avoid sending multiple CMA calls simultaneously from the same process.
        
    *   Add delays between requests in bulk or automated workflows.
        
    *   Cache CMA responses where the data does not change frequently.
        
    *   Use the SDK's built-in retry logic or implement custom retry-with-backoff.
        
3.  Once the CSM confirms the limit has been increased, verify using GET /v3/organizations/<org\_uid>/plan.
    

After the CSM-approved increase is applied, re-run the previously failing operations. If 429 errors no longer occur at the previous volume, the increased limit is active.

### Investigating and Resolving CMA 429 Error Spikes

A spike in 429 errors is observed on a CMA-heavy stack. The errors appear in bursts and may be triggered by a specific automated workflow or integration.

**Root Cause**

429 spikes on CMA are typically caused by unthrottled automated processes, integrations, or SDK-based migrations hitting the CMA simultaneously or in rapid succession. Common triggers include bulk content migrations, automated publish pipelines, third-party integrations without backoff logic, and concurrent CLI or SDK operations.

**Resolution**

1.  Contact Contentstack Support and request CMA error logs for the affected time window and stack. Logs will identify which endpoints and operations are generating the most requests.
    
2.  Review all active integrations, scheduled jobs, and CLI operations that interact with the CMA and identify which are running without throttling.
    
3.  Add per-operation rate limiting, delays, and retry-with-backoff to the identified workflows.
    
4.  Stagger automated jobs so they do not overlap with peak editorial usage periods.
    

After applying throttling to the identified workflows, monitor CMA usage during the next scheduled run. If 429 spikes do not recur at the same magnitude, the workflows are operating within rate limits.

### 429 Too Many Requests Errors from GraphQL Endpoin

GraphQL requests return HTTP 429 Too Many Requests errors, particularly during release events or periods of high traffic. The errors occur in bursts and affect production API performance.

**Root Cause**

Contentstack applies rate limits at the organization or API key level - not per IP address or per content type. Rate limits are triggered when the total number of requests to a given API endpoint exceeds the allowed threshold. The GraphQL API’s platform default for origin (uncached) requests is 80 requests per second per organization; CDN-cached requests are not subject to this limit. The 200 RPS figure below reflects this customer’s specific contracted threshold, not the platform default - reconcile with the 80 RPS default before publishing if the intent is to describe out-of-the-box behavior. Bulk publish events, release deployments, or simultaneous multi-client queries commonly cause request spikes that exceed the applicable limit.

**Resolution**

1.  Review the application’s request patterns and identify spikes above the applicable rate limit (80 RPS by default, or a higher contracted threshold such as 200 RPS if one has been negotiated) during release or publish events.
    
2.  Implement request throttling or exponential backoff in the client application to smooth out traffic spikes.
    
3.  Stagger bulk publish or release operations to distribute requests over a longer time window.
    
4.  Implement a caching layer to reduce repeated identical GraphQL requests hitting the origin.
    
5.  If the rate limit is consistently insufficient for production workloads, contact Contentstack Support to discuss limit adjustments.
    

After implementing throttling and staggered operations, monitor the API logs during the next release event. If 429 errors no longer appear at the same frequency, the rate of requests has been successfully reduced.

### CMA Rate Limit Is Org-Level, Not Per Stack

A team is hitting CMA rate limits but the stack they are working on appears to have low traffic. They are unsure whether rate limits apply per stack or across the entire organization.

**Root Cause**

CMA rate limits in Contentstack are applied at the organization level and are shared across all stacks within the organization. A single heavily-used stack consuming most of the rate limit budget will cause other stacks in the same organization to also receive 429 errors, even if those stacks have low individual activity.

**Resolution**

1.  Monitor CMA traffic across all stacks in the organization, not just the stack experiencing 429 errors.
    
2.  Identify which stacks or integrations are consuming the most CMA requests by reviewing the Analytics dashboard or requesting CMA logs from Contentstack Support.
    
3.  Implement exponential backoff and retry logic across all CMA integrations to handle 429 responses gracefully.
    
4.  Stagger high-volume CMA operations (bulk migrations, automated publishing scripts) to different time windows so they do not compete with editorial activity.
    
5.  If the organization’s CMA rate limit is consistently insufficient for the workload, contact the Customer Success Manager to discuss a rate limit increase.
    

After identifying the high-consumption stacks and staggering their operations, monitor for 429 reduction across the organization.

### Understanding CMA Rate Limit Headers - Soft Limit vs Burst Threshold

The CMA usage log shows 429 errors appearing in spikes even though average usage appears below the confirmed rate limit. The rate limit response header (X-RateLimit-Limit) shows a value of 10 RPS, but the actual agreed limit is higher.

**Root Cause**

The CMA enforces two rate limit values: a soft limit (10 RPS for most CMA GET operations) reflected in the X-RateLimit-Limit response header, and an internal burst threshold (for example, 23 RPS) that is not exposed in headers. Requests are throttled when they exceed the soft limit in a sustained pattern. Short-duration bursts may be absorbed by the burst threshold, but sustained traffic above the soft limit consistently triggers 429 errors.

**Resolution**

1.  Design automation and integration logic to target the X-RateLimit-Limit header value (the soft limit) as the steady-state rate, not the burst threshold.
    
2.  Implement request spacing: rather than firing requests as fast as possible, introduce a configurable delay between requests to stay below the soft limit.
    
3.  On receiving a 429, read the Retry-After header (if present) and wait the specified duration before retrying.
    
4.  For spike prevention during deployments, add a rate-limiting wrapper to all CMA call sites that enforces the soft limit as a ceiling.
    
5.  To check the actual rate limit configuration for the organization directly: GET /v3/organizations/{org\_uid}/plan (requires auth token).
    

After implementing request spacing and retry logic based on the soft limit, monitor the 429 spike frequency during the next high-traffic period and confirm spikes are reduced. Rate limit header values: x-ratelimit-limit shows the soft limit; x-ratelimit-remaining shows requests remaining in the current window.

### 429 Spike Caused by Cache Purge and Traffic Switch to Contentstack Backend

A sudden spike in HTTP 429 errors occurs after a CDN cache purge or a traffic switch that routes requests directly to the Contentstack backend. Request rates reach several hundred per second, exhausting the organization rate limit.

**Root Cause**

When a CDN cache is purged or traffic is switched to bypass the CDN, all requests that were previously served from cache now hit the Contentstack origin simultaneously. This cache stampede drives traffic well above the organization rate limit. Malformed asset URLs (incorrect query parameters) in the traffic also contribute - each unique URL variant creates a separate cache miss, multiplying origin-bound requests.

**Resolution**

1.  After a cache purge, implement a staggered cache warm-up instead of allowing all traffic to hit the origin simultaneously. Gradually re-route traffic or use a crawl-based warm-up script that paces requests.
    
2.  Audit asset URLs for malformed query parameters. Incorrect parameters prevent CDN caching and ensure every request is a cache miss. Fix URL construction in the application to ensure consistent, cacheable URLs.
    
3.  If a planned traffic switch is required, notify Contentstack Support in advance. They can monitor the traffic pattern and assist if rate limits need temporary adjustment.
    
4.  Implement exponential backoff and retry logic in the application to handle 429 responses gracefully during the transition period.
    

After stabilizing the CDN cache state and fixing malformed URLs, monitor the request rate and confirm 429 errors return to baseline.

### 429 Errors After Large Asset or Entry Publish - Publish Triggers CDA Revalidation Traffic

Publishing a large batch of assets (for example, 12,000 assets) or a high-volume entry publish window is followed by a wave of HTTP 429 errors on the Delivery API. The customer asks whether the publish action and the 429 errors are related.

**Root Cause**

Yes - both large asset publishes and large entry publishes drive additional Delivery API and CDN revalidation traffic. When assets or entries are published, Contentstack sends cache invalidation signals to the CDN, prompting it to revalidate cached responses. If a large number of assets or entries are published simultaneously, the resulting cache invalidation and revalidation can temporarily spike request rates above the organization limit. This is compounded when GraphQL queries without CDN caching are in the traffic mix, as cache misses route directly to the origin.

**Resolution**

1.  Avoid publishing large asset batches in a single bulk operation during peak traffic hours. Stagger asset publishes into smaller batches (for example, 500–1000 assets at a time) separated by pauses.
    
2.  Schedule large asset publishes during off-peak periods to minimize overlap with production traffic.
    
3.  Implement retry logic with exponential backoff in applications to handle transient 429 responses after a large publish.
    
4.  If asset publish operations consistently generate revalidation traffic above the rate limit, contact Contentstack Support to review the rate limit allocation.
    

After staggering the asset publish, monitor the Delivery API error rate. If 429 errors do not recur at the same scale, the staggered approach is effective.

### 429 Errors from GraphQL Requests Not Served by CDN Cache

A spike of 20,000+ HTTP 429 errors occurs, with request rates reaching approximately 230 requests per second, exceeding this customer’s contracted CDA limit of 150 RPS (a customer-specific threshold, not the platform default). Analysis shows GraphQL queries are heavily contributing to the spike because they are not benefiting from CDN caching. Note that GraphQL origin requests are also independently capped at a platform default of 80 RPS per organization, separate from the CDA REST limit.

**Root Cause**

GraphQL POST requests may bypass CDN caching if the CDN is not configured to cache them. This causes every GraphQL request to hit the origin, consuming rate limit capacity. This is compounded when GraphQL queries use include\_all or deep reference chains without limit arguments, producing expensive queries that slow origin processing and cause backpressure.

**Resolution**

1.  Ensure the CDN caching layer is configured to cache GraphQL POST responses for frequently used queries. Use consistent query structures and avoid dynamic query generation that would create unique cache keys per request.
    
2.  Avoid using include\_all=true for top-level entry fetches combined with all references. Instead, fetch the top-level entry with specific include\[\] paths, or use separate API calls for heavy reference chains.
    
3.  Add limit arguments to all GraphQL queries to reduce response size and origin processing time.
    
4.  Implement request deduplication so multiple simultaneous identical requests share a single in-flight origin call rather than each hitting the API independently.
    

After improving CDN cache hit rates for GraphQL and reducing over-fetching, monitor the 429 error rate during the next traffic peak and confirm it stays within the rate limit.

### X-RateLimit Headers Now Included in CDA Responses

CDA API responses are returning rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining) that were not observed before. The customer asks whether this is expected and why it was not documented earlier.

**Root Cause**

X-RateLimit headers have been available in CDA responses for some time. They were previously associated primarily with the CMA, which led to the assumption that CDA responses did not include them. The headers are now consistently returned in CDA responses and are useful for monitoring consumption against the rate limit.

**Resolution**

This is expected behavior. Incorporate the headers into monitoring and throttling logic:

1.  X-RateLimit-Limit: the maximum number of requests allowed per second for the organization.
    
2.  X-RateLimit-Remaining: the number of requests remaining in the current rate limit window.
    
3.  When X-RateLimit-Remaining approaches zero, reduce request frequency or queue requests until the window resets.
    

Use X-RateLimit-Remaining as an early warning signal to reduce request rates proactively before 429 errors occur.

### 429 on CMA GET Endpoint - Organization-Level 10 RPS Limit

HTTP 429 responses appear when calling the CMA GET endpoint to fetch entries. The application is not making an obviously high volume of requests.

**Root Cause**

The CMA GET rate limit is 10 requests per second at the organization level by default. Applications that make sequential or lightly parallelized CMA GET calls can reach this limit quickly, especially when processing bulk entry lists or running scheduled jobs during peak editorial activity.

**Resolution**

1.  Implement exponential backoff: on receiving a 429, wait and retry with increasing delay intervals (for example, 1s, 2s, 4s, 8s).
    
2.  Add jitter to backoff intervals to prevent multiple clients from retrying simultaneously.
    
3.  Use pagination (limit + skip) to fetch entries in smaller batches rather than requesting all entries at once.
    
4.  Cache CMA responses where the data does not change frequently to reduce repeated calls.
    
5.  If the default 10 RPS limit is insufficient for the use case, contact the Customer Success Manager to request a rate limit increase (note: increases have commercial implications).
    

After implementing exponential backoff and pagination, re-run the operation and confirm 429 errors no longer appear or are handled gracefully with successful retries.

### Rate Limiting During Stack Migration - Pagination and Backoff Strategy

A migration script moving content between stacks fails partially due to rate limit errors. Each entry has multiple localized versions, generating a high volume of API requests that causes intermittent 429 errors for some locale versions.

**Root Cause**

Migration scripts that process entries sequentially with locale loops generate many API calls in rapid succession. With 17 locale versions per entry, even a modest entry count quickly exhausts the rate limit.

**Resolution**

1.  Implement a rate-aware migration loop: after each API call, check the X-RateLimit-Remaining header. If it falls below a safe threshold (for example, 5), add a pause before the next request.
    
2.  Use exponential backoff with jitter on 429 responses: on receiving a 429, wait the value specified in the Retry-After response header (if present), otherwise use an exponential backoff.
    
3.  Process locales in batches rather than all at once for each entry. For example, process 5 entries across 3 locales before moving to the next batch.
    
4.  Run the migration during off-peak hours to reduce competition with editorial traffic.
    
5.  If the migration volume genuinely requires a higher throughput, contact Contentstack Support in advance to request a temporary rate limit increase for the migration window.
    

After implementing rate-aware pagination and backoff, re-run the migration and confirm all locale versions are successfully migrated without 429 failures.

### Bulk API Pagination - Handling Rate Limits in High-Volume Operations

An application making bulk API calls hits rate limits and needs guidance on how to structure requests to stay within limits reliably.

**Root Cause**

Bulk operations that fetch or process large datasets often generate more API calls per second than the organization rate limit allows, especially when fetching all entries across multiple content types or locales.

**Resolution**

1.  Use limit and skip parameters to paginate through results in manageable chunks: GET /v3/content\_types/{uid}/entries?limit=100&skip=0, then increment skip by 100 per batch.
    
2.  Fetch the total count first using the count=true parameter to determine how many pages to fetch: GET /v3/content\_types/{uid}/entries?count=true.
    
3.  Add a configurable delay between page requests (for example, 50–100ms) to keep the aggregate request rate below the limit.
    
4.  Monitor X-RateLimit-Remaining in each response header and pause if it drops below a safe threshold.
    
5.  Process content types sequentially rather than in parallel to avoid multiple loops competing for the same rate limit budget.
    

After implementing paginated fetching with delays, confirm the total number of entries retrieved matches the count from the initial count request, and that no 429 errors occur during the full fetch.

Note on DataSync: The Contentstack Sync API operates on its own separate rate limit quota, independent of the CDA and CMA quotas. Running a DataSync initial sync concurrently with CDA delivery traffic or CMA migration operations will not cause the two to compete for the same rate limit budget. Each has its own allocation. Additionally, fetching an entry with references counts as a single API request - the reference resolution does not generate additional API calls against the rate limit.

### 429 Too Many Requests Errors on the Content Delivery API

HTTP 429 Too Many Requests errors appear in production, during deployments, or during build processes. The errors occur in bursts and may affect static site generation, server-side rendering, or high-traffic periods.

**Root Cause**

The default Content Delivery API rate limit is 100 requests per second per organization. When the total number of CDA GET requests across all stacks in the organization exceeds this threshold within a one-second window, the API returns 429 responses for the excess requests. Common triggers include:

*   Vercel or Next.js build processes making many simultaneous CDA calls
    
*   Release or bulk publish events triggering high-frequency API queries
    
*   Multiple applications or services sharing the same organization quota
    
*   Integration assets or scripts making unconstrained API calls
    

**Resolution**

1.  Implement request throttling and exponential backoff in all applications to smooth request rates below 100 RPS.
    
2.  Review the x-ratelimit-limit and x-ratelimit-remaining response headers to monitor live usage against the current limit.
    
3.  Stagger build processes and bulk operations to distribute requests over time.
    
4.  Use the Product Analytics dashboard to identify which content types, stacks, or endpoints are generating the highest request volumes.
    
5.  If the default 100 RPS limit is consistently insufficient for production workloads, contact Contentstack Support to request a limit increase. Note that increases above the default may have contractual and cost implications.
    

After implementing throttling and reviewing request patterns, monitor the API for a 24-hour period. If 429 errors no longer appear at the same frequency, the rate of requests is within limits.

### CDA Rate Limit vs GraphQL Rate Limit - These Are Independent

After receiving a CDA rate limit increase to 200 RPS, requests continue to be capped at 80 RPS. The x-ratelimit-limit header continues to show 80 even though the CDA limit was raised.

**Root Cause**

The CDA REST API and GraphQL API have separate, independent rate limits. Increasing the CDA REST limit does not affect the GraphQL limit. The GraphQL API has a hard default limit of 80 requests per second, which is enforced independently of the CDA REST limit. If traffic is routed through GraphQL, the 80 RPS cap applies regardless of the CDA REST limit in effect.

**Resolution**

1.  Identify whether the rate-limited requests are being sent to the CDA REST endpoint (cdn.contentstack.io) or the GraphQL endpoint (graphql.contentstack.com).
    
2.  If requests are hitting the GraphQL endpoint, a separate rate limit increase request is required for the GraphQL API.
    
3.  Contact Contentstack Support to request a GraphQL rate limit increase, noting that this may require a KCR (Key Configuration Request) and has its own approval process.
    
4.  As a workaround while awaiting a GraphQL limit increase, use the CDA REST API for high-volume requests where GraphQL is not strictly required.
    

After identifying the correct endpoint and applying the appropriate limit increase, monitor the x-ratelimit-limit header in responses from each endpoint to confirm the limits are updated.

### CDA Rate Limits Are Organization-Level and Cannot Be Split Per Stack

Multiple stacks within the same organization share an API rate limit. One stack consuming a large proportion of the quota causes 429 errors on other stacks. A request is made to reserve or guarantee a fixed percentage of the rate limit per stack.

**Root Cause**

Contentstack CDA rate limits are enforced at the organization level, not per stack. All stacks within an organization share the same rate limit pool. There is no mechanism to reserve, allocate, or guarantee a fixed portion of the rate limit to an individual stack.

**Resolution**

1.  Implement application-side request throttling for each stack independently to prevent any single stack from consuming a disproportionate share of the organization quota.
    
2.  Use the Product Analytics dashboard to identify which stacks are generating the highest request volumes and apply targeted throttling.
    
3.  Stagger high-volume operations (deployments, builds, releases) across stacks to avoid simultaneous quota consumption.
    
4.  Contact Contentstack Support or your CSM if the aggregate organization limit consistently needs to be higher to support all stacks.
    

After implementing per-stack throttling, monitor the overall organization rate limit usage and confirm that no single stack is causing 429 errors that affect other stacks.

### Identifying and Resolving 429 Errors Caused by an Integration Asset

A sudden spike of 429 errors appears on the Images API or CDA during a specific time window. The errors are not caused by end-user traffic but originate from a backend integration or automated process.

**Root Cause**

An integration asset - such as a third-party connector, a scheduled script, or an automated build pipeline - is making an excessive number of API calls in a short window, exhausting the rate limit and causing 429 errors for all other traffic. The integration does not implement request throttling or back-off logic.

**Resolution**

1.  Review all active integrations, scheduled tasks, and automated pipelines that make CDA or Images API calls.
    
2.  Identify the specific integration responsible by correlating the 429 spike timestamp with integration execution logs.
    
3.  Add request throttling and exponential backoff to the identified integration to prevent it from bursting above the rate limit.
    
4.  Consider scheduling high-volume integration jobs during off-peak hours to reduce overlap with production traffic.
    
5.  Contact Contentstack Support and request logs for the affected time window to confirm the source of the traffic spike.
    

After adding throttling to the integration, monitor the API error rate during the next scheduled integration run. If 429 errors do not recur at the same volume, the integration is operating within the rate limit.

### 429 Rate Limiting on the Images API

HTTP 429 Too Many Requests errors appear on requests to images.contentstack.io rather than on the standard CDA endpoint. The errors occur during short traffic spikes and affect image delivery specifically.

**Root Cause**

The Images API (images.contentstack.io) has its own rate limit, separate from the CDA REST and GraphQL limits. When the volume of asset requests to the Images API exceeds the configured threshold within a one-second window, 429 errors are returned for the excess image requests. This commonly occurs during:

*   High-traffic campaigns or product launches where many users load image-heavy pages simultaneously
    
*   Automated scripts or crawlers requesting large numbers of image URLs in rapid succession
    
*   Integration assets that call image URLs without throttling
    

**Resolution**

1.  Implement client-side caching for image responses to avoid repeated requests for the same asset URL.
    
2.  Use a CDN layer in front of the application to serve image responses from cache and reduce the volume of requests reaching the Contentstack Images API.
    
3.  Audit all integrations and automated processes that make image requests and add throttling where unconstrained calls are identified.
    
4.  Review images.contentstack.io request metrics via Contentstack Support to understand peak consumption patterns.
    
5.  If the Images API limit is consistently insufficient for production traffic, contact Contentstack Support to discuss a limit increase.
    

After implementing caching and throttling for image requests, monitor the 429 error rate on the Images API. If errors reduce or cease, the request volume is within the rate limit.

## Assets & Metadata Management

### Attaching Custom Metadata to Assets for Right to Be Forgotten (RTBF) Workflows

An ingestion platform uploads influencer-created assets to Contentstack and needs to attach creator ID metadata to each asset. The goal is to later query assets by creator ID to support Right to Be Forgotten (RTBF) deletion requests.

**Root Cause**

Contentstack supports custom metadata on assets and entries, but the workflow requires three separate CMA calls to correctly attach and publish the metadata.

**Resolution**

1.  Call 1: Upload the asset: POST /v3/assets with the file data.
    
2.  Call 2: Create metadata: POST /v3/metadata with the asset UID, the metadata key (for example, creator\_id), and the value. Include the extension\_uid or app\_uid in the request.
    
3.  Call 3: Publish the asset: POST /v3/assets/{asset\_uid}/publish. Metadata is published along with the asset.
    
4.  To query assets by creator\_id for RTBF: use the CMA asset search with metadata filters to retrieve all assets matching the creator\_id, then delete them as required.
    

After completing the three-step workflow, retrieve an uploaded asset and confirm the metadata key (creator\_id) is present in the response and correctly reflects the uploaded value.

### Permanent Asset URL Not Updating After File Replacement - Cloudflare Cache

After replacing a PDF or image asset in the CMS and republishing, the permanent URL continues to serve the old file. The file URL (versioned URL) reflects the latest version correctly, but the permanent URL does not.

**Root Cause**

The permanent URL is cached by Cloudflare CDN. After a file replacement, the origin correctly serves the new file, but the Cloudflare cache layer continues to serve the previously cached version of the permanent URL until the cache is purged.

**Resolution**

1.  Contact Contentstack Support and provide the affected asset UID and the permanent URL.
    
2.  Request a Cloudflare cache purge for the specific permanent URL.
    
3.  After the purge is completed, request the permanent URL again and confirm it now serves the updated file.
    
4.  As an interim workaround, use the versioned file URL (which reflects the latest version immediately) until the permanent URL cache is purged.
    

After the Cloudflare cache is purged, request the permanent URL and confirm the replacement file is served correctly.

### CMA Timeout Errors - Increasing SDK Timeout for Large Uploads and Slow API Calls

CMA operations fail with a 408 Request Timeout error. This most commonly affects large asset uploads, but can also occur on slow CMA calls such as fetching all taxonomies or performing complex bulk operations on Vercel-hosted or serverless environments with strict execution time limits.

**Root Cause**

The default client-side timeout in the Contentstack SDK is set to 30 seconds. Any CMA operation that takes longer than this threshold triggers a client-side 408 timeout. Serverless platforms such as Vercel also impose their own request execution time limits (typically 10–30 seconds), which can cause premature timeout failures independent of the SDK setting.

**Resolution**

1.  Increase the timeout value in the Contentstack SDK client initialization. Set the timeout parameter to a higher value such as 60,000 ms (60 seconds) or higher depending on the expected operation duration.
    
2.  Example SDK initialization with extended timeout: Contentstack.Stack({ api\_key: '...', delivery\_token: '...', environment: '...', timeout: 60000 })
    
3.  For Vercel-hosted applications, also increase the function execution timeout in vercel.json or the Vercel dashboard for the affected API routes.
    
4.  For slow taxonomy or bulk CMA calls specifically, consider paginating results (using limit and skip) to reduce per-request response size and processing time.
    
5.  For very large file uploads (>100 MB), consider increasing the timeout further or implementing chunked upload logic.
    

After increasing the timeout in the SDK and platform configuration, retry the failing operation. If it completes without a 408 error, the timeout is now sufficient for the operation's duration.

### Development Content Appearing in Production - Shared Delivery Token

Content published only to the development environment is also appearing in the production environment on the live site. The same content should not be visible in production.

**Root Cause**

The production application is using a delivery token that has access to both the development and production environments. Since the token is not scoped to production only, any content published to development is also returned when the production app queries with this token.

**Resolution**

1.  Navigate to Settings > Tokens in the Contentstack stack.
    
2.  Create a new Delivery Token scoped exclusively to the production environment.
    
3.  Update the production application configuration to use the new production-scoped delivery token.
    
4.  Confirm the development environment has its own separate delivery token scoped only to development.
    

After updating the production application to use the production-scoped token, verify that content published only to development no longer appears on the production site.

### Identifying Unpublished Assets via CMA - Use include_publish_details

A customer needs to identify and publish all assets that are not yet published to a specific environment. The Management API does not appear to support filtering assets by publish status directly.

**Root Cause**

The CMA asset query endpoint does not support direct filtering by publish status or environment in query parameters. However, asset publish details can be retrieved and used for client-side filtering.

**Resolution**

1.  Add include\_publish\_details=true to the CMA asset query: GET /v3/assets?include\_publish\_details=true
    
2.  The response will include a publish\_details array for each asset, showing which environments it is published to.
    
3.  Process the response client-side to filter assets where the target environment is absent from the publish\_details array.
    
4.  For large asset libraries, use incremental queries (for example, filtering by updated\_at range) to reduce response size and processing overhead.
    
5.  After identifying unpublished assets, publish them using: POST /v3/assets/{asset\_uid}/publish
    

After applying the client-side filter, confirm that the identified unpublished assets are correctly targeted and that subsequent publish calls succeed.

### extension_uid Required for Asset Metadata - App-Level Alternative

The CMA documentation requires extension\_uid when creating metadata for assets. The customer wants to use an app (not an extension) for their metadata workflow and is unclear whether this is supported.

**Root Cause**

The metadata feature was originally designed for extensions, which is why extension\_uid appears as a required field in the documentation. Each extension or app has its own metadata namespace, which prevents collision between different integrations. Apps can also use metadata, but must pass the app UID in place of the extension UID.

**Resolution**

1.  When using an app instead of an extension, pass the app UID as the value for extension\_uid in the metadata creation request.
    
2.  The metadata API treats app UIDs and extension UIDs interchangeably in the namespace field.
    
3.  Confirm the app UID in the Contentstack Developer Hub under the app's settings.
    
4.  Include the app UID in the metadata request body: { "metadata": { "extension\_uid": "<your\_app\_uid>", "key": "creator\_id", "value": "12345" } }
    

After using the app UID in the metadata request, confirm the metadata is created and retrievable via the asset's metadata endpoint.

### Adding Multiple Assets to a Single Entry Field

An editor needs to attach multiple assets (for example, images for a photo album) to a single entry. The standard File field only allows one asset to be attached.

**Root Cause**

By default, a File field in Contentstack allows a single asset to be attached. To support multiple assets in one field, the Multiple option must be enabled in the field’s Advanced Properties.

**Resolution**

1.  Navigate to the content type in the Content Type Builder.
    
2.  Select the File field where multiple assets should be allowed.
    
3.  Open the field’s Advanced Properties.
    
4.  Enable the Multiple toggle and set the maximum number of files to allow (for example, 10 for a photo album).
    
5.  Save the content type.
    
6.  Editors can now attach multiple assets within that single File field on the entry.
    

After enabling Multiple on the File field, open a test entry and confirm multiple assets can be uploaded or selected within the field.

### CDN Cache Staleness - Deleted Entries Still Served, New Entries Not Appearing

After creating or deleting entries, the CDN continues to serve stale data: a deleted entry is still returned by the API, a newly created entry does not appear, or a query returns an entry that does not match the request. The issue is observed on the eu-cdn endpoint.

**Root Cause**

In the reported case, this behavior resolved on its own before a root cause could be confirmed - Contentstack’s investigation was limited by the absence of the specific entry UID and request/response details from the affected window, and the CDN endpoint could not be made to reproduce the same behavior afterward. No specific cause was diagnosed. Possible contributing factors for this class of symptom include CDN propagation delay across edge nodes in certain regions, cache-busting logic not triggering correctly for specific query patterns, or a transient CDN routing issue where an edge node has not yet received an invalidation signal - but these are plausible explanations, not a confirmed mechanism.

**Resolution**

1.  Wait briefly - CDN propagation typically completes within a few seconds to minutes. If the correct data appears after a short wait, the propagation delay was the cause.
    
2.  Use a cache-busting query parameter to force a fresh fetch from the origin while investigating: append ?cb=<timestamp> to the request URL.
    
3.  If the stale data persists beyond 10–15 minutes, contact Contentstack Support and provide: the affected entry UIDs, the CDN endpoint (for example, eu-cdn), the operation performed (create/delete/update), the timestamp of the operation, and the incorrect response received.
    
4.  Engineering can force a CDN cache purge for the specific cache key if standard propagation has failed.
    

After the CDN purge or propagation completes, re-query without the cache-busting parameter and confirm the response reflects the correct current state of the entry.

### Image crop Parameter Ignored - CDN-Level Bug

The crop parameter in image transformation URLs has no effect. The original uncropped image is returned despite valid crop parameters being present in the URL. This impacts live, customer-facing pages.

**Root Cause**

The crop parameter being silently ignored is caused by a CDN-level regression. Image transformation parameters such as crop, canvas, and quality are processed by the CDN provider’s image transformation pipeline. When the CDN updates its image transformation configuration or migrates between providers, the transformation pipeline can regress, causing previously working parameters to be ignored.

**Resolution**

1.  If crop parameters stop working unexpectedly, contact Contentstack Support immediately and provide affected image URLs as examples.
    
2.  The Contentstack CDA team will raise the issue with the CDN partner for investigation and fix.
    
3.  As an interim workaround while the CDN fix is applied, consider server-side or build-time image cropping using an external image processing service or tool.
    

After the CDN fix is applied, test image URLs with crop parameters and confirm the expected cropped output is returned.

### Canvas Parameter Stops Preserving Transparency After CDN Migration

The canvas parameter on image URLs, which previously preserved transparent backgrounds, now renders transparency as a solid white background. This affects CRM email campaigns and dark mode rendering.

**Root Cause**

A CDN migration (from Fastly to Cloudflare) caused a regression in how the canvas parameter handles transparency. Cloudflare’s image transformation pipeline handles transparency differently from Fastly’s, and the canvas parameter behavior changed during the migration without a direct configuration equivalent.

**Resolution**

A direct fix for the canvas transparency regression through Cloudflare configuration was not feasible. Recommended workarounds:

1.  Pre-process images to include the correct background before uploading, so the asset itself has the intended background and does not rely on the canvas parameter for transparency handling.
    
2.  Apply background overlay or transparency handling at the frontend rendering layer rather than at the image URL level.
    
3.  Contact Contentstack Support if this regression is impacting production - escalation to the CDN team may produce a configuration fix.
    

After applying the workaround, confirm that image rendering in emails and dark mode displays the correct background behavior.

### Assets Returning application/json Content-Type Instead of Image MIME Type

Images served via the Contentstack CDN intermittently return a Content-Type of application/json instead of the expected image MIME type (for example, image/jpeg or image/png). This causes images to fail to render and broken image placeholders to appear.

**Root Cause**

This Content-Type mismatch is caused by a CDN-level processing regression. The CDN’s image transformation pipeline incorrectly sets the content type on responses for certain image assets, particularly when image transformation parameters (such as resize, quality, or format conversion) are applied. The underlying asset is correct - the issue is in the CDN response headers.

**Resolution**

1.  Contact Contentstack Support immediately if widespread application/json responses are observed for image assets. Provide affected image URLs as examples.
    
2.  The CDA team will investigate and escalate to the CDN partner for a fix.
    
3.  As an interim mitigation, implement client-side content type validation: check the response Content-Type header before rendering as an image, and retry the request without transformation parameters if the content type is incorrect.
    
4.  Remove or simplify image transformation parameters in the URL as a temporary workaround to avoid triggering the transformation pipeline.
    

After the CDN fix is applied, test image URLs with transformation parameters and confirm the correct image MIME type is returned in the Content-Type header.

### Blurry PNG Images When Using auto=webp or auto=avif

PNG images appear blurry or lower quality in production when the auto=webp or auto=avif image transformation parameter is applied. The blurriness is inconsistent - different formats are affected at different times.

**Root Cause**

The blurriness is caused by a CDN-level compression regression in the image transformation pipeline for WebP and AVIF format conversions. The CDN partner’s compression settings for the conversion process produce lower quality output than expected for PNG source images.

**Resolution**

1.  Contact Contentstack Support and provide example image URLs showing the blurry output. The CDA team will escalate to the CDN partner.
    
2.  The CDN partner applies a production fix to correct the compression quality for WebP and AVIF conversions.
    
3.  As a short-term workaround, explicitly set a quality parameter alongside the format conversion: ?auto=webp&quality=85. This overrides the default compression level and can mitigate the blurriness.
    

After the CDN fix is confirmed, test affected image URLs with auto=webp and confirm images are rendered at the expected quality.

### Image Size Increases After CDN Migration from Fastly/Akamai to Cloudflare

After a CDN migration, image files served via Contentstack are noticeably larger than before the migration. The same images were smaller under the previous CDN provider.

**Root Cause**

The previous CDN (Fastly or Akamai) applied image compression by default, reducing file sizes automatically. After migration to Cloudflare, the image compression behavior changed - Cloudflare’s image resizing handles compression differently and may produce larger file sizes for the same source image without explicit quality settings.

**Resolution**

1.  Add an explicit quality parameter to all image URLs: ?quality=85 (or an appropriate value for the use case). This instructs Cloudflare’s image processing pipeline to apply compression, reducing file sizes.
    
2.  Test different quality values to find the right balance between file size reduction and visual quality. Values between 75 and 85 are typically effective for most images.
    
3.  For existing image URLs embedded in content, use a find-and-replace script or URL rewriting rule to append the quality parameter.
    

After adding the quality parameter, verify that image file sizes return to or below the pre-migration sizes while maintaining acceptable visual quality.

### Error 499 - Client Closed Request on Mobile App Image Loads

A mobile application reports approximately 96,000 Error 499 (Client Closed Request) instances for image loading. Images load correctly in desktop web browsers but fail frequently in the mobile app, particularly for users in specific regions such as Australia and Taiwan.

**Root Cause**

HTTP 499 is a Cloudflare/CDN status code indicating that the client terminated the connection before the server completed the response. This is a client-side event - the mobile app closed the connection before the image finished downloading. Investigation confirmed this is not a Contentstack or CDN server error. The root cause is regional network variance: users on weaker cellular signals in the affected regions hit the mobile app’s pre-configured timeout thresholds before the image transfer completes. The error rate was proportionally consistent with overall traffic growth and not an anomaly.

**Resolution**

1.  Error 499 is a client-side termination and does not require a fix on the Contentstack platform.
    
2.  Increase the image request timeout in the mobile app configuration to allow more time for image downloads on slower connections.
    
3.  Implement progressive image loading or placeholder display while images load to improve perceived performance on slow connections.
    
4.  Use image optimization parameters (quality, resize, auto=webp) to reduce image file sizes, making downloads complete faster on slower networks.
    
5.  Consider implementing retry logic in the mobile app for failed image requests rather than treating a single timeout as a permanent failure.
    

After increasing timeouts and reducing image sizes via optimization parameters, monitor the Error 499 rate in the affected regions. A reduction confirms the client timeout was the primary cause.

### Cloudflare Cross-Zone Error 1000 - DNS-Based Custom Domain Asset Mapping

A customer wants to serve Contentstack assets under their own domain (for example, assets.example.com) by mapping a DNS CNAME to images.contentstack.io. The DNS mapping fails with Cloudflare Error 1000.

**Root Cause**

Cloudflare’s cross-zone restriction (Error 1000) prevents DNS CNAME records on a Cloudflare-managed domain from pointing to another Cloudflare-managed zone (such as images.contentstack.io, which is also on Cloudflare). This is a Cloudflare architectural limitation - CNAME flattening between different Cloudflare customers is blocked at the DNS level.

**Resolution**

Two viable alternatives to DNS-based CNAME mapping:

1.  Cloudflare Worker proxy: deploy a Cloudflare Worker on the custom domain that intercepts requests to the custom asset URL, fetches the asset from images.contentstack.io, and returns the response. This allows the custom domain to serve Contentstack assets transparently without a direct CNAME.
    
2.  Mask Asset Domains feature: use the Contentstack Mask Asset Domains feature, which allows the CDA to return asset URLs using a custom domain at the application level. This does not change the underlying CDN delivery but allows the application to control which domain appears in API responses. Refer to the Contentstack Mask Asset Domains documentation for setup.
    
3.  Reverse proxy at the web server layer: configure Nginx, Caddy, or a cloud load balancer to proxy requests from the custom domain path to images.contentstack.io.
    

After implementing the chosen approach, verify that asset URLs served under the custom domain return the correct images and headers, and that no Cloudflare Error 1000 is triggered.

### Unpublished Asset Still Accessible via Direct CDN URL

An asset that has been unpublished in Contentstack remains publicly accessible via its direct CDN URL and continues to be indexed by search engines. Republishing a replacement does not make the old URL inaccessible.

**Root Cause**

Assets hosted on Contentstack are served via CDN. Unpublishing an asset in Contentstack removes it from the CDA API response (it will no longer be returned by content queries), but it does not purge the CDN cache for the direct asset URL or restrict access to the URL. Anyone who has the direct URL can continue to access the asset as long as the CDN has it cached or until the CDN TTL expires.

**Resolution**

1.  Enable the Secure Public URLs feature for the stack. This feature generates time-bound, token-based URLs for assets, making asset URLs non-permanent and inaccessible without a valid token.
    
2.  After enabling Secure Public URLs, the direct asset URL that was previously accessible will require a valid signed token. Existing bookmarked or cached URLs will fail after the token expires.
    
3.  Submit a de-indexing request to search engines (via Google Search Console URL Removal tool) for the old asset URL to remove it from search results.
    
4.  Contact Contentstack Support to request a CDN cache purge for the specific old asset URL if immediate inaccessibility is required.
    

After enabling Secure Public URLs, confirm that accessing the old asset URL directly returns an error (403 or 401) rather than the asset content.

### Assets Loaded on Fraudulent or Unauthorized External Domains

Contentstack-hosted assets are being embedded and displayed on fraudulent or scam websites using the direct asset URLs. The customer wants to restrict which domains can load their assets.

**Root Cause**

Contentstack assets are publicly accessible by default once published - the CDN does not enforce referrer-based domain restrictions. Any website that obtains the direct asset URL can embed and display the asset without restriction.

**Resolution**

1.  Enable the Secure Public URLs feature. This replaces permanent asset URLs with signed, time-bound URLs that expire. Without a valid signed token, the asset URL cannot be loaded - preventing unauthorized websites from using the assets.
    
2.  In the application’s asset delivery logic, generate signed URLs server-side and serve them to end users. Ensure the token expiry is short enough that cached tokens cannot be shared.
    
3.  Report the fraudulent domains to the relevant domain registrar and hosting provider for takedown.
    

After enabling Secure Public URLs and implementing server-side signed URL generation, confirm that the fraudulent domain’s asset embeds no longer load (they will receive access denied errors).

### Permanent Asset URLs Cannot Be Preserved Across Stack Migrations

During a migration to a new Contentstack stack, asset URLs change because new asset UIDs are generated. Existing application code and external links referencing the old asset URLs break after migration.

**Root Cause**

Contentstack asset delivery URLs are derived from the stack API key and the asset UID. When assets are imported into a new stack, the import process generates new asset UIDs. Because the UID is part of the URL, the permanent asset URL changes. There is no mechanism in Contentstack to preserve original asset UIDs, maintain the same URLs across stacks, or configure redirects or aliases at the CDN level.

**Resolution**

Plan for URL changes as part of the migration strategy:

1.  Build a mapping table of old asset URLs to new asset URLs during the migration process. Update all application code, content references, and external documentation to use the new URLs.
    
2.  Implement URL redirects at the application or CDN layer: map old asset URL patterns to new URL patterns using redirect rules in the application server, CDN, or a middleware layer.
    
3.  If the volume of asset URL changes is large, automate the redirect mapping using the asset migration data and implement the redirects programmatically.
    

After setting up URL redirects, verify that requests to old asset URLs are correctly redirected to the new URLs and return the expected assets.

### Restricting Asset Playback or Access to Specific Domains

A customer wants to restrict video or image assets hosted in Contentstack so they can only be played or loaded from their own domain. They are considering a workflow of creating delivery tokens per user session, using the assets, and then deleting the token. They want to understand whether this is viable at scale.

**Root Cause**

Delivery tokens are environment-level credentials, not session-level tokens. They are not designed to be created and deleted per user session. Most Contentstack plans have a hard limit on the total number of delivery tokens per stack (typically 50–100), which would be exhausted almost immediately in a high-traffic scenario. Additionally, token creation and deletion via the CMA is subject to the CMA rate limit (10 RPS), making per-session token management impractical at scale.

**Resolution**

1.  Use the Secure Public URLs (Asset Privatization) feature instead. This generates short-lived, signed URLs for assets that expire after a configurable time window. Only valid signed URLs can access the asset, preventing direct URL sharing or embedding by external sites.
    
2.  To enable Secure Public URLs, contact Contentstack Support or your Customer Success Manager. The feature is enabled at the stack level.
    
3.  Once enabled, generate signed asset URLs server-side using the Contentstack SDK or API for each user session. The URL expires after the configured TTL, preventing long-term sharing.
    
4.  Do not use per-session delivery token creation and deletion - this approach is not viable at scale due to token count limits and CMA rate limits.
    

After enabling Secure Public URLs, verify that assets are only accessible via signed URLs and that direct access to the original asset URL returns an access denied response.

### Mapping a Custom Domain for Asset URLs - Mask Asset Domains

A customer wants API responses to return asset URLs using a custom domain instead of the default images.contentstack.io. Stack-level configuration for this mapping is not available in the Contentstack UI.

**Root Cause**

Contentstack does not currently provide a stack-level UI setting to automatically replace images.contentstack.io with a custom domain in API responses. This capability requires either a client-side URL rewriting approach or the Mask Asset Domains feature.

**Resolution**

1.  Use the Mask Asset Domains feature: this Contentstack feature allows the CDA to return asset URLs using a custom domain in API responses. Refer to the Contentstack Mask Asset Domains documentation for setup steps. Note: this controls what domain appears in the API response but requires a corresponding reverse proxy or CDN configuration to route requests from the custom domain to Contentstack’s CDN.
    
2.  Alternatively, implement URL replacement at the application layer: after fetching entries from the CDA, replace images.contentstack.io with the custom domain in asset URL strings before rendering or passing to the frontend.
    
3.  For a reverse proxy approach: configure Nginx, Caddy, or a cloud CDN rule to serve requests to the custom domain by proxying to images.contentstack.io. This handles routing independently of what the API returns.
    
4.  If stack-level automatic domain mapping is a business requirement, contact your Customer Success Manager - this may be evaluated as a future platform capability.
    

After configuring Mask Asset Domains or the reverse proxy, verify that API responses return asset URLs using the custom domain and that assets load correctly through the custom domain URL.

### Uploaded Assets Are Publicly Accessible Even When Not Published

Assets uploaded to Contentstack remain accessible via their direct URL even when they have not been published to any environment. This prevents restricting access to unpublished or draft assets.

**Root Cause**

By design, Contentstack assets are publicly accessible once uploaded, regardless of their publish status. The asset URL is deterministic and accessible without authentication. Publish status controls whether an asset is returned in API responses, but does not restrict direct URL access.

**Resolution**

Two approaches are available depending on the use case:

1.  Use the Contentstack Delivery API to fetch assets programmatically. Append the environment parameter to the request (for example: ?environment=production) to ensure only assets published to the specified environment are returned.
    
2.  To restrict direct URL access entirely, implement secure asset URLs with token-based access or serve assets through a proxy layer that enforces publish-status checks before delivery.
    

After implementing environment-scoped API fetching, confirm that only published assets are returned in the API response for the specified environment.

### Image quality Parameter Has No Effect on WEBP Lossless Images

Modifying the quality query parameter in the Image Delivery API URL (for example, ?quality=1 vs ?quality=100) produces no change in file size or visual quality for WEBP images. Both values return identical results.

**Root Cause**

The quality parameter is not applicable to WEBP lossless images. WEBP lossless encoding does not use a lossy quality scale; the image data is always compressed without perceptual quality loss regardless of the quality value passed. This is a format-level characteristic, not a Contentstack limitation.

**Resolution**

This is expected behavior and requires no corrective action. To achieve file size reduction for WEBP images:

1.  Use WEBP lossy format by specifying format=webp without lossless encoding - lossy WEBP does respond to the quality parameter.
    
2.  If lossless output is required and file size is a concern, consider pre-optimizing the source image before uploading.
    

After switching to lossy WEBP format, confirm that varying the quality parameter produces a measurable difference in file size.

### All Assets Are Always Served via the Image Delivery API

Assets are requested without any image optimization parameters (for example, without ?quality=100 or format=webp) in an attempt to bypass the Image Delivery API and reduce monthly request counts. However, API usage counts remain unchanged.

**Root Cause**

All assets uploaded to Contentstack are served via the Image Delivery API by default, regardless of whether optimization query parameters are present in the URL. Omitting parameters does not bypass the Image Delivery API - every asset request, with or without parameters, is counted as an Image Delivery API call.

**Resolution**

API request counts from asset delivery cannot be bypassed by changing the URL format. To reduce Image Delivery API usage:

1.  Implement client-side or CDN-level caching to reduce repeated requests to the same asset.
    
2.  Review asset usage patterns in Product Analytics to identify high-frequency asset requests and optimize delivery through caching or lazy loading.
    
3.  Contact the Contentstack account team to review quota allocations if asset delivery volume consistently exceeds plan limits.
    

After implementing caching, monitor the Image Delivery API usage metrics in the Product Analytics dashboard to confirm that repeated requests to the same asset are being served from cache.

### Asset Dimensions Not Returned for IFile References - Use include_dimension and include_all

Image dimensions (width and height) are not returned in the CDA response when fetching entries that contain IFile references, even though the dimensions are visible in the Contentstack entry UI.

**Root Cause**

The Content Delivery API excludes asset dimension data from responses by default to keep payload size small. Two parameters must be explicitly included for dimension data to appear: include\_dimension=true to enable dimension output, and include\_all=true to ensure the full asset metadata within IFile references is resolved.

**Resolution**

1.  Add include\_dimension=true to the CDA request query parameters.
    
2.  Add include\_all=true to the same request to ensure IFile reference metadata is fully resolved.
    
3.  Example: GET /v3/content\_types/{uid}/entries?include\_all=true&include\_dimension=true
    
4.  Re-fetch the entry and confirm the dimensions object containing height and width appears in the asset field of the response.
    

After adding both parameters, execute the API request and verify that the asset field in the response includes a dimensions object with height and width values.

### Asset Download Fails Due to Version Mismatch in Asset URL

Attempting to fetch or download an asset via the API fails. The asset exists in the CMS and has been published, but the request returns an error or an incorrect file.

**Root Cause**

The version number in the asset URL does not match the current version of the asset. When an asset is updated or replaced, its version number is incremented. If an older version number is hardcoded in the URL or stored in a reference, the request targets a version that may no longer exist or has been superseded.

**Resolution**

1.  Retrieve the latest version of the asset by fetching it via the CDA without a version parameter, which returns the currently published version by default.
    
2.  If using a hardcoded asset URL, update it to reflect the current version number retrieved from the asset’s API response.
    
3.  Avoid storing version-specific asset URLs in application code or external systems; instead, store the base asset UID and resolve the URL dynamically via the API.
    

After correcting the asset URL to use the current version number, retry the download request and confirm the asset is returned successfully.

### CDA Returns a Maximum of 250 Assets Per Request

A CDA request to fetch all assets returns only approximately 250 results, even when a high limit value is specified. This differs from previous behavior where thousands of assets could be returned in a single call.

**Root Cause**

The Content Delivery API enforces a maximum limit of 250 assets per request. This is the expected platform cap and has not been reduced - earlier behavior that returned more results was not a supported feature. Requests with higher limit values are silently capped at 250.

**Resolution**

1.  Use pagination to retrieve the full asset set across multiple requests.
    
2.  Set limit=100 (or up to 250) per request and use the skip parameter to page through results.
    
3.  Example sequence: first request with skip=0&limit=100, second with skip=100&limit=100, and so on until the total count is reached.
    
4.  Use the count parameter in an initial request to determine the total number of assets before paginating.
    

After implementing pagination, confirm that running through all pages returns the expected total number of assets.

### Permanent Asset Link Not Updating After File Replacement

A permanent (canonical) asset link continues to serve the old file after the asset has been replaced in the CMS. The updated file is visible in the CMS but the permanent URL still returns the original version.

**Root Cause**

When an asset is replaced, the permanent link should update to reflect the new file. A platform-level issue prevented the permanent link from correctly resolving to the replacement file. This was identified as an engineering defect and required a backend fix.

**Resolution**

1.  If the permanent link is not updating after asset replacement, contact Contentstack Support and report the affected asset UID and permanent link URL.
    
2.  Engineering will investigate and apply the required fix to restore correct permanent link resolution.
    
3.  As an interim workaround, use the versioned asset URL returned in the CDA response, which will correctly point to the latest published version.
    

After engineering applies the fix, confirm by requesting the permanent link URL and verifying it returns the replacement file content.

### Converting Animated GIF to Animated WebP Is Not Supported

Using the Image Delivery API parameter format=webp on an animated GIF returns the original GIF file instead of an animated WebP. Conversion to static formats like JPG works correctly.

**Root Cause**

The Contentstack Image Delivery API does not support conversion of animated GIFs to animated WebP. The format=webp parameter converts the image to a static WebP frame, not an animated sequence. This is a known platform limitation.

**Resolution**

1.  Use an external tool or service (such as FFmpeg, CloudConvert, or Squoosh) to convert animated GIFs to animated WebP before uploading to Contentstack.
    
2.  Upload the pre-converted animated WebP file directly to Contentstack as the source asset.
    
3.  Serve the animated WebP file as-is from Contentstack without applying the format conversion parameter.
    

After uploading the pre-converted animated WebP file, request the asset URL and confirm it delivers the animated WebP format as expected.

### Asset Inside a Global Field Inside a Modular Block Returns No Data

A CDA request returns no data for an asset field when the asset is nested inside a global field that is itself part of a modular block. The structure is valid in the CMS and the REST API call is correctly formed.

**Root Cause**

The asset field is returning no data because the asset has not been published to the target environment. The CDA only returns published assets. An asset that exists in the CMS but has not been published is excluded from the response regardless of the nesting depth or structure.

**Resolution**

1.  Navigate to the Assets section in the CMS and locate the asset referenced within the global field.
    
2.  Publish the asset to the target environment.
    
3.  Re-run the CDA request and confirm that the asset field now returns the expected data.
    

After publishing the asset, execute the CDA request and verify that the asset data is now present in the modular block and global field response.

### AVIF Image Optimization Fails for Images Exceeding 4096 x 4096 Pixels

Image optimization using the AVIF format fails during testing. Error headers are returned in the response when requesting optimized AVIF output, while other formats like JPEG work correctly.

**Root Cause**

The Contentstack Image Delivery API enforces a 4096 x 4096 pixel limit for AVIF optimization. Images with dimensions exceeding this threshold cannot be processed into AVIF format and the optimization request will fail.

**Resolution**

1.  Check the dimensions of the source image. If the image exceeds 4096 pixels in either dimension, AVIF optimization is not available for that asset.
    
2.  Use auto=webp as a workaround. The WebP format does not have the same pixel dimension restriction and will serve a modern, well-compressed format with broad browser support.
    
3.  Alternatively, resize the source image to within 4096 x 4096 pixels before uploading if AVIF output is specifically required.
    

After switching to auto=webp for affected images, confirm that optimized images are served correctly without error headers in the response.

### Scheduled Asset Publish Fires Immediately Instead of at the Scheduled Time

When scheduling an asset to be published or replaced at a specific date and time, the asset publishes immediately rather than waiting for the scheduled time.

**Root Cause**

Asset scheduling for publish and unpublish actions operates differently from entry scheduling. The immediate trigger behavior occurs when the asset publish action is initiated without the scheduling parameters being correctly configured or when the scheduling feature is not fully supported for the specific asset operation being performed.

**Resolution**

1.  Verify that the scheduling parameters (scheduled\_at date/time and timezone) are correctly set in the publish request.
    
2.  Confirm the scheduled publish is configured through the correct UI flow: navigate to the asset, use the Publish option, and select the Schedule option with the target date and time.
    
3.  If the issue persists, contact Contentstack Support with the asset UID, the scheduled time, and the actual publish time to assist in diagnosing the scheduling behavior.
    

After confirming the scheduling configuration, verify that the asset does not appear in the target environment until the scheduled time has passed.

### Image Optimization Best Practices for Contentstack Delivery

High Image Delivery API usage, slow asset load times, or large bandwidth consumption can result from sub-optimal asset delivery configuration. The following practices reduce bandwidth and improve performance.

**Resolution**

*   Use auto=webp to serve WebP format to browsers that support it, reducing file size compared to JPEG or PNG without perceptual quality loss.
    
*   Set quality values between 70 and 85 for JPEG and lossy WebP. Values above 90 provide diminishing returns in visual quality but significant increases in file size.
    
*   Use width and height parameters to serve appropriately sized images per device or viewport, avoiding delivery of oversized images to mobile clients.
    
*   Enable lazy loading in the front-end to defer off-screen image requests until the user scrolls toward them.
    
*   Avoid requesting the same asset with different parameter combinations unnecessarily, as each unique URL combination counts as a separate API request.
    
*   Use fit=bounds or fit=crop to control aspect ratio handling when resizing, preventing unexpected distortion.
    
*   Monitor Image Delivery API consumption in Product Analytics to identify high-frequency or high-bandwidth assets and target them for optimization first.
    

After applying optimization parameters, measure the before-and-after file sizes and load times. If asset sizes are reduced and API call counts decrease due to caching, the optimizations are effective.

### Assets and Asset Folders Not Visible in Newly Created Branches

After creating a new branch, assets and asset folders are not visible in the Assets section. The same assets are accessible via API and appear in the activity log.

**Root Cause**

This is a platform UI bug. Asset and folder visibility in new branches was not correctly initialized in the UI rendering layer, making them appear absent even though the data exists.

**Resolution**

1.  Wait briefly and refresh the Assets section - in some cases the visibility resolves after branch initialization completes.
    
2.  Contact Contentstack Support with the stack API key and branch name. A platform fix has been deployed for this issue.
    

After the platform fix is confirmed, create a test branch and verify assets are immediately visible.

### Unpublished Asset Still Accessible via Direct CDN URL

An asset that was unpublished (or replaced) is still accessible via its direct CDN URL.

**Root Cause**

Asset URLs in Contentstack are public by default. Unpublishing removes the asset from API responses but does not restrict direct access to the CDN-hosted file. The CDN serves the file regardless of publish status because the file was not deleted from storage.

**Resolution**

1.  To make the asset completely inaccessible: enable the Secure Public URLs (Asset Privatization) feature. Contact Contentstack Support to request enablement.
    
2.  To immediately remove access: permanently delete the asset (not just unpublish) - this removes the file from storage and the CDN will return 404 after cache TTL.
    
3.  Request a CDN cache purge from Contentstack Support to immediately invalidate the cached file.
    

After enabling Secure Public URLs or permanently deleting the asset, confirm the direct URL returns a 403 or 404.

### Permanent Asset URL Not Updating After Asset Replacement

After replacing an asset in Contentstack, the permanent URL continues to deliver the old file. The new file is visible in the asset editor.

**Root Cause**

When an asset is replaced, the Asset UID stays the same but a new File UID is generated. The CDN caches the file at the permanent URL with a standard TTL. Until the CDN cache expires or is purged, the old file is served.

**Resolution**

1.  Wait 5-10 minutes - the CDN cache should expire automatically after asset replacement.
    
2.  Perform a hard refresh in the browser (Ctrl+Shift+R) to force a fresh fetch.
    
3.  If the old file is still served after 15 minutes, contact Contentstack Support and request a targeted CDN cache purge.
    
4.  Re-publish any entries referencing the asset after replacement.
    

After the CDN cache expires or is purged, access the permanent asset URL and confirm it delivers the new file.

### ‘Image Has Size Error’ in Entry Preview During Publish

Images in entries are flagged with an ‘image has size error’ message and fail to render correctly in entry previews. The error appears specifically during publishing operations while saving entries works as expected. The issue occurs without any changes to the content model or image dimension requirements.

**Root Cause**

The issue was caused by an inconsistency in image object resolution during the publish process via UI APIs, particularly in non-main branches. When the apply\_draft option was enabled during publish, the file field object was not returned correctly, resulting in incomplete image metadata during validation. Due to the missing metadata, the system incorrectly flagged valid images with a size error and failed to render previews properly.

**Resolution**

A platform fix has been deployed to ensure proper resolution of image/file field objects and restore complete metadata during publish validation.

1.  After the fix, clear browser cache and attempt to publish an entry with images - confirm the ‘image has size error’ no longer appears and images render correctly in both preview and published views.
    
2.  If the error persists after the fix deployment, contact Contentstack Support with the affected entry UIDs, content type, and stack details.
    

After the platform fix, verify that image thumbnails display correctly in entry previews and that publishing entries with images completes without size validation errors.

### Asset List Shows ‘Not Published’ While Management API Returns Publish Details

In a specific branch (for example, dev branch), the Assets list page shows the Publish Status as ‘Not Published’ for specific assets. However, when the same assets are opened in the asset detail view or fetched via the API with include\_metadata=true, they correctly show as published.

**Root Cause**

This is a search index inconsistency in the asset list view. The search layer that powers the Assets list page had a discrepancy - it was not reflecting the correct publish status that was stored in the primary data store. The API (which reads directly from the primary store) returned the correct status, while the UI list view (which reads from the search index) showed the stale ‘Not Published’ status.

**Resolution**

The search team identified and fixed the index discrepancy. Asset publish status in the list view should now match the actual published state.

1.  If the discrepancy is still observed (asset list shows Not Published but detail view and API show published), contact Contentstack Support with the affected asset UIDs, branch name, and stack API key. Engineering can trigger a targeted index refresh.
    

After the fix, navigate to the Assets list in the affected branch and confirm the Publish Status column correctly reflects the published state for previously mismatched assets.

### Asset Thumbnails Duplicating When Scrolling in Grid View

In the Assets library’s thumbnail/grid view, assets duplicate and reappear as the user scrolls. The same asset appears multiple times in the grid, making it difficult to manage assets and identify what is actually in the library.

**Root Cause**

This was a platform-level bug introduced when a fix for missing asset pagination (assets beyond 100 not shown) was deployed. The fix for pagination inadvertently caused assets to duplicate as users scrolled in the thumbnail view. A follow-up fix was subsequently deployed to address the duplication behavior.

**Resolution**

A platform fix has been deployed. The asset library grid now loads unique assets smoothly without duplication when scrolling.

1.  After the fix, navigate to the Assets library thumbnail/grid view, scroll through the assets, and confirm each asset appears only once.
    
2.  If duplication still occurs after the fix deployment, contact Contentstack Support with the stack API key and a screen recording of the duplicating behavior.
    

After the fix, confirm the Assets grid view scrolls continuously without duplicating assets, and all assets are accessible without redundant entries.

<!-- case:00060591 status:draft synced:true bucket:"Assets & Metadata Management" -->
### High-Volume Asset Deletions Overload Purge Services

Deleting a very large number of assets in a short window may place significant load on Contentstack's purge services and slow other operations on the stack.

**Root Cause**

Submitting a high volume of asset deletions in a short period (for example, over 200,000 deletions within a few hours) generates significant load on the platform's purge services, which can affect the performance of other concurrent operations on the stack.

**Resolution**

1.  Throttle bulk asset deletions by introducing a 5–10 second delay after every 25–30 deletions to reduce load on the purge infrastructure.

2.  Use the `api_version: 3.2` request header on bulk asset publishing operations to route them through the optimized publish flow.

After throttling deletion requests, run the bulk deletion again and monitor stack performance during the process. If other operations remain responsive and no purge-related slowdowns occur, the issue is resolved. Escalate with the deletion volume, time window, and request timestamps if performance issues persist.

<!-- end:00060591 -->

<!-- case:00060690 status:draft synced:false bucket:"Assets & Metadata Management" -->
### Get Single Asset Metadata Nested Differently in CDA vs CMA

Requesting asset metadata with include_metadata=true may return a different response structure depending on whether the Get Single Asset call is made through the CMA or the CDA, breaking field mappings built against one API's shape.

**Root Cause**

The CMA returns flattened extension metadata for the Get Single Asset API, while the CDA returns the same metadata nested inside a metadata wrapper. This is expected, long-standing behavior specific to each API rather than a defect.

**Resolution**

1.  Compare the include_metadata=true response for the same asset between the CMA and the CDA to confirm which structure your integration expects.

2.  Enable the org-level flag that flattens the CDA response if your field mappings require the flattened structure used by the CMA.

3.  Alternatively, update your integration's field mapping to handle the CDA's default nested metadata wrapper.

After enabling the flag or updating the field mapping, re-request the asset metadata via the CDA and confirm the structure matches what your integration expects. If field mappings resolve correctly, the issue is resolved. Escalate with the stack API key and the affected asset UID if the response structure still does not match after enabling the flag.

<!-- end:00060690 -->

## Localization via CMA

### Fetching Taxonomy Term Names via API: Use GraphQL

CMA responses for entries return only taxonomy\_uid and term\_uid values, not the human-readable taxonomy term names. Displaying taxonomy names in front-end applications requires additional lookups.

**Root Cause**

The REST CDA and CMA return taxonomy data as UIDs rather than resolved names. Term names require a separate lookup via the Taxonomy API or can be resolved in a single query using GraphQL.

**Resolution**

Option A: GraphQL (recommended): Use GraphQL to query entries and include the taxonomy term names inline. GraphQL resolves the taxonomy\_uid and term\_uid to their display names within the same query, eliminating the need for separate lookups.

Option B: Taxonomy API: Use the CMA Taxonomy Terms endpoint to fetch term names: GET /v3/taxonomies/{taxonomy\_uid}/terms. Build a local lookup map of term\_uid to term name and use it to resolve names from entry responses.

1.  For the GraphQL approach, add the taxonomies field to the entry query and select term name and uid within it.
    
2.  Test the query in the GraphQL Explorer to confirm term names are returned alongside entry data
    

After implementing either approach, confirm that taxonomy term names are displayed correctly in the application without requiring additional API round-trips per entry.

### Syncing Entries Across Locales: Limitations and Workarounds

An attempt to sync entries from a source locale to a target locale via script fails. The Delivery API returns nested references correctly, but those references are not attached when creating or updating entries in the target locale.

**Root Cause**

Bulk locale-to-locale entry sync is not directly supported by Contentstack. When references are resolved by the Delivery API, the resolved reference objects cannot be passed back directly into the CMA create or update payload — only reference UIDs and content type UIDs should be provided. Additionally, referenced entries that belong to different content types must be independently localized before they can be referenced in the target locale entry.

**Resolution**

1.  Export entries as JSON from the source locale.
    
2.  Update the locale UIDs in the exported JSON to match the target locale.
    
3.  For each referenced entry, ensure the referenced entry also has a localized version in the target locale before importing the parent.
    
4.  Re-import the modified JSON using the CMA import endpoint with overwrite=true.
    

**Note:** This approach has limitations for complex reference hierarchies spanning multiple content types. Engage a Solutions Architect for complex cross-locale sync implementations.

After completing the export-modify-import cycle, fetch entries in the target locale and confirm referenced entries are correctly attached.

### Missing Image Data for Localized Entries in Preview GraphQL API

Localized entries (for example, fr-fr) return missing or null image data when queried through the Preview GraphQL API. The same query against the Delivery API returns the correct images.

**Root Cause**

The Preview GraphQL API does not automatically apply locale fallback behavior. If an image field is not explicitly set for the requested locale, the Preview API will not fall back to the master locale to retrieve the image, unlike the Delivery API which applies fallback behavior by default.

**Resolution**

1.  Add fallback\_locale: true to the GraphQL query parameters when querying via the Preview API.
    
2.  Alternatively, ensure that the image field is populated and published for the specific locale being queried.
    
3.  Re-run the Preview API query after adding the fallback\_locale parameter.
    

After adding fallback\_locale: true to the query, execute the Preview API request for the affected locale. If image data is now returned, the fallback behavior is active for the Preview API.

### GraphQL Fallback Locale Issues After Adding a New Language

After adding a new language to a stack, GraphQL queries for that language return unexpected or empty results. Questions also arise about whether there is an upper limit on the number of languages and whether adding more incurs additional cost.

**Root Cause**

When a new language is added to a stack, the fallback locale configuration for that language must be published before GraphQL can correctly apply fallback behavior. Without publishing the fallback locale, GraphQL may not resolve content for the new language correctly.

**Resolution**

1.  After adding the new language, publish the fallback locale for that language in the CMS.
    
2.  Verify that the fallback locale is correctly set to the intended master or parent language.
    
3.  Re-run the GraphQL query for the new language and confirm that content is returned correctly.
    

Regarding language limits: Contentstack does not enforce a strict maximum on the number of languages per stack, and adding additional languages does not incur a separate per-language cost. Confirm with your account team if specific plan limits apply.

After publishing the fallback locale, execute the GraphQL query for the new language. If content is returned correctly, the fallback locale configuration is active.

### GraphQL Returns Master Locale Content Even When fallback_locale Is Set to False

A GraphQL query includes fallback\_locale: false to prevent fallback behavior, but the API continues to return content from the master locale instead of returning null or an empty response for the requested locale.

**Root Cause**

This is expected behavior when an entry has not been localized for the target language. The fallback\_locale: false parameter instructs GraphQL not to apply locale fallback - but only when a localized version of the entry exists. If the entry has never been localized and exists only in the master locale, GraphQL returns the master locale content regardless of the fallback\_locale setting, because there is no localized version to suppress.

In other words: fallback\_locale: false prevents fallback from a non-master locale to the master locale, but it does not suppress the master locale content itself when the entry is master-only.

**Resolution**

1.  Open the affected entry in the CMS.
    
2.  Localize the entry for the specific target language by creating a locale-specific version.
    
3.  Publish the localized version to the target environment.
    
4.  Re-run the GraphQL query with fallback\_locale: false. The query will now return the localized content instead of the master locale content.
    

If no content should be returned for a locale where the entry is intentionally absent, the entry must have a localized version (even if blank or unpublished) for fallback suppression to take effect.

After localizing and publishing the entry for the target locale, re-run the query with fallback\_locale: false. If localized content is returned instead of master locale content, the entry is correctly localized.

### Non-Localizable Fields Appearing Editable Inside Multiple Group Fields in Localized Entries

Fields marked as Non-localizable in the master locale are appearing editable in a localized entry when they are nested inside a Multiple Group field. The affected fields are intended to inherit values from the master locale but display incorrectly in the localized entry editor.

**Root Cause**

This is a known platform bug affecting Non-localizable fields nested inside Group fields marked as Multiple. The non-localizable metadata is not correctly applied to each group instance in the localized entry’s internal data structure. As a result, localized entries may show those fields as editable and may not correctly display or inherit the master locale value.

**Resolution**

**Option 1 - API update:**

1.  Fetch the affected entry via the CMA: GET /v3/content\_types/{uid}/entries/{entry\_uid}?locale={locale}
    
2.  Locate the affected Group field instances in the entry JSON. For each instance within the Multiple Group, add the non\_localizable\_content: true property within the \_metadata object.
    
3.  Update the entry via the CMA: PUT /v3/content\_types/{uid}/entries/{entry\_uid}?locale={locale} with the corrected entry JSON.
    

**Option 2 - UI approach:**

1.  Identify a previous version of the entry (for example, version 2) that contains the correct \_metadata with non\_localizable\_content set correctly.
    
2.  In the CMS entry editor, use the version history dropdown to open that version.
    
3.  Create a new version from that older version. The correct non\_localizable metadata will be restored in the new version.
    

After applying either fix, open the localized entry and confirm that the Non-localizable fields inside the Multiple Group field display as read-only and show the correct master locale value.

### Error 119 - Asset UID and Content Type UID Required During REST Localization

A REST API integration for localizing entries returns Error 119: ‘Asset UID and Content Type UID are required properties’ across multiple nested fields when sending translated content back to Contentstack. A secondary error - ‘that\[typeValidator\] is not a function’ - also appears. The errors occur only for certain entries involving complex nested fields.

**Root Cause**

The integration is sending the read (response) JSON structure back to the API instead of the required write format. Two specific causes:

*   Root Cause 1: Asset reference fields in custom extension-backed fields (such as Image Preset Builder) require a specific write format. The connector sends the full read response object (including URLs, dimensions, etc.) rather than just the required uid and \_content\_type\_uid fields.
    
*   Root Cause 2: Some field values are being sent as stringified JSON instead of parsed JSON objects, causing type validation failures.
    

**Resolution**

1.  Always send data in the documented write format, not the read/response format. For asset reference fields, the write format is: { “uid”: “<asset\_uid>”, “\_content\_type\_uid”: “sys\_assets” }
    
2.  Ensure all custom field values are passed as parsed JSON objects, not as strings. Validate the payload before sending.
    
3.  For fields backed by Marketplace apps (such as Image Preset Builder), only translate permitted fields (such as asset title or description) and preserve all structural metadata unchanged.
    
4.  For unknown or extension-backed fields whose schema is unclear, treat them as non-translatable and pass the original value through unchanged to avoid validation failures.
    

After updating the integration to send write-format payloads with correctly typed values, re-run the localization workflow on a test entry and confirm Error 119 and the typeValidator error no longer appear.

### Cannot Change Master Locale from the UI - Use CLI

A customer wants to change the master locale of an existing stack (for example, from English to Portuguese Brazil). The option is not available in the Contentstack UI.

**Root Cause**

Contentstack does not support changing the master locale directly through the UI. The master locale is a foundational setting tied to the stack’s content structure, and modifying it requires a data migration approach.

**Resolution**

1.  Use the Contentstack CLI to export the stack content.
    
2.  Modify the export to define the desired language as the master locale.
    
3.  Re-import the stack with the updated locale configuration.
    
4.  For stacks where locales differ and fallback behavior is sufficient, configure fallback locales to achieve similar behavior without a full migration.
    

After completing the CLI-based migration and re-import, verify the master locale is set correctly and existing content is accessible under the new structure.

### Fallback Content Not Working for a Specific Locale

Locale fallback is not working for the en-gb locale. The API returns empty or incorrect content instead of falling back to the master locale content.

**Root Cause**

Fallback behavior applies to entries that have not been localized for the requested locale and returns the master locale version. However, if an older, outdated localized version of the entry exists for en-gb (even if blank or incorrect), it takes precedence over the fallback. Contentstack returns the localized version even if it is outdated.

**Resolution**

1.  Identify entries where the en-gb localized version is outdated or incorrect.
    
2.  Unpublish the outdated en-gb version. This removes the localized version from the delivery layer.
    
3.  After unpublishing, the CDA will fall back to the master locale content for en-gb requests.
    

After unpublishing the outdated localized version, re-query the CDA for the en-gb locale and confirm the correct master locale content is returned.

### Tags in Localized Entries Do Not Sync to Master Locale

Tags added to an entry in a localized version (for example, fr-fr) do not appear in the corresponding master locale (en) entry. Editors expect tags to be shared across locales.

**Root Cause**

The Tags field is localizable by default. Tags added in a localized entry are stored specifically for that locale and are not automatically inherited by or synced to the master locale entry. Only non-localizable fields are shared across all locales automatically.

**Resolution**

This is expected behavior. To have tags shared across locales:

1.  Add the same tags manually to each locale version where they are needed.
    
2.  Alternatively, use a non-localizable custom Select or Reference field for structured tagging that must be consistent across locales.
    

If tag consistency across locales is a business requirement, consider using a non-localizable field for the tagging use case instead of the native Tags field.

### include_fallback=false Still Returns Non-Localized Entries

When calling the All Entries API with a specific locale parameter (for example, locale=zh-it) and include\_fallback=false, entries that have not been explicitly localized for zh-it are still returned in the response.

**Root Cause**

Setting include\_fallback=false prevents the API from returning the master locale version as a fallback, but it does not exclude entries that have not been explicitly localized. An entry must have an active localized version for the requested locale in order for locale filtering to work as expected. Without explicit localization, the entry still appears in results because it exists in the stack and the fallback suppression only applies to the content fields, not to the entry’s presence in the result set.

**Resolution**

1.  To receive only entries that have been explicitly localized for a specific locale, localize each required entry for that locale in the CMS.
    
2.  Alternatively, add a query filter for the locale field in the request: query={“locale”:“zh-it”} - this restricts results to entries where the zh-it locale version exists.
    
3.  Combine the locale parameter, include\_fallback=false, and the locale field filter for the most restrictive locale-specific query.
    

After localizing the entries or adding the locale query filter, re-run the API call and confirm that only entries with explicit zh-it localization are returned.

### CDA Auto-Fallback vs Live Preview Requiring Explicit include_fallback

CDA queries for unlocalized but published entries correctly return content in the en-us locale. However, the same entry appears empty in Live Preview and Timeline mode when the en-us locale is queried without include\_fallback=true.

**Root Cause**

The CDA and Live Preview/Timeline apply fallback logic differently. The CDA assumes that published entries should return content and automatically falls back to the master locale when a localized version does not exist for the requested locale. Live Preview and Timeline do not apply this automatic fallback - they return empty results if localized content does not exist for the requested locale unless include\_fallback=true is explicitly provided in the request.

**Resolution**

1.  Always include include\_fallback=true in Live Preview and Timeline API requests when content may not be localized for every available locale.
    
2.  Alternatively, create explicit locale versions of entries for all locales used in Live Preview to avoid relying on fallback behavior.
    
3.  If consistent behavior between CDA and Live Preview is required, add include\_fallback=true to both request types.
    

After adding include\_fallback=true to Live Preview requests, verify that unlocalized entries display the master locale content in the preview mode as expected.

### “Published before localized” Error on Referenced Entries in a Locale

A locale-specific page fails to load in the production environment. Referenced entries on that page display the error Published before localized in the CMS, and the page renders blank or with missing content.

**Root Cause**

The error Published before localized appears when a referenced entry was published to an environment before it was localized. The entry exists in the master locale but has not been saved as a localized version for the target language. The CDA cannot serve the localized version because it does not exist, causing the page to fail or display incomplete content.

**Resolution**

1.  Navigate to each referenced entry showing the Published before localized error in the CMS.
    
2.  Open the entry in the target locale (for example, German or de).
    
3.  Save the entry in that locale - even without content changes - to create the localized version.
    
4.  Publish the localized version to the target environment.
    
5.  Reload the production page and confirm it now renders correctly.
    

After saving and publishing the localized version of all referenced entries, request the affected page URL. If the page loads correctly, all referenced entries are now localized and published.

### Entry Returned for the Wrong Locale - Expected Fallback Behavior

An entry of a specific content type is returned when querying the CDN API with a locale parameter (for example, locale=fr-fr), even though the entry does not exist in French. Only the base locale and a Chinese localization exist for the entry.

**Root Cause**

This is expected behavior. When a localized version of an entry does not exist for the requested locale (in this case fr-fr), Contentstack automatically falls back to the base locale and returns that entry in the response. The fallback chain goes from the requested locale to its parent locale and ultimately to the master/base locale.

**Resolution**

To fetch the entry in a specific localization (for example, Chinese), the API request must explicitly specify that locale:

1.  Update the request to use locale=zh-cn (or the correct locale code for Chinese) instead of locale=fr-fr.
    
2.  To prevent fallback entries from appearing for locales that have no content, add include\_fallback=false to the request. Note that this suppresses the fallback content fields but the entry may still appear in results - see the include\_fallback filtering guidance for full exclusion.
    
3.  Localize the entry explicitly for all required locales to have full control over what is returned per locale.
    

After updating the locale parameter to match the target localization, confirm that the API response returns the correct localized content for that language.

### ‘Copy Entry - All Languages’ Fails When Referenced Entries Not Available in All Locales

Using ‘Copy - All Languages’ fails for certain locales. The bulk task queue shows failures and copied entry is missing locale versions.

**Root Cause**

During the copy process, Contentstack attempts to create copies of the entry and all referenced entries across all selected locales. If a referenced entry or asset does not have a localized version in a target locale, the copy fails for that locale.

**Resolution**

1.  Review the bulk task queue to identify which locales failed and which referenced entries caused the failure.
    
2.  Localize the referenced entries in the failing locales before retrying the copy operation.
    
3.  Alternatively, use ‘Copy - Master Only’ first, then manually add locale versions.
    

After localizing referenced entries in the failing locales, retry ‘Copy - All Languages’ and confirm all locales are created successfully.

### Non-Localizable Field Changes in Master Not Updating in Other Locales

A non-localizable field value is updated in the master locale but does not immediately appear in localized entry views (for example, French). Editors see stale data in the localized entry.

**Root Cause**

In the reported case, Contentstack was unable to reproduce this behavior, and the customer subsequently confirmed the update had synced correctly with no further action taken - no root cause was confirmed. Client-side or browser-level caching of the localized entry view is a plausible explanation for the apparent delay, since non-localizable fields are expected to propagate immediately across all locales, but this has not been confirmed as the cause.

**Resolution**

1.  Verify the correct value is present in the CDA API response for the localized entry: GET /v3/content\_types/{uid}/entries/{entry\_uid}?locale={locale} - if the API returns the updated value, the issue is UI-side only.
    
2.  Perform a hard refresh (Ctrl+Shift+R / Cmd+Shift+R) on the localized entry view.
    
3.  If the field still shows the old value after a hard refresh, re-save the master locale entry to trigger re-propagation.
    
4.  If the stale value persists in both the UI and the API response, contact Contentstack Support with the entry UID, affected locale, and stack details for further investigation.
    

After hard-refreshing (or re-saving the master entry), confirm the non-localizable field reflects the latest master locale value in the localized entry view.

### New Block With Non-Localizable Fields Added Outside Group in Translated Entry

When adding a new block containing non-localizable fields to the master locale within a group, the block is added outside the group in the translated (localized) entry.

**Root Cause**

Once master and localized entries have diverged in block structure, the system cannot automatically map new block instances to the correct position in the localized entry’s group.

**Resolution**

1.  Use the CMA to align the block structure in the localized entry with the master locale.
    
2.  Fetch the localized entry: GET /v3/content\_types/{uid}/entries/{entry\_uid}?locale={locale}
    
3.  Compare the block array structure against the master locale entry and identify the positional mismatch.
    
4.  Update the localized entry via CMA PUT to place the new block at the correct position within the group.
    

After aligning the block structure via CMA, verify the localized entry renders correctly in both the CMS editor and the frontend.

### Boolean Default Value Not Applying to Pre-Existing Entries When Added via Global Field

A global field containing a boolean field with a default value of true is added to an existing content type. When editing pre-existing entries, the boolean field appears as false instead of the expected default value.

**Root Cause**

Default field values in Contentstack are applied only to new entries created after the field and its default are configured. Pre-existing entries already have a saved data state - even if the boolean field was absent before, the existing entries are not retroactively updated with the default value when the field is added. This applies whether the field is added directly or via a Global Field.

**Resolution**

This is expected behavior. Default values are forward-looking only. For pre-existing entries:

1.  Use a CMA script to fetch all pre-existing entries, check if the boolean field value is false or undefined, set it to true programmatically, and update each entry via PUT.
    
2.  Alternatively, if the volume is small, open each pre-existing entry in the editor and manually set the boolean field to true before saving.
    
3.  For future reference: when adding a boolean (or any) field with a default value to an existing content type, plan to run a migration script to backfill the default value for existing entries.
    

After running the backfill script, fetch a sample of pre-existing entries via the CDA and confirm the boolean field returns true.

### ‘Non-Localizable Exception’ Error in Localized Entry Despite Field Existing in Master

localized entry shows the error: ‘Non-localizable (Exception) - This field instance does not exist in the master language entry, so it is editable.’ The field does exist in the master locale entry, and saving the master locale entry does not resolve the issue.

**Root Cause**

This error occurs when a field is marked as non-localizable after data has already been added to the localized entry for that field, without the corresponding value being present in the master locale entry. The misalignment between the master and localized entry structures creates an exception state where the system cannot determine the authoritative value for the non-localizable field.

**Resolution**

1.  Unlocalize the affected entry: in the entry editor, use the Unlocalize option for the specific locale. This removes the locale-specific version.
    
2.  Recreate the localized entry from the master locale: after unlocalizing, localize the entry again by switching to the locale and making the necessary translations.
    
3.  This process ensures a clean mapping of fields across locales, realigning the entry structure with the current content type schema.
    
4.  If unlocalizing would cause significant content loss, first export the localized content via CMA as a backup before unlocalizing.
    

After unlocalizing and recreating the localized entry, confirm the ‘Non-localizable Exception’ error no longer appears and the field shows the correct master locale value.

## CMA Behavior, Limits & Miscellaneous

### Date Field Time Resets When Saving an Entry

The time value set in a date field is adjusted or reset when an entry is saved. The original time entered by the user does not persist as entered.

**Root Cause**

The date field in Contentstack follows the user's local browser timezone when saving. The time is stored in UTC on the server, and when the entry is loaded again, the time is converted back to the user's local timezone. If users in different timezones edit the same entry, they will see different local time representations of the same UTC value. This is the current intended behavior of the date field.

**Resolution**

This is a known behavior and a platform enhancement is planned to improve timezone handling. In the meantime:

1.  Standardize the timezone for all content editors by advising them to set their browser or OS timezone to UTC or a single agreed timezone.
    
2.  When storing date-time values that must be timezone-precise, store the timezone information separately as a text field alongside the date field.
    
3.  Contact Contentstack Support to stay informed about the roadmap item for improved timezone handling in date fields.
    

After standardizing the editor timezone, confirm that time values entered in the date field persist as expected when the entry is saved and reloaded.

### Exporting Entries: CLI Only, No UI Option for Content Managers

A content manager needs to export a list of entries but does not have access to the Contentstack CLI due to their role. No UI-based export option is available.

**Root Cause**

Entry export in Contentstack is currently only available via the CLI (using the cm:stacks:export command). There is no native UI option for content managers to export entries directly. The CLI requires developer-level access and familiarity with the command-line environment.

**Resolution**

1.  Coordinate with a developer on the team who has CLI access to run the export on behalf of the content manager.
    
2.  Alternatively, use the CMA GET entries endpoint programmatically to retrieve all entries and export them to a CSV or JSON file using a script. A developer can build this as a one-time or recurring export tool.
    
3.  Submit a feature request to Contentstack for a UI-based entry export option if this is a recurring need.
    

After working with a developer to run the CLI export, confirm the exported file contains the expected entries in the correct format.

### Analytics API Returns No Data or Format Error: Wrong Endpoint

The Usage Analytics API returns no results or a format error. The request appears correctly structured but consistently fails.

**Root Cause**

The Analytics API and the CMA use different base URLs. Analytics requests sent to the CMA endpoint will fail. Analytics requests must be sent to the Analytics-specific endpoint.

**Resolution**

1.  Use the correct base URL for Analytics API requests:
    
    *   EU region: [https://eu-app.contentstack.com](https://eu-app.contentstack.com)
        
    *   NA region: [https://app.contentstack.com](https://app.contentstack.com)
        
2.  Do not use the CMA base URL (api.contentstack.io for AWS NA, or eu-api.contentstack.com for AWS EU) for Analytics API calls.
    
3.  Update the endpoint in the application or Postman configuration and re-run the Analytics request.
    

After correcting the base URL, re-run the Analytics API request. If data is returned without a format error, the correct endpoint is now in use.

### Understanding Bandwidth and API Usage Metrics

There is confusion about how Subscription Usage bandwidth is calculated, what time period it covers, and whether the Top URLs counter reflects all-time data or the selected date range.

**Root Cause**

Contentstack Analytics metrics follow specific calculation and refresh rules that are not always clearly communicated:

*   Subscription Usage bandwidth: a rolling 30-day metric that updates once per day, not in real time.
    
*   Top URLs counter: applies only to the selected date range filter in the Analytics dashboard, not all-time data.
    
*   No direct API exists to query highest-bandwidth entries specifically, but the Analytics API provides URL-level data that can be filtered for this purpose.
    

**Resolution**

1.  Use the Analytics API to retrieve URL-level request data: the response can be analyzed to identify which asset or entry URLs are generating the most bandwidth.
    
2.  When reviewing Subscription Usage, allow up to 24 hours for the metric to reflect the latest data.
    
3.  When filtering Top URLs, ensure the date range is set to the desired analysis period: the counter resets with each filter change.
    

After adjusting expectations for the 24-hour refresh cycle and using the correct date range in the Analytics dashboard, confirm that the bandwidth and URL data align with the expected consumption patterns.

### Duplicate Values in Organization Invitations API: Use desc Parameter

The Organization Invitations API returns duplicate entries in the response, making it difficult to get an accurate and clean list of pending invitations.

**Root Cause**

Without the desc parameter, the API may return results in an ordering that produces duplicate entries in the paginated response due to a shifting dataset during pagination (skip-limit overlap). Adding the desc parameter stabilizes the sort order and prevents duplicates from appearing across pages.

**Resolution**

1.  Add the desc parameter to the Organization Invitations API request: GET /v3/organizations/{org\_uid}/invitations?desc=created\_at
    
2.  The desc parameter sorts results in descending order by creation date, which prevents duplicate entries from appearing across paginated responses.
    
3.  Re-run the request and confirm the invitation list no longer contains duplicate entries.
    

After adding the desc parameter, verify the response contains unique invitation entries with no duplicates.

### api.contentstack.io vs cdn.contentstack.io: When to Use Each

There is confusion about the difference between the api.contentstack.io and cdn.contentstack.io endpoints and when each should be used.

**Root Cause**

The two endpoints serve completely different purposes and should never be used interchangeably:

*   api.contentstack.io (and regional equivalents such as eu-api.contentstack.com): the Content Management API (CMA) endpoint. Used for creating, updating, deleting, and managing content, users, stacks, and settings. Requires a management token or auth token.
    
*   cdn.contentstack.io (and regional equivalents such as eu-cdn.contentstack.com): the Content Delivery API (CDA) endpoint. Used for fetching published content for delivery to end users. Requires a delivery token.
    

**Resolution**

1.  Use api.contentstack.io for all CMA operations: content creation, schema management, user management, and automation workflows.
    
2.  Use cdn.contentstack.io for all CDA operations: fetching published entries and assets for front-end delivery.
    
3.  Mixing these endpoints will result in authentication errors (using a delivery token on the CMA endpoint) or unauthorized access to unpublished data (using a management token on the CDA endpoint).
    

After updating application configurations to use the correct endpoint per operation type, confirm that CMA operations succeed with the auth/management token and CDA operations succeed with the delivery token.

### Resource Container Limited to 100 Selectable Items

The Resource Container (reference field picker) in the CMS UI is limited to selecting only 100 items. The customer needs to query and select more than 100 entries in a reference field.

**Root Cause**

The Resource Container has a default selection limit of 100 items. This limit is configurable and can be increased by Contentstack Support.

**Resolution**

1.  Contact Contentstack Support and request an increase to the Resource Container selection limit for the affected stack.
    
2.  Provide the stack API key, the content type, and the reference field UID in the request.
    
3.  After Support confirms the increase, reload the CMS and verify the Resource Container now allows selecting more than 100 items
    

After the limit is increased, open the reference field picker in the affected content type and confirm entries beyond the previous 100-item limit are selectable.

### Fetching All Taxonomies and Terms Requires Separate Calls Per Taxonomy

A customer wants to fetch all taxonomies and their associated terms from a stack in a single API call to avoid making multiple requests.

**Root Cause**

The CMA does not support fetching all taxonomies and all of their terms in a single request. Each taxonomy's terms must be retrieved individually using the taxonomy's UID. This is a current platform limitation.

**Resolution**

1.  Fetch all taxonomies using: GET /v3/taxonomies — this returns all taxonomy UIDs and names.
    
2.  For each taxonomy UID, fetch its terms: GET /v3/taxonomies/{taxonomy\_uid}/terms
    
3.  Implement a loop to iterate over all taxonomy UIDs and collect terms recursively.
    
4.  Cache the full taxonomy-term mapping at the start of the session to reduce repeated API calls.
    

After implementing the recursive fetch loop, confirm the resulting data structure contains all taxonomies and their associated terms from the stack.

### Extracting All Stack Users via CMA

A stack administrator needs a list of all users added to their stack for reporting or auditing purposes. No built-in UI export is available.

**Root Cause**

Contentstack does not provide a native UI export for stack user lists. However, all stack users can be retrieved programmatically via the CMA and the JSON response can be processed into a CSV or spreadsheet format.

**Resolution**

1.  Call GET /v3/stacks/users with the auth token and stack API key headers.
    
2.  The response returns a JSON array of all users, including their uid, email, first\_name, last\_name, and role.
    
3.  Parse the JSON response and export it to CSV using a script or a tool such as jq for command-line JSON processing.
    
4.  Refer to the CMA documentation for the Get All Users endpoint for full response schema details.
    

After running the CMA users call and parsing the response, confirm the output file contains the expected list of users with their associated roles.

### IP Whitelisting for Contentstack Endpoints

A customer needs to whitelist Contentstack IP addresses on their firewall or network to allow outbound CMA and CDA requests. The AWS North America IP list does not resolve the connectivity issue.

**Root Cause**

Contentstack operates on multiple cloud providers and regions. If a stack is hosted on Azure North America (as opposed to AWS North America), the AWS IP ranges will not be the correct ones to whitelist. The correct IP ranges depend on which cloud and region the stack is provisioned on.

**Resolution**

1.  Identify the cloud provider and region for the stack from the Contentstack dashboard URL or the stack's API endpoint URL (for example, azure-na indicates Azure North America).
    
2.  Request the appropriate IP ranges from Contentstack Support based on the identified region:
    
    *   AWS North America: api.contentstack.io / cdn.contentstack.io
        
    *   Azure North America: azure-na-api.contentstack.com / azure-na-cdn.contentstack.com
        
    *   AWS EU: eu-api.contentstack.com / eu-cdn.contentstack.com
        
    *   Azure EU: azure-eu-api.contentstack.com / azure-eu-cdn.contentstack.com
        
3.  After receiving the correct IP ranges, update the firewall whitelist and retest connectivity.
    

After updating the whitelist with the correct region's IP ranges, confirm that API calls to the Contentstack endpoint succeed without connection errors.

### Using the Audit Log API to Count Publish and Unpublish Activity Per User

An administrator needs a consolidated count of how many publish and unpublish actions were performed by each user within a specific date range. No built-in analytics view provides this breakdown.

**Root Cause**

Contentstack does not provide a pre-built analytics report for publish and unpublish counts per user. However, the Audit Log API records every content action including publish and unpublish events, with the associated user, timestamp, and action type. This data can be retrieved and aggregated to produce the required count.

**Resolution**

1.  Call the Audit Log API with a date range filter: GET /v3/audit-logs?from=<start\_date>&to=<end\_date>&limit=100, then paginate through all results using skip.
    
2.  Filter the response for entries where the action field is publish or unpublish.
    
3.  Group the filtered results by the user field to produce a per-user count.
    
4.  Export or process the aggregated data into a report format as required.
    

**Note:** The Audit Log API has a record limit per call. For large date ranges (for example, 11 months of activity), paginate through all results before aggregating. Contact Contentstack Support if the audit log history does not extend to the required start date.

After aggregating the filtered audit log data, verify the per-user publish and unpublish counts against known activity to confirm the results are accurate.

### Custom JSON Field Limit Error Despite Being Below the Configured Limit

Adding a new custom JSON field to a content type returns an error stating the maximum allowed limit for custom field extensions has been reached, even though the current field count appears to be below the configured limit of 70.

**Root Cause**

The error occurs because a plan-level configuration key that governs the custom JSON field limit was not correctly applied to the stack. The platform is enforcing a lower default limit rather than the raised limit. This is a backend configuration issue, not a content type schema error.

**Resolution**

1.  Contact Contentstack Support and report the error, providing the stack API key and the current custom JSON field count.
    
2.  Engineering will add the appropriate plan key to raise the effective limit to the configured level.
    
3.  After the fix is applied, retry adding the custom JSON field and confirm the limit error no longer appears.
    

After the plan key is applied, verify that custom JSON fields can be added up to the expected limit without errors.

### include[] Parameter on CMA Single Entry Endpoint - Supported; Queried Content Type Limit

A developer asks whether include\[\] is supported on the CMA single-entry fetch endpoint (GET /v3/content\_types/{uid}/entries/{uid}). They also encounter a MAX\_QUERIED\_CONTENT\_TYPE\_LIMIT\_EXCEEDED error. Documentation states the default limit is 3, but the error shows 6.

**Root Cause**

The include\[\] parameter is supported on the CMA single-entry endpoint, though it is primarily documented for the CDA. The MAX\_QUERIED\_CONTENT\_TYPE\_LIMIT\_EXCEEDED error is triggered when the number of distinct content types being resolved (across include paths and the base content type) exceeds the configured limit. The default limit in public documentation is 3, but specific organizations may have a higher limit applied (such as 6) based on their plan or support request.

**Resolution**

1.  include\[\] is confirmed safe and supported on: GET /v3/content\_types/{uid}/entries/{uid}?include\[\]=field\_uid
    
2.  To avoid MAX\_QUERIED\_CONTENT\_TYPE\_LIMIT\_EXCEEDED, reduce the number of distinct content types being resolved across include paths. Fetch references from a limited set of content types per call.
    
3.  If a higher queried content type limit is needed, contact Contentstack Support to request an increase. Provide the current error value shown in the response (for example, 6) and the required limit.
    

After reducing include paths to stay within the content type limit, verify the response returns all required reference data without the limit exceeded error.

### CDA Timeout Behavior - No Single Published Timeout Value

An application needs to configure client-side timeouts and fallbacks for CDA requests. The question is: what is the standard timeout for Contentstack CDA calls?

**Root Cause**

Contentstack does not publish a single fixed timeout value for all CDA calls. The effective timeout varies based on the endpoint type (REST vs GraphQL vs Images API), query complexity (reference depth, result set size), CDN region, and current infrastructure load. A simple entry fetch may respond in under 100ms; a deeply nested reference query under load may take several seconds.

**Resolution**

Configure client-side timeouts based on the specific endpoint and use case:

1.  For simple GET entry or asset calls: set a timeout of 5–8 seconds. These calls should respond quickly and a longer timeout indicates a problem worth surfacing.
    
2.  For complex reference-heavy queries: set a timeout of 10–15 seconds to allow for origin processing under normal load.
    
3.  For GraphQL queries with large result sets: set a timeout of 15–30 seconds for complex queries.
    
4.  Always pair timeouts with retry logic and fallback behavior (for example, serve cached content or a graceful degraded state) so a single timed-out request does not cause a page load failure.
    
5.  Monitor p99 response times for each endpoint type over time and adjust timeouts based on observed baseline performance in the specific region.
    

After configuring endpoint-appropriate timeouts and fallback behavior, confirm that requests exceeding the timeout fail gracefully and trigger the fallback rather than hanging indefinitely.

### Secondary Sort Not Supported in the Content Delivery API

A customer wants to sort entries by a date field in descending order and use created\_at as a secondary sort field for entries with the same date value. The CDA does not appear to support multi-field sorting.

**Root Cause**

The Contentstack Content Delivery API supports only a single sort parameter per request. Multi-parameter (secondary) sorting is not supported. When entries share the same value for the primary sort field, their relative order is not deterministic.

**Resolution**

1.  Fetch entries with the primary sort applied (for example, asc\_date or desc\_date) as usual.
    
2.  Apply secondary sorting client-side after retrieving the results. Sort the response array by the primary field, and for entries with equal primary values, sort by created\_at as a tiebreaker.
    
3.  For use cases that require server-side multi-sort, consider using GraphQL where the orderBy argument may offer more flexibility in certain scenarios.
    

After implementing client-side secondary sorting, confirm the entry list is correctly ordered by date (primary) and created\_at (secondary) for entries sharing the same date.

### No Historical Publish Status Per Entry Version

A user wants to know, for a given entry, whether each past version was published and to which environment. They expect a version-by-version publish history.

**Root Cause**

Contentstack does not retain a per-version publish history for entries. The include\_publish\_details flag returns the current publish state of the latest version only. The /versions endpoint lists all version numbers and their creation timestamps, but does not include publish status for each individual version.

**Resolution**

There is no API endpoint that provides per-version publish history. Available alternatives:

1.  Use the Audit Log API (GET /v3/audit-logs) to retrieve publish and unpublish events for specific entries. Audit log events include the entry UID, timestamp, action type, environment, and user. Cross-reference with version numbers to approximate a publish history.
    
2.  Configure webhooks to fire on publish and unpublish events. Capture the payload (which includes the entry UID, version, environment, and timestamp) in an external system to build a persistent per-version publish history.
    
3.  Use include\_publish\_details=true in the CDA request to retrieve the current publish status for the current version.
    

For teams that need per-version publish tracking, the webhook-based approach provides the most complete ongoing record. The audit log API is useful for reconstructing historical data from existing records.

### Select Field Returns Value in API - Not Display Label (Key)

A Select field configured with key-value pairs (for example, display label ‘New York’, stored value ‘NY’) returns only the value (‘NY’) in the Delivery API response. The frontend needs to display the human-readable label.

**Root Cause**

This is expected behavior. In Contentstack, when a Select field uses key-value pairs, the CMS editor UI displays the key (the human-readable label) for editorial ease. However, the API response returns the value (the stored string) - not the label. This design allows the stored value to be short, consistent, and suitable for programmatic use, while the label is for display purposes only.

**Resolution**

1.  Fetch the content type schema via the CMA: GET /v3/content\_types/{uid} and retrieve the enum options array for the Select field, which contains both key and value pairs.
    
2.  Build a lookup map on the frontend: { ‘NY’: ‘New York’, ‘CA’: ‘California’, … }
    
3.  Use the lookup map to resolve the value returned by the API to the corresponding display label before rendering.
    
4.  Cache the content type schema lookup map at application start to avoid fetching it on every request.
    

After building the lookup map, verify that API values are correctly resolved to their display labels in the application UI.

**Note:** The Sync API follows the same behavior. When consuming the Sync API (via stack.sync() in the SDK), multi-select Enum fields with advanced key-value choices also return only the raw value string(s), not the full key-value pair object. For example, a field with choices { key: ‘Growth Seller’, value: ‘GROWTH’ } returns ‘GROWTH’ (single select) or \[‘GROWTH’, ‘STARTER’\] (multi-select) in the sync payload. There is no SDK flag or include option to retrieve the display label alongside the value in sync responses. Use the same content type schema lookup map approach to resolve values to display labels in the sync consumer.

### referenced_in Metadata Not Exposed via the Content Delivery API

A request is made to expose the referenced\_in metadata via the CDA to enable programmatic identification of unused or orphaned entries for content audit purposes.

**Root Cause**

The referenced\_in metadata is an internal Contentstack data structure that tracks which entries reference a given entry. It is available via the CMS UI (under an entry’s References tab) but is not exposed through the Content Delivery API. This is an intentional design decision - the CDA is optimized for delivering published content to end users and does not expose internal content management metadata.

**Resolution**

The referenced\_in data is not available via the CDA. Available alternatives for content audit use cases:

1.  Use the Content Management API (CMA) - the CMA can return referenced\_in data for entries via: GET /v3/content\_types/{uid}/entries/{entry\_uid}?include\_referenced\_in=true (check current documentation for exact parameter support).
    
2.  Build a custom reference graph by fetching all entries via the CMA and analyzing the reference fields in each entry’s data to determine which entries reference which others.
    
3.  Use the Contentstack Audit Log to track reference creation and removal events over time.
    

After implementing a CMA-based reference graph or using the include\_referenced\_in parameter, verify that unused entries can be identified programmatically for content audit workflows.

### Taxonomy Must Be Published to Environments for CDA Taxonomy Queries

After the Taxonomy Publishing feature rollout, taxonomy-based delivery queries return no results or fail to filter correctly, even though taxonomy terms are correctly assigned to entries.

**Root Cause**

The Taxonomy Publishing feature makes taxonomy data environment-specific in the CDA. After the rollout, taxonomy terms and their hierarchies must be explicitly published to each environment for taxonomy-based CDA queries to function. Previously, taxonomies were available in the CDA without environment-specific publishing.

**Resolution**

1.  Navigate to the Taxonomies section in the Contentstack dashboard.
    
2.  Publish each taxonomy and its terms to the target environments where they need to be accessible via the CDA.
    
3.  After publishing, re-run taxonomy-based CDA queries and confirm results are returned correctly.
    
4.  Include taxonomy publishing in the content operations workflow - whenever a new taxonomy or term is created, publish it to all relevant environments.
    

After publishing taxonomies to the target environments, confirm that CDA taxonomy queries return the expected filtered results.

### Increasing the x-cs-variant-uid Header Limit for Variant-Heavy Migrations

An application managing a large number of personalization experiences (for example, 200+ variant experiences) needs to pass multiple variant UIDs in the x-cs-variant-uid header per request. The default header limit (typically 3) forces multiple API calls per page load and causes functional issues because variant resolution depends on header ordering rather than the actual entry configuration.

**Root Cause**

The x-cs-variant-uid header has a default limit on the number of variant UIDs that can be passed per request. For organizations managing large-scale personalization migrations with many concurrent variant experiences, this default limit is too low and forces inefficient multi-call patterns.

**Resolution**

1.  Contact Contentstack Support and request an increase to the x-cs-variant-uid header limit for the organization. Provide the number of experiences that need to be supported concurrently and the stack API key.
    
2.  Engineering will evaluate and apply a higher limit at the organization level to accommodate the migration or production use case.
    
3.  While awaiting the limit increase, implement a prioritization strategy: identify which variant UIDs are most critical per request and include only those within the current limit, fetching secondary variants in a subsequent request if needed.
    

After the limit is increased, re-test variant resolution across the full set of experiences and confirm that variant content is correctly resolved without requiring multiple API calls.

### Fetching Entries by Custom Slug - Limitations and Correct Approach

A customer wants to set up custom slugs for entries and fetch content using those slugs directly, without relying on query parameters. They want a URL-based lookup that returns a unique entry.

**Root Cause**

Fetching entries solely by a URL slug without query parameters is not directly supported because a single URL may correspond to an entry that references multiple other entries through reference fields, modular blocks, or other structures. It is not possible to deterministically derive a unique entry UID and content type UID from a URL alone in all cases.

**Resolution**

1.  Use the URL field in Contentstack entries to store the slug value. Each entry’s URL field serves as a unique path identifier.
    
2.  Query entries by their URL field value using the query JSON parameter: GET /v3/content\_types/{uid}/entries?query={“url”:“/my-slug”}&environment=production
    
3.  Ensure the URL field value is unique across entries within the content type to guarantee a single matching result.
    
4.  For multi-locale setups, include the locale parameter alongside the URL query to retrieve the correct locale version: &locale=fr-fr
    
5.  If slugs must be routable across multiple content types (for example, a catch-all routing pattern), query each relevant content type sequentially until a match is found, or build a routing table at build time.
    

After implementing URL field queries, confirm that fetching a known URL slug returns the expected single entry without requiring the entry UID.

### Enabling ‘Show as Tab’ Feature for Groups and Global Fields

The ‘Show as Tab’ feature is not available in stack settings. Customers need this to organize complex content types.

**Root Cause**

‘Show as Tab’ is a configurable feature that must be enabled at the organization level by Contentstack. It is not enabled by default.

**Resolution**

1.  Contact Contentstack Support and request enablement of the ‘Show as Tab’ feature for the organization. Provide the Organization ID.
    
2.  After enablement, navigate to the Group or Global Field configuration in the Content Type Builder and confirm the ‘Show as Tab’ toggle is now available.
    

After the feature is enabled, configure the desired Group or Global Field to show as a tab and verify it renders as a separate tab in the entry editor.

### Cannot Delete a Parent Branch Without Deleting Child Branches

A team attempts to delete a parent branch but receives an error. Child branches forked from the parent still exist.

**Root Cause**

Contentstack does not support deleting a parent branch while child branches exist. Child branches inherit content versions and dependencies from their parent. Deleting the parent independently would create orphaned child branches.

**Resolution**

1.  Delete all child branches first before attempting to delete the parent.
    
2.  Navigate to Settings > Branches, identify all branches forked from the parent, and delete them in sequence.
    
3.  If child branches contain content that should be preserved, merge relevant changes back to the main branch first.
    

After deleting all child branches, confirm the parent branch can be deleted without errors.

### Modular Block Max Limit Appears Bypassed via the ‘+’ Icon

Users can add block instances beyond the configured maximum by clicking ‘+’. The limit does not appear to be enforced.

**Root Cause**

This is expected behavior. Empty block instances added beyond the limit do not count because empty blocks are not saved. The extra empty instances will be discarded when the entry is saved - only blocks with at least one populated field are saved and counted.

**Resolution**

No action is required. The maximum limit is correctly enforced at save time. Empty instances beyond the limit are discarded on save. This is expected behavior.

### Stack API Key Security - Cannot Be Rotated or Changed

A customer wants to rotate or change the Stack API key following a security concern. They cannot find a rotation option.

**Root Cause**

The Stack API key is a public identifier for the stack. Unlike tokens, it is not a sensitive credential on its own - it identifies the stack but does not authorize write access without an accompanying token. The API key cannot be rotated via the UI or internally.

**Resolution**

*   The Stack API key is commonly included in public-facing code and is not a secret.
    
*   Delivery tokens and management tokens provide actual authorization - rotate these immediately if exposed.
    

1.  If a management token or delivery token was exposed (not just the API key), rotate those immediately via Settings > Tokens.
    
2.  If the API key must change for compliance reasons, clone the stack (which creates a new stack with a new API key) and migrate traffic to the new stack.
    

After rotating any exposed tokens, confirm the old tokens return authentication errors and the application functions correctly with new tokens.

### Content Type Limit Counts Include All Branches

The dashboard reports a much higher content type count than the actual number of unique content types managed. The organization is approaching the plan limit.

**Root Cause**

Content type limits are counted across all branches. Each branch maintains its own copy. A stack with 50 unique content types across 6 branches counts as 300 against the limit.

**Resolution**

1.  Review active branches and delete any development or test branches that are no longer needed.
    
2.  Keep branch count minimal to control the content type total.
    
3.  Contact your Customer Success Manager to clarify how the plan’s content type limit is calculated.
    

After deleting unused branches, verify the content type count in the dashboard decreases proportionally.

### URL Slug Accented Characters Replaced With Hyphens Instead of Transliteration

When generating URL slugs from titles containing accented characters (ñ, ä, ó), Contentstack removes the character and inserts a hyphen instead of converting to the non-accented equivalent.

**Root Cause**

The URL slug generator removes characters outside the standard ASCII range and inserts a separator. It does not apply automatic transliteration. This is the platform’s default behavior.

**Resolution**

1.  Implement transliteration in the URL generation logic on the frontend or in a webhook/automation. Use a library such as slugify with unicode: true (Node.js) or Python’s unidecode library.
    
2.  For existing entries with incorrect slugs, use a CMA script to fetch entries, apply transliteration to URL field values, and update entries programmatically.
    
3.  Consider a custom App SDK extension on the URL field that automatically applies transliteration as the user types the entry title.
    

After implementing transliteration, verify that new entries with accented characters generate slugs with correctly transliterated ASCII equivalents.

<!-- case:00060883 status:draft synced:false bucket:"CMA Behavior, Limits & Miscellaneous" -->
### Bulk Task Queue Jobs Stuck Behind One Stalled Job

Bulk Task Queue jobs, such as branch-creation jobs, may appear stuck in a Waiting state across multiple stacks, blocking further queue processing.

**Root Cause**

Bulk Task Queue jobs process sequentially per organization. When one job stalls on the backend, all subsequent queued jobs remain blocked and show as Waiting in the UI, even though they are not individually broken.

**Resolution**

1.  Retrieve all incomplete jobs for the organization using GET /v3/organizations/{org_uid}/jobs?completed=false with an org owner or admin authtoken to identify which job is stalled.

2.  Identify the stalled job from the response.

3.  Retry the stalled job using POST /v3/organizations/{org_uid}/jobs/{job_id}/retry with an org owner or admin authtoken.

4.  Confirm the queue clears and the remaining jobs process normally.

Note that no delete-job API exists; retry is the only supported action for a stuck job.

After retrying the stalled job, check the Bulk Task Queue again and confirm the remaining jobs move out of the Waiting state and complete. If the queue clears and new jobs process normally, the issue is resolved. Escalate with the organization UID and job ID if the queue remains stuck after a retry.

<!-- end:00060883 -->

<!-- case:00060593 status:draft synced:true bucket:"CMA Behavior, Limits & Miscellaneous" -->
### Recovering Accidentally Deleted Entries via Trash

Deleting published or unpublished entries across multiple stacks may result in permanent-feeling content loss when no stack-wide point-in-time restore is available to recover them automatically.

**Root Cause**

Accidental deletion removes entries from the live stack, and Contentstack does not offer a stack-wide point-in-time restore. The Publish Queue and Audit Log also do not retain enough history to confirm which entry version was live in each environment prior to the deletion.

**Resolution**

1.  Open Trash in the affected stack and restore the deleted entries.

2.  Republish the latest available version of each restored entry to the required environments.

3.  If entries were removed in bulk and the pre-deletion state can't be confirmed, treat Publish Queue and Audit Log history as unreliable beyond a limited window when reconstructing what was live.

After restoring entries from Trash and republishing them, verify the previously deleted content is live again in the required environments. If the content matches what was published before the deletion, the issue is resolved. Escalate with the affected stack UID and the approximate deletion timeframe if entries cannot be restored from Trash.

<!-- end:00060593 -->

## AI Assistant & Polaris Features

<!-- case:00060830 status:draft synced:true bucket:"AI Assistant & Polaris Features" -->
### Polaris Fails to Load Despite AI Credits Enabled

Polaris may fail to load and display an error prompt even when AI Credits and Polaris are enabled at the organization level.

**Root Cause**

The failure originated from a backend provisioning issue on Contentstack's side rather than a client-side or configuration problem. The specific defect was identified and corrected internally by the Contentstack engineering team; the source case notes do not detail the exact backend mechanism beyond confirming it was unrelated to org-level AI Credits or Polaris configuration.

**Resolution**

1.  Confirm that AI Credits and Polaris are enabled at the organization level in account settings.
2.  Note whether the load error clears after clicking Retry or persists across repeated attempts, including in an incognito or private browsing window.
3.  Capture the browser console errors shown at the time of failure.
4.  Contact Contentstack Support with the captured console errors and confirmation that AI Credits and Polaris are enabled at the org level, so the backend provisioning issue can be corrected.

After Contentstack Support confirms the backend provisioning issue has been corrected, reload Polaris. If it loads successfully without the error prompt, the issue is resolved. Escalate with updated console errors if it persists after the fix is applied.

<!-- end:00060830 -->

<!-- case:00060779 status:draft synced:false bucket:"AI Assistant & Polaris Features" -->
### Organization Admins Unable to Access AI Settings

Accessing Administration → AI Settings may be blocked for a user even when that user holds Organization Admin privileges.

**Root Cause**

The access failure was caused by a permissions-handling defect on Contentstack's backend rather than a stack-level configuration issue. Contentstack engineering identified and corrected the defect in production.

**Resolution**

1.  Confirm the affected user holds Organization Admin privileges and is still unable to access or manage Administration → AI Settings.

2.  Toggle an AI setting off and on to confirm existing AI functionality behaves as expected, since access alone does not guarantee full functional verification.

3.  Contact Contentstack Support with the organization UID and a description of the access failure if the issue persists after the fix.

After confirming the permissions fix is applied, reload Administration → AI Settings as an Organization Admin. If the page loads and settings can be managed, the issue is resolved. Escalate with the organization UID if access remains blocked.

<!-- end:00060779 -->