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
- [schemas/](schemas): Canonical machine-readable schemas, registries, compatibility records, validation manifests, and the exact five-lock contract. It owns the bounded inspiration-source registry schema without creating a new state, gate, or lock.
- [framework_validation/](framework_validation): Standard-library deterministic framework self-validation, bounded cinematic/inspiration and rendered-visual evidence helpers, and the provider-neutral clean-room execution coordinator for the Visual Prototype operating mode with physical staged-workspace and browser-morphology proof. It does not call providers, generate ASN, mutate frozen projects, or replace Website Director authorities.

- [intelligence/frontend-design/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/intelligence/frontend-design): Anthropic Frontend Design Distinctiveness Discipline (subject grounding, hero thesis, structural meaning, signature element, boldness budget, and evaluation helper `engine/evaluate.py`).
- [intelligence/gsap-skills/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/intelligence/gsap-skills): Official GreenSock GSAP Motion Implementation Engine (8 official skills: `core`, `timeline`, `scrolltrigger`, `plugins`, `utils`, `react`, `frameworks`, `performance`, recipes, and query adapter `engine/query.py`).
- [intelligence/ui-ux-pro-max/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/intelligence/ui-ux-pro-max): Vendored UI/UX Pro Max design intelligence dataset (192 product types, 79 styles, 192 color palettes, 74 font pairings, 119 UX guidelines, 16 stack guides) and BM25 query engine (`engine/query.py`).
- [templates/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/templates): Master reusable specification and artifact templates for all Website Director builds, including V1.1 research/motion templates, V1.2 SEO intelligence templates, V1.3 Gauntlet templates (`website-gauntlet-report.md`), V1.4 Design Intelligence templates (`design-intelligence.md`), V1.5 Motion Implementation templates (`motion-implementation-spec.md`), V1.8 Creative Briefing templates (`creative-intent-contract.md`), V1.9 Visual Prototype templates (`visual-prototype-review.md`), V2.0 Asset Director templates (`asset-intent-brief.md`, `asset-manifest.json`, `asset-provenance.md`, `photography-shot-list.md`), V2.1 Immersive Web templates (`immersive-implementation-brief.md`), V2.6 Conversion & Analytics templates (`measurement-plan.md`, `analytics-event-manifest.json`, `experiment-brief.md`), V2.7 Security, Privacy & Compliance templates (`security-privacy-review.md`, `security-privacy-register.json`), V2.8 Browser & Regression QA templates (`browser-qa-plan.md`, `browser-qa-manifest.json`), V2.9 Accessibility templates (`accessibility-review.md`, `accessibility-test-manifest.json`), V2.10 Launch Operations templates (`launch-plan.md`, `launch-evidence-manifest.json`), V2.12 Evidence & Asset Provenance templates (`evidence-ledger.md`, `evidence-ledger.json`), V2.13 Content Operations & CMS templates (`content-model.md`, `content-model.json`, `cms-decision.md`), V2.14 Localization & Internationalization templates (`localization-plan.md`, `localization-manifest.json`, `locale-registry.json`), and V2.15 Conditional Application Architecture templates (`application-architecture-plan.md`, `application-architecture-manifest.json`, `application-architecture-review.md`, `application-module-registry.json`).
- [content-ops/](content-ops): Capability #8 Content Operations and CMS Architecture validator, CMS-necessity assessment, content-model integrity, editorial lifecycle, publishing authority, slug/redirect, rich-text, portability, media-reference, and provenance-boundary checks. It does not own V2.5 long-term handoff operations or Capability #9/#10.
- [localization/](localization): Capability #9 Localization and Internationalization validator for evidence-based requirement assessment, BCP 47-style locales, routing, fallback, translation lifecycle, formatting, RTL, typography, localized SEO, accessibility, analytics, assets, provenance, and handoff. It does not own provider accounts, legal approval, production deployment, or Capability #10.
- [application/](application): Capability #10 conditional Application, Commerce, and Authentication architecture validator. Owns behavior-based requirement assessment, classifications, minimal module activation, dependency closure, security boundaries, and fail-closed synthetic controls. It does not own provider accounts, credentials, live users, live payments, deployment, production verification, adjacent state, or any owner lock.
- [integrations/](integrations): Bounded, replaceable external-evidence adapters. The V2.11.1 `design-inspiration/` child owns the audited pinned MCP discovery transport, normalized reference schema, query/credential policy, and deterministic fixtures. Integrations do not own design authority, production assets, project state, or the cross-cutting Capability 7 provenance authority.
- [launch-ops/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/launch-ops): Deterministic Phase 12.25 validators (V2.10). `validator.py` — the `launch_ops{}` status model + allowed transition graph, the `[RELEASE_READY]` readiness gate (`evaluate_release_readiness`), the owner deployment-authorization boundary (`evaluate_deployment_authorization` — `RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED`), the production-verification checks against a known release identity (`evaluate_production_verification`), and the rollback-trigger evaluator (`evaluate_rollback_trigger`). Policy is canonical (`../LAUNCH-OPERATIONS-PROTOCOL.md`). No network, no browser, no deploy; production browser verification is delegated to `browser-qa/` in `environment = "production"` mode. Directory name is hyphenated like `browser-qa/` — import `validator` by putting the directory on `sys.path`.
- [examples/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/examples): Reference documentation, the AetherDB worked example, V1.1 validation simulations, V1.3 Gauntlet validation suite (`GAUNTLET-INTEGRATION-VALIDATION.md`), V1.3.1 Impeccable validation suite (`IMPECCABLE-INTEGRATION-VALIDATION.md`), V1.4 Design Intelligence validation suite (`UIUX-INTELLIGENCE-VALIDATION.md`), V1.5 GSAP validation suite (`GSAP-INTEGRATION-VALIDATION.md`), V1.6 Frontend Design validation suite (`FRONTEND-DESIGN-INTEGRATION-VALIDATION.md`), V1.8 Creative Briefing validation suite (`CREATIVE-BRIEFING-INTEGRATION-VALIDATION.md`), V1.9 Visual Prototype validation suite (`VISUAL-PROTOTYPE-INTEGRATION-VALIDATION.md`), V2.0 Asset Director validation suite (`ASSET-DIRECTOR-INTEGRATION-VALIDATION.md`), V2.1 Immersive Web validation suite (`IMMERSIVE-WEB-INTEGRATION-VALIDATION.md`), V2.6 Conversion & Analytics validation suite (`CONVERSION-ANALYTICS-INTEGRATION-VALIDATION.md`), V2.7 Security, Privacy & Compliance validation suite (`SECURITY-PRIVACY-COMPLIANCE-INTEGRATION-VALIDATION.md`), V2.8 Browser & Regression QA validation suite (`BROWSER-REGRESSION-QA-INTEGRATION-VALIDATION.md`), V2.9 Accessibility Intelligence validation suite (`ACCESSIBILITY-INTELLIGENCE-INTEGRATION-VALIDATION.md`), V2.10 Launch & Post-Launch Operations validation suite (`LAUNCH-OPERATIONS-INTEGRATION-VALIDATION.md`), V2.13 Content Operations and CMS Architecture validation suite (`CONTENT-OPERATIONS-CMS-INTEGRATION-VALIDATION.md`), V2.14 Localization and Internationalization validation suite (`LOCALIZATION-INTERNATIONALIZATION-INTEGRATION-VALIDATION.md`), V2.15 Conditional Application Architecture validation suite (`APPLICATION-ARCHITECTURE-INTEGRATION-VALIDATION.md`). Examples are reference-only; executable verification lives in `schemas/test-suites.json`.
- [tests/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/tests): The canonical 13-suite registry combines current behavior names, browser/accessibility controls, release/client-handoff controls, and historical compatibility fixtures. Composite suites may execute non-discoverable child case modules, but no suite may mutate `projects/`; every protected-project run uses `browser-qa/guards/frozen_integrity_guard.py`.
- [browser-qa/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/browser-qa): Reusable, framework-level Phase 10.5 Browser & Regression QA harness (V2.15). Replaceable `BROWSER_QA_ENGINE` (`engine/` — `playwright` real + `simulation` deterministic), requirement-traced assertion catalogue (`assertions/`), frozen-project integrity guard (`guards/`), manifest-driven runner (`runner.py`), config (`config/`), and synthetic negative-control fixtures (`fixtures/`). Policy is canonical (`../BROWSER-REGRESSION-QA-PROTOCOL.md`); the engine is swappable. V2.9 adds the accessibility assertion group (`assertions/catalog.py` `check_accessibility`, source `ACCESSIBILITY_REVIEW`) and a replaceable axe-core hook in `engine/playwright_engine.py` (`vendor/axe.min.js`, git-ignored). V2.10 reuses this harness unchanged for Phase 12.25 Production Browser QA via the manifest's `"environment": "production"` — no second runner. V2.13 content behavior, V2.14 localization behavior, and V2.15 application behavior (`check_content`, `check_localization`, `check_application`) are consumed through the same harness; no second content, localization, or application runner. See `browser-qa/AGENTS.md`, `../ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md`, `../LAUNCH-OPERATIONS-PROTOCOL.md`, and `../APPLICATION-COMMERCE-AUTH-PROTOCOL.md`.
- [V2.15 cinematic proof](framework_validation/cinematic_inspiration.py): Rendered visual claims require named real-browser screenshot receipts with persisted paths, SHA-256 identity, and fresh post-repair review. Source-only, simulation-only, and stale captures cannot pass.
- [projects/alpha-starts-now/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now): Working state and specification artifacts for the Alpha Starts Now pilot. **Frozen V1 baseline — do not modify under any V1.1/V1.2/V1.3/V1.4/V1.5/V1.6/V1.7/V1.8/V1.9/V2.0/V2.1 maintenance task.**
- [projects/alpha-starts-now-v1-1/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-v1-1): Working state, visual research intelligence, token specifications, Information Architecture, Content Plan, Design System, Motion Direction, and production redesign for **Alpha Starts Now (V1.1 Production Redesign)**. Status: **`CLOSED_OWNER_APPROVED_LOCAL_CANDIDATE`** (Test Result: 98/100 PASS; Owner Approved AS-IS; Release Worktree Staged & Frozen; Production Deployment Deferred by Owner Decision).
- [projects/alpha-starts-now-v1-6-flagship/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-v1-6-flagship): Working state, owner-approved art direction (**Cinematic Midnight Alpha**), 5-gate locks, GSAP Level 2 cinematic kinetics, ASN Certified hardware spec grid, 7-Day Reset dossier, Impeccable audit, and Gauntlet sign-off for the **Alpha Starts Now V1.6 Flagship Candidate**. Status: **`ALPHA_STARTS_NOW_V1_6_FLAGSHIP_OWNER_REVIEW_READY`** (Independent QA 98/100 PASS; Gauntlet 98/100 PASS; Ready for Owner Visual Review).
- [projects/alpha-starts-now-clean-room/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-clean-room): Working state, clean-room art direction reset (Option 2: The Raw Atelier / Obsidian Manifesto), 0px industrial brutalist token system, interactive Discipline Calibration Engine, GSAP Level 2 kinetics. Status: **`UNAPPROVED_CREATIVE_EXPERIMENT`** (Preserved as creative experiment; awaiting explicit owner direction selection).
- [projects/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects): Five active Alpha Starts Now project surfaces remain protected and are never mutated by framework tests. Historical certification project directories are archived from the active checkout; Git history is the recovery authority, and compatibility behavior is covered by small synthetic fixtures under `tests/fixtures/`.
- [projects/alpha-starts-now-flagship-proof/](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-flagship-proof): Working state, verified brand truth ledger, live showcase research, three distinct Chromium-rendered prototypes, complete 5-gate specification locks, and standalone production build for the **Alpha Starts Now (The 5 Morning Rituals)** flagship. Status: **`PRODUCTION_DEPLOYMENT_READY`** (Approved: Direction C — The Dawn Vanguard; Production SHA-256: `63C77DA756B6857C73B7B9F7FF73D2B7FC3095ACC644E0DB149890956F84B049`).

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

