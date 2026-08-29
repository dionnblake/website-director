# CONVERSION & ANALYTICS INTELLIGENCE PROTOCOL

> **Version:** 2.6.0  
> **Status:** Authoritative Conversion Measurement, Analytics Architecture, Attribution & Experimentation Standard  
> **Supersedes:** `CRO-ANALYTICS-EXPERIMENTATION-PROTOCOL.md` (V2.4.0) — retained as a superseded pointer for link stability. All of its normative content is absorbed here.  
> **Governs:** `PHASE 6.5` (Conversion & Analytics Intelligence) and `PHASE 8.97` (Experimentation & Instrumentation Readiness)  
> **Readiness Gate:** `GATE MEASUREMENT: [CONVERSION_MEASUREMENT_COMPLETE]`  
> **Core Principle:** Website Director does not merely assert that a CTA *should* convert. It defines what the conversion is, which event represents it, how that event is triggered, which KPI it serves, how attribution is preserved, and how the implementation is verified. Measure what matters. Never track everything merely because analytics exists. Never fabricate a number.

---

## 1. Purpose & Architectural Position

Website Director already captures commercial intent — primary conversion, secondary conversion, CTA labels, target metrics, objections, trust requirements, funnel structure, and content hierarchy. What it historically lacked was a first-class system converting that intent into a **deterministic measurement architecture**.

This protocol is that layer. It sits between the content structure lock and the design system phase, so measurement requirements **inform** design rather than being retrofitted onto a finished build.

```text
PHASE 5: INFORMATION ARCHITECTURE
        ↓
LOCK 2: INFORMATION_ARCHITECTURE_LOCKED
        ↓
PHASE 6: CONTENT STRUCTURE & EVIDENCE PLAN
        ↓
LOCK 3: CONTENT_STRUCTURE_LOCKED
        ↓
PHASE 6.5: CONVERSION & ANALYTICS INTELLIGENCE
        ↓
GATE MEASUREMENT: CONVERSION_MEASUREMENT_COMPLETE
        ↓
PHASE 7: DESIGN SYSTEM TOKEN ARCHITECTURE
```

**Why after Lock 3.** Measurement is derived from the locked content structure. CTAs, funnel steps, and form surfaces must exist and be approved before they can be traced to events. Planning measurement earlier would invent funnel steps; planning it later (as V2.4 did exclusively at Phase 8.97) forces instrumentation to be retrofitted onto design decisions already frozen.

**What remains at Phase 8.97.** Experimentation design, provider wiring specifics, and instrumentation readiness verification remain at Phase 8.97 under `[CRO_MEASUREMENT_READY]`, which is now a **downstream sub-gate reading the same `measurement{}` state**. It is not an independent flag.

---

## 2. System Invariants & Core Governance

1. **Single Completion Flag Invariant:** `measurement.complete` in `site-profile.json` is the **only** authoritative readiness flag for `[CONVERSION_MEASUREMENT_COMPLETE]`. No second, independently-writable completion flag may ever be created for measurement readiness.
2. **No Sixth Owner Lock:** `[CONVERSION_MEASUREMENT_COMPLETE]` is a **readiness gate**, not an owner lock. Exactly 5 owner locks remain immutable (`design_direction_locked`, `information_architecture_locked`, `content_structure_locked`, `design_system_locked`, `motion_direction_locked`).
3. **Planning ≠ Verification Invariant:** `measurement.complete` certifies that a measurement *plan* exists. It NEVER means analytics has been observed working. Implementation verification is `measurement.implementation_verified`. Production verification is `measurement.production_verified`. These three states are permanently distinct and must never be collapsed.
4. **Anti-Fabrication Invariant:** Website Director must never invent baselines, conversion rates, industry benchmarks, attribution chains, downstream revenue, or implementation success. Unknown is recorded as `UNKNOWN`. Unassessed is recorded as `UNASSESSED`.
5. **Anti-Surveillance & Data Minimization Invariant:** Analytics collects ONLY the minimal behavioral data required for defined measurement. PII (email, phone, full name, address, password, free-text form input, payment card data, medical information, SSN, date of birth) is strictly forbidden in analytics payloads (`PII_IN_ANALYTICS = 0`).
6. **Anti-Dark-Pattern Invariant:** Conversion optimization must never employ deception, fake scarcity, countdown timers, confirmshaming, hidden opt-outs, or forced continuity (`DARK_PATTERN_CHECK = PASS`). A conversion increase that degrades brand trust, clarity, or accessibility is a failure, not a win.
7. **Analytics Failure Resilience:** The website must remain 100% functional (navigation, forms, CTAs, animations, styling) if analytics scripts fail, are blocked, or are disabled (`ANALYTICS_FAILURE_POLICY = SITE_FUNCTIONAL`). Analytics is observation infrastructure, never application-critical infrastructure.
8. **Provider Neutrality:** No analytics vendor is hardwired. Vendor selection is conditional and may legitimately be unresolved.
9. **Locks Always Win:** Measurement may never silently mutate approved IA, locked copy, CTA wording, design tokens, or motion direction. See §16.
10. **No External Side Effects:** This protocol produces specifications. It never creates analytics properties, modifies GTM containers or ad accounts, installs pixels on live sites, deploys, publishes, transmits production data, or uses owner credentials.

