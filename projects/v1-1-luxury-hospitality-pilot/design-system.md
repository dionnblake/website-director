# DESIGN SYSTEM SPECIFICATION & TOKENS — SÖLVIK FJORD RETREAT

> **Pilot Code:** `WD-V1.1-HOSP-001`  
> **Schema Version:** 1.1.0  
> **Lock 4:** `design_system_locked = true`  

---

## 1. Color Palette System

```css
:root {
  /* Surface & Background Hierarchy */
  --bg-abyss: #070B0E;              /* Base Canvas — Deepest Norwegian Fjord Abyss */
  --bg-surface: #0E151A;            /* Primary Section Surface — Slate Mist */
  --bg-card: #141E24;               /* Elevated Card Surface — Wet Granite */
  --bg-card-hover: #1B2830;         /* Card Interactive Lift */
  --bg-overlay: rgba(7, 11, 14, 0.85); /* Backdrop Blur Glassmorphism */

  /* Borders & Dividers */
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-accent: rgba(200, 131, 70, 0.35);
  --border-glow: rgba(200, 131, 70, 0.6);

  /* Brand Accents */
  --accent-amber: #C88346;          /* Nordic Hearth Amber & Embers */
  --accent-amber-light: #E09E64;    /* Hover Amber */
  --accent-lichen: #7B8C86;         /* Mountain Lichen & Moss */
  --accent-fjord: #3B5A6B;          /* Glacial Fjord Water */

  /* Text & Content Tokens */
  --text-pure: #F4F1EA;             /* Bone White Display & Headings */
  --text-primary: #D6D2C4;          /* Warm Light Gray Primary Body */
  --text-secondary: #969C9B;        /* Muted Lichen Secondary Meta */
  --text-dim: #606869;              /* Captions & Technical Coordinates */

  /* Shadows & Depth */
  --shadow-ambient: 0 20px 50px rgba(0, 0, 0, 0.6);
  --shadow-hearth: 0 0 40px rgba(200, 131, 70, 0.15);
  --shadow-glow: 0 0 25px rgba(200, 131, 70, 0.3);
}
```

---

## 2. Typography Hierarchy

* **Display & Heading Serif:** `Fraunces, "Playfair Display", Georgia, serif`
  * *Scale:* `h1` (clamp(2.75rem, 6vw, 4.75rem)), `h2` (clamp(2rem, 4vw, 3.25rem)), `h3` (1.75rem), `h4` (1.25rem)
  * *Tracking:* `-0.02em`
  * *Weight:* `400` (Restrained elegance)
* **Body Sans-Serif:** `Plus Jakarta Sans, -apple-system, sans-serif`
  * *Scale:* Body Large (1.125rem), Body Standard (1rem), Body Small (0.875rem)
  * *Line Height:* `1.65`
  * *Weight:* `300` / `400`
* **Meta & Spatial Monospace:** `JetBrains Mono, Menlo, monospace`
  * *Scale:* `0.75rem` / `0.8125rem`
  * *Tracking:* `0.1em` uppercase

---

## 3. Component Specifications

1. **Top Navigation Bar:**
   * Height: `80px`
   * Background: `rgba(7, 11, 14, 0.75)` with `backdrop-filter: blur(16px)`
   * Layout: Brand wordmark left, centered editorial links, primary "Plan Your Stay" CTA right.
2. **Pavilion Cards:**
   * Dark stone surface (`--bg-card`), 1px subtle border, full-width high-definition architectural imagery, spatial tag badges, interactive "Configure Stay" trigger.
3. **Thermal Ritual Progression:**
   * 3-step interactive tabs with temperature indicators (`39°C`, `6°C`, `88°C`), photography reveal, and sensory descriptions.
4. **"Plan Your Stay" Drawer:**
   * Slide-in modal drawer from right on desktop / bottom sheet on mobile, featuring season selector, pavilion category, guest count, and instant inquiry confirmation.

---

## 4. Design System Sign-Off
`design_system_locked = true`