The specialist policy is canonical in
`LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md`, with machine-readable
artifacts owned by `localization/` and `templates/`. This root contract keeps
only the routing boundary: localization is evidence-based, provider-neutral,
review-gated, separate from adjacent authorities, and never a sixth owner
lock or authorization for publishing, deployment, or production verification.

### Conditional Application, Commerce and Authentication Governance (V2.15 - Additive)

The specialist policy is canonical in
`APPLICATION-COMMERCE-AUTH-PROTOCOL.md`, with executable checks owned by
`application/`. This root contract keeps only the routing boundary:
application architecture is conditional, opt-in, provider-neutral,
fail-closed, separate from live users/payments/deployment, and adds no owner
lock.

### Cinematic Production Intelligence, Inspiration and Rendered Proof (V2.15 - Additive)

The specialist policies are canonical in `CINEMATIC-INTEGRATION-PROTOCOL.md`,
`VISUAL-RESEARCH-PROTOCOL.md`, `AWWWARDS-SHOWCASE-INTELLIGENCE.md`, and the
existing Visual Prototype and Browser QA authorities. The bounded
`templates/inspiration-source-registry.json` is reference-only data, not a
second design authority. Rendered claims remain fail-closed and require fresh
real-browser receipts; no provider, project, lock, or deployment authority is
created here.