---

## 3. Derived Inputs (Do Not Re-Interview)

Measurement requirements are derived from artifacts that already exist. The owner is re-engaged **only** for genuinely unresolved commercial facts (e.g. "which analytics provider do you use?", "does an affiliate platform report conversions back to you?").

| Input Artifact | What Is Extracted |
| :--- | :--- |
| `project-brief.md` | Business model, commercial objective, owner constraints |
| `positioning.md` | Value proposition, audience, competitive frame |
| `information-architecture.md` | Page inventory, funnel topology, route structure |
| `content-plan.md` | **Authoritative CTA inventory**, copy strings, form surfaces, proof placement |
| `keyword-map.md` | Landing intent per page, entry-point expectations |
| `seo-content-briefs.md` | Per-page search intent, conversion expectations |
| `site-profile.json` → `conversion_context{}` | `primary_conversion`, `secondary_conversion`, `cta_label`, `target_metric`, objections, trust requirements |

*Rule:* If a required input is absent, record the deficiency in `measurement.blocked_reason` rather than inventing the missing fact.

---

## 4. Business Objective Determination

Determine what business outcome the site is intended to produce. **Do not assume every website has the same conversion model.**

Supported objective classes (`BUSINESS_OBJECTIVE`):

```text
LEAD                 SALE                  CONSULTATION
BOOKING              AFFILIATE_OUTBOUND    NEWSLETTER_SIGNUP
ACCOUNT_REGISTRATION SOFTWARE_TRIAL        DOWNLOAD
APPLICATION          PHONE_CALL            STORE_VISIT
CONTENT_ENGAGEMENT   DONATION              MEMBERSHIP
```

A project may declare one primary objective and any number of secondary objectives. `CONTENT_ENGAGEMENT` is a legitimate primary objective only where the business model genuinely monetizes attention (publisher, ad-supported, affiliate) — never as a fallback because no real conversion could be identified.

---

## 5. KPI Architecture

### 5.1 The Four-Tier Distinction

Website Director must explicitly separate:

```text
BUSINESS OUTCOME KPI
        ≠
FUNNEL KPI
        ≠
DIAGNOSTIC METRIC
        ≠
VANITY METRIC
```

| Tier | Identifier | Definition | Decision Use |
| :--- | :--- | :--- | :--- |
| **Business Outcome KPI** | `PRIMARY_KPI` | The single metric most directly associated with the primary business objective. Exactly one. | Determines whether the site is succeeding commercially |
| **Funnel KPI** | `SECONDARY_KPI` | Supporting metrics indicating progression toward the primary conversion | Locates where progression breaks |
| **Diagnostic Metric** | `DIAGNOSTIC_METRIC` | Explains *why* an outcome occurred. Not a business outcome itself. | Root-cause analysis |
| **Guardrail Metric** | `GUARDRAIL_METRIC` | Health thresholds that must NOT degrade (lead quality, form error rate, page speed, accessibility, refund/bounce rate) | Blocks harmful "wins" |
| **Vanity Metric** | `VANITY_METRIC` | Prohibited as an optimization target | None — flagged and rejected |

### 5.2 Vanity Metric Prohibition

