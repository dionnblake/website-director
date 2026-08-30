# Content Model and Editorial Architecture

<!-- FRAMEWORK_VERSION: 2.13.0 -->

**Project:** `[PROJECT_NAME]`
**Phase:** 6.25
**Gate:** `[CONTENT_OPERATIONS_READY]`
**State:** `content_ops.complete`
**Owner lock count:** five exactly; this document creates no content lock

Use this document with [`content-model.json`](content-model.json). The JSON
file is the machine-readable contract; this file records the human decisions
and evidence needed to complete it. Do not duplicate the V2.5 client editor
guide, training plan, backup/restore procedure, cost register, or handoff
acceptance record.

## CMS Requirement

- `CMS_REQUIRED`: `[true | false | UNKNOWN]`
- `CMS_CLASS`: `[NO_CMS_REQUIRED | STATIC_STRUCTURED_CONTENT | FILE_BASED_CMS | HEADLESS_CMS | TRADITIONAL_CMS | DATABASE_BACKED_CONTENT | ECOMMERCE_CATALOG | APPLICATION_DATA | HYBRID]`
- Assessment factors: volume, update frequency, editors, technical level,
  relationships, preview, scheduling, channels, localization, SEO, media,
  workflow, and portability.
- Rationale and unresolved owner questions: `[RECORD FACTS]`

## Content Inventory

| Route or surface | Content purpose | Current source | Volume | Update frequency | Editor | Repeatable | Relationships | SEO/media/evidence risk | Migration status |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| `[ROUTE]` | `[PURPOSE]` | `[SOURCE]` | `[COUNT/UNKNOWN]` | `[FREQUENCY]` | `[ROLE]` | `[YES/NO]` | `[TYPES]` | `[RISK]` | `[STATUS]` |

Activate only content types required by this project. Repeated entities must
not be maintained as individually duplicated markup.

## Content Types

For every type record `TYPE_ID`, `NAME`, `PURPOSE`, `ROUTES_USED`, `FIELDS`,
`REQUIRED_FIELDS`, `OPTIONAL_FIELDS`, `RELATIONSHIPS`, `SEO_FIELDS`,
`MEDIA_FIELDS`, `PROVENANCE_FIELDS`, `EDITORIAL_STATUS`, `SLUG_POLICY`, and
`ARCHIVE_POLICY`.

| TYPE_ID | Name | Purpose | Routes used | Editorial status | Slug policy | Archive policy |
| --- | --- | --- | --- | --- | --- | --- |
| `[TYPE_ID]` | `[NAME]` | `[SUBJECT ENTITY]` | `[ROUTES]` | `[STATES]` | `[POLICY]` | `[POLICY]` |

## Content Ownership

Every activated type records an explicit `CONTENT_OWNER`. Use an existing
person, client, team, or project role; do not infer an organization that has
not been confirmed. Keep long-term client ownership, training, maintenance,
and handoff acceptance in the V2.5 handoff authority.

## Field Definitions

For every field record `FIELD_ID`, `LABEL`, `TYPE`, `REQUIRED`, `VALIDATION`,
`DEFAULT`, `EDITOR_HELP`, `CHARACTER_LIMIT`, `RELATIONSHIP`, `LOCALIZABLE`,
`SEO_ROLE`, and `PROVENANCE_ROLE`.

| FIELD_ID | Label | Type | Required | Validation | Default | Editor help | Character limit | Relationship | Localizable | SEO role | Provenance role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `[FIELD_ID]` | `[LABEL]` | `[TYPE]` | `[true/false]` | `[RULE]` | `[VALUE/NULL]` | `[GUIDANCE]` | `[LIMIT/NULL]` | `[TARGET/NULL]` | `[true/false]` | `[ROLE]` | `[ROLE]` |

Use semantic names such as `headline`, `summary`, `body`, `image`, `category`,
`author`, and `call_to_action`. Never use presentation fields such as
`left_column_heading_blue`, `third_card_image`, `desktop_margin_top`, or
`hero_text_line_2_blue`.

## Relationships

Record source field, target type, target field, cardinality, validation,
ownership, and delete behavior for every relationship. Unknown type or field
references block readiness.

## Taxonomies

Record only taxonomies needed for navigation, filtering, editorial consistency,
or a documented SEO purpose. Include stable ID, label, allowed values,
ownership, and archive behavior. Do not create presentation-only taxonomy.

## Editable Surfaces

Classify each surface as `OWNER_EDITABLE`, `EDITOR_EDITABLE`, `ADMIN_ONLY`,
`DEVELOPER_CONTROLLED`, `SYSTEM_GENERATED`, or `LOCKED_BRAND_ELEMENT`.
Analytics event identifiers, structured-data schema, security headers, design
tokens, canonical lock state, and other system contracts are not editor fields.

## Roles/Permissions