### Design-First Production Flow (V2.15 bounded operating overlay)

Design-first is an operating mode of `VISUAL-PROTOTYPE-PROTOCOL.md`. It
requires business understanding before visual design, a complete rendered
homepage before full production implementation, explicit owner review before
Design System derivation, and inheritance of the approved homepage system by
the remaining pages.

The flow may record
`visual_prototypes.homepage_visual_approved` under the existing Visual
Prototype object as approval evidence. It creates no new phase, readiness
gate, state authority, or owner lock. The exact five owner locks remain the
only owner locks. Clean-room is another bounded mode of that same authority;
its execution coordinator remains in `framework_validation/`. Browser QA
remains the behavior authority and the Website Gauntlet remains the post-QA
qualitative authority.

### Alpha Starts Now Brand Color Authority (Owner Contract — 2026-09-02)

For current and future non-frozen Alpha Starts Now work, the authoritative
brand palette is **navy blue as primary** and **yellow as accent**. White and
restrained light/dark neutrals may support contrast and accessibility.
The machine-readable current owner contract is
`templates/alpha-starts-now-owner-intent.json`; its semantic tokens are
`ASN_NAVY` and `ASN_YELLOW` and it intentionally does not invent exact hex
values. The authority precedence and enforcement behavior are canonical in
`FRAMEWORK-VALIDATION-PROTOCOL.md` and
`framework_validation/owner_intent.py`.
Historical Alpha Starts Now palettes are comparison-only and must not be used
to infer current brand colors. Orange, burnt orange, peach, amber, beige,
dominant cream, black/silver/white primary palettes, and older orange/blue
combinations are not current brand authority. Reference websites may inform
composition, movement, typography, interaction, pacing, spatial design, and
section transitions, but may not redefine the Alpha Starts Now palette. Any
proposed palette change requires explicit owner approval. Frozen historical
projects remain immutable; this contract governs active and future work and
does not retroactively re-gate those artifacts.

