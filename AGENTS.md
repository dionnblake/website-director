# DOX framework

> **Version:** 2.15.0

- DOX is highly performant AGENTS.md hierarchy installed here
- Agent must follow DOX instructions across any edits

## Core Contract

- AGENTS.md files are binding work contracts for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Read every AGENTS.md found along each route
5. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
6. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
7. If docs conflict, the closer doc controls local work details, but no child doc may weaken DOX

Do not rely on memory. Re-read the applicable DOX chain in the current session before editing.

## Update After Editing

Every meaningful change requires a DOX pass before the task is done.

Update the closest owning AGENTS.md when a change affects:

- purpose, scope, ownership, or responsibilities
- durable structure, contracts, workflows, or operating rules
- required inputs, outputs, permissions, constraints, side effects, or artifacts
- user preferences about behavior, communication, process, organization, or quality
- AGENTS.md creation, deletion, move, rename, or index contents

Update parent docs when parent-level structure, ownership, workflow, or child index changes. Update child docs when parent changes alter local rules. Remove stale or contradictory text immediately.

## Hierarchy

- Root AGENTS.md is the DOX rail: project-wide instructions, global preferences, durable workflow rules, and the top-level Child DOX Index
- Child AGENTS.md files own domain-specific instructions and their own Child DOX Index
- Each parent explains what its direct children cover and what stays owned by the parent
- The closer a doc is to the work, the more specific and practical it must be

## Style

- Keep docs concise, current, and operational
- Document stable contracts, not diary entries
- Put broad rules in parent docs and concrete details in child docs
- Prefer direct bullets with explicit names
- Do not duplicate rules across many files unless each scope needs a local version
- Delete stale notes instead of explaining history

## Closeout

1. Re-check changed paths against the DOX chain
2. Update nearest owning docs and any affected parents or children
3. Refresh every affected Child DOX Index
4. Remove stale or contradictory text
5. Run existing verification when relevant

## User Preferences

When the user requests a durable behavior change, record it here or in the relevant child AGENTS.md

## Child DOX Index

- [outputs/kernel-refactor/](outputs/kernel-refactor/AGENTS.md): Reduction inventories, certification and preservation-only worktree evidence.

- [provenance/](provenance): Capability 7 Evidence, Claim and Asset Provenance boundary. Owns the canonical evidence ledger, source and rights traceability, attribution, hash identity, risk classification, and deterministic validator. It does not own Asset Director readiness, Security & Privacy disclosure, or production deployment.
- [schemas/](schemas): Canonical machine-readable schemas, registries, compatibility records, validation manifests, and the exact five-lock contract. It owns the bounded inspiration-source registry schema without creating a new state, gate, or lock.
- [framework_validation/](framework_validation): Standard-library deterministic framework self-validation, bounded cinematic/inspiration and rendered-visual evidence helpers, and the provider-neutral Clean-Room Creative Mode execution coordinator with staged workspaces, stage-aware continuous browser morphology, and evidence-only preserved-render rechecks. It does not call providers, generate ASN, mutate frozen projects, or replace Website Director authorities.

