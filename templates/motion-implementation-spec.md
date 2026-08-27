# MOTION IMPLEMENTATION SPECIFICATION

> **Project Name:** [Insert Project Name]  
> **Evaluation Date:** [YYYY-MM-DD]  
> **Protocol:** `GSAP-IMPLEMENTATION-PROTOCOL.md` (Website Director V1.5.0)  
> **Motion Strategy Authority:** `motion-direction.md` (Lock 5: `[MOTION_DIRECTION_LOCKED]`)  
> **Motion Implementation Engine:** Official GreenSock GSAP Skills Engine (`v3.15.0+`, SHA: `aed9cfd3277740755f6bfc1155c7aa645403b760`)  
> **Runtime Status:** `GSAP_REQUIRED = [TRUE | FALSE]`  

---

## 1. Engine & Stack Context

| Parameter | Configuration Value |
| :--- | :--- |
| **Approved Motion Level** | `[MOTION_LEVEL_0 | MOTION_LEVEL_1 | MOTION_LEVEL_2 | MOTION_LEVEL_3]` |
| **Framework Target** | `[React / Next.js / Vue / Nuxt / Svelte / Vanilla]` |
| **GSAP Runtime Package** | `[gsap / @gsap/react / NONE (CSS-Only)]` |
| **Authorized Plugins** | `[ScrollTrigger, Flip, Draggable, SplitText, etc. / NONE]` |
| **Lifecycle Cleanup Standard**| `[useGSAP() with scope / gsap.context() + ctx.revert()]` |

---

## 2. Motion Registry & Implementation Matrix

| Motion ID | Target Element / Selector | Purpose ("Why Does This Move?") | Trigger & Scope | GSAP API & Plugins | Easing & Duration | Responsive Mobile Adaptation | Reduced-Motion Fallback |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **M-01** | `.hero-headline, .hero-sub` | Reveal core proposition on page mount | Mount (`useGSAP`) | `gsap.from()` | `power3.out`, 0.9s (stagger 0.15s) | Identical, stagger reduced to 0.1s | Fade only, zero Y translation (`autoAlpha: 0`) |
| **M-02** | `.metric-counter` | Draw attention to verified proof numbers | Viewport `top 80%` | `gsap.from()`, `ScrollTrigger` | `power2.out`, 1.2s | Viewport `top 90%` | Instant static display |
| **M-03** | `.feature-card-deck` | Spatial storytelling of product workflow | Scroll Scrub (`top top`) | `gsap.timeline()`, `ScrollTrigger` (pin) | `none`, scrub: 1s | Unpinned vertical stack | Stacked cards, no scrub pinning |

---

## 3. Plugin Justification & Governance

| Plugin Name | Purpose & Approved Scope | Why Core GSAP is Insufficient | Accessibility Review | Performance Risk & Mitigation |
| :--- | :--- | :--- | :---: | :--- |
| **ScrollTrigger** | [e.g., Progress bar & card reveals] | [Requires scroll position linking] | `PASS` (`matchMedia` included) | `invalidateOnRefresh: true`, compositor only |
| **[Plugin 2]** | [Approved Scope] | [Justification] | `PASS` | [Mitigation] |

---

## 4. Lifecycle Cleanup & Memory Leak Guarantees

```javascript
// Target Implementation Lifecycle Pattern
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

if (typeof window !== 'undefined') {
  gsap.registerPlugin(useGSAP, ScrollTrigger);
}

// Scoped to container with automatic reversion on unmount
useGSAP(() => {
  const mm = gsap.matchMedia();
  
  mm.add('(prefers-reduced-motion: no-preference)', () => {
    // Normal Choreography
  });
  
  mm.add('(prefers-reduced-motion: reduce)', () => {
    // Accessible Alternative
  });
}, { scope: containerRef });
```

---

## 5. Pre-Flight Verification Sign-Off

- **Lock Fidelity Check:** `VERIFIED (Zero contradiction with motion-direction.md)`
- **Compositor Integrity Check:** `VERIFIED (Zero layout properties animated: top/left/width/height prohibited)`
- **Reduced Motion Tested:** `VERIFIED (prefers-reduced-motion presents accessible alternative)`
- **Mobile Viewport Tested:** `VERIFIED (Simplified layout on screens <= 768px)`
- **Lifecycle Cleanup Tested:** `VERIFIED (Zero orphan timelines or ScrollTriggers after unmount)`
- **Runtime Dependency Governance:** `VERIFIED (gsap included only in client project package.json)`
