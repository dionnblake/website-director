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

- [provenance/](provenance): Capability 7 Evidence, Claim and Asset Provenance boundary. Owns the canonical evidence ledger, source and rights traceability, attribution, hash identity, risk classification, and deterministic validator. It does not own Asset Director readiness, Security & Privacy disclosure, or production deployment.

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

Website Director is the authoritative design governance system. It maintains deterministic progressive discovery, adaptive creative briefing (`DISCOVERY-PROTOCOL.md`), mandatory SEO/competitive intelligence, bounded unified design-inspiration discovery, external visual research, Awwwards showcase benchmarking (`AWWWARDS-SHOWCASE-INTELLIGENCE.md`), design intelligence candidate synthesis (`DESIGN-INTELLIGENCE-PROTOCOL.md`), subject-grounded distinctiveness discipline (`DESIGN-CONSTITUTION.md` §7), archetype synthesis, pre-lock high-fidelity visual prototypes (`VISUAL-PROTOTYPE-PROTOCOL.md`), owner visual direction selection, token specifications, 5-gate lock control (including deliberate motion direction), authoritative art direction & visual asset production (`ASSET-DIRECTOR-PROTOCOL.md`), immersive WebGL / Three.js specialist architecture (`IMMERSIVE-WEB-PROTOCOL.md`), interactive vector motion & state machines (`RIVE-INTERACTIVE-MOTION-PROTOCOL.md`), page experience & route continuity (`PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md`), deterministic conversion measurement, KPI hierarchy, CTA-to-event traceability, attribution & UTM governance, affiliate measurement integrity, and privacy-preserving analytics architecture (`CONVERSION-ANALYTICS-PROTOCOL.md`), production risk governance covering site risk classification, data inventory, data minimization, secret custody, form/auth/payment safeguards, security headers, transport, dependency and third-party script accountability, consent classification and truthful disclosure (`SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md`), official GSAP motion engineering (`GSAP-IMPLEMENTATION-PROTOCOL.md`), implementation contracts, deterministic Impeccable quality scans (`IMPECCABLE-ENGINE-PROTOCOL.md`), reference-grounded adversarial Gauntlet refinement loops (`WEBSITE-GAUNTLET-PROTOCOL.md`), and one canonical launch authority separating release candidate / deployed / production-verified / stabilised, requiring explicit per-release owner deployment authorization, and verifying a known release identity on the production surface (`LAUNCH-OPERATIONS-PROTOCOL.md`). See [SKILL.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/SKILL.md) for the full operating manual and the single-source-of-truth rules governing `creative_intent{}`, `research{}`, `visual_prototypes{}`, `assets{}`, `immersive{}`, `rive{}`, `page_experience{}`, `measurement{}`, `security_privacy{}`, `accessibility{}`, `browser_qa{}`, `launch_ops{}`, `motion{}`, `seo{}`, `design_intelligence{}`, and `gauntlet{}` state.

**Version:** 2.15.0 (Additive to V2.14.0, V2.13.0, V2.12.0, V2.11.1, V2.11.0, V2.10, V2.9, V2.8, V2.7, V2.6, V2.5.1, V2.5, V2.4, V2.3, V2.2, V2.1, V2.0, V1.9, V1.8, V1.7, V1.6, V1.5, V1.4, V1.3.1, V1.3, V1.2, V1.1, and V1). V2.15 integrates conditional Capability 10 Application, Commerce, and Authentication Architecture at Phase 6.99 without adding a sixth owner lock. It is activated only by explicit behavior and user stories.
**System Status:** **`WEBSITE_DIRECTOR_CAPABILITY_10_APPLICATION_ARCHITECTURE_COMPLETE`**

Historical version record: V2.7 integrates the Security, Privacy & Compliance Intelligence Subsystem; V2.13 preserves that additive compatibility contract.

