# GSAP MOTION IMPLEMENTATION ENGINE PROTOCOL

> **Version:** 1.0.0 (Website Director V1.5.0 Subsystem)  
> **Status:** Mandatory Motion Engineering & Implementation Standard  
> **Governance:** Website Director Orchestration Rail (`SKILL.md` §2, Phase 8, 9, 10 & Phase 11.5)  
> **Attribution:** Adapted from the **Official GreenSock Skills** by **Jack Doyle / GreenSock** ([github.com/greensock/gsap-skills](https://github.com/greensock/gsap-skills)), licensed under the [MIT License](https://github.com/greensock/gsap-skills/blob/main/LICENSE).  
> **Source Provenance:** Repo: `https://github.com/greensock/gsap-skills`, Commit SHA: `aed9cfd3277740755f6bfc1155c7aa645403b760`, Version: `3.15.0+`.

---

## 1. Architectural Mission & Core Distinction

The **GSAP Motion Implementation Engine** translates an already-approved Website Director Motion Direction into performant, clean, accessible, and mathematically precise code.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           CORE ARCHITECTURE                              │
│                                                                          │
│  WEBSITE DIRECTOR OWNS MOTION STRATEGY & CREATIVE DIRECTION.             │
│  OFFICIAL GSAP SKILLS OWN MOTION IMPLEMENTATION & ENGINEERING.           │
│                                                                          │
│  GSAP does NOT decide:                                                   │
│  - whether a site needs motion                                           │
│  - how cinematic a site should be                                        │
│  - what emotional tone motion should create                              │
│  - what elements should dominate visitor attention                       │
│  - whether owner-approved motion decisions may be changed                │
└──────────────────────────────────────────────────────────────────────────┘
```

### The End-to-End Motion Lifecycle:
```
RESEARCH & COMPETITOR RECON (Phase 3)
      ▼
DESIGN INTELLIGENCE CANDIDATES (Phase 3.5 - UI/UX Pro Max)
      ▼
DESIGN DIRECTION SYNTHESIS (Phase 4 - Lock 1)
      ▼
MOTION DIRECTION STRATEGY & LEVEL ASSIGNMENT (Phase 8 - Lock 5)
      ▼
OWNER MOTION LOCK APPROVAL (Gate 5)
      ▼
GSAP MOTION IMPLEMENTATION SPECIFICATION (templates/motion-implementation-spec.md)
      ▼
OFFICIAL GSAP IMPLEMENTATION BUILD (Phase 10 - @gsap/react / useGSAP / ScrollTrigger)
      ▼
IMPECCABLE MOTION QUALITY SCAN (Phase 11 - Compositor, 65ch, Anti-Slop)
      ▼
WEBSITE GAUNTLET ADVERSARIAL CRITIQUE (Phase 11.5 - Motion Critic vs Reference Bar)
      ▼
PRODUCTION PRE-FLIGHT VERIFICATION (Phase 12 - Performance & Pre-flight Sign-off)
```

---

## 2. Epistemic Separation & Hard Governance Invariants

```
┌───────────────────────────┬────────────────────────────────────────────────────────┐
│ Subsystem / Authority     │ Core Question & Responsibility                         │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 1. Website Director       │ "What is the approved Motion Level (0-3), physics,     │
│    (Creative Authority)   │ choreography intent, and conversion purpose?"          │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 2. Official GSAP Skills   │ "How is this approved motion implemented correctly,    │
│    (Engineering Authority)│ with proper lifecycle cleanup, scoping, and eases?"    │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 3. Impeccable Critic      │ "Is the resulting animation technically disciplined,   │
│    (Code Quality)         │ free of layout thrashing, and anti-slop compliant?"    │
├───────────────────────────┼────────────────────────────────────────────────────────┤
│ 4. Website Gauntlet       │ "Does the rendered visual motion meet or beat the      │
│    (Adversarial Critic)   │ approved dimensional Reference Bar?"                   │
└───────────────────────────┴────────────────────────────────────────────────────────┘
```

### Hard Rules of Motion Governance:

1. **HARD RULE 1: Motion Direction Lock is Absolute Authority**
   - GSAP cannot independently introduce scroll storytelling, parallax, pinning, text splitting, smooth scrolling, physics, or transitions unless authorized by `motion-direction.md` (Lock 5).
   - If an implementation opportunity requires altering locked motion tokens: **STOP**. Issue a structured `LOCKED_CHANGE_REQUIRED` Change Request for Owner Review.
2. **HARD RULE 2: GSAP is NOT Automatic**
   - If `MOTION_LEVEL = LEVEL_0` (static) or CSS transitions suffice: `GSAP_REQUIRED = FALSE`.
   - Never add `gsap` or `@gsap/react` to a static or lightweight project merely because the engine exists.
3. **HARD RULE 3: Official GSAP Knowledge is Implementation Authority**
   - Official GreenSock practices supersede ad-hoc snippets, remembered APIs, or AI guesswork.
4. **HARD RULE 4: No Second Motion Director**
   - There is exactly one creative motion authority: Website Director Phase 8.
5. **HARD RULE 5: Resolve UI/UX Pro Max Deferral**
   - UI/UX Pro Max `motion.csv` conceptual terms are retained as *design intelligence inspiration*.
   - Raw un-scoped GSAP code snippets in `motion.csv` are **REJECTED** in favor of official GreenSock knowledge.
6. **HARD RULE 6: Runtime Dependency Governance**
   - Website Director core has **zero** runtime GSAP dependency.
   - Only generated frontend projects that require JS animation include `gsap` / `@gsap/react` in their `package.json`.

---

## 3. Official GSAP Skill Integration Architecture

Website Director vendors and references the 8 official GreenSock skill domains:

```
intelligence/gsap-skills/skills/
├── gsap-core/           # Tweens (to/from/fromTo/set), eases, staggers, matchMedia
├── gsap-timeline/       # Choreography, sequencing, labels, position parameter
├── gsap-scrolltrigger/  # Scroll reveals, progress links, pinning, scrub
├── gsap-plugins/        # Flip, Draggable, SplitText, ScrollSmoother, DrawSVG
├── gsap-utils/          # clamp, mapRange, interpolate, toArray, wrap, snap
├── gsap-react/          # @gsap/react, useGSAP(), scoped selectors, contextSafe
├── gsap-frameworks/     # Vue 3 / Nuxt 3, Svelte / SvelteKit, Vanilla JS lifecycle
└── gsap-performance/    # Compositor transforms, will-change, zero layout thrash
```

### 3.1 GSAP Core (`gsap-core`)
- **Primary Methods:** `gsap.to()`, `gsap.from()`, `gsap.fromTo()`, `gsap.set()`.
- **Visibility:** Use `autoAlpha` (which toggles `opacity` and `visibility: hidden`) to prevent invisible elements from intercepting clicks or failing accessibility audits.
- **Transforms:** Always prefer `xPercent` / `yPercent` and `x` / `y` over `left` / `top`.
- **Durations:** Values are strictly in **seconds** (e.g. `duration: 0.8`, not `800`).
- **Standard Eases:** Use string syntax: `'power2.out'`, `'power3.out'`, `'expo.out'`, `'sine.inOut'`, `'none'`.

### 3.2 GSAP Timeline (`gsap-timeline`)
- **Choreography:** Group multi-element sequences into `gsap.timeline({ defaults: { ease: 'power2.out', duration: 0.6 } })`.
- **Position Parameter:** Use relative alignments (`'<0.1'`, `'+=0.2'`, `'-=0.3'`) rather than calculating hard delay offsets.
- **Labels:** Anchor complex section milestones with `tl.addLabel('phase2')`.

### 3.3 GSAP ScrollTrigger (`gsap-scrolltrigger`)
- **Trigger Structure:**
  ```javascript
  ScrollTrigger.create({
    trigger: element,
    start: 'top 80%',
    end: 'bottom 20%',
    toggleActions: 'play none none reverse',
    invalidateOnRefresh: true
  });
  ```
- **Pinning Rules:**
  1. Never animate the pinned trigger element itself with vertical transforms (`y`, `yPercent`, `top`). Wrap inside a dedicated pin-container.
  2. Always specify `pinSpacing: true` unless implementing overlay card decks.
  3. Include `anticipatePin: 1` to eliminate visual pinning stutters.
- **Refresh Discipline:** Call `ScrollTrigger.refresh()` after dynamic font loading or layout-shifting DOM mutations.

### 3.4 GSAP React / Next.js (`gsap-react`)
- **Standard Hook:** Always use `useGSAP()` from `@gsap/react` with a scoped container reference:
  ```javascript
  import gsap from 'gsap';
  import { useGSAP } from '@gsap/react';
  import { useRef } from 'react';

  // Register in component or client root
  gsap.registerPlugin(useGSAP);

  export default function Hero() {
    const container = useRef(null);

    useGSAP(() => {
      gsap.from('.headline', { y: 30, autoAlpha: 0, duration: 0.8 });
    }, { scope: container }); // Automatically reverts & cleans up on unmount!

    return <section ref={container}><h1 className="headline">Title</h1></section>;
  }
  ```
- **SSR Safety:** Ensure GSAP plugin registration occurs inside client components (`"use client"` in Next.js App Router) or client lifecycle checks (`typeof window !== 'undefined'`).
- **Event Callbacks:** Wrap async callbacks or event triggers in `contextSafe()`.

### 3.5 GSAP Frameworks (`gsap-frameworks`)
- **Vue 3 / Nuxt 3:** Use `gsap.context()` in `onMounted()` and call `ctx.revert()` in `onUnmounted()`.
- **Svelte / SvelteKit:** Use `gsap.context()` in `onMount()` and call `ctx.revert()` in `onDestroy()`.
- **Vanilla JS:** Return a teardown closure `() => ctx.revert()` from the initialization module.

### 3.6 GSAP Performance (`gsap-performance`)
- **Compositor Only:** Animate `transform` (`x`, `y`, `xPercent`, `yPercent`, `scale`, `rotation`) and `opacity` / `autoAlpha`.
- **Zero Layout Thrashing:** Animating `width`, `height`, `padding`, `margin`, `top`, `left`, `bottom`, `right` is **STRICTLY BANNED** on continuous animations.
- **will-change Allocation:** Apply `will-change: transform` only to actively animating elements during scroll or interaction; never apply `will-change` globally to entire pages.

---

## 4. Purposeful Motion & Accessibility Standards

### 4.1 Purposeful Motion Rule
Every animation in `motion-implementation-spec.md` must answer: **"WHY DOES THIS MOVE?"**
Valid purposes include:
- Directing visitor focal attention to primary value proposition.
- Revealing structural hierarchy upon viewport entry.
- Maintaining spatial continuity during state transitions (tabs, drawers, modals).
- Communicating interactive feedback on user engagement.

*Animations added solely for decorative novelty without structural purpose are prohibited.*

### 4.2 Mandatory Reduced-Motion Architecture
All GSAP implementations must provide an explicit reduced-motion fallback using `gsap.matchMedia()`:
```javascript
const mm = gsap.matchMedia();

// Standard Motion (Full choreography)
mm.add('(prefers-reduced-motion: no-preference)', () => {
  gsap.from('.card', { y: 40, autoAlpha: 0, duration: 0.8, stagger: 0.15 });
});

// Reduced Motion (Instant or subtle fade, zero translation)
mm.add('(prefers-reduced-motion: reduce)', () => {
  gsap.from('.card', { autoAlpha: 0, duration: 0.2 });
});
```

### 4.3 Responsive Motion Adaptation
Desktop motion sequences do not blindly execute on mobile. The Motion Implementation Plan must specify:
- **Desktop:** Full scroll scrub / pinning / multi-card stagger.
- **Mobile ($\le 768\text{px}$):** Simplified viewport trigger, zero heavy pinning, reduced stagger duration, touch-optimized swipe.

### 4.4 Cinematic Journey synchronization (V2.15 additive)

When GSAP coordinates a Cinematic Journey, it consumes the render strategy
selected by Motion Direction. It does not decide whether video or canvas is
correct. The implementation must:

- measure `SCROLL_MOTION_ALIGNMENT` at start, mid-scroll, and settle states;
- use a delta-time-normalized `requestAnimationFrame` smoothing loop where a
  media scrubber needs interpolation;
- use `SEEK_COALESCING` so rapid scroll input leaves only the latest needed seek;
- use `DELTA_GATED_DOM_UPDATES` for text and metadata instead of writing on
  every frame without a value change;
- isolate composited media layers and bound `will-change` to active motion;
- expose poster, mobile, reduced-motion, and `COMPLETE_WITHOUT_VIDEO` paths;
- remove listeners, timelines, object URLs, and scroll triggers on teardown.

The browser evidence manifest, not source inspection, decides whether the
chosen strategy is stable enough for a visual-quality review. A failed scrub,
flicker, or unreadable moving background is recorded as a defect and is not
hidden by a static code scan.

---

## 5. Plugin Governance & Smooth Scroll Policy

### 5.1 Plugin Authorization Matrix
Plugins are capabilities granted per project need, never loaded by default:

| Plugin Name | Approved Use Case | Dependency Justification | A11y / Perf Check Required |
| :--- | :--- | :--- | :---: |
| **ScrollTrigger** | Scroll reveals, progress bars, section pinning | Required for scroll-linked timeline control | **YES** (`anticipatePin`, reduced motion) |
| **Flip** | Smooth layout state transitions (grid/list, filters) | FLIP animation without manual bounding math | **YES** (Zero layout jumps) |
| **Draggable / Inertia**| Sliders, carousels, interactive maps | Momentum physics on touch/mouse | **YES** (Keyboard navigation parity) |
| **SplitText** | Editorial headline reveals | Character/word splitting without DOM corruption | **YES** (Preserve screen reader text) |
| **ScrollSmoother** | Smooth momentum scrolling on luxury/portfolio sites | Smooth normalized scroll on desktop | **YES** (Strictly disabled on touch/reduced motion) |

### 5.2 ScrollSmoother & Smooth Scroll Conservatism
- Native browser scrolling is the preferred default.
- `ScrollSmoother` is authorized **only** for `MOTION_LEVEL_3` luxury or portfolio projects with explicit Owner sign-off.
- Smooth scrolling is **STRICTLY DISABLED** on mobile touch devices (`smoothTouch: false` or bypassed) and when `(prefers-reduced-motion: reduce)` is active.

---

## 6. Lifecycle Cleanup Guarantee & Memory Leak Prevention

Every framework implementation must achieve a **Zero-Leak Guarantee**:
1. When a component unmounts or a page navigates, **all** tweens, timelines, and ScrollTriggers created within that scope must be reverted.
2. React: `useGSAP({ scope: containerRef })` handles automatic reversion.
3. Vue / Nuxt / Svelte / Vanilla: `ctx.revert()` is called on component destroy / route change.
4. Validation check: Invoking unmount in test fixtures must result in `ScrollTrigger.getAll().length === 0`.

---

## 8. Lenis Smooth Inertial Scroll & GSAP Synchronization Protocol

For elite, award-winning craft, butter-smooth inertial scrolling elevates the physical sensation of the website. `Lenis` is authorized and recommended for high-end editorial, luxury, and portfolio builds.

### 8.1 Lenis + GSAP ScrollTrigger Integration Standard
```javascript
// Initialize Lenis with refined inertia constants
const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // Exponential ease-out
  direction: 'vertical',
  gestureDirection: 'vertical',
  smooth: true,
  mouseMultiplier: 1.0,
  smoothTouch: false, // Keep native touch physics on mobile
  touchMultiplier: 2,
  infinite: false,
});

