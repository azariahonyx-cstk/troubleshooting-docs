---
title: "Rich Text Editor Reformats HTML Structure on Direct Edit"
slug: "rich-text-editor-reformats-html-structure-on-direct-edit"
pod: "CMS - UI"
section: "Rich Text Editor"
order: 1
meta_title: "Troubleshooting Rich Text Editor | Contentstack"
meta_description: "Common issues with the Contentstack Rich Text Editor, including HTML reformatting, structure changes on direct edits, and content rendering problems."
status: "published-in-drive"
source_case_id: null
contentstack_entry_uid: null
migrated_from: "CMS - UI (main, Jun 21 2026)"
migrated_on: "2026-07-08"
---

# Rich Text Editor Reformats HTML Structure on Direct Edit

Editing content directly within the Rich Text Editor field may alter the HTML structure, including rearranging tags, inserting additional whitespace characters (such as &nbsp;), or modifying the nesting of elements like <strong> and <sup> tags.

## Root cause

The Rich Text Editor applies internal HTML normalization when content is edited directly within the editor. This normalization process restructures HTML to conform to the editor's internal model, which can differ from the original markup. Pasting content from an external text editor typically bypasses this normalization, which is why pasted content tends to retain its original structure.

## Resolution

1. Review the Contentstack Rich Text Editor documentation to understand which HTML constructs are supported and how the editor processes formatting.
2. Avoid editing complex or custom HTML structures directly in the RTE's visual or source mode when precise markup preservation is required.
3. If exact HTML output is critical, consider using a plain text field or a JSON RTE field instead, which provides more control over the content structure.
4. If content must be entered via the RTE, use the paste-from-external-editor workflow, as this approach better preserves original formatting.

## Verification

After completing these steps, review the rendered HTML output to confirm the structure matches expectations. If the editor continues to reformat content in unexpected ways, escalate with the specific HTML snippet (before and after), the field type configuration, and the browser version.

## See also

Rich Text Editor documentation — https://www.contentstack.com/docs/developers/create-content-types/rich-text-editor
