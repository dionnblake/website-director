# MOTION DIRECTION SPECIFICATION: ALPHA STARTS NOW (V1.1)

> **Date Updated:** 2026-08-23  
> **Status:** LOCKED (`locks.motion_direction_locked: true`)  
> **Gate 5 Status:** CLEARED & LOCKED  
> **Stage:** Phase 8 — Motion / Cinematic Direction  
> **Design Authority:** Website Director V1.1  
> **Authoritative Location:** `projects/alpha-starts-now-v1-1/`  
> **Core Motion Philosophy:** *"Cinematic where emotion matters. Restrained where reading matters."*  

---

## 1. Selected Motion Level & Hierarchy Architecture

- **Selected System Level:** `MOTION_LEVEL_3 (Hybrid / Tiered)`
- **Architectural Hierarchy:**
  1. **HERO (Selective Level 3):** Primary cinematic event. Atmospheric, passive narrative progression introducing the brand with documentary realism.
  2. **DOCUMENTARY STORY BREAK (Level 1–2):** Measured visual break; subtle ambient depth.
  3. **EDITORIAL HOMEPAGE (Level 1–2):** Crisp, restrained micro-interactions (<150ms).
  4. **NAVIGATION / CONTROLS (Level 1):** Immediate tactile feedback.
  5. **LONG-FORM ARTICLES (Level 0 / Static):** 100% static reading experience with zero distracting animations, scroll hijacking, or spring physics.
  6. **MOBILE HERO (Reduced Level 2 Equivalent):** Lightweight, non-blocking media with direct scroll continuation.
  7. **PREFERS-REDUCED-MOTION (Level 0 Static Parity):** Single representative static hero frame with complete informational parity.

---

## 2. Hero Interaction Model & Storytelling Behavior

### 2.1 Passive Cinematic Progression (No Media Player UI)
- **Passive Progression:** The hero advances naturally as a cinematic background narrative without requiring visitor interaction.
- **No Complex Player Controls:** Zero scrubber widgets, zero forced step-by-step clicks, zero mandatory completion.
- **Unrestricted Scroll Continuity:** The visitor is free to scroll past the hero immediately at any point. Strictly **zero scroll locking or scroll hijacking**.
- **Optional Accessibility Control:** Subtle, minimal "Pause Motion" button available for users who prefer static presentation.

### 2.2 Hero Copy Stability
- The main headline (*"Where You Are Is Not Where You Have To Stay. Start Now."*) and lead dek remain completely static, stable, and readable throughout all background transitions.
- Strictly **zero text scrambling, typewriter effects, or kinetic headline cycling**.

---

## 3. Performance Contract & Loading Strategy

The cinematic hero operates strictly as a **progressive enhancement** and must never degrade core web vitals.

1. **Cumulative Layout Shift (CLS = 0):** Hero container dimensions are strictly reserved before any media loads.
2. **Largest Contentful Paint (LCP Optimization):** High-resolution first-frame poster image displays immediately with critical headline text rendered before video/secondary media initialize.
3. **No Heavy Mobile Downloads:** Mobile viewports receive specifically optimized, lightweight assets; desktop-scale assets are never downloaded unnecessarily on mobile.
4. **Zero Autoplay Audio:** The experience is engineered natively for silent documentary power.
5. **Fail-Safe Accessibility:** If media loading is delayed or blocked, the static first-frame poster and typography guarantee 100% comprehension.

---

## 4. Technical Motion Parameters & Semantic Timing Ranges

Motion timings are organized into restrained semantic ranges rather than rigid identical durations.

```css
/* --- Semantic Motion Duration Ranges --- */
--motion-micro-ui:       100ms - 180ms; /* Button hovers, toggle states, filter active indicators */
--motion-editorial:      180ms - 350ms; /* Drawer reveals, dropdowns, form validation messages */
--motion-cinematic:      400ms - 700ms; /* Background narrative transitions & atmospheric cross-fades */
--motion-ambient-drift:  8s - 12s;      /* Slow continuous background drift (used selectively) */

/* --- Easing Curves --- */
--ease-out-editorial:    cubic-bezier(0.16, 1, 0.3, 1); /* Measured deceleration */
--ease-in-out-cinematic: cubic-bezier(0.45, 0, 0.55, 1); /* Filmic background cross-fades */
```

---

## 5. Media-Format Strategy & Evaluation Policy

The Motion Direction specifies the **experience requirement** rather than prematurely locking a rigid technical format.

### Required Experience Standard:
- Mature cinematic documentary atmosphere.
- Smooth transitions with zero visual tearing.
- Fast perceived load time.
- Responsive mobile focal crops.
- Zero scroll hijacking.

*Implementation Evaluation (Phase 9):* The build engine may evaluate optimized HTML5 video (`AV1` / `WebM` / `MP4`), layered high-resolution photography, or hybrid web media based on real assets and measured browser performance.

---

## 6. Mobile & Reduced-Motion Specifications

### 6.1 Mobile Strategy (No Swipeable Card Carousel)
- Rejects generic swipeable card carousels.
- Delivers a streamlined, lightweight cinematic composition or single strong moving/still hero with center-top focal crop and bottom gradient scrim.
- Direct scroll continuation into the Core Thesis and 5 Pillars with zero performance lag.

### 6.2 `prefers-reduced-motion` Static Parity
- When `prefers-reduced-motion: reduce` is detected:
  - All automatic video playback, scaling, and opacity transitions are disabled.
  - Displays the strongest representative static hero photograph with the identical headline, dek, and CTA.
  - All interactive UI states become instantaneous (0ms).
  - 100% complete informational parity with zero replacement widget bloat.

---

## 7. Cinematic Specialist & Asset Status

- **Cinematic Specialist Protocol:** `VALIDATED`
- **Specialist Runtime Invocation:** `PENDING RUNTIME AVAILABILITY`
- **Asset Boundary Policy:** No paid media-generation API calls are authorized without explicit prior owner authorization (`OWNER_COST_AUTHORIZATION_REQUIRED`).
- **Resilience Standard:** If external specialist invocation is unavailable during implementation, the site will be built using the strongest supported web-native media techniques without blocking release.

---

## 8. Motion Lock Declaration

- [x] §1 Names explicit level: `MOTION_LEVEL_3 (Hybrid / Tiered)`.
- [x] Passive hero storytelling established (no video player/scrubber UI clutter).
- [x] 5 beats codified as invisible art-direction structure.
- [x] Performance contract specified (reserved dimensions, poster LCP, zero CLS, zero autoplay audio).
- [x] Semantic timing ranges established (100–180ms UI / 400–700ms cinematic).
- [x] Mobile and reduced-motion static parity codified.
- [x] Specialist and paid media boundaries recorded truthfully.
- [x] **`locks.motion_direction_locked: true`** — Gate 5 officially cleared and locked.
