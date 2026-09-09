# Website Director Examples

## Purpose

Own reference documentation and integration-validation examples for the
Website Director framework. Examples explain protocol boundaries and
deterministic synthetic controls without becoming production project state.

## Ownership

`APPLICATION-ARCHITECTURE-INTEGRATION-VALIDATION.md` documents the conditional
application control matrix. Examples are reference documentation only; the
historical capability compatibility checks live in
`tests/test_framework_validation.py`, and the registered test composites own
executable verification.

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
turn a synthetic example into a production claim. Do not add a second test
runner here.

## Verification

Run the complete registered suite through
`python -m framework_validation --run-suites`. Examples themselves have no
independent executable harness.

## Child DOX Index

- None.
