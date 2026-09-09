# DESIGN SYSTEM SPECIFICATION: [PROJECT NAME]

> **Date Created:** YYYY-MM-DD  
> **Status:** DRAFT | LOCKED (`DESIGN_SYSTEM_LOCKED: true`)  
> **Rule:** All CSS variables, Tailwind tokens, and component classes must derive strictly from this document.

---

## 0. Approved Homepage Derivation

- **Homepage Source:** `APPROVED_HOMEPAGE` (`visual_prototypes.homepage_visual_approved = true`)
- **Homepage Approval Reference:** [Owner review ID / rendered evidence path]
- **Derivation Rule:** This document formalizes the approved homepage's typography, color, spacing, grid, geometry, imagery, component, responsive, accessibility, and motion language. It must not reinterpret or contradict that approved visual direction.
- **Downstream Rule:** Remaining pages and components inherit this system. A component library, framework, model, or implementation convenience cannot redefine it.

## 1. Brand Posture & Theme Fundamentals
- **Archetype Blend:** [e.g., 60% Modernist + 30% Technical + 10% Editorial]
- **Theme Paradigm:** [Dark Mode Native / Light Mode Native / Dual Theme Toggle]
- **Brand Attributes:** [e.g., Surgical, Infallible, Authoritative, High-Contrast]

---

## 2. Typography Tokens & Mathematical Scale

```css
:root {
  /* Font Families */
  --font-display: 'Syne', sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Typographic Scale */
  --text-display: clamp(2.75rem, 5vw, 4.5rem); /* 44px - 72px */
  --text-h1: clamp(2.25rem, 4vw, 3.25rem);      /* 36px - 52px */
  --text-h2: clamp(1.75rem, 3vw, 2.25rem);      /* 28px - 36px */
  --text-h3: clamp(1.25rem, 2vw, 1.5rem);       /* 20px - 24px */
  --text-lead: 1.25rem;                         /* 20px */
  --text-body: 1.0rem;                          /* 16px */
  --text-caption: 0.875rem;                     /* 14px */
  --text-mono: 0.8125rem;                       /* 13px */

  /* Line Heights */
  --leading-tight: 1.1;
  --leading-snug: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.65;

  /* Letter Spacing */
  --tracking-tight: -0.03em;
  --tracking-snug: -0.015em;
  --tracking-normal: 0em;
  --tracking-wide: 0.05em;
  --tracking-widest: 0.15em;
}
```

---

## 3. Color Tokens & Semantic Assignments

```css
:root {
  /* Surface & Canvas (60%) */
  --bg-primary: #0A0D12;
  --bg-secondary: #121820;
  --bg-surface: #182230;
  --bg-surface-hover: #1F2C3F;
  --bg-elevated: #24344B;

  /* Text & Content (30%) */
  --text-primary: #F9FAFB;
  --text-secondary: #94A3B8;
  --text-muted: #64748B;
  --text-inverse: #0A0D12;

  /* Structural Lines & Dividers */
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-medium: rgba(255, 255, 255, 0.16);
  --border-strong: rgba(255, 255, 255, 0.28);
  --border-focus: #38BDF8;

  /* Primary Brand Action & Accent (10%) */
  --accent-primary: #0284C7;
  --accent-primary-hover: #0369A1;
  --accent-primary-fg: #FFFFFF;

  /* Semantic Feedback */
  --status-success: #10B981;
  --status-warning: #F59E0B;
  --status-error: #EF4444;
  --status-info: #38BDF8;
}
```

---

## 4. Spacing Cadence & Layout Tokens

```css
:root {
  /* 8-Point Baseline Scale */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;
  --space-24: 96px;
  --space-32: 128px;

  /* Layout Containers */
  --container-narrow: 768px;
  --container-standard: 1200px;
  --container-wide: 1440px;
}
```

---

## 5. Grid, Breakpoints & Container Geometry

```css
:root {
  /* Breakpoint Bounds */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;

  /* Layout Containers */
  --container-narrow: 768px;
  --container-standard: 1200px;
  --container-wide: 1440px;
  --container-full: 100%;
}
```

