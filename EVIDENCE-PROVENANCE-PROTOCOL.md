# Evidence, Claim & Asset Provenance Intelligence Protocol

**Framework:** Website Director V2.13.0
**Phase:** 6.95, after Accessibility and before Design System  
**Readiness gate:** EVIDENCE_PROVENANCE_READY  
**Canonical state:** provenance.complete  
**Canonical machine contract:** schemas/evidence-ledger.schema.json  
**Canonical validator:** provenance/validator.py

## 0. Scope and authority

This protocol implements Capability 7. It governs traceability of evidence,
claims, research references, testimonials, certifications, and production
assets. It does not add Content/CMS architecture, Localization, Ecommerce,
Authentication, Application, or any other Capability #8 module. Capability #8
Content Operations consumes this protocol's references; it does not duplicate
the ledger or change provenance authority.

The invariant is:

> No production claim or production asset without traceable provenance
> appropriate to its risk.

The system records source identity, support, rights evidence, permitted use,
attribution, review freshness, and byte identity. It does not determine legal
ownership, grant exclusivity, certify copyright, or certify regulatory
compliance.

Asset Director remains the authority for visual asset strategy, generation,
selection, optimization, and asset readiness. This protocol owns
cross-cutting source identity, evidence, rights records, attribution,
permitted-use boundaries, claim traceability, and release references. Existing
assets.provenance_status remains valid and distinct from provenance.complete.

Content records may carry a `PROVENANCE_REF` to this ledger for factual claims
and production media. High-risk claims without a resolvable reference remain
blocked or failed. Research and inspiration media remain `REFERENCE_ONLY` and
cannot be promoted by a CMS field. Asset Director still owns asset production,
and Content Operations owns only the content-facing reference contract.

## 1. Lifecycle placement and state

Phase 6.95 runs after Phase 6.9 Accessibility and before Phase 7 Design System.
The readiness gate is not an owner lock. Website Director continues to have
exactly five owner locks:

- design_direction_locked
- information_architecture_locked
- content_structure_locked
- design_system_locked
- motion_direction_locked

The current site profile may carry one cross-cutting provenance object:

    provenance {
      complete: false,
      ledger_ref: "evidence-ledger.json",
      claim_inventory_complete: false,
      asset_inventory_complete: false,
      research_reference_inventory_complete: false,
      license_review_complete: false,
      attribution_review_complete: false,
      implementation_verified: false,
      production_verified: false,
      unresolved_items: [],
      high_risk_items: [],
      blocked_reason: null,
      exception: { applied: false, reason: null }
    }

implementation_verified requires build or browser evidence. production_verified
requires owner-supplied production evidence. Neither state is inferred from a
plan or from a local simulation. A complete state requires a PASS ledger result
with the same ledger identity and a resolvable ledger_ref. Provenance never
writes a lock.

## 2. Evidence source contract

Every source receives a durable SOURCE_ID and records:

- SOURCE_TYPE
- TITLE
- SOURCE_URL_OR_REF
- SOURCE_DATE
- RETRIEVED_DATE
- evidence excerpt or bounded summary
- SHA256 for important source or license snapshots

Allowed evidence strength values are PRIMARY_SOURCE,
AUTHORITATIVE_SECONDARY, REPUTABLE_SECONDARY, OWNER_ATTESTED,
CUSTOMER_ATTESTED, INTERNAL_RECORD, RESEARCH_REFERENCE, and UNVERIFIED.
UNVERIFIED is a recorded non-release state, not evidence for a production
claim.

An AI response, model suggestion, generated citation, or statement equivalent
to AI said so is not a source. A hash proves identity of the recorded bytes; it
does not prove rights.

## 3. Claim contract

Each production claim is a record with:

    CLAIM_ID
    CLAIM_TEXT
    CLAIM_TYPE
    ROUTE
    COMPONENT
    SOURCE
    SOURCE_TYPE
    SOURCE_URL_OR_REF
    SOURCE_DATE
    VERIFIED_DATE
    EVIDENCE_STRENGTH
    OWNER
    EXPIRATION_OR_REVIEW_DATE
    DISCLOSURE_REQUIRED
    CLAIM_ORIGIN (for affiliate claims)
    EVIDENCE_REF
    EVIDENCE_MATCH
    PRODUCTION_STATUS
    CLAIM_STATUS

