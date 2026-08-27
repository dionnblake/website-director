# IMPLEMENTATION CONTRACT SPECIFICATION: ALPHA STARTS NOW

> **Date Generated:** 2026-08-23  
> **Status:** READY FOR CODING (All 4 Locks Verified)  
> **Governance Authority:** Website Director V1 Specification  
> **Implementation Target:** `alpha-starts-now-website`  

---

## 1. Design Lock Verification Matrix

All four mandatory design gates have been formally approved and locked:

| Gate | Status | Verified Authority Artifact | Locked Timestamp |
| :--- | :---: | :--- | :--- |
| **Gate 1: `DESIGN_DIRECTION_LOCKED`** | **LOCKED (true)** | [design-direction.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now/design-direction.md) | 2026-08-23 |
| **Gate 2: `INFORMATION_ARCHITECTURE_LOCKED`** | **LOCKED (true)** | [information-architecture.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now/information-architecture.md) | 2026-08-23 |
| **Gate 3: `CONTENT_STRUCTURE_LOCKED`** | **LOCKED (true)** | [content-plan.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now/content-plan.md) | 2026-08-23 |
| **Gate 4: `DESIGN_SYSTEM_LOCKED`** | **LOCKED (true)** | [design-system.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/projects/alpha-starts-now/design-system.md) | 2026-08-23 |

---

## 2. Technical Stack Constraints & Architecture

- **Core Framework & Architecture:** HTML5 Semantic Structure + Modern CSS Architecture (Pure CSS Custom Properties or Tailwind CSS strictly aliased to CSS variables).
- **Typography Sourcing:**
  - Display: `Cabinet Grotesk` or `General Sans` (Fontsource / Google Fonts / Local WOFF2)
  - Body: `Inter` or `Geist Sans`
  - Editorial / Manifesto: `Newsreader` or `Fraunces`
  - Monospace / Metadata: `JetBrains Mono`
- **Icon Library:** `Lucide Icons` (Uniform `1.5px` stroke weight).
- **Image Optimization:** Modern `WebP` / `AVIF` with explicit `width`, `height`, and `aspect-ratio` definitions.

---

## 3. Strict Prohibitions During Implementation

The coding agent is strictly prohibited from introducing:

1. **Unregistered Colors:** Zero inline hex values (`#123456`), arbitrary RGB strings, or default framework color utilities (e.g., `bg-indigo-500` or generic purple gradients). Every color MUST resolve to a design token:
   - Base canvas: `var(--bg-primary)`, `var(--bg-secondary)`, `var(--bg-surface)`, `var(--bg-paper)`
   - Typography: `var(--text-primary)`, `var(--text-secondary)`, `var(--text-muted)`
   - Action Accent: `var(--accent-primary)`, `var(--accent-primary-hover)`
   - Dividers: `var(--border-subtle)`, `var(--border-medium)`
2. **Unregistered Typography:** Zero arbitrary font sizes (e.g., `text-[27px]`) or unmapped weights. All text must snap to the mathematical type scale (`--text-display` through `--text-mono`).
3. **Arbitrary Spacing:** Zero random margins or paddings (e.g., `mt-[37px]`). All spatial values must snap to the 8-point scale (`--space-1` through `--space-32`).
4. **Improvised UI Components:** Zero inventing new bulbous card borders, floating decorative badge animations, or unapproved glassmorphic blur cards.
5. **Structural Layout Deviations:** Zero altering the sequence of sections, collapsing the 5 pillars, or turning the asymmetric hero into a generic centered template.
6. **Placeholder Content:** Zero `Lorem Ipsum`, fake testimonials, or placeholder marketing slogans. All copy must strictly match `content-plan.md`.

---

## 4. Spec-First Change Management Procedure

If during coding an unforeseen technical obstacle or layout collision occurs:

```
TECHNICAL / DESIGN COLLISION ENCOUNTERED
                    │
                    ▼
          HALT IMPLEMENTATION
                    │
                    ▼
      UPDATE SPECIFICATION ARTIFACT
   (e.g., projects/alpha-starts-now/design-system.md)
                    │
                    ▼
         RE-VERIFY DESIGN LOCKS
                    │
                    ▼
          RESUME IMPLEMENTATION
```

**Never fix a design issue by hacking custom CSS in the component without updating the design system specification first.**

---

## 5. Pre-Implementation Verification Sign-Off

- [x] All 4 locks evaluate to `true` in `site-profile.json`.
- [x] Zero manufactured proof or fake statistics permitted.
- [x] Design token schema and CSS custom properties finalized.
- [x] Ready to authorize Phase 8 Build Execution in `alpha-starts-now-website`.
