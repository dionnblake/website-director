# WEBSITE DIRECTOR

> **Version:** 2.11.0  
> **Status:** Production-Grade Skill & Specification System  
> **Purpose:** Turn vague business requirements into production-grade website design and implementation specifications, informed by adaptive creative briefing (Creative Briefing Room V1.8), real search demand, competitive intelligence, external visual research, Awwwards showcase benchmarking, design intelligence candidate synthesis (UI/UX Pro Max), subject-grounded distinctiveness discipline (Anthropic Frontend Design), pre-lock high-fidelity visual prototypes, owner visual direction selection, deterministic conversion measurement architecture (Conversion & Analytics Intelligence V2.6), official GSAP motion implementation engineering (gsap-skills), deterministic Impeccable quality scans, and adversarial Gauntlet quality-bar evaluations, without visual improvisation, generic AI slop, or an unresearched sitemap.

---

## 1. What Is Website Director?

**Website Director** is a deterministic design governance skill and operating methodology. It bridges the gap between commercial strategy and frontend engineering.

### The Problem It Solves
AI coding agents are proficient at generating code, but when left without rigorous art direction, they default to generic, uncurated aesthetic tropes ("AI slop")—indiscriminate card grids, purple SaaS gradients, floating fake UI elements, and identical section layouts.

Website Director solves this by establishing a **strict separation of Design Authority from Implementation Execution**. It guides non-designers through adaptive creative briefing, extracts business truth, runs bounded external visual research before committing to a direction, builds an uncompromising design system with exact mathematical tokens, makes a deliberate motion-level decision, locks the specification across 5 mandatory gates, and provides a binding implementation contract that prevents coding agents from improvising visual language during the build.

### What V1.8 Adds (Creative Briefing Room & Grilling System)
V1.8 establishes the conversational **Creative Briefing Room** (Phase 1):
- **Adaptive Grilling:** 2–5 targeted questions per turn with epistemic confidence tracking.
- **The Four Anchor Questions:** Purpose, People, Feeling, and Action.
- **Creative Intent Contract (`creative-intent-contract.md`):** Classifies `CREATIVE_AMBITION` (`STANDARD`, `PREMIUM`, `SHOWCASE`, `EXPERIMENTAL`), visual intensity, and experimentation tolerance.
- **Read-Back & Confirmation Gate:** Requires explicit owner confirmation (`creative_intent.confirmed = true`) before research or strategy begins.