Raw page views, raw clicks, aggregate time on page, unmotivated scroll percentage, animation triggers, and follower/impression counts are **invalid optimization targets**.

> **Pageviews must never automatically be treated as success. A website with 100,000 visits and zero conversions is not successful merely because traffic increased.**

Interpret metrics in context: high time-on-page can reflect confusion; fast task completion can reflect excellence.

### 5.3 Conversion Hierarchy (`CONVERSION_LEVEL`)

Every tracked interaction belongs to exactly one level:

| Level | Description | Examples |
| :--- | :--- | :--- |
| `MACRO` | The primary business/visitor milestone | Purchase, qualified consultation request, application submitted, booking completed |
| `MICRO` | Meaningful progression toward macro conversion | Pricing viewed, configurator completed, spec downloaded, case study viewed |
| `DIAGNOSTIC` | UX health and orientation signals | Navigation selection, filter toggle, section exposure, form validation error |

---

## 6. Funnel Measurement Model

Map the visitor journey into **observable** behavior. Use the existing cognitive journey where applicable:

```text
UNDERSTAND  →  BELIEVE  →  EVALUATE  →  CONVERT
```

Translate into observable stages. A representative lead-generation translation:

```text
Landing page viewed
        ↓
Primary content engaged
        ↓
Offer evaluated
        ↓
CTA activated
        ↓
Form started
        ↓
Form submitted
        ↓
Business outcome confirmed
```

**Do not invent funnel steps that do not exist on the actual website.** If the site has no pricing page, there is no "pricing evaluated" stage.

### 6.1 Funnel Topology (`FUNNEL_MODEL`)

- `LINEAR` — classical multi-step progression
- `BRANCHED` — audience-segmented pathways
- `CONTENT_LED` — editorial discovery into contextual conversion
- `COMMERCE` — catalog → configuration → checkout
- `LEAD_GENERATION` — problem awareness → proof → inquiry
- `SELF_SERVICE` — documentation/tool exploration → account creation
- `AFFILIATE_OUTBOUND` — content discovery → comparison → merchant handoff
- `NONLINEAR` — freeform exploration with persistent conversion accessibility

For each stage record: `STAGE_NAME`, `VISITOR_QUESTION`, `PAGE_OR_COMPONENT`, `SUCCESS_SIGNAL`, `FAILURE_SIGNAL`, `MEASUREMENT_EVENT`, `OBSERVABLE` (`TRUE` / `FALSE` / `PARTIAL`).

A stage marked `OBSERVABLE = FALSE` is a legitimate finding, not a defect to be papered over. Record it and state why.

---

## 7. Event Taxonomy

Events must be **action based, stable, human-readable, implementation-neutral, versionable, non-duplicative, and directly traceable to a business or diagnostic purpose.**

Illustrative canonical vocabulary (**examples only — do not install every event on every website**):

```text
primary_cta_click          secondary_cta_click       lead_form_start
lead_form_submit           newsletter_signup         affiliate_outbound_click
product_view               checkout_start            purchase
demo_request               booking_start             booking_complete
resource_download          video_start               video_complete
search_use                 contact_click             phone_click
email_click                pricing_view              case_study_view
form_validation_error      navigation_select         page_view
experiment_exposure
```

*Rule:* Only measurable interactions justified by the actual project belong in the event model. An event that no one can name a decision for is deleted, not shipped.

---

## 8. Event Definition Contract

Every tracked event MUST carry a complete specification. An event missing any mandatory field is not implementable.

```text
event_name              Canonical lowercase_snake_case identifier
business_purpose        The decision this event informs. MANDATORY.
associated_kpi          PRIMARY_KPI | SECONDARY_KPI | DIAGNOSTIC_METRIC | GUARDRAIL_METRIC
conversion_level        MACRO | MICRO | DIAGNOSTIC
trigger                 Precise observable condition that fires the event
page_or_component       Where it lives, traceable to information-architecture.md
required_parameters     Parameters that must be present
optional_parameters     Parameters that may be present
deduplication_rule      How repeat firing is prevented
consent_dependency      REQUIRED | NOT_REQUIRED | UNASSESSED
implementation_method   How it is wired (data attribute, listener, callback, server confirmation)
verification_method     How its correctness is proven
event_version           Integer, incremented on contract change
```

