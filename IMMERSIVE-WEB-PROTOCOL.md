# IMMERSIVE WEB & THREE.JS SPECIALIST GOVERNANCE PROTOCOL

> **Version:** 2.1.0  
> **Status:** Authoritative Runtime Architecture & Specification Standard  
> **Core Principle:** 3D exists exclusively because it communicates the brand, product, physical environment, or narrative with superior spatial clarity. 3D NEVER exists simply because the toolchain knows Three.js.

---

## 1. Governance & System Invariants

1. **Anti-Demo-Slop Rule:** Reject generic 3D tropes (random floating glass toruses, unmotivated neon grid floors, glowing orb particles, chrome spheres on dark backdrops) unless grounded in authentic subject physics. If a 3D scene could be copied across 20 unrelated agency portfolios, `IMMERSIVE_DISTINCTIVENESS = FAIL`.
2. **Semantic Content Primacy:** Primary headlines (H1), core value propositions, navigation, conversion CTAs, and essential product specifications MUST remain in accessible semantic HTML/DOM. They must never be trapped exclusively inside WebGL canvas pixels.
3. **No Sixth Owner Lock:** `[IMMERSIVE_IMPLEMENTATION_READY]` is a quality readiness check, NOT an owner lock. Exactly 5 owner locks remain immutable (`design_direction_locked`, `information_architecture_locked`, `content_structure_locked`, `design_system_locked`, `motion_direction_locked`).
4. **Boundary with Asset Director (V2.0):**
   - **Asset Director V2.0 Owns:** 3D model art direction, provenance, licensing, visual quality, texture authenticity, and asset files in `assets/source/` and `assets/web/`.
   - **Immersive Specialist V2.1 Owns:** Runtime scene graph, Three.js/R3F rendering, lighting setups, camera choreography, interaction physics, custom GLSL shaders, scroll-sync, resource disposal, and capability fallbacks.
5. **Universal Fallback Requirement:** Every WebGL experience MUST have an operational 2D fallback (`WEBGL_FALLBACK = READY`) and a complete `prefers-reduced-motion` strategy (`REDUCED_MOTION_3D_POLICY = READY`).

---

## 2. Immersive Capability Levels

Immersive 3D is never a binary toggle. Website Director classifies immersive work into four deliberate tiers:

| Level | Identifier | Description | Typical Use Cases | Justification Standard |
| :--- | :--- | :--- | :--- | :--- |
| **Level 0** | `0_NONE` | **No WebGL / 3D Canvas.** Standard HTML/CSS/GSAP/media. | Editorial, corporate SaaS, clean commerce, text-first journals. | Default state for most web builds. |
| **Level 1** | `1_ENHANCEMENT` | **Bounded Subtle 3D Element.** Micro-depth, subtle object tilt, material shimmer, ambient depth particles. | Product card 3D tilt, subtle badge depth, mechanical indicator. | Low performance cost; site 100% usable without it. |
| **Level 2** | `2_FEATURE` | **Significant Interactive 3D Component.** Interactive product viewer, exploded assembly, material configurator. | Mechanical assemblies, architectural sections, scientific instruments. | High spatial value: user gains genuine comprehension by rotating/exploding. |
| **Level 3** | `3_CENTERPIECE` | **Central Immersive World / Narrative.** Spatial hero narrative, scroll-driven 3D journey, cinematic 3D staging. | Flagship luxury showcases, interactive spatial journeys, immersive brand reveals. | Highest justification; requires rigorous performance budgets and mobile fallbacks. |

---

## 3. The Immersive Activation Decision Framework

Before any 3D architecture is approved, Website Director must evaluate the 10-Point Justification Matrix:

1. **Spatial Clarity:** Does the visitor understand the subject fundamentally better in 3D than in high-resolution photography/video?
2. **Exploded / Internal Visibility:** Does the subject possess internal mechanical/architectural complexity that 2D cannot convey?
3. **Material Tactility:** Does interactive lighting reveal authentic material properties (brushed titanium, refractive crystal, woven carbon)?
4. **Narrative Value:** Does the 3D environment tell the brand story rather than act as background decoration?
5. **Audience Value:** Does the target decision-maker value tactile inspection over quick transactional checkout?
6. **Performance Budget:** Can the target frame rate (60 FPS desktop, stable 30+ FPS mobile) be guaranteed on representative hardware?
7. **Mobile Dignity:** Does the mobile viewport receive an intentional, touch-safe composition rather than an unmanageable miniature desktop scene?
8. **Reduced Motion:** Does the experience retain full informational integrity when all camera and object motion is frozen?
9. **Semantic Independence:** Can a screen reader or search engine index 100% of the core content if WebGL is disabled?
10. **Anti-Slop Check:** Is the visual treatment completely free of generic demo tropes?

