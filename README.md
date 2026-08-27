# WEBSITE DIRECTOR

> **Version:** 1.6.0  
> **Status:** Production-Grade Skill & Specification System  
> **Purpose:** Turn vague business requirements into production-grade website design and implementation specifications, informed by real search demand, competitive intelligence, external visual research, design intelligence candidate synthesis (UI/UX Pro Max), subject-grounded distinctiveness discipline (Anthropic Frontend Design), official GSAP motion implementation engineering (gsap-skills), deterministic Impeccable quality scans, and adversarial Gauntlet quality-bar evaluations, without visual improvisation, generic AI slop, or an unresearched sitemap.

---

## 1. What Is Website Director?

**Website Director** is a deterministic design governance skill and operating methodology. It bridges the gap between commercial strategy and frontend engineering.

### The Problem It Solves
AI coding agents are proficient at generating code, but when left without rigorous art direction, they default to generic, uncurated aesthetic tropes ("AI slop")—indiscriminate card grids, purple SaaS gradients, floating fake UI elements, and identical section layouts.

Website Director solves this by establishing a **strict separation of Design Authority from Implementation Execution**. It guides non-designers through a 4-stage progressive discovery process, extracts business truth, runs bounded external visual research before committing to a direction, builds an uncompromising design system with exact mathematical tokens, makes a deliberate motion-level decision, locks the specification across 5 mandatory gates, and provides a binding implementation contract that prevents coding agents from improvising visual language during the build.

### What V1.1 Adds Over V1
V1 proved AI design improvisation could be controlled through discovery, archetypes, and locks alone. The Alpha Starts Now pilot exposed a gap: Website Director had never *looked* at the current visual landscape before choosing a direction. V1.1 adds a bounded Visual Research Director phase (industry landscape, Landbook discovery, cross-industry references, and JCodesMore-style reconnaissance in a research-only mode — see `VISUAL-RESEARCH-PROTOCOL.md`), and a deliberate Motion Direction phase (four motion levels, with the Robonuggets `cinematic-sites` skill invocable as an optional bounded specialist — see `MOTION-DIRECTION-PROTOCOL.md` and `CINEMATIC-INTEGRATION-PROTOCOL.md`). Both are additive: V1's 4-lock core, 14 archetypes, and 100-point rubric are unchanged and remain fully backward compatible — see `SKILL.md` §6.

### What V1.2 Adds Over V1.1
V1.1 closed the visual-research gap; it still let Website Director draw a sitemap and write content strategy purely from commercial psychology, with no evidence of what the target audience actually searches for or who already wins that search market. V1.2 adds a bounded SEO Intelligence Director phase — business/audience context, keyword discovery and search-intent classification, first-party Google Search Console evidence where available, a competitive landscape pass that explicitly separates business competitors from SEO competitors, opportunity-scored keyword clustering, and a page-level keyword map — that must complete (or be explicitly declared not applicable) before `INFORMATION_ARCHITECTURE_LOCKED` and `CONTENT_STRUCTURE_LOCKED` may engage. See `SEO-INTELLIGENCE-PROTOCOL.md`. It is additive and narrowly scoped: it does not gate `DESIGN_DIRECTION_LOCKED` (visual and search evidence are independent streams), does not become a sixth lock, and never authorizes keyword stuffing over the Design Constitution's human-clarity and brand-voice requirements — see `SKILL.md` §5.3.

### What V1.3 Adds Over V1.2 (The Website Gauntlet Subsystem)
V1.2 established search-demand and visual intelligence; however, candidate builds could still suffer from builder self-evaluation bias. V1.3 integrates the **Website Gauntlet Subsystem** (Phase 11.5) based on the Gauntlet Loop methodology (credited to Matt Shumer, packaged under CC BY 4.0 by Jay E. / RoboNuggets). The Gauntlet introduces:
- **Builder != Critic Separation:** Builders never grade their own work; fresh-context evaluators inspect rendered artifacts.
- **Dimensional Reference Bars (`REFERENCE_BAR`):** Concrete benchmarks (Named, Fetchable, Comparable) across 8 explicit dimensions (Typography, Motion, Hero, Brand, Conversion, IA, Editorial, Mobile).
- **8 Specialized Critics:** Craft, Brand, Conversion, Trust, Motion, AI-Slop, Accessibility, and Reference critics.
- **Simulated Audience Panel:** 5-perspective visitor evaluation heuristic (`SIMULATED_AUDIENCE_EVALUATION`).
- **Targeted Repair & Lock Protection:** Builder executes the smallest safe fix for the single largest remaining gap (`BIGGEST_REMAINING_GAP`); changes requiring token/spec mutations halt and generate a `LOCKED_CHANGE_REQUIRED` Change Request for Owner Review.
- **Resource Governance:** Hard iteration caps (`max_iterations`, default 3) and diminishing-return circuit breakers return `GAUNTLET_CAP_REACHED` rather than faking a pass. See `WEBSITE-GAUNTLET-PROTOCOL.md`.