**Events without a defined business or diagnostic purpose are prohibited.**

---

## 9. Event Naming Governance

- **Convention:** `lowercase_snake_case`, `object_action` ordering where natural.
- Names describe **what happened**, not what element was touched.

Prohibited vague names:

```text
click1        button_click     event_4
conversion_event             engagement2
```

### 9.1 Vendor Naming Mapping

Where an analytics vendor requires a different convention (e.g. GA4 reserved names, a platform requiring `camelCase`), create an explicit **mapping table** rather than corrupting Website Director's canonical vocabulary:

| Canonical Event | Vendor | Vendor Event Name | Notes |
| :--- | :--- | :--- | :--- |
| `lead_form_submit` | GA4 | `generate_lead` | GA4 recommended-event alias |
| `purchase` | GA4 | `purchase` | Identical |
| `primary_cta_click` | Plausible | `Primary CTA Click` | Plausible goal display name |

The canonical name remains authoritative in `measurement-plan.md`. The mapping is an implementation-boundary translation only.

---

## 10. CTA Traceability

**Every primary and meaningful secondary CTA in `content-plan.md` must be traceable to measurement architecture.** A CTA that exists in locked copy but has no measurement row is a gate failure.

Required traceability shape:

```text
CTA:              "Start Here"
BUSINESS PURPOSE: Lead user into qualification funnel
EVENT:            start_here_cta_click
KPI RELATION:     Secondary funnel KPI
DESTINATION:      /start-here
VERIFICATION:     Browser interaction + analytics/debug network evidence
```

*Rule:* All values must come from the project. **Never invent analytics events unrelated to the locked content structure.** If a CTA genuinely does not warrant measurement (e.g. a footer "back to top" control), record it as `MEASUREMENT: NOT_REQUIRED` with a reason — do not silently omit it.

---

## 11. Affiliate Website Support

Website Director explicitly supports affiliate business models.

### 11.1 The Three-State Distinction

```text
AFFILIATE CLICK
        ≠
AFFILIATE CONVERSION
        ≠
AFFILIATE COMMISSION
```

| State | What It Proves | Evidence Source |
| :--- | :--- | :--- |
| `affiliate_outbound_click` | A visitor left toward a merchant | First-party site instrumentation |
| `affiliate_conversion` | The merchant recorded a completed action | **Affiliate platform reporting only** |
| `affiliate_commission` | Money was actually earned and confirmed | **Affiliate platform payout data only** |

**Website Director must never fabricate downstream revenue attribution.** An outbound click is NEVER treated as a confirmed sale, conversion, or commission. If the affiliate platform provides no conversion feed, `affiliate_conversion` and `affiliate_commission` are recorded as `NOT_OBSERVABLE` with the reason stated.

### 11.2 Permitted Parameters

```text
merchant             Merchant identifier (non-personal)
placement            Where in the page the link sat
page                 Route the click originated from
offer_category       Category of the offer
link_identifier      Stable non-personal link ID
```

**Do NOT place personally identifying information in affiliate events.**

### 11.3 Outbound Integrity

Internal navigation must never be labelled as outbound affiliate activity. The outbound event fires only for links whose destination host is external AND which carry an affiliate relationship. Host comparison is by resolved hostname, not by substring matching.

---

## 12. Attribution & UTM Governance

Define a **bounded** attribution strategy. Attribution answers "where did this visitor come from" — nothing more.

### 12.1 Supported Parameters

| Parameter | Purpose | Casing |
| :--- | :--- | :--- |
| `utm_source` | Origin platform/publication | `lowercase` |
| `utm_medium` | Channel class (`email`, `cpc`, `social`, `referral`, `affiliate`) | `lowercase` |
| `utm_campaign` | Named campaign | `lowercase_snake_case` |
| `utm_content` | Creative/placement variant | `lowercase_snake_case` |
| `utm_term` | Paid keyword, where relevant | `lowercase` |

### 12.2 Governance Rules

