# PAGE EXPERIENCE & TRANSITION PROTOCOL

> **Version:** 2.3.0  
> **Status:** Authoritative Page Experience, Route Continuity & Transition Standard  
> **Core Principle:** Page transitions exist to preserve user orientation, reinforce information hierarchy, and improve perceived visual continuity. Transitions must never exist merely because "every click needs an animation."

---

## 1. System Invariants & Core Governance

1. **Anti-Transition-Slop Invariant:** Reject gratuitous fullscreen curtains, 2-second black loading screens, generic diagonal wipes, identical agency-style zoom masks, and any motion that delays user access to content. If a transition could belong unchanged to 20 unrelated websites, `TRANSITION_DISTINCTIVENESS = FAIL`.
2. **Semantic Content & URL Primacy:** Every route MUST preserve real URLs, native browser history (Back/Forward), deep links, refresh parity, page titles, semantic `<h1>`, and structured content. No transition system may flatten multi-page architecture into an ambiguous client-only state.
3. **No Sixth Owner Lock:** `[PAGE_EXPERIENCE_READY]` is an engineering readiness check under existing Lock 5 (Motion Direction), NOT a sixth owner lock. Exactly 5 owner locks remain immutable (`design_direction_locked`, `information_architecture_locked`, `content_structure_locked`, `design_system_locked`, `motion_direction_locked`).
4. **Boundary Separation:**
   - **Page Experience System:** Owns navigation lifecycle (leave, swap, enter), history coordination, scroll restoration, focus management, and route capability fallbacks.
   - **Native View Transitions API:** Authoritative baseline for same-document and cross-document visual state morphs.
   - **GSAP:** Authoritative for detailed motion choreography and DOM timeline animation during lifecycle hooks.
   - **Three.js (V2.1):** WebGL scenes must gracefully snapshot, freeze, or cleanly unmount across page transitions without leaking animation loops or WebGL contexts.
   - **Rive (V2.2):** Interactive vector state machines must pause or dispose cleanly during route departures without dangling canvas instances.
   - **Asset Director (V2.0):** Authoritative for visual assets, transition textures, and imagery provenance.
5. **Universal Fallback Requirement:** `NO_TRANSITION_SUPPORT != BROKEN_NAVIGATION`. Standard navigation MUST succeed if transition scripts fail, are unsupported, or are disabled via `?forceTransitionFallback=1`.

---

## 2. Transition Capability Levels (`PAGE_TRANSITION_LEVEL`)

| Level | Identifier | Description | Typical Budget | Target Use Cases |
| :--- | :--- | :--- | :--- | :--- |
| **Level 0** | `0_NONE` | **Standard Browser Navigation.** Zero custom transition layer. Instant native swap. | 0ms | High-utility tools, dense editorial, documentation, or when motion adds no semantic value. Valid across all ambition tiers. |
| **Level 1** | `1_SUBTLE` | **Restrained Route Continuity.** Short cross-fade, persistent navigation bar, subtle content reveal. | 150ms – 300ms | Premium editorial, clean SaaS dashboards, modern brand sites. |
| **Level 2** | `2_SIGNATURE` | **Authored Brand Continuity.** Shared-element expansion (e.g. card to hero), editorial wipe, mask reveal. | 250ms – 500ms | Showcase portfolios, luxury showcases, narrative products. |
| **Level 3** | `3_CINEMATIC` | **Narrative Spatial Journey.** Immersive environment handoff, coordinate-mapped multi-element choreography. | 400ms – 800ms (strict justification) | Experimental storytelling, flagship product interactive launches. |

---

## 3. Creative Ambition Calibration

- **`STANDARD`:** Default `PAGE_TRANSITION_LEVEL = 0_NONE` or `1_SUBTLE`. Avoid unnecessary router complexity.
- **`PREMIUM`:** Evaluate Level 1 or Level 2. Prioritize perceived responsiveness and reading context.
- **`SHOWCASE`:** Transition character must be deliberately authored. Level 0 remains valid if architectural restraint best serves the concept.
- **`EXPERIMENTAL`:** Levels 1–3 explored. Navigation integrity, history parity, and accessibility remain strict requirements.

---

## 4. Transition Justification Gate (`TRANSITION_JUSTIFICATION`)

Before approving custom page transitions, verify:
1. Does visual continuity help the visitor maintain spatial/contextual orientation?
2. Is there a genuine relationship between source and destination views?
3. Does the transition reinforce the core design thesis without blocking user intent?
4. Does mobile performance remain 60fps with zero layout thrashing?
5. Does browser Back/Forward navigation feel immediate and native?

