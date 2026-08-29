# IMPECCABLE QUALITY ENGINE: DETERMINISTIC DETECTION & CRAFT INTELLIGENCE PROTOCOL

> **Version:** 1.0.0 (Website Director V1.3.1 Subsystem)  
> **Status:** Mandatory Quality & Craft Intelligence Standard  
> **Governance:** Website Director Orchestration Rail (`SKILL.md` §2, Phase 11 & Phase 11.5)  
> **Attribution:** Adapted from **Impeccable** by **Paul Bakaus** and contributors ([github.com/pbakaus/impeccable](https://github.com/pbakaus/impeccable)), licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).  
> **Source Provenance:** Repo: `https://github.com/pbakaus/impeccable`, Commit SHA: `63b04e2530f5c7b41ea83c133daab24f34912456`, Version: `skill v4.1.2 (CLI v3.6.1)`.

---

## 1. Architectural Mission & Core Role

The **Impeccable Quality Engine** provides Website Director with deterministic frontend anti-pattern detection, rigorous craft rules, UI hardening knowledge, and systematic refinement playbooks.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           CORE ARCHITECTURE                              │
│                                                                          │
│  Impeccable is a QUALITY ENGINE and INTELLIGENCE SOURCE.                 │
│  It is NOT a second Website Director, NOT a second state machine,        │
│  and does NOT create competing critics or bypass existing locks.         │
└──────────────────────────────────────────────────────────────────────────┘
```

### Architectural Mapping:
```
                      ┌─────────────────────────────────┐
                      │        WEBSITE DIRECTOR         │
                      │     (Orchestrating Authority)   │
                      └────────────────┬────────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
┌──────────────────┐          ┌──────────────────┐          ┌──────────────────┐
│ DESIGN           │          │ DESIGN SYSTEM    │          │ IMPECCABLE       │
│ CONSTITUTION     │          │ TOKENS           │          │ QUALITY ENGINE   │
│ (Anti-AI-Slop)   │          │ (Mathematical)   │          │ (Detection &     │
└──────────────────┘          └──────────────────┘          │  Craft Intel)    │
                                                            └────────┬─────────┘
                                                                     │
                   ┌─────────────────────────────────────────────────┴──┐
                   ▼                                                    ▼
       ┌───────────────────────────────┐               ┌───────────────────────────────┐
       │ PHASE 11: DESIGN QA AUDIT     │               │ PHASE 11.5: WEBSITE GAUNTLET  │
       │ - Deterministic Scan Engine   │               │ - AI-Slop Critic (Enhanced)   │
       │ - 100-Point Evaluation Rubric │               │ - Craft Critic (Enhanced)     │
       │ - Hardening & Edge-Case Scan  │               │ - A11y & Motion (Enhanced)    │
       └───────────────────────────────┘               └───────────────────────────────┘
```

---

## 2. Finding Taxonomy & Method Distinction

To preserve analytical honesty, findings produced by Website Director must explicitly identify their origin and discovery method. A deterministic code check must never be represented as subjective model opinion, and a subjective aesthetic critique must never be represented as mathematical proof.

```
┌───────────────────────────┬────────────────────────────────────────────────────────┐
│ Finding Method            │ Description & Epistemological Basis                    │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 1. `DETERMINISTIC`        │ Verifiable code/DOM check (contrast ratio math,        │
│                           │ layout transitions, unmapped tokens, raw hex colors,   │
│                           │ banned cubic-beziers, missing touch-target size).      │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 2. `HEURISTIC`            │ Structural pattern recognition (3-card loops, repeated │
│                           │ kickers, radial background blobs, icon-tile stacks).   │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 3. `LLM_CRITIQUE`         │ Qualitative judgment of brand expression, hierarchy,   │
│                           │ emotional resonance, and conversion psychology.        │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 4. `VISUAL_COMPARISON`    │ Side-by-side rendering comparison against an approved  │
│                           │ Reference Bar on an assigned dimension.                │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 5. `BROWSER_EXECUTED`     │ Machine-run assertion against a live page in a real    │
│    (V2.8)                 │ browser: actual horizontal overflow at a viewport,     │
│                           │ runtime console/network errors, an event that fired,   │
│                           │ a form's real success/failure state, reduced-motion    │
│                           │ behaviour as rendered. Owned by Phase 10.5             │
│                           │ (`BROWSER-REGRESSION-QA-PROTOCOL.md`).                 │
└───────────────────────────┴────────────────────────────────────────────────────────┘
```

### 2.1 Static vs. Runtime Rule Ownership (V2.8)

Website Director keeps **one owner for each rule**. Impeccable owns the *static* half; Browser QA owns the *runtime-observable* half of the same concern. Neither re-implements the other.

| Concern | Static owner (Impeccable, `DETERMINISTIC`/`HEURISTIC`) | Runtime owner (Browser QA, `BROWSER_EXECUTED`) |
| :--- | :--- | :--- |
| Layout-triggering transition | `transition: all` / `width` / `top` in a stylesheet | — (compositor perf is static-detectable) |
| Horizontal overflow | — | `documentElement.scrollWidth > clientWidth` at a live viewport |
| Bounce easing | banned `cubic-bezier` string in CSS | — |
| Reduced motion | `@media (prefers-reduced-motion)` block present | content still meaningful *as rendered* under `reduce` |
| Console errors | — | uncaught errors at runtime |
| AI-slop structural patterns | markup/CSS heuristics | — |
| Touch target size | declared box `< 44px` in CSS | computed box `< 44px` at a mobile viewport |

Browser QA consumes Impeccable's static findings via the shared `FINDING` schema below; it adds no duplicate static detector.

### Standardized Finding Schema:
Every finding recorded in QA reviews and Gauntlet reports uses this structure:
```text
FINDING_ID:    [UNIQUE-ID, e.g., DET-001, HEUR-002, CRIT-003]
SOURCE:        [IMPECCABLE_DETECTOR | GAUNTLET_CRITIC | QA_RUBRIC]
METHOD:        [DETERMINISTIC | HEURISTIC | LLM_CRITIQUE | VISUAL_COMPARISON | BROWSER_EXECUTED]
RULE:          [e.g., skill-color-verify-contrast / skill-ban-layout-transition]
LOCATION:      [File path, selector, line numbers]
SEVERITY:      [CRITICAL | MAJOR | MINOR]
EVIDENCE:      [Exact computed CSS, code snippet, or measurement]
REMEDIATION:   [Specific code/token fix to resolve the defect]
LOCK_IMPACT:   [NONE (Code fix) | LOCKED_CHANGE_REQUIRED (Requires Owner Review)]
```

---

## 3. The 18 Deterministic & Heuristic Detector Rules

Impeccable's rule engine is integrated into Website Director across two operational categories: **Universal Technical Violations** (always errors) and **Context-Dependent Heuristics** (errors unless authorized by an approved archetype/lock).

### 3.1 Universal Technical Violations (`DETERMINISTIC`)
These rules represent mathematical, accessibility, or performance defects that are never permissible:

1. **`low-contrast`:** Text failing WCAG AA contrast math ($< 4.5:1$ body, $< 3:1$ large bold text).
2. **`gray-on-color`:** Neutral gray text (`#6b7280`, `rgba(0,0,0,0.5)`) on colored surfaces; secondary text must be tinted from the background hue or foreground.
3. **`layout-transition`:** Animating layout-triggering properties (`transition: all`, `transition: width`, `transition: height`, `transition: top`, `transition: margin`). Transitions must use compositor-only properties (`transform`, `opacity`).
4. **`bounce-easing`:** Exaggerated toy-like bounce curves (`cubic-bezier(0.68, -0.55, 0.265, 1.55)`). Smooth exponential ease-out or crisp mechanical timing is required.
5. **`dark-glow`:** 0-offset saturated neon drop-shadows creating artificial radio-active halos in dark mode.
6. **`touch-target-undersized`:** Interactive controls with bounding box $< 44\text{px} \times 44\text{px}$ on mobile viewports.

### 3.2 Anti-AI-Slop Heuristic Checks (`HEURISTIC`)
These checks detect default machine-generated tropes unless explicitly justified by the chosen archetype:

7. **`ai-color-palette`:** Uncurated purple/indigo/cyan gradient pairings (#6366f1, #8b5cf6, #06b6d4) defaulted by AI models.
8. **`hero-eyebrow-chip`:** Cliché small pill chip immediately above hero title (`"✨ Announcing v2.0 ->"`).
9. **`icon-tile-stack`:** Monotonous repeating 3-card feature loop with colored circular icon badges.
10. **`radial-halo`:** Giant blurred radial gradient blob in background with no material or spatial justification.
11. **`side-tab` / `border-accent-on-rounded`:** 2–4px colored accent border riding one edge of a rounded card without alert/status semantic context.
12. **`pulsing-dot`:** Arbitrary radar/ping animated dot on non-critical status items.
13. **`marquee`:** Unrestrained infinite horizontal logo ticker with no interactive pause control or editorial purpose.
14. **`shape-assembled-illustration`:** Decorative floating CSS geometric shapes assembled to fill whitespace.
15. **`monotonous-spacing`:** Flat, uniform padding across all sections with zero macro/micro contrast.
16. **`gradient-text`:** Low-contrast `-webkit-background-clip: text` gradients causing unreadable character edges.
17. **`kicker-above-heading`:** Mechanical eyebrow text stacked uniformly above every heading on the page.
18. **`italic-serif-display`:** Gratuitous italicized single-word accent in headings without typographic justification.

> [!NOTE]
> **Contextual Override Rule:**  
> If a heuristic rule (such as an italic serif accent or section eyebrow) is explicitly specified in the locked `design-direction.md` (e.g. for an `Editorial` or `Heritage` archetype), the finding is classified as `HEURISTIC_AUTHORIZED_BY_LOCK` and will not block deployment.

---

## 4. Enhanced Gauntlet Critic Intelligence

Impeccable intelligence directly enriches Website Director's existing Gauntlet Critics (`WEBSITE-GAUNTLET-PROTOCOL.md` §4):

### 4.1 AI-Slop Critic (Enhanced)
- Incorporates Impeccable's full anti-pattern suite: detects identical card loops, uncurated SaaS gradients, floating decorator chips, and fake proof badges.
- Flags machine-generated predictability and enforces asymmetric layout variety.

### 4.2 Craft Critic (Enhanced)
- **Typography Floor:** Enforces measure 65–75ch for body text, tracking floor -0.04em for headings, mathematical type scale steps, and `font-variant-numeric: tabular-nums` on numerical data and pricing tables.
- **Spacing Rhythm:** Enforces tight semantic groups, generous section boundaries, and greater whitespace *above* headings than below them.
- **Browser Surface Theming:** Requires intentional styling of browser defaults: `::selection` highlight color, custom scrollbar tracks, high-contrast focus rings, and input carets matching the design system.

### 4.3 Accessibility Critic (Enhanced)
- Rigorous computed contrast verification across both light and dark themes.
- Enforces tinting secondary text from the background hue rather than muddy gray (`gray-on-color`).
- Verifies touch target ergonomics ($\ge 44\text{px}$) and keyboard navigation focus states.

### 4.4 Motion Critic (Enhanced)
- Strictly audits CSS transitions: flags any animation of `width`, `height`, `margin`, `top`, or `left`.
- Eliminates mechanical section fade-ups on scroll in favor of intentional, hierarchy-driven choreography.
- Audits `prefers-reduced-motion` compliance to ensure layout remains functional and expressive without animation.

---

## 5. UI Hardening & Edge-Case Resilience

Impeccable's `harden.md` principles ensure that websites are resilient against real-world production data variations:

1. **Extreme Text Lengths:**
   - Long strings: Multi-line clamping (`-webkit-line-clamp`) or graceful text wrapping; zero broken layouts or unconstrained horizontal overflows.
   - Short/Empty values: Robust fallbacks and empty-state placeholders.
2. **Internationalization & Translation Expansion:**
   - Headings and button containers accommodate text expansion up to 30% without clipping or collision.
3. **Interactive & System States:**
   - Every interactive control must provide distinct states for: `default`, `hover`, `active`, `focus-visible`, `disabled`, `loading`, and `error`.
4. **Touch & Pointer Density:**
   - Clean separation between fine pointer hover interactions and coarse touch taps.

---

## 6. Governed Creative Playbooks (`bolder`, `delight`, `overdrive`)

Impeccable contains creative expansion techniques (`bolder.md`, `delight.md`, `overdrive.md`). In Website Director, these playbooks are strictly **opt-in** and subject to lock constraints:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      CREATIVE PLAYBOOK GOVERNANCE                        │
│                                                                          │
│  "More impressive" does NOT equal "better".                              │
│  Creative escalation playbooks can ONLY be engaged if authorized by     │
│  the locked Design Direction (Lock 1) and Motion Direction (Lock 5).     │
└──────────────────────────────────────────────────────────────────────────┘
```

- **`BOLDER` Playbook:** Increases typographic scale contrast, amplifies color accent saturation, and sharpens visual tension — valid only when the brand posture demands high-impact authority.
- **`DELIGHT` Playbook:** Introduces purposeful micro-interactions (magnetic buttons, tactile hover states) — valid only when justified against the Six Motion Justifications (`MOTION-DIRECTION-PROTOCOL.md` §3).
- **`OVERDRIVE` Playbook:** Experimental canvas, 3D WebGL, or scroll-coupled cinematic timelines — restricted to `MOTION_LEVEL_3` projects and bound by `cinematic-brief.md`.

---

## 7. Context Model Integration

Impeccable's context artifacts map seamlessly into Website Director's single source of truth without creating redundant files:

| Impeccable Context | Website Director Canonical Artifact | Authority |
| :--- | :--- | :--- |
| `PRODUCT.md` | `project-brief.md`, `positioning.md`, `site-profile.json` | Discovery & Business Context |
| `DESIGN.md` | `design-direction.md`, `design-system.md`, `DESIGN-CONSTITUTION.md` | Visual & Token Architecture |
| Surface Briefs | `information-architecture.md`, `content-plan.md` | Page & Content Strategy |
| Hardening Specs | `PRODUCTION-CHECKLIST.md`, `QA-RUBRIC.md` | Pre-Flight & QA Matrix |

---

## 8. Live Browser Inspection & Tooling Policy

Impeccable supports live browser overlay and CDP inspection tools. For Website Director:
- **Headless & Static Inspection:** Fully integrated via deterministic AST/regex scans and screenshot artifact review.
- **Ephemeral Browser Automation (V2.8):** Phase 10.5 Browser & Regression QA (`BROWSER-REGRESSION-QA-PROTOCOL.md`) launches a real browser via a replaceable `BROWSER_QA_ENGINE`, runs the plan, and tears down every context, child process, server, and profile in `stop()`. This is a per-run tool, not a daemon.
- **Persistent Live Browser Daemons:** **`REJECTED_FOR_NOW`**. Website Director does not launch background browser servers or persistent daemons, preserving runtime portability and resource governance across all agent environments.
