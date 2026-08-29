# DESIGN SYSTEM SPECIFICATION: ALPHA STARTS NOW
## The 5 Morning Rituals (Direction C: The Dawn Vanguard Flagship)

> **Date Created:** 2026-08-27  
> **Status:** READY_FOR_GATE_4_LOCK (`DESIGN_SYSTEM_LOCKED: true`)  
> **Aesthetic Theme:** Dark Mode Native (Obsidian Navy & Solar Gold)  
> **Approved Direction:** Direction C (The Dawn Vanguard)  

---

## 1. Brand Posture & Theme Fundamentals
- **Archetype Blend:** 50% Cinematic Editorial + 30% Architectural Discipline + 20% Tactical Precision
- **Theme Paradigm:** Dark Mode Native (Obsidian Night Canvas & Radiant Dawn Accents)
- **Brand Attributes:** Dignified, Disciplined, Authoritative, Gravitational, Uncompromising

---

## 2. Typography Tokens & Mathematical Scale

```css
:root {
  /* Font Families */
  --font-display: 'Cinzel', Georgia, serif;
  --font-body: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Fluid Typographic Scale */
  --text-hero: clamp(3rem, 7vw, 5.5rem);       /* 48px - 88px */
  --text-h1: clamp(2.5rem, 5vw, 3.75rem);      /* 40px - 60px */
  --text-h2: clamp(1.85rem, 3.5vw, 2.75rem);   /* 30px - 44px */
  --text-h3: clamp(1.35rem, 2.2vw, 1.75rem);   /* 22px - 28px */
  --text-lead: 1.25rem;                        /* 20px */
  --text-body: 1.0rem;                         /* 16px */
  --text-caption: 0.875rem;                    /* 14px */
  --text-eyebrow: 0.8125rem;                   /* 13px */

  /* Line Heights */
  --leading-tight: 1.08;
  --leading-snug: 1.25;
  --leading-normal: 1.6;
  --leading-relaxed: 1.75;

  /* Letter Spacing */
  --tracking-tight: -0.02em;
  --tracking-normal: 0em;
  --tracking-wide: 0.08em;
  --tracking-cinematic: 0.18em;
}
```

---

## 3. Color Tokens & Semantic Assignments

```css
:root {
  /* Canvas & Atmospheric Surfaces (60%) */
  --canvas-obsidian: #040914;
  --canvas-midnight: #0A1528;
  --canvas-surface: #10213B;
  --canvas-elevated: #162B4D;

  /* Text & Readability (30%) */
  --text-pure: #FFFFFF;
  --text-slate: #CBD5E1;
  --text-muted: #94A3B8;
  --text-inverse: #040914;

  /* Solar Gold Brand Accents (10%) */
  --gold-solar: #F59E0B;
  --gold-dawn: #FDE047;
  --gold-amber: #D97706;
  --gold-glow: rgba(245, 158, 11, 0.35);

  /* Structural Geometry & Dividers */
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-gold: rgba(245, 158, 11, 0.28);
  --border-gold-bright: rgba(245, 158, 11, 0.65);
}
```

---

## 4. Spacing Cadence & Layout Tokens

```css
:root {
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

  --container-max: 1280px;
  --container-narrative: 960px;
  --container-form: 560px;
}
```

---

## 5. Surface Geometry, Elevation & Physics

```css
:root {
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-full: 9999px;

  --shadow-node: 0 20px 40px rgba(0, 0, 0, 0.6);
  --shadow-gold-glow: 0 0 35px rgba(245, 158, 11, 0.4);

  --ease-cinematic: cubic-bezier(0.16, 1, 0.3, 1);
  --transition-smooth: 350ms var(--ease-cinematic);
}

@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 6. Design System Lock Gate

```ini
GATE_4_NAME              = DESIGN_SYSTEM
GATE_4_STATUS            = LOCKED_AND_FROZEN
TOKENS_DERIVED_FROM_C    = TRUE
WCAG_CONTRAST_PASS       = TRUE
DESIGN_SYSTEM_LOCKED     = TRUE
```