// Synchronize Lenis scroll position with GSAP ScrollTrigger
lenis.on('scroll', ScrollTrigger.update);

// Bind GSAP ticker to Lenis RAF for unified frame rendering
gsap.ticker.add((time) => {
  lenis.raf(time * 1000);
});

// Disable lagSmoothing to prevent stutter during rapid scrolls
gsap.ticker.lagSmoothing(0);
```

---

## 9. Kinetic Typography & Split-Mask Reveals

High-end sites avoid simple opacity fades for primary titles. Text must be masked with clean clip-paths or nested overflow-hidden wrapper containers.

### 9.1 CSS/DOM Mask Architecture
```html
<h1 class="split-mask-heading">
  <span class="mask-line"><span class="mask-inner">DISCIPLINE</span></span>
  <span class="mask-line"><span class="mask-inner">BUILDS THE MAN</span></span>
</h1>
```

```css
.mask-line {
  display: block;
  overflow: hidden;
  line-height: 1.1;
}
.mask-inner {
  display: block;
  transform: translateY(115%);
  will-change: transform;
}
```

### 9.2 GSAP Reveal Choreography
```javascript
gsap.to('.split-mask-heading .mask-inner', {
  y: '0%',
  duration: 1.1,
  ease: 'power4.out',
  stagger: 0.12,
  scrollTrigger: {
    trigger: '.split-mask-heading',
    start: 'top 85%',
    toggleActions: 'play none none reverse'
  }
});
```

---

## 10. Pinned Horizontal Scrollytelling Standard

For complex narratives (e.g. 7-Day Protocols, Product Breakdowns, Archives), pinned horizontal scroll tracks create dramatic engagement.

### 10.1 Pinned Track Blueprint
```javascript
const scrollTrack = document.querySelector('.horizontal-track');
const scrollContainer = document.querySelector('.horizontal-section');

