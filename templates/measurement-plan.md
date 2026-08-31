# MEASUREMENT PLAN

> **Project Name:** [Project Name]  
> **Schema Version:** 2.6.0  
> **Phase:** 6.5 — Conversion & Analytics Intelligence  
> **Gate:** `[CONVERSION_MEASUREMENT_COMPLETE]`  
> **Status:** `Draft` | `Ready` | `Blocked` | `Exception`  
> **Governance:** [CONVERSION-ANALYTICS-PROTOCOL.md](../CONVERSION-ANALYTICS-PROTOCOL.md)

> **Anti-Fabrication Notice:** Every number in this document is either measured, owner-stated, or cited. Unknown values are recorded as `UNKNOWN`. Unassessed values are recorded as `UNASSESSED`. Nothing here is estimated to look complete.

---

## 1. Business Objective

- **BUSINESS_OBJECTIVE:** `[LEAD | SALE | CONSULTATION | BOOKING | AFFILIATE_OUTBOUND | NEWSLETTER_SIGNUP | ACCOUNT_REGISTRATION | SOFTWARE_TRIAL | DOWNLOAD | APPLICATION | PHONE_CALL | STORE_VISIT | CONTENT_ENGAGEMENT | DONATION | MEMBERSHIP]`
- **What business outcome is this site intended to produce?** [Plain-language statement]
- **How does the business actually make money from this outcome?** [Required — if this cannot be answered, the objective is wrong]
- **SECONDARY_OBJECTIVES:** [List, or `NONE`]
- **Source:** `project-brief.md` / `positioning.md` / owner statement

---

## 2. Primary Conversion

| Field | Value |
| :--- | :--- |
| **Primary conversion** | [e.g. Qualified consultation request submitted] |
| **Canonical event** | `[e.g. lead_form_submit]` |
| **Conversion level** | `MACRO` |
| **Where it happens** | [Route / component, from `information-architecture.md`] |
| **Success definition** | [What technically constitutes success — e.g. server accepted submission and returned confirmation] |
| **Confirmable?** | `SERVER_CONFIRMED` \| `CLIENT_ONLY` \| `NOT_DETERMINABLE` |

> **Rule:** Where success is server-determinable, the conversion event fires on confirmed success only — never on button click.

---

## 3. Secondary Conversions

| Conversion | Canonical Event | Level | Location | Why It Matters |
| :--- | :--- | :--- | :--- | :--- |
| [e.g. Pricing evaluated] | `pricing_view` | `MICRO` | [route] | [decision it informs] |
| | | | | |

---

## 4. KPI Hierarchy

### 4.1 Primary KPI (Business Outcome)

- **PRIMARY_KPI:** [exactly one, e.g. Qualified lead submissions per month]
- **Why this and not traffic:** [Required justification]

### 4.2 Secondary KPIs (Funnel)

| KPI | Funnel Stage | What It Reveals |
| :--- | :--- | :--- |
| | | |

### 4.3 Diagnostic Metrics

| Metric | What It Explains |
| :--- | :--- |
| | |

### 4.4 Guardrail Metrics

| Guardrail | Must Not Degrade Below |
| :--- | :--- |
| Lead quality | [definition] |
| Form error rate | [threshold] |
| Page performance | [threshold] |
| Accessibility | No regression |

### 4.5 Explicitly Rejected Vanity Metrics

| Metric | Why It Is Not a Success Measure Here |
| :--- | :--- |
| Pageviews | Traffic without conversion is not success |
| | |

---

## 5. Funnel Map

- **FUNNEL_MODEL:** `[LINEAR | BRANCHED | CONTENT_LED | COMMERCE | LEAD_GENERATION | SELF_SERVICE | AFFILIATE_OUTBOUND | NONLINEAR]`

| # | Stage | Visitor Question | Page / Component | Success Signal | Failure Signal | Measurement Event | Observable |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| 1 | | | | | | | `TRUE` |
| 2 | | | | | | | |

**Stages that are NOT observable** (record honestly, do not invent instrumentation):

| Stage | Why Not Observable |
| :--- | :--- |
| | |

