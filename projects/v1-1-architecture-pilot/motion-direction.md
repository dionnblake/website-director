# MOTION DIRECTION SPECIFICATION: VALENTIN & HESSE Architects

> **Date Created:** 2026-08-23  
> **Status:** LOCKED (`locks.motion_direction_locked: true`)  
> **Stage:** Phase 8 — Motion / Cinematic Direction (after `DESIGN_SYSTEM_LOCKED`)  
> **Rule:** Every motion behavior must serve at least one of the Six Motion Justifications, or it is removed.

---

## 1. Selected Motion Level
- **Level:** `MOTION_LEVEL_2` — Curated Spatial & Storytelling Motion (per `MOTION-DIRECTION-PROTOCOL.md` §2).
- **Rationale:** High-end architecture requires a digital presence that feels physically three-dimensional, grounded, and unhurried. Motion Level 2 provides:
  1. Subtle image reveal masks that mimic the experience of natural daylight illuminating an interior volume.
  2. Gentle zoom parallax on scroll (1.0 to 1.04) that establishes depth of field without causing motion sickness.
  3. Seamless slide-in Case Study Drawers and Dual-View (Photo $\leftrightarrow$ Blueprint CAD) transitions.
  4. Tactile, instantaneous material specimen switching with smooth illumination cross-fading.
- **Research Input:** Grounded in findings from `research-synthesis.md` §7 and `reference-deconstruction.md` (Norm Architects & Van Duysen motion analysis).

---

## 2. Motion Manifesto
- **Hero Behavior:** Atmospheric, slow-moving spatial anchor with soft upward fade-in of the manifesto typography and subtle downward reveal of the atelier coordinates.
- **Scroll Behavior:** Progressive viewport reveal using CSS IntersectionObserver and subtle translateY(24px to 0) with `--ease-spatial` curve.
- **Section-Transition Philosophy:** Generous vertical rhythm; sections do not collide abruptly, but breathe into view.
- **Hover Behavior:** Tactile feedback on project cards (subtle 2% image scale + caption contrast elevation) and interactive button underline slides (`transform: scaleX(0)` to `scaleX(1)`).
- **Selected Advanced Modules:**
  - `Module A: Dual-View Architectural Flipper` (Smooth cross-fade between finished spatial photography and wireframe CAD section plans).
  - `Module B: Tactile Material Specimen Explorer` (Interactive stone, timber, and metal tactile switcher with live ambient light simulation).
  - `Module C: Case Study Modal Drawer` (Smooth right-side slide drawer with backdrop blur).

---

## 3. Rationale vs. the Six Motion Justifications
1. **Hierarchy:** Soft stagger reveals guide the eye from the monolithic project photograph down to the architectural metadata (typology, location, square meters).
2. **Orientation:** The smooth sliding Case Study Drawer preserves the visitor's location in the portfolio grid without causing disruptive full-page navigation.
3. **Storytelling:** Dual-view cross-fading tells the complete story of a building—from raw structural CAD geometry to final sunlit timber and stone.
4. **Feedback:** Clear, crisp tactile feedback on material specimen selection, tab filtering, and consultation form steps confirms user actions instantly.
5. **Atmosphere:** Slow, deliberate easing (`cubic-bezier(0.25, 1, 0.5, 1)`) creates a meditative European atelier atmosphere.
6. **Brand Expression:** Rejects the frenetic, jittery animations of tech websites in favor of timeless architectural permanence.

---

## 4. Technical Parameters
- **Easing / Durations:**
  - Micro-interactions (hover, focus): `180ms var(--ease-out-smooth)`
  - Standard transitions (tabs, filters, forms): `320ms var(--ease-spatial)`
  - Spatial transitions (drawer, image reveals): `500ms var(--ease-spatial)`
- **Mobile Reduction:**
  - Parallax scales disabled on mobile viewports ($< 768\text{px}$) to conserve battery and avoid GPU stutter.
  - Case study drawer adapts to full-screen vertical modal.
- **Reduced-Motion Behavior:**
  - When `@media (prefers-reduced-motion: reduce)` is active, all opacity fades, translations, and scaling effects are replaced with instantaneous state changes (`0.001ms`).
- **Performance Constraints:**
  - 60fps GPU-accelerated rendering utilizing `transform` and `opacity` exclusively.
  - Zero layout thrashing (`will-change: transform` applied only during active transitions).

---

## 5. Cinematic Specialist
- **Specialist Required:** No (Pure CSS3 & performant Vanilla JS state transitions fulfill all Motion Level 2 requirements without external heavy 3D WebGL runtime dependencies or paid asset generations).
- **`cinematic-brief.md` Status:** COMPLETE (Documented in `cinematic-brief.md` for architectural governance).

---

## 6. Motion Lock Declaration
- [x] §1 "Selected Motion Level" explicitly set to `MOTION_LEVEL_2`.
- [x] Every motion behavior strictly justified against the Six Motion Justifications.
- [x] All easing/duration values strictly resolve to design system tokens.
- [x] Full `prefers-reduced-motion` and mobile fallbacks verified.
- [x] **`locks.motion_direction_locked = true` (Lock 5 engaged)**.
