# Evidence, Claim & Asset Provenance Ledger

Project: [Project Name]  
Schema: 2.12.0  
Owner: [Owner]  
Status: NOT_EVALUATED

This ledger records evidence identity, support, rights evidence, permitted use,
attribution, review dates, and production boundaries. It does not certify legal
ownership, exclusivity, copyright, or regulatory compliance.

## 1. Production rule

No production claim or production asset is usable without provenance
appropriate to its risk. Missing, stale, contradictory, ambiguous, or
unverified evidence is BLOCKED or FAIL, not an inferred pass.

Prototype, local-demo, and internal exceptions must be explicitly recorded and
must remain PROTOTYPE_ONLY.

## 2. Evidence source register

For every source record:

| Field | Value |
|---|---|
| SOURCE_ID | |
| SOURCE_TYPE | PRIMARY_SOURCE / AUTHORITATIVE_SECONDARY / REPUTABLE_SECONDARY / OWNER_ATTESTED / CUSTOMER_ATTESTED / INTERNAL_RECORD / RESEARCH_REFERENCE / UNVERIFIED |
| TITLE | |
| SOURCE_URL_OR_REF | |
| SOURCE_DATE | |
| RETRIEVED_DATE | |
| EVIDENCE_EXCERPT_OR_SUMMARY | |
| SHA256 | Required for important snapshots |

AI said so is not a source type or evidence.

## 3. Claim inventory

Every factual or persuasive production claim receives an EVIDENCE_REF that
resolves to the source register. Direct URLs, free-text citations, and model
output do not replace a registered source record.

| Field | Value |
|---|---|
| CLAIM_ID | |
| CLAIM_TEXT | |
| CLAIM_TYPE | |
| ROUTE | |
| COMPONENT | |
| SOURCE | |
| SOURCE_TYPE | |
| SOURCE_URL_OR_REF | |
| SOURCE_DATE | |
| VERIFIED_DATE | |
| EVIDENCE_STRENGTH | |
| OWNER | |
| EXPIRATION_OR_REVIEW_DATE | |
| DISCLOSURE_REQUIRED | |
| CLAIM_ORIGIN (affiliate only) | MERCHANT / EDITORIAL / OWNER / THIRD_PARTY |
| EVIDENCE_REF | |
| EVIDENCE_MATCH | true only when the registered source supports the exact claim |
| PRODUCTION_STATUS | |
| CLAIM_STATUS | |

Allowed claim types include FACTUAL, QUANTITATIVE, COMPARATIVE,
PERFORMANCE, HEALTH, FINANCIAL, CERTIFICATION, AWARD, TESTIMONIAL,
CUSTOMER_COUNT, YEARS_IN_BUSINESS, LOCATION, PRODUCT_FEATURE,
AFFILIATE_PRODUCT, and GUARANTEE.

Allowed claim status values are SUPPORTED, PARTIALLY_SUPPORTED, UNVERIFIED,
CONTRADICTED, EXPIRED, OWNER_ATTESTED, REVIEW_REQUIRED, and PROHIBITED. Never
invent statistics, awards, certifications, customer counts, years, locations,
guarantees, or performance outcomes.

## 4. Testimonials

Record source, authority, consent, edit history, attribution, date, and
production approval. Do not use fake, composite, or untraceable testimonials.
Demo testimonials stay PROTOTYPE_ONLY.

## 5. Certifications and awards

Record issuer, status, evidence reference, validity period, and authorization
to display. Production statuses must be active/current/valid, verified, issued,
or renewed. Revoked, expired, suspended, unverified, unknown, or other
non-release statuses are blocked.

## 6. Research and inspiration references

Record PLATFORM, SOURCE_URL, QUERY, RETRIEVED_AT, REFERENCE_PURPOSE, GRADE,
PATTERN_TO_LEARN, WHAT_NOT_TO_COPY, and UPSTREAM_SHA256. Research and
screenshot references are REFERENCE_ONLY; they are not production asset
provenance and cannot be promoted into a hero or signature asset. MCP input
provenance is consumed from the bounded adapter and is not reimplemented here.

## 7. Asset origin and rights register

Allowed origins are OWNER_PROVIDED, CLIENT_PROVIDED, ORIGINAL_CREATED,
AI_GENERATED, LICENSED_STOCK, OPEN_LICENSE, PUBLIC_DOMAIN, COMMISSIONED,
THIRD_PARTY_BRAND, SCREENSHOT_REFERENCE, RESEARCH_REFERENCE, and UNKNOWN.

| Field | Value |
|---|---|
| ASSET_ID | |
| FILE | |
| ASSET_TYPE | |
| ORIGIN | |
| SOURCE_URL_OR_REF | |
| CREATOR | |
| OWNER | |
| LICENSE | |
| LICENSE_EVIDENCE_REF | |
| AUTHORIZED_USES | |
| ATTRIBUTION | |
| MODIFIED | |
| MODIFICATION_NOTES | |
| PROVIDER_OR_TOOL | Required for AI media |
| GENERATION_DATE | Required for AI media |
| SOURCE_INPUTS | Required for AI media |
| SHA256 | Required for important or production assets |
| PRODUCTION_APPROVED | |
| HANDOFF_RESTRICTIONS | |

Hashes establish byte identity, not rights. AI-generated media is not
automatically exclusive or rights-cleared. External assets, fonts, icons,
logos, trademarks, screenshots, and quoted material require evidence of
permitted use appropriate to their risk.

## 8. Attribution and affiliate controls

Required attribution must be recorded in the ledger and rendered where the
license or source requires it. Affiliate product claims record merchant versus
editorial origin, freshness, evidence, and disclosure dependency. Allowed
origins are MERCHANT, EDITORIAL, OWNER, and THIRD_PARTY; UNVERIFIED is blocked.
Merchant performance copy without classification is blocked.

## 9. Risk classification

Use LOW, MODERATE, HIGH, or SPECIALIST_REVIEW_REQUIRED. Health, financial,
unresolved trademark, ambiguous commissioned, and unknown-rights records
require specialist review or remain blocked.

## 10. Cross-system references

- Content Plan: use EVIDENCE_REF, do not duplicate the full ledger.
- SEO: factual metadata, structured data, ratings, and FAQ claims resolve to
  evidence records.
- Asset Director: keep assets.provenance_status and add asset-level
  provenance_ref; unresolved high-risk assets cannot be production-ready.
- Security & Privacy: owns data risk and disclosure; this ledger owns source
  traceability and permitted-use records.
- Accessibility: owns alt text and interaction; this ledger records source and
  rights identity for media.
- Launch Ops and Client Handoff consume the same ledger and do not create a
  second provenance authority.

## 11. Verification state

| State | Value |
|---|---|
| provenance.complete | false until inventory, license, and attribution review pass |
| claim_inventory_complete | |
| asset_inventory_complete | |
| research_reference_inventory_complete | |
| license_review_complete | |
| attribution_review_complete | |
| implementation_verified | Requires build/browser evidence |
| production_verified | Requires owner-supplied production evidence |
| unresolved_items | |
| high_risk_items | |
| blocked_reason | |
| exception | Prototype-only exception with reason, if any |

## 12. Approval

EVIDENCE_PROVENANCE_READY is a readiness gate, not an owner lock. Production
deployment remains subject to the existing launch authority and owner
authorization.