Capability 8 is implemented as a provider-neutral content architecture
subsystem. Its `[CONTENT_OPERATIONS_READY]` readiness gate and
`content_ops.complete` state are separate from the V2.5 handoff authority and
do not authorize provider installation, autonomous publishing, deployment, or
production changes. Capability 9 adds a provider-neutral localization and
internationalization subsystem at Phase 6.35 with the `[LOCALIZATION_READY]`
readiness gate and `localization.complete` state. Capability 10 is implemented
as a conditional, provider-neutral application architecture subsystem at
Phase 6.99 with the `[APPLICATION_ARCHITECTURE_READY]` readiness gate and
`application.complete` state. It does not own deployment, provider accounts,
credentials, live users, live payments, or production verification.

### Localization & Internationalization Governance (V2.14 - Additive)

These rules are additive. They do not replace the existing SEO, Content
Operations, Accessibility, Security & Privacy, Measurement, Provenance,
Browser QA, Launch Operations, or V2.5 Handoff authorities.

1. **Execute Phase 6.35 when required.** Assess localization after Content
   Operations (6.25) and before Measurement (6.5). NOT_REQUIRED is valid for
   an evidence-backed English-only site; requirement is never inferred from
   IP, browser language, ethnicity, company name, or stereotype.
2. **One state and one gate.** localization.complete is the only readiness
   flag for LOCALIZATION_READY. No parallel i18n/l10n/translation state and
   no localization, language, translation, or i18n owner lock may be created.
3. **Required locale contracts are explicit.** Record one source locale, one
   default locale, BCP 47-style locale identifiers, route strategy, default
   URL policy, coverage, fallback, direction, review ownership, and SEO status.
4. **Translation is review-gated.** Machine translation is draft material.
   Human or explicitly authorized review is required before publication;
   legal translation is never automatically legally approved. Stale source
   variants remain stale until re-reviewed.
5. **Engineering is locale-aware.** Use semantic UI IDs, safe interpolation,
   plural categories, locale-aware formatting, explicit currency, unit rules,
   RTL/logical CSS, script/font provenance, expansion tests, and localized
   SEO/accessibility behavior.
6. **Adjacent authorities remain owners.** Localization consumes V2.13
   content models and V2.12 provenance, preserves slugs/redirects, reuses
   measurement event names with a locale parameter, extends the existing
   Browser QA runner, and transfers durable operations through V2.5 Handoff.
7. **No external side effects.** No provider account, translation API, live
   analytics property, production credential, publish, deploy, DNS change, or
   production verification is performed by this capability. Launch Operations
   owns production verification.
8. **Compatibility and stop boundary.** Historical profiles and frozen pilots
   may omit localization state and are not retrofitted. Capability #10
   Ecommerce, Authentication, and Application Architecture is a separate
   conditional capability governed by `APPLICATION-COMMERCE-AUTH-PROTOCOL.md`.

### Conditional Application, Commerce and Authentication Governance (V2.15 - Additive)

These rules are additive. They do not replace SEO, Content Operations,
Localization, Measurement, Security and Privacy, Accessibility, Provenance,
Browser QA, Launch Operations, or V2.5 Handoff authority.

1. **Execute Phase 6.99 when required.** Assess actual behavior and user
   stories after the preceding planning authorities and before Design System
   and implementation. Static marketing and public content sites remain
   `NOT_REQUIRED` when they have no stateful application behavior.
2. **One conditional state and one gate.** `application.complete` is the sole
   readiness flag for `[APPLICATION_ARCHITECTURE_READY]`. Do not create
   `auth.complete`, `commerce.complete`, `payments.complete`,
   `application_locked`, or an application owner lock. Exactly five owner
   locks remain.
3. **Modules are opt-in.** Activate only the module records justified by
   explicit stories and include their dependency closure. Do not activate the
   complete registry automatically.
4. **Provider-neutral and fail-closed.** Passwords, sessions, server-side
   authorization, object access, pricing, payment confirmation, order state,
   signed/idempotent webhooks, entitlements, bookings, uploads, UGC,
   transactional email, integrations, secrets, and high-risk operations have
   explicit controls. Unknown or unavailable providers are `BLOCKED`.
5. **Adjacent authorities remain owners.** Security and Privacy owns sensitive
   data and legal-review boundaries; Measurement owns events; Localization,
   Content Operations, Provenance, Accessibility, Browser QA, Launch Ops, and
   V2.5 Handoff remain their own authorities. Application readiness never
   authorizes provider setup, live users, payments, publishing, deployment, or
   production verification.