*Rule:* If the primary motivation is "It looks cool" or "We want to show off WebGL", `IMMERSIVE_APPROVAL = FAIL` and `IMMERSIVE_LEVEL` is set to `0_NONE`.

---

## 4. Creative Ambition Calibration

- **`STANDARD`:** Default `IMMERSIVE_LEVEL = 0_NONE`. 3D permitted only for businesses with mandatory spatial configurator requirements.
- **`PREMIUM`:** Evaluate Level 1 (Enhancement) or Level 2 (Feature) where product complexity warrants it.
- **`SHOWCASE`:** Immersive capability is evaluated against the 10-Point Matrix. It is NOT mandatory. An editorial showcase may proudly choose Level 0.
- **`EXPERIMENTAL`:** Levels 1–3 evaluated with artistic latitude, but accessibility, performance, and cleanup invariants remain mandatory.

---

## 5. Technical Stack & Implementation Engines

The Immersive Specialist selects the engine that strictly matches the application stack:

```
┌────────────────────────────────────────────────────────┐
│               STACK SELECTION DECISION                 │
├──────────────────────────┬─────────────────────────────┤
│ Vanilla JS / Astro / MPA │ THREE_JS_VANILLA            │
│ React / Next.js SPA      │ REACT_THREE_FIBER (R3F)     │
│ Complex R3F Helpers      │ DREI (Used selectively)     │
└──────────────────────────┴─────────────────────────────┘
```

---

## 6. Scene Graph Architecture & Separation of Concerns

Three.js code must maintain clear modular separation across distinct concerns:

1. **`SceneRoot` / Canvas Container:** Manages DOM canvas mounting, WebGL renderer initialization, and DPR bounds.
2. **`CameraManager`:** Governs camera projection (Perspective/Orthographic), position, FOV, and art-directed view boundaries.
3. **`LightingRig`:** Configures key, fill, rim, and environment/HDRI maps matching the locked brand lighting language.
4. **`SubjectManager`:** Loads, instantiates, and positions primary 3D models/procedural meshes.
5. **`InteractionController`:** Bounded pointer parallax, touch drag, raycast hotspots, and hover physics.
6. **`MotionCoordinator`:** Bridges GSAP / ScrollTrigger with Three.js object transforms, camera timelines, and shader uniforms.
7. **`PostProcessingPipeline`:** Optional, restrained tone mapping, subtle bloom, and depth-of-field (disabled on mobile).
8. **`FallbackManager`:** Renders high-fidelity 2D image/SVG when WebGL is unsupported or disabled.
9. **`LifecycleManager`:** Manages resource disposal (`geometry.dispose()`, `material.dispose()`, `texture.dispose()`, `renderer.dispose()`) and event unbinding.

---

## 7. Camera Direction & Framing Taxonomy

Free-flying, unconstrained `OrbitControls` are strictly prohibited on production websites unless explicitly required for a 360° inspection tool. Camera movement must be art-directed:

- `STATIC_PRODUCT`: Fixed viewpoint with subtle mouse/gyro parallax (±5°).
- `CONSTRAINED_INSPECTION`: Bounded orbital arc with strict polar/azimuth angle clamps and damping inertia.
- `SCROLL_DOLLY`: Camera moves along Z/Y axis strictly synchronized to scroll progress.
- `FOCUS_TRANSITION`: Smooth GSAP camera transition between distinct mechanical component viewpoints upon user selection.
- `CINEMATIC_PATH`: Scripted camera fly-through triggered by narrative section scroll triggers.

---

## 8. Performance Budget & Device Pixel Ratio (DPR) Policy

Rendering at raw device pixel ratios (e.g., DPR 3.0 on retina phones) destroys mobile fill-rate and battery life. Bounded DPR is mandatory:

```
┌────────────────────────────────────────────────────────┐
│               PERFORMANCE BUDGET TIERS                 │
├────────────────────────┬───────────────┬───────────────┤
│ Metric                 │ Desktop       │ Mobile        │
├────────────────────────┼───────────────┼───────────────┤
│ Max DPR                │ 2.0           │ 1.5           │
│ Target Frame Rate      │ 60 FPS        │ 30 - 60 FPS   │
│ Draw Calls (Max)       │ <= 50         │ <= 25         │
│ Triangle Count (Max)   │ <= 150,000    │ <= 50,000     │
│ Texture Memory (Max)   │ <= 64 MB      │ <= 24 MB      │
│ Initial 3D Payload     │ <= 2.5 MB     │ <= 1.0 MB     │
└────────────────────────┴───────────────┴───────────────┘
```

---

