# Framework Validation Package

## Purpose

Own the deterministic Website Director self-validation library and its
`python -m framework_validation` CLI, including registry-driven execution of
the design-inspiration adapter suite, the evidence and asset-provenance suite,
the content-operations suite, the localization and internationalization
suite, and the conditional application architecture suite. It also owns the
provider-neutral cinematic/inspiration and rendered-visual evidence helpers
used by the bounded V2.15 regression suite, plus the provider-neutral
clean-room execution coordinator for the Visual Prototype operating mode and
its test-only synthetic proof.
It also owns the bounded Impeccable source scanner in impeccable.py, including
its normalized finding contract, curated v4.3.1 rule subset, contextual
override handling, and fail-closed official-engine artifact audit helper.
It also owns `copy_quality.py`, the bounded, advisory, source-copy pattern
precheck for supplied English copy. It emits deterministic review findings
without scoring, rewriting, claim validation, or lifecycle authority.

## Ownership

`validator.py` owns framework validation rules, findings, reports, suite
execution, and read-only mutation evidence. Launch-state status and transition
rules remain canonical in `launch-ops/validator.py`; this package consumes that
validator when checking site profiles. `cinematic_inspiration.py` owns pure registry,
owner-reference, provider-neutrality, and rendered-visual receipt checks.
`owner_intent.py` owns the provider-neutral normalization, authority
precedence, historical/reference boundary, brand-token, contradiction,
motion-trace, and owner-compliance helpers. It does not own site state or a
new owner lock.
`design_first_flow.py` owns the bounded business-understanding, optional
discovery/transcript, full-homepage review, explicit owner-approval,
homepage-to-Design-System derivation, component-routing, asset-intent, and
downstream-authority helpers. It does not create a phase, gate, state writer,
provider dependency, browser runner, or owner lock.
`clean_room.py` owns the clean-room input firewall, ordered concept/render/
negative-baseline/critic handoffs, physical staged creative workspaces,
browser-derived morphology evidence, and machine-readable execution receipts.
Its canonical boundary is `prepare_clean_room_concept_run`; compatibility
aliases delegate to it. Deterministic synthetic proof adapters belong to the
test suite, not the production kernel. It does not call providers, generate
ASN, write under `projects/`, or add a state, gate, or owner lock. Existing
owner-selection authority is consumed only at the final unlock boundary.
impeccable.py owns read-only source-text design-quality detection for the
existing design_qa_impeccable capability. It does not own browser runtime
observations, accessibility runtime assertions, qualitative Gauntlet critique,
design-system token identity, or any lifecycle state.
`copy_quality.py` owns only the selected source-copy pattern heuristics. It does
not own factual proof, provenance, localized-copy validation, rendered-copy
observation, Browser QA, Gauntlet critique, or content-lock authority.
`__main__.py` owns the module entrypoint.

## Local Contracts

- Use the standard library only.
- Read repository artifacts and run only commands registered in
  `schemas/test-suites.json`.
- Write only the designated runtime and certification report paths.
- `.clean-room-runs/` is disposable clean-room execution evidence and is
  ignored by source-mutation snapshots; it must never contain repository or
  historical positive inputs.
- Never publish, deploy, push, merge, use credentials, perform network
  mutation, or mutate `projects/`.
- The protected `projects/` inventory is the five active Alpha Starts Now
  surfaces. Historical certification behavior is consumed through minimal
  synthetic fixtures and Git history is the recovery authority.
- The clean-room operating mode must run through
  `prepare_clean_room_concept_run`; historical output is available only
  through the post-render negative-baseline adapter. The boundary stages only
  manifest-declared inputs, emits the bounded generator package before the
  builder callback, derives morphology from the existing browser engine, and
  stops at `OWNER_CONCEPT_SELECTION_PENDING` unless the existing
  `visual_prototypes.owner_selection_confirmed` event is valid.
- Runtime isolation is framework-level staged context only:
  `FRAMEWORK_CREATIVE_CONTEXT_ISOLATION = STAGED_WORKSPACE_ONLY`,
  `OS_FILESYSTEM_SANDBOX = NONE`, and
  `UNRESTRICTED_AGENT_PATH_ACCESS_RISK = PRESENT`. Do not describe the staged
  workspace as an OS sandbox.
- Framework validation state stays outside `templates/site-profile.json`.
- The Impeccable scanner is standard-library-only and has no provider, network,
  subprocess, browser, daemon, install, hook, repair, or project-write path.
- The scanner preserves the exact five owner locks and reports a locked repair
  impact without changing the lock registry.
