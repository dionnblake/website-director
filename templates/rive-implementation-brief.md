# RIVE IMPLEMENTATION BRIEF: [RIVE_COMPONENT_ID]

> **Project:** [Project Name]  
> **Schema Version:** 2.2.0  
> **Governance:** RIVE-INTERACTIVE-MOTION-PROTOCOL.md  
> **Rive Level:** `0_NONE | 1_MICRO | 2_COMPONENT | 3_SIGNATURE`  
> **Runtime Stack:** `RIVE_WEB | RIVE_REACT`  
> **Readiness Status:** `not_evaluated | planning | prototype_ready | implementation_ready | blocked`

---

## 1. Rive Justification & Functional Purpose

- **Functional Role:** [Describe why state-driven vector animation communicates better than CSS/GSAP/Video/Three.js]
- **Anti-Rive-Slop Validation:** [Confirm absence of gratuitous mascots, bouncing blobs, or unmotivated eye-tracking]
- **Audience & Business Value:** [How this interaction advances comprehension, engagement, or conversion]

---

## 2. Asset & State Machine Architecture

- **Asset ID / Path:** `[assets/source/filename.riv | assets/web/filename.riv]`
- **Artboard Name:** `[Main / Default]`
- **State Machine Name:** `[State Machine Name]`
- **Inputs & Types:**
  - `[Input 1]`: `BOOLEAN | NUMBER | TRIGGER` — [Purpose & Default Value]
  - `[Input 2]`: `BOOLEAN | NUMBER | TRIGGER` — [Purpose & Default Value]
- **States & Transitions:**
  - `[State A]` -> `[State B]` via `[Input condition]`
  - Default State: `[State A]`
- **Data Binding / ViewModel (if applicable):**
  - Bound Properties: `[Property list]`
  - Semantic Source: `[Authoritative application state source]`

---

## 3. Interaction & Input Methods

- **Input Triggers:** `[Pointer Drag | Click/Tap | Hover | Keyboard Focus | Programmatic Data]`
- **Touch / Mobile Handling:** `[Explicit tap targets / Bounded drag / Simplified state machine]`
- **No Hover-Only Rule:** [Confirm all essential states are accessible via tap, click, or keyboard]

---

## 4. Accessibility, Fallback & Lifecycle Teardown

- **Semantic DOM Mirroring:** [List exact HTML elements outside canvas reflecting values, status, and instructions]
- **Reduced Motion Strategy (`prefers-reduced-motion: reduce`):** [Freeze idle animation, snap transitions, disable continuous tracking]
- **Capability Fallback Mode:** `[STATIC_SVG | STATIC_IMAGE | HTML_COMPONENT | CSS_STATE]`
- **Lifecycle Cleanup Hook:** `[window.disposeRiveComponent() | useEffect unmount cleanup]`

