# DESIGN INTELLIGENCE ENGINE: UI/UX PRO MAX PROTOCOL

> **Version:** 1.0.0 (Website Director V1.4.0 Subsystem)  
> **Status:** Mandatory Design Intelligence & Candidate Generation Standard  
> **Governance:** Website Director Orchestration Rail (`SKILL.md` §2, Phase 3.5 & Phase 4)  
> **Attribution:** Adapted from **UI/UX Pro Max** by **Next Level Builder** ([github.com/nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)), licensed under the [MIT License](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/main/LICENSE).  
> **Source Provenance:** Repo: `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`, Commit SHA: `e4f45473691e4b389519ee4bc359a3d6df666c26`, Version: `2.13.0`.

---

## 1. Architectural Mission & Core Role

The **Design Intelligence Engine** enriches Website Director with structured domain knowledge, style candidates, industry conventions, font pairings, color theory mappings, UX guidelines, and tech stack implementation best practices.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           CORE ARCHITECTURE                              │
│                                                                          │
│  UI/UX Pro Max is a DESIGN INTELLIGENCE ENGINE.                          │
│  It provides EVIDENCE and CANDIDATE RECOMMENDATIONS.                     │
│  It is NOT Website Director's design authority and DOES NOT create a     │
│  competing design system, state machine, or duplicate motion framework.  │
└──────────────────────────────────────────────────────────────────────────┘
```

### The Integrated Architecture:
```
                      ┌─────────────────────────────────┐
                      │        WEBSITE DIRECTOR         │
                      │     (Orchestrating Authority)   │
                      └────────────────┬────────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
┌──────────────────┐          ┌──────────────────┐          ┌──────────────────┐
│ PHASE 1-3:       │          │ PHASE 3.5:       │          │ PHASE 4-8:       │
│ DISCOVERY, SEO   │─────────►│ DESIGN           │─────────►│ SYNTHESIS &      │
│ & RESEARCH       │          │ INTELLIGENCE     │          │ 5-GATE LOCKS     │
│ (Empirical Data) │          │ (UI/UX Pro Max)  │          │ (Authoritative)  │
└──────────────────┘          └──────────────────┘          └────────┬─────────┘
                                                                     │
                   ┌─────────────────────────────────────────────────┴──┐
                   ▼                                                    ▼
       ┌───────────────────────────────┐               ┌───────────────────────────────┐
       │ PHASE 10-11: BUILD & QA       │               │ PHASE 11.5: WEBSITE GAUNTLET  │
       │ - Impeccable Quality Engine   │──────────────►│ - Adversarial 8 Critics       │
       │ - Deterministic Code Scans    │               │ - Dimensional Reference Bars  │
       │ - UI Hardening Checklist      │               │ - Bounded Refinement Loop     │
       └───────────────────────────────┘               └───────────────────────────────┘
```

---

## 2. Epistemic Separation & Decision Precedence

To preserve clarity, Website Director strictly separates the roles of its integrated subsystems:

```
┌───────────────────────────┬────────────────────────────────────────────────────────┐
│ Subsystem / Domain        │ Core Epistemic Question Answered                       │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 1. Project Research       │ "What exists in the real market, what do competitors   │
│                           │ do, and what search demand/audience evidence exists?"  │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 2. Design Intelligence    │ "Given this context, what established styles, palettes,│
│    (UI/UX Pro Max)        │ font pairings, and UX rules exist as viable options?"  │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 3. Website Director       │ "Which specific design direction is synthesized,       │
│    (Authoritative Locks)  │ approved by the owner, and locked for production?"     │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 4. Quality Engine         │ "Is the built frontend crafted cleanly, accessible,    │
│    (Impeccable)           │ hardened against edge cases, and free of AI slop?"     │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 5. Website Gauntlet       │ "Does the rendered artifact beat the approved          │
│    (existing WD subsystem)│ dimensional Reference Bars under adversarial critique?"│
└───────────────────────────┴────────────────────────────────────────────────────────┘
```

### Precedence Hierarchy (Conflict Resolution):
When recommendations and project requirements conflict, decisions resolve in this exact order:
```
1. OWNER REQUIREMENT
      ▼
2. APPROVED BRAND / EXISTING LOCKS
      ▼
3. ACCESSIBILITY / SAFETY / FUNCTIONAL REQUIREMENT
      ▼
4. PROJECT RESEARCH (Visual & SEO Evidence)
      ▼
5. APPROVED REFERENCE BAR EVIDENCE
      ▼
6. WEBSITE DIRECTOR DESIGN CONSTITUTION
      ▼