- **Naming:** `utm_campaign` follows `lowercase_snake_case`. Campaign names are declared in the measurement plan before use, never improvised per-send.
- **Preservation:** Campaign parameters present on the landing URL are preserved across client-side route transitions for the session where they are required for legitimate business measurement.
- **Landing-page attribution:** The first landing route of a session is recorded as the attribution entry point.
- **Lead attribution:** Attribution may be associated with a lead **only** where the form/CRM legitimately supports carrying a non-personal campaign identifier.
- **Cross-domain:** Where a conversion completes on a different host (payment processor, booking platform), record the cross-domain requirement explicitly. If linker/decoration is unavailable, record the attribution boundary honestly rather than claiming continuity.
- **Affiliate boundary:** Attribution ends at the outbound handoff. Downstream merchant attribution is the merchant's data, not Website Director's.

### 12.3 Prohibitions

- Random or per-send improvised campaign naming
- Inconsistent casing across campaigns
- **Personally identifying information in UTM parameters** (never an email, name, phone, or user identifier)
- Fabricated attribution chains
- Silently dropping campaign parameters that are required for legitimate business measurement

---

## 13. Baseline & Target Governance

Website Director may record three separate values per KPI, and must never blur them:

| Field | Meaning | When Unknown |
| :--- | :--- | :--- |
| `BASELINE` | Measured historical performance | `BASELINE = UNKNOWN` |
| `TARGET` | Desired performance, owner-stated or explicitly inferred | `TARGET = NOT_SET` |
| `OBSERVED` | Actually measured after launch | `OBSERVED = NOT_YET_MEASURED` |

**Rules:**

- If no baseline exists, record `BASELINE = UNKNOWN`. Do not estimate one.
- If traffic is insufficient to establish a reliable conversion benchmark, state that explicitly (`INSUFFICIENT_TRAFFIC_FOR_BENCHMARK`).
- Do **not** invent claims such as *"Industry conversion rate is 4.2%"* unless credible evidence is actually available **and cited** with its source in the Provenance section.
- A target the owner did not state and Website Director inferred must be labelled `WEBSITE_DIRECTOR_INFERRED`.

---

## 14. CRO & Experiment Readiness

Website Director may identify conversion hypotheses, friction points, trust deficits, CTA ambiguity, unnecessary form fields, weak proof placement, funnel drop-off hypotheses, and possible future experiments.

### 14.1 Evidence Taxonomy

Every conversion claim carries exactly one label. **A hypothesis must never be presented as proven fact.**

| Label | Meaning |
| :--- | :--- |
| `OBSERVED` | Directly seen in the artifact or build (e.g. the form has 11 fields) |
| `EVIDENCE_SUPPORTED` | Supported by cited external research or the project's own data |
| `HYPOTHESIS` | A reasoned proposal with no confirming data |
| `EXPERIMENT_CANDIDATE` | A hypothesis worth testing when traffic and tooling permit |
| `PROVEN` | Validated by a completed, statistically sound experiment on this project |

### 14.2 Experimentation Boundaries

**Website Director must NOT automatically launch A/B tests.** Experiments require sufficient traffic, appropriate tooling, and deliberate authorization.

Every experiment begins with a structured hypothesis (`CRO_HYPOTHESIS`):

```text
OBSERVATION       = [Empirical drop-off or friction pattern]
PROBLEM           = [Underlying user obstacle, confusion, or unmet need]
HYPOTHESIS        = [Proposed cause-and-effect mechanism]
CHANGE            = [Exact visual, copy, or structural modification]
EXPECTED_BEHAVIOR = [Anticipated user reaction]
PRIMARY_METRIC    = [Direct measure of success]
GUARDRAIL_METRICS = [Indicators that must NOT degrade]
DECISION_RULE     = [Statistical and qualification criteria for action]
```

*Random A/B Testing Rule:* Testing arbitrary button colors, trivial font tweaks, or clickbait headlines without a structured hypothesis is strictly prohibited.

**Governance:**
- **Assignment Stability:** Variant assignment stable across reloads without flicker.
- **Exposure Requirement:** `experiment_exposure` fires ONLY when the qualifying variant is actively rendered, never on global page load.
- **Collision Detection:** Overlapping experiments on the same component or journey are flagged (`EXPERIMENT_COLLISION_CHECK`).
- **Sample Ratio Mismatch:** Allocation balance verified before analysis (`SAMPLE_RATIO_CHECK`).
- **State Engine:** `DRAFT` → `READY` → `RUNNING` → `PAUSED` → `COMPLETED` | `INVALIDATED`.
- **Result States:** `INSUFFICIENT_EVIDENCE`, `DIRECTIONAL_ONLY`, `STATISTICALLY_SUPPORTED`, `INCONCLUSIVE`, `INVALIDATED`.
- **Statistical Humility:** Synthetic or low-traffic tests never declare winners.

