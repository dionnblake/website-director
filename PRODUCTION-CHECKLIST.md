# PRODUCTION QA CHECKLIST: PRE-FLIGHT VERIFICATION MATRIX

> **Version:** 1.3.0
> **Status:** Mandatory Pre-Deployment Gate
> **Rule:** Every checkbox must be validated and signed off in `templates/production-review.md`.

---

## 1. Viewport & Cross-Device Ergonomics
- [ ] **Desktop (1440px+):** Layout uses max-width containers properly; no awkward stretched lines or oversized margins.
- [ ] **Laptop (1024px - 1280px):** Content scales smoothly; horizontal menus and split grids do not collide.
- [ ] **Tablet (768px - 1023px):** Multi-column grids reflow cleanly (typically into 2-column or structured 1-column layouts).
- [ ] **Mobile (375px - 428px):** Zero horizontal scrollbar/overflow (`overflow-x: hidden` verified).
- [ ] **Touch Targets:** All clickable/tappable elements (buttons, links, form inputs) are at least `44px x 44px`.

---

## 2. Interactive Systems & Controls
- [ ] **Navigation & Menus:**
  - Desktop nav links route correctly.
  - Sticky nav transition triggers smoothly on scroll.
  - Mobile hamburger menu opens, locks body scroll, closes on click-outside, and closes on route change.
- [ ] **Forms & Inputs:**
  - All input fields have visible labels or accessible `aria-label` attributes.
  - Custom focus rings are high contrast and visible on keyboard tab navigation.
  - Inline validation triggers on invalid submit with clear, helpful error copy.
  - Submit buttons display loading/disabled states during submission.
  - Success confirmation / thank-you state is presented upon successful submission.
- [ ] **Links & Buttons:**
  - All external links have `rel="noopener noreferrer"` and `target="_blank"` where appropriate.
  - Zero dead or `#` placeholder links.
  - Distinct `hover`, `active`, `focus-visible`, and `disabled` visual states exist for every button variant.

---

## 3. Accessibility & Usability (WCAG 2.1 AA)
- [ ] **Contrast Compliance:** All text colors meet minimum contrast ratio of `4.5:1` against their backgrounds (`3:1` for large display headings).
- [ ] **Keyboard Navigation:** Full page can be traversed using `Tab` / `Shift+Tab`; focus order follows logical visual reading order.
- [ ] **Modals & Dialogs:** Traps focus when opened; pressing `Escape` closes the modal and returns focus to the trigger element.
- [ ] **Semantic Structure:** Exactly one `<h1>` tag per page; headings (`<h2>`, `<h3>`, `<h4>`) follow a strict hierarchical structure without skipping levels.
- [ ] **Media Descriptions:** All `<img>` elements possess descriptive, contextual `alt` text (empty `alt=""` only for purely decorative SVG shapes with `aria-hidden="true"`).

---

## 4. Performance, Assets & Core Web Vitals
- [ ] **Largest Contentful Paint (LCP):** Under `2.5s` on mobile networks.
- [ ] **Cumulative Layout Shift (CLS):** Under `0.1`. All images, videos, and embeds have explicit `width` and `height` (or aspect-ratio CSS).
- [ ] **Interaction to Next Paint (INP):** Under `200ms`.
- [ ] **Image Optimization:** Images served in modern formats (`WebP` / `AVIF`), appropriately compressed, with `loading="lazy"` on below-the-fold assets.
- [ ] **Font Loading Strategy:** Fonts use `font-display: swap;` with preconnect headers for external font CDNs to prevent Flash of Invisible Text (FOIT).
- [ ] **Console Cleanliness:** Zero uncaught JavaScript errors, failed network requests (404s), or React/DOM hydration warnings in browser developer console.

### 4.1 Motion Level 2–3 Performance Budget (V1.1)
Applies only when `motion.level` is `MOTION_LEVEL_2` or `MOTION_LEVEL_3` per `MOTION-DIRECTION-PROTOCOL.md`. These are additive to §4 above, not a replacement for it.
- [ ] **Hero Asset Budget:** Total hero frame-sequence/video payload documented in `templates/motion-direction.md` §4 and verified against the stated budget before shipping.
- [ ] **Preload Strategy:** Frames/assets load progressively with a visible loading state; first-frame paint does not wait on the full sequence.
- [ ] **Mobile Asset Reduction:** A lighter asset set (or a static fallback) is served on mobile/constrained networks — verified, not assumed.
- [ ] **JavaScript Weight:** Animation library payload (GSAP/ScrollTrigger, etc.) is accounted for in bundle size; no duplicate animation libraries loaded.
- [ ] **`prefers-reduced-motion` Verified in Browser:** Toggling the OS/browser reduced-motion setting actually suppresses the scroll-driven/hero animation and reveals the static fallback with equivalent meaning — confirmed by testing, not just present in code.
- [ ] **Core Web Vitals Hold Under Motion:** LCP/CLS/INP thresholds in §4 above are re-verified specifically on the motion-heavy pages, not only on motion-free pages of the same site.

