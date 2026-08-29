# EXPERIMENT BRIEF

> **Project Name:** [Project Name]  
> **Schema Version:** 2.4.0  
> **Experiment ID:** [experiment-id-slug]  
> **Status:** `DRAFT` | `READY` | `RUNNING` | `PAUSED` | `COMPLETED` | `INVALIDATED`  
> **Governance:** `CRO-ANALYTICS-EXPERIMENTATION-PROTOCOL.md`

---

## 1. Hypothesis & Rationale

- **OBSERVATION:** [Empirical drop-off or friction observed in behavioral data or user testing]
- **PROBLEM:** [Underlying obstacle, confusion, or unmet expectation experienced by visitor]
- **HYPOTHESIS:** [Clear cause-and-effect statement: If we change X, then Y will happen because Z]
- **CHANGE:** [Specific design, structural, or copy modification implemented in the challenger variant]
- **EXPECTED_BEHAVIOR:** [Predicted visitor reaction]

---

## 2. Variant Definitions

- **CONTROL:** [Description of baseline design / copy / component]
- **VARIANT:** [Description of challenger variant design / copy / component]
- **AUDIENCE:** [Target traffic segment or qualifying condition, e.g. all qualified desktop & mobile visitors]
- **ASSIGNMENT_STRATEGY:** `DETERMINISTIC_LOCAL` | `STABLE_ANONYMOUS_ID` | `SERVER_ASSIGNED`

---

## 3. Telemetry & Metrics

- **EXPOSURE_EVENT:** `experiment_exposure` (Fired strictly when qualifying variant element is rendered in viewport)
- **PRIMARY_METRIC:** [Direct conversion rate metric testing the hypothesis, e.g. `qualified_consultation_start_rate`]
- **SECONDARY_METRICS:** [Supporting indicators, e.g. `pricing_view_rate`, `case_study_scroll_depth`]
- **GUARDRAIL_METRICS:**
  - `Lead Quality`: Must not degrade qualification criteria
  - `Form Error Rate`: Must not increase submission friction
  - `Page Performance`: Core Web Vitals must remain within baseline budget
  - `Brand Trust & Accessibility`: WCAG AA compliance and visual craft preserved

---

## 4. Execution & Stopping Criteria

- **SAMPLE_SIZE_TARGET:** [Calculated minimum sample size per variant or synthetic test limit]
- **MINIMUM_DURATION:** [e.g. 14 days to capture day-of-week seasonality]
- **START_CRITERIA:** Pre-flight SRM check passed, PII check passed, dark pattern check passed.
- **STOP_CRITERIA:** Pre-determined sample reached OR severe guardrail failure triggered.
- **RISK_ASSESSMENT:** [Potential brand, UX, or conversion risks and mitigation plans]

---

## 5. Result Interpretation & Decision Record

- **RESULT:** `INSUFFICIENT_EVIDENCE` | `DIRECTIONAL_ONLY` | `STATISTICALLY_SUPPORTED` | `INCONCLUSIVE` | `INVALIDATED`
- **SAMPLE_RATIO_CHECK:** `PASS` | `FAIL` | `NOT_MEASURED`
- **NOVELTY_RISK:** `LOW` | `MEDIUM` | `HIGH`
- **DECISION:** [Deploy variant / Iterate hypothesis / Retain control / Invalidate test]
- **LEARNING_SUMMARY:** [Key takeaways for future design and content strategy]