> **Rule:** Do not invent funnel steps that do not exist on the actual website.

---

## 6. CTA Measurement Matrix

Every primary and meaningful secondary CTA in `content-plan.md` appears here. A CTA in locked copy with no row is a gate failure.

| CTA Label (verbatim from `content-plan.md`) | Location | Business Purpose | Canonical Event | KPI Relation | Destination | Verification Method |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| | | | | | | |

**CTAs deliberately not measured:**

| CTA | Reason `MEASUREMENT: NOT_REQUIRED` |
| :--- | :--- |
| | |

> **Rule:** CTA labels are copied verbatim from locked copy. Measurement never rewords a CTA. If a CTA is ambiguous, raise a locked-change request (§18) — do not edit it.

---

## 7. Event Dictionary

One block per event. Every field is mandatory per `CONVERSION-ANALYTICS-PROTOCOL.md` §8.

### `[event_name]`

```text
event_name              [lowercase_snake_case]
business_purpose        [the decision this event informs]
associated_kpi          [PRIMARY_KPI | SECONDARY_KPI | DIAGNOSTIC_METRIC | GUARDRAIL_METRIC]
conversion_level        [MACRO | MICRO | DIAGNOSTIC]
trigger                 [precise observable firing condition]
page_or_component       [route / component]
required_parameters     [list]
optional_parameters     [list]
deduplication_rule      [how repeat firing is prevented]
consent_dependency      [REQUIRED | NOT_REQUIRED | UNASSESSED]
implementation_method   [data attribute | listener | callback | server confirmation]
verification_method     [how correctness is proven]
event_version           [integer]
```

*(Repeat for each event. Events without a business or diagnostic purpose are prohibited.)*

---

## 8. Event Parameters

### 8.1 Global Parameter Rules

- Naming: `lowercase_snake_case`
- **Forbidden in every payload:** email, phone, full name, address, free-text message body, password, payment card data, medical information, SSN, date of birth
- Validation-error events carry a field **category**, never a field **value**

### 8.2 Parameter Registry

| Parameter | Type | Used By | Allowed Values / Format | PII Risk |
| :--- | :--- | :--- | :--- | :---: |
| | | | | `NONE` |

---

## 9. Attribution / UTM Strategy

- **ATTRIBUTION_REQUIRED:** `TRUE` | `NOT_APPLICABLE`

### 9.1 Parameter Conventions

| Parameter | Casing | Declared Values |
| :--- | :--- | :--- |
| `utm_source` | `lowercase` | |
| `utm_medium` | `lowercase` | `email` \| `cpc` \| `social` \| `referral` \| `affiliate` |
| `utm_campaign` | `lowercase_snake_case` | [declared campaign names] |
| `utm_content` | `lowercase_snake_case` | |
| `utm_term` | `lowercase` | |

### 9.2 Preservation & Boundaries

- **Preservation rule:** [How campaign parameters survive route transitions]
- **Landing-page attribution:** [Entry point recording rule]
- **Lead attribution:** [Supported / not supported, and by what mechanism]
- **Cross-domain:** [Requirement, or `NOT_APPLICABLE`. If continuity is unavailable, state the boundary honestly.]
- **Affiliate boundary:** Attribution ends at outbound handoff.

### 9.3 Prohibitions Acknowledged

- [ ] No PII in UTM parameters
- [ ] No improvised per-send campaign naming
- [ ] No inconsistent casing
- [ ] No fabricated attribution chains
- [ ] Required campaign parameters are not silently dropped

---

## 10. Analytics Provider / Implementation Method

| Field | Value |
| :--- | :--- |
| **Provider** | `[GA4 \| GTM \| PLAUSIBLE \| POSTHOG \| MATOMO \| FATHOM \| FIRST_PARTY \| CUSTOM_EVENT_PIPELINE \| NOT_SELECTED \| NO_ANALYTICS]` |
| **Implementation mode** | `[DIRECT_SNIPPET \| TAG_MANAGER \| SERVER_SIDE \| FIRST_PARTY_ENDPOINT \| DEFERRED]` |
| **Provider selected by** | [Owner / not yet selected] |
| **Failure resilience** | Site remains 100% functional if analytics is blocked or fails |