Roles explicitly declare `CAN_EDIT`, `CAN_REVIEW`, `CAN_PUBLISH`,
`CAN_ARCHIVE`, and `CAN_DELETE`. Editing does not imply publishing. Agents may
generate drafts but may not hold autonomous `CAN_PUBLISH` authority.

## Lifecycle

Use `DRAFT`, `IN_REVIEW`, `APPROVED`, `SCHEDULED`, `PUBLISHED`, and `ARCHIVED`
as applicable. A simple static site may explicitly reduce this to
`DRAFT`/`PUBLISHED`. Archive, unpublish, and delete remain distinct actions.

## Publishing Workflow

Describe draft creation, review, approval, publication, unpublication,
archive, deletion, rollback, and failure handling. Agent-generated content
must follow `AGENT_GENERATED_CONTENT -> DRAFT -> human review -> PUBLISHED`.
No workflow in this document authorizes a production publish action.

## Preview

Record preview route, renderer, data source, access boundary, and validation
behavior. Preview must use the real route composition and design system. A raw
JSON response is not a visual preview.

## Scheduling

If scheduling is needed, record `SCHEDULED_AT`, `TIMEZONE`,
`PUBLISHING_SYSTEM`, and `FAILURE_BEHAVIOR`. This capability specifies the
architecture only; it does not create a scheduler, queue, webhook, or provider
job.

## SEO Fields

Record applicable `SEO_TITLE`, `META_DESCRIPTION`, `CANONICAL_OVERRIDE`,
`OG_TITLE`, `OG_DESCRIPTION`, `OG_IMAGE`, `INDEXABILITY`, and bounded
`STRUCTURED_DATA_INPUTS`. Consume the canonical SEO strategy. Reject local or
staging canonicals, accidental noindex, duplicate titles, fabricated ratings,
unsupported claims, and editor-authored structured-data schema.

## Media References

Record `MEDIA_ID`, `ASSET_ID`, `PROVENANCE_REF`, `ALT_TEXT`, `CAPTION`, and
`CROP_POLICY` as applicable. Asset Director owns production readiness,
Evidence Provenance owns origin/rights/attribution/hash identity, and
Accessibility owns alt semantics. Research and inspiration images remain
`REFERENCE_ONLY`.

## Evidence/Provenance References

High-risk factual, quantitative, health, financial, certification, affiliate,
and comparable claims must carry a resolvable V2.12 evidence/provenance
reference. This document links the ledger; it does not recreate or replace
[`EVIDENCE-PROVENANCE-PROTOCOL.md`](../EVIDENCE-PROVENANCE-PROTOCOL.md).

## Slug/Redirect Rules

Slugs are lowercase kebab-case, unique, normalized, and checked against
reserved routes. A published or archived slug change requires a durable 301
redirect from the historical URL to the new URL. Nested route policy and
historical URL retention are explicit.

## Archive/Delete Rules

Record who may archive, unpublish, or delete; whether inbound links are
redirected; how media and evidence references are retained; and how restore is
handled. Delete is not archive. The V2.5 backup/restore and handoff records
remain the operational authority.

## Portability

Record `EXPORT_FORMAT`, `MEDIA_EXPORT`, `RELATIONSHIP_EXPORT`, `SLUG_EXPORT`,
and `PROVENANCE_EXPORT`. If a provider lacks export capability, record the
lock-in risk, owner acceptance, and exit plan. Do not claim portability without
an inspectable export path.

## Migration

For each migrated record capture `SOURCE_URL`, `SOURCE_TYPE`, `TARGET_TYPE`,
`TARGET_SLUG`, `MIGRATION_STATUS`, `REDIRECT_REQUIRED`, `ASSET_REFS`,
`PROVENANCE_REFS`, and `SEO_NOTES`. Unknown mappings, missing assets, or
unresolved provenance remain blocked.

## Known Constraints

Record provider, editor, preview, runtime, deployment, security, cost,
portability, content-volume, and accessibility constraints as facts. Mark
unknown values explicitly; do not turn assumptions into requirements.

## Exceptions

Every exception records `applied: true`, owner, scope, reason, expiry or
review date, and compensating control. An exception never grants permission to
break the five owner-lock invariant, publish agent content autonomously,
expose secrets, or bypass evidence, SEO, security, accessibility, analytics,
or redirect controls.

## Handoff Requirements

Transfer this model, the type/field inventory, roles, lifecycle, preview and
scheduling policy, CMS decision, portability and migration records, publishing
boundary, limitations, and unresolved owner decisions into the existing V2.5
handoff package. Do not duplicate the V2.5 editor guide, training plan,
backup/restore runbook, environment inventory, cost register, or acceptance
authority.

## Readiness Evidence

The readiness gate is `[CONTENT_OPERATIONS_READY]` and the only state flag is
`content_ops.complete`. Run `python tests/test_v2_13_content_operations.py`
and the registered framework suite. No new owner lock, provider installation,
production publish, deployment, network request, or frozen-project mutation
is permitted by this template.