### Conversion & Analytics Governance (V2.6 — Additive)

These rules are additive. They do not replace any existing Website Director governance.

1. **Execute Phase 6.5.** After `locks.content_structure_locked` engages and before Phase 7 (Design System), agents MUST run Phase 6.5 per `CONVERSION-ANALYTICS-PROTOCOL.md` and populate `templates/measurement-plan.md`.
2. **Do not skip measurement on commercial builds.** A commercial, public-facing website may never silently proceed without a measurement plan. Absence of an analytics provider is `measurement.mode = "blocked"` with a stated `blocked_reason` — it is not an exception and it is not a reason to skip the phase.
3. **Do not fabricate conversion data.** Baselines, conversion rates, industry benchmarks, attribution chains, and downstream revenue are never invented. Unknown is `UNKNOWN`; unassessed is `UNASSESSED`. Cited external claims require a source recorded in the plan's Provenance section.
4. **Do not invent analytics implementation success.** `measurement.complete` means a plan exists. It never means analytics was observed working. Only browser + network evidence sets `measurement.implementation_verified`; only owner-supplied production evidence sets `measurement.production_verified`. Never set either by inference.
5. **Do not expose analytics secrets.** No API keys, tokens, or service-account credentials are written to the repository, the measurement plan, or generated project source.
6. **Respect existing owner locks.** Measurement never silently mutates approved IA, locked copy, CTA wording, design tokens, or motion direction. A structural conflict HALTS and produces a locked-change request for owner decision.
7. **Distinguish planning from production verification.** These three states are permanently distinct and must be reported separately in QA, the production checklist, and client handoff. A blocked integration is reported as blocked, never as passing.
8. **No external side effects.** Agents never create analytics properties, modify GTM containers or advertising accounts, install pixels on live sites, deploy, publish, transmit production analytics data, or use owner credentials.
9. **Single completion flag.** `measurement.complete` is the only authoritative readiness flag for `[CONVERSION_MEASUREMENT_COMPLETE]`. Never create a second, independently-writable measurement completion flag. Legacy `cro{}` is grandfathered and read-only.
10. **Five owner locks remain.** `[CONVERSION_MEASUREMENT_COMPLETE]` is a readiness gate, not a sixth lock.

### Security, Privacy & Compliance Governance (V2.7 — Additive)

These rules are additive. They do not replace any existing Website Director governance.

1. **Execute Phase 6.75.** After Phase 6.5 produces `measurement{}` state and before Phase 7 (Design System), agents MUST run Phase 6.75 per `SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md` and populate `templates/security-privacy-review.md`.
2. **Never certify legal compliance.** Agents must NEVER output `GDPR COMPLIANT`, `CCPA COMPLIANT`, `HIPAA COMPLIANT`, `PCI COMPLIANT`, `COPPA COMPLIANT`, or `LEGAL COMPLIANCE VERIFIED`. Permitted: `REQUIREMENTS REVIEWED`, `TECHNICAL CONTROLS IMPLEMENTED`, `KNOWN GAPS DOCUMENTED`, `LEGAL REVIEW REQUIRED`, `COMPLIANCE_NOT_CERTIFIED`. `security_privacy.compliance_certified` is permanently `false`.
3. **Requirements derive from actual functionality.** Never impose ecommerce, authentication, or payment obligations on a static brochure site; never treat an authenticated application as a brochure site.
4. **Never guess applicable law.** Jurisdiction is never inferred from an IP address or assumed geography. Where applicability cannot be reliably determined, `OWNER_OR_COUNSEL_REVIEW_REQUIRED` is the correct outcome.
5. **Escalate sensitive data.** Health, biometric, government-identifier, highly sensitive financial, and children's data escalate automatically to `SPECIALIST_REVIEW_REQUIRED`. Never self-certify.
6. **No secrets, ever.** No API keys, tokens, OAuth secrets, database credentials, or service-account material in client-side source, source control, examples, logs, screenshots, or any artifact. `.env.example` holds names and placeholders only. Never request a real credential.
7. **No unexplained third-party scripts.** Every production third-party runtime script requires a purpose, a page scope, and a consent dependency in the approved inventory.
8. **Privacy beats conversion; locks beat both.** Consent beats silent tracking, disclosure beats layout, minimization beats speculative marketing fields. A safeguard requiring a locked change HALTS and produces a locked-change request.
9. **Distinguish specification from verification.** `security_privacy.complete` means requirements are specified. Only build inspection plus browser/network evidence sets `implementation_verified`; only production evidence sets `production_verified`. Never set either by inference.
10. **Single completion flag.** `security_privacy.complete` is the only authoritative readiness flag for `[SECURITY_PRIVACY_READY]`. Never create a second security/privacy completion flag. `measurement{}` remains canonical for measurement — do not create a second analytics model.
11. **Five owner locks remain.** `[SECURITY_PRIVACY_READY]` is a readiness gate, not a sixth lock.
12. **No external side effects.** Never modify live websites, deploy, create analytics properties, configure consent platforms, change DNS, touch payment accounts, create legal documents in external systems, contact attorneys, use production credentials, transmit personal data, or run intrusive testing against external systems.