if (scrollTrack && scrollContainer && window.innerWidth > 992) {
  const totalWidth = scrollTrack.scrollWidth - window.innerWidth + 120;
  
  gsap.to(scrollTrack, {
    x: () => -totalWidth,
    ease: 'none',
    scrollTrigger: {
      trigger: scrollContainer,
      pin: true,
      scrub: 1,
      start: 'top top',
      end: () => `+=${totalWidth}`,
      invalidateOnRefresh: true,
    }
  });
}
```

---

## 11. Micro-Physics & Magnetic Cursor Engine

### 11.1 Magnetic Pull Standard
Magnetic elements pull smoothly toward the cursor within an active proximity threshold, then spring back with damping.
```javascript
document.querySelectorAll('[data-magnetic]').forEach((el) => {
  el.addEventListener('mousemove', (e) => {
    const rect = el.getBoundingClientRect();
    const x = (e.clientX - (rect.left + rect.width / 2)) * 0.35;
    const y = (e.clientY - (rect.top + rect.height / 2)) * 0.35;
    gsap.to(el, { x: x, y: y, duration: 0.4, ease: 'power2.out' });
  });

  el.addEventListener('mouseleave', () => {
    gsap.to(el, { x: 0, y: 0, duration: 0.7, ease: 'elastic.out(1, 0.4)' });
  });
});
```
