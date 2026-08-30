# Website Director Content Operations and CMS Architecture Protocol

<!-- FRAMEWORK_VERSION: 2.13.0 -->

**Version:** 2.13.0
**Capability:** #8 Content Operations and CMS Architecture
**Phase:** 6.25
**Readiness gate:** `[CONTENT_OPERATIONS_READY]`
**Canonical state:** `content_ops.complete`
**Owner lock count:** exactly five; this protocol adds no lock

## 1. Purpose

This protocol turns the locked content structure into a reusable, editable,
safe, portable content architecture before design-system and implementation
work. It answers what content exists, which content is modeled as an entity,
which surfaces may be edited, what lifecycle and publishing authority apply,
and whether a CMS is actually needed.

The protocol is architecture and readiness work. It is not a CMS vendor
installation, a production integration, a deployment action, or permission to
publish. The deterministic implementation is
[`content-ops/validator.py`](content-ops/validator.py); the human contract is
[`templates/content-model.md`](templates/content-model.md); the machine
contract is [`templates/content-model.json`](templates/content-model.json); and
the vendor-neutral decision record is
[`templates/cms-decision.md`](templates/cms-decision.md).

## 2. Authority and overlap boundary

Capability #8 owns the pre-build content model, editability strategy, CMS
necessity decision, content relationships, editorial workflow, and publishing
state architecture.

The existing V2.5
[`CLIENT-CMS-HANDOFF-PROTOCOL.md`](CLIENT-CMS-HANDOFF-PROTOCOL.md) remains the
authority for client ownership, training, backup and restore, maintenance,
environment inventory, recurring cost records, long-term independence, and
handoff acceptance. This protocol supplies that handoff with the model and
decision inputs. It does not create a competing `handoff.cms_requirement`,
`handoff.cms_provider`, or `handoff.cms_architecture` authority and does not
retrofit the frozen V2.5 pilot.

Adjacent authorities remain separate:

- [`SEO-INTELLIGENCE-PROTOCOL.md`](SEO-INTELLIGENCE-PROTOCOL.md) owns SEO
  strategy and keyword intelligence. Content Operations exposes safe editable
  SEO fields and consumes that strategy.
- [`EVIDENCE-PROVENANCE-PROTOCOL.md`](EVIDENCE-PROVENANCE-PROTOCOL.md) owns
  source identity, evidence strength, rights, attribution, permitted use, and
  hash identity. Content Operations stores references only.
- Asset Director owns asset production and readiness; Accessibility owns alt
  semantics and WCAG verification; Security and Privacy owns risk,
  minimization, consent, disclosure, and technical controls; Conversion and
  Analytics owns measurement events and attribution. Content Operations does
  not create replacement state or duplicate ledgers for them.
- Capability #10 owns Ecommerce, Authentication, and Application Modules.
  Content Operations may recognize `ECOMMERCE_CATALOG` and `APPLICATION_DATA`
  as requirement classes, but does not design their application behavior.
- Capability #9 Localization and I18n is out of scope for this release. The
  field contract records whether a field is localizable so a later capability
  can act without coupling content to layout.

## 3. Phase placement and preconditions

Phase 6.25 runs after `locks.content_structure_locked` and before Phase 6.5
Conversion and Analytics. It does not renumber any existing phase. The Phase
6.5 precondition is now `[CONTENT_OPERATIONS_READY]`, so commercial builds do
not silently skip content operations before measurement, security, or
accessibility planning.

The phase consumes the locked IA/content structure and relevant evidence,
asset, SEO, security, accessibility, and measurement requirements. It
produces:

1. a content inventory;
2. activated semantic content types and field contracts;
3. editable-surface and role boundaries;
4. lifecycle, preview, scheduling, slug, redirect, archive, and migration
   policies;
5. a vendor-neutral CMS decision and portability record; and
6. a validated `content_ops{}` state object.

