# INFORMATION ARCHITECTURE SPECIFICATION: VALENTIN & HESSE Architects

> **Date Created:** 2026-08-23  
> **Status:** LOCKED (`INFORMATION_ARCHITECTURE_LOCKED: true`)  
> **Rule:** Architecture follows commercial psychology, not generic templates.

---

## 1. Visitor Psychology & Conversion Funnel

```
VISITOR ARRIVAL (Affluent Homeowner / Art Collector / Institutional Patron)
      │
      ▼
UNDERSTAND: "Who are Valentin & Hesse, what is their architectural philosophy, and what caliber of space do they create?"
      │ (Achieved via Monolithic Hero & Atelier Manifesto)
      ▼
BELIEVE & EXPERIENCE: "Is their built work undeniably authentic, structurally permanent, and materially exquisite?"
      │ (Achieved via Curated Selected Works Matrix & Interactive Case Study Blueprints)
      ▼
EVALUATE: "How do they work with stone, timber, and light? What is their pedagogical pedigree and process?"
      │ (Achieved via Interactive Material Specimen Laboratory & Studio Founders Pedigree)
      ▼
VERIFY: "What is their track record across alpine, lakeside, and urban typologies?"
      │ (Achieved via Complete Tabular Project Index & Commission Archive)
      ▼
CONVERT: "Initiate a private, confidential spatial briefing for our upcoming commission."
      │ (Achieved via Private Consultation Suite & Direct Atelier Dispatch)
```

---

## 2. Page Footprint & Navigation Architecture

| Experience Component | Identifier | Cognitive Purpose | Primary Interaction |
| :--- | :--- | :--- | :--- |
| **Floating Atelier Bar** | `#atelier-nav` | Persistent wayfinding, studio locations, and inquiry trigger | Smooth anchor scrolling & modal trigger |
| **Monolithic Spatial Hero** | `#hero` | Volumetric atmosphere & core manifesto | Instant comprehension & ambient scroll down |
| **Selected Works Matrix** | `#works` | Core architectural portfolio with typology filtering | Filter by Alpine / Villa / Urban / Heritage; Open Case Study |
| **Case Study Modal Drawer** | `#case-study-drawer` | Dual-view deep dive (Finished Photography + Architectural Plans + Material Specs) | Toggle between Photo and Blueprint view; Inspect details |
| **Material & Light Laboratory** | `#materials` | Interactive sensory exploration of stone, wood, and metal | Switch specimen (Quartzite, Travertine, Larch, Bronze) |
| **Studio & Founders** | `#studio` | ETH Zurich & Politecnico di Milano credentials and philosophy | Read architectural essay & leadership bio |
| **Project Commission Archive** | `#archive` | Comprehensive tabular proof of completed commissions | Tabular inspection by year, location, and scale |
| **Private Consultation Suite** | `#inquiry` | High-touch, confidential spatial consultation scheduler | Submit project parameters & request consultation |
| **Colophon & Atelier Footer** | `#colophon` | Permanent atelier addresses (Zurich, Engadin, Milan) & imprint | Geographic verification & direct correspondence |

---

## 3. Section Morphology & Layout Rhythm

To prevent visual fatigue, consecutive sections strictly alternate layout morphology, column density, and visual weight.

```
┌────────────────────────────────────────────────────────────────────────┐
│ SECTION 1: MONOLITHIC SPATIAL HERO                                     │
│ Morphology: Full-bleed architectural landscape with asymmetric bottom  │
│ text anchor (Left: High-contrast serif manifesto / Right: Locations)   │
│ Density: Spacious & atmospheric.                                       │
├────────────────────────────────────────────────────────────────────────┤
│ SECTION 2: CURATED SELECTED WORKS MATRIX                               │
│ Morphology: Asymmetric 12-column staggered grid (alternating 7/5 & 5/7 │
│ column photo spans with integrated architectural metadata)             │
│ Density: High visual impact, generous gutter spacing.                  │
├────────────────────────────────────────────────────────────────────────┤
│ SECTION 3: TACTILE MATERIAL & LIGHT LABORATORY                         │
│ Morphology: 2-column interactive specimen console (Left: Interactive   │
│ tactile swatch selectors / Right: Live material specimen display &     │
│ architectural light absorption metrics)                                │
│ Density: High-engagement interactive craft.                            │
├────────────────────────────────────────────────────────────────────────┤
│ SECTION 4: STUDIO ESSAY & FOUNDERS PEDIGREE                            │
│ Morphology: 3-column asymmetric layout (Col 1: Philosophical Thesis /  │
│ Col 2-3: Founder profiles, ETH/Politecnico credentials, and craft team)│
│ Density: Literary editorial reading rhythm.                            │
├────────────────────────────────────────────────────────────────────────┤
│ SECTION 5: COMPLETE COMMISSION ARCHIVE & METADATA                      │
│ Morphology: Structured tabular index with hairline dividers            │
│ Density: High-density typographic rigor.                               │
├────────────────────────────────────────────────────────────────────────┤
│ SECTION 6: PRIVATE CONSULTATION SUITE (CONVERSION FINALE)              │
│ Morphology: Bounded limestone container with structured 2-step inquiry │
│ consultation form (Typology, Location, Approximate Timeline, Notes)    │
│ Density: Low-friction, confidential atelier intake.                    │
├────────────────────────────────────────────────────────────────────────┤
│ SECTION 7: ATELIER COLOPHON & FOOTER                                   │
│ Morphology: 4-column structured address & legal imprint matrix         │
│ Density: Grounded Swiss-Italian coordinates.                           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Section Morphology Review & Anti-Repetition Audit
- [x] No two consecutive sections use the same grid geometry.
- [x] Visual weight rhythmically alternates between atmospheric full-bleed imagery, asymmetric project pairs, interactive consoles, editorial typography, and structured tabular data.
- [x] Mobile reflow defined for each section with uncompromised typography and touch targets.
- [x] Every section directly serves the visitor cognitive journey.
- [x] **`locks.information_architecture_locked = true` (Lock 2 engaged)**.
