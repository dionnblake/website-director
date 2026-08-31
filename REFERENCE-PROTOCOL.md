# REFERENCE PROTOCOL: DECONSTRUCTION & INTERPRETATION

> **Version:** 1.1.0
> **Status:** Mandatory Operating Standard
> **Rule:** Never clone a website. Deconstruct underlying principles into an original design system.

---

## 0. Relationship to V1.1 Visual Research

This protocol governs deconstruction of the 1–3 references a *user* directly supplies at Discovery Stage 4. As of V1.1, Website Director may also arrive at this phase already holding `templates/research-synthesis.md`, produced by the Visual Research Director from *agent-discovered* references (industry landscape, Landbook, cross-industry, and deep-reconnaissance findings — see `VISUAL-RESEARCH-PROTOCOL.md`). When that synthesis exists, treat its recommended references and principles as additional candidate input to the same 12-Vector Deconstruction Matrix below — do not run a second, parallel deconstruction system. If the user also supplies their own references, both sources populate the same `templates/reference-analysis.md` matrix; agent-discovered deep-recon findings use `templates/reference-deconstruction.md` first and are then summarized into the relevant matrix rows here.

---

## 1. Operating Modes Overview

Website Director operates in one of two distinct visual direction pathways:

```
                  ┌────────────────────────────────────────┐
                  │          DISCOVERY STAGE 4             │
                  │        Visual Direction Path           │
                  └───────────────────┬────────────────────┘
                                      │
                 ┌────────────────────┴────────────────────┐
                 │                                         │
                 ▼                                         ▼
     ┌───────────────────────┐                 ┌───────────────────────┐
     │    ORIGINAL_MODE      │                 │    REFERENCE_MODE     │
     ├───────────────────────┤                 ├───────────────────────┤
     │ Archetype synthesis   │                 │ Deconstruction of 1-3 │
     │ from business context │                 │ external URL/image    │
     │ and industry dynamics │                 │ inspiration sources   │
     └───────────┬───────────┘                 └───────────┬───────────┘
                 │                                         │
                 │                                         ▼
                 │                             ┌───────────────────────┐
                 │                             │ EXTRACT 12 PRINCIPLES │
                 │                             │  (No Direct Copying)  │
                 │                             └───────────┬───────────┘
                 │                                         │
                 │                                         ▼
                 │                             ┌───────────────────────┐
                 │                             │ INTERPRET & SYNTHESIZE│
                 │                             └───────────┬───────────┘
                 │                                         │
                 └────────────────────┬────────────────────┘
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │ BESPOKE DESIGN SYSTEM &   │
                        │ IMPLEMENTATION SPEC       │
                        └───────────────────────────┘
```

---

## 2. REFERENCE_MODE Deconstruction Matrix

When a user provides external inspiration (URLs, screenshots, or live websites), Website Director executes an objective **12-Principle Visual Deconstruction**.

### The 12 Extraction Vectors:

| Vector | What to Analyze in the Reference | What to Extract (The Underlying Principle) |
| :--- | :--- | :--- |
| **1. Composition & Grid** | Column counts, asymmetry, horizontal margins, alignment anchors. | Mathematical grid structure, gutter-to-column ratio, content containment boundaries. |
| **2. Visual Hierarchy** | What catches the eye 1st, 2nd, 3rd? How is contrast achieved? | Typographic scale ratios, weight differentials, focal anchor techniques. |
| **3. Typographic Pairing** | Serif vs Sans vs Mono, weight choices, letter-spacing, line-height. | Typographic contrast strategy, historical classification harmony, tracking rules. |
| **4. Spacing Cadence** | Section padding, card gaps, whitespace volume, breathing room. | Base spacing unit (e.g., 4px, 8px, 12px), density index, margin inflation rates. |
| **5. Density & Economy** | Information density per viewport height. | Compact vs spacious information architecture, progressive disclosure patterns. |
| **6. Imagery & Art Direction** | Treatment, lighting, aspect ratios, color grading, framing. | Visual asset genre (monochrome studio, macro texture, architectural, 3D render). |
| **7. Color Architecture** | Background-to-surface contrast, saturation levels, accent frequency. | 60/30/10 tonal distribution, semantic color usage, background luminance values. |
| **8. Geometry & Line Work** | Corner radius values, border weights, dividers, bounding boxes. | Sharp (0px), subtle (4-8px), or organic (24px+); border contrast and presence. |
| **9. Navigation Architecture** | Floating pill nav, fixed full-width bar, sidebar, minimal drawer. | Header footprint, scrolling behavior (shrink, blur, sticky), menu hierarchy. |
| **10. Section Morphology** | Layout rhythms between sequential sections. | Alternation cadence (Split $\rightarrow$ Matrix $\rightarrow$ Text-heavy $\rightarrow$ Gallery $\rightarrow$ CTA). |
| **11. Motion & Physics** | Easing curves, duration, trigger thresholds, micro-interactions. | Motion philosophy (Instant/mechanical, smooth/cinematic, bouncy/spring). |
| **12. Brand Soul & Posture** | The unspoken psychological impression the site commands. | Tone of voice, authority level, emotional posture. |

---

## 3. The 4-Step Transformation Pipeline

```
REFERENCE(S) ──► EXTRACT PRINCIPLES ──► INTERPRET FOR BRAND ──► ORIGINAL DESIGN SYSTEM
```

### Step 1: Input Ingestion
Ingest 1 to 3 reference URLs or visual artifacts provided by the user.

### Step 2: Principle Extraction
Fill out `templates/reference-analysis.md`. Document the exact design mechanics without referencing proprietary brand assets of the reference.

### Step 3: Brand Interpretation
Cross-reference extracted principles with the client's actual industry, offerings, and brand posture established in `DISCOVERY-PROTOCOL.md`.
- *Example:* If the reference is an ultra-minimalist Swedish watchmaker with an editorial Didone serif, and the client is a high-performance database company, **interpret** the typography as a razor-sharp modern grotesque with monospace accents while maintaining the reference's exceptional spatial discipline and micro-contrast.

### Step 4: Generation of Unique Tokens
Generate an original, bespoke Design System specification (`templates/design-system.md`). The resulting site must be completely distinct in identity, imagery, copy, and layout details while capturing the level of polish and craft exhibited in the reference.

---

## 4. Anti-Cloning Rules

1. **Never replicate trademark layouts or brand assets:** Never copy logos, exact color hex triplets, specific custom icons, or copyrighted copy.
2. **Never duplicate distinctive signature illustrations or bespoke 3D assets:** Create custom visual metaphors tailored to the client's actual domain.
3. **The "Swap Test":** If the final design looks like a reskinned fork of the reference rather than an original creation inspired by its structural rigor, the specification fails QA.

---

## 4.1 Evidence and rights boundary

Reference inputs are research evidence, not production asset provenance.
Record the exact source URL, access date, reference purpose, transferable
pattern, and what must not be copied in the project evidence ledger. A
reference screenshot, logo, illustration, or composition cannot be promoted
into a production asset without independent origin and permitted-use evidence.
Claim language derived from a reference also requires its own EVIDENCE_REF.

## 5. ORIGINAL_MODE Workflow

When no references are provided:
1. Review `DISCOVERY-PROTOCOL.md` (Stages 1 through 3).
2. Consult `DESIGN-ARCHETYPES.md` to identify the best primary archetype (or 60/30/10 blend) matching the client's industry, audience, and emotional posture.
3. Map the chosen archetype directly into the comprehensive tokens defined in `DESIGN-SYSTEM-PROTOCOL.md`.
4. Output the complete direction in `templates/design-direction.md` and `templates/design-system.md`.