- The copy-quality precheck scans only supplied English source copy when a
  known locale is present. Known non-English input is `NOT_APPLICABLE` and an
  unknown locale is `BLOCKED`; neither is a clean-copy verdict.
- Copy findings use the existing evidence-oriented review path with
  `COPY_PATTERN_SCANNER` and `HEURISTIC` metadata. The precheck has no score,
  automatic rewrite, provider/model path, proof verdict, new state, new gate,
  new phase, or new owner lock. Locked-copy findings point to the existing
  Owner Change Request path.
- Numeric or social proof remains owned by Capability 7 Provenance, broad
  qualitative critique remains owned by the Gauntlet, and post-build rendered
  copy is deferred unless an existing rendered-text observation is present.
- Adapter suites remain deterministic and are run only through the commands
  registered in `schemas/test-suites.json`; framework validation itself makes
  no live MCP or provider request.
- Capability 7 provenance validation is fail-closed for production records,
  reference-only for research inputs, and separate from Asset Director
  provenance_status. Its readiness flag is not an owner lock.
- Capability #8 content operations validation is provider-neutral, fail-closed
  for unsafe models and publishing boundaries, and separate from V2.5 client
  handoff operations. Its readiness flag is not an owner lock.
- Capability #9 localization validation is provider-neutral, fail-closed for
  invalid locale, route, fallback, translation, formatting, RTL, typography,
  provenance, SEO, accessibility, analytics, CMS, and handoff contracts. Its
  readiness flag is not an owner lock and it never calls a translation provider.
- Capability #10 application architecture validation is conditional,
  behavior-based, provider-neutral, fail-closed for unsafe authentication,
  authorization, data, commerce, payment, booking, upload, UGC, integration,
  and high-risk contracts. Its sole readiness flag is `application.complete`,
  it adds no owner lock, and it never calls an application or payment provider.
- Cinematic production intelligence remains provider/model-neutral. Inspiration
  records default to `REFERENCE_ONLY`; source reuse requires license,
  provenance, stack-adaptation, and design-system-adaptation evidence.
- Rendered visual validation derives status from real-browser screenshot paths
  and SHA-256 receipts for the required surface set. Source-only, incomplete,
  stale-after-repair, simulation-only, or critic-without-fresh-input evidence
  is blocked.
- Keep the exact five owner-lock invariant and fail closed on missing evidence.
- The Impeccable scanner resolves ignore directories relative to the selected
  `scan_path` root, so an explicitly selected `build` or `dist` root remains
  scannable while nested ignored directories remain excluded. Empty or
  unsupported-only `scan_path` roots and `scan_sources` maps fail closed with
  `ValueError("no supported source files to scan")`.
- Accessibility owns the logical heading hierarchy requirement and Browser QA
  executes its canonical heading-order assertion; Impeccable does not emit
  `skipped-heading`. Impeccable's `broken-image` is only an obvious
  source-level precheck, never the Browser QA runtime asset-integrity verdict.
- Owner requirements are normalized with explicit class, source, currentness,
  scope, and authority metadata. Current owner instructions supersede
  historical project material and reference inspiration; unresolved same-tier
  contradictions fail closed.
- Brand validation is semantic and role/dominance-aware. It permits approved
  shades, derivatives, accessibility neutrals, and opacity/gradient variants,
  while rejecting unrelated dominant hues. The Alpha Starts Now current
  owner-intent artifact records navy blue primary and yellow accent without
  inventing exact values.
- Explicit cinematic, immersive, animation-heavy, or scroll-driven owner
  intent resolves to `MOTION_LEVEL_3` and cannot be silently downgraded. Level
  2/3 implementation requires a brief-to-location-to-real-browser runtime
  evidence trace and meaningful sequence diversity.
- The design-first flow keeps the Business Understanding Pack canonical at
  `templates/project-brief.md`, keeps transcript extraction optional, requires
  real desktop/mobile homepage evidence and explicit owner approval before
  full production, and derives rather than reinterprets the Design System.

## Work Guidance

Keep checks deterministic and explainable. Expose small pure helpers when a
negative control or compatibility fixture needs to prove a rule. Do not add
special cases that turn invalid evidence into a pass.

## Verification

Run `python -m framework_validation --run-suites`. This is the canonical
full-verification path and includes the browser/accessibility and
release/handoff composites, cinematic and design/motion unit suites, and the
clean-room suite. The framework_validation registry also runs the targeted
Impeccable synthetic proof. Inspect both generated reports and the final
mutation evidence.

## Child DOX Index

- None.
