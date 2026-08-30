# Framework Validation Tests

## Purpose

Own deterministic tests for Website Director framework self-validation,
compatibility, negative controls, isolation, and release evidence.

## Ownership

`test_v2_11_framework_validation.py` owns the Capability 6 regression and
negative-control suite registered in `schemas/test-suites.json`.

## Local Contracts

- Tests use temporary directories and fixtures for mutation probes.
- Tests do not modify the protected `projects/` corpus, external systems, or
  production credentials.
- Each required failure mode must prove a real validator signal, not merely a
  missing-file assumption.
- Tests are order-independent and runnable with the standard library.

## Work Guidance

Prefer pure validator helpers for malformed fixtures and use the registered
FrozenIntegrityGuard for frozen-project mutation evidence. Keep historical
fixtures read-only and distinguish `FAIL` from `BLOCKED`.

## Verification

Run `python -m unittest tests.test_v2_11_framework_validation` directly and via
`python -m framework_validation --run-suites`.

## Child DOX Index

- None.
