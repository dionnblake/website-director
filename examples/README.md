# WEBSITE DIRECTOR: WORKFLOW & WORKED EXAMPLE

This directory provides reference documentation and a complete end-to-end worked demonstration showing how a commercial project transitions from vague requirements into locked, production-grade specifications.

> **V1.1 Note:** This worked example (AetherDB) predates the V1.1 Visual Research and Motion Direction phases and does not include `RESEARCH_COMPLETE` or `MOTION_DIRECTION_LOCKED` — it remains a valid illustration of the shared 10-step core. For the V1.1 research/motion planning flow applied to three contrasting businesses, see [V1.1-VALIDATION-SIMULATIONS.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/examples/V1.1-VALIDATION-SIMULATIONS.md).

---

## The End-to-End Workflow Pipeline

```
1. BUSINESS INPUT (User answers Progressive Discovery in plain English)
      │
      ▼
2. DISCOVERY SYNTHESIS (Templates: project-brief.md, positioning.md)
      │
      ▼
3. DIRECTION & ARCHETYPE (Templates: reference-analysis.md OR design-direction.md)
      │
      ├─► [LOCK GATE 1: DESIGN_DIRECTION_LOCKED]
      │
      ▼
4. INFORMATION ARCHITECTURE (Template: information-architecture.md)
      │
      ├─► [LOCK GATE 2: INFORMATION_ARCHITECTURE_LOCKED]
      │
      ▼
5. CONTENT & COPYWRITING (Template: content-plan.md)
      │
      ├─► [LOCK GATE 3: CONTENT_STRUCTURE_LOCKED]
      │
      ▼
6. DESIGN SYSTEM TOKENS (Template: design-system.md)
      │
      ├─► [LOCK GATE 4: DESIGN_SYSTEM_LOCKED]
      │
      ▼
7. IMPLEMENTATION CONTRACT (Template: implementation-contract.md)
      │
      ▼
8. CODING BUILD (Coding Agent executes pixel-perfect translation)
      │
      ▼
9. DESIGN QA & REFINEMENT (Template: design-review.md - 100-pt Rubric)
      │
      ▼
10. PRODUCTION PRE-FLIGHT (Template: production-review.md - Pre-flight Checklist)
```

---

## Complete Worked Example: "AetherDB" (Distributed Edge Database)

### 1. User Input (Progressive Discovery)
- **Stage 1 (Business):** *"We build AetherDB, a distributed serverless SQL database with sub-5ms global replication for high-concurrency fintech and AI workloads. Primary CTA is to start a free developer cluster or book an enterprise architecture audit."*
- **Stage 2 (Brand):** *"We want to look surgical, infallible, and high-performance. Avoid cheesy cartoon SaaS illustrations and purple gradients. We want a dark, technical, high-contrast look like a high-end financial Bloomberg terminal meets modern Swiss graphic design."*
- **Stage 3 (Evidence):** *"SOC2 Type II certified, 99.999% SLA, powers $4.2B in daily transactions for Apex Capital and Nexus Labs, sub-5ms P99 latency globally."*
- **Stage 4 (Visual Direction):** Chosen blend: **60% Technical + 30% Modernist + 10% Cinematic**.

---

### 2. Resulting `site-profile.json` State
```json
{
  "project_name": "AetherDB",
  "business_type": "Distributed SQL Database",
  "audience": {
    "primary_decision_maker": "VP Infrastructure / Lead Data Architect",
    "market_segment": "High-Growth Fintech & Enterprise AI"
  },
  "primary_conversion": {
    "goal": "Deploy Free Cluster",
    "cta_label": "Create Free Cluster in 60s →",
    "target_metric": "Developer Activation Rate"
  },
  "brand_attributes": ["Surgical", "Infallible", "High-Contrast", "Engineered", "Restrained"],
  "design_archetypes": {
    "primary": "Technical",
    "primary_weight": 0.6,
    "secondary": "Modernist",
    "secondary_weight": 0.3,
    "accent": "Cinematic",
    "accent_weight": 0.1
  },
  "density": "high",
  "layout_style": "asymmetric_12_column_grid",
  "geometry": "sharp_modernist",
  "corner_style": "4px",
  "typography_direction": {
    "display_family": "Syne",
    "body_family": "Inter",
    "mono_family": "JetBrains Mono"
  },
  "ai_slop_tolerance": 0.0,
  "locks": {
    "design_direction_locked": true,
    "information_architecture_locked": true,
    "design_system_locked": true,
    "content_structure_locked": true
  }
}
```

---

### 3. Design Tokens Generated (`templates/design-system.md`)
- **Backgrounds:** Pitch Obsidian (`#080A0E`), Surface Slate (`#10151E`), Elevated Border (`#1B2230`).
- **Typography:** `Syne` for monumental titles, `Inter` for interface copy, `JetBrains Mono` for latency benchmarks and SQL queries.
- **Accents:** High-Voltage Cyan (`#00F0FF`) for primary CTAs and live query execution indicators.
- **Geometry:** 4px radius, 1px subtle coordinate grid lines, dark elevated panels.

---

### 4. Implementation Governance
The coding agent writes code adhering strictly to `var(--bg-primary)`, `var(--accent-primary)`, and the 8-point spatial system. No inline styling or invented UI components are introduced.

---

### 5. Design QA Evaluation (`templates/design-review.md`)
- **Visual Hierarchy:** 15/15
- **Brand Differentiation:** 15/15 (Passed Swap Test; completely bespoke visual architecture)
- **Typography Execution:** 10/10 (Strict leading/tracking scale)
- **Composition & Spacing:** 10/10
- **Content Hierarchy:** 10/10
- **Conversion Clarity:** 9/10
- **Mobile Execution:** 10/10
- **Interaction Quality:** 5/5
- **Imagery & Renders:** 5/5
- **Accessibility:** 5/5 (4.8:1 minimum contrast verified)
- **AI-Slop Resistance:** 5/5 (0 unmotivated gradients or generic cards)
- **TOTAL SCORE:** **99 / 100 (PRODUCTION CANDIDATE)**

---

### 6. Production Pre-Flight Sign-Off
All 20+ checks in `PRODUCTION-CHECKLIST.md` are audited, and the site is authorized for deployment.