Allowed CLAIM_TYPE values are FACTUAL, QUANTITATIVE, COMPARATIVE, PERFORMANCE,
HEALTH, FINANCIAL, CERTIFICATION, AWARD, TESTIMONIAL, CUSTOMER_COUNT,
YEARS_IN_BUSINESS, LOCATION, PRODUCT_FEATURE, AFFILIATE_PRODUCT, and
GUARANTEE.

Allowed affiliate origins are MERCHANT, EDITORIAL, OWNER, and THIRD_PARTY;
UNVERIFIED is never a release classification.

Allowed claim statuses are SUPPORTED, PARTIALLY_SUPPORTED, UNVERIFIED,
CONTRADICTED, EXPIRED, OWNER_ATTESTED, REVIEW_REQUIRED, and PROHIBITED.
Supported means the recorded source actually supports the exact claim. It does
not mean an agent believes the claim.

Production claims without a registered source record, a bounded evidence
strength, and a recorded support match are BLOCKED. Direct URLs, free-text
citations, and model output do not replace a source-register record.
Contradicted, prohibited, expired, and unverified claims cannot pass.
Quantitative, performance, certification,
award, testimonial, customer-count, years-in-business, guarantee, health, and
financial claims receive elevated risk. Health and financial claims require
specialist review evidence.

No statistic, award, certification, customer count, years-in-business claim,
location claim, guarantee, or performance outcome may be fabricated.

## 4. Testimonial and certification controls

Testimonials record text, source, authority, consent, edited state, edit notes,
attribution, date, and production approval. Fake, composite, untraceable, or
demo testimonials do not pass production. Demo material remains
PROTOTYPE_ONLY.

Certifications and awards record issuer, status, evidence reference, validity
period, and authorized display. Missing issuer, evidence, validity, or display
authorization is BLOCKED. Production statuses must be active/current/valid,
verified, issued, or renewed; revoked, expired, suspended, unverified, unknown,
and other non-release statuses are blocked. The validator does not turn a
record into a legal or institutional certification.

## 5. Research-reference boundary

Research and inspiration references remain REFERENCE_ONLY. Record:

- platform
- source_url
- query
- retrieved_at
- reference_purpose
- grade
- PATTERN_TO_LEARN
- WHAT_NOT_TO_COPY
- upstream SHA256
- reference_only = true

Dribbble, Behance, Awwwards, Land-book, competitor, showcase, screenshot, and
similar material may inform interpretation, but cannot become a production
hero, signature asset, or claim source merely because it was viewed.

When the Design Inspiration MCP adapter supplies an input, consume its
platform, source_url, query, retrieved_at, upstream SHA256, and
REFERENCE_ONLY boundary. This protocol does not reimplement or replace the
bounded adapter.

## 6. Asset provenance contract

Each important or production asset records:

- ASSET_ID
- FILE
- ASSET_TYPE
- ORIGIN
- SOURCE_URL_OR_REF
- CREATOR
- OWNER
- LICENSE
- LICENSE_EVIDENCE_REF (a source-register reference; free text alone is not evidence)
- AUTHORIZED_USES
- ATTRIBUTION
- MODIFIED
- MODIFICATION_NOTES
- PROVIDER_OR_TOOL
- GENERATION_DATE
- SOURCE_INPUTS
- SHA256
- PRODUCTION_APPROVED
- HANDOFF_RESTRICTIONS

Allowed origins are OWNER_PROVIDED, CLIENT_PROVIDED, ORIGINAL_CREATED,
AI_GENERATED, LICENSED_STOCK, OPEN_LICENSE, PUBLIC_DOMAIN, COMMISSIONED,
THIRD_PARTY_BRAND, SCREENSHOT_REFERENCE, RESEARCH_REFERENCE, and UNKNOWN.

Production asset manifest entries must carry provenance_ref resolving to the
same ASSET_ID in the cross-cutting ledger. A high-risk or external asset
without resolved evidence cannot be marked production-ready by Asset Director.

### 6.1 Origin-specific controls

- OWNER_PROVIDED and CLIENT_PROVIDED require recorded attestation or usage
  authority.
- ORIGINAL_CREATED records creator and owner context.
- LICENSED_STOCK records provider, source, license identity, license evidence,
  authorized uses, freshness, and attribution where required.
- OPEN_LICENSE and PUBLIC_DOMAIN record the applicable source and evidence of
  that basis; public-domain treatment is not inferred from age or appearance.
- COMMISSIONED records a commission or usage reference and any handoff
  restrictions.
- THIRD_PARTY_BRAND records mark owner, authorized context, and authorization
  status. Unknown authorization is review-required.
- SCREENSHOT_REFERENCE and RESEARCH_REFERENCE are never production assets.
- UNKNOWN is blocked from production.

