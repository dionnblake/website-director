# Framework Validation Package

## Purpose

Own the deterministic Website Director self-validation library and its
`python -m framework_validation` CLI, including registry-driven execution of
the additive V2.11.1 adapter suite and the V2.12 Capability 7 provenance suite.

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
- Keep the exact five owner-lock invariant and fail closed on missing evidence.

## Work Guidance

Keep checks deterministic and explainable. Expose small pure helpers when a
negative control or compatibility fixture needs to prove a rule. Do not add
special cases that turn invalid evidence into a pass.

## Verification

Run `python -m unittest tests.test_v2_11_framework_validation`,
`python -m unittest tests.test_v2_12_evidence_asset_provenance`, and
`python -m framework_validation --run-suites`. Inspect both generated reports
and the final mutation evidence.

## Child DOX Index

- None.
