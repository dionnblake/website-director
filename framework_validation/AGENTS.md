# Framework Validation Package

## Purpose

Own the deterministic Website Director self-validation library and its
`python -m framework_validation` CLI, including registry-driven execution of
the additive V2.11.1 adapter suite, the V2.12 Capability 7 provenance suite,
the V2.13 Capability #8 content-operations suite, the V2.14 Capability #9
localization and internationalization suite, and the V2.15 conditional
Capability #10 application architecture suite. It also owns the
provider-neutral cinematic/inspiration and rendered-visual evidence helpers
used by the bounded V2.15 regression suite.

## Ownership

`validator.py` owns validation rules, findings, reports, suite execution, and
read-only mutation evidence. `cinematic_inspiration.py` owns pure registry,
owner-reference, provider-neutrality, and rendered-visual receipt checks.
`owner_intent.py` owns the provider-neutral normalization, authority
precedence, historical/reference boundary, brand-token, contradiction,
motion-trace, and owner-compliance helpers. It does not own site state or a
new owner lock.
`__main__.py` owns the module entrypoint.

## Local Contracts

- Use the standard library only.
- Read repository artifacts and run only commands registered in
  `schemas/test-suites.json`.
- Write only the designated runtime and certification report paths.
- Never publish, deploy, push, merge, use credentials, perform network
  mutation, or mutate `projects/`.
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

## Work Guidance

Keep checks deterministic and explainable. Expose small pure helpers when a
negative control or compatibility fixture needs to prove a rule. Do not add
special cases that turn invalid evidence into a pass.

## Verification

Run the V2.11, V2.12, V2.13, V2.14, and V2.15 suites directly, including
`python -m unittest tests.test_cinematic_inspiration`, then run
`python -m framework_validation --run-suites`. Inspect both generated reports
and the final mutation evidence.

## Child DOX Index

- None.
