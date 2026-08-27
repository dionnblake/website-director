# DESIGN SYSTEM PROTOCOL: TOKEN SPECIFICATION & ARCHITECTURE

> **Version:** 1.0.0  
> **Status:** Mandatory Design System Architecture  
> **Purpose:** Establish the exhaustive, deterministic design specification required before any implementation code is written.

---

## 1. The Design System Mandate

No implementation agent may write a single line of CSS, Tailwind utility class, or HTML structure without a fully completed and locked `templates/design-system.md` file.

The design system specification is organized into 14 explicit sub-systems.

---

## 2. The 14 Sub-Systems

```
┌─────────────────────────────────────────────────────────────┐
│ 1. BRAND POSTURE & MOOD MATRIX                              │
│ 2. TYPOGRAPHY HIERARCHY & TYPE SCALE                        │
│ 3. COLOR ARCHITECTURE & TOKEN MAPPING                       │
│ 4. SPATIAL CADENCE & DENSITY SCALE                          │
│ 5. GRID, BREAKPOINTS & CONTAINER GEOMETRY                   │
│ 6. SURFACE GEOMETRY, BORDERS & ELEVATION                    │
│ 7. IMAGERY & VISUAL ASSET ART DIRECTION                     │
│ 8. ICONOGRAPHY SYSTEM                                       │
│ 9. INTERACTIVE CONTROLS (BUTTONS & LINKS)                   │
│ 10. FORM & INPUT CONTROLS                                   │
│ 11. NAVIGATION & FOOTER SYSTEMS                             │
│ 12. CONTAINER & CARD SPECIFICATIONS                         │
│ 13. MOTION PHYSICS & TRANSITION CHOREOGRAPHY                │
│ 14. ACCESSIBILITY (A11Y) & USABILITY CONSTRAINTS            │
└─────────────────────────────────────────────────────────────┘
```

---

### 1. Brand Posture & Mood Matrix
- **Core Archetype Blend:** (e.g., 60% Modernist + 30% Technical + 10% Editorial).
- **Brand Attributes:** 3 to 5 non-negotiable adjectives (e.g., *Surgical, Authoritative, High-Contrast, Restrained, Infallible*).
- **Mood Board Keywords:** Visual textures, lighting styles, physical material inspirations (e.g., *matte titanium, obsidian glass, Swiss editorial printing*).

---

### 2. Typography Hierarchy & Type Scale

#### Font Family Roles:
- **Display / Headline Font:** (e.g., `Syne`, `Fraunces`, `Instrument Sans`, `Plus Jakarta Sans`).
- **Body / Interface Font:** (e.g., `Inter`, `Geist Sans`, `DM Sans`, `Newsreader`).
- **Data / Accent Mono Font:** (e.g., `JetBrains Mono`, `Space Mono`, `Fira Code`).

#### Mathematical Type Scale (Desktop & Mobile):
All scales must define Size (`rem`/`px`), Weight (`font-weight`), Line Height (`leading`), and Letter Spacing (`tracking`).

| Token | Desktop Size | Mobile Size | Weight | Line Height | Tracking | Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `text-display` | 4.5rem (72px) | 2.75rem (44px) | 700/800 | 1.05 | -0.03em | Monumental Hero Title |
| `text-h1` | 3.25rem (52px) | 2.25rem (36px) | 700 | 1.15 | -0.02em | Section Primary Titles |
| `text-h2` | 2.25rem (36px) | 1.75rem (28px) | 600 | 1.25 | -0.015em| Subsection & Feature Headers |
| `text-h3` | 1.5rem (24px) | 1.25rem (20px) | 600 | 1.35 | -0.01em | Card & Component Titles |
| `text-lead` | 1.25rem (20px) | 1.125rem (18px)| 400/500 | 1.6 | normal | Hero Subheading & Introductions |
| `text-body` | 1.0rem (16px) | 1.0rem (16px) | 400 | 1.65 | normal | Paragraph Copy & Descriptions |
| `text-caption`| 0.875rem (14px)| 0.875rem (14px)| 400/500 | 1.5 | +0.01em | Secondary Meta & Form Labels |
| `text-mono` | 0.8125rem(13px)| 0.8125rem(13px)| 500 | 1.4 | +0.05em | Badges, Metrics, Code & Tags |

---

### 3. Color Architecture & Token Mapping

Color systems must follow a strict **60-30-10 Rule**:
- **60% Base / Backgrounds:** Dominant canvas tones.
- **30% Structural Surfaces & Typography:** High-contrast text, borders, and content planes.
- **10% Accent / Conversion:** High-intensity action buttons, focal badges, and critical interactive feedback.

#### Semantic Token Schema:
```css
/* Canvas / Backgrounds */
--bg-primary: #0A0D12;
--bg-secondary: #121820;
--bg-surface: #182230;
--bg-surface-hover: #1F2C3F;
--bg-elevated: #24344B;

/* Typography & Content */
--text-primary: #F9FAFB;
--text-secondary: #94A3B8;
--text-muted: #64748B;
--text-inverse: #0A0D12;

/* Structural Borders & Rules */
--border-subtle: rgba(255, 255, 255, 0.08);
--border-medium: rgba(255, 255, 255, 0.16);
--border-strong: rgba(255, 255, 255, 0.28);
--border-focus: #38BDF8;

/* Primary Action / Brand Accent */
--accent-primary: #0284C7;
--accent-primary-hover: #0369A1;
--accent-primary-fg: #FFFFFF;

/* Status & Feedback */
--success: #10B981;
--warning: #F59E0B;
--error: #EF4444;
--info: #38BDF8;
```

---

### 4. Spatial Cadence & Density Scale