Fonts, icons, logos, trademarks, screenshots, quoted material, and stock
photography receive the same source and permitted-use treatment. Attribution
required by the evidence record must be present in the delivered experience or
the release is blocked.

### 6.2 AI-generated media

AI-generated media records provider or tool, generation date, source inputs,
edit history where modified, and output SHA256. AI generation is not a
determination of copyright, exclusivity, ownership, or permitted commercial
use. Unsupported rights assertions are rejected.

## 7. Hash and identity policy

Use SHA-256 for important evidence, license snapshots, research snapshots, and
important or production assets. Compare recorded hashes with the bytes at the
declared relative path. Production hash validation without a validation root,
a present file, and matching bytes is BLOCKED or FAIL. A matching hash proves
only that the inspected bytes equal the recorded bytes.

Paths must remain inside the declared validation root. Absolute paths and path
escape are invalid.

## 8. Risk and status model

Risk is LOW, MODERATE, HIGH, or SPECIALIST_REVIEW_REQUIRED. Unknown rights,
unresolved third-party marks, ambiguous commissioned work, health or financial
claims, and other specialist cases do not become a pass through wording.

Validator results are PASS, BLOCKED, or FAIL:

- PASS means the recorded contract is complete for the requested mode.
- BLOCKED means required evidence is absent, stale, unresolved, or unavailable.
- FAIL means a contradiction, forbidden promotion, identity mismatch, duplicate
  identifier, unsupported assertion, or other hard invariant was found.

The status is evidence-based. It is not a legal opinion.

## 9. Exceptions and backward compatibility

Exceptions are limited to prototype, local-demo, or internal use. They require
a reason, are recorded in the ledger and state, and remain PROTOTYPE_ONLY.
Exceptions never certify production.

Historical projects that predate V2.12 remain valid under their recorded
schema. Do not retrofit frozen pilots. Historical asset-provenance records,
research references, and SHA-256 evidence remain historical evidence and are
not silently rewritten.

## 10. Cross-system ownership

- Content Structure records compact EVIDENCE_REF values and does not duplicate
  the ledger.
- SEO resolves factual metadata, structured data, ratings, and FAQ claims to
  evidence and does not invent freshness or authority.
- Security & Privacy owns data classification, disclosure, consent, and
  security controls. This protocol owns source and rights traceability.
- Accessibility owns alt text and interaction verification. This protocol
  records the identity and permitted-use boundary for media.
- Asset Director owns visual asset strategy and readiness. This protocol
  blocks unresolved high-risk provenance.
- Launch Ops consumes provenance status and release identity but does not
  create a second provenance authority.
- Client Handoff transfers the ledger, restrictions, review dates, and
  attribution obligations without creating a new state machine.

## 11. Required negative controls

The deterministic suite uses disposable synthetic fixtures and a read-only
snapshot of the frozen corpus to prove:

A supported statistic passes; B invented statistic fails; C untraceable
testimonial fails; D certification without issuer fails; E owner-attested asset
passes; F research reference hero promotion fails; G screenshot promotion
fails; H licensed stock with evidence passes; I unknown stock license blocks;
J unlicensed font blocks; K evidenced open-license font passes; L unresolved
partner logo authorization blocks; M AI media metadata and hash pass; N
unsupported AI rights assertion fails; O changed asset hash fails; P omitted
required attribution fails; Q unclassified affiliate performance claim blocks;
R expired claim blocks; S duplicate provenance ID fails; T missing production
asset provenance reference fails; U a sixth owner lock fails; V frozen fixture
mutation is caught by the integrity guard. W-AK cover validated-ledger state,
unknown modes, contradictory status, overstated or contradicted evidence,
freshness, license-register resolution, hash-root availability, testimonial
shape, exception masking, direct-URL bypass, free-text license evidence,
certification release status, and unverified affiliate origin.

## 12. Closeout contract

The implementation closeout records:

    framework_version
    branch
    baseline_sha
    final_worktree_status
    files_changed
    tests_run
    tests_passed
    tests_failed
    framework_validation_status
    evidence_provenance_status
    frozen_projects_modified
    sixth_lock_detected
    production_or_external_actions
    unresolved_warnings
    next_action

The only completion token for this capability is
WEBSITE_DIRECTOR_EVIDENCE_ASSET_PROVENANCE_COMPLETE. If required evidence or
verification cannot pass, use WEBSITE_DIRECTOR_EVIDENCE_ASSET_PROVENANCE_BLOCKED.