7. UI/UX PRO MAX RECOMMENDATION
```
*A database recommendation never overrides stronger project-specific evidence or locked decisions.*

---

## 3. Semantic State Separation: Recommended vs Selected vs Locked

Every design attribute progresses through three explicit states:

1. **`RECOMMENDED` (Design Intelligence):** Candidates generated by UI/UX Pro Max based on product/industry queries (e.g. `dark-mode-oled`, `Calistoga + Inter`).
2. **`SELECTED` (Design Synthesis):** The candidate chosen by Website Director during Phase 4 design direction synthesis after weighing brand, research, and owner requirements.
3. **`LOCKED` (Owner Gate):** The authoritative decision approved by the Owner under Gate 1 (`DESIGN_DIRECTION_LOCKED`) or Gate 4 (`DESIGN_SYSTEM_LOCKED`).

### Existing Locks Invariant:
If Design Intelligence is queried on a project with existing approved locks, it **cannot silently alter** any locked decision. Any material contradiction triggers a `LOCKED_CHANGE_REQUIRED` Change Request.

---

## 4. Single Design System Invariant (No `MASTER.md`)

UI/UX Pro Max includes capability to generate `design-system/MASTER.md`. In Website Director:
- **`MASTER.md` is STRICTLY PROHIBITED.**
- Website Director maintains **one authoritative Design System** ([`templates/design-system.md`](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/templates/design-system.md)) governed by Lock 4 (`DESIGN_SYSTEM_LOCKED`).
- Useful palette values, font pairings, and component tokens from UI/UX Pro Max are mapped directly into Website Director's canonical token model.

---

## 5. Multi-Domain Design Intelligence

### 5.1 Product & Industry Interpretation
Queries `products.csv` and `ui-reasoning.csv` (192 product types) to establish industry priors:
- Target audience expectations and psychological posture.
- Layout strategies (e.g., asymmetrical editorial split vs dense analytical grid).
- Trust builders (e.g., regulatory badges, audited performance, client case studies).
- Common domain pitfalls (e.g., cognitive overload in fintech, sterile feel in luxury hospitality).

### 5.2 Style Intelligence & Combination Governance
Queries `styles.csv` (79 styles, 50 active) to generate candidate aesthetic directions.
- **Single Style:** High-cohesion visual direction matching brand posture.
- **Combined Styles (Governed):** When combining two styles, Website Director requires:
  1. `PRIMARY_STYLE` (e.g., `Editorial Minimalism` - governs 80% of layouts and typography).
  2. `SUPPORTING_STYLE` (e.g., `Modern Dark Cinema` - restricted to hero canvas and card transitions).
  3. `COMBINATION_RATIONALE` (explicit reason why single style is insufficient).
  4. `CONFLICT_CHECK` (verifies zero contradiction between typography and radius tokens).
  *Arbitrary "style soup" (mixing 4+ styles without boundary) is strictly banned.*

### 5.3 Color & Palette Intelligence
Queries `colors.csv` (192 palettes).
- If brand colors are fixed by Owner: UI/UX Pro Max assists with semantic role assignment, neutral background/card elevation mapping, and contrast-safe border tokens.
- If brand palette is open: Generates candidate primary, secondary, accent, and surface pairs tested against WCAG AA contrast rules.

### 5.4 Typography Pairing Intelligence
Queries `typography.csv` (74 font pairings) and `google-fonts.csv`.
- Recommends pairing names, heading fonts, body fonts, and Google Fonts import URLs.
- Evaluated against Website Director's Impeccable Craft Floor (measure 65–75ch, tabular figures on numbers, tracking floor -0.04em).

### 5.5 UX Guidelines & Classification
Queries `ux-guidelines.csv` (119 guidelines). Each guideline is mapped into Website Director's architecture:
- `ALREADY_COVERED`: Handled by Impeccable or Design Constitution.
- `UIUX_STRONGER` / `NEW_CAPABILITY`: Adopted into Phase 11 QA or Implementation Contract.
- `CONTEXT_DEPENDENT`: Applied only when specific feature is present (e.g. multi-step forms).

### 5.6 Tech Stack Implementation Guidance
Queries `stacks/*.csv` (16 frameworks: Next.js, React, Astro, Svelte, Vue, Tailwind, Shadcn, etc.).
- Does **not** choose or switch the project's tech stack.
- Answers: *"Given the approved project stack, what implementation patterns, component structures, and performance optimizations should the implementation contract require?"*

### 5.7 Charts & Data Visualization (Contextual Only)
Queries `charts.csv` (25 chart types). Active *only* when the website genuinely includes data reporting or visual metrics. Banned from being forced onto standard marketing pages.

### 5.8 Motion Presets Status: DEFERRED
- `UIUX_GSAP_MOTION_PRESETS = DEFERRED`.
- UI/UX Pro Max motion presets and GSAP snippets are **not integrated** into Website Director at this time, preserving Website Director's dedicated Motion Direction subsystem (`MOTION-DIRECTION-PROTOCOL.md`, Lock 5).

---

## 6. Project State & Artifact Integration

### 6.1 State Machine Schema (`site-profile.json`)
Design intelligence tracking is embedded directly into the authoritative `site-profile.json`:
```json
"design_intelligence": {
  "status": "NOT_STARTED | IN_PROGRESS | COMPLETE",
  "source_sha": "e4f45473691e4b389519ee4bc359a3d6df666c26",
  "product_type_matched": "string",
  "candidate_styles": ["string"],
  "selected_style": "string",
  "candidate_palette_matched": "string",
  "candidate_typography_matched": "string",
  "stack_guidance_applied": "string",
  "completed_at": "ISO-8601 Timestamp"
}
```

### 6.2 Readiness Gate: `[DESIGN_INTELLIGENCE_COMPLETE]`
Before Lock 1 (`DESIGN_DIRECTION_LOCKED`) can be engaged:
1. Product/industry context queried via `intelligence/ui-ux-pro-max/engine/query.py`.
2. Candidate styles, palettes, and typography recorded in `templates/design-intelligence.md`.
3. Recommendations synthesized with project research.
4. Selected direction documented with explicit rationale for any rejected recommendations.
5. `site-profile.json` → `design_intelligence.status` set to `"COMPLETE"`.

---

## 7. Command Execution & Local Tooling

Website Director provides a fast, zero-dependency Python CLI adapter:

```bash
# Full product synthesis
python intelligence/ui-ux-pro-max/engine/query.py --product "fintech wealth management"

# Domain-specific search
python intelligence/ui-ux-pro-max/engine/query.py --domain style --query "editorial minimal"
python intelligence/ui-ux-pro-max/engine/query.py --domain typography --query "modern serif"
python intelligence/ui-ux-pro-max/engine/query.py --domain color --query "luxury architecture"

# Stack implementation guidance
python intelligence/ui-ux-pro-max/engine/query.py --stack nextjs --query "image optimization"
```
