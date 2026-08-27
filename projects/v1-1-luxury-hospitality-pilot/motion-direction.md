# MOTION DIRECTION PROTOCOL — SÖLVIK FJORD RETREAT

> **Pilot Code:** `WD-V1.1-HOSP-001`  
> **Schema Version:** 1.1.0  
> **Lock 5:** `motion_direction_locked = true`  
> **Motion Classification:** `MOTION_LEVEL_3` (Atmospheric Fjord Parallax, Raking Hearth Glow, and Choreographed Pavilion Reveals)  

---

## 1. Motion Philosophy & Atmospheric Purpose
In luxury destination hospitality, motion must never feel aggressive, mechanical, or gamified. Motion serves three crucial sensorial functions:
1. **Atmospheric Immersion:** Simulating the gentle rolling of morning fjord mist, changing natural light across timber, and pulsing hearth ember warmth.
2. **Spatial Orientation:** Guiding the guest effortlessly from estate philosophy down to pavilion architecture, thermal wellness, dining, and reservation.
3. **Tactile Interaction:** Subtle hover lifts on pavilion cards, smooth tab switches between thermal rituals, and an unhurried drawer entry for "Plan Your Stay."

---

## 2. Motion Behaviors by Section

| Section | Trigger | Animation Behavior | Duration / Physics | Reduced Motion Fallback |
| :--- | :--- | :--- | :--- | :--- |
| **Hero Portal** | Page load & scroll | Ambient mist drift + subtle scale-in of architectural establishing shot + soft title reveal | 1200ms `cubic-bezier(0.16, 1, 0.3, 1)` | Instant opacity 1, zero drift |
| **Philosophy Metrics** | Scroll into view | Smooth counter increment + border illumination sweep | 800ms ease-out | Static display of numbers |
| **Pavilion Showcase** | Interactive click / tab | Cross-fade pavilion photography + smooth metric reflow | 400ms `cubic-bezier(0.2, 0, 0, 1)` | Immediate tab switch |
| **Thermal Ritual** | Tab selection | Atmospheric temperature transition + image fade | 350ms ease | Immediate display |
| **Plan Your Stay Drawer** | CTA click | Smooth slide-in from right with backdrop blur fade | 400ms `cubic-bezier(0.16, 1, 0.3, 1)` | Immediate modal display |

---

## 3. Motion Lock Sign-Off
`motion_direction_locked = true`
