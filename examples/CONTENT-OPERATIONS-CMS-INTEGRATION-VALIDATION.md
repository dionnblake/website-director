# Content Operations & CMS Architecture Integration Validation

<!-- FRAMEWORK_VERSION: 2.13.0 -->

**Capability:** #8 Content Operations and CMS Architecture
**Phase:** 6.25
**Protocol:** `CONTENT-OPERATIONS-CMS-PROTOCOL.md`
**Readiness gate:** `[CONTENT_OPERATIONS_READY]`
**State:** `content_ops.complete`
**Owner locks:** five exactly; no content lock added

This is a deterministic synthetic validation record for the provider-neutral
content operations subsystem. It proves the validator's boundaries without
selecting a live provider, making a network request, publishing content,
deploying, using credentials, or modifying `projects/`.

## Authority reconciliation

Capability #8 owns the pre-build content model, CMS need/no-need decision,
editable surfaces, editorial lifecycle, publishing authority, preview,
scheduling architecture, relationships, taxonomies, slugs, redirects,
portability, migration, media references, and content-facing provenance
requirements. V2.5 `CLIENT-CMS-HANDOFF-PROTOCOL.md` remains the authority for
client ownership, training, backups/restores, maintenance, costs, environment,
long-term operations, and handoff acceptance.

SEO, Measurement, Security & Privacy, Accessibility, Asset Director, and
Evidence Provenance remain their own authorities. Capability #9
Localization/I18n and Capability #10 Ecommerce, Authentication, and
Application Modules are not implemented here.

## Scenarios A–V

| ID | Synthetic condition | Expected result | Boundary proved |
| --- | --- | --- | --- |
| A | Five-page brochure, rare updates, one technical owner, no relationships or workflow | `PASS`: `NO_CMS_REQUIRED` or justified static class | CMS restraint |
| B | 500 articles, frequent updates, nontechnical editors, relationships, preview, approval | `PASS`: CMS-required classification | Bounded necessity |
| C | Repeated case studies hard-coded individually | `FAIL` | Entity modeling |
| D | Field `hero_text_line_2_blue` | `FAIL` | Presentation separation |
| E | Semantic field `headline` | `PASS` | Meaning-based field contract |
| F | `DRAFT` content publicly visible | `FAIL` | Draft leakage |
| G | `PUBLISHED` content publicly visible | `PASS` | Published route behavior |
| H | Editor can edit analytics event name | `FAIL` | Measurement boundary |
| I | Editor can edit design tokens | `FAIL` | Design-system boundary |
| J | Published slug changed without 301 redirect | `FAIL` | Historical URL continuity |
| K | Archived slug changed with valid 301 redirect | `PASS` | Archive/redirect behavior |
| L | High-risk claim has no provenance reference | `FAIL` | V2.12 evidence boundary |
| M | Asset Director asset and provenance references resolve | `PASS` | Media integration |
| N | Dribbble/research reference used as production media | `FAIL` | Reference-only boundary |
| O | Rich text contains script or arbitrary style | `FAIL` | Semantic rich-text safety |
| P | Static Markdown source is justified | `PASS` | No-CMS/static adapter |
| Q | Selected CMS provider unavailable | `BLOCKED` | Honest provider state |
| R | Agent-generated article is directly `PUBLISHED` | `FAIL` | Human publishing authority |
| S | Agent-generated article remains `DRAFT` | `PASS` | Safe agent default |
| T | Proprietary CMS has no export path | `PASS` with warning | Visible lock-in and owner acceptance |
| U | `content_ops_locked` is added to the profile | `FAIL` | Five-lock invariant |
| V | Protected frozen fixture is mutated | `FAIL` | Frozen integrity guard |

## Negative-control inventory

The suite also exercises the concrete issue signals
`PRESENTATION_COUPLED_FIELD`, `DUPLICATE_CONTENT_TYPE_ID`,
`RELATIONSHIP_TARGET_INVALID`, `DRAFT_PUBLIC_LEAK`,
`PUBLISHED_SLUG_REDIRECT_MISSING`, `UNSAFE_RICH_TEXT`,
`CLAIM_PROVENANCE_REQUIRED`, `REFERENCE_ASSET_NOT_PRODUCTION`,
`AGENT_PUBLISHING_FORBIDDEN`, `CONTENT_OPS_LOCK_FORBIDDEN`, and
`FROZEN_FIXTURE_MUTATION`.

## Execution contract

```text
python tests/test_v2_13_content_operations.py
python -m framework_validation --run-suites
```

The test registry runs the suite with temporary fixtures and no external
writes. The framework validator remains the authority for registry integrity,
version lineage, exact five locks, historical compatibility, and frozen
corpus protection. The content-operations validator remains the authority for
the Capability #8 content/CMS contract.
