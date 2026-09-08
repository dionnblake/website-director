# Framework Validation Package

## Purpose

Own the deterministic Website Director self-validation library and its
`python -m framework_validation` CLI, including registry-driven execution of
the additive V2.11.1 adapter suite, the V2.12 Capability 7 provenance suite,
the V2.13 Capability #8 content-operations suite, the V2.14 Capability #9
localization and internationalization suite, and the V2.15 conditional
Capability #10 application architecture suite. It also owns the
provider-neutral cinematic/inspiration and rendered-visual evidence helpers
used by the bounded V2.15 regression suite, plus the provider-neutral
Clean-Room Creative Mode execution coordinator and its synthetic proof entry
point.

## Ownership

`validator.py` owns validation rules, findings, reports, suite execution, and
read-only mutation evidence. Launch status and transition checks consume the
canonical `launch-ops/validator.py` authority through a lazy isolated import.
Direction imports do not activate launch code; explicit transition checks or
legacy constant access load the owning authority without a second graph.
`cinematic_inspiration.py` owns pure registry,
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
browser-derived morphology evidence, machine-readable execution receipts, and
the deterministic `python -m framework_validation.clean_room --synthetic`
proof. `prepare_clean_room_concept_run` is the canonical runtime boundary;
compatibility aliases delegate to it. It does not call providers, generate
ASN, write under `projects/`, or add a state, gate, or owner lock. Existing
owner-selection authority is consumed only at the final unlock boundary.
`rendered_morphology.py` owns stage applicability, complete-evidence checks,
normalized continuous vector comparison, and the 60 percent divergence rule.
`morphology_recheck.py` owns evidence-only remeasurement of preserved renders,
owner-review morphology reporting, immutable source-receipt linkage, complete
creative-artifact hashing, and exact-allowlist critic-package preparation. It
never invokes concept generation or a critic.
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
- Clean-Room Creative Mode must run through
  `prepare_clean_room_concept_run`; historical output is available only
  through the post-render negative-baseline adapter. The boundary stages only
  manifest-declared inputs, emits the bounded generator package before the
  builder callback, derives morphology from the existing browser engine, and
  stops at `OWNER_CONCEPT_SELECTION_PENDING` unless the existing
  `visual_prototypes.owner_selection_confirmed` event is valid.
- At `HERO_PLUS_SIGNATURE_DEVICE_ONLY`, exactly seven morphology vectors are
  applicable and three repeated-page vectors are `NOT_APPLICABLE`. Incomplete
  applicable evidence blocks, and verdicts use normalized measurements before
  labels. A preserved-render recheck may identify a signature region with an
  explicit selector, but selectors and class names are never scoring evidence.
  Rechecks write a distinct hash-linked receipt and do not rewrite the original
  execution receipt.
- Runtime isolation is framework-level staged context only:
  `FRAMEWORK_CREATIVE_CONTEXT_ISOLATION = STAGED_WORKSPACE_ONLY`,
  `OS_FILESYSTEM_SANDBOX = NONE`, and
  `UNRESTRICTED_AGENT_PATH_ACCESS_RISK = PRESENT`. Do not describe the staged
  workspace as an OS sandbox.
- Framework validation state stays outside `templates/site-profile.json`.
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

Run the V2.11, V2.12, V2.13, V2.14, and V2.15 suites directly, including
`python -m unittest tests.test_cinematic_inspiration`, then run
`python -m unittest tests.test_clean_room_creative_mode`, the synthetic
`python -m framework_validation.clean_room --synthetic` proof, and then
`python -m framework_validation --run-suites`. Inspect both generated reports
and the final mutation evidence.

## Child DOX Index

- None.

## Kernel routing

design_first_flow.py reads the sole SKILL.md activation table and phases.json lifecycle.
Routing is explicit, stateless, fail-closed, and never imports specialists or invokes
providers. clean_room.py checks this route before sending its bounded generation pack
to the direct-reference builder. Only the output pack, not this controller context,
reaches generation. Initial Direction contains no specialist guidance.