---

## 6. Surface Geometry, Borders & Elevation

```css
:root {
  /* Border Radius Tier: [Sharp: 0-2px | Refined: 4-8px | Modern: 8-12px | Organic: 16-24px] */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Elevation Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.2);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -2px rgba(0, 0, 0, 0.3);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
}
```

---

## 7. Imagery & Visual Asset Art Direction
- **Primary Aspect Ratios:** `16/9` (Hero/Video), `4/3` (Case Studies), `1/1` (Portraits), `21/9` (Panoramas).
- **Art Direction Treatment:** [e.g., High-contrast monochrome studio captures with subtle vignette and dark ambient background separation].
- **Anti-Stock Mandate:** Zero generic office handshakes; all visuals must be bespoke 3D renders, real platform screenshots, or architectural photography.

---

## 8. Iconography System
- **Icon Library:** [e.g., `Lucide Icons` / `Phosphor Icons` / `Heroicons`]
- **Stroke Width:** Unified `1.5px` across all instances.
- **Sizing Tokens:** `icon-sm` (16px), `icon-md` (20px), `icon-lg` (24px), `icon-xl` (32px).

---

## 9. Interactive Controls (Buttons & Links)
- **Button Primary:** Height `44px-48px`, background `var(--accent-primary)`, text `var(--accent-primary-fg)`, border-radius `var(--radius-md)`. States: `default`, `hover`, `active`, `focus-visible`, `disabled`.
- **Button Secondary:** Height `44px-48px`, background `var(--bg-surface)`, border `1px solid var(--border-medium)`.
- **Button Ghost / Outline:** Transparent background, border `1px solid var(--border-subtle)`.
- **Link Buttons:** Underlined on hover with directional arrow micro-interaction (`→`).

---

## 10. Form & Input Controls
- **Input Dimensions:** Minimum height `44px` (Desktop: `44px-48px`, Mobile: `48px`).
- **Focus Rings:** `outline: 2px solid var(--border-focus); outline-offset: 2px;`.
- **Validation Styling:** Inline error copy in `--status-error` with `aria-live="polite"`.

---

## 11. Navigation & Footer Systems
- **Header:** Height `72px`, sticky blur background `rgba(10, 13, 18, 0.85)` with `backdrop-filter: blur(12px)`.
- **Mobile Menu:** Slide-out drawer with body scroll lock and touch targets $\ge 48\text{px}$.
- **Footer Structure:** Multi-column sitemap, status beacon, compliance links, copyright.

---

## 12. Container & Card Specifications
- **Card Purpose Rule:** Only wrap discrete interactive units or distinct data entities.
- **Card Padding:** `var(--space-6)` (24px) interior padding, background `var(--bg-surface)`, border `1px solid var(--border-subtle)`.

---

## 13. Motion Physics & Transition Choreography

```css
:root {
  --transition-fast: 150ms cubic-bezier(0.16, 1, 0.3, 1);
  --transition-normal: 250ms cubic-bezier(0.16, 1, 0.3, 1);
  --transition-smooth: 400ms cubic-bezier(0.16, 1, 0.3, 1);
}

@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 14. Accessibility (A11Y) & Usability Constraints
- **Contrast:** Minimum `4.5:1` body text contrast, `3.0:1` large heading contrast against backgrounds.
- **Keyboard Navigation:** Logical tab order across all interactive elements.
- **Touch Targets:** Minimum `44px x 44px` on all mobile viewports.
- **Semantic HTML:** Semantic landmark tags used throughout (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`).

---

## 15. Design System Lock Gate
- [ ] Approved full homepage is rendered, reviewed, and explicitly approved by the owner.
- [ ] Homepage approval is recorded under the existing `visual_prototypes.homepage_visual_approved` evidence field.
- [ ] Every token and subsystem above is traceable to the approved homepage; no aesthetic reinterpretation was introduced.
- [ ] All 14 design system sub-systems validated and populated.
- [ ] Zero ambiguous styling rules or unmapped tokens.
- [ ] Ready to lock `DESIGN_SYSTEM_LOCKED` in `site-profile.json`.
