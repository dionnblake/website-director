# Framework Schemas and Registries

## Purpose

Own the canonical machine-readable schema, registry, compatibility, and
validation-manifest contracts for Website Director Capability 6 and the
additive Capability 6.5 adapter registration.

## Ownership

- `site-profile.schema.json` owns the current profile shape and exact five-lock
  definition.
- `protocols.json`, `gates.json`, `phases.json`, and `state-ownership.json` own
  lifecycle identity, gate classification, phase order, and state authority.
- `compatibility.json` owns historical schema and deprecation policy.
- `frozen-projects.json` owns the protected historical inventory.
- `test-suites.json` owns discoverable isolated test commands.
- `validation-manifest.json` owns source roots and report destinations.
- `framework-validation-report.schema.json` owns report shape.
- The V2.11.1 integration registry entries point to the bounded design-
  inspiration adapter without creating a new site-profile state, phase, gate,
  or owner lock.

## Local Contracts

- `framework-version.json` is the only current version source; schemas may
  reference it but must not become competing version authorities.
- The current owner-lock set is exactly five names and no registry may add a
  sixth lock.
- Historical entries are explicit and non-authoritative. This corrected V2.11
  checkout carries the complete certified V2.10 corpus; missing registered
  artifacts are validation failures, not migration permission.
- Framework-validation state is external to the site profile.
- Registry references must resolve or carry an explicit historical status and
  replacement policy.

## Work Guidance

Prefer additive, versioned fields and preserve old records. Update the
validator, tests, protocol, and affected DOX when a durable contract changes.

## Verification

Run `python -m unittest tests.test_v2_11_framework_validation` and
`python -m framework_validation --run-suites`. Validate every JSON file under
the manifest's canonical roots.

## Child DOX Index

- None.
