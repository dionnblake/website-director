# REFERENCE DECONSTRUCTION SUITE: DEEP RECON TARGETS

> **Date Created:** 2026-08-23  
> **Status:** APPROVED  
> **Stage:** Visual Research Director — Step 5 (Deep Reconnaissance)  
> **Mode:** RESEARCH_ONLY_MODE (per `REFERENCE-RECON-PROTOCOL.md`)  
> **Rule:** Forensic reconnaissance, never reconstruction. 

---

# DECONSTRUCTION 1: Vincent Van Duysen Architects

## 1. Study Metadata
- **Reference:** Vincent Van Duysen Architects (Antwerp / Milan)
- **URL:** `https://vincentvanduysen.com`
- **Source Type:** `jcodesmore_deep_recon`
- **Access Date:** 2026-08-23
- **Purpose of Study:** Forensic analysis of archival layout discipline, quiet navigation, and minimal typographic scale.

## 2. Layout System
- **Grid:** 12-column asymmetric flexible grid with generous outer margins (48px desktop, 20px mobile).
- **Container Width:** Max-width 1680px with edge padding.
- **Section Sequence:** Full-bleed hero frame → Filterable project index → Curated case study monograph → Studio biography → Discrete footer.

## 3. Typography System
- **Type Relationships:** Custom grotesque sans (Univers variant) with subtle weights (Light 300 / Regular 400).
- **Tracking / Leading:** Heading tracking `0.05em` (expanded uppercase for labels), body line-height `1.6`.
- **Scale:** Restrained scale ratio (1.200 Minor Third): H1 32px, H2 24px, Body 15px, Meta 12px.

## 4. Spacing & Color
- **Spacing Rhythm:** Base unit 8px; section padding `96px–128px` desktop, `48px–64px` mobile.
- **Color Relationships:** Background #F7F5F2 (Warm Bone/Alabaster), Surface #EFECE6 (Limestone), Text Primary #1C1A17 (Deep Umber), Border #DDD9D0 (Fine Mortar).

## 5. Imagery & Section Morphology
- **Image Treatment:** Natural daylight photography, muted contrast, subtle warm cast, zero artificial saturation.
- **Aspect Ratios:** 16:10, 4:3, and vertical 3:4 for interior vignettes.

## 6. Navigation & Responsive Behavior
- **Navigation:** Floating minimalist header bar with blur backdrop (`backdrop-filter: blur(12px)`), logo left, clean category links right.
- **Responsive Transformation:** Desktop horizontal nav collapses to clean overlay drawer at `< 960px`.

## 7. Interaction & Motion
- **Interaction Model:** Quiet hover states with opacity transitions (1.0 to 0.75) and subtle image scaling (1.0 to 1.02 over 400ms).
- **Scroll Behavior:** Smooth scrolling with gentle reveal fades on section entry.
- **Easing:** `cubic-bezier(0.25, 1, 0.5, 1)`.

## 8. Quality Assessment
- **What Creates Perceived Quality:** Extreme spatial restraint and refusal to shout; the interface completely yields to the built architecture.
- **What Feels Generic:** Lack of interactive material details or architectural section drawings.

## 9. Transferability
- **Must Not Transfer:** Proprietary photos, Belgian bluestone case studies, specific logo wordmark.
- **Transferable Principles:** Calm background tone (#F8F6F0 family), restrained typographic scale, floating blurred header bar, generous margins.

---

# DECONSTRUCTION 2: Norm Architects

## 1. Study Metadata
- **Reference:** Norm Architects (Copenhagen)
- **URL:** `https://normcph.com`
- **Source Type:** `jcodesmore_deep_recon`
- **Access Date:** 2026-08-23
- **Purpose of Study:** Forensic analysis of tactile storytelling, multi-scale image grids, and subtle scroll reveals.

## 2. Layout System
- **Grid:** Asymmetrical editorial grid with offset image pairings (e.g. 7-col hero image alongside 5-col poetic text block).
- **Container Width:** Max-width 1560px.
- **Section Sequence:** Atmospheric hero → Editorial Manifesto → Multi-scale project matrix → Material tactile essay → Inquiries.

## 3. Typography System
- **Type Relationships:** Contemporary clean sans paired with editorial styling.
- **Tracking / Leading:** Headings `-0.02em`, body text generous `1.75` leading for effortless reading.
- **Scale:** 1.250 Major Third (Display 48px, H1 36px, H2 28px, Body 16px, Caption 13px).

## 4. Spacing & Color
- **Spacing Rhythm:** Base unit 8px; dynamic spacing `clamp(64px, 8vw, 140px)`.
- **Color Relationships:** Canvas #F4F1EA (Warm Chalk), Card #EAE5DC, Accent #8A6E4F (Warm Oak/Earth), Text #211F1D.

## 5. Imagery & Section Morphology
- **Image Treatment:** Atmospheric, high-tactility, macro textures (linen, oak grain, honed stone, morning shadows).
- **Section Morphology:** Alternating rhythmic blocks: full-bleed panorama → 2-up asymmetric pair → wide editorial pull-quote.

## 6. Interaction & Motion
- **Motion:** Motion Level 2: Soft image zoom parallax on scroll, smooth stagger reveals of grid elements (`duration: 350ms`).
- **State Changes:** Filterable work categories transition with smooth fade-in and translateY(-8px to 0).

## 7. Quality Assessment & Transferability
- **What Creates Perceived Quality:** The rhythm of reading feels like browsing an exquisite hardbound coffee table book.
- **Transferable Principles:** Asymmetric editorial section rhythm, tactile macro imagery pairing, smooth scroll stagger reveals.

---

# DECONSTRUCTION 3: Studio KO

## 1. Study Metadata
- **Reference:** Studio KO (Paris / Marrakech)
- **URL:** `https://www.studioko.fr`
- **Source Type:** `jcodesmore_deep_recon`
- **Access Date:** 2026-08-23
- **Purpose of Study:** Forensic analysis of monolithic mineral color palettes, raking light photography, and geographic project classification.

## 2. Layout System & Typography
- **Grid:** Monolithic full-bleed viewports with strict geometric alignment.
- **Typography:** High-contrast classical serif display headings paired with understated sans-serif geographic coordinates (Paris, Marrakech, London).
- **Color Palette:** Warm mineral sand, baked clay terracotta, raw plaster grey, deep umber text.

## 3. Interaction & Quality Assessment
- **Interaction Model:** Immersive project slider with smooth horizontal paging and elegant project title overlays.
- **Perceived Quality:** Deep cultural authenticity and tactile monolithic weight.
- **Transferable Principles:** High-contrast serif headlines for architectural statements; warm earthy mineral tones; celebrating regional stone and earth.

---

## 4. Synthesis & Transferability Protocol
- All findings from these 3 deep recon targets are strictly filtered through the **Seven Pillars of Justification**.
- Zero pixel copying, zero asset borrowing, zero layout cloning.
- Ready to feed `projects/v1-1-architecture-pilot/research-synthesis.md`.