### 4.2 Immersive 3D & WebGL Production Verification (V2.1)
Applies when `immersive.status = "implementation_ready"` per `IMMERSIVE-WEB-PROTOCOL.md`.
- [ ] **Semantic DOM Parity:** 100% of primary headlines, copy, CTAs, and specifications exist in accessible semantic HTML outside the canvas.
- [ ] **Zero-CLS 2D Fallback:** Verified that disabling WebGL or testing with `?forceWebGLFallback=1` displays an instantaneous 2D fallback graphic without layout shift.
- [ ] **Bounded DPR Enforced:** Verified that renderer caps DPR to `<= 2.0` on desktop and `<= 1.5` on mobile devices.
- [ ] **Mobile Policy Active:** Verified `MOBILE_3D_POLICY` (`FULL`, `SIMPLIFIED`, `STATIC_RENDER`, or `DISABLED`) functions correctly at 390px viewport with touch-safe scrolling.
- [ ] **Reduced Motion Active:** Verified `(prefers-reduced-motion: reduce)` halts continuous scene rotation and camera sweeps.
- [ ] **Lifecycle Cleanup Implemented:** Verified Three.js disposal routines (`disposeScene()`) release geometries, materials, textures, and event listeners on teardown.
- [ ] **Visibility Throttling:** Verified rendering loop pauses when `document.hidden === true`.

### 4.3 Asset Director Quality & Provenance Verification (V2.0)
Applies to all visual media implemented per `ASSET-DIRECTOR-PROTOCOL.md`:
- [ ] **Asset Manifest Integrity:** All production assets exist in `templates/asset-manifest.json` with valid paths, formats, dimensions, and file sizes.
- [ ] **Master/Web Separation:** Source files in `assets/source/` remain uncompressed and untouched; web pages reference only optimized files in `assets/web/`.
- [ ] **Hero Asset Strength:** Hero image satisfies `HERO_ASSET_STRENGTH` with verified text-safe contrast and crisp mobile reflow.
- [ ] **Signature Asset Present:** For `SHOWCASE` projects, the dedicated signature asset is produced and integrated.
- [ ] **AI Artifact Clearance:** All generated images verified 100% free of AI defects (`AI_ARTIFACT_CHECK = PASS`).
- [ ] **Factual Authenticity:** Zero fake AI customers, facilities, staff, or clinical metrics presented as factual evidence (`FACTUAL_EVIDENCE_MEDIA` verified authentic).
- [ ] **Stock Discipline:** Zero generic corporate stock photos present.
- [ ] **Provenance & Licensing:** All external assets possess verified commercial licenses in `templates/asset-provenance.md`; zero stolen/copied reference gallery media.
- [ ] **Responsive `<picture>` Verification:** Responsive crops physically verified on desktop (1440px), tablet (768px), and mobile (390px) viewports.

---

## 5. SEO, Metadata & Social Sharing
- [ ] **Title Tag:** Unique, compelling, under 60 characters with primary brand and value proposition.
- [ ] **Meta Description:** Engaging, under 160 characters summarizing the page's core benefit.
- [ ] **Canonical URL:** Configured to avoid duplicate content penalties.
- [ ] **Open Graph Tags:** `og:title`, `og:description`, `og:type`, and `og:url` present and verified.
- [ ] **Social Share Image:** `og:image` is high resolution (`1200x630px`), properly hosted, and tested via social preview debuggers.
- [ ] **Favicon Package:** Favicon `.ico`, `apple-touch-icon.png`, and SVG vector icon configured in `<head>`.
- [ ] **Custom 404 Page:** Bespoke, helpful error page matching design system with clear navigation back to home.