### Browser & Regression QA Governance (V2.8 — Additive)

These rules are additive. They do not replace any existing Website Director governance.

1. **Execute Phase 10.5.** After the Phase 10 build and before Phase 11, agents MUST run machine-executed browser verification per `BROWSER-REGRESSION-QA-PROTOCOL.md`, populate `templates/browser-qa-plan.md` / `browser-qa-manifest.json`, and run `browser-qa/runner.py`.
2. **Machine evidence, not assertion.** Where a requirement can be verified by machine (overflow, console, network, broken assets, form failure/success, measurement events, reduced motion, route integrity, browser-observable security), the sign-off requires the Phase 10.5 evidence manifest.
3. **The engine is replaceable; the policy is canonical.** `BROWSER_QA_ENGINE` (`playwright` real / `simulation` deterministic / a future adapter) is swappable behind `BrowserQAEngine.observe()`. The assertion catalogue, plan/manifest templates, state object, flake policy, evidence schema, and baseline governance are canonical.
4. **Never mutate frozen fixtures.** Every run wraps itself in `browser-qa/guards/frozen_integrity_guard.py`. `FROZEN_FIXTURE_MUTATION = FAIL`; a later restore does not launder it into a PASS. A passing test that changed a frozen file is a failed QA architecture. **Suites and the harness must not write anything under `projects/`.**
5. **Unavailable ≠ pass; flaky ≠ pass.** A missing engine or unreachable site is `BLOCKED` with a reason. Fail-then-pass on bounded retry is `FLAKY`, recorded in `browser_qa.flaky_tests`, never promoted to `PASS`.
6. **Local ≠ production.** `browser_qa.complete` ≠ `implementation_verified` (real browser, local build) ≠ `production_verified` (real production URL). A localhost run never sets `production_verified`; the `simulation` engine sets neither.
7. **Consume, don't duplicate.** Browser QA consumes `measurement{}` and `security_privacy{}` and reuses Impeccable's static findings. It invents no events, re-authors no requirements, and adds no duplicate static detector — it owns only the runtime-observable half (`BROWSER_EXECUTED`).
8. **No silent baseline updates, no broad ignores, no masked defects.** A visual diff is reported; a baseline change requires recorded owner authorisation. Every console/network ignore is a justified, owned, expiring manifest entry.
9. **Single completion flag.** `browser_qa.complete` is the only authoritative readiness flag for `[BROWSER_QA_PASS]`. Never create a second browser-QA completion flag.
10. **Five owner locks remain.** `[BROWSER_QA_PASS]` is a verification gate, not a sixth lock. `browser_qa{}` contains no lock boolean.
11. **Feeds the Gauntlet, does not merge with it.** Phase 11.5 does not begin until `browser_qa.complete` is `true` (or recorded `blocked`/`exception`). No new Gauntlet critic and no second state machine.
12. **No external side effects.** No browsing/testing arbitrary external sites, no real form submissions, no email, no real analytics events, no deploys, no production mutation, no destructive security testing. Framework validation uses local synthetic fixtures only.