---

## 15. Privacy Boundary

A dedicated Security / Privacy / Compliance subsystem is future work. This protocol does **not** implement it, and does **not** give legal advice. It enforces these immediate invariants:

1. **No PII in analytics events by default.** Forbidden: email, phone, full name, address, free-text message bodies, SSN, date of birth.
2. **No passwords** in any payload, ever.
3. **No payment card data** in any payload, ever.
4. **No medical information** in any payload, ever.
5. **No sensitive form data** — capture field *category* on validation error, never field *value*.
6. **No secrets or analytics credentials committed to source control.** Measurement IDs that are legitimately public (e.g. a GA4 measurement ID) are still recorded in the plan as configuration references, never as committed API keys, secrets, or service-account credentials.
7. **Consent dependency recorded.** Any tracking requiring consent records `consent_dependency = REQUIRED`.
8. **Unknown consent requirements remain `UNASSESSED`** — never guessed, never defaulted to `NOT_REQUIRED`.
9. **Deferred activation supported.** Analytics strategy must be able to specify "planned, activation deferred pending privacy review" without that being recorded as failure or as completion.
10. **Session replay `DISABLED` by default.** Requires explicit owner justification and strict masking policy if ever proposed.

---

## 16. Locks Always Win

Conversion & Analytics Intelligence may **NOT** silently mutate approved information architecture, locked copy, CTA wording, design tokens, motion direction, or any owner-approved decision.

If measurement reveals a structural problem requiring a locked change:

```text
HALT.
Generate a locked-change request.
Present it to the owner.
Do not silently edit the website to make analytics easier.
```

A locked-change request records: the locked artifact affected, the measurement problem observed, the evidence label (§14.1), the proposed change, and the consequence of not changing. The owner decides.

---

## 17. State Model & Semantics

### 17.1 The `measurement{}` Object

`measurement{}` in `site-profile.json` is the sole authoritative measurement state. See §18 for the schema.

### 17.2 What `measurement.complete = true` Means

It means **all** of the following:

- The business conversion model is identified
- A KPI hierarchy exists (primary, secondary, diagnostic separated)
- Required events are defined under the §8 Event Definition Contract
- CTA/event traceability exists for every primary and meaningful secondary CTA
- Attribution requirements are defined where applicable
- Provider / implementation approach is defined **or formally blocked**
- Verification requirements exist
- The measurement plan is complete enough for implementation

### 17.3 What It Does NOT Mean

`measurement.complete = true` **NEVER** means production analytics have been observed working.

| Flag | Certifies | Set When |
| :--- | :--- | :--- |
| `measurement.complete` | A plan exists and is implementable | End of Phase 6.5 |
| `measurement.implementation_verified` | Instrumentation was verified in the built artifact | Post-build (Phase 11/12), by browser + network evidence |
| `measurement.production_verified` | Events were observed in the real production analytics environment | Post-deployment, by owner-supplied evidence |

These three states are permanently distinct. Setting a later flag never implies an earlier one was skipped, and setting an earlier one never implies a later one.

### 17.4 `measurement.mode` Values

| Value | Meaning |
| :--- | :--- |
| `not_evaluated` | Phase 6.5 has not run |
| `planning` | Phase 6.5 in progress |
| `standard` | Full measurement architecture defined and implementable |
| `blocked` | Strategy defined, implementation capability unavailable — see §19 |
| `exception` | Bounded exception applied — see §20 |
| `not_required` | Non-commercial surface with a recorded exception |

---

## 18. `site-profile.json` Schema

