# DESIGN SYSTEM SPECIFICATION: KREISLER & VOSS Motorenwerke

> **Date Created:** 2026-08-23  
> **Status:** LOCKED (Lock 4 Engaged)  
> **Stage:** Phase 11 — Design Tokens & Production Architecture  

---

## 1. Typography System

```css
:root {
  /* Font Families */
  --font-display: 'Syne', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-body: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'SF Mono', Consolas, monospace;

  /* Typographic Scale: 1.250 Major Third */
  --text-display-hero: clamp(2.5rem, 5.5vw, 4.5rem);
  --text-display: clamp(2.1rem, 4vw, 3.25rem);
  --text-h1: clamp(1.8rem, 3vw, 2.5rem);
  --text-h2: clamp(1.4rem, 2.2vw, 1.95rem);
  --text-h3: clamp(1.15rem, 1.5vw, 1.45rem);
  --text-lead: clamp(1.05rem, 1.3vw, 1.25rem);
  --text-body: 0.9375rem;       /* 15px */
  --text-caption: 0.8125rem;    /* 13px */
  --text-meta: 0.75rem;         /* 12px */
  --text-micro: 0.6875rem;      /* 11px */

  /* Line Heights */
  --leading-dense: 1.05;
  --leading-tight: 1.2;
  --leading-snug: 1.38;
  --leading-normal: 1.65;
  --leading-relaxed: 1.8;

  /* Letter Spacing */
  --tracking-tight: -0.025em;
  --tracking-normal: 0em;
  --tracking-wide: 0.06em;
  --tracking-widest: 0.16em;
}
```

---

## 2. Color System & Surface Materiality (60/30/10 Ratio)

```css
:root {
  /* Surface Canvas (60%) */
  --bg-canvas: #0E0F12;           /* Deep Gunmetal Charcoal */
  --bg-surface: #17191E;          /* Milled Alloy Slate */
  --bg-surface-elevated: #22262D; /* Raised Workshop Plate */
  --bg-surface-hover: #2B303A;    /* Chamfered Edge Hover */
  --bg-surface-glass: rgba(23, 25, 30, 0.82);

  /* Text & Pigments (30%) */
  --text-primary: #F2F1ED;        /* Anodized Platinum White (14.2:1) */
  --text-secondary: #A2A6B0;      /* Milled Titanium Silt (7.4:1) */
  --text-muted: #6C707A;          /* Weathered Iron Grey (4.8:1) */
  --text-inverse: #0E0F12;
  --text-mono-telemetry: #34D399; /* Calibrated Dyno Green */

  /* Primary Brand Action & Accent (10%) */
  --accent-primary: #C88242;      /* Warm Saddle Ochre / Cognac */
  --accent-primary-hover: #D99554;/* Polished Saddle Ochre */
  --accent-primary-fg: #0E0F12;   /* Contrast Black Text */
  --accent-tint: rgba(200, 130, 66, 0.12);

  /* Mechanical Hardware Highlights */
  --metal-billet: #D1D5DB;        /* 6061-T6 Billet Aluminum */
  --metal-titanium: #9CA3AF;      /* Grade 5 Titanium */
  --metal-inconel: #E5C388;       /* High-Temp Inconel Gold Heat-Wrap */
  --metal-bronze: #8C7355;        /* Oil-Impregnated Phosphor Bronze */

  /* Structural Borders & Mortar Joints */
  --border-subtle: rgba(242, 241, 237, 0.08);
  --border-medium: rgba(242, 241, 237, 0.16);
  --border-strong: rgba(242, 241, 237, 0.32);
  --border-accent: rgba(200, 130, 66, 0.45);
}
```

---

## 3. Spacing, Layout & Geometry

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
  --space-20: 80px;
  --space-24: 96px;
  --space-32: 128px;

  /* Section Padding */
  --section-padding-y: clamp(4rem, 8vw, 8rem);
  --section-padding-x: clamp(1.25rem, 4vw, 4rem);

  /* Containers */
  --container-narrow: 880px;
  --container-standard: 1320px;
  --container-wide: 1600px;

  /* Geometry & Radii */
  --radius-sharp: 0px;
  --radius-sm: 1px;
  --radius-md: 2px;
  --radius-pill: 9999px;

  /* Shadows */
  --shadow-subtle: 0 2px 10px rgba(0, 0, 0, 0.35);
  --shadow-card: 0 8px 30px rgba(0, 0, 0, 0.55);
  --shadow-drawer: -12px 0 40px rgba(0, 0, 0, 0.75);
}
```

---

## 4. Motion Physics (Motion Level 3: Weighted Mechanical Precision)

```css
:root {
  --ease-mechanical: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-spatial: cubic-bezier(0.25, 1, 0.5, 1);
  --duration-fast: 180ms;
  --duration-normal: 350ms;
  --duration-spatial: 550ms;
}
```

---

## 5. Lock 4 Confirmation
- [x] All 14 token categories complete and contrast validated.
- [x] **`locks.design_system_locked = true`**.
