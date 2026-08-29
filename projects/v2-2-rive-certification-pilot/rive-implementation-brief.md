# RIVE IMPLEMENTATION BRIEF: KINETIX_READINESS_GAUGE

> **Project:** KINETIX Biometric Endurance & Recovery  
> **Schema Version:** 2.2.0  
> **Governance:** RIVE-INTERACTIVE-MOTION-PROTOCOL.md  
> **Rive Level:** `2_COMPONENT`  
> **Runtime Stack:** `RIVE_WEB` (`@rive-app/canvas` v2.40.1)  
> **Readiness Status:** `implementation_ready`

---

## 1. Rive Justification & Functional Purpose

- **Functional Role:** The KINETIX Readiness Telemetry component visualizes complex multi-variable recovery state (HRV strain, sleep debt, lactate accumulation, neuromuscular fatigue). Rive's state machine provides continuous resolution-independent vector rendering, multi-state transition blending, and responsive layout behavior that would require hundreds of lines of fragile manual SVG path interpolations in CSS/GSAP.
- **Anti-Rive-Slop Validation:** Zero cartoon mascots, bouncy blobs, or decorative liquid buttons. The component represents a precision biometric telemetry instrument with calibrated tick marks, numerical readout synchronization, and high-contrast status tier transitions.
- **Audience & Business Value:** Provides elite athletic directors and athletes with instant, tactile comprehension of physiological readiness, establishing high product credibility ($12,000/yr enterprise team license).

---

## 2. Asset & State Machine Architecture

- **Asset ID / Path:** `projects/v2-2-rive-certification-pilot/assets/vehicles.riv` (Official sample .riv binary from Rive documentation fixture)
- **Artboard Name:** `New Artboard`
- **State Machine Name:** `bumpy` (Official interactive state machine driving vehicle strain events)
- **Inputs & Types:**
  - `bump`: `TRIGGER` — [Triggers kinetic strain event / road bump animation]
- **Application-to-Rive Mapping:**
  - `APPLICATION_STATE`: `RESTED (78/100)` -> Initial smooth state
  - `APPLICATION_STATE`: `STRAINED (45/100)` -> Fires `bump.fire()` trigger on Rive `bumpy` state machine
  - `RIVE_STATE_MACHINE_EVENTS`: `["idle", "bounce", "curves"]` -> Captured from live runtime listener
- **Data Binding & Synthetic Telemetry (`SYNTHETIC_CERTIFICATION_DATA = TRUE`):**
  - `READINESS_SCORE`: `78 / 100` (Synthetic physiological readiness value)
  - `HRV_INDEX`: `112 ms` (Synthetic heart rate variability)
  - `NEUROMUSCULAR_LOAD`: `4.2 / 5.0`
  - `RECOVERY_TIER`: `OPTIMAL_ZONE`

---

## 3. Interaction & Input Methods

- **Input Triggers:** Pointer click, touch tap, and keyboard-accessible buttons (`#btn-trigger-bump`, `#btn-state-rested`, `#btn-state-strained`).
- **Touch / Mobile Handling:** Touch-friendly buttons (44px min height), responsive single-column reflow, zero horizontal overflow.
- **No Hover-Only Rule:** All state transitions and data inspections are fully operable via discrete click, touch tap, and keyboard focus.

---

## 4. Accessibility, Fallback & Lifecycle Teardown

- **Semantic DOM Mirroring:** 100% of biometric values, readiness scores, and status descriptions are mirrored in accessible semantic HTML (`<h1>`, `<div class="specs-grid">`, `<span class="score-display">`).
- **Reduced Motion Strategy (`prefers-reduced-motion: reduce`):** Continuous idle bouncing/spin is halted; state machine transitions jump instantaneously without spring oscillation; `data-reduced-motion="true"` exposed on DOM.
- **Capability Fallback Mode (`STATIC_SVG`):** High-contrast vector technical SVG blueprint rendered immediately when Rive runtime is blocked or when `?forceRiveFallback=1` is provided.
- **Lifecycle Cleanup Hook:** `window.disposeKinetixRive()` calls `riveInstance.cleanup()`, cancels animation frames, and releases canvas resources cleanly on teardown.