### Accessibility Intelligence Governance (V2.9 — Additive)

These rules are additive. They do not replace any existing Website Director governance.

1. **Execute Phase 6.9.** After Phase 6.75 and before Phase 7 (Design System), agents MUST run Phase 6.9 per `ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md`, populate `templates/accessibility-review.md` / `accessibility-test-manifest.json`, and set `accessibility.complete`.
2. **One authority.** Accessibility rules scattered across the production checklist, QA rubric, Gauntlet Accessibility Critic, Impeccable contrast/target detectors, browser-QA keyboard smoke, security consent rules, and the design system are **reconciled** into this authority — never duplicated, never given a second completion flag.
3. **Default technical target: WCAG 2.2 AA** for applicable public production sites. This is a design/verification target.
4. **Never claim legal accessibility compliance.** Agents must NEVER output `ADA COMPLIANT`, `FULLY ACCESSIBLE`, `ACCESSIBILITY GUARANTEED`, `WCAG COMPLIANT`, `SECTION 508 COMPLIANT`, or `EN 301 549 COMPLIANT`. Permitted evidence-based wording: `WCAG 2.2 AA TARGET TESTS PASSED`, `MANUAL REVIEW COMPLETED`, `KNOWN ACCESSIBILITY GAPS = NONE OBSERVED`, `BLOCKED_SCREEN_READER_ENVIRONMENT`.
5. **Four distinct states.** `requirements_defined` ≠ `automated_verified` ≠ `manual_verified` ≠ `production_verified`; `screen_reader_verified` is separate again. `accessibility.complete = true` means the *spec* is implementable, never that the build passed testing.
6. **Requirements derive from real functionality.** Do not impose dialog, drag, media, or authentication criteria on a project that has none.
7. **Consume, don't duplicate.** Impeccable owns the contrast math; `MOTION-DIRECTION-PROTOCOL.md` owns the motion policy; `SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md` owns consent-requirement determination. Accessibility owns interaction accessibility and re-authors none of them.
8. **Extend V2.8 Browser QA — no separate runner.** The accessibility assertion group lives in `browser-qa/assertions/catalog.py` (source `ACCESSIBILITY_REVIEW`), gated on the plan's `accessibility` block. One runner, one evidence system, one `FrozenIntegrityGuard`. No second post-build state machine.
9. **Replaceable engine.** `axe-core` (recommended) is an implementation engine, not the policy authority. Record name + version. An unavailable engine ⇒ `BLOCKED_ACCESSIBILITY_ENGINE_UNAVAILABLE`, never PASS. Zero automated violations never establishes WCAG conformance.
10. **Screen-reader honesty.** No screen-reader environment ⇒ `BLOCKED_SCREEN_READER_ENVIRONMENT`, never PASS. An engine-clean run with a failing manual keyboard review is not a full PASS.
11. **`44×44` vs `24×24` kept distinct.** Preserve Website Director's ergonomic `44 × 44 px` where already approved; the WCAG 2.2 AA floor `24 × 24 px` is a separate, weaker criterion. Both recorded.
12. **Precedence.** Accessibility and safety override SEO and conversion. A locked visual/IA/copy/motion decision that fails a required accessibility check produces an **owner change request** — never a silent degradation in either direction. Security↔accessibility conflicts escalate to an explicit owner decision.
13. **Five owner locks remain.** `[ACCESSIBILITY_READY]` is a readiness gate, not a sixth lock. `accessibility{}` contains no lock boolean. The Gauntlet Accessibility Critic is preserved and enriched — **no new critic**.
14. **No external side effects.** No deploy, no production mutation, no testing arbitrary external sites, no real form submissions, no personal data, no consent-platform changes, no intrusive tooling against third-party systems, no push/merge without owner authorisation. Local and synthetic fixtures only.

### Launch & Post-Launch Operations Governance (V2.10 — Additive)

These rules are additive. They do not replace any existing Website Director governance.

