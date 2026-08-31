# Localization and Internationalization Intelligence

## Purpose

Own the provider-neutral Capability #9 localization and internationalization validator and its local contracts. This boundary supports locale identity, routing, fallback, translation lifecycle, formatting, RTL, typography, localized assets, SEO, accessibility, analytics, Content Operations, provenance, browser QA, launch, and handoff integrations.

## Ownership

`localization/validator.py` owns deterministic contract validation only. The canonical state is `localization.complete`; the canonical readiness gate is `[LOCALIZATION_READY]`. Content Operations, SEO, Accessibility, Security and Privacy, Measurement, Provenance, Browser QA, Launch Ops, and V2.5 Handoff remain the authorities for their own domains.

## Local Contracts

- Locale identifiers are BCP 47-style and distinguish language, script, and region.
- A required project has exactly one source locale and exactly one default locale.
- Route strategy, default URL policy, fallback policy, content coverage, and review ownership are explicit.
- Machine translation is draft material. Human or explicitly authorized review is required before production publication.
- Source changes make translations stale. Stale translations are not current or publishable.
- Currency is explicit. Dates, numbers, units, pluralization, and interpolation are locale-aware.
- RTL uses document direction and logical CSS where practical. Brand marks are not mechanically mirrored.
- Font coverage and redistribution provenance are release inputs. Research references are not production media.
- Localization adds no owner lock and no second CMS, analytics, browser runner, provenance ledger, or handoff authority.
- The validator never calls a network provider, uses production credentials, publishes, deploys, or changes anything under `projects/`.

## Work Guidance

Keep the implementation standard-library only and provider-neutral. Accept synthetic mappings and lists so the test suite can exercise contracts without mutating frozen pilots. Keep requirement assessment evidence-based and fail closed for missing or contradictory required facts. Add compatibility aliases only when they cannot weaken the canonical status or review rules.

## Verification

Run `python tests/test_v2_14_localization.py` for the A-AF suite. Run `python -m framework_validation --run-suites` for framework certification. The suite must use temporary fixtures and `browser-qa/guards/frozen_integrity_guard.py`; no test may write under `projects/`.

## Child DOX Index

No child DOX documents currently exist.