- [intelligence/frontend-design/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/intelligence/frontend-design): Anthropic Frontend Design Distinctiveness Discipline (subject grounding, hero thesis, structural meaning, signature element, boldness budget, and evaluation helper `engine/evaluate.py`).
- [intelligence/gsap-skills/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/intelligence/gsap-skills): Official GreenSock GSAP Motion Implementation Engine (8 official skills: `core`, `timeline`, `scrolltrigger`, `plugins`, `utils`, `react`, `frameworks`, `performance`, recipes, and query adapter `engine/query.py`).
- [intelligence/ui-ux-pro-max/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/intelligence/ui-ux-pro-max): Vendored UI/UX Pro Max design intelligence dataset (192 product types, 79 styles, 192 color palettes, 74 font pairings, 119 UX guidelines, 16 stack guides) and BM25 query engine (`engine/query.py`).
- [templates/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/templates): Master reusable specification and artifact templates for all Website Director builds, including V1.1 research/motion templates, V1.2 SEO intelligence templates, V1.3 Gauntlet templates (`website-gauntlet-report.md`), V1.4 Design Intelligence templates (`design-intelligence.md`), V1.5 Motion Implementation templates (`motion-implementation-spec.md`), V1.8 Creative Briefing templates (`creative-intent-contract.md`), V1.9 Visual Prototype templates (`visual-prototype-review.md`), V2.0 Asset Director templates (`asset-intent-brief.md`, `asset-manifest.json`, `asset-provenance.md`, `photography-shot-list.md`), V2.1 Immersive Web templates (`immersive-implementation-brief.md`), V2.6 Conversion & Analytics templates (`measurement-plan.md`, `analytics-event-manifest.json`, `experiment-brief.md`), V2.7 Security, Privacy & Compliance templates (`security-privacy-review.md`, `security-privacy-register.json`), V2.8 Browser & Regression QA templates (`browser-qa-plan.md`, `browser-qa-manifest.json`), V2.9 Accessibility templates (`accessibility-review.md`, `accessibility-test-manifest.json`), V2.10 Launch Operations templates (`launch-plan.md`, `launch-evidence-manifest.json`), V2.12 Evidence & Asset Provenance templates (`evidence-ledger.md`, `evidence-ledger.json`), V2.13 Content Operations & CMS templates (`content-model.md`, `content-model.json`, `cms-decision.md`), V2.14 Localization & Internationalization templates (`localization-plan.md`, `localization-manifest.json`, `locale-registry.json`), and V2.15 Conditional Application Architecture templates (`application-architecture-plan.md`, `application-architecture-manifest.json`, `application-architecture-review.md`, `application-module-registry.json`).
- [content-ops/](content-ops): Capability #8 Content Operations and CMS Architecture validator, CMS-necessity assessment, content-model integrity, editorial lifecycle, publishing authority, slug/redirect, rich-text, portability, media-reference, and provenance-boundary checks. It does not own V2.5 long-term handoff operations or Capability #9/#10.
- [localization/](localization): Capability #9 Localization and Internationalization validator for evidence-based requirement assessment, BCP 47-style locales, routing, fallback, translation lifecycle, formatting, RTL, typography, localized SEO, accessibility, analytics, assets, provenance, and handoff. It does not own provider accounts, legal approval, production deployment, or Capability #10.
- [application/](application): Capability #10 conditional Application, Commerce, and Authentication architecture validator. Owns behavior-based requirement assessment, classifications, minimal module activation, dependency closure, security boundaries, and fail-closed synthetic controls. It does not own provider accounts, credentials, live users, live payments, deployment, production verification, adjacent state, or any owner lock.
- [integrations/](integrations): Bounded, replaceable external-evidence adapters. The V2.11.1 `design-inspiration/` child owns the audited pinned MCP discovery transport, normalized reference schema, query/credential policy, and deterministic fixtures. Integrations do not own design authority, production assets, project state, or the cross-cutting Capability 7 provenance authority.
- [launch-ops/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/launch-ops): Deterministic Phase 12.25 validators (V2.10). `validator.py` — the `launch_ops{}` status model + allowed transition graph, the `[RELEASE_READY]` readiness gate (`evaluate_release_readiness`), the owner deployment-authorization boundary (`evaluate_deployment_authorization` — `RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED`), the production-verification checks against a known release identity (`evaluate_production_verification`), and the rollback-trigger evaluator (`evaluate_rollback_trigger`). Policy is canonical (`../LAUNCH-OPERATIONS-PROTOCOL.md`). No network, no browser, no deploy; production browser verification is delegated to `browser-qa/` in `environment = "production"` mode. Directory name is hyphenated like `browser-qa/` — import `validator` by putting the directory on `sys.path`.
- [examples/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/examples): Reference documentation, the AetherDB worked example, V1.1 validation simulations, V1.3 Gauntlet validation suite (`GAUNTLET-INTEGRATION-VALIDATION.md`), V1.3.1 Impeccable validation suite (`IMPECCABLE-INTEGRATION-VALIDATION.md`), V1.4 Design Intelligence validation suite (`UIUX-INTELLIGENCE-VALIDATION.md`), V1.5 GSAP validation suite (`GSAP-INTEGRATION-VALIDATION.md`), V1.6 Frontend Design validation suite (`FRONTEND-DESIGN-INTEGRATION-VALIDATION.md`), V1.8 Creative Briefing validation suite (`CREATIVE-BRIEFING-INTEGRATION-VALIDATION.md`), V1.9 Visual Prototype validation suite (`VISUAL-PROTOTYPE-INTEGRATION-VALIDATION.md`), V2.0 Asset Director validation suite (`ASSET-DIRECTOR-INTEGRATION-VALIDATION.md`), V2.1 Immersive Web validation suite (`IMMERSIVE-WEB-INTEGRATION-VALIDATION.md`), V2.6 Conversion & Analytics validation suite (`CONVERSION-ANALYTICS-INTEGRATION-VALIDATION.md`), V2.7 Security, Privacy & Compliance validation suite (`SECURITY-PRIVACY-COMPLIANCE-INTEGRATION-VALIDATION.md`), V2.8 Browser & Regression QA validation suite (`BROWSER-REGRESSION-QA-INTEGRATION-VALIDATION.md`), V2.9 Accessibility Intelligence validation suite (`ACCESSIBILITY-INTELLIGENCE-INTEGRATION-VALIDATION.md`), V2.10 Launch & Post-Launch Operations validation suite (`LAUNCH-OPERATIONS-INTEGRATION-VALIDATION.md`), V2.13 Content Operations and CMS Architecture validation suite (`CONTENT-OPERATIONS-CMS-INTEGRATION-VALIDATION.md`), V2.14 Localization and Internationalization validation suite (`LOCALIZATION-INTERNATIONALIZATION-INTEGRATION-VALIDATION.md`), V2.15 Conditional Application Architecture validation suite (`APPLICATION-ARCHITECTURE-INTEGRATION-VALIDATION.md`), and `test_runner.py` (V2.0–V2.15 protocol/template/pilot invariant harness, including neutral `content_ops{}`/`localization{}`/`application{}`/`provenance{}` state and no-sixth-lock assertions).
- [tests/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/tests): Automated framework assertion suites run directly with `python tests/<file>.py` (exit 0 = pass). Covers V2.5 Client CMS & Handoff (`test_v2_5_client_handoff.py` — repaired under V2.8 to run all mutable CMS operations in a disposable temp copy under the frozen-integrity guard), V2.5.1 Signature Choreography, V2.7 Security/Privacy/Compliance, V2.8 Browser & Regression QA (`test_v2_8_browser_regression_qa.py` — repo invariants + scenario A–L negative controls), V2.9 Accessibility Intelligence (`test_v2_9_accessibility.py` — repo invariants + scenario A–R accessibility negative controls), V2.10 Launch & Post-Launch Operations (`test_v2_10_launch_operations.py` — repo invariants + state-machine + scenario A–R launch negative controls), V2.12 Evidence & Asset Provenance (`test_v2_12_evidence_asset_provenance.py` — A–V synthetic evidence, rights, hash, reference, and frozen-integrity controls plus W–AK fail-closed regression edges), V2.13 Content Operations & CMS (`test_v2_13_content_operations.py` — A–V synthetic content, editorial, CMS, provenance, redirect, and frozen-integrity controls), V2.14 Localization & Internationalization (`test_v2_14_localization.py` — A–AF locale, route, fallback, translation, formatting, RTL, SEO, provenance, handoff, and frozen-integrity controls), and V2.15 Application Architecture (`test_v2_15_application_architecture.py` — A–AV conditional application, authentication, authorization, commerce, payment, booking, upload, UGC, integration, provider, and frozen-integrity controls). **A suite must not mutate anything under `projects/`** — frozen certification pilots are read-only fixtures; every suite wraps itself in `browser-qa/guards/frozen_integrity_guard.py`.
- [browser-qa/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/browser-qa): Reusable, framework-level Phase 10.5 Browser & Regression QA harness (V2.15). Replaceable `BROWSER_QA_ENGINE` (`engine/` — `playwright` real + `simulation` deterministic), requirement-traced assertion catalogue (`assertions/`), frozen-project integrity guard (`guards/`), manifest-driven runner (`runner.py`), config (`config/`), and synthetic negative-control fixtures (`fixtures/`). Policy is canonical (`../BROWSER-REGRESSION-QA-PROTOCOL.md`); the engine is swappable. V2.9 adds the accessibility assertion group (`assertions/catalog.py` `check_accessibility`, source `ACCESSIBILITY_REVIEW`) and a replaceable axe-core hook in `engine/playwright_engine.py` (`vendor/axe.min.js`, git-ignored). V2.10 reuses this harness unchanged for Phase 12.25 Production Browser QA via the manifest's `"environment": "production"` — no second runner. V2.13 content behavior, V2.14 localization behavior, and V2.15 application behavior (`check_content`, `check_localization`, `check_application`) are consumed through the same harness; no second content, localization, or application runner. See `browser-qa/AGENTS.md`, `../ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md`, `../LAUNCH-OPERATIONS-PROTOCOL.md`, and `../APPLICATION-COMMERCE-AUTH-PROTOCOL.md`.
- [V2.15 cinematic proof](framework_validation/cinematic_inspiration.py): Rendered visual claims require named real-browser screenshot receipts with persisted paths, SHA-256 identity, and fresh post-repair review. Source-only, simulation-only, and stale captures cannot pass.
- [projects/alpha-starts-now/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now): Working state and specification artifacts for the Alpha Starts Now pilot. **Frozen V1 baseline — do not modify under any V1.1/V1.2/V1.3/V1.4/V1.5/V1.6/V1.7/V1.8/V1.9/V2.0/V2.1 maintenance task.**
- [projects/alpha-starts-now-v1-1/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-v1-1): Working state, visual research intelligence, token specifications, Information Architecture, Content Plan, Design System, Motion Direction, and production redesign for **Alpha Starts Now (V1.1 Production Redesign)**. Status: **`CLOSED_OWNER_APPROVED_LOCAL_CANDIDATE`** (Test Result: 98/100 PASS; Owner Approved AS-IS; Release Worktree Staged & Frozen; Production Deployment Deferred by Owner Decision).
- [projects/v1-1-architecture-pilot/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/v1-1-architecture-pilot): Working state, visual research intelligence, token specifications, and build implementation for the **VALENTIN & HESSE Architects** real-world pilot under Website Director V1.1. Status: **`V1_1_ARCHITECTURE_PILOT_VALIDATED`** (Independent QA 94/100 PASS; Cleared all 4 V1.1 supplemental gates; P1 responsive fix applied; Frozen baseline).
- [projects/v1-1-automotive-restomod-pilot/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/v1-1-automotive-restomod-pilot): Working state, visual research intelligence, Landbook provenance, JCodesMore deep recon, Motion Level 3 cinematic brief, and production build for **KREISLER & VOSS Motorenwerke**. Status: **`V1_1_AUTOMOTIVE_PILOT_VALIDATED`** (Independent QA 92/100 PASS; Cleared all capability targets; Complete & Validated).
- [projects/v1-1-luxury-hospitality-pilot/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/v1-1-luxury-hospitality-pilot): Working state, visual research intelligence, Landbook provenance, deep DOM recon, Motion Level 3 direction, and production build for **SÖLVIK FJORD RETREAT & THERMAL SANCTUARY**. Status: **`V1_1_HOSPITALITY_PILOT_VALIDATED`** (Independent QA 95/100 PASS; 4th Distinct Visual Family Certified; Complete & Validated).
- [projects/alpha-starts-now-v1-6-flagship/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-v1-6-flagship): Working state, owner-approved art direction (**Cinematic Midnight Alpha**), 5-gate locks, GSAP Level 2 cinematic kinetics, ASN Certified hardware spec grid, 7-Day Reset dossier, Impeccable audit, and Gauntlet sign-off for the **Alpha Starts Now V1.6 Flagship Candidate**. Status: **`ALPHA_STARTS_NOW_V1_6_FLAGSHIP_OWNER_REVIEW_READY`** (Independent QA 98/100 PASS; Gauntlet 98/100 PASS; Ready for Owner Visual Review).
- [projects/alpha-starts-now-clean-room/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-clean-room): Working state, clean-room art direction reset (Option 2: The Raw Atelier / Obsidian Manifesto), 0px industrial brutalist token system, interactive Discipline Calibration Engine, GSAP Level 2 kinetics. Status: **`UNAPPROVED_CREATIVE_EXPERIMENT`** (Preserved as creative experiment; awaiting explicit owner direction selection).
- [projects/v1-6-marine-chronometry-pilot/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/v1-6-marine-chronometry-pilot): Working state, visual research intelligence, SEO strategy, UI/UX Pro Max intelligence, Anthropic Two-Pass synthesis, 5-gate locks, GSAP Level 2 implementation, and Gauntlet evaluation for **KESTREL & ROWE Chronométrie Navale**. Status: **`WEBSITE_DIRECTOR_V1_6_FRESH_END_TO_END_PILOT_VALIDATED`** (Independent QA 96/100 PASS; Gauntlet PASS against 3 Reference Bars; Complete & Validated).
- [projects/v1-9-visual-prototype-certification-pilot/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/v1-9-visual-prototype-certification-pilot): Working state, visual prototype comparison review, Chromium real-rendered screenshot evidence (9 PNGs), Portfolio Art Director audit, and hard stop governance for **Thalassa Batho-Systems**. Status: **`WEBSITE_DIRECTOR_V1_9_REAL_VISUAL_CERTIFIED`** (Independent Visual QA PASS; 10 Divergence Vectors Proven; Hard Stop Enforced).
- [projects/v2-0-asset-director-pilot/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/v2-0-asset-director-pilot): Working state, Asset Intent Brief, Photography Shot List, Asset Manifest, Provenance Ledger, master/web directory separation, and Asset Readiness Gate for **VANDENBERG VELO**. Status: **`WEBSITE_DIRECTOR_V2_0_ASSET_DIRECTOR_VALIDATED`** (24/24 Validation Cases PASS; 5-Lock Invariant Maintained; Complete & Validated).
- [projects/v2-1-immersive-web-certification-pilot/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/v2-1-immersive-web-certification-pilot): Working state, Immersive Implementation Brief, procedural Three.js mechanical assembly, lighting rig, camera transitions, bounded DPR, zero-CLS WebGL fallback, reduced motion, and real-browser WebGL certification for **AETHEL Precision Horology & Chronométrie**. Status: **`WEBSITE_DIRECTOR_V2_1_IMMERSIVE_WEB_SPECIALIST_CERTIFIED`** (Real Chromium WebGL QA PASS; 28/28 Validation Cases PASS; 5-Lock Invariant Maintained; Complete & Validated).
- [projects/v2-2-rive-certification-pilot/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/v2-2-rive-certification-pilot): Working state, Rive Implementation Brief, state machine interactive vehicle readiness gauge, touch/keyboard accessible inputs, zero-CLS SVG fallback, reduced motion, and real-browser Rive certification for **KINETIX Biometric Endurance & Recovery**. Status: **`WEBSITE_DIRECTOR_V2_2_RIVE_INTERACTIVE_MOTION_SPECIALIST_CERTIFIED`** (Real Chromium Rive QA PASS; 28/28 Validation Cases PASS; 5-Lock Invariant Maintained; Complete & Validated).
- [projects/v2-3-page-experience-certification-pilot/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/v2-3-page-experience-certification-pilot): Working state, Page Experience Brief, multi-route MPA architecture, native View Transitions, shared-element media expansion, history parity, scroll restoration, reduced-motion bypass, and real-browser certification for **ATLAS FORM Architecture & Industrial Design Journal**. Status: **`WEBSITE_DIRECTOR_V2_3_PAGE_EXPERIENCE_TRANSITION_SYSTEM_CERTIFIED`** (Real Chromium QA PASS; 30/30 Validation Cases PASS; 5-Lock Invariant Maintained; Complete & Validated).
- [projects/v2-5-1-signature-choreography-certification-pilot/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/v2-5-1-signature-choreography-certification-pilot): Working state, 18-pattern library integration, Signature Interaction Brief, pinned horizontal scrollytelling, scroll-driven assembly, mobile reflow, and zero-lock spatial choreography for **ARC//FORGE Advanced Fabrication**. Status: **`WEBSITE_DIRECTOR_V2_5_1_SIGNATURE_SCROLL_SPATIAL_CHOREOGRAPHY_LIBRARY_CERTIFIED`** (32/32 Automated Assertions PASS; 56/56 Validation Cases PASS; Complete & Validated).
- [projects/v2-5-client-handoff-certification-pilot/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/v2-5-client-handoff-certification-pilot): Working state, synthetic CMS content models, permission matrices, slug change 301 redirects, SHA-256 backup/restore proof, complete 9-document handoff package, and client independence certification for **Morrow & Vale Architecture and Industrial Design**. Status: **WEBSITE_DIRECTOR_V2_5_CLIENT_CMS_HANDOFF_SYSTEM_CERTIFIED** (37/37 Automated Assertions PASS; 42/42 Validation Cases PASS; 5-Lock Invariant Maintained; Complete & Validated).
- [projects/alpha-starts-now-flagship-proof/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-flagship-proof): Working state, verified brand truth ledger, live showcase research, three distinct Chromium-rendered prototypes, complete 5-gate specification locks, and standalone production build for the **Alpha Starts Now (The 5 Morning Rituals)** flagship. Status: **`PRODUCTION_DEPLOYMENT_READY`** (Approved: Direction C — The Dawn Vanguard; Production SHA-256: `63C77DA756B6857C73B7B9F7FF73D2B7FC3095ACC644E0DB149890956F84B049`).
- [projects/v2-4-cro-analytics-certification-pilot/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/v2-4-cro-analytics-certification-pilot): Working state, Analytics Measurement Plan, Event Manifest, synthetic bus, experiment brief, deterministic assignment, PII rejection, page-view deduplication, and real-browser certification for **NORTHSTAR Performance Lab**. Status: **`WEBSITE_DIRECTOR_V2_4_CRO_ANALYTICS_EXPERIMENTATION_SYSTEM_CERTIFIED`** (Real Chromium QA PASS; 32/32 Validation Cases PASS; 5-Lock Invariant Maintained; Complete & Validated).