```json
"measurement": {
  "complete": false,
  "mode": null,
  "business_objective": null,
  "provider": null,
  "implementation_mode": null,
  "primary_kpi": null,
  "secondary_kpis": [],
  "funnel_model": null,
  "events_defined": [],
  "event_schema_version": "1.0.0",
  "cta_traceability_complete": false,
  "utm_strategy_defined": false,
  "attribution_boundaries_defined": false,
  "affiliate_model": "NOT_APPLICABLE",
  "baseline_status": "UNKNOWN",
  "consent_dependency": "UNASSESSED",
  "pii_check": "not_evaluated",
  "dark_pattern_check": "not_evaluated",
  "experimentation_required": false,
  "experiment_plan_ready": false,
  "session_replay": "DISABLED",
  "implementation_verified": false,
  "production_verified": false,
  "blocked_reason": null,
  "exception": {
    "applied": false,
    "reason": null
  }
}
```

**Field constraints:**

- `mode` — one of §17.4 values
- `provider` — `null` | `GA4` | `GTM` | `PLAUSIBLE` | `POSTHOG` | `MATOMO` | `FATHOM` | `FIRST_PARTY` | `CUSTOM_EVENT_PIPELINE` | `NOT_SELECTED` | `NO_ANALYTICS`
- `implementation_mode` — `null` | `DIRECT_SNIPPET` | `TAG_MANAGER` | `SERVER_SIDE` | `FIRST_PARTY_ENDPOINT` | `DEFERRED`
- `affiliate_model` — `NOT_APPLICABLE` | `CLICK_ONLY` | `CLICK_AND_PLATFORM_REPORTED_CONVERSION`
- `baseline_status` — `UNKNOWN` | `RECORDED` | `INSUFFICIENT_TRAFFIC_FOR_BENCHMARK`
- `consent_dependency` — `UNASSESSED` | `REQUIRED` | `NOT_REQUIRED`
- `pii_check` / `dark_pattern_check` — `not_evaluated` | `PASS` | `FAIL`

`measurement{}` contains **no lock boolean**. Exactly 5 owner locks remain.

---

## 19. Blocked Mode

`measurement.mode = "blocked"` applies where the measurement **strategy is known** but required implementation capability is unavailable.

Legitimate blockers:

- Analytics provider not yet selected by the owner
- Owner credentials unavailable (and must not be requested or used)
- External system inaccessible
- Required integration not yet configured
- Privacy review pending

**Rules:**

- The measurement plan remains fully usable — events, KPIs, funnel, CTA traceability, and UTM strategy are all still authored.
- `measurement.blocked_reason` records the specific blocker in plain language.
- `measurement.complete` MAY be `true` in blocked mode **if and only if** the plan itself is complete and the blocker is purely an implementation-capability blocker (§17.2 explicitly permits "provider/implementation approach is defined **or formally blocked**").
- `measurement.implementation_verified` and `measurement.production_verified` remain `false`.
- **Do not fabricate success.** A blocked integration stays honestly blocked through QA and production checklist reporting.

---

## 20. Exception Mode

Bounded exceptions are permitted for surfaces where conversion measurement is genuinely inapplicable:

- Private prototype
- Offline demo
- Disposable visual experiment
- Explicitly non-commercial internal surface

A measurement exception must be **explicit, documented, justified, and visible in `site-profile.json`** (`measurement.exception.applied = true` with a substantive `reason`).

> **Never silently skip conversion measurement for a commercial public-facing website.**

An exception is never applied because measurement was difficult, because the provider was unknown (that is `blocked`, §19), or because the phase was skipped.

---

## 21. Readiness Gate: `[CONVERSION_MEASUREMENT_COMPLETE]`

The gate engages when **all** of the following hold:

```text
BUSINESS_OBJECTIVE_DEFINED        = TRUE
PRIMARY_KPI_DEFINED               = TRUE
KPI_HIERARCHY_DEFINED             = TRUE
FUNNEL_MODEL_DEFINED              = TRUE
EVENT_CONTRACTS_COMPLETE          = TRUE   (every event satisfies §8)
CTA_TRACEABILITY_COMPLETE         = TRUE   (every primary/meaningful secondary CTA resolved)
ATTRIBUTION_DEFINED               = TRUE | NOT_APPLICABLE
PROVIDER_RESOLVED                 = TRUE | FORMALLY_BLOCKED
CONSENT_DEPENDENCY_RECORDED       = TRUE   (REQUIRED | NOT_REQUIRED | UNASSESSED — all valid; unrecorded is not)
PII_CHECK                         = PASS
DARK_PATTERN_CHECK                = PASS
VERIFICATION_PLAN_DEFINED         = TRUE
BASELINE_GOVERNANCE_RECORDED      = TRUE
```

