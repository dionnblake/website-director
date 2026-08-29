# WEBSITE DIRECTOR

> **Version:** 2.6.0  
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
- **`GAUNTLET_PASS` (Gate Gauntlet):** Certifies that the build has passed fresh-context adversarial evaluation against approved Reference Bars before Phase 12 pre-flight sign-off.

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
│   └── site-profile.json             # Machine-readable state & lock schema (v2.7.0)
└── examples/
    ├── README.md                     # End-to-end worked example (AetherDB)
    ├── V1.1-VALIDATION-SIMULATIONS.md # Planning-only Dental / Architecture / Plumbing diversity test
    └── GAUNTLET-INTEGRATION-VALIDATION.md # Gauntlet adversarial evaluation & targeted repair validation suite (V1.3)
```

---

## 7. How to Invoke Website Director

When pair programming or prompting an AI agent:

```text
Activate Website Director for [Company Name].
```

The agent will load [SKILL.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/SKILL.md), initialize [templates/site-profile.json](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/templates/site-profile.json), and begin guided extraction.