### 5.1 SEO Strategy Fidelity (V1.2)
Verifies the build matches the locked SEO specification (`templates/keyword-map.md`, `templates/seo-content-briefs.md`). This is implementation verification, not a re-run of SEO strategy — a failure here means the build drifted from the spec, not that the spec should be redone (redoing the spec means reopening `SEO-INTELLIGENCE-PROTOCOL.md` explicitly).
- [ ] **Approved Pages Exist:** Every page in `keyword-map.md` §1 is built; no unapproved page was added.
- [ ] **Page/Keyword Mapping Preserved:** Each page's shipped title/H1/content targets the primary keyword and intent assigned in `keyword-map.md`.
- [ ] **Search Intent Preserved:** Page type matches assigned intent (informational → guide/hub, transactional → service/product page, navigational → homepage/brand page, local → location page only where a real presence exists).
- [ ] **Unique Title Tags:** No two pages share a title tag.
- [ ] **Heading Hierarchy Sensible:** One meaningful `<h1>` per page; `h2`–`h4` follow without skipping levels.
- [ ] **Internal Links Implemented:** Per `keyword-map.md` §2 Internal Link Targets.
- [ ] **Canonicals Correct:** Every page has a correct self-referencing or intentional cross-page canonical.
- [ ] **Sitemap Correct:** XML sitemap lists exactly the approved page set, no more, no fewer.
- [ ] **Robots Directives Correct:** No accidental `noindex`/`nofollow` on a page intended to rank.
- [ ] **Structured Data Valid:** JSON-LD present only where `seo-content-briefs.md` specifies it, and validates against schema.org.
- [ ] **Images Have Meaningful Alt Text:** Where appropriate — not keyword-stuffed alt attributes.
- [ ] **Important Content Rendered/Crawlable:** No SEO-critical content hidden behind client-side-only rendering a crawler cannot see.
- [ ] **No Obvious Keyword Stuffing:** Spot-check copy against `SEO-INTELLIGENCE-PROTOCOL.md` §11 — natural language, not repeated exact-match phrases.
- [ ] **No Duplicate/Thin Pages:** Every shipped page has a stated purpose in `keyword-map.md`; none exist solely because a keyword was noticed during build.

---

## 5.2 Conversion & Analytics Verification (V2.6)

Verified against `templates/measurement-plan.md` under `CONVERSION-ANALYTICS-PROTOCOL.md`. Skip only where `measurement.mode = "not_required"` or `"exception"` with a recorded justification. **A blocked integration is reported as blocked — never as passing.**

### 5.2.1 Loading & Library Integrity
- [ ] Analytics loads correctly in the built artifact (or is honestly recorded as deferred/blocked).
- [ ] **No duplicate analytics libraries** are present. Exactly one instance of the provider runtime.
- [ ] Site remains 100% functional — navigation, forms, CTAs, motion, styling — with analytics blocked or disabled.

### 5.2.2 Event Firing Correctness
- [ ] Every event required by the measurement plan **fires** on its specified trigger.
- [ ] Every event fires **exactly once** per qualifying interaction (verified under rapid repeat interaction).
- [ ] Event names match `measurement-plan.md` **exactly** — no drift, no vendor name leaking into application code.
- [ ] All `required_parameters` are present on every emission.
- [ ] No event exists in the build that is absent from the measurement plan.

### 5.2.3 CTA Mapping
- [ ] Every CTA event maps to the **correct control**. No event bound to the wrong button.
- [ ] Every primary and meaningful secondary CTA in `content-plan.md` has working instrumentation or a recorded `MEASUREMENT: NOT_REQUIRED`.

### 5.2.4 Form Integrity
- [ ] **Form start is not confused with form success.** `lead_form_start` fires on first interaction; the success event does not.
- [ ] **Failed forms do not generate successful conversion events.** Submit with a server-rejected payload and confirm no success conversion event is emitted.
- [ ] Rejected submissions emit the specified failure/validation event instead.
- [ ] Rapid repeat submit clicks do not emit multiple conversion events.

### 5.2.5 Affiliate Integrity
- [ ] Affiliate outbound events fire correctly on genuine external affiliate links.
- [ ] **Internal navigation is not mislabelled as outbound affiliate activity** (hostname resolved, not substring matched).
- [ ] No `affiliate_conversion` or `affiliate_commission` event is emitted from a click.

### 5.2.6 Attribution
- [ ] UTM handling matches the measurement plan's Attribution / UTM Strategy.
- [ ] Required campaign parameters survive client-side route transitions.
- [ ] No PII appears in any UTM parameter.

### 5.2.7 Route Measurement
- [ ] SPA route transitions are measured where required.
- [ ] A single route transition emits **exactly one** `page_view` across document navigation, View Transitions callbacks, and `popstate`.

### 5.2.8 Privacy & Secrets
- [ ] **No analytics secrets are exposed** — no API keys, tokens, or service-account credentials in source control or the built bundle.
- [ ] **No PII is present in any tracked payload** — inspect actual network payloads, not just source code.
- [ ] Validation-error events carry field category only, never field values.
- [ ] Consent dependency is respected as recorded (`REQUIRED` / `NOT_REQUIRED` / `UNASSESSED`).
- [ ] Session replay remains `DISABLED` unless explicitly justified with a masking policy.

