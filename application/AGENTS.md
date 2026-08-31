# Conditional Application Architecture

## Purpose

Own the provider-neutral Capability #10 application, authentication, and
commerce architecture validator. This boundary assesses whether application
behavior is required and validates only the modules justified by explicit user
stories and runtime behavior.

## Ownership

- `validator.py` owns deterministic requirement assessment, classifications,
  module dependency checks, security invariants, and blocked-provider states.
- The canonical readiness state remains `application.complete` in the project
  profile. This directory does not create owner locks or parallel completion
  flags.
- Provider accounts, credentials, live users, payments, publishing, deploys,
  and production verification remain outside this boundary.

## Local Contracts

- Supported classifications and modules are explicit constants in
  `validator.py`.
- Requirement decisions use declared behavior and user stories only. Never
  infer application requirements from industry, company name, geography, IP,
  browser language, or stereotype.
- Validation is provider-neutral and fail-closed for authentication,
  authorization, object access, payment confirmation, webhook signatures and
  idempotency, secrets, uploads, subscriptions, booking, UGC, and high-risk
  operations.
- A static marketing or public content site must not acquire application
  infrastructure merely because this capability exists.

## Work Guidance

- Keep module selection minimal and dependency-aware.
- Treat machine-translated, provider-specific, and production claims as
  unverified until their own evidence exists.
- Do not generate a production implementation from a plan or validator run.

## Verification

Run `python tests/test_v2_15_application_architecture.py` for the complete
synthetic A-AV suite. Run `python -m framework_validation` for the registered
framework and compatibility checks.

## Child DOX Index

No child DOX boundaries currently exist.