`[CONTENT_OPERATIONS_READY]` is a readiness gate, not an owner approval lock.
The five locks remain `design_direction_locked`,
`information_architecture_locked`, `content_structure_locked`,
`design_system_locked`, and `motion_direction_locked`.

## 4. Discovery before provider selection

Do not select a CMS because a familiar vendor is available. Record evidence
for:

- content types, current volume, expected growth, and repeated content;
- update frequency, number of editors, editor technical level, and ownership;
- relationships, taxonomy, media volume, and route structure;
- preview, approval, scheduling, archive, delete, and rollback needs;
- SEO editability and safe structured-data boundaries;
- multi-channel delivery, localization requirements, and future portability;
- security, privacy, credentials, third-party runtime, and deployment impact;
- handoff, training, maintenance, cost, and exit requirements.

Unknown facts remain `UNKNOWN` or `OWNER_CONFIRMATION_REQUIRED`. They are not
filled with invented volume, conversion, cost, provider, or legal assumptions.

## 5. CMS requirement classes

The bounded classification is one of:

`NO_CMS_REQUIRED`, `STATIC_STRUCTURED_CONTENT`, `FILE_BASED_CMS`,
`HEADLESS_CMS`, `TRADITIONAL_CMS`, `DATABASE_BACKED_CONTENT`,
`ECOMMERCE_CATALOG`, `APPLICATION_DATA`, or `HYBRID`.

`NO_CMS_REQUIRED` is a valid result. A small brochure with a few pages, one
technical owner, rare updates, no relationships, no scheduling, and no
nontechnical editorial workflow should not acquire a CMS merely to appear
more sophisticated. `STATIC_STRUCTURED_CONTENT` or `FILE_BASED_CMS` may be
appropriate when semantic files provide useful editability without a provider.

`ECOMMERCE_CATALOG` and `APPLICATION_DATA` identify a later Capability #10
boundary. Their presence here never authorizes implementation of payments,
accounts, checkout, or application behavior.

## 6. Bounded CMS-necessity model

`calculate_cms_necessity()` in `content-ops/validator.py` provides an
explainable pressure-point assessment across:

`CONTENT_VOLUME`, `UPDATE_FREQUENCY`, `NUMBER_OF_EDITORS`,
`EDITOR_TECHNICAL_LEVEL`, `CONTENT_RELATIONSHIPS`, `PREVIEW_REQUIREMENTS`,
`SCHEDULING_REQUIREMENTS`, `MULTI_CHANNEL_REQUIREMENTS`,
`LOCALIZATION_REQUIREMENTS`, `SEO_EDITABILITY`, `MEDIA_VOLUME`,
`APPROVAL_WORKFLOW`, and `PORTABILITY_REQUIREMENTS`.

The output records the observed factors, bounded score, threshold explanation,
classification, rationale, and confidence note. The score is a planning aid,
not mathematical proof and not a vendor recommendation. Owner or client
confirmation is required where a factor materially changes cost, security,
ownership, or long-term operations.

## 7. Content inventory and activation

`Content Inventory` records route, content purpose, current source, volume,
update behavior, editor, status, repeatability, relationships, SEO role,
media role, evidence risk, and migration status. Activate only types required
by the site. Do not create taxonomies, fields, workflows, or provider tables
for hypothetical future content.

Repeated case studies, articles, products, team members, testimonials, or
projects are modeled as reusable entities. Individual duplicated markup is a
content-model defect when the content repeats or needs independent editorial
management.

## 8. Content type contract

Every activated type records:

`TYPE_ID`, `NAME`, `PURPOSE`, `ROUTES_USED`, `FIELDS`, `REQUIRED_FIELDS`,
`OPTIONAL_FIELDS`, `RELATIONSHIPS`, `SEO_FIELDS`, `MEDIA_FIELDS`,
`PROVENANCE_FIELDS`, `EDITORIAL_STATUS`, `SLUG_POLICY`, and `ARCHIVE_POLICY`.

