# PAGE EXPERIENCE BRIEF: ATLAS_FORM_EDITORIAL_CONTINUITY

> **Project:** ATLAS FORM — Architecture & Industrial Design Journal  
> **Schema Version:** 2.3.0  
> **Governance:** PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md  
> **Transition Level:** `2_SIGNATURE`  
> **Navigation Model:** `CROSS_DOCUMENT`  
> **Engine:** `NATIVE_VIEW_TRANSITIONS`  
> **Readiness Status:** `implementation_ready`

---

## 1. Transition Justification & UX Objective

- **Contextual Role:** Preserves visual and spatial continuity when transitioning from editorial journal overview to curated monograph index and individual architectural case studies (`KRONOS PAVILION`).
- **Anti-Transition-Slop Validation:** Zero full-screen loading curtains, zero artificial progress delays, zero generic diagonal wipes. Motion budget strictly bounded to 280ms.
- **Audience & Brand Alignment:** High-end architectural and industrial design readership demanding editorial gravitas, high visual contrast, and immediate navigation response.

---

## 2. Route Topology & Shared Element Architecture

- **Primary Routes:**
  - `Home / Journal Index`: `index.html` -> Journal cover and latest monographs
  - `Project Archive`: `projects.html` -> Full catalogue of spatial monographs
  - `Project Monograph Detail`: `project-detail.html` -> Deep case study for Kronos Pavilion (featuring `#materials` deep anchor)
- **Shared Elements (`view-transition-name`):**
  - `kronos-hero-media`: Card thumbnail (`.project-card-image`) in `projects.html` -> Hero banner (`.monograph-hero-image`) in `project-detail.html`
  - `brand-header-mark`: Persistent brand logotype (`.brand-logo`) across all routes
- **Directional Navigation Model:** `FORWARD` (Overview -> Detail) / `BACK` (Detail -> Overview) / `LATERAL` (Nav bar switches)

---

## 3. History, Scroll & Focus Policies

- **History Policy (`POPSTATE_TRANSITION_POLICY`):** `RESTORE_CONTEXT` (Subtle 120ms reverse cross-fade; never replays entry animation)
- **Scroll Restoration (`SCROLL_RESTORATION_POLICY`):** `TOP_ON_NEW_ROUTE` (Direct forward navigation scrolls to top; Back navigation restores prior reading depth)
- **Focus Management (`ROUTE_FOCUS_POLICY`):** Focus updates to destination `<h1>` (`tabindex="-1"`) to maintain accessibility hierarchy for screen readers and keyboard users
- **Deep Link & Refresh Parity:** Complete semantic HTML and CSS render on hard refresh and direct URL entry (`project-detail.html`) without router dependencies

---

## 4. Accessibility, Fallback & Lifecycle Teardown

- **Reduced Motion Strategy (`prefers-reduced-motion: reduce`):** Bypasses shared-element translation and scaling. Uses instantaneous route swap with opacity fade $\le 80\text{ms}$.
- **Mobile Strategy (`MOBILE_TRANSITION_POLICY`):** `SIMPLIFIED` (Hero image cross-fade without horizontal displacement on viewports $< 768\text{px}$).
- **Failure Fallback:** `STANDARD_NAVIGATION` (If native View Transitions are unsupported or disabled via `?forceTransitionFallback=1`, standard browser document navigation executes cleanly).
- **Subsystem Resource Cleanup:**
  - Three.js: Not required in this editorial build (`THREE_TRANSITION_LIFECYCLE = NOT_APPLICABLE`).
  - Rive: Not required in this editorial build (`RIVE_TRANSITION_LIFECYCLE = NOT_APPLICABLE`).


