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
`test_v2_12_evidence_asset_provenance.py` owns Capability 7 synthetic A–V
evidence, claim, rights, attribution, hash, research-reference, and
frozen-integrity negative controls, plus W–AK fail-closed regression edges.
`test_v2_13_content_operations.py` owns Capability #8 synthetic A–V content
model, CMS decision, editorial lifecycle, publishing, slug, rich-text,
portability, provenance-boundary, and frozen-integrity controls.
`test_v2_14_localization.py` owns Capability #9 synthetic A-AF requirement,
locale, route, fallback, translation, formatting, RTL, typography, SEO,
content-model, accessibility, analytics, provenance, handoff, and
frozen-integrity controls.
`test_v2_15_application_architecture.py` owns conditional Capability #10
synthetic A-AV application, authentication, authorization, commerce, payment,
booking, upload, UGC, integration, high-risk, provider-outage, and
frozen-integrity controls.
`test_client_intake.py` owns the dependency-free Client Website Intake route,
contract, raw/derived artifact separation, server validation, and sample
fixture checks. It uses an ephemeral local server and temporary submission
directory only.
`test_alpha_leverage_pilot.py` owns the dependency-free Alpha Leverage local
candidate checks, including intake traceability, static content boundaries,
loopback serving, security headers, and accessibility hooks.
`test_cinematic_inspiration.py` owns the bounded V2.15 source-registry,
owner-reference, model-neutrality, rendered-screenshot, fresh-critic,
repair-recapture, five-lock, and frozen-integrity controls.
`test_owner_intent_enforcement.py` owns the deterministic owner-authority,
current-versus-historical brand, reference-boundary, contradiction,
motion-level, motion-trace, runtime-engine, generic-fade, neutral-color,
frozen-integrity, and disposable static-fixture controls.
`test_design_first_production_flow.py` owns the bounded Business Understanding
Pack, optional discovery/transcript, ambition, full-homepage, lower-half,
client-voice, owner-approval, derivation, component, inspiration, asset,
Browser QA/Gauntlet, five-lock, and frozen-integrity controls.

## Local Contracts

- Tests use temporary directories and fixtures for mutation probes.
- Tests do not modify the protected `projects/` corpus, external systems, or
  production credentials.
- Historical V2.5-V2.10 suites are direct script entrypoints and are run by
  the registry; pytest collection is limited to the registered V2.11-V2.15
  unittest suites.
- The Design Inspiration MCP suite uses synthetic structured results only and
  never requires a live Serper key or upstream package execution.
- The Evidence and Asset Provenance suite uses synthetic records and temporary
  hash fixtures only. It never retrofits historical projects or makes a live
  provider, browser, network, credential, or production request.
- The Content Operations suite uses synthetic content models, decisions,
  redirects, media/provenance references, and temporary mutation fixtures. It
  never selects a real provider, publishes content, or modifies projects/.
- The Localization suite uses synthetic locale registries, translation records,
  browser-observable page metadata, formatting, RTL, font, asset, CMS, and
  temporary mutation fixtures. It never calls a translation provider, uses
  production credentials, publishes, deploys, or modifies projects/.
- The Application Architecture suite uses synthetic behavior and observation
  fixtures only. It never creates users, charges cards, calls providers,
  sends email, publishes, deploys, or modifies projects/.
- The Client Intake suite uses a temporary local HTTP server and temporary
  artifact directory. It never submits personal data to an external service,
  modifies `projects/`, or treats localhost evidence as production proof.
- The Alpha Leverage candidate suite uses a temporary local HTTP server only.
  It never modifies `projects/`, configures GoHighLevel, collects real
  prospect data, or treats localhost evidence as production proof.
- The cinematic/inspiration suite uses synthetic owner records and screenshot
  receipts only. It never calls source sites, models, asset providers, or
  deployment services, and it never treats source-only or simulation evidence
  as rendered visual proof.
- The owner-intent suite uses synthetic records and a disposable fixture only.
  It never rebuilds Alpha Starts Now, mutates frozen pilots, calls reference
  providers, or treats a screenshot-only/static or simulation result as
  Level 2/3 runtime motion proof.
- The design-first suite uses synthetic business/design records and the
  existing inspiration registry only. It never requires a transcript, model,
  provider, browser, deployment, production credential, or mutation under
  `projects/`.
- Each required failure mode must prove a real validator signal, not merely a
  missing-file assumption.
- Tests are order-independent and runnable with the standard library.

## Work Guidance

Prefer pure validator helpers for malformed fixtures and use the registered
FrozenIntegrityGuard for frozen-project mutation evidence. Keep historical
fixtures read-only and distinguish `FAIL` from `BLOCKED`.

## Verification

Run the V2.11, V2.12, V2.13, V2.14, and V2.15 suites directly, including
`python -m unittest tests.test_cinematic_inspiration`, then run all registered
suites through `python -m framework_validation --run-suites`.

## Child DOX Index

- None.
