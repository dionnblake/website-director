# CINEMATIC BRIEF: KREISLER & VOSS Motorenwerke

> **Date Created:** 2026-08-23  
> **Status:** APPROVED (Phase 15 — Binding Cinematic Specialist Contract)  
> **Authority:** Website Director V1.1 (Binding on Specialist)  
> **Protocol Reference:** `CINEMATIC-INTEGRATION-PROTOCOL.md`  

---

## 1. Hero Cinematic Concept
- **Concept Title:** *"From Billet to Machine — The Coachbuilder's Metamorphosis"*
- **Subject:** The KV-01 "Monolith GT" Air-Cooled Grand Tourer.
- **Environment:** Atmospheric private engineering workshop at dusk in Cologne. Milled concrete floor, warm tungsten worklights casting long raking shadows, dark anodized steel backdrop.
- **Camera & Lens Language:** 85mm anamorphic prime lens aesthetic, shallow depth of field on mechanical macros transitioning to wide cinematic 21:9 framing on full vehicle reveal.

---

## 2. Scroll-Driven Motion Sequence (4 Keyframes)

```
0% SCROLL (FRAME 0)
Macro close-up of 5-axis CNC-milled 6061-T6 aluminum velocity stack / intake trumpet.
Sharp metallic specular highlights. Focus on machining toolpaths.

↓ (30% SCROLL)
Camera pulls back along the hand-formed aluminum widebody fender.
A horizontal raking light sweep illuminates the coachbuilt muscular haunches.

↓ (65% SCROLL)
Saddle Ochre leather cockpit and titanium roll cage emerge through dark tinted glazing.
Exhaust tips and mechanical diffuser take volumetric shape.

↓ (100% SCROLL)
Full side/three-quarter profile of KV-01 Monolith GT revealed in complete majesty.
Manifesto headline and primary commission CTA snap into crystal focus.
Page unpins for natural vertical scroll flow.
```

---

## 3. Approved vs Prohibited Cinematic Modules

### Approved Modules:
- `Canvas / SVG Frame Sequence Scrubber` (Smooth requestAnimationFrame timeline interpolation).
- `Tactile Component Lighting Scrubber` (Interactive specular reflection pass).
- `Dual-View Technical Mode Switcher` (Spatial photography ↔ CAD vector blueprints).

### Prohibited Modules:
- ❌ Flying 3D spark/smoke particles (AI-slop / gamer cliché).
- ❌ Aggressive mouse-follow glowing cursor or magnetic text scramble.
- ❌ Heavy Three.js / WebGL 3D meshes that exceed performance budgets.
- ❌ Automatic looping audio or engine rev sound effects.

---

## 4. Cost Boundary & External Services
- **External Paid Service Requirement:** **NONE ($0.00)**.
- **Implementation Mechanism:** High-performance procedural SVG/Canvas multi-layer render + optimized vector paths with requestAnimationFrame interpolation.
- **Cost Authorization Gate:** Passed with zero external fees (`OWNER_COST_AUTHORIZATION_REQUIRED = NONE`).

---

## 5. Performance Budget & Assets
- **Total Initial Hero Payload:** `< 250 KB` (entire HTML/CSS/JS/SVG bundle).
- **Target Frame Rate:** Stable 60 FPS on desktop and modern mobile.
- **Memory Footprint:** `< 40 MB` active heap.

---

## 6. Fallback Specifications
- **Mobile Fallback (`max-width: 768px`):** Replaces pinned 200vh scroll with an interactive touch scrubber and immediate hero showcase with zero layout shifts.
- **Reduced Motion Fallback (`prefers-reduced-motion: reduce`):** Bypasses all scroll-linked canvas animations; displays the finished KV-01 vehicle immediately in full fidelity.

---

## 7. Sign-Off & Lock Engagement
- [x] Cinematic brief complete and approved.
- [x] Specialist boundaries and fallbacks locked.
- [x] **`motion.cinematic_brief_complete = true`**.
- [x] **`locks.motion_direction_locked = true`**.