---

# WEBSITE-DIRECTOR

**Version:** 2.15.0
Website Director owns design governance and exactly five owner locks.
The protocol catalog is available on demand via schemas/protocols.json.
SKILL.md controls lifecycle and activation; module documents own their bounded behavior.

## Resident governance and activation

FEATURE_FREEZE = ACTIVE. refactor/kernel is reduction only; no new capability,
specialist, protocol, readiness gate, design engine, or feature version.
Website and ASN generation are frozen for this task. No production changes.
The seven top-level gates are BRIEF, DIRECTION, IA, CONTENT, BUILD, VERIFY, LAUNCH.
SKILL.md is the resident operating kernel and owns the only activation table.
Do not preload README history, protocols, specialist skill manuals, or frozen pilots.
Decimal phases are internal activities. Child ownership does not imply activation.
Exactly five owner locks remain; schemas/state-ownership.json owns state semantics.
No evidence means no verification. complete is not implementation_verified, which
is not production_verified. Unknown baseline and unavailable engines fail closed.
BrowserQAEngine.observe() and FrozenIntegrityGuard remain mandatory contracts.

### Accessibility Intelligence Governance

ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md owns component requirements and manual
versus automated evidence. Never infer WCAG or ADA compliance from automated checks.

### Security, Privacy & Compliance Governance

SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md owns safeguards, disclosure and data
boundaries. It cannot grant legal compliance or consequential-action approval.

### Launch & Post-Launch Operations Governance

LAUNCH-OPERATIONS-PROTOCOL.md and launch-ops/validator.py own release facts and
the canonical transition graph. RELEASE_READY does not authorize deployment.
Owner authorization is required for push, merge, deploy, DNS and production actions.
This refactor request authorizes a certified commit and push, then stop without merge.

## Refactor evidence ownership

outputs/kernel-refactor/ owns inventories, before/after metrics, certification and
the preservation-only worktree plan. work/kernel-refactor/ holds disposable helpers;
remove them after certification. Keep the isolated worktree for review after push.
No pruning or deletion of other worktrees, branches, or evidence is authorized.

## Framework self-validation contract

<!-- FRAMEWORK_VERSION: 2.15.0 -->
<!-- FRAMEWORK_GOVERNANCE
framework_version_source=framework-version.json
owner_locks=design_direction_locked,information_architecture_locked,content_structure_locked,design_system_locked,motion_direction_locked
frozen_projects=projects/
deployment_authority=OWNER_APPROVAL_REQUIRED
external_side_effects=NONE
state_ownership=schemas/state-ownership.json
browser_qa=browser-qa/guards/frozen_integrity_guard.py
accessibility=owner-controlled historical protocol state
security_privacy=owner-controlled historical protocol state
content_ops=content_ops.complete
localization=localization.complete
framework_phase=0:Framework Self-Validation:ACTIVE
framework_gate=FRAMEWORK_VALIDATION_PASS
framework_validation_state=EXTERNAL_TO_SITE_PROFILE
-->

