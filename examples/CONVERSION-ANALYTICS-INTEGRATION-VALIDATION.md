# CONVERSION & ANALYTICS INTELLIGENCE — INTEGRATION VALIDATION

> **Subsystem Version:** 2.6.0  
> **Governance:** [CONVERSION-ANALYTICS-PROTOCOL.md](../CONVERSION-ANALYTICS-PROTOCOL.md)  
> **Gate Under Test:** `[CONVERSION_MEASUREMENT_COMPLETE]`  
> **Mode:** Planning-only validation. No analytics properties were created, no containers or advertising accounts modified, no pixels installed, nothing deployed, no owner credentials used, no production data transmitted.

---

## 0. Method & Scope

Each scenario exercises one invariant of the subsystem against a synthetic project profile. A scenario **passes** only when the subsystem produces the correct state *and* refuses the incorrect state.

**What this validation proves:** the protocol's decision rules, state semantics, and refusal behavior are internally consistent and produce the specified `measurement{}` values.

**What it does not prove:** that any built website's instrumentation works. That is `measurement.implementation_verified`, established per-project by browser and network evidence, and is out of scope here by design — asserting otherwise would violate the very invariant under test (§2.3).

---

## Scenario A — Lead-Generation Site, GA4/GTM Available

**Profile:** B2B consultancy. Primary conversion is a qualified consultation request. Owner has an existing GA4 property and a GTM container. Build has not started.

**Subsystem execution:**

| Step | Result |
| :--- | :--- |
| `BUSINESS_OBJECTIVE` | `CONSULTATION` |
| `PRIMARY_KPI` | Qualified consultation requests per month |
| Secondary KPIs | `pricing_view` rate, `lead_form_start` rate, case study engagement |
| Vanity metrics rejected | Pageviews, aggregate time on page, scroll depth |
| `FUNNEL_MODEL` | `LEAD_GENERATION` |
| Events defined | `page_view`, `navigation_select`, `pricing_view`, `case_study_view`, `lead_form_start`, `form_validation_error`, `lead_form_submit` |
| Event contracts | All 13 fields populated per §8 |
| CTA traceability | 4 CTAs traced; 1 footer control recorded `MEASUREMENT: NOT_REQUIRED` |
| Vendor mapping | `lead_form_submit` → GA4 `generate_lead` (canonical name retained in app code) |
| Attribution | UTM conventions declared; `utm_campaign` in `lowercase_snake_case` |
| Consent | `REQUIRED` (owner confirmed EU traffic) |

**Expected terminal state (before implementation):**

```json
"measurement": {
  "complete": true,
  "mode": "standard",
  "provider": "GA4",
  "implementation_mode": "TAG_MANAGER",
  "implementation_verified": false,
  "production_verified": false
}
```

**Result:** ✅ **PASS**

- `measurement.complete = true` — the plan is complete and implementable.
- `implementation_verified = false` — no build exists, therefore no instrumentation evidence exists.
- `production_verified = false` — nothing deployed, no owner-supplied production evidence.
- The subsystem **refused** to set either verification flag from the fact that a provider was available. Provider availability is not evidence of working instrumentation.

---

## Scenario B — Affiliate Content Site

**Profile:** Product comparison publisher. Revenue is affiliate commission. The affiliate network provides a click report but **no** conversion postback to the site.

**Subsystem execution:**

| State | Event / Source | Observable? | Recorded As |
| :--- | :--- | :---: | :--- |
| Affiliate click | `affiliate_outbound_click` | ✅ Yes | First-party instrumentation |
| Affiliate conversion | — | ❌ No | `NOT_OBSERVABLE` — network provides no postback |
| Affiliate commission | — | ❌ No | `NOT_OBSERVABLE` — payout data lives in the network dashboard |

**Outbound event parameters:** `merchant`, `placement`, `page`, `offer_category`, `link_identifier`. Zero PII.

**Refusal tests:**

| Attempt | Subsystem Response |
| :--- | :--- |
| Set `PRIMARY_KPI` = "affiliate revenue" derived from click volume | ❌ **REJECTED.** Revenue is not observable from clicks. `PRIMARY_KPI` set to outbound click-through to qualified merchants; revenue recorded as `NOT_OBSERVABLE`. |
| Emit `affiliate_conversion` on outbound click | ❌ **REJECTED.** §11.1 — a click is not a conversion. |
| Estimate commission as `clicks × assumed_rate × assumed_AOV` | ❌ **REJECTED.** §2.4 anti-fabrication. Recorded `BASELINE = UNKNOWN`. |
| Fire outbound event on an internal `/reviews/` link | ❌ **REJECTED.** §11.3 — hostname resolves internal. |

**Result:** ✅ **PASS** — `CLICK ≠ CONVERSION ≠ COMMISSION` enforced. `affiliate_model = "CLICK_ONLY"`. The subsystem refused to infer the latter two states from a click.

---

## Scenario C — Commercial Site, No Analytics Provider Selected

