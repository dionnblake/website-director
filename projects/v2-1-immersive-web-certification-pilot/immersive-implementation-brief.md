# IMMERSIVE IMPLEMENTATION BRIEF: AETHEL_CALIBRE_01

> **Project:** AETHEL Precision Horology & Chronométrie  
> **Schema Version:** 2.1.0  
> **Governance:** IMMERSIVE-WEB-PROTOCOL.md  
> **Immersive Level:** `2_FEATURE`  
> **Technical Engine:** `THREE_JS_VANILLA`  
> **Readiness Status:** `implementation_ready`

---

## 1. Immersive Justification & Communication Purpose

- **Spatial Narrative Role:** The AETHEL Calibre 01 is an integrated column-wheel chronograph with an architectural 4-tier movement. Static 2D photography cannot communicate the mechanical interaction between the escapement bridge, chronograph column wheel, balance wheel oscillation, and skeletal sapphire dial. A controlled, exploded 3D spatial presentation enables collectors to understand the micro-mechanical depth.
- **Anti-Demo-Slop Validation:** Zero generic demo tropes (no neon grids, floating toruses, or random particles). The procedural 3D model is constructed strictly from authentic horological movement geometries: titanium baseplates, ruthenium bridges, blued steel screws, column wheels, and sapphire crystal discs.
- **Audience & Commercial Value:** Demonstrates extreme manufacturing tolerance (0.001mm) and high horology craft, establishing collector pricing power ($85,000 MSRP).

---

## 2. Scene Graph Architecture & Technical Specifications

- **Container Selector / Canvas Mount:** `#three-viewport`
- **Camera Direction:**
  - Type: `PerspectiveCamera` (FOV: 45°, Near: 0.1, Far: 100)
  - Behavior: `CONSTRAINED_INSPECTION` + `SCROLL_DOLLY`
  - Position: `(0, 0, 5.5)`
  - Limits: Bounded pointer parallax (±4° pitch/yaw) with smooth lerping.
- **Lighting Rig:**
  - Key Light: Directional 5600K @ Intensity 1.8 (Pos: 4, 6, 5)
  - Fill Light: Directional 4000K @ Intensity 0.6 (Pos: -4, -2, 3)
  - Rim Light: Cool Specular @ Intensity 2.2 (Pos: 0, 4, -5)
  - Ambient: Neutral diffuse @ Intensity 0.4
- **Primary Subject (Procedural Movement Geometry):**
  - **Tier 1 (Baseplate):** Brushed Grade 5 Titanium circular chassis with circular graining (`CylinderGeometry`, `MeshStandardMaterial` metalness 0.9, roughness 0.25).
  - **Tier 2 (Gear Train & Column Wheel):** Golden brass escapement gears and blued-steel 8-pillar column wheel (`TorusGeometry` & `CylinderGeometry`).
  - **Tier 3 (Balance Wheel & Bridge):** Oscillating balance wheel with ruthenium-treated skeleton bridge (`RingGeometry` + `BoxGeometry`).
  - **Tier 4 (Sapphire Dial & Bezel):** Transparent anti-reflective crystal with engraved index markings (`RingGeometry` with `MeshPhysicalMaterial` transmission 0.95, roughness 0.05).

---

## 3. Motion & Interaction Specifications

- **Ambient Motion:** Slow continuous axial rotation (0.003 rad/frame) + balance wheel counter-oscillation.
- **Interactive Inspection:** Mouse pointer / touch drag tilts the movement within bounded ±15° arcs.
- **Exploded View Trigger:** Interactive toggle button (`#btn-explode`) shifts the 4 mechanical tiers along the Z-axis (`z = [-0.6, -0.2, 0.3, 0.8]`) with smooth GSAP easing.
- **Reduced Motion Behavior (`prefers-reduced-motion: reduce`):** Ambient rotation is paused, pointer parallax disabled, and exploded views snap immediately without continuous animation.

---

## 4. Responsive & Capability Fallback Policies

- **Mobile Policy (`MOBILE_3D_POLICY = SIMPLIFIED`):** Reduced tier complexity, DPR clamped to 1.5, touch drag enabled with touch-action isolation.
- **Universal 2D Fallback (`WEBGL_FALLBACK`):** High-resolution SVG mechanical technical drawing rendered instantly if WebGL is unavailable or when `?forceWebGLFallback=1` is provided.
- **Semantic DOM Parity:** 100% of technical calibre specifications (Jewels, Power Reserve, Frequency, Materials) and conversion CTAs exist in accessible semantic HTML.
- **Lifecycle Cleanup Plan:** `disposeScene()` executes on teardown, purging all geometries, materials, and cancelling the `requestAnimationFrame` loop.