1. **Execute Phase 12.25.** After Phase 12 pre-flight and before Phase 12.5 handoff, agents run Phase 12.25 per `LAUNCH-OPERATIONS-PROTOCOL.md`, populate `templates/launch-plan.md` / `launch-evidence-manifest.json`, and set `launch_ops.complete`.
2. **One canonical launch authority.** Release/deployment/launch logic previously implied in `PRODUCTION-CHECKLIST.md` §9–§10, the V2.5 release runbook, and historical `projects/` conventions is **reconciled** here — never duplicated, never given a second completion flag.
3. **Four permanently distinct facts.** `launch_ops.complete` (plan done) ≠ `launch_ops.deployed` ≠ the six `launch_ops.production_*_verified` flags ≠ `launch_ops.stabilization_complete`. `launch_ops.complete = true` never means deployed, production verified, or stable.
4. **`RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED`.** Deployment is an external side effect. Website Director **never deploys, pushes, merges, alters DNS, or configures SSL.** Deployment authorization is an explicit per-release owner act (or a recorded durable policy) — never inferred from passing QA, a completed build, an approved design, "looks good", a prior project, or a previous release.
5. **Verify a known release identity on the production surface.** `deployed_sha` matches `release_sha`, or `DEPLOYED_IDENTITY = UNVERIFIED` and the check is `BLOCKED`. A localhost or staging evidence manifest sets **no** `production_*_verified` flag. Never mark staging as production.
6. **Deterministic state machine.** `launch_ops.status` moves only along `launch-ops/validator.py` → `STATE_TRANSITIONS`. Impossible jumps (`NOT_EVALUATED → STABILIZED`, `RELEASE_READY → PRODUCTION_VERIFIED`) are rejected.
7. **Consume, don't duplicate.** Production Browser QA is the V2.8 harness in `environment = "production"` mode — no second runner. Production verification writes the canonical `accessibility.production_verified` / `security_privacy.production_verified` / `measurement.production_verified` fields. V2.5 `CLIENT-CMS-HANDOFF-PROTOCOL.md` owns long-term operations; Launch Operations hands its record into Phase 12.5 intake (§13) and sets `handoff_transferred`.
8. **Rollback discipline.** A rollback plan (`rollback_ready`) exists before authorization where practical; `rollback_tested` is a separate stronger flag; concrete triggers (`SEV0`/`SEV1` → `ROLLBACK_REQUIRED`) — never "rollback if something looks bad". No destructive production rollback in this task.
9. **Post-launch is protocol, not a daemon.** A site-class-sized observation window with an incident checklist (`SEV0`–`SEV3`, append-only `known_incidents[]`). No background monitoring is run. CRO optimization decisions stay out of Launch Operations.
10. **Owning specs / locks always win.** A production repair needing a change to IA, copy, tokens, motion, or to accessibility / measurement / security-privacy / SEO requirements HALTs (`status = "BLOCKED"`) and routes back with an Owner Change Request. No invisible production-only fixes.
11. **Single completion flag; five owner locks remain.** `launch_ops.complete` is the only authoritative readiness flag for `[RELEASE_READY]`. `launch_ops{}` contains no lock boolean. `[RELEASE_READY]` is a readiness gate, not a sixth lock.
12. **No external side effects.** Never deploy, push, merge, alter DNS, modify hosting, configure SSL, create monitoring services, submit production forms, send email, generate real leads or conversions, modify Search Console / analytics / consent platforms, access customer data, use production credentials, or perform rollback on a live system. Framework validation uses in-memory synthetic fixtures only.