On engagement: set `measurement.complete = true` and `measurement.mode` to `standard` or `blocked`.

For non-commercial surfaces with a recorded exception: `measurement.mode = "exception"` or `"not_required"`, `measurement.exception.applied = true`.

`[CRO_MEASUREMENT_READY]` at Phase 8.97 is a downstream sub-gate that reads this same state plus experimentation fields. It writes no independent completion flag.

---

## 22. Verification Model

### 22.1 Implementation Verification (`measurement.implementation_verified`)

Performed post-build, before production sign-off. For each event:

- The event fires on the specified trigger
- It fires **exactly once** per qualifying interaction
- The event name matches `measurement-plan.md` exactly
- Required parameters are present
- No PII appears in the payload
- Deduplication holds under rapid repeat interaction
- SPA route transitions emit exactly one `page_view` (see §23)
- Form success is distinguished from form start
- A server-rejected form emits **no** success conversion event

Evidence: browser interaction plus analytics debug/network capture, recorded in the project's evidence directory.

### 22.2 Production Verification (`measurement.production_verified`)

Performed only after deployment, only with owner-supplied evidence from the real analytics environment. Website Director never sets this flag from inference, and never accesses owner analytics accounts to obtain it.

If production evidence is unavailable, the flag stays `false` and the status is reported as `NOT_YET_VERIFIED` — never as passing.

---

## 23. Subsystem Integration Boundaries

1. **Page Experience & View Transitions (V2.3):** A single route transition must emit exactly one `page_view`. Document navigation, View Transitions callbacks (`pagereveal`, `pageswap`), and `popstate` history must deduplicate route telemetry (`PAGE_VIEW_SOURCE_OF_TRUTH = ROUTE_SETTLED`).
2. **Immersive Web / Three.js (V2.1):** Never track render-loop frames or camera ticks. Track only intentional milestones (`3d_inspection_start`, `3d_hotspot_select`).
3. **Rive Interactive Motion (V2.2):** Never track continuous idle loops or hover flicker. Track only meaningful state completions (`configurator_state_complete`).
4. **Forms:** Track `form_view`, `lead_form_start`, `form_validation_error`, and `lead_form_submit`. Never capture field values or keystrokes. Deduplicate submit handlers so rapid clicks cannot produce multiple conversion events.
5. **Signature Choreography (V2.5.1):** Scroll choreography progress is not a conversion signal and is not instrumented as one.
6. **Client Handoff (V2.5):** The measurement plan and its blocked/exception status are handoff deliverables. A blocked provider is disclosed to the client, never hidden.

---

## 24. Gauntlet Integration

**No new critic is created.** The existing Website Gauntlet **Conversion Critic** and **CRO & Analytics Critic** are the qualitative authority, enriched to inspect:

- Whether measurement actually supports the intended business outcome
- Whether any critical CTA lacks a measurement definition
- Whether events are meaningless vanity instrumentation
- Whether the declared funnel is genuinely observable

`BUILDER != CRITIC` is maintained. No parallel Gauntlet state is created; findings flow through the existing `gauntlet{}` object.

---

## 25. Required Deliverables

| Artifact | Purpose |
| :--- | :--- |
| `templates/measurement-plan.md` | The authoritative 19-section measurement plan |
| `templates/analytics-event-manifest.json` | Machine-readable event contract manifest |
| `templates/experiment-brief.md` | Per-experiment hypothesis brief (only when experimentation is authorized) |
| `site-profile.json` → `measurement{}` | Machine-readable state |

---

## 26. Backward Compatibility

- A pre-V2.6 project whose `site-profile.json` has no `measurement{}` object **remains valid**. Tooling treats it as absent without raising a schema exception.
- Projects carrying the legacy `cro{}` object remain valid and readable. `cro{}` is **grandfathered, read-only**, and is not migrated automatically.
- **Frozen historical pilots are not retrofitted.** Do not mutate existing frozen Website Director pilot outputs merely to make their state files look current.
- New Website Director projects use V2.6 `measurement{}` behavior.
- Major new work on an older project may enter V2.6 measurement planning when that project is **deliberately reopened** by the owner.
