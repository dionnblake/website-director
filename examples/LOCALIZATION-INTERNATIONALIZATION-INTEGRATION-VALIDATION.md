# Localization and Internationalization Integration Validation

<!-- FRAMEWORK_VERSION: 2.14.0 -->

This document records the deterministic V2.14 Capability #9 validation shape.
It is a framework integration reference, not a live translation, CMS, analytics,
deployment, or legal-certification record.

## Authority map

- Protocol: `LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md`
- Plan: `templates/localization-plan.md`
- Manifest: `templates/localization-manifest.json`
- Registry: `templates/locale-registry.json`
- State: `localization.complete`
- Gate: `[LOCALIZATION_READY]`
- Phase: `6.35`, after Content Operations and before Measurement
- Validator: `localization/validator.py`
- Suite: `tests/test_v2_14_localization.py`
- Frozen guard: `browser-qa/guards/frozen_integrity_guard.py`

## Scenario matrix

| Scenario | Control |
| --- | --- |
| A | English-only requirement is `NOT_REQUIRED` and does not create locale bloat. |
| B | English and Spanish registry, routing, fallback, translation, SEO, and integrations pass. |
| C | Duplicate default locale fails. |
| D | Missing source locale fails. |
| E | Invalid `english_USA` locale identifier fails. |
| F | `es-MX` fallback to parent `es` passes when the parent is registered. |
| G | Fallback cycle fails. |
| H | Route collision fails. |
| I | Wrong document `html lang` fails. |
| J | Missing reciprocal `hreflang` fails. |
| K | Localized canonical pointing to the source route fails. |
| L | Published machine draft fails. |
| M | Human-reviewed published translation passes. |
| N | Source version change identifies `STALE`. |
| O | Stale content treated as current fails. |
| P | UI concatenation and unsafe pluralization fail. |
| Q | Fixed `MM/DD/YYYY` formatting fails. |
| R | Currency inferred from language fails. |
| S | RTL locale declared LTR fails. |
| T | Mechanical brand-logo mirroring in RTL fails. |
| U | Pseudo-localized CTA overflow fails. |
| V | Missing script font coverage is blocked. |
| W | Unresolved font license fails. |
| X | Translation that strengthens a claim fails. |
| Y | Machine-translated legal content marked legally approved fails. |
| Z | Unreviewed published translation fails. |
| AA | Existing analytics event with a locale parameter passes. |
| AB | Per-language analytics event names fail. |
| AC | Localized CMS record retains content-model and portability provenance. |
| AD | Research reference cannot become production media. |
| AE | Framework rejects a sixth owner lock. |
| AF | Frozen-integrity guard records a protected-path mutation. |

## Execution

Run from the repository root:

```text
python tests/test_v2_14_localization.py
python -m framework_validation --run-suites
```

The suite uses synthetic dictionaries and temporary directories. It does not
write under `projects/`, call a translation provider, use production
credentials, publish, deploy, modify DNS, create analytics properties, or
change a live site. A failed or unavailable control remains `FAIL` or
`BLOCKED`; it is not promoted by changing prose.

## Required result

The V2.14 suite must report zero failures, preserve the exact five owner locks,
and leave the frozen project corpus byte-identical. Framework certification
also requires the V2.10 Launch Operations, V2.11 framework and Design
Inspiration, V2.12 Evidence and Asset Provenance, V2.13 Content Operations,
and current V2.14 Localization suites to pass through the registered runner.
