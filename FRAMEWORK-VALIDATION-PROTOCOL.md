# Website Director Framework Self-Validation Protocol

<!-- FRAMEWORK_VERSION: 2.14.0 -->
<!-- protocol-id: FRAMEWORK_VALIDATION -->
<!-- protocol-status: ACTIVE -->
<!-- protocol-domain: framework-governance -->
<!-- protocol-phase: 0 -->
<!-- gate: FRAMEWORK_VALIDATION_PASS phase:0 -->

## Purpose and boundary

Capability 6 validates Website Director itself: its version authority,
registries, schemas, references, state ownership, compatibility records,
frozen-project integrity, test isolation, and read-only CI policy. The additive
Capability 6.5 Design Inspiration MCP adapter is validated by its registered
deterministic suite, while this validator remains offline and does not connect
to the MCP or provider. Capability 7 Evidence, Claim and Asset Provenance is
validated by its own registered deterministic suite and offline validator. It
does not validate subjective visual quality, publish the prototype, deploy
production, send messages, use credentials, or begin Capability #9
Localization/I18n or Capability #10 Ecommerce, Authentication, and Application
modules. Capability #8 Content Operations and CMS Architecture is validated by
its own registered deterministic suite and provider-neutral content-ops validator.
Capability #9 Localization and Internationalization is validated by its own
registered deterministic suite and provider-neutral localization validator.

The corrected checkout is based directly on the certified V2.10 lineage and
retains its operational documents, browser-QA harness, and complete frozen
`projects/` corpus. Capability 6 adds framework self-validation without
rewriting historical project material or introducing external side effects.

## Canonical authorities

- [framework-version.json](framework-version.json) is the only current version
  source. Versions use strict `MAJOR.MINOR.PATCH` semantic versioning and must
  increase monotonically from the declared predecessor.
- [schemas/validation-manifest.json](schemas/validation-manifest.json) defines
  the validator's source roots, report paths, registries, and workflow.
- [schemas/site-profile.schema.json](schemas/site-profile.schema.json) defines
  the current site-profile contract.
- [templates/site-profile.json](templates/site-profile.json) is the current
  V2.14-compatible profile fixture. Framework-validation state is external to
  it, and provenance.complete remains distinct from assets.provenance_status.
- [schemas/protocols.json](schemas/protocols.json),
  [schemas/gates.json](schemas/gates.json),
  [schemas/phases.json](schemas/phases.json), and
  [schemas/state-ownership.json](schemas/state-ownership.json) are the
  canonical lifecycle and state registries.
- [schemas/compatibility.json](schemas/compatibility.json) is the explicit
  historical-schema and deprecation policy.
- [schemas/frozen-projects.json](schemas/frozen-projects.json) records the
  protected historical corpus and
  [browser-qa/guards/frozen_integrity_guard.py](browser-qa/guards/frozen_integrity_guard.py)
  is the reusable integrity guard.
- [schemas/test-suites.json](schemas/test-suites.json) is the versioned suite
  registry. Active suites must be deterministic, isolated, order-independent,
  and free of external side effects.
- [schemas/evidence-ledger.schema.json](schemas/evidence-ledger.schema.json)
  and [provenance/validator.py](provenance/validator.py) are the Capability 7
  machine contract and validator. They verify recorded evidence boundaries
  without determining ownership or legal status.
- [LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md](LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md),
  [localization/validator.py](localization/validator.py),
  [templates/localization-plan.md](templates/localization-plan.md),
  [templates/localization-manifest.json](templates/localization-manifest.json),
  and [templates/locale-registry.json](templates/locale-registry.json) are the
  Capability #9 provider-neutral localization and internationalization
  authorities. They add no owner lock and require no provider account.
- [CONTENT-OPERATIONS-CMS-PROTOCOL.md](CONTENT-OPERATIONS-CMS-PROTOCOL.md),
  [content-ops/validator.py](content-ops/validator.py),
  [templates/content-model.md](templates/content-model.md),
  [templates/content-model.json](templates/content-model.json), and
  [templates/cms-decision.md](templates/cms-decision.md) are the Capability #8
  content/CMS architecture authorities. V2.5 remains the long-term handoff
  authority.

## Invariants

The validator must fail closed for broken structure, invalid JSON, malformed
semantic versions, version drift, broken internal references, duplicate active
state owners, obsolete current state, invalid state transitions, unknown gate
owners, broken protocol or template paths, an invalid current profile, an
incorrect lock set, an unavailable frozen guard, a mutated protected corpus,
unsafe CI permissions, missing test isolation, or an unproven negative control.