Strict **8-Point Spatial System** (with a 4px sub-grid for fine alignment):
- `space-1`: 4px
- `space-2`: 8px
- `space-3`: 12px
- `space-4`: 16px
- `space-6`: 24px
- `space-8`: 32px
- `space-12`: 48px
- `space-16`: 64px
- `space-24`: 96px
- `space-32`: 128px

**Section Vertical Padding:**
- Hero Section: `96px` to `128px` (Desktop) / `64px` to `80px` (Mobile).
- Standard Content Sections: `80px` to `112px` (Desktop) / `48px` to `64px` (Mobile).
- Compact / Transition Sections: `48px` to `64px`.

---

### 5. Grid, Breakpoints & Container Geometry

#### Breakpoints:
- `sm`: 640px (Mobile landscape / large phones)
- `md`: 768px (Tablets portrait)
- `lg`: 1024px (Tablets landscape / small laptops)
- `xl`: 1280px (Standard desktop)
- `2xl`: 1536px (Large widescreen monitors)

#### Containers:
- `container-narrow`: `768px` (Editorial articles, single column forms, legal text).
- `container-standard`: `1200px` (Standard marketing pages, feature grids, pricing).
- `container-wide`: `1440px` (Dense data matrices, dashboard previews, expansive showcases).
- `container-full`: `100%` (Cinematic full-bleed sections with horizontal padding).

---

### 6. Surface Geometry, Borders & Elevation

- **Border Radius Discipline:** All elements must inherit from one coherent geometry tier:
  - *Sharp Modernist / Industrial / Luxury:* `0px` to `2px`.
  - *Refined Corporate / Editorial:* `4px` to `8px`.
  - *Modern SaaS / Technical:* `8px` to `12px`.
  - *Organic / Playful:* `16px` to `28px` (Pill: `9999px`).
- **Shadow Tokens (Layered Depth):**
  - `shadow-sm`: `0 1px 2px 0 rgba(0, 0, 0, 0.05)`
  - `shadow-md`: `0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)`
  - `shadow-xl`: `0 20px 25px -5px rgba(0, 0, 0, 0.25), 0 8px 10px -6px rgba(0, 0, 0, 0.25)`

---

### 7. Imagery & Visual Asset Art Direction
- **Aspect Ratios:** Explicitly defined per component (`16/9` for videos/hero, `4/3` for case studies, `1/1` for portraits, `21/9` for widescreen panoramas).
- **Art Direction Protocol:** Specifies treatment (e.g., desaturated duotone, high-contrast studio monochrome, grain overlay, or soft ambient glow).
- **No Stock Clichés:** All images must have specific art direction prompts and semantic context.

---

### 8. Iconography System
- **Single Icon Family:** (e.g., `Lucide Icons`, `Phosphor Icons`, `Heroicons`, or custom SVGs). Never mix icon families with differing line weights.
- **Stroke Width:** Unified across the entire project (e.g., uniform `1.5px` or `2.0px`).
- **Icon Sizing Tokens:** `icon-sm` (16px), `icon-md` (20px), `icon-lg` (24px), `icon-xl` (32px).

---

### 9. Interactive Controls (Buttons & Links)

Every button variant must specify all states: `default`, `hover`, `active`, `focus-visible`, and `disabled`.

- **Button Primary:** High contrast accent color, prominent padding (`12px 24px`), font-weight 600.
- **Button Secondary:** Surface background with subtle border, font-weight 500.
- **Button Ghost / Outline:** Transparent background, hairline border, subtle hover tint.
- **Button Link:** Underlined on hover, accompanied by directional micro-icon (`→`).

---

### 10. Form & Input Controls
- **Input Dimensions:** Minimum touch target height `44px` (Desktop: `44px-48px`, Mobile: `48px`).
- **Focus States:** Crisp 2px outline with `--border-focus` offset by 2px (`outline: 2px solid var(--border-focus); outline-offset: 2px;`).
- **Validation Styling:** Inline error messages below input with red accent and `aria-live="polite"`.

---

### 11. Navigation & Footer Systems
- **Header States:** Transparent at top $\rightarrow$ Elevated with background blur on scroll.
- **Mobile Navigation:** High-speed slide-in drawer or full-screen overlay with clear tap targets ($\ge 48\text{px}$) and body scroll locking.
- **Footer Architecture:** Clean hierarchical organization: Brand statement, sitemap columns, compliance/legal links, copyright, and status indicator.

---

### 12. Container & Card Specifications
- **Strict Justification Rule:** A card container is ONLY permitted if it encapsulates discrete interactive content or distinct data entities. Empty card wrapping for single lines of text is strictly prohibited.
- **Padding:** Uniform interior padding matching the spacing scale (e.g., `p-6` / 24px or `p-8` / 32px).

---

### 13. Motion Physics & Transition Choreography
- **Default Transition:** `all 200ms cubic-bezier(0.16, 1, 0.3, 1)` (snappy, responsive).
- **Modal / Drawer Easing:** `transform 300ms cubic-bezier(0.32, 0.72, 0, 1)`.
- **Accessibility:** Mandatory `@media (prefers-reduced-motion: reduce)` disabling all non-essential movement and converting transitions to instantaneous opacity changes.

---

### 14. Accessibility (A11Y) & Usability Constraints
- **Contrast Ratios:** Minimum `4.5:1` for normal body text and `3.0:1` for large headlines against backgrounds (WCAG 2.1 AA compliant).
- **Keyboard Focus:** Visible, high-contrast focus rings on all interactive elements.
- **Touch Targets:** Minimum `44px x 44px` physical touch area on all mobile viewports.
- **Semantic HTML:** `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`.
