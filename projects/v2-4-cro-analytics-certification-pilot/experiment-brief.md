# EXPERIMENT BRIEF: CONSULTATION POSITIONING V1

> **Project:** Northstar Performance Lab  
> **Schema Version:** 2.4.0  
> **Experiment ID:** `consultation-positioning-v1`  
> **Status:** `RUNNING` (Synthetic Certification State)  
> **Governance:** `CRO-ANALYTICS-EXPERIMENTATION-PROTOCOL.md`

---

## 1. Hypothesis & Rationale

- **OBSERVATION:** Enterprise leaders visiting the executive assessment portal explore diagnostic case studies but demonstrate hesitancy before initiating an inquiry.
- **PROBLEM:** High-discernment C-suite visitors fear aggressive sales follow-up and lack certainty regarding mutual qualification fit.
- **HYPOTHESIS:** Framing the primary CTA around mutual fit assessment ("See If We're a Fit") rather than direct commitment ("Request Strategy Session") will lower psychological barrier while maintaining executive lead quality.
- **CHANGE:** Update Hero CTA copy and subtitle to emphasize diagnostic qualification fit.
- **EXPECTED_BEHAVIOR:** Increase qualified consultation start rate without degrading lead qualification tier.

---

## 2. Variant Definitions

- **CONTROL:** Primary CTA button label: `"Request Strategy Session"`; Subtitle: `"Confidential 45-minute diagnostic session with managing partners."`
- **VARIANT (`challenger`):** Primary CTA button label: `"See If We're a Fit"`; Subtitle: `"Evaluate executive diagnostic fit before confidential booking."`
- **AUDIENCE:** All incoming visitors to Northstar Lab overview.
- **ASSIGNMENT_STRATEGY:** `DETERMINISTIC_LOCAL` (`?variant=control` or `?variant=challenger`, default `control`).

---

## 3. Telemetry & Metrics

- **EXPOSURE_EVENT:** `experiment_exposure` (Payload: `experiment_id: "consultation-positioning-v1"`, `variant_id: "control" | "challenger"`). Fired once when hero CTA is rendered in viewport.
- **PRIMARY_METRIC:** `consultation_start_rate`
- **SECONDARY_METRICS:** `case_study_view_rate`, `pricing_view_rate`
- **GUARDRAIL_METRICS:**
  - `Lead Quality Tier`: Percentage of submissions matching Tier 1 C-Suite criteria must remain $\ge 85\%$.
  - `Form Validation Error Rate`: Must remain $\le 10\%$.
  - `Page Performance`: 60 FPS, LCP $< 1.2\text{s}$, zero CLS.
  - `Brand Perception & Trust`: Monochrome editorial aesthetic and dignity maintained.

---

## 4. Execution & Stopping Criteria

- **SAMPLE_SIZE_TARGET:** 2,400 qualified executive sessions per variant.
- **START_CRITERIA:** SRM check passed, PII check passed, dark pattern check passed.
- **STOP_CRITERIA:** Sample target reached OR severe guardrail failure triggered.
- **SYNTHETIC_EXPERIMENT_ASSIGNMENT:** `TRUE`

---

## 5. Result Interpretation & Decision Record

- **RESULT:** `INSUFFICIENT_EVIDENCE` (Deterministic certification fixture has synthetic traffic and cannot establish a real-world statistical winner).
- **SAMPLE_RATIO_CHECK:** `PASS`
- **NOVELTY_RISK:** `LOW`
- **DECISION:** Certification fixture certified; production deployment deferred until real live traffic and owner authorization.