## 9. Responsive 3D Art Direction & Mobile Simplification Policy

3D scenes must not merely shrink naively on mobile screens. Every Level 2/3 project must declare `MOBILE_3D_POLICY`:

- `FULL`: Same 3D scene with adjusted mobile camera distance, FOV, and bounded DPR.
- `SIMPLIFIED`: Lower-polygon mesh, disabled post-processing, simplified lighting, baked shadows.
- `STATIC_RENDER`: 3D canvas replaced with high-resolution pre-rendered WebP/AVIF keyframe on mobile viewports (< 768px).
- `DISABLED`: 3D omitted entirely on mobile, presenting structured semantic product specifications.

---

## 10. WebGL Failure & Fallback Governance

If WebGL initialization fails (hardware disabled, context creation error, blacklisted GPU, or test override `?forceWebGLFallback=1`):
1. The canvas container is hidden gracefully.
2. A high-fidelity 2D fallback graphic/image is rendered instantly.
3. Zero layout shifts (CLS), zero broken typography, and zero infinite loading spinners.
4. All semantic HTML headlines, copy, and CTAs remain 100% visible and interactive.

---

## 11. Reduced-Motion Compliance (`prefers-reduced-motion`)

When `(prefers-reduced-motion: reduce)` is detected:
- Continuous ambient scene rotation and particle velocity are frozen or clamped to static states.
- Scroll-bound camera zooms/dollies snap directly to resting keyframe poses without spatial jumps.
- Interactive pointer parallax is disabled.
- Exploded views offer discrete step buttons instead of continuous animated transitions.

---

## 12. Lifecycle Management & Memory Leak Prevention

Memory leaks in WebGL crash mobile browsers and degrade performance over time. Every Three.js implementation MUST implement explicit teardown:

```javascript
function disposeScene(scene, renderer, animationFrameId) {
  if (animationFrameId) cancelAnimationFrame(animationFrameId);
  scene.traverse((obj) => {
    if (obj.geometry) obj.geometry.dispose();
    if (obj.material) {
      if (Array.isArray(obj.material)) {
        obj.material.forEach((m) => disposeMaterial(m));
      } else {
        disposeMaterial(obj.material);
      }
    }
  });
  if (renderer) {
    renderer.dispose();
    renderer.forceContextLoss();
    if (renderer.domElement && renderer.domElement.parentNode) {
      renderer.domElement.parentNode.removeChild(renderer.domElement);
    }
  }
}

function disposeMaterial(mat) {
  Object.keys(mat).forEach((prop) => {
    if (mat[prop] && typeof mat[prop].dispose === 'function') {
      mat[prop].dispose();
    }
  });
  mat.dispose();
}
```

---

## 13. Visibility & Offscreen Throttling

To preserve battery and CPU/GPU cycles, rendering MUST pause when:
- `document.hidden === true` (tab switched or minimized).
- The canvas element is completely out of the viewport (monitored via `IntersectionObserver`).

---

## 14. Immersive Readiness Gate (`[IMMERSIVE_IMPLEMENTATION_READY]`)

Prior to building production 3D scenes in Phase 10, the Immersive Readiness check evaluates:
- `immersive.status = "implementation_ready"`
- `IMMERSIVE_JUSTIFICATION = PASS`
- `IMMERSIVE_LEVEL` declared (`0_NONE`, `1_ENHANCEMENT`, `2_FEATURE`, `3_CENTERPIECE`)
- `SCENE_ARCHITECTURE` documented
- `MOBILE_POLICY` declared and configured
- `REDUCED_MOTION_3D_POLICY` configured
- `WEBGL_FALLBACK` verified
- `PERFORMANCE_BUDGET` specified
- `ACCESSIBILITY_ALTERNATIVE` defined in semantic DOM
- `CLEANUP_PLAN` verified

---

## 15. Dependency Governance & Version Selection Policy

1. **Project-Pinned Versioning:** Immersive web builds must use the project's installed or pinned compatible dependency version (`THREE_VERSION`, `R3F_VERSION`, `DREI_VERSION`).
2. **No Hardcoded Ancient Baselines:** Prohibit obsolete legacy baselines (e.g. "r128+"). Always evaluate compatibility against the project's contemporary toolchain and runtime requirements.
3. **Migration & Deprecation Audit:** When upgrading or selecting Three.js versions, run an explicit `DEPRECATED_API_AUDIT` to verify renderer color spaces (`outputColorSpace`), geometry signatures, material transmission properties, and disposal hooks.
4. **Honest Support Classification:** Documented architectural support for frameworks (R3F, Drei) must remain classified as `DOCUMENTED` unless an executable test suite with installed packages explicitly verifies runtime behavior. 
