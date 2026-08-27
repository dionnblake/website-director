# DESIGN SYSTEM SPECIFICATION (LOCK 4)

## 1. Token Architecture Overview
- **Status:** **`DESIGN_SYSTEM_LOCKED`** (Engaged Lock 4)
- **Visual Stance:** Industrial Brutalism, 0px border-radius, heavy 2D borders, monolithic typography, high-contrast matte canvas.

## 2. CSS Custom Properties Tokens

```css
:root {
  /* Surface Colors */
  --bg-primary: #111215;
  --bg-surface: #181A20;
  --bg-surface-elevated: #22252E;
  --bg-surface-subtle: #14161C;
  --bg-overlay: rgba(17, 18, 21, 0.85);

  /* Text Colors */
  --text-primary: #FFFFFF;
  --text-secondary: #9FA4B2;
  --text-muted: #626775;
  --text-inverted: #111215;

  /* Accent & Status Colors */
  --accent-amber: #D97706;
  --accent-amber-hover: #F59E0B;
  --accent-amber-subtle: rgba(217, 119, 6, 0.12);
  --accent-cyan-laser: #06B6D4;
  --status-active: #10B981;

  /* Borders & Dividers */
  --border-hairline: 1px solid #2B2F3B;
  --border-heavy: 2px solid #3E4353;
  --border-active: 2px solid #D97706;
  --border-subtle: 1px solid rgba(255, 255, 255, 0.08);

  /* Geometry & Radius */
  --radius-none: 0px;
  --radius-sm: 0px;
  --radius-md: 0px;
  --radius-lg: 0px;

  /* Typography */
  --font-display: 'Clash Display', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-body: 'General Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;

  /* Type Scale */
  --type-display-giant: clamp(3.5rem, 9vw, 9.5rem);
  --type-h1: clamp(2.5rem, 5vw, 4.5rem);
  --type-h2: clamp(1.8rem, 3.5vw, 3rem);
  --type-h3: clamp(1.3rem, 2.2vw, 1.8rem);
  --type-body: 1.05rem;
  --type-body-sm: 0.9rem;
  --type-mono-badge: 0.8rem;

  /* Spacing Scale */
  --space-2xs: 0.25rem;
  --space-xs: 0.5rem;
  --space-sm: 1rem;
  --space-md: 1.5rem;
  --space-lg: 2.5rem;
  --space-xl: 4rem;
  --space-2xl: 7rem;

  /* Max Widths */
  --max-width-container: 1440px;
  --max-width-editorial: 960px;
}
```