`TYPE_ID` is stable and machine-safe. It identifies a subject entity, not a
visual slot. A type should say `case_study`, `article`, `person`, or `offer`,
not `third_card` or `left_column`.

## 9. Field contract

Every field records:

`FIELD_ID`, `LABEL`, `TYPE`, `REQUIRED`, `VALIDATION`, `DEFAULT`, `EDITOR_HELP`,
`CHARACTER_LIMIT`, `RELATIONSHIP`, `LOCALIZABLE`, `SEO_ROLE`, and
`PROVENANCE_ROLE`.

Semantic fields such as `headline`, `summary`, `body`, `image`, `category`,
`author`, and `call_to_action` survive route and layout changes. Fields such as
`left_column_heading_blue`, `third_card_image`, `desktop_margin_top`, and
`hero_text_line_2_blue` are rejected by the validator because they couple
content to presentation.

## 10. Content model versus UI component model

Content models describe entities, meaning, validation, relationships, and
editorial risk. UI component models describe layout, composition, design
tokens, responsive behavior, motion, and interaction. They may be mapped at
render time, but content records must not contain component slot names,
breakpoint values, CSS properties, arbitrary colors, or design-token IDs.

This separation protects content portability, preview integrity, accessibility,
SEO, measurement, and future redesigns.

## 11. Editable-surface classes and safety

Every surface is classified as one of:

`OWNER_EDITABLE`, `EDITOR_EDITABLE`, `ADMIN_ONLY`, `DEVELOPER_CONTROLLED`,
`SYSTEM_GENERATED`, or `LOCKED_BRAND_ELEMENT`.

Editors may edit approved semantic content within validation boundaries. They
must not change analytics event identifiers, attribution keys, structured-data
schema, security headers, design tokens, canonical lock state, or other
system-controlled contracts. Owner-editable content does not grant permission
to bypass those protections.

The surface contract must prevent editors from breaking layout, keyboard and
screen-reader semantics, contrast or media requirements, SEO controls,
measurement contracts, legal disclosures, evidence/provenance requirements,
navigation, or form behavior.

## 12. Editorial lifecycle and publishing authority

The full lifecycle is `DRAFT`, `IN_REVIEW`, `APPROVED`, `SCHEDULED`,
`PUBLISHED`, and `ARCHIVED`. A simple site may use only `DRAFT` and
`PUBLISHED`, but the reduced workflow must be explicit.

State and authority are separate. Roles independently record `CAN_EDIT`,
`CAN_REVIEW`, `CAN_PUBLISH`, `CAN_ARCHIVE`, and `CAN_DELETE`. A role may not
implicitly publish because it can edit. Archive, delete, unpublish, and draft
are distinct operations.

Agent-generated content is recorded as `AGENT_GENERATED_CONTENT`, enters
`DRAFT`, and requires human review before `PUBLISHED`. No agent receives
autonomous `CAN_PUBLISH` authority. A draft exposed on a public route is a
failure; a published item must resolve on the intended release surface.

## 13. Preview and scheduling

Preview renders through the real design-system and route composition. A raw
JSON dump is not a visual preview and cannot prove layout, responsive,
accessibility, SEO, or interaction behavior.

Scheduling is architecture only in this capability. If used, record
`SCHEDULED_AT`, `TIMEZONE`, `PUBLISHING_SYSTEM`, and `FAILURE_BEHAVIOR`.
This release does not create a scheduler, queue, provider webhook, or
production publishing job.

## 14. Rich text

Rich text is limited to semantic headings, paragraphs, lists, links, quotes,
emphasis, captions, and validated media references. The implementation must
reject scripts, event-handler attributes, inline CSS, arbitrary font sizes or
colors, unsafe URLs, arbitrary iframes/embeds, and unvalidated HTML. The
validator applies this boundary before content can be considered ready.

## 15. SEO fields

Where editorial SEO control is required, a type may expose:

`SEO_TITLE`, `META_DESCRIPTION`, `CANONICAL_OVERRIDE`, `OG_TITLE`,
`OG_DESCRIPTION`, `OG_IMAGE`, `INDEXABILITY`, and bounded
`STRUCTURED_DATA_INPUTS`.

