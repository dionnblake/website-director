# RIVE INTERACTIVE MOTION SPECIALIST GOVERNANCE PROTOCOL

> **Version:** 2.2.0  
> **Status:** Authoritative Runtime Architecture & Specification Standard  
> **Core Principle:** Use Rive when state-driven interactive vector motion communicates brand, product, or UI states fundamentally better than CSS, GSAP, video, or Three.js. Rive is NEVER a mandatory decoration layer.

---

## 1. System Invariants & Technology Boundaries

1. **Anti-Rive-Slop Rule:** Reject gratuitous vector noise (random bouncing blobs, endlessly waving cartoon mascots with no brand role, eye-following novelty gimmicks, fake "liquid" buttons, motion added simply because Rive exists). If an animation could be pasted across 20 unrelated SaaS products without losing meaning, `RIVE_DISTINCTIVENESS = FAIL`.
2. **Semantic Content Primacy:** Core data, labels, values, instructions, headlines, and conversion CTAs MUST exist in accessible semantic HTML/DOM. They must never be trapped exclusively inside Rive canvas pixels.
3. **No Sixth Owner Lock:** `[RIVE_IMPLEMENTATION_READY]` is a quality readiness check, NOT an owner lock. Exactly 5 owner locks remain immutable (`design_direction_locked`, `information_architecture_locked`, `content_structure_locked`, `design_system_locked`, `motion_direction_locked`).
4. **Boundary Separation:**
   - **CSS:** Owns basic hover, opacity, simple transform transitions, and micro icon states.
   - **GSAP:** Authoritative for page choreography, scroll-driven layout timelines, DOM sequencing, and viewport transitions.
   - **Three.js (V2.1):** Authoritative for genuine spatial 3D meshes, lighting rigs, PBR materials, and camera navigation.
   - **Asset Director (V2.0):** Authoritative for `.riv` art direction, vector design system coherence, brand authenticity, licensing, and provenance ledger.
   - **Rive Specialist (V2.2):** Authoritative for runtime loading, state machine wiring, inputs, data binding, view models, touch/pointer interaction, lifecycle disposal, and capability fallbacks.
5. **Universal Fallback Requirement:** Every Rive integration MUST define an instant, zero-CLS fallback (`STATIC_SVG`, `STATIC_IMAGE`, `HTML_COMPONENT`, or `CSS_STATE`) and a complete `prefers-reduced-motion` strategy.

---

## 2. Rive Capability Levels

| Level | Identifier | Description | Typical Use Cases | Justification Standard |
| :--- | :--- | :--- | :--- | :--- |
| **Level 0** | `0_NONE` | **No Rive Canvas.** Standard CSS / GSAP / static SVG. | Editorial, corporate SaaS, clean commerce, text-first journals. | Default state for most web builds. |
| **Level 1** | `1_MICRO` | **Small Interactive UI Motion.** Animated icon, stateful toggle, status badge, micro-indicator. | Audio toggle, network status badge, theme selector, dynamic indicator. | Low runtime footprint; non-essential visual polish. |
| **Level 2** | `2_COMPONENT` | **Substantial Interactive Component.** Multi-state gauge, interactive explainer, data-driven diagram. | Endurance readiness gauge, financial portfolio visualizer, process selector. | High functional value: state machine conveys complex multi-variable state. |
| **Level 3** | `3_SIGNATURE` | **Central Branded Feature / Narrative Graphic.** High-fidelity hero visual, branded interactive system. | Flagship hero explainer, signature interactive identity mark, flagship simulator. | Highest justification; requires explicit Creative Intent alignment and strict performance budgeting. |

---

## 3. Technology Selection & Justification Matrix

Before selecting Rive (`RIVE_REQUIRED = TRUE`), Website Director must evaluate:
1. **Multi-State Requirement:** Does the visual require multiple non-linear interactive states?
2. **State Machine Value:** Does user or programmatic input need to transition between states with designer-authored blending?
3. **Resolution Independence:** Does the graphic need continuous crisp vector rendering across high-DPR screens?
4. **Data Reactivity:** Does numerical or boolean data dynamically alter the visual form?
5. **Simplicity Test:** Can CSS transitions or a 3-line GSAP timeline achieve the same result with zero WASM overhead? (If yes, `RIVE_REQUIRED = FALSE`).
6. **Efficiency Test:** Is video more efficient for non-interactive linear playback? (If yes, choose Video).
7. **Dimensionality Test:** Does the subject require true spatial 3D depth and lighting? (If yes, choose Three.js).

---

## 4. Creative Ambition Calibration

