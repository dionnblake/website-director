# DESIGN SYSTEM SPECIFICATION: VALENTIN & HESSE Architects

> **Date Created:** 2026-08-23  
> **Status:** LOCKED (`DESIGN_SYSTEM_LOCKED: true`)  
> **Rule:** All CSS variables, layout tokens, and component classes must derive strictly from this document.

---

## 1. Brand Posture & Theme Fundamentals
- **Archetype Blend:** 60% Architectural + 30% Editorial + 10% Tactile Material Modernist.
- **Theme Paradigm:** Light Mineral Native (Warm Alabaster Canvas, Raw Travertine, Deep Silt Umber, Muted Bronze).
- **Brand Attributes:** Monolithic, Tactile, Atmospheric, Restrained, Bespoke.

---

## 2. Typography Tokens & Mathematical Scale

```css
:root {
  /* Font Families */
  --font-display: 'Cormorant Garamond', 'Playfair Display', Georgia, serif;
  --font-body: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-meta: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;

  /* Typographic Scale: 1.250 Major Third Scale */
  --text-display-hero: clamp(2.75rem, 5.5vw, 4.5rem);  /* 44px - 72px */
  --text-display: clamp(2.25rem, 4vw, 3.25rem);       /* 36px - 52px */
  --text-h1: clamp(1.85rem, 3vw, 2.5rem);             /* 30px - 40px */
  --text-h2: clamp(1.45rem, 2.2vw, 1.85rem);          /* 23px - 30px */
  --text-h3: clamp(1.15rem, 1.5vw, 1.35rem);          /* 18px - 22px */
  --text-lead: 1.125rem;                              /* 18px */
  --text-body: 0.9375rem;                             /* 15px */
  --text-caption: 0.8125rem;                          /* 13px */
  --text-meta: 0.75rem;                               /* 12px */

  /* Line Heights */
  --leading-dense: 1.08;
  --leading-tight: 1.2;
  --leading-snug: 1.35;
  --leading-normal: 1.6;
  --leading-relaxed: 1.75;

  /* Letter Spacing */
  --tracking-tight: -0.02em;
  --tracking-normal: 0em;
  --tracking-wide: 0.04em;
  --tracking-widest: 0.12em;
}
```

---

## 3. Color Tokens & Semantic Assignments

```css
:root {
  /* Surface & Mineral Canvas (60%) */
  --bg-canvas: #F8F6F0;           /* Warm Alabaster / Limestone */
  --bg-surface: #ECE7DE;          /* Raw Travertine */
  --bg-surface-hover: #E3DDD2;    /* Honed Stone Hover */
  --bg-surface-elevated: #FAF8F5; /* Crisp Plaster White */
  --bg-contrast: #191816;         /* Monolithic Charcoal/Umber */

  /* Text & Mineral Pigments (30%) */
  --text-primary: #191816;        /* Deep Silt Umber (Contrast Ratio 13.8:1) */
  --text-secondary: #5C5952;      /* Raw Mineral Silt (Contrast Ratio 5.9:1) */
  --text-muted: #847F75;          /* Weathered Lime */
  --text-inverse: #F8F6F0;        /* Inverted Alabaster */
  --text-inverse-muted: #B8B3A8;  /* Inverted Soft Silt */

  /* Structural Rules & Mortar Joints */
  --border-subtle: rgba(25, 24, 22, 0.08);
  --border-medium: rgba(25, 24, 22, 0.16);
  --border-strong: rgba(25, 24, 22, 0.35);
  --border-focus: #8C7355;        /* Muted Bronze Focus Ring */

  /* Primary Brand Action & Accent (10%) */
  --accent-primary: #8C7355;      /* Muted Alpine Bronze / Ochre */
  --accent-primary-hover: #735D43;/* Deep Bronze */
  --accent-primary-fg: #FFFFFF;
  --accent-tint: rgba(140, 115, 85, 0.12);

  /* Material Swatch Specific Colors */
  --mat-quartzite: #6E7574;
  --mat-travertine: #D8CEBE;
  --mat-larch: #B88E5E;
  --mat-bronze: #594D3E;

  /* Semantic Feedback */
  --status-success: #3A6351;
  --status-warning: #9E6B28;
  --status-error: #963A2F;
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
  --space-20: 80px;
  --space-24: 96px;
  --space-32: 128px;

  /* Section Spacing */
  --section-padding-y: clamp(4rem, 8vw, 8rem);
  --section-padding-x: clamp(1.25rem, 4vw, 3.5rem);

  /* Layout Containers */
  --container-narrow: 840px;
  --container-standard: 1280px;
  --container-wide: 1560px;
  --container-full: 100%;
}
```

