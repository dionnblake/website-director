# IMMERSIVE IMPLEMENTATION BRIEF: [SCENE_ID]

> **Project:** [Project Name]  
> **Schema Version:** 2.1.0  
> **Governance:** IMMERSIVE-WEB-PROTOCOL.md  
> **Immersive Level:** [0_NONE | 1_ENHANCEMENT | 2_FEATURE | 3_CENTERPIECE]  
> **Technical Engine:** [THREE_JS_VANILLA | REACT_THREE_FIBER | DREI]  
> **Readiness Status:** [planning | prototype_ready | implementation_ready | blocked]

---

## 1. Immersive Justification & Communication Purpose

- **Spatial Narrative Role:** [Explain why 3D is superior to 2D media for this specific communication job]
- **Anti-Demo-Slop Validation:** [Confirm scene physics/aesthetics are subject-grounded and free of generic tropes]
- **Audience & Commercial Value:** [Explain decision-maker cognitive benefit and trust generation]

---

## 2. Scene Graph Architecture & Technical Specifications

- **Container Selector / Canvas Mount:** `#webgl-stage`
- **Camera Direction:**
  - Type: `PerspectiveCamera` (FOV: 45°, Near: 0.1, Far: 1000)
  - Behavior: `[STATIC_PRODUCT | CONSTRAINED_INSPECTION | SCROLL_DOLLY | FOCUS_TRANSITION | CINEMATIC_PATH]`
  - Limits: Polar angle [30°, 85°], Azimuth angle [-45°, 45°], Distance [2.0m, 6.0m]
- **Lighting Rig:**
  - Key Light: Directional 5800K @ Intensity 1.8 (Pos: 5, 8, 4)
  - Fill Light: Ambient Diffuse 4500K @ Intensity 0.6
  - Rim Light: Hard Blue-Shift Specular @ Intensity 2.2 (Pos: -4, 2, -5)
  - Environment Map: Studio neutral HDRI (Blur: 0.8)
- **Primary Subject & Assets:**
  - Source: [Procedural Three.js Geometry | Asset Director Manifest Asset ID: `asset-3d-01`]
  - Master Mesh: [Geometry hierarchy and node naming]
  - Materials: PBR `MeshStandardMaterial` / `MeshPhysicalMaterial` (Roughness: 0.25, Metalness: 0.85)

---

## 3. Motion & Scroll Synchronization

- **Coordination Engine:** `GSAP_SCROLLTRIGGER`
- **Scroll Timeline Bindings:**
  - `0% - 30%`: Hero intro rotation and initial camera dolly-in.
  - `30% - 70%`: Pinned component disassembly / exploded structural view.
  - `70% - 100%`: Reassembly and camera transition to telemetry detail angle.
- **Micro-Interaction:** Pointer parallax damped with 0.08 smoothing factor.

---

## 4. Responsive & Capability Fallback Policies

- **Mobile Policy (`MOBILE_3D_POLICY`):** `[FULL | SIMPLIFIED | STATIC_RENDER | DISABLED]`
- **Device Pixel Ratio (DPR):** Desktop Max: `2.0`, Mobile Max: `1.5`
- **Performance Budget:**
  - Max Draw Calls: `<= 35`
  - Max Triangles: `<= 85,000`
  - Target Frame Rate: `60 FPS` (Desktop), `30+ FPS` (Mobile)
- **WebGL Fallback (`WEBGL_FALLBACK`):** High-resolution 2D keyframe rendered with zero layout shift when WebGL is unavailable or when `?forceWebGLFallback=1` is passed.
- **Reduced Motion (`REDUCED_MOTION_3D_POLICY`):** Ambient spin frozen, scroll transitions snapped to discrete keyframes.
- **Semantic DOM Parity:** 100% of product specifications, headlines, and CTAs available in accessible semantic HTML alongside canvas.
- **Cleanup & Disposal Plan:** Explicit `geometry.dispose()`, `material.dispose()`, `renderer.dispose()`, and animation loop cancellation on unmount. 