**Profile:** Regional services business, public-facing and commercial. Owner has not chosen an analytics vendor and has no existing property.

**Subsystem execution:** The full measurement architecture is authored regardless — business objective, KPI hierarchy, observable funnel, event dictionary with complete contracts, CTA matrix, UTM conventions, verification plan. Only the *implementation binding* is unresolved.

**Expected terminal state:**

```json
"measurement": {
  "complete": true,
  "mode": "blocked",
  "provider": "NOT_SELECTED",
  "implementation_mode": "DEFERRED",
  "blocked_reason": "Owner has not selected an analytics provider. Event contracts are vendor-neutral and portable to any provider on selection.",
  "implementation_verified": false,
  "production_verified": false,
  "exception": { "applied": false, "reason": null }
}
```

**Refusal tests:**

| Attempt | Subsystem Response |
| :--- | :--- |
| Apply an exception because no provider exists | ❌ **REJECTED.** §20 — an unresolved provider is `blocked`, not `exception`. This is a commercial public-facing site. |
| Skip Phase 6.5 entirely | ❌ **REJECTED.** §20 — measurement is never silently skipped for a commercial site. |
| Default `provider` to GA4 to unblock | ❌ **REJECTED.** §2.8 provider neutrality. Vendor selection is the owner's. |
| Report the site as measurement-ready for launch | ❌ **REJECTED.** Blocked status surfaces through QA, production checklist §5.2.9, and client handoff. |

**Result:** ✅ **PASS** — architecture created, provider status honest, no fabricated implementation success. `complete = true` is correct here because §17.2 explicitly permits "provider/implementation approach is defined **or formally blocked**."

---

## Scenario D — Internal Non-Commercial Prototype

**Profile:** Disposable internal visual experiment. Never public, no commercial purpose, no visitors outside the team.

**Expected terminal state:**

```json
"measurement": {
  "complete": true,
  "mode": "exception",
  "provider": "NO_ANALYTICS",
  "implementation_verified": false,
  "production_verified": false,
  "exception": {
    "applied": true,
    "reason": "Disposable internal visual experiment. Not public-facing, no commercial objective, no visitor population. Measurement is inapplicable rather than deferred."
  }
}
```

**Refusal tests:**

| Attempt | Subsystem Response |
| :--- | :--- |
| Apply the same exception to a public marketing page | ❌ **REJECTED.** §20 — commercial public-facing surfaces never qualify. |
| Apply exception with reason `null` | ❌ **REJECTED.** §20 requires explicit, documented, justified, and visible in `site-profile.json`. |
| Apply exception because measurement was time-consuming | ❌ **REJECTED.** §20 — difficulty is not an exception. |

**Result:** ✅ **PASS** — bounded exception applied without corrupting the workflow. Phases 7 onward proceed normally.

---

## Scenario E — Existing Pre-V1.8 Frozen Project

**Profile:** `projects/v1-1-architecture-pilot/` — `schema_version = 1.1.0`, frozen certified baseline. No `measurement{}`, no `cro{}`, no `seo{}`.

**Subsystem execution:**

| Check | Result |
| :--- | :--- |
| Schema validation against V2.6 tooling | ✅ Valid — `measurement{}` absence treated as absent, no exception raised (§26) |
| Project marked corrupt or non-compliant? | ❌ No |
| Retrofitted with `measurement{}`? | ❌ No — frozen pilots are not mutated |
| Five owner locks intact? | ✅ Yes |

**Refusal tests:**

| Attempt | Subsystem Response |
| :--- | :--- |
| Inject `measurement{}` to make state files look current | ❌ **REJECTED.** §26 — do not mutate frozen pilot outputs for cosmetic currency. |
| Fail validation because `measurement{}` is missing | ❌ **REJECTED.** §26 — absence is valid for pre-V2.6 projects. |
| Migrate `cro{}` → `measurement{}` automatically on a V2.4 project | ❌ **REJECTED.** §26 — `cro{}` is grandfathered read-only; migration requires deliberate owner reopening. |

**Result:** ✅ **PASS** — backward compatibility preserved. Verified physically in §2 of the Repository Integrity Report below (frozen project files unmodified).

---

## Scenario F — Event Attempts to Include PII

**Profile:** Builder proposes enriching the lead conversion event so sales can identify the lead in analytics.

**Proposed (rejected) payload:**

```json
{
  "event_name": "lead_form_submit",
  "email": "buyer@example.com",
  "full_name": "A. Buyer",
  "phone": "+1-555-0100",
  "message": "We need help with our Q3 rollout"
}
```

**Subsystem response:** ❌ **REJECTED** at four independent layers:

| Layer | Rule |
| :--- | :--- |
| Protocol §15.1 | No PII in analytics events by default — email, phone, full name, free-text body all forbidden |
| Event manifest `pii_governance.forbidden_fields` | `email`, `phone`, `full_name`, `message` explicitly enumerated |
| Implementation contract §2.5.3 / prohibition #14 | Builder may not add parameters carrying PII |
| Production checklist §5.2.8 | Network payloads inspected, not just source code |

