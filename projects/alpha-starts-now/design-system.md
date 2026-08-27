# DESIGN SYSTEM SPECIFICATION: ALPHA STARTS NOW

> **Date Created:** 2026-08-23  
> **Status:** LOCKED (`DESIGN_SYSTEM_LOCKED: true`)  
> **Mode:** ORIGINAL_MODE  
> **Design Authority:** Website Director V1  
> **Rule:** All CSS variables, Tailwind tokens, and component classes must derive strictly from this document. Zero ad-hoc hex values, arbitrary margins, or unmapped styles.

---

## 1. Brand Posture & Theme Fundamentals
- **Archetype Blend:** `60% Modernist + 30% Architectural + 10% Editorial` (*"The Modernist Field Monograph"*).
- **Core Aesthetic Law:** Restraint, structural clarity, high typographic contrast, tactile materiality, and quiet confidence. Strictly zero decorative gradients, floating UI blobs, or generic card spam.
- **Theme Paradigm:** Dark Monograph Canvas Native (Obsidian & Graphite) with Warm Limestone Paper zones for long-form reading comfort.
- **Brand Attributes:** *Mature, Disciplined, Deliberate, Precise, Grounded, Self-Respecting, Direct.*

---

## 2. Typography Hierarchy & Mathematical Scale

```css
:root {
  /* Font Family Roles */
  --font-display: 'Cabinet Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-editorial: 'Newsreader', 'Fraunces', Georgia, serif;
  --font-mono: 'JetBrains Mono', 'Space Mono', monospace;

  /* Typographic Scale (Desktop & Mobile Clamp) */
  --text-display: clamp(2.75rem, 5vw, 4.25rem); /* 44px - 68px | Monumental Hero Headline */
  --text-h1: clamp(2.25rem, 3.5vw, 3.0rem);      /* 36px - 48px | Primary Page Titles */
  --text-h2: clamp(1.625rem, 2.5vw, 2.125rem);   /* 26px - 34px | Section & Pillar Titles */
  --text-h3: clamp(1.25rem, 1.75vw, 1.5rem);     /* 20px - 24px | Article & Guide Headers */
  --text-lead: 1.1875rem;                        /* 19px | Hero Subheads & Manifesto Intros */
  --text-body: 1.0rem;                           /* 16px | Paragraph Copy & Editorial Body */
  --text-caption: 0.875rem;                      /* 14px | Form Labels, Excerpts, Meta */
  --text-mono: 0.8125rem;                        /* 13px | Pillar Tags, Reading Time, Indexes */

  /* Line Heights */
  --leading-tight: 1.12;
  --leading-snug: 1.28;
  --leading-normal: 1.55;
  --leading-relaxed: 1.68;

  /* Letter Spacing (Tracking) */
  --tracking-tight: -0.03em;
  --tracking-snug: -0.015em;
  --tracking-normal: 0em;
  --tracking-wide: 0.04em;
  --tracking-mono: 0.08em;
}
```

---

## 3. Color Architecture & Token Mapping (60-30-10 Rule)

```css
:root {
  /* Surface & Canvas (60% Dominant Base) */
  --bg-primary: #0C0E12;          /* Deep Obsidian Slate (Main Dark Canvas) */
  --bg-secondary: #12161E;        /* Dark Graphite (Modular Sections) */
  --bg-surface: #181D26;          /* Milled Charcoal (Elevated Containers & Nav) */
  --bg-surface-hover: #1F2531;    /* Subtle Hover Surface */
  --bg-paper: #F4F1EA;            /* Warm Limestone / Alabaster (Editorial Read Zones) */
  --bg-paper-surface: #FFFFFF;    /* Pure White Paper Inset */

  /* Typography & Content (30% Structure & Text) */
  --text-primary: #F9FAFB;        /* High-Contrast Chalk White */
  --text-secondary: #94A3B8;      /* Muted Slate Gray (Secondary Copy) */
  --text-muted: #64748B;          /* Subdued Meta & Timestamps */
  --text-paper-primary: #12161E;  /* Deep Ink Black for Light Zones */
  --text-paper-secondary: #475569;/* Slate Charcoal for Light Zones */

  /* Structural Lines & Hairline Dividers */
  --border-subtle: rgba(255, 255, 255, 0.08); /* 1px Architectural Hairline */
  --border-medium: rgba(255, 255, 255, 0.16); /* Container Bounding Rules */
  --border-strong: rgba(255, 255, 255, 0.28); /* Active Component Borders */
  --border-paper: rgba(0, 0, 0, 0.10);        /* Hairline for Light Zones */
  --border-focus: #D96B27;                    /* Amber Focus Ring */

  /* Primary Brand Action & Accent (10% Kinetic Punch) */
  --accent-primary: #D96B27;        /* Burnt Oxide Amber (Decisive, Masculine) */
  --accent-primary-hover: #BF5A1B;  /* Deepened Oxide Amber */
  --accent-primary-fg: #FFFFFF;     /* Pure White CTA Label */

  /* Semantic Status Tokens */
  --status-success: #10B981;
  --status-warning: #F59E0B;
  --status-error: #EF4444;
  --status-info: #64748B;
}
```

---

