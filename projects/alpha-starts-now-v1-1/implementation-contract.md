# IMPLEMENTATION CONTRACT SPECIFICATION: ALPHA STARTS NOW (V1.1)

> **Date Generated:** 2026-08-23  
> **Status:** READY FOR PRODUCTION BUILD (`IMPLEMENTATION_CONTRACT_VALIDATED: true`)  
> **Governance Authority:** Website Director V1.1  
> **Authoritative Location:** `projects/alpha-starts-now-v1-1/`  
> **Build Target Directory:** `projects/alpha-starts-now-v1-1/build/`  

---

## 1. Design Governance Lock Verification Matrix

All five gates in `site-profile.json` → `locks{}` are verified as **`LOCKED (true)`**:

| Gate | Status | Verified Artifact | Locked Timestamp |
| :--- | :---: | :--- | :--- |
| **`design_direction_locked`** | **`LOCKED`** | [design-direction.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-v1-1/design-direction.md) | 2026-08-23T17:32:55 |
| **`information_architecture_locked`** | **`LOCKED`** | [information-architecture.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-v1-1/information-architecture.md) | 2026-08-23T17:51:01 |
| **`content_structure_locked`** | **`LOCKED`** | [content-plan.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-v1-1/content-plan.md) | 2026-08-23T17:59:32 |
| **`design_system_locked`** | **`LOCKED`** | [design-system.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-v1-1/design-system.md) | 2026-08-23T18:03:51 |
| **`motion_direction_locked`** | **`LOCKED`** | [motion-direction.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-v1-1/motion-direction.md) & [cinematic-brief.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now-v1-1/cinematic-brief.md) | 2026-08-23T18:06:12 |

*Precondition:* `research.complete = true` was verified before Gate 1 locked.

---

## 2. Technical Stack & Build Architecture Constraints

- **Core Architecture:** Multi-page semantic HTML5 + Vanilla CSS custom properties + clean, vanilla JavaScript for interaction.
- **Styling Pipeline:** Pure, modular CSS deriving 100% of values from locked CSS custom properties (`styles/tokens.css`, `styles/base.css`, `styles/layout.css`, `styles/components.css`).
- **Typography Sourcing:** Google Fonts CDN (`Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400..600` and `Plus+Jakarta+Sans:wght@400;500;600;700`) with robust system fallbacks.
- **Page Footprint:**
  1. `index.html` (Flagship Homepage — 8 Alternating Cadence Sections)
  2. `start-here.html` (Interactive 5-Pathway Editorial Navigator)
  3. `guides.html` (The Editorial Knowledge Library & Pillar Filter Index)
  4. `recommended.html` (The Curated Resource Desk & FTC Transparency)
  5. `about.html` (The Manifesto, 5 Beliefs, and Independence Policy)
  6. `dispatch.html` (Dedicated Newsletter Landing Page)
  7. `privacy.html`, `terms.html`, `affiliate-disclosure.html` (Legal & Compliance)
- **Image & Media Pipeline:** Optimized SVG icons, progressive WebP images with reserved aspect-ratio boxes, and high-performance silent cinematic media.

---

## 3. Strict Code Generation Guardrails

1. **Zero Aesthetic Improvisation:** Build strictly to the locked specifications in `design-system.md`. Never invent arbitrary hex codes, margin numbers, or card styles.
2. **Exact Variable Mapping:** Every style must resolve to a defined `--token-name`.
3. **No Inline Style Hacks:** Strictly zero inline style overrides with magic pixel values.
4. **Responsive Layout Transitions:** Adhere strictly to the breakpoint container thresholds (`360px`, `640px`, `768px`, `1024px`, `1280px`).
5. **Zero Motion Improvisation:** Adhere strictly to `motion-direction.md` (Level 3 passive hero, Level 1–2 UI, Level 0 static reading, zero scroll hijacking, zero autoplay audio).
6. **Commercial Endpoint Configuration:** The ASN Dispatch subscription engine must bind cleanly to `window.ASN_SITE.config.leadEndpoint` with robust mock fallback and visual validation states.
