# DESIGN SYSTEM SPECIFICATION: CINEMATIC MIDNIGHT ALPHA (LOCK 4)

## 1. Token Architecture Overview
- **Status:** **`DESIGN_SYSTEM_LOCKED`** (Engaged Lock 4)
- **Palette Architecture:** Deep Midnight Canvas (`#080C14`), Slate Navy Elevators (`#0F172A`), Architectural Steel (`#1E293B`), Electric Blue Energy Accent (`#0066FF`), Pure White (`#FFFFFF`), and Silver Steel (`#94A3B8`).

## 2. CSS Custom Properties Tokens

```css
:root {
  /* Surface Layers */
  --bg-midnight: #080c14;
  --bg-slate: #0f172a;
  --bg-slate-elevated: #15203b;
  --bg-surface-subtle: #0b111d;
  --bg-glass-hud: rgba(8, 12, 20, 0.88);

  /* Typography Colors */
  --text-white: #ffffff;
  --text-silver: #cbd5e1;
  --text-muted: #64748b;
  --text-cyan-glow: #38bdf8;

  /* Alpha Electric Energy */
  --accent-electric-blue: #0066ff;
  --accent-blue-hover: #1d78ff;
  --accent-blue-subtle: rgba(0, 102, 255, 0.12);
  --accent-blue-glow: 0 0 24px rgba(0, 102, 255, 0.4);

  /* Borders & Dividers */
  --border-hairline: 1px solid rgba(255, 255, 255, 0.08);
  --border-steel: 1px solid #1e293b;
  --border-steel-heavy: 2px solid #27354a;
  --border-blue-active: 2px solid #0066ff;

  /* Geometry */
  --radius-none: 0px;
  --radius-subtle: 2px;
  --radius-notch: 4px;

  /* Typography Fonts */
  --font-display: 'Barlow Condensed', 'Saira Condensed', -apple-system, sans-serif;
  --font-body: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;

  /* Type Scale */
  --type-hero-giant: clamp(3.8rem, 8.5vw, 8.5rem);
  --type-h1: clamp(2.6rem, 5vw, 4.5rem);
  --type-h2: clamp(1.8rem, 3.5vw, 3rem);
  --type-h3: clamp(1.2rem, 2.2vw, 1.7rem);
}
```