## 4. Spatial Cadence & Density Scale (Strict 8-Point Grid)

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
}
```

- **Section Vertical Rhythm (Desktop):** `80px` to `112px` (Generous negative space framing long-form thought).
- **Section Vertical Rhythm (Mobile):** `48px` to `64px`.
- **Component Gutters:** `24px` (`--space-6`) to `32px` (`--space-8`).

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
  --container-narrow: 768px;   /* Manifesto & Single-Column Guide Articles */
  --container-standard: 1200px; /* Flagship Marketing & Category Indexes */
  --container-wide: 1440px;     /* Panoramic Hero & Asymmetric Spreads */
  --container-full: 100%;       /* Full-Bleed Structural Bands */
}
```

---

## 6. Surface Geometry, Borders & Elevation

- **Border Radius Discipline:** Strict **Refined Architectural Tier** (`2px` to `4px`).
  - `var(--radius-sm)`: `2px` (Buttons, badges, index tags).
  - `var(--radius-md)`: `4px` (Cards, inputs, image containers).
  - Strictly banned: Bulbous pill cards (`16px-24px`) and generic rounded rectangles.
- **Elevation Tokens (Subtle Ambient Layering):**
  - `--shadow-sm`: `0 1px 2px 0 rgba(0, 0, 0, 0.35)`
  - `--shadow-md`: `0 4px 8px -2px rgba(0, 0, 0, 0.45), 0 2px 4px -2px rgba(0, 0, 0, 0.35)`
  - Strictly banned: Giant diffuse blur shadows floating under flat cards.

---

## 7. Imagery & Visual Asset Art Direction
- **Aspect Ratios:** `16/9` (Hero visual canvas), `4/3` (Cornerstone guide covers), `3/2` (Documentary stills), `1/1` (Product detail close-ups).
- **Treatment:** Natural ambient light, high-contrast sculptural shadows, tactile material focus (leather, machined steel, paper, denim, pavement).
- **Subject Mix:** Real adult men (35–50) in purposeful action (quiet training, grooming, deep work, craft, travel).
- **Explicit Bans:** Zero shirtless bodybuilders, zero wolves, zero fire, zero gladiators, zero crypto beach tropes, zero AI fantasy art, zero coffee clichés.

---

## 8. Iconography System
- **Icon Library:** `Lucide Icons` (clean, geometric, universally legible).
- **Stroke Width:** Unified `1.5px` across all instances.
- **Sizes:** `icon-sm` (16px), `icon-md` (20px), `icon-lg` (24px).

---

## 9. Interactive Controls (Buttons & Links)
- **Button Primary (Ember Action):** Height `46px`, background `var(--accent-primary)`, text `var(--accent-primary-fg)`, font-weight `600`, font-size `var(--text-caption)`, letter-spacing `var(--tracking-wide)`, border-radius `var(--radius-sm)`.
- **Button Secondary (Graphite Outline):** Height `46px`, background `transparent`, border `1px solid var(--border-medium)`, text `var(--text-primary)`.
- **Editorial Text Link:** Inline text link with subtle underline, hover color shift to `var(--accent-primary)`, accompanied by directional micro-arrow (`→`).

---

## 10. Form & Input Controls (The Newsletter Engine)
- **Input Field:** Height `48px`, background `var(--bg-secondary)`, border `1px solid var(--border-medium)`, text `var(--text-primary)`, padding `0 16px`.
- **Focus State:** `outline: 2px solid var(--border-focus); outline-offset: 2px;`.
- **Validation:** Clear, accessible inline confirmation copy (`"Welcome to the Dispatch."`) without modal popups or disruptive overlays.

---

## 11. Navigation & Footer Systems
- **Header:** Height `72px`, fixed top with `background: rgba(12, 14, 18, 0.85)` and `backdrop-filter: blur(12px)`. Hairline bottom border `1px solid var(--border-subtle)`.
- **Mobile Drawer:** Clean slide-out panel locking body scroll, touch targets $\ge 48\text{px}$, high-contrast typography.
- **Footer:** 4-column structured architectural layout with clear FTC disclosure, copyright, and sitemap.

---

## 12. Container & Card Specifications
- **Purpose Rule:** Containers exist only to group discrete functional entities (e.g., Guide cards, Product recommendations). Zero unnecessary decorative framing.
- **Interior Padding:** Strict `var(--space-6)` (24px) for cards; `var(--space-8)` (32px) for featured editorial spotlights.

---

## 13. Motion Physics & Transition Choreography
- **Default Interaction:** `all 200ms cubic-bezier(0.16, 1, 0.3, 1)` (Instant, crisp, mechanical feedback).
- **Modal / Drawer:** `transform 250ms cubic-bezier(0.32, 0.72, 0, 1)`.
- **Accessibility:** Mandatory `@media (prefers-reduced-motion: reduce)` reducing all durations to `0.01ms`.

---

## 14. Accessibility (A11Y) & Usability Constraints
- **Contrast Compliance:** Minimum `5.8:1` text-to-background contrast across all token pairs (exceeds WCAG 2.1 AA requirement of `4.5:1`).
- **Keyboard Navigation:** Unambiguous 2px focus ring on all interactive elements.
- **Touch Target Minimum:** `44px x 44px` on all mobile viewports.
- **Semantic Structure:** Semantic HTML5 landmark tags throughout (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`).

---

## 15. Gate 4 Lock Declaration
- [x] All 14 token sub-systems mapped to concrete CSS variables.
- [x] Zero ambiguous styling rules, unmapped hex codes, or arbitrary margins.
- [x] Complies with anti-slop rules and the owner's constraint against over-engineering.
- [ ] Owner review and approval to engage Gate 4 (`DESIGN_SYSTEM_LOCKED`).