### What V1.9 Adds (Visual Prototype Gate & Awwwards Showcase Intelligence)
V1.9 solves the core problem: **The owner should never again have to select a major visual direction from prose alone.**
- **High-Fidelity Visual Prototypes (Phase 4.5):** Bounded, browser-rendered slices (`projects/[project]/prototypes/direction-XX/`) containing header, hero (`HERO_THESIS`), representative content section, signature element, CTA, and mobile (390px) evidence.
- **True Divergence Mandate:** SHOWCASE ambition requires 3 genuinely distinct creative points of view evaluated across 10 Divergence Vectors.
- **Visual Prototype Comparison Package (`templates/visual-prototype-review.md`):** Owner compares rendered desktop/mobile prototypes and selects visually before Design Direction Lock (Lock 1) is synthesized.
- **Awwwards Showcase Intelligence (Phase 3.75):** Formal external benchmarking from [Awwwards](https://www.awwwards.com/) across 10 dimensional reference bars (`AWWWARDS_HERO_BAR`, `AWWWARDS_TYPOGRAPHY_BAR`, `AWWWARDS_LAYOUT_BAR`, `AWWWARDS_INTERACTION_BAR`, `AWWWARDS_MOTION_BAR`, `AWWWARDS_MOBILE_BAR`), with anti-copying rules, trend contamination filters, and the 11-question **Portfolio Art Director Critic**.

### What V2.6 Adds (Conversion & Analytics Intelligence)
V2.6 closes the gap between commercial intent and measurable outcome. Website Director could already say *"this CTA should convert."* It can now also define and verify: **this conversion is measurable, this is the event representing it, this is how it is triggered, this is the KPI it contributes to, this is how attribution is preserved, and this is how implementation is verified.**

- **Phase 6.5 (`CONVERSION-ANALYTICS-PROTOCOL.md`):** Runs after Lock 3 and before the design system, so measurement *informs* design instead of being retrofitted onto a frozen build.
- **KPI Architecture:** Enforces `BUSINESS OUTCOME KPI ≠ FUNNEL KPI ≠ DIAGNOSTIC METRIC ≠ VANITY METRIC`. A site with 100,000 visits and zero conversions is not a success.
- **Event Definition Contract:** Every event carries 13 mandatory fields — business purpose, trigger, parameters, deduplication rule, consent dependency, implementation method, and verification method. Events without a business or diagnostic purpose are prohibited.
- **CTA Traceability:** Every primary and meaningful secondary CTA in locked copy is traced to an event, KPI relation, destination, and verification method.
- **Attribution & UTM Governance:** Bounded naming conventions, preservation rules, landing-page attribution, cross-domain boundaries — and a hard prohibition on PII in campaign parameters.
- **Affiliate Measurement Integrity:** Enforces `AFFILIATE CLICK ≠ AFFILIATE CONVERSION ≠ AFFILIATE COMMISSION`. An outbound click is never inferred to be a sale.
- **Anti-Fabrication Governance:** `BASELINE = UNKNOWN` where no baseline exists. No invented industry benchmarks. Evidence taxonomy (`OBSERVED` → `EVIDENCE_SUPPORTED` → `HYPOTHESIS` → `EXPERIMENT_CANDIDATE` → `PROVEN`) prevents a hypothesis being presented as fact.
- **Three Distinct Verification States:** `measurement.complete` (a plan exists) ≠ `measurement.implementation_verified` (instrumentation proven in the build) ≠ `measurement.production_verified` (observed in production). Planning is never reported as production success.
- **Blocked & Exception Modes:** An unselected analytics provider is honestly `blocked`, not skipped and not faked. Bounded exceptions exist for non-commercial surfaces only.
- **Supersedes V2.4:** `CRO-ANALYTICS-EXPERIMENTATION-PROTOCOL.md` is absorbed and retained as a pointer. `site-profile.json` → `measurement{}` replaces `cro{}` as the single authoritative state; `cro{}` is grandfathered read-only.

### What V2.7 Adds (Security, Privacy & Compliance Intelligence)
V2.7 closes the **production risk governance** gap. Website Director could already design, measure, and refine. It can now also determine: **what security, privacy, consent, data-handling, and disclosure obligations does this website actually create — and what must the build do about them?**

- **Phase 6.75 (`SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md`):** Runs after the measurement plan and before the design system, so safeguards *inform* the build instead of being retrofitted onto a shipped site.
- **Proportional Risk Classification:** 13 site classifications and a bounded `LOW | MODERATE | HIGH | SPECIALIST_REVIEW_REQUIRED` risk model derived from actual functionality. A static brochure site never inherits ecommerce or authentication obligations; an authenticated SaaS application is never treated as a brochure site.
- **Deterministic Data Inventory:** Every data class records ten fields — source, purpose, collection point, destination, third party, retention, consent dependency, sensitivity, and whether production genuinely requires it.
- **Data Minimization As Architecture:** Every field needs a documented purpose. Fields inherited from a form template, collected speculatively, or duplicated without purpose are removed — not footnoted.
- **Secret Governance:** No secrets in client-side source, in Git, or in examples. `.env.example` holds names and placeholders only. Website Director identifies which secrets the architecture requires and **never asks for a real credential**.
- **Safeguard Specification:** Form security, authentication/session security, payment boundary (`PAYMENT PROVIDER INTEGRATION ≠ STORING PAYMENT CARD DATA`), evidence-driven security headers, HTTPS/transport, and dependency/supply-chain governance — each specified only where the functionality actually exists.
- **Third-Party Accountability:** Every production third-party runtime script must have a reason, a scope, and a consent dependency. **Unexplained third-party scripts are prohibited.**
- **Consent Without Guessing:** `NOT_REQUIRED | REQUIRED | CONDITIONALLY_REQUIRED | UNASSESSED | OWNER_OR_COUNSEL_REVIEW_REQUIRED`. Applicable law is never inferred from an IP address. Where it cannot be reliably determined, escalation is the correct answer — not a confident guess.
- **Truthful Disclosure:** `AFFILIATE DISCLOSURE ≠ PRIVACY POLICY ≠ TERMS ≠ ADVERTISING CONSENT`. Disclosure belongs near the recommendation, not buried exclusively in a remote footer page.
- **Hard Legal Boundary:** Website Director **never** outputs `GDPR COMPLIANT`, `CCPA COMPLIANT`, `HIPAA COMPLIANT`, `PCI COMPLIANT`, `COPPA COMPLIANT`, or `LEGAL COMPLIANCE VERIFIED`. `security_privacy.compliance_certified` is permanently `false`. Health, biometric, government-identifier, and children's data escalate automatically.
- **Privacy Beats Conversion:** Where they conflict, consent beats silent tracking, disclosure beats a cleaner layout, and data minimization beats speculative marketing fields. Approved locks still beat both and require an owner change request.
- **Three Distinct Verification States:** `security_privacy.complete` (requirements specified) ≠ `implementation_verified` (controls proven in the build) ≠ `production_verified` (proven on the deployed surface). Planning is never reported as production safety.
- **Reconciles, Does Not Duplicate:** `CONVERSION-ANALYTICS-PROTOCOL.md` §15 now delegates consent and privacy determination to this single authority. `measurement{}` stays canonical for measurement. No new Gauntlet critic and no second security state machine were created.

### What V2.8 Adds (Browser & Regression QA)
V2.8 closes the **verification** gap. Website Director could already design, measure, secure, and refine — but "the agent checked the browser" was still an assertion. V2.8 makes it evidence.

- **Phase 10.5 (`BROWSER-REGRESSION-QA-PROTOCOL.md`):** Runs after the Phase 10 build and before the Phase 11 audit. `REQUIREMENT → MACHINE-EXECUTED BROWSER TEST → EVIDENCE ARTIFACT → PASS / FAIL / FLAKY / BLOCKED / NOT_APPLICABLE → REGRESSION BASELINE`.
- **Replaceable engine, canonical policy:** the `browser-qa/` harness ships a `playwright` real-browser engine and a dependency-free deterministic `simulation` engine behind one `BrowserQAEngine.observe()` contract. Puppeteer/CDP or Selenium can be added without touching the policy.
- **Canonical viewport matrix:** small mobile / standard mobile / tablet / laptop / desktop, with a required smoke matrix and an extended regression matrix.
- **Requirement-traced assertions:** every check traces to `LOCKED_SPEC`, `PRODUCTION_CHECKLIST`, `MEASUREMENT_PLAN`, `SECURITY_PRIVACY_REVIEW`, `MOTION_SPEC`, `PAGE_EXPERIENCE_SPEC`, or `BROWSER_QA_PLAN`. Real overflow is detected, not masked by `overflow-x: hidden`. A server-rejected form renders no success state and fires no success conversion event.
- **Frozen Project Integrity Guard:** every run snapshots `projects/`; `FROZEN_FIXTURE_MUTATION = FAIL`, and a later restore never launders it into a PASS.
- **Bounded flake policy:** fail-then-pass on retry is `FLAKY`, never `PASS`. An unavailable engine is `BLOCKED` with a reason, never a PASS.
- **Local vs. production:** `browser_qa.complete` ≠ `implementation_verified` (real browser, local build) ≠ `production_verified` (real production URL). Localhost never sets `production_verified`.
- **Visual regression with governance:** explicit baselines, no silent overwrite, narrow masks, deterministic fixtures for dynamic content; a diff is evidence of change, not automatically a defect.
- **Feeds the Gauntlet, doesn't merge with it:** the qualitative Website Gauntlet no longer spends cycles on a build with broken navigation, JS exceptions, missing assets, or failed forms. No new Gauntlet critic and no second state machine.
- **Repairs two pre-existing validation defects:** `tests/test_v2_5_client_handoff.py` no longer mutates frozen pilots (all mutable work runs in a temp copy under the integrity guard); `examples/test_runner.py` asserts framework invariants and the canonical `measurement{}` architecture instead of a frozen `schema_version == "2.4.0"` / `cro{}` literal, while still verifying the grandfathered V2.4 pilot as-is.

### What V2.9 Adds (Accessibility Intelligence & WCAG 2.2 AA Verification)
V2.9 gives Website Director **one canonical accessibility authority**. Accessibility rules already lived in the production checklist, the QA rubric, the Gauntlet Accessibility Critic, Impeccable's contrast/target detectors, the browser-QA keyboard smoke, the security consent rules, and the design system — but scattered. V2.9 reconciles them.

- **Phase 6.9 (`ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md`):** Runs after Security/Privacy and **before the design system**, so accessibility informs tokens before Lock 4. Derives an applicable-component inventory and requirements for semantics, name/role/value, keyboard, focus (incl. WCAG 2.2 *focus not obscured*), contrast, colour independence, reflow at 320 CSS px, text spacing, target size, dragging, motion, images, media, forms, live regions, dialogs, tables, authentication, and consent-UI accessibility — only for what the project actually contains.
- **`[ACCESSIBILITY_READY]`** is a readiness gate, **not** a sixth owner lock. `accessibility.complete` is the single readiness flag; it means the *specification* is implementable, never that the build passed testing.
- **Four permanently distinct states:** `requirements_defined` ≠ `automated_verified` (engine, real browser) ≠ `manual_verified` (keyboard/zoom) ≠ `production_verified` (owner production evidence). `screen_reader_verified` is separate again.
- **No false conformance claims.** Website Director never writes `ADA COMPLIANT`, `FULLY ACCESSIBLE`, `ACCESSIBILITY GUARANTEED`, or `WCAG COMPLIANT`. Permitted: `WCAG 2.2 AA TARGET TESTS PASSED`, `MANUAL REVIEW COMPLETED`, `KNOWN ACCESSIBILITY GAPS = NONE OBSERVED`, `BLOCKED_SCREEN_READER_ENVIRONMENT`.
- **Extends V2.8 Browser QA — no separate runner.** An accessibility assertion group joins the `browser-qa/` catalogue (source `ACCESSIBILITY_REVIEW`), with a replaceable automated engine (axe-core recommended; `BLOCKED_ACCESSIBILITY_ENGINE_UNAVAILABLE` when absent, never a PASS). Same runner, same evidence system, same `FrozenIntegrityGuard`.
- **`44×44` vs `24×24` kept distinct.** Website Director's ergonomic `44×44 px` preference is preserved where approved; the WCAG 2.2 AA `24×24 px` floor is a separate, weaker criterion — both are recorded.
- **Consumes, doesn't duplicate:** Impeccable owns the contrast math; `MOTION-DIRECTION-PROTOCOL.md` owns the motion policy; Security/Privacy owns consent-requirement determination. The Gauntlet **Accessibility Critic is preserved and enriched** to focus on experiential quality — **no new critic, no second post-build state machine**.
- **Screen-reader honesty.** A bounded manual smoke protocol (NVDA/VoiceOver/Orca); where no screen reader can run, `BLOCKED_SCREEN_READER_ENVIRONMENT` — never a claimed pass. An engine-clean run with a failing manual keyboard review is not a full PASS.

### What V2.10 Adds (Launch & Post-Launch Operations Intelligence)
V2.10 closes the **launch boundary** gap. Website Director could get a project to a strong production candidate — but it conflated *release candidate* with *deployed*, *deployed* with *production verified*, and *production verified* with *stable*. V2.10 makes each a separately recorded state.

- **Phase 12.25 (`LAUNCH-OPERATIONS-PROTOCOL.md`):** Runs after Phase 12 pre-flight and before Phase 12.5 handoff. `LOCAL BUILD → RELEASE CANDIDATE → [RELEASE_READY] → DEPLOYMENT AUTHORIZATION → PRODUCTION DEPLOYMENT → PRODUCTION VERIFICATION → POST-LAUNCH STABILITY → OPERATIONS/HANDOFF`.
- **`[RELEASE_READY]`** is a readiness gate, **not** a sixth owner lock. `launch_ops.complete` is the single readiness flag; it means the launch *plan* is complete and the candidate may request deployment authorization — never that the site is deployed, production verified, or stable.
- **`RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED`.** Deployment is an external side effect. Website Director never deploys, pushes, merges, or touches DNS. Deployment authorization is an explicit per-release owner act — never inferred from passing QA, a completed build, an approved design, "looks good", a prior project, or a previous release.
- **Verify a known release identity on the production surface.** `deployed_sha` must match `release_sha` or `DEPLOYED_IDENTITY = UNVERIFIED` / `BLOCKED`. A localhost or staging evidence manifest never sets any `production_*_verified` flag.
- **16-state status model + a deterministic transition graph** (`launch-ops/validator.py`). Impossible jumps (`NOT_EVALUATED → STABILIZED`, `RELEASE_READY → PRODUCTION_VERIFIED`) are rejected.
- **Rollback readiness, concrete rollback triggers, a site-class-sized post-launch observation window, and a `SEV0`–`SEV3` incident model.** A `SEV0`/`SEV1` incident meeting a defined trigger sets `ROLLBACK_REQUIRED`.
- **Consumes, doesn't duplicate.** Production Browser QA is the V2.8 harness in `environment = "production"` mode — no second runner. Production verification writes the canonical `accessibility.production_verified` / `security_privacy.production_verified` / `measurement.production_verified` fields those specs already defined. V2.5 `CLIENT-CMS-HANDOFF-PROTOCOL.md` remains the long-term operations authority; Launch Operations hands its record into Phase 12.5 intake (§13).

---

---

## 2. The Core Architecture

```
BUSINESS INPUT
      │
      ▼
PHASE 1: CREATIVE BRIEFING ROOM (Stages A-G)
      ├─► [GATE BRIEF: CREATIVE_INTENT_CONFIRMED] (readiness gate)
      │
      ▼
PHASE 2: POSITIONING & ANTI-BRAND BOUNDARIES
      │
      ▼
PHASE 2.5: SEO INTELLIGENCE (SEO Intelligence Director)
      ├─► [GATE SEO: SEO_COMPLETE] (readiness gate, not an approval lock)
      │
      ▼
PHASE 3: VISUAL RESEARCH (Visual Research Director)
      ├─► [GATE 0: RESEARCH_COMPLETE] (readiness gate, not an approval lock)
      │
      ▼
PHASE 3.5: DESIGN INTELLIGENCE CANDIDATE SYNTHESIS (UI/UX Pro Max)
      ├─► [GATE INTEL: DESIGN_INTELLIGENCE_COMPLETE] (readiness gate)
      │
      ▼
PHASE 3.75: AWWWARDS SHOWCASE BENCHMARKING (SHOWCASE Tier Intelligence)
      │
      ▼
PHASE 4: TWO-PASS DESIGN SYNTHESIS & DIRECTION FORMULATION (Pass 1 & Pass 2)
      │
      ▼
PHASE 4.5: HIGH-FIDELITY VISUAL PROTOTYPES & OWNER COMPARISON GATE
      ├─► [GATE PROTO: VISUAL_PROTOTYPES_OWNER_REVIEW_READY]
      ├─► [OWNER VISUALLY SELECTS DIRECTION]
      ├─► [LOCK 1: DESIGN_DIRECTION_LOCKED]
      │
      ▼
PHASE 5: INFORMATION ARCHITECTURE & SECTION MORPHOLOGY
      ├─► [LOCK 2: INFORMATION_ARCHITECTURE_LOCKED]
      │
      ▼
PHASE 6: CONTENT STRATEGY, UX WRITING & COPYWRITING
      ├─► [LOCK 3: CONTENT_STRUCTURE_LOCKED]
      │
      ▼
PHASE 6.5: CONVERSION & ANALYTICS INTELLIGENCE
      ├─► [GATE MEASUREMENT: CONVERSION_MEASUREMENT_COMPLETE] (readiness gate)
      │
      ▼
PHASE 7: DESIGN SYSTEM TOKEN ARCHITECTURE
      ├─► [LOCK 4: DESIGN_SYSTEM_LOCKED]
      │
      ▼
PHASE 8: MOTION DIRECTION & GSAP IMPLEMENTATION SPEC
      ├─► [LOCK 5: MOTION_DIRECTION_LOCKED]
      │
      ▼
PHASE 9: IMPLEMENTATION CONTRACT ISSUANCE
      │
      ▼
PHASE 10: BUILD EXECUTION (Strict Token/Spec Consumption & Scoped Lifecycle)
      │
      ▼
PHASE 11: 100-POINT DESIGN QA & IMPECCABLE PRE-SCAN
      │
      ▼
PHASE 11.5: WEBSITE GAUNTLET ADVERSARIAL REFINEMENT LOOP (Builder != Critic)
      ├─► [GATE GAUNTLET: GAUNTLET_PASS]
      │
      ▼
PHASE 12: PRODUCTION PRE-FLIGHT CHECKLIST
      │
      ▼
PRODUCTION-READY CODEBASE (Zero AI Slop, Subject-Grounded, Distinctive & Verified)
```


---

## 3. Reference Mode vs. Original Mode

Website Director adapts to user context through two primary pathways:

- **`ORIGINAL_MODE`:** Leverages Website Director's catalog of 14 curated design archetypes (e.g., *Editorial, Luxury, Cinematic, Industrial, Architectural, Modernist, Technical, Heritage, Organic, Boutique, Premium Corporate, Playful, Experimental, High Fashion*) and applies the **60/30/10 Blending Formula** to synthesize a custom aesthetic tailored to the business domain. As of V1.1, `research-synthesis.md`'s archetype recommendation is a weighted input to this choice, not a replacement for it.
- **`REFERENCE_MODE`:** Deconstructs 1 to 3 external URL/screenshot references across 12 fundamental design vectors (composition, visual hierarchy, typography pairing, spacing cadence, density, imagery art direction, color architecture, geometry, navigation, section morphology, motion physics, and brand posture) to extract underlying principles without cloning proprietary assets.

---

## 4. The Five Mandatory Locks (V1.1)

Implementation is strictly blocked until all five gates in `locks{}` evaluate to `true` in `site-profile.json`. `RESEARCH_COMPLETE` (§5 below) is a precondition for Lock 1 but is not itself a member of `locks{}` — see `SKILL.md` §5.2 for why the two are categorically different.

1. **`design_direction_locked`:** Art direction narrative, archetype blend, and emotional posture signed off.
2. **`information_architecture_locked`:** Sitemaps, conversion funnels, and non-repetitive section morphology signed off.
3. **`content_structure_locked`:** Copywriting, headline hierarchy, proof assets, and CTA labels signed off (zero `Lorem Ipsum`).
4. **`design_system_locked`:** Mathematical type scale, 60/30/10 color tokens, 8-point spatial system, surface geometry, and component states signed off.
5. **`motion_direction_locked`:** Motion level (0–3), hero/scroll/hover behavior, reduced-motion and mobile fallbacks signed off — even a static (Level 0) site locks this to prove the absence of motion was deliberate.

---

## 5. Readiness & Refinement Gates

- **`RESEARCH_COMPLETE` (Gate 0):** Certifies that industry landscape, Landbook, cross-industry, and deep-recon research have completed before Lock 1 engages.
- **`SEO_COMPLETE` (Gate SEO):** Certifies that business context, keyword discovery, competitive SERP analysis, and keyword mapping have completed before Lock 2 and Lock 3 engage.
- **`CONVERSION_MEASUREMENT_COMPLETE` (Gate Measurement):** Certifies that the business objective, KPI hierarchy, observable funnel, event contracts, CTA traceability, attribution strategy, and verification plan are defined before Lock 4 engages. A readiness gate, **not** a sixth owner lock. It never means production analytics were observed.
- **`SECURITY_PRIVACY_READY` (Gate Security):** Certifies that risk classification, data inventory, data minimization, applicable technical safeguards, consent/privacy dependencies, required disclosures, escalations, and implementation requirements are specified before Lock 4 engages. A readiness gate, **not** a sixth owner lock. It never means legal compliance is certified, implementation is verified, or the site is vulnerability-free.
- **`ACCESSIBILITY_READY` (Gate Accessibility):** Certifies that the accessibility specification — applicable-component inventory, semantic / name-role-value / keyboard / focus / contrast / colour-independence / reflow / text-spacing / target-size / motion / media / form / dialog requirements, and an automated + manual + screen-reader test plan — is complete against the WCAG 2.2 AA technical target before Lock 4 engages. A readiness gate, **not** a sixth owner lock. `accessibility.complete` never means the implementation passed accessibility testing, and Website Director never claims legal accessibility compliance.
- **`BROWSER_QA_PASS` (Gate Browser):** Certifies that machine-executed browser tests ran against the built artifact and passed — responsive invariants, navigation, forms, console/network cleanliness, measurement events, browser-observable security/privacy, reduced motion, keyboard smoke, and visual regression — with frozen-project integrity intact. A verification gate, **not** a sixth owner lock. `browser_qa.complete` never means production (DNS, CDN, real TLS, production headers) was verified.
- **`GAUNTLET_PASS` (Gate Gauntlet):** Certifies that the build has passed fresh-context adversarial evaluation against approved Reference Bars before Phase 12 pre-flight sign-off.
- **`RELEASE_READY` (Gate Launch):** Certifies that the Phase 12.25 launch plan is complete — immutable release identity, deployment target, environment readiness, domain/DNS/HTTPS/redirect plan, monitoring determination, rollback plan and triggers — and the candidate may request deployment authorization. A readiness gate, **not** a sixth owner lock. `launch_ops.complete` never means the site is deployed (`RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED`), production verified, or stable. Deployment is an external owner act; Website Director never deploys.

---

## 6. Repository Structure

```
website-director/
├── SKILL.md                          # Primary operating manual for AI agents (12-phase + Phase 2.5 + Phase 11.5 flow)
├── README.md                         # Project overview and architectural manual
├── DESIGN-CONSTITUTION.md            # Anti-AI-slop rules & the 7 Pillars of Justification
├── DISCOVERY-PROTOCOL.md             # 4-stage progressive discovery framework
├── SEO-INTELLIGENCE-PROTOCOL.md      # SEO Intelligence Director role, pipeline, SEO_COMPLETE gate (V1.2)
├── WEBSITE-GAUNTLET-PROTOCOL.md      # Website Gauntlet subsystem, critics, Reference Bars, lock protection (V1.3)
├── CONVERSION-ANALYTICS-PROTOCOL.md  # Conversion measurement, KPI architecture, event contracts, attribution, affiliate integrity (V2.6)
├── SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md # Risk classification, data inventory/minimization, secrets, form/auth/payment safeguards, headers, consent, disclosure, SECURITY_PRIVACY_READY gate (V2.7)
├── BROWSER-REGRESSION-QA-PROTOCOL.md # Phase 10.5 machine-executed browser verification, viewport matrix, assertion catalogue, flake policy, frozen-project guard, BROWSER_QA_PASS gate (V2.8)
├── ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md # Phase 6.9 WCAG 2.2 AA spec + Phase 10.5 verification, replaceable a11y engine, screen-reader smoke, no false conformance claims, ACCESSIBILITY_READY gate (V2.9)
├── LAUNCH-OPERATIONS-PROTOCOL.md     # Phase 12.25 release identity, owner deployment authorization boundary, production verification against a known release, rollback readiness/triggers, post-launch observation, incident model, RELEASE_READY gate (V2.10)
├── DESIGN-ARCHETYPES.md              # 14 complete archetypes & 60/30/10 blending rules
├── REFERENCE-PROTOCOL.md             # 12-vector deconstruction & anti-cloning protocol
├── DESIGN-SYSTEM-PROTOCOL.md         # 14-subsystem design token architecture
├── VISUAL-RESEARCH-PROTOCOL.md       # Visual Research Director role, pipeline, RESEARCH_COMPLETE gate
├── RESEARCH-SOURCES.md               # Industry / Landbook / cross-industry / JCodesMore channels + provenance
├── REFERENCE-RECON-PROTOCOL.md       # Bounded RESEARCH_ONLY_MODE forensic reconnaissance
├── MOTION-DIRECTION-PROTOCOL.md      # Motion Levels 0-3, justification rule, MOTION_DIRECTION_LOCKED
├── CINEMATIC-INTEGRATION-PROTOCOL.md # Robonuggets cinematic-sites as a bounded optional specialist
├── IMPLEMENTATION-CONTRACT.md        # Governance contract binding coding phase + Builder SEO + Gauntlet repair rules
├── QA-RUBRIC.md                      # 100-point evaluation rubric + V1.1 supplemental dimensions + Gauntlet handoff
├── PRODUCTION-CHECKLIST.md           # Pre-flight verification matrix + SEO fidelity + Gauntlet verification (V1.3)
├── templates/
│   ├── project-brief.md              # Stage 1: Business extraction template
│   ├── positioning.md                # Stage 2: Brand posture & anti-brand template
│   ├── seo-business-context.md       # SEO required business/audience/market context (V1.2)
│   ├── keyword-research.md           # Keyword universe, intent classification, opportunity scoring (V1.2)
│   ├── seo-competitive-landscape.md  # SEO competitor classification & page analysis (V1.2)
│   ├── keyword-map.md                # Page-level keyword mapping, feeds IA & content locks (V1.2)
│   ├── seo-content-briefs.md         # Per-page SEO content briefs for PRIMARY pages (V1.2)
│   ├── measurement-plan.md           # 19-section conversion measurement plan (V2.6)
│   ├── analytics-event-manifest.json # Machine-readable event contract manifest (V2.6)
│   ├── security-privacy-review.md    # 25-section security, privacy & compliance review (V2.7)
│   ├── security-privacy-register.json # Machine-readable data / third-party / storage register (V2.7)
│   ├── browser-qa-plan.md            # Phase 10.5 browser & regression QA plan (V2.8)
│   ├── browser-qa-manifest.json      # Machine-readable browser QA manifest consumed by browser-qa/runner.py (V2.8)
│   ├── accessibility-review.md       # Phase 6.9 29-section WCAG 2.2 AA accessibility review (V2.9)
│   ├── accessibility-test-manifest.json # Machine-readable accessibility test manifest (V2.9)
│   ├── launch-plan.md                # Phase 12.25 26-section launch & post-launch operations plan (V2.10)
│   ├── launch-evidence-manifest.json # Machine-readable launch evidence manifest, tied to a release identity (V2.10)
│   ├── research-brief.md             # Visual research scoping template
│   ├── competitor-landscape.md       # Industry landscape (visual/design) research template
│   ├── inspiration-board.md          # Landbook + cross-industry discovery template
│   ├── reference-deconstruction.md   # Deep reconnaissance template (per target)
│   ├── research-synthesis.md         # Research-to-decision synthesis template
│   ├── reference-analysis.md         # Reference deconstruction matrix template
│   ├── design-direction.md           # Visual direction & gate 1 locking template
│   ├── information-architecture.md   # Commercial UX & section morphology template
│   ├── design-system.md              # 14-subsystem token specification template
│   ├── content-plan.md               # Copywriting & proof plan template
│   ├── motion-direction.md           # Motion level & gate 5 locking template
│   ├── cinematic-brief.md            # Binding brief for the cinematic specialist
│   ├── implementation-contract.md    # Active implementation governance instance
│   ├── design-review.md              # 100-point QA review & upgrade recommendations
│   ├── website-gauntlet-report.md    # Phase 11.5 Gauntlet evaluation and targeted repair report (V1.3)
│   ├── production-review.md          # Production pre-flight audit sign-off
│   └── site-profile.json             # Machine-readable state & lock schema (v2.10.0)
├── launch-ops/                       # Deterministic Phase 12.25 validators (V2.10)
│   └── validator.py                  # launch_ops{} state machine, release-readiness gate, deployment-authorization boundary, production-verification checks, rollback-trigger evaluator
├── browser-qa/                       # Reusable Phase 10.5 harness (V2.8; V2.9 accessibility assertions; V2.10 environment=production)
│   ├── runner.py                     # Manifest-driven orchestrator + evidence manifest emitter
│   ├── engine/                       # Replaceable BROWSER_QA_ENGINE: playwright (real) + simulation (deterministic)
│   ├── assertions/                   # Requirement-traced assertion catalogue
│   ├── guards/                       # frozen_integrity_guard.py — protected-path snapshot/verify
│   ├── config/                       # viewports.json · browser-policy.json · ignore-justifications.example.json
│   └── fixtures/                     # Synthetic scenario pages for the negative-control validation
├── tests/
│   ├── test_v2_5_client_handoff.py   # V2.5 CMS/handoff (repaired: temp-copy isolation + integrity guard)
│   ├── test_v2_5_1_signature_choreography.py
│   ├── test_v2_7_security_privacy.py
│   ├── test_v2_8_browser_regression_qa.py # V2.8 repo invariants + scenario A-L negative controls
│   ├── test_v2_9_accessibility.py     # V2.9 repo invariants + scenario A-R accessibility negative controls
│   └── test_v2_10_launch_operations.py # V2.10 repo invariants + state-machine + scenario A-R launch negative controls
└── examples/
    ├── README.md                     # End-to-end worked example (AetherDB)
    ├── test_runner.py                # V2.0-V2.7 protocol/template/pilot invariant harness (repaired under V2.8)
    ├── V1.1-VALIDATION-SIMULATIONS.md # Planning-only Dental / Architecture / Plumbing diversity test
    ├── GAUNTLET-INTEGRATION-VALIDATION.md # Gauntlet adversarial evaluation & targeted repair validation suite (V1.3)
    ├── BROWSER-REGRESSION-QA-INTEGRATION-VALIDATION.md # Phase 10.5 scenario A-L validation suite (V2.8)
    ├── ACCESSIBILITY-INTELLIGENCE-INTEGRATION-VALIDATION.md # Phase 6.9/10.5 scenario A-R validation suite (V2.9)
    └── LAUNCH-OPERATIONS-INTEGRATION-VALIDATION.md # Phase 12.25 state-machine + scenario A-R validation suite (V2.10)
```

---

## 7. How to Invoke Website Director

When pair programming or prompting an AI agent:

```text
Activate Website Director for [Company Name].
```

The agent will load [SKILL.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/SKILL.md), initialize [templates/site-profile.json](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/templates/site-profile.json), and begin guided extraction.

---

## Framework Self-Validation (V2.11)

<!-- FRAMEWORK_VERSION: 2.11.0 -->

The V2.11 framework self-validation layer is additive to the certified V2.10
Website Director system. The corrected lineage starts directly from the V2.10
certification commit and retains the complete historical `projects/` corpus.

Run the deterministic framework gate locally with:

```text
python -m framework_validation --run-suites
```

The validator checks the framework registries and schemas, current-version
references, historical compatibility, frozen-project integrity, test isolation,
negative controls, and the read-only GitHub Actions policy. Runtime reports are
written under `framework-validation/reports/runtime/`; certification reports are
explicit evidence artifacts and do not authorize deployment or publishing.

The framework contract deliberately remains outside the current site profile.
Exactly five owner locks remain authoritative:
`design_direction_locked`, `information_architecture_locked`,
`content_structure_locked`, `design_system_locked`, and
`motion_direction_locked`.
