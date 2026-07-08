# troubleshooting-docs

Source of truth for Contentstack customer-facing troubleshooting articles, generated from resolved Salesforce support cases. Replaces the Google Drive folder as the storage layer of the documentation intelligence pipeline (Jira: TD-5299).

## Pipeline

```
Salesforce case closed
  -> #feed-salesforce-docs (Slack)
  -> Claude article generator (filter, dedupe, draft)
  -> branch + PR to this repo            <- you are here (Phase 1)
  -> GitHub Actions validation (validate.yml)
  -> human review + merge = publish gate
  -> Contentstack Management API publish (publish.yml, Phase 2)
  -> Jira TD review ticket + reviewer feedback loop (Phase 3)
  -> manifest layer feeds MCP / RAG / deflection analytics (Phase 4)
```

## Structure

```
docs/{pod}/{section}/{NN}-{slug}.md              article (YAML frontmatter + body)
docs/{pod}/{section}/{NN}-{slug}.manifest.json   AI manifest (keywords, traceability, entry UID)
schemas/manifest.schema.json                     manifest schema
scripts/validate_articles.py                     CI validator (stdlib only)
scripts/publish_to_contentstack.py               CMA publisher (stdlib only)
scripts/migrate_from_gdocs.py                    one-time Drive migration (already run)
.github/workflows/validate.yml                   runs on every PR
.github/workflows/publish.yml                    runs on merge to main (dry-run by default)
```

## Article format

Frontmatter keys: `title, slug, pod, section, order, meta_title, meta_description, status, source_case_id, contentstack_entry_uid`. Body sections: problem statement, `## Root cause`, `## Resolution` (numbered steps), `## Verification`, optional `## See also`.

Status lifecycle: `draft -> in-review -> approved -> published`. Migrated articles carry `published-in-drive` until their Contentstack entry is created.

## For the article generator routine

Change only the output target: instead of writing Google Docs, for each run create branch `articles/run-YYYY-MM-DD`, write one `.md` + `.manifest.json` per validated case using the format above (set `status: "draft"`, fill `source_case_id`), commit, and open a single PR titled `Articles: run YYYY-MM-DD (<n> articles)`. All existing filtering, dedup, and rejection rules stay unchanged.

## Going live with publishing (Phase 2 checklist)

1. Add repo secrets `CS_API_KEY` and `CS_MGMT_TOKEN` (management token with entry create/update/publish scope on the docs stack).
2. Confirm the FAQ content type UID and field mapping in `scripts/publish_to_contentstack.py` (`build_entry`).
3. Optionally set repo variables `CS_REGION_HOST`, `CS_CONTENT_TYPE`, `CS_ENVIRONMENT`.
4. Set repo variable `PUBLISH_LIVE=1`. Until then every merge runs in dry-run mode and logs the payloads it would send.

## Provenance

42 articles migrated on 2026-07-08 from the Drive folder (mains + "Additions" side-docs merged). Known review item: AUTH article 07 and General/Authentication article 03 describe the same forced-logout 502 incident from two different case angles — candidates for consolidation.