### Validated Pilots
- **Alpha Starts Now:** Operating under `MODE = ORIGINAL_MODE`, pre-V1.1 (`schema_version` absent, four locks only). Status: **`WEBSITE_DIRECTOR_V1_PILOT_VALIDATED`** (Independent Retest 95/100 PASS; Design System V1 Frozen; Awaiting Owner Visual Review & Live Serverless Email Endpoint for Commercial Launch). This record is frozen and must not be edited or re-gated retroactively by V1.1/V1.2/V1.3/V1.4/V1.8/V1.9 tooling.
- **Alpha Starts Now (V1.6 Flagship Candidate):** Operating under `schema_version = 1.6.0` with full 5-gate lock sequence, SEO strategy, UI/UX Pro Max intelligence, owner-approved **Cinematic Midnight Alpha** art direction, GSAP Level 2 motion, and Gauntlet validation. Status: **`ALPHA_STARTS_NOW_V1_6_FLAGSHIP_OWNER_REVIEW_READY`** (Independent QA 98/100 PASS; Gauntlet 98/100 PASS; Fifth distinct visual family proven; Complete & Ready for Review).
- **Alpha Starts Now (Clean-Room Reset Candidate):** Operating under `schema_version = 1.6.0` executing Option 2 (The Raw Atelier / Obsidian Manifesto), full 5-gate lock sequence, 0px brutalist tokens, interactive Discipline Calibration Engine, GSAP Level 2 motion, and Gauntlet validation. Status: **`ALPHA_STARTS_NOW_CLEAN_ROOM_CANDIDATE_VALIDATED`** (Independent QA 97/100 PASS; 8-Critic Gauntlet PASS; Ready for Owner Visual Review).
- **Valentin & Hesse Architects:** Operating under `schema_version = 1.1.0` with full 5-gate lock sequence and Visual Research Director intelligence. Status: **`V1_1_ARCHITECTURE_PILOT_VALIDATED`** (Independent QA 94/100 PASS; Zero ASN homogenization; P1 responsive header fix applied; Frozen baseline).
- **Kreisler & Voss Motorenwerke:** Operating under `schema_version = 1.1.0` with Motion Level 3, Landbook discovery, JCodesMore forensic recon, and cinematic brief. Status: **`V1_1_AUTOMOTIVE_PILOT_VALIDATED`** (Independent QA 92/100 PASS; Zero homogenization; All 10 capability targets proven).
- **Sölvik Fjord Retreat & Thermal Sanctuary:** Operating under `schema_version = 1.1.0` with Motion Level 3, Landbook provenance audit, deep DOM recon, and bespoke concierge drawer. Status: **`V1_1_HOSPITALITY_PILOT_VALIDATED`** (Independent QA 95/100 PASS; Fourth distinct visual family proven; Complete & Validated).
- **Kestrel & Rowe Chronométrie Navale:** Operating under `schema_version = 1.6.0` with full 5-gate lock sequence, SEO intelligence, UI/UX Pro Max intelligence, Anthropic Two-Pass synthesis, official GSAP Level 2 motion, Impeccable scan, and Gauntlet Loop. Status: **`WEBSITE_DIRECTOR_V1_6_FRESH_END_TO_END_PILOT_VALIDATED`** (Independent QA 96/100 PASS; Gauntlet PASS against 3 Reference Bars; Complete & Validated).
- **ARC//FORGE Advanced Fabrication:** Operating under `schema_version = 2.5.1` with pinned horizontal scrollytelling (`PAT-01`), scroll-driven assembly (`PAT-04`), mobile reflow, reduced motion fallback, and Motion Lock 5 integration. Status: **`WEBSITE_DIRECTOR_V2_5_1_SIGNATURE_SCROLL_SPATIAL_CHOREOGRAPHY_LIBRARY_CERTIFIED`** (Independent QA PASS; 56/56 Validation Cases PASS; Complete & Validated).
- **Morrow & Vale Architecture and Industrial Design:** Operating under schema_version = 2.5.0 with full synthetic CMS, 9 handoff documents, 301 slug redirect registry, SHA-256 backup/restore proof, zero secrets, and full client independence. Status: **WEBSITE_DIRECTOR_V2_5_CLIENT_CMS_HANDOFF_SYSTEM_CERTIFIED** (Independent QA PASS; 42/42 Validation Cases PASS; Complete & Validated).
- **Thalassa Batho-Systems (V1.9 Real-Browser Certification Pilot):** Operating under `schema_version = 1.9.0` (`CREATIVE_AMBITION = SHOWCASE`, `DIRECTION_COUNT = 3`, 3 real Chromium-rendered visual prototypes, 10 divergence vectors, Portfolio Art Director audit, Asset limitation recorded). Status: **`VISUAL_PROTOTYPES_OWNER_REVIEW_READY`** (Real-Browser QA PASS; Hard Stop Enforced; Terminal Lock 1 False).

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