SEO fields consume the canonical SEO strategy. Local, preview, staging, and
invalid canonicals are rejected. Duplicate titles, accidental `noindex`,
fabricated reviews or ratings, unsupported claims, and free-form structured
data schema are not safe editor inputs. Structured data generation remains
system-controlled and evidence-bound.

## 16. Slugs, redirects, and route continuity

Slugs are normalized to lowercase kebab-case, checked for uniqueness, kept
clear of reserved routes, and evaluated with nested-route policy. A published
slug change requires a durable 301 redirect from the historical URL to the
new URL. Archived content may retain a redirect while disappearing from
public listings. A delete or unpublish operation must preserve inbound-link
and redirect impact review. A slug change must never silently break a known
historical URL.

Migration records include `SOURCE_URL`, `SOURCE_TYPE`, `TARGET_TYPE`,
`TARGET_SLUG`, `MIGRATION_STATUS`, `REDIRECT_REQUIRED`, `ASSET_REFS`,
`PROVENANCE_REFS`, and `SEO_NOTES`.

## 17. Relationships and taxonomy

Relationships explicitly name source field, target type, target field when
needed, cardinality, validation, and delete behavior. References to unknown
types or fields fail validation. Taxonomies are created only when they serve
navigation, filtering, editorial consistency, or a documented SEO purpose.
Taxonomy bloat and presentation-only categories are rejected as design noise.

## 18. Portability, revisions, and destructive operations

The portability record includes `EXPORT_FORMAT`, `MEDIA_EXPORT`,
`RELATIONSHIP_EXPORT`, `SLUG_EXPORT`, and `PROVENANCE_EXPORT`. A provider
without a usable export path produces a visible lock-in warning and requires
explicit owner acceptance and an exit plan. It is not silently treated as
portable.

Revision policy is one of `VERSIONED`, `NOT_REQUIRED`, `PROVIDER_MANAGED`, or
`CUSTOM_REQUIRED`. Archive, delete, and unpublish are separately documented;
delete requires authority and an inbound-link, asset, evidence, and restore
impact review. The V2.5 backup/restore and long-term operations contract
remains the handoff authority.

## 18.1 Content ownership

Every activated content type records an operational `CONTENT_OWNER`. The
owner may be a person, client, team, or already-defined project role, but it
must be an explicit accountable owner rather than an inferred organization.
Where a type can be edited, reviewed, published, archived, or deleted, its
owner and role boundary are recorded together. This capability records the
ownership input; V2.5 remains authoritative for long-term client ownership,
training, maintenance, and handoff acceptance.

## 19. Media, evidence, provenance, accessibility, security, and measurement

Content media references may carry `MEDIA_ID`, `ASSET_ID`, `PROVENANCE_REF`,
`ALT_TEXT`, `CAPTION`, and `CROP_POLICY`. Asset Director owns production
readiness, Evidence Provenance owns origin/rights/attribution/hash identity,
and Accessibility owns the semantic alt-text decision. A Dribbble, Behance,
Landbook, screenshot, or other research reference remains `REFERENCE_ONLY`
and cannot become a production image merely by entering a CMS field.

Factual, quantitative, health, financial, certification, affiliate, and other
high-risk claims require a resolvable V2.12 evidence/provenance reference
before release. Content Operations does not recreate the evidence ledger.

The model records requirements discovered by Security and Privacy,
Accessibility, and Conversion and Analytics, but those systems remain their
own authorities. No content field may expose secrets, credentials, tracking
identifiers, security configuration, or legal text that bypasses approved
disclosure controls. Measurement events and attribution are consumed from the
canonical V2.6 plan and are not editable content.

