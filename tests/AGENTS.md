# Framework Validation Tests

## Purpose

Own deterministic tests for Website Director framework self-validation,
compatibility, negative controls, isolation, and release evidence.

## Ownership

`test_v2_11_framework_validation.py` owns the Capability 6 regression and
negative-control suite registered in `schemas/test-suites.json`.
`test_v2_11_design_inspiration_mcp.py` owns the deterministic V2.11.1
Capability 6.5 A–R adapter, credential, provenance, originality, token, and
frozen-integrity controls.

## Local Contracts

- Tests use temporary directories and fixtures for mutation probes.
- Tests do not modify the protected `projects/` corpus, external systems, or
  production credentials.
- Historical V2.5-V2.10 suites are direct script entrypoints and are run by
  the registry; pytest collection is limited to the two V2.11 unittest suites.
- The Design Inspiration MCP suite uses synthetic structured results only and
  never requires a live Serper key or upstream package execution.
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
