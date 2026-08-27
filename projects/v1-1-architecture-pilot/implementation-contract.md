# IMPLEMENTATION CONTRACT SPECIFICATION: VALENTIN & HESSE Architects

> **Date Generated:** 2026-08-23  
> **Status:** READY FOR CODING  
> **Governance Authority:** Website Director V1.1 Specification

---

## 1. Design Lock Verification Matrix

Implementation is officially authorized because all five design & motion locks in `site-profile.json` evaluate to `LOCKED (true)`:

| Gate | Status | Verified Artifact | Locked Timestamp |
| :--- | :---: | :--- | :--- |
| **`design_direction_locked`** | **LOCKED (true)** | `projects/v1-1-architecture-pilot/design-direction.md` | 2026-08-23T08:44:47 |
| **`information_architecture_locked`** | **LOCKED (true)** | `projects/v1-1-architecture-pilot/information-architecture.md` | 2026-08-23T08:44:57 |
| **`content_structure_locked`** | **LOCKED (true)** | `projects/v1-1-architecture-pilot/content-plan.md` | 2026-08-23T08:45:10 |
| **`design_system_locked`** | **LOCKED (true)** | `projects/v1-1-architecture-pilot/design-system.md` | 2026-08-23T08:45:23 |
| **`motion_direction_locked`** | **LOCKED (true)** | `projects/v1-1-architecture-pilot/motion-direction.md` | 2026-08-23T08:45:32 |

*Precondition Verified: `research.complete` is `true` (Gate 0 engaged).*

---

## 2. Technical Stack Constraints
- **Core Markup & Architecture:** Semantic HTML5 + Vanilla JavaScript (Modern ES6+).
- **Styling Architecture:** Pure Vanilla CSS with CSS Custom Properties strictly matching the 14 token systems in `design-system.md`.
- **Typography Sourcing:** Google Fonts (`Cormorant Garamond` + `Plus Jakarta Sans`).
- **Icons:** Minimalist bespoke SVG inline icons with unified `1.5px` stroke.
- **Imagery & Blueprints:** Scalable high-fidelity SVG/Canvas vector architectural plans and warm mineral daylight photography.

---

## 3. Code Generation Guardrails for Coding Agent
1. **Zero Aesthetic Improvisation:** Build strictly to locked tokens. No improvised colors, spacing, or borders.
2. **Exact Variable Mapping:** Every color, font, spacing, and radius must use `var(--...)` custom properties.
3. **No Inline Styling Hacks:** No `style="..."` attributes with arbitrary hex or pixel values.
4. **Responsive Reflow:** Layout must reflow flawlessly across all target breakpoints (1440px, 1280px, 1024px, 768px, 390px, 360px).
5. **Zero Motion Improvisation:** Motion Level 2 only—smooth spatial reveals, interactive material switcher, modal case-study drawer, and strict reduced-motion fallback.
6. **Anti-Homogenization Check:** Under no circumstances inject Alpha Starts Now's dark obsidian, burnt orange, monospaced plate labels, or crosshair styling.
