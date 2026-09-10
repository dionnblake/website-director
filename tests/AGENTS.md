# Framework Validation Tests

## Purpose

Own deterministic tests for Website Director framework self-validation,
compatibility, negative controls, isolation, and release evidence.

## Ownership

`test_framework_validation.py` owns the Capability 6 regression, historical
compatibility fixture, and negative-control suite registered in
`schemas/test-suites.json`. It also owns the seven-stage kernel routing table,
one-primary-stage invariant, default-path boundaries, conditional dispatch,
and deterministic agent-comprehension assertions. These are documentation and
governance checks only; they create no kernel runtime state.
`test_design_inspiration.py` owns the deterministic Capability 6.5 adapter,
credential, provenance, originality, token, and frozen-integrity controls.
`test_asset_provenance.py` owns Capability 7 synthetic evidence, claim, rights,
attribution, hash, research-reference, and frozen-integrity negative controls,
plus fail-closed regression edges.
`test_content_operations.py` owns Capability #8 synthetic content
model, CMS decision, editorial lifecycle, publishing, slug, rich-text,
portability, provenance-boundary, and frozen-integrity controls.
`test_localization.py` owns Capability #9 synthetic locale requirement,
locale, route, fallback, translation, formatting, RTL, typography, SEO,
content-model, accessibility, analytics, provenance, handoff, and
frozen-integrity controls.
`test_application_architecture.py` owns conditional Capability #10
synthetic A-AV application, authentication, authorization, commerce, payment,
booking, upload, UGC, integration, high-risk, provider-outage, and
frozen-integrity controls.
`test_security_privacy.py` owns the deterministic security, privacy,
compliance, legal-claim, secret-boundary, and frozen-integrity controls.
`test_browser_qa.py` is the canonical Browser QA composite. It owns browser
repository invariants, runtime observations, accessibility integration, all
Browser QA negative controls, and the shared frozen-integrity boundary.
`accessibility_cases.py` is a child case module executed by that composite;
it is not independently registered or pytest-discoverable.
`test_release_and_handoff.py` is the canonical release composite. It owns
release readiness, deployment authorization, production verification,
rollback, and the client handoff boundary.
`client_handoff_cases.py` is a child case module executed by that composite;
it is not independently registered or pytest-discoverable.
`test_cinematic_inspiration.py` owns the bounded V2.15 source-registry,
owner-reference, model-neutrality, rendered-screenshot, fresh-critic,
repair-recapture, five-lock, and frozen-integrity controls.
`test_design_and_motion.py` owns the deterministic owner-authority,
current-versus-historical brand, reference-boundary, contradiction,
motion-level, motion-trace, runtime-engine, generic-fade, neutral-color,
signature choreography compatibility, frozen-integrity, and disposable
static-fixture controls.
`test_design_first_production_flow.py` owns the bounded Business Understanding
Pack, optional discovery/transcript, ambition, full-homepage, lower-half,
client-voice, owner-approval, derivation, component, inspiration, asset,
Browser QA/Gauntlet, five-lock, and frozen-integrity controls.
`test_clean_room_creative_mode.py` owns the clean-room operating mode
quarantine, physical staged-workspace, provenance, pre-generation
cheap-concept, ordered execution, browser-derived morphology, blind-critic,
owner-selection unlock, and zero-side-effect synthetic end-to-end controls.

`test_impeccable.py` owns the synthetic proof for the bounded Impeccable
source scanner: the existing 18-rule contract, the selected v4.3.1 additions,
selected-output-root traversal, nested-ignore behavior, fail-closed empty and
unsupported-input controls, finding normalization, contextual authorization,
lock protection, official engine fail-closed controls, single-owner boundaries
for heading and image checks, owner separation, path handling, frozen
integrity, and historical compatibility. It is a child module of the
framework_validation suite, not a new registered suite.
`test_copy_quality.py` owns the synthetic proof for the bounded source-copy
pattern precheck: positive and negative controls for each adopted rule,
locale applicability, Markdown extraction, Unicode normalization, finding and
lock metadata, proof ownership, determinism, provider/process absence, and
protected-corpus read-only behavior. It is a child module of the existing
framework_validation suite, not a new registered suite.

## Local Contracts

- Tests use temporary directories and fixtures for mutation probes.
- Tests do not modify the protected `projects/` corpus, external systems, or
  production credentials. The protected checkout boundary now contains the
  five active Alpha Starts Now projects; historical certification behavior is
  represented by small synthetic fixtures.
- The registry is the one canonical full-verification entrypoint. Composite
  scripts may execute child case modules, but only the 13 registry entries are
  active suites. Pytest collection remains limited to the two standard-library
  unit modules named in `pyproject.toml`. These suites must not require
  complete historical project directories.
- The Design Inspiration MCP suite uses synthetic structured results only and
  never requires a live Serper key or upstream package execution.
- The copy-quality tests use supplied text and read-only repository fixtures
  only. They never rewrite copy, call a provider or model, add a gate or lock,
  or modify the protected projects corpus. Every scan supplies the existing
  canonical `content_locked` boolean explicitly and covers missing and
  non-boolean lock context as fail-closed inputs.
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
- The clean-room suite uses provider-neutral synthetic adapters plus the
  existing Playwright engine for the rendered proof. It proves that historical
  input is blocked before adapter execution and absent from the staged pack,
  the bounded generator package contains no historical sentinels,
  negative-baseline loading happens after candidate rendering, the blind
  critic receives no implementation source or builder secrets, morphology is
  derived from browser layout rather than labels, and the existing owner
  selection authority unlocks full-homepage progression without a new lock.
- Each required failure mode must prove a real validator signal, not merely a
  missing-file assumption.
- Tests are order-independent and runnable with the standard library.

## Work Guidance

Prefer pure validator helpers for malformed fixtures and use the registered
FrozenIntegrityGuard for protected-project mutation evidence. Use disposable
minimal fixtures for unchanged, modification, addition, deletion, and
restore-after-observation controls. Keep compatibility fixtures read-only and
distinguish `FAIL` from `BLOCKED`.

## Verification

Run targeted composite or child cases only while developing. The completion
path is `python -m framework_validation --run-suites`, which discovers all 13
registered suites, including the browser/accessibility and release/handoff
composites, then inspect the generated report and frozen-integrity evidence.

## Child DOX Index

- None.