Affiliate content, when required, records `MERCHANT`, `PRODUCT`,
`AFFILIATE_URL`, `DISCLOSURE_REQUIREMENT`, `CLAIM_EVIDENCE`, and
`LAST_VERIFIED`. A click is never represented as a sale without downstream
evidence. Time-sensitive content may record `LAST_VERIFIED_AT`,
`REVIEW_DUE_AT`, and `EXPIRES_AT`; stale content remains visible as a review
finding or release blocker according to risk.

## 20. CMS provider decision

[`templates/cms-decision.md`](templates/cms-decision.md) records:

`CMS_REQUIRED`, `CMS_CLASS`, `CANDIDATES`, `SELECTED_PROVIDER`, `WHY_SELECTED`,
`WHY_OTHERS_REJECTED`, `COST_MODEL`, `LOCK_IN_RISK`, `EXPORT_CAPABILITY`,
`EDITOR_EXPERIENCE`, `DEPLOYMENT_IMPACT`, and `SECURITY_IMPACT`.

Cost values are classified `KNOWN`, `UNKNOWN`, or
`OWNER_CONFIRMATION_REQUIRED`; no cost is invented. A provider can be
selected only after the content and operational facts are recorded. The
selection does not authorize installation or production configuration.

## 21. Machine validation and readiness state

`content-ops/validator.py` validates unique type and field IDs, required and
optional fields, field types, presentation coupling, relationships,
taxonomies, editable surfaces, roles, lifecycle, publishing authority,
preview/scheduling contracts, rich text, SEO, media and provenance references,
affiliate/freshness fields, slugs and redirects, migrations, portability,
CMS decisions, and the `content_ops{}` state.

The state shape is:

```json
{
  "content_ops": {
    "complete": false,
    "cms_requirement": "UNASSESSED",
    "content_model_ready": false,
    "editable_surfaces_defined": false,
    "editorial_workflow_defined": false,
    "publishing_authority_defined": false,
    "slug_policy_defined": false,
    "portability_reviewed": false,
    "migration_required": false,
    "selected_architecture": null,
    "blocked_reason": null,
    "exception": {"applied": false, "reason": null}
  }
}
```

The state is distinct from V2.5 `handoff.status` and its CMS handoff fields.
No `cms_locked`, `content_ops_locked`, or `publishing_locked` field is a
permitted substitute for the readiness gate.

## 22. Implementation, browser QA, handoff, and launch integration

Builders follow the validated model and do not invent content fields in
markup, route code, or provider adapters. Browser QA consumes applicable
content behavior through the existing V2.8 harness: draft non-visibility,
published resolution, required-field behavior, preview rendering, rich-text
safety, SEO and redirect behavior, media/evidence references, and editor
boundary behavior. It does not create a second content runner.

The V2.5 handoff package receives the finalized model, type/field inventory,
role matrix, lifecycle, preview/scheduling policy, provider decision,
portability and migration records, publishing boundary, limitations, and
operational inputs. It remains responsible for ownership, training,
backup/restore, maintenance, environment, costs, and acceptance.

Launch operations verifies that the selected content source/provider is
configured for the known release and that content routes, redirects, and
critical fields behave in production. Launch does not redefine the model or
authorize autonomous publication.

## 23. Required validation scenarios

The registered V2.13 suite proves scenarios A–V and negative controls for
presentation coupling, duplicate type IDs, broken relationships, draft
leakage, missing redirects, unsafe rich text, missing provenance, research
images, autonomous publication, sixth locks, and frozen-project mutation.
The suite uses synthetic and temporary fixtures only and never writes under
`projects/` or to an external system.

## 24. Completion rule

`CONTENT_OPERATIONS_READY` may be reported only when the content model, CMS
decision, editable surfaces, workflow, publishing authority, slug policy,
portability review, and applicable migration/media/evidence references are
validated. A missing provider, unresolved evidence, unknown required fact,
unsafe field, or unverified production behavior remains explicit as
`BLOCKED`, `FAIL`, or `UNKNOWN`.

This protocol does not begin Capability #9 Localization/I18n or Capability #10
Ecommerce, Authentication, or Application Modules.