Capability 6 is the framework's self-validation and CI layer. Its canonical
protocol is `FRAMEWORK-VALIDATION-PROTOCOL.md`; its version source is
`framework-version.json`; and its executable surface is `framework_validation/`.
It validates framework structure, schemas, references, state ownership,
historical compatibility, frozen-project integrity, test isolation, negative
controls, and read-only CI policy. Capability 6.5 is the bounded Design
Inspiration MCP adapter under `integrations/design-inspiration/`; it supplies
reference evidence to Visual Research and has its own deterministic suite.

The certified V2.10 lineage and its real frozen `projects/` corpus remain
authoritative. Framework validation and the adapter are additive and external
to `templates/site-profile.json`. The five owner locks are the complete set.
No measurement, SEO, security, privacy, accessibility, browser-QA, launch,
asset, handoff, framework-validation, or adapter state may become an owner
lock. Capability 7 Evidence & Asset Provenance is now implemented at Phase
6.95 through EVIDENCE-PROVENANCE-PROTOCOL.md, provenance/validator.py, and the
provenance.complete state. Capability 8 Content Operations and CMS Architecture
is implemented in this checkout. Capability 9 Localization and Internationalization
is implemented at Phase 6.35 through the canonical protocol, localization/
validator.py, `localization.complete`, and `[LOCALIZATION_READY]`. Capability 10
is implemented conditionally at Phase 6.99 through the canonical application
protocol, `application/validator.py`, `application.complete`, and
`[APPLICATION_ARCHITECTURE_READY]`.

