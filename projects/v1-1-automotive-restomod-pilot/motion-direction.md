# MOTION DIRECTION SPECIFICATION: KREISLER & VOSS Motorenwerke

> **Date Created:** 2026-08-23  
> **Status:** APPROVED (Phase 12 — Motion Level Selection & Governance)  
> **Motion Level:** `MOTION_LEVEL_3` (Cinematic Scroll & Volumetric Staging)  

---

## 1. Selected Motion Level & Justification
- **Selected Level:** **`MOTION_LEVEL_3`**.
- **Strategic Justification:**
  - High-end coachbuilding and powertrain restomodding are inherently mechanical, spatial, and dynamic disciplines.
  - A scroll-driven canvas/SVG frame progression hero directly communicates the multi-stage transformation from raw CNC-machined components to the finished grand tourer.
  - Interactive component inspection and dual-layer blueprint switches require weighted mechanical easing (`cubic-bezier(0.16, 1, 0.3, 1)`) to feel substantial rather than flighty.

---

## 2. Motion Behaviors & Seven Pillars Justification

| Motion Behavior | Trigger | Seven Pillars Justification | Desktop Implementation | Mobile Fallback |
| :--- | :--- | :--- | :--- | :--- |
| **1. Scroll-Driven Hero Reveal** | Viewport Scroll (0%–100% of hero pinning) | **Storytelling & Brand Expression:** Illustrates the coachbuilding metamorphosis. | Pinned 200vh section with scrubbing canvas/SVG lighting pass and component assembly. | Static hero presentation with smooth entrance fade and touch scrubber. |
| **2. Category Filter Reflow** | Filter Tab Click | **Hierarchy & Orientation:** Clear feedback on active commission typology. | Staggered fade and `translateY(-8px to 0)` over 280ms. | Horizontal scroll snap with instant card reflow. |
| **3. Case Study Drawer Slide** | Project Card Click | **Orientation & Focus:** Isolates technical case study without page reload. | Smooth horizontal slide-in from right (`translateX: 100% to 0`) with `16px` backdrop blur. | Full-width slide-up modal with touch close. |
| **4. Dual-View Mode Switch** | Photo ↔ Blueprint Toggle | **Verification & Technical Rigor:** Immediate swap between aesthetic photography and engineering line schematics. | Crossfade opacity with 180ms ease. | Instantaneous crossfade. |
| **5. Material & Light Scrubber** | Component Swatch / Lighting Scrub | **Tactile Feedback:** Real-time reflection feedback on billet metal and saddle leather. | Real-time SVG/Canvas specular highlight sweep. | Direct specimen card select. |

---

## 3. Reduced Motion Compliance
- Under `@media (prefers-reduced-motion: reduce)`:
  - All scroll-driven pinning is disabled (`position: relative !important; height: auto !important;`).
  - Transition durations set to `0.001ms !important`.
  - Hero displays the final fully revealed grand tourer state immediately.
  - Zero loss of content, functionality, or commission access.

---

## 4. Specialist Requirement
- `motion.cinematic_specialist_required = true`.
- Hand-off governed via `cinematic-brief.md`.
