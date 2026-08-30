# Framework Schemas and Registries

## Purpose

Own the canonical machine-readable schema, registry, compatibility, and
validation-manifest contracts for Website Director Capability 6, the additive
  Capability 6.5 adapter registration, Capability 7 evidence provenance,
  Capability #8 Content Operations and CMS Architecture, and Capability #9
  Localization and Internationalization.

## Ownership

- `site-profile.schema.json` owns the current profile shape and exact five-lock
  definition.
- `protocols.json`, `gates.json`, `phases.json`, and `state-ownership.json` own
  lifecycle identity, gate classification, phase order, and state authority.
- `compatibility.json` owns historical schema and deprecation policy.
- `frozen-projects.json` owns the protected historical inventory.
- `test-suites.json` owns discoverable isolated test commands.
- `validation-manifest.json` owns source roots and report destinations.
- framework-validation-report.schema.json owns report shape.
- evidence-ledger.schema.json owns the cross-cutting claims, sources,
  testimonials, certifications, research-reference, and asset evidence shape.
- provenance state, the EVIDENCE_PROVENANCE protocol, Phase 6.95, and the
  EVIDENCE_PROVENANCE_READY readiness gate are additive and remain separate
  from Asset Director provenance_status.
- The V2.11.1 integration registry entries point to the bounded design-
  inspiration adapter without creating a new site-profile state, phase, gate,
  or owner lock. Capability 7 consumes that reference evidence but does not
  reimplement the adapter.
- Content Operations state, the CONTENT_OPERATIONS_CMS protocol, Phase 6.25,
  the CONTENT_OPERATIONS_READY readiness gate, and its test suite are distinct
  from V2.5 handoff state and add no owner lock.
- Localization state, the LOCALIZATION_INTERNATIONALIZATION protocol, Phase
  6.35, the LOCALIZATION_READY readiness gate, the locale registry, manifest,
  and test suite are distinct from Content Operations, V2.5 handoff, and all
  adjacent authorities. They add no owner lock.

## Local Contracts

- `framework-version.json` is the only current version source; schemas may
  reference it but must not become competing version authorities.
- The current owner-lock set is exactly five names and no registry may add a
  sixth lock.
- Historical entries are explicit and non-authoritative. This corrected V2.11
  checkout carries the complete certified V2.10 corpus; missing registered
  artifacts are validation failures, not migration permission.
- Framework-validation state is external to the site profile.
- The current framework version is 2.14.0. The content-operations,
  localization, and provenance readiness gates are not owner locks; the exact five-lock
  invariant remains authoritative.
- Registry references must resolve or carry an explicit historical status and
  replacement policy.

## Work Guidance

Prefer additive, versioned fields and preserve old records. Update the
validator, tests, protocol, and affected DOX when a durable contract changes.

## Verification

Run `python -m unittest tests.test_v2_11_framework_validation` and
`python -m framework_validation --run-suites`. Validate every JSON file under
the manifest's canonical roots, including evidence-ledger.schema.json,
localization-manifest.schema.json, and the provenance, content-operations, and
localization state/gate/phase registries.

## Child DOX Index

- None.