### 10.1 Vendor Naming Mapping

Canonical names remain authoritative. This table is an implementation-boundary translation only.

| Canonical Event | Vendor | Vendor Event Name | Notes |
| :--- | :--- | :--- | :--- |
| | | | |

> **Rule:** No credentials, API keys, secrets, or service-account material appear in this document or in source control.

---

## 11. Consent Dependency

- **CONSENT_DEPENDENCY:** `REQUIRED` | `NOT_REQUIRED` | `UNASSESSED`
- **Basis for this determination:** [Owner statement / jurisdiction context / `NOT YET ASSESSED`]
- **Activation policy:** [Immediate | Deferred pending privacy review]
- **SESSION_REPLAY:** `DISABLED` (default; enabling requires explicit owner justification and a masking policy)

> **Rule:** Unknown consent requirements remain `UNASSESSED`. Never guessed, never defaulted to `NOT_REQUIRED`. A dedicated Security / Privacy / Compliance subsystem is future work; this plan does not give legal advice.

---

## 12. Affiliate Measurement

- **AFFILIATE_MODEL:** `NOT_APPLICABLE` | `CLICK_ONLY` | `CLICK_AND_PLATFORM_REPORTED_CONVERSION`

*(Complete the remainder of this section only if affiliate links are part of the business model.)*

### 12.1 The Three-State Distinction

| State | Event / Source | Observable Here? | Evidence Source |
| :--- | :--- | :---: | :--- |
| **Affiliate click** | `affiliate_outbound_click` | | First-party instrumentation |
| **Affiliate conversion** | — | | Affiliate platform reporting only |
| **Affiliate commission** | — | | Affiliate platform payout data only |

> **Rule:** An outbound click is NEVER treated as a confirmed sale, conversion, or commission. Where the platform provides no conversion feed, record `NOT_OBSERVABLE` with the reason.

### 12.2 Outbound Event Parameters

| Parameter | Value Source | PII |
| :--- | :--- | :---: |
| `merchant` | | `NONE` |
| `placement` | | `NONE` |
| `page` | | `NONE` |
| `offer_category` | | `NONE` |
| `link_identifier` | | `NONE` |

### 12.3 Outbound Integrity

- Host comparison is by **resolved hostname**, not substring matching
- Internal navigation is never labelled outbound affiliate activity

---

## 13. Conversion Hypotheses

Every claim carries exactly one evidence label. A hypothesis is never presented as fact.

| # | Claim | Evidence Label | Basis | Proposed Response |
| :-- | :--- | :--- | :--- | :--- |
| 1 | | `OBSERVED` \| `EVIDENCE_SUPPORTED` \| `HYPOTHESIS` \| `EXPERIMENT_CANDIDATE` \| `PROVEN` | | |

**Friction points observed:** [list, labelled]  
**Trust deficits observed:** [list, labelled]  
**Experiment candidates:** [list — none are launched without traffic, tooling, and explicit authorization]

> **Rule:** Website Director does not automatically launch A/B tests.

---

## 14. Baseline / Target / Observation

| KPI | Baseline | Target | Observed | Notes |
| :--- | :--- | :--- | :--- | :--- |
| [PRIMARY_KPI] | `UNKNOWN` | `NOT_SET` | `NOT_YET_MEASURED` | |
| | | | | |

- **BASELINE_STATUS:** `UNKNOWN` | `RECORDED` | `INSUFFICIENT_TRAFFIC_FOR_BENCHMARK`
- **Targets labelled `WEBSITE_DIRECTOR_INFERRED`:** [list, or `NONE`]

> **Rule:** No invented benchmarks. A claim such as "industry conversion rate is X%" appears here only with a cited source recorded in §19.

---

## 15. Implementation Requirements

Binding requirements handed to the coding agent via `IMPLEMENTATION-CONTRACT.md` §2.3.