### What V1.3.1 Adds (Impeccable Quality Engine Integration)
V1.3.1 integrates the frontend quality intelligence, deterministic anti-pattern detection, craft floor rules, and UI hardening knowledge from **Impeccable** (by Paul Bakaus and contributors, Apache-2.0). It establishes:
- **Deterministic vs Heuristic vs Critique Taxonomy:** Explicitly distinguishes `DETERMINISTIC_FINDING`, `HEURISTIC`, `LLM_CRITIQUE`, and `VISUAL_COMPARISON` to eliminate epistemic conflation.
- **18 Machine-Verifiable Detector Rules:** Static and DOM scanning for contrast math, layout transitions, bounce curves, gray-on-color contrast failures, and AI tropes.
- **Enriched Gauntlet Critics:** Enriches AI-Slop, Craft, Accessibility, and Motion critics without adding duplicate critics or competing state machines.
- **Craft Floor & Surface Polish:** Enforces browser surface theming (`::selection`, custom scrollbars, carets), tabular numerals on data, and reading measures. See `IMPECCABLE-ENGINE-PROTOCOL.md`.

### What V1.4 Adds (UI/UX Pro Max Design Intelligence Engine)
V1.4 integrates domain-specific design intelligence from **UI/UX Pro Max** (by Next Level Builder, MIT License) as a candidate generation engine in **Phase 3.5**:
- **Design Intelligence vs. Design Authority:** UI/UX Pro Max provides candidate styles (79 styles, 50 active), color palettes (192 product types), font pairings (74 pairings), and 119 UX guidelines. It informs Website Director; Website Director governs UI/UX Pro Max.
- **Zero Second Design System (No `MASTER.md`):** All token recommendations map directly to Website Director's canonical `design-system.md` (Lock 4). Competing `MASTER.md` files are strictly banned.
- **Precedence & Existing Locks Win:** Approved brand requirements and existing locks override database candidates unconditionally.
- **Deferred Motion Presets:** `UIUX_GSAP_MOTION_PRESETS = DEFERRED` to keep Website Director's dedicated motion direction architecture clean and unpolluted. See `DESIGN-INTELLIGENCE-PROTOCOL.md`.

### What V1.5 Adds (Official GreenSock GSAP Implementation Engine)
V1.5 integrates official GreenSock engineering skills from **GSAP Skills** (by Jack Doyle / GreenSock, MIT License) as the motion implementation authority:
- **Strategy Authority vs. Implementation Authority:** Website Director Phase 8 (`motion-direction.md`, Lock 5) owns motion strategy and level decisions. Official GSAP skills (`gsap-core`, `timeline`, `scrolltrigger`, `react`, `frameworks`, `performance`, `plugins`, `utils`) own implementation engineering.
- **GSAP is NOT Automatic:** Static or CSS-only projects evaluate to `GSAP_REQUIRED = FALSE` with zero added runtime overhead.
- **React `useGSAP()` & Zero-Leak Guarantees:** Enforces `@gsap/react` scoped refs and automatic lifecycle cleanup (`ctx.revert()`).
- **Compositor Performance & Accessibility:** Prohibits layout-property animation and mandates `(prefers-reduced-motion: reduce)` fallbacks via `gsap.matchMedia()`. See `GSAP-IMPLEMENTATION-PROTOCOL.md`.

### What V1.6 Adds (Anthropic Frontend Design Distinctiveness Discipline)
V1.6 integrates distinctiveness and intentional-design principles from **Anthropic Frontend Design** (Apache-2.0, unversioned) into Phase 4 and Phase 6:
- **Two-Pass Design Synthesis:** Pass 1 derives visual language directly from the subject's world (materials, instruments, vernacular); Pass 2 runs an anti-interchangeability challenge (*"Could this fit 5 competitors with only logo/copy swapped?"*).
- **Hero as Thesis (`HERO_THESIS`):** Replaces generic headline+buttons+stats template formulas with the single most characteristic encounter.
- **Structure Must Encode Information (`STRUCTURE_MUST_ENCODE_INFORMATION`):** Eliminates decorative `01 / 02 / 03` numbering on unordered cards.
- **Signature Element & Boldness Budget:** Identifies one memorable signature while keeping surrounding layout disciplined.
- **Interface Copy Discipline:** Enforces user-perspective vocabulary and action-descriptive buttons without compromising factual integrity.

---

## 2. The Core Architecture

```
BUSINESS INPUT
      │
      ▼
PHASE 1: PROGRESSIVE DISCOVERY (Stages 1-4)
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
PHASE 4: TWO-PASS DESIGN SYNTHESIS & DISTINCTIVENESS PRE-CHECK (Pass 1 & Pass 2)
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
│   └── site-profile.json             # Machine-readable state & lock schema (v1.3.0)
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