Capability 8 Content Operations and CMS Architecture is implemented at Phase
6.25 through `CONTENT-OPERATIONS-CMS-PROTOCOL.md`, `content-ops/validator.py`,
the `content_ops.complete` state, and the `[CONTENT_OPERATIONS_READY]`
readiness gate. It remains distinct from V2.5 client handoff operations and
adds no owner lock. Localization remains distinct from Content Operations,
Measurement, SEO, Accessibility, Security and Privacy, Provenance, Browser QA,
Launch Ops, and V2.5 Handoff. Capability 10 remains conditional and provider-
neutral; it is activated only when application behavior or user stories
require it and adds no owner lock.

The adapter accepts only the audited immutable upstream commit, keeps
`SERPER_API_KEY` environment-only, recognizes five platforms through one
replaceable transport, refuses exact-copy requests, keeps image URLs
`REFERENCE_ONLY`, and leaves token extraction blocked unless deliberate
reference-deconstruction conditions are independently satisfied.

## Framework validation Child DOX Index

- `.github/AGENTS.md` - read-only CI workflow boundary.
- `framework-validation/AGENTS.md` - certification report and runtime artifact boundary.
- `framework_validation/AGENTS.md` - deterministic validator package and CLI.
- `schemas/AGENTS.md` - canonical framework registries, schemas, and compatibility policy.

