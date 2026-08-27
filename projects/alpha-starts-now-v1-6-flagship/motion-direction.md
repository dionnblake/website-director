# MOTION DIRECTION & GSAP SPECIFICATION: CINEMATIC MIDNIGHT ALPHA (LOCK 5)

## 1. Motion Strategy Overview
- **Status:** **`MOTION_DIRECTION_LOCKED`** (Enhanced Motion Polish Pass Complete)
- **Motion Level:** **Level 2 (GSAP Kinetic Experience — Cinematic Moderate)**
- **Kinetics Metaphor:** Controlled energetic authority, atmospheric volumetric light, mechanical snap, interactive category filtering, and tactical telemetry.

## 2. Implemented Choreographed Sequences
1. **Hero Word-by-Word Choreography:**
   - Word staggered reveal: `DISCIPLINE` → `BUILDS` → `THE MAN.` (`stagger: 0.08s, ease: "power3.out"`).
   - Numeric counters: Smooth interpolation from 0 to target metrics (94%, 4.2x, 180m, SOVEREIGN PRIME).
2. **Signature Motion Element ("THE ALPHA SHIFT"):**
   - Precision laser scanline dividers (`.laser-scanline`) sweep across section entries on ScrollTrigger.
3. **Arsenal Interactive Experience (`#sec-arsenal`):**
   - Category Filter Bar: `ALL`, `BIOMETRICS & GPS`, `AXIAL IRON`, `HOROLOGY`, `THERMAL SLEEP` with smooth GSAP autoAlpha / scale filtering.
   - Utility Meter Gauges: Animated tactical rating bars (`9.9 / 10`, `9.8 / 10`) fill dynamically on viewport entry.
   - 3D Pointer Tilt: Subtle desktop mousemove tilt with `gsap.quickTo`.
4. **7-Day Reset Interactive Dossier (`#sec-reset`):**
   - Interactive chapter switcher revealing dynamic protocol previews for Days 01–07.
5. **Scroll-Aware Navigation HUD:**
   - Glassmorphism navbar contraction and active-section tracking indicator.
6. **Full `prefers-reduced-motion: reduce` graceful degradation.**