**Corrected specification:** `lead_form_submit` carries `form_id` and `qualification_tier` only. Lead identity lives in the CRM, which is the correct system for it. `measurement.pii_check` cannot be set `PASS` until the violation is removed.

**Additional refusal:** the same rejection applies to placing an email in a `utm_content` parameter (§12.3).

**Result:** ✅ **PASS** — PII rejected and flagged, with a compliant alternative specified rather than the requirement simply denied.

---

## Scenario G — Conversion Fires on Click Despite Server Rejection

**Profile:** Build emits `lead_form_submit` in the button's click handler. The server rejected the submission (validation failure, HTTP 422). No lead was created.

**Observed behavior:**

```text
User clicks "Request Consultation"
  → lead_form_submit  EMITTED          ← conversion recorded
  → POST /api/lead    422 Unprocessable ← no lead created
  → Error shown to user
```

**Subsystem response:** ❌ **FAIL — verification blocked.**

| Layer | Violated Rule |
| :--- | :--- |
| Protocol §22.1 | "A server-rejected form emits **no** success conversion event" |
| Measurement plan §2 | Success definition is `SERVER_CONFIRMED`; the event fired on click instead |
| Implementation contract §2.5.10 | "Firing a conversion on click while the server rejected the submission is a contract violation and a QA failure" |
| Implementation contract §2.5.2 | `MACRO` events fire on confirmed success wherever technically determinable |
| Production checklist §5.2.4 | "Failed forms do not generate successful conversion events" |
| Prohibition #15 | False conversion signals |

**Consequences enforced:**

- `measurement.implementation_verified` **cannot** be set `true`.
- Production checklist §5.2 fails; deployment authorization is withheld.
- Gauntlet Critic 4.14 raises the defect *"success conversion event fires where the server actually rejected the submission."*
- Required remediation: move emission to the confirmed-success callback; emit `form_validation_error` on the rejection path.

**Result:** ✅ **PASS** (validation correctly **failed** the implementation) — the conversion-success event must correspond to actual successful completion where technically determinable.

---

## Scenario Summary

| # | Scenario | Invariant Under Test | Result |
| :-: | :--- | :--- | :---: |
| A | Lead-gen, GA4/GTM available | Planning ≠ verification | ✅ PASS |
| B | Affiliate content site | `CLICK ≠ CONVERSION ≠ COMMISSION` | ✅ PASS |
| C | Commercial, no provider | Blocked mode honesty | ✅ PASS |
| D | Internal prototype | Bounded exception | ✅ PASS |
| E | Pre-V1.8 frozen project | Backward compatibility | ✅ PASS |
| F | PII in event payload | Privacy boundary | ✅ PASS |
| G | Conversion on rejected submit | Verification integrity | ✅ PASS |

**7 / 7 scenarios passed.**

---

## Repository Integrity Report

### 1. Single Completion Flag

Searched the framework for any second, independently-writable measurement completion flag.

- `measurement.complete` — **the only** readiness flag for `[CONVERSION_MEASUREMENT_COMPLETE]`.
- Legacy `cro.status` removed from `templates/site-profile.json`; retained only as grandfathered read-only state in existing projects, documented in `SKILL.md` §5.11 and the superseded protocol's migration map.
- `[CRO_MEASUREMENT_READY]` (Phase 8.97) reads the same `measurement{}` object and writes no independent completion flag.

**Verdict:** ✅ No duplicate measurement completion flags.

### 2. Five Owner Locks

```text
design_direction_locked
information_architecture_locked
content_structure_locked
design_system_locked
motion_direction_locked
```

`measurement{}` contains **no** lock boolean. `[CONVERSION_MEASUREMENT_COMPLETE]` is documented as a readiness gate in `CONVERSION-ANALYTICS-PROTOCOL.md` §2.2, `SKILL.md` (Phase 6.5 + §5.11), `README.md` §5, and `AGENTS.md` governance rule 10.

**Verdict:** ✅ Exactly five owner locks preserved.

### 3. Frozen Projects

No file under `projects/` was created, modified, or deleted by this upgrade.

**Verdict:** ✅ Frozen pilots untouched.

### 4. Secrets

No API keys, tokens, measurement IDs, or service-account credentials were added. Prohibitions recorded at protocol §15.6, implementation contract §2.5.6 and prohibition #16, and production checklist §5.2.8.

**Verdict:** ✅ No secrets added.

### 5. Existing Architecture Intact

SEO Intelligence, Visual Research, Design Intelligence, Motion/GSAP, Asset Director, Immersive Web, Rive, Page Experience, Signature Choreography, Client Handoff, Impeccable Engine, and the Website Gauntlet remain intact. The Gauntlet Conversion Critic (4.3) and CRO & Analytics Critic (4.14) were **enriched, not duplicated** — no new critic was created and no parallel Gauntlet state was introduced. `BUILDER != CRITIC` maintained.

**Verdict:** ✅ Existing architecture preserved.
