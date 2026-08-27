# MOTION IMPLEMENTATION SPECIFICATION (OFFICIAL GSAP SKILLS)

> **Protocol:** `GSAP-IMPLEMENTATION-PROTOCOL.md` (Website Director V1.6.0)  
> **Engine:** Official GreenSock GSAP Skills Engine (`v3.15.0+`, SHA: `aed9cfd3277740755f6bfc1155c7aa645403b760`)  
> **Runtime Status:** `GSAP_REQUIRED = TRUE`  

---

## 1. Implementation Registry

| ID | Selector | Purpose | Trigger | GSAP API | Ease & Duration | Responsive Mobile | Reduced Motion |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **M-01** | `.hero-dial, .hero-copy` | Reveal opening thesis on page load | Page Load | `gsap.from()` | `power3.out`, 1.0s (stagger 0.12s) | Instant fade | `autoAlpha: 0` (0.2s fade, no Y) |
| **M-02** | `.metric-cell` | Highlight astronomical timing thresholds | Viewport `top 85%` | `ScrollTrigger` | `power2.out`, 0.8s (stagger 0.1s) | Identical | Static numbers |
| **M-03** | `.gimbal-sim` | Interactive 3-axis gyro simulation | User slider input | GSAP ticker / `gsap.to()` | `power1.out`, 0.3s | Touch slider | Static fallback |
| **M-04** | `.ledger-row` | Display observatory trial history | Viewport `top 80%` | `ScrollTrigger` | `power2.out`, 0.6s | Viewport `top 90%` | Instant static display |

---

## 2. Reduced Motion & Lifecycle Cleanup
```javascript
// Scoped Lifecycle & matchMedia Pattern
const ctx = gsap.context(() => {
  const mm = gsap.matchMedia();
  mm.add('(prefers-reduced-motion: no-preference)', () => {
    // Full mechanical choreography
  });
  mm.add('(prefers-reduced-motion: reduce)', () => {
    // Accessible instant fade
  });
});
// Teardown: ctx.revert()
```
