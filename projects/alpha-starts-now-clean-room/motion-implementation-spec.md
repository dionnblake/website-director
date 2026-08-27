# MOTION DIRECTION & GSAP IMPLEMENTATION SPECIFICATION (LOCK 5)

## 1. Motion Strategy Overview
- **Status:** **`MOTION_DIRECTION_LOCKED`** (Engaged Lock 5)
- **Motion Level:** **Level 2 (Official GSAP Kinetic Experience)**
- **Kinetics Metaphor:** Heavy industrial machinery, precision watch escapements, instantaneous mechanical switches, zero floaty delays.

## 2. GSAP Implementation Architecture

### A. Core Physics & Easings
- Mechanical Snap Ease: `power3.out` (Duration: 0.35s to 0.5s)
- Micro-Telemetry Counter: `none` / stepped ticker for coordinate HUD numbers.
- Hover Inversions: Direct 0.15s crisp background/border color inversion (`#181A20` → `#22252E`, amber highlight).

### B. Choreographed Sequences
1. **Hero Entrance Timeline (`tlHero`):**
   - Headline letter stagger reveal: `y: 40, opacity: 0, stagger: 0.04, duration: 0.6, ease: "power3.out"`.
   - HUD telemetry box reveal: `scaleY: 0, transformOrigin: "top", duration: 0.4, ease: "power2.inOut"`.
   - Vitals counter increment: GSAP numeric tween from 0 to target metrics (94%, 4.2x, 180m, 100%).
2. **Discipline Calibration Engine Dynamic Recalibration:**
   - Active tab switch triggers instantaneous panel wipe: `opacity: 0, x: -15` → `opacity: 1, x: 0` with `duration: 0.25s`.
   - Dial gauge indicator rotation animated smoothly to the decade angle.
3. **ScrollTrigger Section Entrances:**
   - Coordinate badges (`// SEC_01`, `// PROTOCOL_02`) snap into view with a horizontal hairline scan line.
   - Arsenal spec sheets trigger staggered slide-up with `0.1s` interval.
4. **Reduced Motion Graceful Fallback (`prefers-reduced-motion: reduce`):**
   - Disables all transforms/staggers; instantly sets `opacity: 1` and reveals metrics statically.
