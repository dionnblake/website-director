# CMS Decision Record

<!-- FRAMEWORK_VERSION: 2.13.0 -->

**Project:** `[PROJECT_NAME]`
**Phase:** 6.25
**Gate:** `[CONTENT_OPERATIONS_READY]`
**Decision status:** `[DRAFT | REVIEW | ACCEPTED | BLOCKED]`

This is a vendor-neutral decision record. Complete the content model and
necessity assessment before selecting a provider. The V2.5 handoff protocol
owns long-term client operations, cost records, training, backup/restore, and
acceptance; this record supplies its architecture inputs.

## Need/No-Need Assessment

- `CMS_REQUIRED`: `[true | false | UNKNOWN]`
- `CMS_CLASS`: `[NO_CMS_REQUIRED | STATIC_STRUCTURED_CONTENT | FILE_BASED_CMS | HEADLESS_CMS | TRADITIONAL_CMS | DATABASE_BACKED_CONTENT | ECOMMERCE_CATALOG | APPLICATION_DATA | HYBRID]`
- Assessment output: `[bounded score, factors, rationale]`
- Unknowns requiring owner confirmation: `[LIST]`

The bounded factors are `CONTENT_VOLUME`, `UPDATE_FREQUENCY`,
`NUMBER_OF_EDITORS`, `EDITOR_TECHNICAL_LEVEL`, `CONTENT_RELATIONSHIPS`,
`PREVIEW_REQUIREMENTS`, `SCHEDULING_REQUIREMENTS`,
`MULTI_CHANNEL_REQUIREMENTS`, `LOCALIZATION_REQUIREMENTS`, `SEO_EDITABILITY`,
`MEDIA_VOLUME`, `APPROVAL_WORKFLOW`, and `PORTABILITY_REQUIREMENTS`.

## Candidates

| Candidate/provider | Content fit | Editor fit | Preview/workflow | Security/deployment impact | Export/portability | Cost status | Rejected or retained |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `[CANDIDATE]` | `[FACTS]` | `[FACTS]` | `[FACTS]` | `[FACTS]` | `[FACTS]` | `[KNOWN/UNKNOWN/OWNER_CONFIRMATION_REQUIRED]` | `[REASON]` |

No credentials, API keys, production URLs, or provider account data belong in
this record.

## Decision

- `CMS_REQUIRED`: `[VALUE]`
- `CMS_CLASS`: `[VALUE]`
- `SELECTED_PROVIDER`: `[VALUE OR NONE]`
- `WHY_SELECTED`: `[CONTENT AND OPERATIONS FACTS]`
- `WHY_OTHERS_REJECTED`: `[FACTS AND TRADEOFFS]`
- `EDITOR_EXPERIENCE`: `[DESCRIPTION]`
- `DEPLOYMENT_IMPACT`: `[DESCRIPTION]`
- `SECURITY_IMPACT`: `[DESCRIPTION]`

`ECOMMERCE_CATALOG` and `APPLICATION_DATA` only identify Capability #10
boundaries. This record does not authorize checkout, payments, authentication,
or application-module implementation.

## Tradeoffs and Lock-In

- `COST_MODEL`: `[KNOWN | UNKNOWN | OWNER_CONFIRMATION_REQUIRED]` plus source
- `LOCK_IN_RISK`: `[LOW | MODERATE | HIGH | PROPRIETARY | UNKNOWN]`
- `EXPORT_CAPABILITY`: `[FORMAT AND TESTED EXIT PATH | NONE | UNKNOWN]`
- `MEDIA_EXPORT`: `[METHOD]`
- `RELATIONSHIP_EXPORT`: `[METHOD]`
- `SLUG_EXPORT`: `[METHOD]`
- `PROVENANCE_EXPORT`: `[METHOD]`
- Owner acceptance and exit plan if export is limited: `[REQUIRED WHEN APPLICABLE]`

A proprietary provider without export capability is a visible lock-in warning,
not a silently passing portability claim.

## Ongoing Operations

Record the inputs that must transfer to the existing V2.5 handoff package:

- content model, fields, relationships, taxonomies, and validation;
- editable surfaces, roles, lifecycle, publishing authority, and agent draft
  boundary;
- preview, scheduling, archive/delete, slug/redirect, revision, and migration
  behavior;
- provider configuration boundary, environment impact, backup/restore input,
  training input, maintenance owner, and cost-register input;
- limitations, unresolved decisions, owner approvals, and review cadence.

Do not duplicate V2.5 long-term operations documents here.

## Readiness and Constraints

- Provider availability: `[AVAILABLE | UNAVAILABLE | UNKNOWN]`
- Migration required: `[true | false | UNKNOWN]`
- Content model reference: `[templates/content-model.json]`
- Validator result: `[PASS | FAIL | BLOCKED | UNRUN]`
- Exception: `[applied/reason/owner/review date or none]`
- External side effects performed: `NONE`

`[CONTENT_OPERATIONS_READY]` requires a resolved decision, validated model,
editable-surface and publishing boundary, slug policy, and portability review.
It adds no owner lock and does not mean a provider is installed, content is
published, or production is verified.