### Conversion & Analytics Governance (V2.6 — Additive)

The specialist policy is canonical in `CONVERSION-ANALYTICS-PROTOCOL.md`.
Measurement planning, experimentation, event contracts, and implementation
verification remain one `measurement{}` authority; historical `cro{}` state is
read-only. This root contract preserves only the boundary that measurement is
fail-closed, secret-free, lock-aware, and never a sixth owner lock.

### Security, Privacy & Compliance Governance (V2.7 — Additive)

The specialist policy is canonical in
`SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md`. It owns proportional risk,
privacy, consent, secrets, and legal-review boundaries. This root contract
preserves only the fail-closed boundary: requirements derive from actual
functionality, compliance is never self-certified, no credentials or external
systems are used, and the capability adds no owner lock.

### Browser & Regression QA Governance (V2.8 — Additive)

The specialist policy and single runner are canonical in
`BROWSER-REGRESSION-QA-PROTOCOL.md` and `browser-qa/`. Browser QA owns
deterministic machine evidence, frozen-project integrity, and the distinction
between local implementation and production verification. It feeds, but does
not merge with, the qualitative Website Gauntlet, and adds no owner lock.

### Accessibility Intelligence Governance (V2.9 — Additive)

The specialist policy is canonical in
`ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md`; its assertion group extends the
existing `browser-qa/` runner. Accessibility owns applicable interaction
requirements and specialist evidence, while Impeccable, Motion, Security and
the Gauntlet retain their distinct responsibilities. It never certifies legal
conformance and adds no owner lock.

### Launch & Post-Launch Operations Governance (V2.10 — Additive)

The specialist policy and state machine are canonical in
`LAUNCH-OPERATIONS-PROTOCOL.md` and `launch-ops/`. This root contract keeps
only the routing boundary: `launch_ops{}` is the single launch-state
authority, `RELEASE_READY` is distinct from owner deployment authorization,
production identity remains separately verified, and V2.5
`CLIENT-CMS-HANDOFF-PROTOCOL.md` owns long-term operations. No deploy,
publish, DNS change, credential use, or production mutation is authorized by
this repository contract.

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

The certified V2.10 lineage and the five active protected Alpha Starts Now
projects remain authoritative. Historical certification artifacts are preserved
by Git history rather than an in-checkout archive copy. Framework validation and
the adapter are additive and external to `templates/site-profile.json`. The
five owner locks are the complete set.
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