*If the only answer is "it looks cool," custom transitions fail the gate and default to `0_NONE`.*

---

## 5. Technology Selection & Engine Decision Matrix

1. **Native View Transitions (`NATIVE_VIEW_TRANSITIONS` - Preferred Baseline):**
   - Use CSS `@view-transition { navigation: auto; }` for modern cross-document MPA transitions.
   - Use `document.startViewTransition()` for progressive same-document enhancement.
   - Zero external router overhead. Full MPA and SEO compatibility.
2. **Framework Router Transitions (`FRAMEWORK_ROUTER`):**
   - Used when project stack is React (Next.js), Vue (Nuxt), or SvelteKit with native layout transitions.
3. **GSAP Coordinated Transitions (`GSAP_COORDINATED`):**
   - Transition system owns Navigation Lifecycle; GSAP owns Motion Choreography.
4. **Barba.js Boundary (`BARBA_JS` - Optional / Non-Default):**
   - Barba is NOT default. Only used when legacy MPA requirements mandate complex lifecycle coordination not achievable via native View Transitions.

---

## 6. Shared Element Continuity (`SHARED_ELEMENT_TRANSITIONS`)

1. **Deterministic Naming:** Assign `view-transition-name` only to genuine shared anchors (e.g., `project-hero-media`, `brand-mark`).
2. **Anti-Spam Invariant:** Never assign transition names to arbitrary lists of cards or paragraphs.
3. **Cross-Document Pairing:** Ensure source thumbnail and destination hero share identical `view-transition-name` tokens.

---

## 7. History, Scroll, Focus & Accessibility Governance

1. **History Parity:** Full support for popstate, pushState, Browser Back/Forward, Deep Links, and Page Refresh.
2. **Popstate Policy (`POPSTATE_TRANSITION_POLICY = RESTORE_CONTEXT`):** Never replay long intro sequences on browser Back. Use instant or subtle reverse fades.
3. **Scroll Restoration (`SCROLL_RESTORATION_POLICY`):**
   - Forward to new route: Scroll to top (`window.scrollTo(0, 0)`) or anchor target.
   - History Back/Forward: Preserve previous reading position via native `history.scrollRestoration = 'manual'` coordination.
4. **Route Focus Policy (`ROUTE_FOCUS_POLICY`):** On same-document/SPA swaps, update `<title>` and move focus to destination `<h1>` or `#main-content` with `tabindex="-1"`.
5. **Anchor & Modifier Keys:** Never intercept `Ctrl/Cmd + Click`, middle clicks, `target="_blank"`, `#anchor` hash links, or `download` attributes.
6. **Reduced Motion (`prefers-reduced-motion: reduce`):** Mandatory. Instantly bypass morph/slide transitions. Use immediate swap or minimal opacity fade ( $\le 100\text{ms}$ ).
7. **Mobile Policy (`MOBILE_TRANSITION_POLICY = SIMPLIFIED`):** Disable high-GPU coordinate travel on small viewports. Preserve touch responsiveness.

---

## 8. Third-Party Vendor Immutability

`THIRD_PARTY_RUNTIME_SOURCE_MUTATED = NO`. Website Director configures, imports, bundles, initializes, wraps, and adapts application-side integrations. Website Director MUST NOT silently mutate or patch third-party vendor runtime artifacts.

---

## 9. Page Experience Readiness Gate (`[PAGE_EXPERIENCE_READY]`)

Prior to enabling production transitions, evaluate:
- `page_experience.status = "implementation_ready"`
- `TRANSITION_JUSTIFICATION = PASS`
- `PAGE_TRANSITION_LEVEL` declared (`0_NONE`, `1_SUBTLE`, `2_SIGNATURE`, `3_CINEMATIC`)
- `NAVIGATION_MODEL` declared (`SAME_DOCUMENT`, `CROSS_DOCUMENT`, `FRAMEWORK_ROUTER`, `STANDARD_DOCUMENT_NAVIGATION`)
- `TRANSITION_ENGINE` declared
- `HISTORY_POLICY` verified (`RESTORE_CONTEXT`)
- `SCROLL_RESTORATION_POLICY` declared
- `FOCUS_POLICY` declared
- `REDUCED_MOTION_POLICY` configured
- `MOBILE_POLICY` declared
- `FAILURE_FALLBACK` verified (`STANDARD_NAVIGATION`)
- `RESOURCE_CLEANUP` verified (Three.js / Rive teardowns)