The owner-lock set is exactly:

1. `design_direction_locked`
2. `information_architecture_locked`
3. `content_structure_locked`
4. `design_system_locked`
5. `motion_direction_locked`

Measurement, SEO, security, privacy, accessibility, provenance, content
operations, browser QA, launch, assets, handoff, and framework-validation
status are not owner locks. Readiness
and verification gates may refer to state, but they do not own lifecycle locks.

## Validation sequence

The reusable entrypoint is:

    python -m framework_validation

It performs the following deterministic sequence:

1. Capture branch, commit, worktree, and `origin/main` divergence metadata.
2. Load the validation manifest and verify required directories and files.
3. Validate the canonical version source, document markers, monotonicity, and
   V2.10 lineage metadata, V2.13 Capability #8 registration, and V2.14
   Capability #9 registration.
4. Validate JSON parsing, the current profile schema, historical compatibility,
   and the external framework-validation state boundary.
5. Validate protocol, gate, phase, state-ownership, template, and Markdown
   references, including exact path casing.
6. Parse framework Python sources without writing bytecode and validate the
   read-only workflow contract.
7. Snapshot and verify the registered `FrozenIntegrityGuard` boundary.
8. Discover and, for release certification, run all active registered suites,
   including the Capability 7 A-V evidence and asset provenance controls plus
   W-AK fail-closed regression edges and the Capability #8 A-V content/CMS
   controls and the Capability #9 A-AF localization controls.
9. Run deterministic negative controls for the required failure modes.
10. Record change impact and mutation evidence, then write the runtime and
    versioned certification reports only to their designated paths.

The command returns zero only for `PASS`; `BLOCKED` and `FAIL` are non-zero.
The report includes `framework_version`, `commit_sha`, UTC timestamp, status,
check counts, and findings with `RULE_ID`, `SEVERITY`, `FILE`, `LOCATION`,
`MESSAGE`, `EXPECTED`, `OBSERVED`, and `OWNER`.

## Compatibility and migration policy

Historical schemas are read-only compatibility fixtures. They may be parsed
and checked against the explicitly listed versions in
[schemas/compatibility.json](schemas/compatibility.json), but the validator
does not rewrite them, infer missing state, promote an alias to current, or
silently migrate them. `cro.complete` is a historical alias and is obsolete
for current state; `measurement.complete` is the current concept owner.

Protocol, gate, and state deprecations must retain a machine-readable status
and replacement pointer where applicable. New current state requires an
explicit registry change, version decision, schema review, protocol update,
test coverage, and owner approval. No new owner lock may be introduced by a
specialist, validator, template, or CI change.

## Frozen-project policy

The `projects/` root is protected historical material. The validator snapshots
it through the V2.8 guard before active suites run and verifies it afterward.
Mutation, addition, deletion, or a failed restoration remains a failure. The
registry is reconciled to the complete V2.10 corpus, so a missing registered
project is a validation failure, not permission to regenerate or migrate it.

## CI policy

The core workflow at
[.github/workflows/framework-validation.yml](.github/workflows/framework-validation.yml)
runs on pull requests, pushes to `framework-development` and `release/**`,
manual dispatch, and a matrix of Ubuntu and Windows runners. It grants only
`contents: read`, installs no project dependency beyond the standard Python
runtime, runs the core validator and registered tests, uploads reports, and
performs no deploy, publish, push, merge, credential, or network-mutation step.

Browser execution is optional for this capability. The core gate does not
claim browser certification. A future opt-in browser job must use temporary
profiles, isolated ports, the frozen guard, and explicit owner approval; it
must not weaken the core framework gate or introduce a scheduled external
side effect.

## Release certification

The generated artifact is
`framework-validation/reports/<framework_version>-certification.json`.
Its machine-readable status is one of:

- `FRAMEWORK_VALIDATION_PASS`
- `FRAMEWORK_VALIDATION_FAIL`
- `FRAMEWORK_VALIDATION_BLOCKED`

Certification is `PASS` only when structural, schema, reference, invariant,
compatibility, versioned-suite, frozen-integrity, and negative-control
categories all pass. Missing execution evidence is `BLOCKED`, not a pass. The
report is evidence of framework validation only and is not deployment or
production readiness.

## Review template

Use [templates/framework-validation-review.md](templates/framework-validation-review.md)
for a human review record. The template is an editable artifact and does not
replace the machine-readable report.
