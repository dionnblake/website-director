# DOX framework

**Version:** 2.15.0

## Core Contract

- `AGENTS.md` files are binding contracts for their subtrees.
- The root contract supplies repository-wide rules; the nearest applicable child
  contract supplies local ownership and workflow detail.
- A child contract may specialize local work but may not weaken safety, owner
  control, project isolation, fail-closed behavior, or verification requirements.
- Keep source, evidence, instructions, and durable artifacts understandable from
  the applicable DOX chain and the repository itself.

## Read Before Editing

1. Identify the files or directories in scope.
2. Read this root contract.
3. Walk from the repository root to each target and read only the `AGENTS.md`
   files on those paths, including any indexed child boundary.
4. Use the nearest contract for local detail and re-check the chain after edits.
5. Inspect the actual checkout, current files, and existing verification before
   claiming a change is complete.

## Website Director resident rail

- `SKILL.md` is the canonical operator router. Read it next, then load only the
  specialist protocol, schema, template, registry, or child DOX required by the
  active stage and evidence.
- The current conceptual lifecycle is exactly:

  `UNDERSTAND -> RESEARCH -> DESIGN -> ASSETS -> BUILD -> VERIFY -> RELEASE`

- The kernel is navigation, not a second runtime or control plane. It creates no
  state object, registry, readiness gate, runner, orchestrator, or owner lock.
- The only owner locks are exactly:
  `design_direction_locked`, `information_architecture_locked`,
  `content_structure_locked`, `design_system_locked`, and
  `motion_direction_locked`.
- Existing protocols, validators, schemas, registries, templates, and project
  artifacts retain their state, gate, evidence, and side-effect authority.
  Use them instead of inventing parallel state or a new registry.
- Conditional capabilities are dispatched only from explicit behavior, stories,
  assets, route needs, or selected ambition. Their existing `NOT_REQUIRED`,
  `blocked`, and exception semantics remain local; inactivity is not readiness.

## Global safety and evidence boundaries

- Missing, unknown, stale, or unavailable required evidence fails closed. Keep
  planning, implementation verification, production verification, owner review,
  manual review, simulation, and browser evidence distinct. A local or staging
  result is not production verification.
- During DESIGN, the bounded source-copy precheck remains advisory and before
  `content_structure_locked`; it emits review evidence only and never rewrites
  copy or owns a lock. Provenance remains the authority for applicable claims.
- During VERIFY, framework validation, Browser QA, Impeccable, and the Website
  Gauntlet remain separate authorities. Browser QA owns deterministic runtime
  observation and frozen-project integrity; Impeccable owns source scans; the
  Gauntlet owns fresh qualitative rendered critique after deterministic checks.
- Asset Director owns art-directed production assets. Accessibility, Security &
  Privacy, Measurement, Content Operations, Localization, Application
  Architecture, and Provenance retain their existing specialist contracts and
  readiness states; none is an owner lock.
- Launch Operations is the single release and production-state authority.
  `RELEASE_READY` never implies `DEPLOYMENT_AUTHORIZED`.
- `projects/` is protected during framework maintenance and tests. Use the
  existing `browser-qa/guards/frozen_integrity_guard.py` boundary and stop on
  detected project mutation.
- No deployment, publishing, push, merge, DNS change, credential or provider
  setup, payment, real message, production mutation, or destructive action may
  occur without explicit owner authorization.

### Security, Privacy & Compliance Governance

Security, Privacy & Compliance owns proportional risk, privacy, consent,
secrets, and legal-review boundaries. Its readiness state is not an owner lock.

### Browser & Regression QA Governance

Browser QA owns deterministic runtime observation and frozen-project integrity;
it remains separate from the Website Gauntlet and adds no owner lock.

## DOX maintenance

- Update the nearest owning child when a local durable contract changes.
- Update this root only for global structure, invariants, ownership boundaries,
  or the child index.
- Remove stale duplication instead of relocating history or creating a parallel
  documentation system.

## Child DOX Index

Read the entry for the target subtree; nested boundaries are indexed by their
parent.

- [.github/](.github/AGENTS.md): read-only framework-validation CI workflow boundary.
- [application/](application/AGENTS.md): conditional application, authentication, and commerce architecture.
- [browser-qa/](browser-qa/AGENTS.md): browser/runtime QA and frozen-integrity controls.
- [content-ops/](content-ops/AGENTS.md): content operations and CMS architecture.
- [examples/](examples/AGENTS.md): reference documentation and integration examples.
- [framework_validation/](framework_validation/AGENTS.md): deterministic framework validation package and CLI.
- [framework-validation/](framework-validation/AGENTS.md): generated validation-report artifacts.
- [integrations/](integrations/AGENTS.md): bounded external-evidence adapters and nested integration DOX.
- [localization/](localization/AGENTS.md): localization and internationalization contracts.
- [provenance/](provenance/AGENTS.md): evidence, claim, asset-rights, attribution, and hash validation.
- [schemas/](schemas/AGENTS.md): canonical schemas, registries, compatibility, and validation manifests.
- [templates/](templates/AGENTS.md): site profiles and planning/review templates.
- [tests/](tests/AGENTS.md): registered framework tests, negative controls, and isolation evidence.
- [projects/alpha-starts-now-clean-room/](projects/alpha-starts-now-clean-room/AGENTS.md): local candidate contract.
- [projects/alpha-starts-now-flagship-proof/](projects/alpha-starts-now-flagship-proof/AGENTS.md): local proof-run contract.
- [projects/alpha-starts-now-v1-1/](projects/alpha-starts-now-v1-1/AGENTS.md): local frozen V1.1 contract.

## Closeout

- Re-check the applicable DOX chain and final diff.
- Run the relevant targeted and repository verification.
- Confirm no protected project bytes or secrets changed.
- Report evidence and distinguish implemented/verified, unverified, blocked, or
  failed states. Do not infer completion from a green partial check.

## Framework self-validation contract

Framework self-validation is owned by `framework_validation/` and remains
outside `templates/site-profile.json`. The canonical version is
`framework-version.json`; the registered full path is
`python -m framework_validation --run-suites`.

<!-- FRAMEWORK_VERSION: 2.15.0 -->
<!-- FRAMEWORK_GOVERNANCE
framework_version_source=framework-version.json
owner_locks=design_direction_locked,information_architecture_locked,content_structure_locked,design_system_locked,motion_direction_locked
frozen_projects=projects/
deployment_authority=OWNER_APPROVAL_REQUIRED
external_side_effects=NONE
state_ownership=schemas/state-ownership.json
browser_qa=browser-qa/guards/frozen_integrity_guard.py
accessibility=owner-controlled historical protocol state
security_privacy=owner-controlled historical protocol state
provenance=provenance.complete
content_ops=content_ops.complete
localization=localization.complete
application=application.complete
framework_phase=0:Framework Self-Validation:ACTIVE
framework_gate=FRAMEWORK_VALIDATION_PASS
framework_validation_state=EXTERNAL_TO_SITE_PROFILE
-->