### 5.2.9 Status Recording
- [ ] `measurement.implementation_verified` set **only** on browser + network evidence, stored in the project evidence directory.
- [ ] **Production verification status recorded honestly.** `measurement.production_verified` remains `false` unless owner-supplied production evidence exists. Absent evidence is reported as `NOT_YET_VERIFIED`, never as passing.
- [ ] **Blocked integrations remain honestly blocked** — `measurement.blocked_reason` is present and surfaced in handoff, not quietly cleared.
- [ ] No external side effects occurred: no analytics properties created, no tag manager or ad accounts modified, no pixels installed on live sites, no owner credentials used.

---

## 6. Website Gauntlet Verification (V1.3)
- [ ] **Adversarial Critic Sign-Off:** Phase 11.5 Website Gauntlet report generated (`templates/website-gauntlet-report.md`).
- [ ] **Subsystem Status Verified:** `site-profile.json` → `gauntlet.status` is `GAUNTLET_PASS`, owner-accepted `GAUNTLET_CAP_REACHED`, or documented `GAUNTLET_EXCEPTION_APPLIED`.
- [ ] **Builder/Critic Separation Maintained:** Evaluators inspected actual rendered output in fresh context against named Reference Bars.
- [ ] **Lock Invariant Preserved:** No locked tokens or decisions were mutated during refinement without explicit Owner Change Authorization.
- [ ] **Residual Defects Triaged:** Any non-blocking residual defects logged and escalated to Owner review.

---

## 7. UI Hardening & Edge-Case Resilience (Impeccable Quality Engine)
- [ ] **Extreme Text Handling:** Interface tested with extra-long strings; multi-line clamps (`-webkit-line-clamp`) or graceful wraps verified with zero layout clipping.
- [ ] **Empty & Error States:** Robust empty state placeholders and inline error messages present for dynamic components.
- [ ] **Browser Surfaces Themed:** `::selection`, custom scrollbars, carets, and `:focus-visible` rings explicitly styled from tokens (`IMPECCABLE-ENGINE-PROTOCOL.md` §4.2).
- [ ] **Tabular Numerals on Data:** Pricing, statistics, and counter metrics declare `font-variant-numeric: tabular-nums`.
- [ ] **Transition Performance Clean:** Zero CSS transitions on layout properties (`width`, `height`, `margin`, `top`); transitions restricted to `transform` and `opacity`.
- [ ] **Contrast Surface Harmony:** Secondary copy on colored surfaces tinted from background/foreground hues; zero muddy `gray-on-color` contrast failures.

---

## 8. Creative Intent Fidelity Verification (V1.8)
- [ ] **Commercial Objective Met:** Finished site structure and primary CTA directly execute `templates/creative-intent-contract.md` §1 (`PROJECT_PURPOSE` & `PRIMARY_CONVERSION`).
- [ ] **First-3-Second Impression Aligned:** Emotional posture matches confirmed `DESIRED_FIRST_3_SECOND_FEELING` in `creative-intent-contract.md` §3.
- [ ] **Anti-Brand Boundaries Respected:** Zero elements present that violate confirmed negative boundaries (`creative-intent-contract.md` §5).
- [ ] **Creative Ambition Satisfied:** Visual intensity and craft match confirmed `CREATIVE_AMBITION` (`STANDARD`, `PREMIUM`, `SHOWCASE`, `EXPERIMENTAL`) in `creative-intent-contract.md` §4.
- [ ] **Owner Non-Negotiables Honored:** All constraints in `creative-intent-contract.md` §7 verified in shipping codebase.

---

## 9. Final Sign-Off & Deployment Authorization
- [ ] **Design Review Score:** $\ge 90$ points achieved in `templates/design-review.md`.
- [ ] **Website Gauntlet Verdict:** `GAUNTLET_PASS` or authorized exception.
- [ ] **Pre-Flight Review Documented:** All items above signed off in `templates/production-review.md`.
- [ ] **Release Worktree Tagged:** Git branch/tag prepared for deployment.

---

## 10. Production Build & Deployment Integrity
- [ ] **Build Validation:** Production bundle compiles cleanly (`npm run build` or framework equivalent) without warnings or lint errors.
- [ ] **Asset Minification:** CSS and JavaScript bundles are minified and tree-shaken.
- [ ] **Environment Variables:** All development API keys and mock URLs replaced with production configurations.
