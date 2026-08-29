# CRO, ANALYTICS & EXPERIMENTATION PROTOCOL — SUPERSEDED

> **Status:** SUPERSEDED as of V2.6.0  
> **Superseded by:** [CONVERSION-ANALYTICS-PROTOCOL.md](CONVERSION-ANALYTICS-PROTOCOL.md)  
> **Last independent version:** 2.4.0  
> **This file is retained for link stability only. Do not author new guidance here.**

---

## Why This Document Was Superseded

V2.4.0 established the first CRO, analytics, and experimentation discipline in Website Director. It correctly governed conversion hierarchy, funnel modelling, privacy-first event taxonomy, dark-pattern prohibition, and statistical humility.

It did **not** provide a complete measurement architecture. V2.6.0 adds:

- Attribution and UTM governance
- Affiliate measurement with the `CLICK ≠ CONVERSION ≠ COMMISSION` invariant
- CTA-to-event traceability against locked copy
- The mandatory 13-field Event Definition Contract
- Baseline / target / observation governance and the anti-fabrication invariant
- Separation of planning, implementation verification, and production verification
- Blocked mode and bounded exception mode
- The evidence taxonomy (`OBSERVED` → `PROVEN`)
- Vendor naming mapping that preserves canonical vocabulary
- Phase 6.5 placement, so measurement informs design instead of being retrofitted

All normative content of V2.4.0 has been absorbed into the superseding protocol. Nothing was dropped.

---

## Migration Map

| V2.4.0 Concept | V2.6.0 Location |
| :--- | :--- |
| System invariants | `CONVERSION-ANALYTICS-PROTOCOL.md` §2 |
| Outcome definition | §4 Business Objective Determination |
| Conversion hierarchy (`MACRO` / `MICRO` / `DIAGNOSTIC`) | §5.3 |
| Funnel & journey modelling (`FUNNEL_MODEL`) | §6.1 |
| CRO hypothesis engine (`CRO_HYPOTHESIS`) | §14.2 |
| Metric classification & vanity prohibition | §5.1–§5.2 |
| Event taxonomy & naming standard | §7, §9 |
| Event schema & versioning | §8 Event Definition Contract |
| Privacy, consent & governance | §15 Privacy Boundary |
| Subsystem integration boundaries | §23 |
| Experimentation governance | §14.2 |
| `[CRO_MEASUREMENT_READY]` gate | §21 — now a downstream sub-gate of `[CONVERSION_MEASUREMENT_COMPLETE]` |

---

## State Migration

| V2.4.0 State | V2.6.0 State |
| :--- | :--- |
| `site-profile.json` → `cro{}` | `site-profile.json` → `measurement{}` |
| `cro.status` | `measurement.mode` + `measurement.complete` |
| `cro.pii_check` | `measurement.pii_check` |
| `cro.dark_pattern_check` | `measurement.dark_pattern_check` |
| `cro.analytics_provider` | `measurement.provider` |
| `cro.measurement_plan_ready` | `measurement.complete` |
| `cro.experimentation_required` | `measurement.experimentation_required` |
| — | `measurement.implementation_verified` *(new)* |
| — | `measurement.production_verified` *(new)* |

`measurement.complete` is the **single** authoritative readiness flag. No duplicate completion flag exists.

---

## Backward Compatibility

Projects created under V2.4 or V2.5 that carry a `cro{}` object **remain valid**. `cro{}` is grandfathered and read-only. It is **not** migrated automatically, and frozen pilot projects are **not** retrofitted.

New projects use `measurement{}`.

---

## Template Migration

| V2.4.0 Template | V2.6.0 Template |
| :--- | :--- |
| `templates/analytics-measurement-plan.md` | [templates/measurement-plan.md](templates/measurement-plan.md) — superseded, retained for existing projects |
| `templates/analytics-event-manifest.json` | Retained and still current |
| `templates/experiment-brief.md` | Retained and still current |
