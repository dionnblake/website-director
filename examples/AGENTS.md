# Website Director Examples

## Purpose

Own reference documentation and integration-validation examples for the
Website Director framework. Examples explain protocol boundaries and
deterministic synthetic controls without becoming production project state.

## Ownership

`APPLICATION-ARCHITECTURE-INTEGRATION-VALIDATION.md` documents the V2.15
Capability #10 A-AV control matrix. `test_runner.py` owns the cross-version
protocol, template, pilot, and five-lock invariant harness.

## Local Contracts

- Examples remain provider-neutral and use synthetic evidence only.
- They must not create users, charge payment methods, call live providers,
  publish, deploy, or mutate `projects/`.
- Capability #10 is conditional. Static and content-only examples must not be
  burdened with application modules that their behavior does not require.
- Readiness gates are not owner locks; the exact five-lock invariant remains
  authoritative.

## Work Guidance

Keep scenario IDs, expected verdicts, and framework markers aligned with the
registered test suite and canonical protocol. Do not copy provider secrets or
turn a synthetic example into a production claim.

## Verification

Run `python examples/test_runner.py` and
`python tests/test_v2_15_application_architecture.py`, then run the complete
registered suite through `python -m framework_validation --run-suites`.

## Child DOX Index

- None.
