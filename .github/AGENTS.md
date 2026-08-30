# Framework Validation CI

## Purpose

Own the GitHub Actions workflow that runs Capability 6 framework validation in
clean, isolated Ubuntu and Windows environments.

## Ownership

`.github/workflows/framework-validation.yml` owns triggers, matrix execution,
report upload, and CI-only verification commands.

## Local Contracts

- Grant only `contents: read` permissions.
- Run the core validator and every active suite registered in
  `schemas/test-suites.json`.
- Use no deployment, publishing, push, merge, credential, or external network
  mutation step.
- Keep browser execution optional and separate from the core framework gate.
- Upload inspectable reports without changing repository state.

## Work Guidance

Keep the workflow dependency-light. Use the repository's standard Python and
Node runtimes. A workflow change requires validator and negative-control
coverage.

## Verification

Run `python -m framework_validation --run-suites` locally and inspect the
workflow's read-only policy with `validate_workflow_text`.

## Child DOX Index

- None.
