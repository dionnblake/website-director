# MOTION DIRECTION SPECIFICATION: ALPHA STARTS NOW
## The 5 Morning Rituals (Direction C: The Dawn Vanguard Flagship)

> **Date Created:** 2026-08-27  
> **Status:** READY_FOR_GATE_5_LOCK (`locks.motion_direction_locked: true`)  
> **Selected Motion Level:** `MOTION_LEVEL_2` (Kinetic / Scrollytelling Choreography)  

---

## 1. Selected Motion Level & Rationale
- **Level:** `MOTION_LEVEL_2` (Kinetic & Scrollytelling Choreography)
- **Rationale:** The core narrative of Alpha Starts Now is the chronological mastery of the dawn (05:00 to 06:00+). Smooth, hardware-accelerated timeline transitions and ambient crest luminescence reinforce the gravitational discipline of the brand without decorative bloat.

---

## 2. Motion Manifesto
- **Hero Motion:** Ambient breathing glow on the official Wolf Crest (`animation: pulseGlow 4s infinite alternate ease-in-out`), with subtle staggered entrance for display typography.
- **Timeline Scrollytelling:** Central golden axis track with interactive hover states and progressive node illumination.
- **Interactive Feedback:** Solar gold button scale (`transform: scale(1.05)` with `box-shadow: 0 0 35px rgba(245, 158, 11, 0.6)`) and node elevation (`transform: translateY(-4px)`).
- **Reduced Motion Fallback:** Full zero-duration bypass under `@media (prefers-reduced-motion: reduce)` preserving full layout readability and instant visual state.

---

## 3. Rationale vs. The Six Motion Justifications
1. **Hierarchy:** Directs the eye instantly to the official Wolf Crest and hero value thesis.
2. **Orientation:** The vertical timeline track provides continuous spatial orientation throughout the 5 morning stages.
3. **Storytelling:** Chronological progression matches the actual waking sequence of a disciplined man.
4. **Feedback:** Micro-elevation and glow expansion confirm hover and focus interactions on ritual nodes and CTAs.
5. **Atmosphere:** Deep solar gradients and subtle pulse give the feeling of standing at dawn's horizon.
6. **Brand Expression:** Unflinching, calm, gravitational kinetics that convey self-mastery.

---

## 4. Technical Parameters & Performance
- **Transforms Used:** Strictly hardware-accelerated `transform` and `opacity` (zero layout-thrashing `top/left/width` animations).
- **Easing:** `cubic-bezier(0.16, 1, 0.3, 1)` (Cinematic ease-out).
- **Mobile Behavior:** Timeline simplifies to a clean left-track on screens `< 768px` with no horizontal overflow.
- **Reduced Motion Support:** All animations duration set to `0.01ms !important`.

---

## 5. Motion Lock Gate Record

```ini
GATE_5_NAME               = MOTION_DIRECTION
GATE_5_STATUS             = LOCKED_AND_FROZEN
SELECTED_MOTION_LEVEL     = MOTION_LEVEL_2
REDUCED_MOTION_VERIFIED   = TRUE
MOTION_DIRECTION_LOCKED   = TRUE
```
