# Framework Validation Package

## Purpose

Own the deterministic Website Director self-validation library and its
`python -m framework_validation` CLI, including registry-driven execution of
the additive V2.11.1 adapter suite, the V2.12 Capability 7 provenance suite,
the V2.13 Capability #8 content-operations suite, the V2.14 Capability #9
localization and internationalization suite, and the V2.15 conditional
Capability #10 application architecture suite.

## Ownership

`validator.py` owns validation rules, findings, reports, suite execution, and
read-only mutation evidence. `__main__.py` owns the module entrypoint.

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
- Keep the exact five owner-lock invariant and fail closed on missing evidence.

## Work Guidance

Keep checks deterministic and explainable. Expose small pure helpers when a
negative control or compatibility fixture needs to prove a rule. Do not add
special cases that turn invalid evidence into a pass.

## Verification

Run the V2.11, V2.12, V2.13, V2.14, and V2.15 suites directly, then run
`python -m framework_validation --run-suites`. Inspect both generated reports
and the final mutation evidence.

## Child DOX Index

- None.
