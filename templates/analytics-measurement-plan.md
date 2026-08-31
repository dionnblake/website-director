# ANALYTICS & CRO MEASUREMENT PLAN — SUPERSEDED

> **Status:** SUPERSEDED as of V2.6.0. Retained for existing V2.4/V2.5 projects only.  
> **Superseded by:** [measurement-plan.md](measurement-plan.md)  
> **New projects MUST use `templates/measurement-plan.md`.** It adds the Event Definition Contract, CTA traceability matrix, attribution/UTM governance, affiliate measurement integrity, baseline governance, and the separation of planning / implementation verification / production verification.

> **Project Name:** [Project Name]  
> **Schema Version:** 2.4.0  
> **Status:** Draft / Ready  
> **Governance (superseded):** `CRO-ANALYTICS-EXPERIMENTATION-PROTOCOL.md` → now `CONVERSION-ANALYTICS-PROTOCOL.md`

---

## 1. Business & Visitor Outcomes

- **PRIMARY_BUSINESS_OUTCOME:** [e.g. Generate qualified enterprise architecture inquiries]
- **SECONDARY_BUSINESS_OUTCOME:** [e.g. Establish category leadership through technical publication reach]
- **PRIMARY_VISITOR_OUTCOME:** [e.g. Evaluate technical capability and schedule architectural assessment]
- **PRIMARY_CONVERSION:** [e.g. consultation_submit_success]
- **SECONDARY_CONVERSIONS:** [e.g. pricing_view, whitepaper_download, case_study_view]
- **SUCCESS_CRITERIA:** [e.g. Form submissions matching qualification criteria]

---

## 2. Conversion Hierarchy

| Level | Event Name | Trigger | Value / Decision Use |
| :--- | :--- | :--- | :--- |
| **MACRO** | `consultation_submit_success` | Validated lead form submission | Measures primary pipeline generation |
| **MICRO** | `consultation_start` | First user focus/interaction in form | Measures intent initiation rate |
| **MICRO** | `pricing_view` | Pricing component viewed | Evaluates commercial consideration |
| **MICRO** | `case_study_view` | Portfolio/case study detail engaged | Evaluates proof/evidence consumption |
| **DIAGNOSTIC** | `form_validation_error` | Submission blocked by validation | Identifies form UX friction points |
| **DIAGNOSTIC** | `navigation_select` | Menu or header link clicked | Analyzes navigation path efficiency |

---

## 3. Funnel & Journey Architecture

- **FUNNEL_MODEL:** `LEAD_GENERATION` | `LINEAR` | `BRANCHED` | `CONTENT_LED` | `NONLINEAR`

| Stage | Visitor Question | Target Component / URL | Success Signal | Failure Signal | Tracked Event |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Orientation** | "What does this company do and does it fit my problem?" | Hero (`/`) | Scroll into value proposition | Immediate bounce | `page_view` |
| **2. Capability** | "What services or solutions do they provide?" | Services (`/services.html`) | Exploration of service tiers | Abandonment | `navigation_select` |
| **3. Proof** | "Have they solved this for peers with verifiable rigor?" | Case Study (`/case-study.html`) | Full case study engagement | Disinterest | `case_study_view` |
| **4. Consideration** | "What is the engagement model and investment level?" | Pricing Section | Inspection of tiers | Drop-off | `pricing_view` |
| **5. Intent** | "How do we begin a qualified evaluation?" | Lead Form (`/consultation.html`) | Form field interaction | Form bounce | `consultation_start` |
| **6. Conversion** | "Is my consultation request confirmed?" | Form Confirmation State | Successful validation & submission | Validation loop | `consultation_submit_success` |

---

## 4. Event Taxonomy & Schema Manifest

| Metric ID | Event Name | Version | Category | PII Allowed | Guardrails / Properties |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `M-01` | `page_view` | 1 | Navigation | `false` | `page_path`, `page_title`, `referrer` |
| `M-02` | `navigation_select` | 1 | Navigation | `false` | `target_path`, `menu_location` |
| `M-03` | `pricing_view` | 1 | Consideration | `false` | `component_id`, `viewport_ratio` |
| `M-04` | `case_study_view` | 1 | Proof | `false` | `study_id`, `client_sector` |
| `M-05` | `consultation_start` | 1 | Intent | `false` | `form_id`, `source_intent` |
| `M-06` | `form_validation_error` | 1 | Diagnostic | `false` | `form_id`, `error_field_category` (NO INPUT VALUES) |
| `M-07` | `consultation_submit_success` | 1 | Conversion | `false` | `form_id`, `qualification_tier` |
| `M-08` | `experiment_exposure` | 1 | Experiment | `false` | `experiment_id`, `variant_id` |

---

## 5. Privacy, Data Minimization & Security

- **PII_IN_ANALYTICS:** `0` (Strictly zero personal data in payloads)
- **DATA_MINIMIZATION:** Collect only behavioral signals required for defined metrics.
- **ANALYTICS_MODE:** `PRIVACY_PRESERVING` | `ESSENTIAL_ONLY` | `CONSENT_GATED`
- **SESSION_REPLAY:** `DISABLED` (High-sensitivity session recording prohibited by default)
- **ANALYTICS_PROVIDER:** `NO_ANALYTICS` | `PRIVACY_FOCUSED_ANALYTICS` | `CUSTOM_EVENT_PIPELINE` | `GA4` (Configured intentionally, zero real credentials during development)
- **FAILURE_RESILIENCE:** Site functionality 100% independent of analytics script execution.

---

## 6. Optimization & Experimentation Boundaries

- **DARK_PATTERN_CHECK:** `PASS` (No fake timers, no disguised ads, no confirmshaming)
- **BRAND_GUARDRAILS:** High visual craft, layout discipline, and accessibility cannot be compromised for click volume.
- **STATISTICAL_POLICY:** Inconclusive or synthetic samples are marked `INSUFFICIENT_EVIDENCE`.