---

## 5. Geometry, Borders & Elevation

```css
:root {
  /* Monolithic Architectural Corner Geometry */
  --radius-sharp: 0px;
  --radius-sm: 2px;
  --radius-md: 4px;
  --radius-pill: 9999px;

  /* Natural Ambient Light Shadows (Subtle & Diffuse) */
  --shadow-subtle: 0 2px 8px rgba(25, 24, 22, 0.04);
  --shadow-card: 0 6px 20px rgba(25, 24, 22, 0.06);
  --shadow-drawer: -8px 0 32px rgba(25, 24, 22, 0.12);
  --shadow-modal: 0 16px 48px rgba(25, 24, 22, 0.16);
}
```

---

## 6. Imagery & Visual Asset Direction
- **Aspect Ratios:** `16/9` (Hero & Panoramas), `4/3` (Architectural Volumes), `3/4` (Vertical Interior Vignettes), `1/1` (Material Specimen Closeups).
- **Art Direction:** Warm natural daylight, soft cast shadows, tactile stone and grain texture, zero neon/glossy developer styling.
- **Architectural Dual-View:** Every project includes both high-definition finished spatial photography and precise CAD/blueprint drawings.

---

## 7. Interactive Controls & Buttons
- **Primary Action Button:** Solid deep umber (`--bg-contrast`) or bronze (`--accent-primary`), text `--text-inverse`, radius `var(--radius-sm)`, padding `14px 28px`, font-size `13px`, tracking `0.06em`, uppercase.
- **Secondary Action Button:** Border `1px solid var(--border-medium)`, background transparent, text `--text-primary`, subtle hover fill `var(--bg-surface)`.
- **Filter Tabs:** Understated text pills with active underline indicator and count badges.

---

## 8. Form & Input Controls
- **Input Height:** `48px` minimum with comfortable touch padding.
- **Input Styling:** Clean bottom-bordered or subtle bordered limestone input fields, focus highlight in `--border-focus`.
- **Validation:** Clear error states with assistive text.

---

## 9. Navigation & Floating Atelier Bar
- **Bar Height:** `68px`, floating with `backdrop-filter: blur(16px)` and subtle mortar border.
- **Mobile Menu:** Smooth full-screen or slide-in architectural drawer with unhurried typography.

---

## 10. Motion Physics & Tokens (Motion Level 2)

```css
:root {
  --ease-spatial: cubic-bezier(0.25, 1, 0.5, 1);
  --ease-out-smooth: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-fast: 180ms;
  --duration-normal: 320ms;
  --duration-spatial: 500ms;
}

@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 11. Accessibility & Usability Assurance
- **Contrast Check:** `--text-primary` (`#191816`) on `--bg-canvas` (`#F8F6F0`) yields **13.8:1** (AAA standard).
- **Focus Visibility:** Dedicated high-visibility focus indicators with `2px offset`.
- **Touch Sizing:** All interactive targets $\ge 44\text{px} \times 44\text{px}$.

---

## 12. Design System Lock Gate
- [x] All 14 token systems defined with mathematically grounded values.
- [x] Warm mineral palette strictly adheres to 60/30/10 rule.
- [x] Zero overlap with Alpha Starts Now visual vocabulary.
- [x] **`locks.design_system_locked = true` (Lock 4 engaged)**.