- **Event names:** Exactly as specified in §7. The builder must not invent, rename, or add events.
- **Data attributes:** [e.g. `data-analytics-event`, `data-analytics-*` parameter attributes]
- **Component traceability:** [Which components own which events]
- **Deduplication:** [Submit-handler guarding, single-fire rules]
- **SPA route changes:** Exactly one `page_view` per settled route. `PAGE_VIEW_SOURCE_OF_TRUTH = ROUTE_SETTLED`.
- **Form start vs. form success:** `lead_form_start` on first meaningful interaction; success event only on confirmed successful completion.
- **Failed submissions:** A server-rejected submission fires `form_validation_error` or an equivalent failure event, and **no** success conversion event.
- **Affiliate outbound:** [Handling rules, or `NOT_APPLICABLE`]
- **UTM handling:** [Preservation implementation]
- **Provider boundary:** [Where provider SDK code is allowed to live]
- **Failure resilience:** Analytics failure must not break navigation, forms, CTAs, motion, or styling.

> **Escalation rule:** If implementation conflicts with this specification, the coding agent HALTS and escalates. It does not improvise.

---

## 16. Verification Plan

How each event will be proven correct at build time.

| Event | Verification Steps | Expected Evidence |
| :--- | :--- | :--- |
| | | |

**Global checks:**

- [ ] Analytics loads correctly; no duplicate libraries
- [ ] Each event fires on its specified trigger
- [ ] Each event fires **exactly once** per qualifying interaction
- [ ] Event names match this document exactly
- [ ] Required parameters present
- [ ] No PII in any payload
- [ ] CTA events map to the correct controls
- [ ] Form start is not confused with form success
- [ ] Server-rejected forms produce no success conversion event
- [ ] Internal navigation is not mislabelled as outbound affiliate activity
- [ ] UTM handling matches §9
- [ ] SPA route transitions emit exactly one `page_view`
- [ ] No analytics secrets exposed
- [ ] Consent dependency respected

**Sets:** `measurement.implementation_verified`

---

## 17. Production Verification

- **PRODUCTION_VERIFIED:** `false` (default)
- **Evidence source:** Owner-supplied evidence from the real analytics environment only
- **Status if unavailable:** `NOT_YET_VERIFIED` — never reported as passing

| Event | Observed in Production? | Date | Evidence Reference |
| :--- | :---: | :--- | :--- |
| | | | |

> **Rule:** Website Director never accesses owner analytics accounts, and never sets this flag by inference.

**Sets:** `measurement.production_verified`

---

## 18. Exceptions / Blockers

### 18.1 Blockers

- **MEASUREMENT_MODE:** `standard` | `blocked` | `exception` | `not_required`
- **BLOCKED_REASON:** [Specific blocker in plain language, or `NONE`]

| Blocker | Impact | What Remains Usable | Resolution Owner |
| :--- | :--- | :--- | :--- |
| | | | |

### 18.2 Exception

- **EXCEPTION_APPLIED:** `false` | `true`
- **EXCEPTION_REASON:** [Substantive justification, or `N/A`]

> **Rule:** Never silently skip conversion measurement for a commercial public-facing website. Difficulty is not an exception; an unresolved provider is `blocked`, not `exception`.

### 18.3 Locked-Change Requests Raised

| Locked Artifact | Measurement Problem | Evidence Label | Proposed Change | Owner Decision |
| :--- | :--- | :--- | :--- | :--- |
| | | | | |

> **Rule:** Measurement never silently edits locked IA, copy, CTA wording, design tokens, or motion direction.

---

## 19. Provenance / Evidence

| Claim / Value | Source | Type | Date |
| :--- | :--- | :--- | :--- |
| | | `OWNER_STATED` \| `DERIVED_FROM_ARTIFACT` \| `CITED_EXTERNAL` \| `WEBSITE_DIRECTOR_INFERRED` | |

**Derived from:**

- `project-brief.md`
- `positioning.md`
- `information-architecture.md`
- `content-plan.md`
- `keyword-map.md`
- `seo-content-briefs.md`
- `site-profile.json` → `conversion_context{}`

**Unresolved questions put to the owner:**

| Question | Status | Answer |
| :--- | :--- | :--- |
| | `OPEN` \| `ANSWERED` | |
