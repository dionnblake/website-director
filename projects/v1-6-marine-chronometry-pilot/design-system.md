# DESIGN SYSTEM TOKEN ARCHITECTURE: KESTREL & ROWE

> **Status:** LOCKED (`DESIGN_SYSTEM_LOCKED: true`)  
> **Standard:** 14-Subsystem Token Framework (`DESIGN-SYSTEM-PROTOCOL.md`)  

---

## 1. Color Palette (60/30/10 Rule)
- **Dominant Base (60%):** `--color-bg-abyss: #050C1A`, `--color-surface-abyss: #0A1526`, `--color-surface-panel: #101E33`
- **Structural Supporting (30%):** `--color-text-primary: #F0F4F8`, `--color-text-secondary: #94A3B8`, `--color-text-muted: #8295AC`, `--color-border-hairline: #1E293B`, `--color-border-accent: #334155`
- **High-Impact Accent (10%):** `--color-naval-brass: #C5A059`, `--color-brass-glow: rgba(197, 160, 89, 0.25)`, `--color-phosphor-mint: #38E5A1`, `--color-phosphor-glow: rgba(56, 229, 161, 0.2)`

---

## 2. Typography Subsystem
- **Display Headings:** `Cinzel, serif` (`font-weight: 500, 700`, `letter-spacing: 0.04em`, `text-transform: uppercase`)
- **Body & Editorial:** `Source Serif 4, Georgia, serif` (`font-weight: 400`, `line-height: 1.65`, `max-width: 68ch`)
- **Data & Telemetry:** `JetBrains Mono, monospace` (`font-variant-numeric: tabular-nums`, `font-size: 0.875rem`)

---

## 3. Spatial & Geometry Subsystem
- **8-Point Cadence:** `4px`, `8px`, `16px`, `24px`, `32px`, `48px`, `64px`, `96px`
- **Geometry:** Razor `2px` corners (`--radius-subtle: 2px`)
- **Reading Measure:** `--measure-body: 68ch`
- **Surface Theming:** Custom `::selection` in naval brass with deep navy text, high-contrast `:focus-visible` rings in phosphor mint.
