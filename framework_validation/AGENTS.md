# Framework Validation Package

## Purpose

Own the deterministic Website Director self-validation library and its
`python -m framework_validation` CLI.

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
- Keep the exact five owner-lock invariant and fail closed on missing evidence.

## Work Guidance

Keep checks deterministic and explainable. Expose small pure helpers when a
negative control or compatibility fixture needs to prove a rule. Do not add
special cases that turn invalid evidence into a pass.

## Verification

Run `python -m unittest tests.test_v2_11_framework_validation` and
`python -m framework_validation`. Inspect both generated reports and the final
mutation evidence.

## Child DOX Index

- None.