- **`STANDARD`:** Default `RIVE_LEVEL = 0_NONE`. Level 1 evaluated only where functional clarity is meaningfully improved.
- **`PREMIUM`:** Evaluate Level 1 (Micro) or Level 2 (Component) for high-craft dashboard controls or interactive diagrams.
- **`SHOWCASE`:** Evaluate Level 2 or Level 3 (Signature) when the core concept centers on interactive vector motion. Rive is NOT mandatory.
- **`EXPERIMENTAL`:** Levels 1–3 evaluated with creative latitude, retaining strict accessibility and lifecycle cleanup.

---

## 5. Dependency Governance & Runtime Selection

1. **Stack-Appropriate Runtimes:**
   - **`RIVE_WEB`:** Vanilla JS, Astro, static HTML (`@rive-app/canvas` or `@rive-app/webgl2`).
   - **`RIVE_REACT`:** React, Next.js (`@rive-app/react-canvas` or `@rive-app/react-webgl2`).
2. **Project-Pinned Versioning:** Use the project's installed or pinned compatible dependency version (`RIVE_RUNTIME_VERSION`). Never copy ancient tutorial snippets or hardcode permanent version assumptions.
3. **WASM Preloading & Governance:** For production performance, host matching `.wasm` binaries locally or bundle via verified build tooling. Ensure runtime `.js` and `.wasm` versions match exactly.
4. **Third-Party Vendor Immutability (`THIRD_PARTY_RUNTIME_SOURCE_MUTATED = NO`):** Website Director configures, imports, bundles, initializes, wraps, and adapts application-side integrations. Website Director MUST NOT silently mutate or patch third-party vendor runtime artifacts. Any vendor modifications require an explicit fork and change-management record.

---

## 6. Asset & State Machine Governance

1. **Asset Identity & Provenance:** Every `.riv` asset must be recorded in `site-profile.json` and `asset-manifest.json` with:
   - `asset_id`, `source`, `owner`, `license`, `artboard`, `state_machine`, `file_size_bytes`, `status` (`PROTOTYPE_ONLY`, `PRODUCTION_READY`, `BLOCKED`).
2. **State Machine Architecture:**
   - Document state machine name, default state, state list, inputs (`BOOLEAN`, `NUMBER`, `TRIGGER`), and transitions.
   - Avoid transition spaghetti. Keep state machines modular and bounded.
3. **Data Binding & ViewModels:** Where modern Rive ViewModels or Data Binding are utilized, document properties, update direction, and bound semantic data sources. Synthetic data must be explicitly flagged (`SYNTHETIC_CERTIFICATION_DATA = TRUE`).

---

## 7. Interaction, Touch & Accessibility Rules

1. **No Hover-Only Critical Behavior:** Hover must never be the exclusive mechanism to access essential information. All interactive states must be accessible via tap/click, keyboard focus, or programmatic state buttons.
2. **Semantic DOM Mirroring:** Every numeric value, status label, and state description inside a Rive graphic MUST be mirrored in accessible semantic HTML elements outside the canvas.
3. **Reduced Motion (`prefers-reduced-motion: reduce`):**
   - Mandatory handling. Pause continuous idle loops, disable continuous tracking, and snap state machine transitions immediately without transitional tweening.
4. **Zero-CLS Fallback:** If WASM fails, canvas fails, or the `.riv` asset is blocked, an instant 2D fallback (SVG or semantic HTML component) must display in the exact reserved layout box.

---

## 8. Performance & Lifecycle Cleanup

1. **Performance Budgeting:**
   - Single `.riv` file size should ideally stay `< 200 KB`.
   - Bounded instance count (avoid running multiple uncoordinated Rive canvases on a single view).
2. **Visibility Throttling:** Rendering MUST pause when `document.hidden === true` or when the canvas is offscreen.
3. **Explicit Teardown:** Every Rive instance must be explicitly cleaned up on teardown (`riveInstance.cleanup()`, event listener removal, DOM detachment) to prevent memory leaks in Single Page Applications.

---

## 9. Rive Readiness Gate (`[RIVE_IMPLEMENTATION_READY]`)

Prior to building production Rive components, the readiness check evaluates:
- `rive.status = "implementation_ready"`
- `RIVE_JUSTIFICATION = PASS`
- `RIVE_LEVEL` declared (`0_NONE`, `1_MICRO`, `2_COMPONENT`, `3_SIGNATURE`)
- `RIVE_RUNTIME` declared and pinned
- `RIVE_ASSET_STATUS` verified (`PRODUCTION_READY` or licensed fixture)
- `STATE_MACHINE_MAP` documented
- `ACCESSIBILITY_ALTERNATIVE` mirrored in DOM
- `REDUCED_MOTION_POLICY` configured
- `FALLBACK_POLICY` verified
- `RESPONSIVE_POLICY` declared
- `CLEANUP_PLAN` verified

