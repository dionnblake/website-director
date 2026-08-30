# PRODUCTION QA CHECKLIST: PRE-FLIGHT VERIFICATION MATRIX

> **Version:** 1.7.0
> **Status:** Mandatory Pre-Deployment Gate
> **Rule:** Every checkbox must be validated and signed off in `templates/production-review.md`.
> **V2.10 Rule:** This checklist verifies the **release candidate** (Phase 12). It does **not** authorize deployment and does **not** verify production. "Authorized for deployment" here means the candidate is `RELEASE_READY`. Deployment authorization, production verification against a known release identity, rollback readiness, and post-launch observation are owned by **Phase 12.25** (`LAUNCH-OPERATIONS-PROTOCOL.md`, `launch_ops{}`). See §11.
> **V2.8 Rule:** Where a requirement can be verified by machine (horizontal overflow, console cleanliness, broken assets, reduced motion, form failure/success, route integrity, measurement events, browser-observable security), the sign-off requires the **machine evidence** produced by Phase 10.5 Browser & Regression QA (`§5.4`) — not an agent assertion. Avoid checkbox theater.
> **V2.9 Rule:** Accessibility is classified per criterion — `AUTO_VERIFIED` / `MANUAL_VERIFIED` / `BLOCKED` / `NOT_APPLICABLE` / `KNOWN_GAP` — against the **WCAG 2.2 AA** target (`§3`, `§5.5`, `ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md`). Untested criteria are never marked PASS. Website Director never records `ADA COMPLIANT`, `FULLY ACCESSIBLE`, `ACCESSIBILITY GUARANTEED`, or `WCAG COMPLIANT`.

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

## 3. Accessibility & Usability (WCAG 2.2 AA target — classify each row)

> Canonical authority: `ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md` (Phase 6.9 spec, Phase 10.5 verification). Full verification detail: §5.5. Classify every row `AUTO_VERIFIED` / `MANUAL_VERIFIED` / `BLOCKED` / `NOT_APPLICABLE` / `KNOWN_GAP`. This is a **technical target**, not a legal conformance statement.

- [ ] **Contrast (1.4.3 / 1.4.11):** Text meets `4.5:1` (`3:1` large); UI components, graphical objects, and focus indicators meet `3:1`. Verified by the Impeccable contrast scan + computed-style browser check — `AUTO_VERIFIED`.
- [ ] **Colour independence (1.4.1):** No error, status, selected, required, or chart-series meaning conveyed by colour alone.
- [ ] **Keyboard (2.1.1 / 2.1.2):** All functionality operable by keyboard where the interaction supports it; logical order; **no keyboard trap**. Automated trap heuristic + `MANUAL_VERIFIED` walkthrough.
- [ ] **Focus visible & not obscured (2.4.7 / 2.4.11 / 2.4.13):** Visible indicator on every control; focus not hidden behind sticky headers, consent banners, or drawers. Feasible cases `AUTO_VERIFIED`; the rest `MANUAL_VERIFIED`.
- [ ] **Modals & Dialogs:** Correct role, accessible name, initial focus, Escape closes and returns focus to the trigger, background inert.
- [ ] **Semantic structure (1.3.1 / 2.4.6):** Landmark regions present; one meaningful `<h1>`; heading hierarchy without skipped levels; native controls preferred over reconstructed ARIA.
- [ ] **Page language & title (3.1.1 / 2.4.2):** `<html lang>` set; unique non-empty `<title>` per page.
- [ ] **Names, roles, values (4.1.2 / 2.5.3):** Every interactive control exposes a name/role/state; the visible label is contained in the accessible name.
- [ ] **Reflow & zoom (1.4.4 / 1.4.10):** Content usable at 200% text zoom and reflows at 320 CSS px with no 2-D scroll (legitimate exceptions listed), no clipped text, no lost control, no hidden conversion path.
- [ ] **Text spacing (1.4.12):** Layout tolerates the WCAG text-spacing override with no loss — `AUTO_VERIFIED` via the synthetic fixture.
- [ ] **Target size (2.5.8):** No control below the WCAG `24 × 24 px` floor without an exception; adjacent targets meet the project minimum (`44 × 44 px` where approved).
- [ ] **Dragging (2.5.7):** Every drag interaction has a non-drag alternative — `NOT_APPLICABLE` where no drag exists.
- [ ] **Motion (2.2.2 / 2.3.1):** Reduced motion honoured; nothing flashes > 3×/s; autoplaying content > 5s is pausable; no meaning only in animation.
- [ ] **Images (1.1.1):** Meaningful images have meaningful contextual `alt`; decorative images use empty `alt`/`aria-hidden`; `alt` is not keyword-stuffed.
- [ ] **Media (1.2.x):** Captions / transcript / controls / keyboard access where media exists — `NOT_APPLICABLE` otherwise.
- [ ] **Forms (3.3.x / 1.3.5):** Persistent labels; required state in text; programmatic error association; error identification not by colour; focus to first error; an accessibility repair caused no false conversion success.
- [ ] **Status messages (4.1.3):** Required dynamic changes are announced with intentional politeness; no unnecessary live regions.
- [ ] **Accessible authentication (3.3.8):** Where auth exists — no cognitive-function test without an accessible alternative; paste allowed into password/OTP; security↔accessibility conflicts escalated, not silently resolved.
- [ ] **Consent UI:** Keyboard operable, screen-reader understandable, readable at zoom/reflow, non-deceptive, rejection as reachable as acceptance.
- [ ] **Screen-reader smoke (§5.5):** `MANUAL_VERIFIED` against the recorded environment, or `BLOCKED_SCREEN_READER_ENVIRONMENT` — **never PASS by default**.

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

## 5.1 Content Operations & CMS Verification (V2.13)

> Canonical architecture: `CONTENT-OPERATIONS-CMS-PROTOCOL.md`,
> `templates/content-model.md`, `templates/content-model.json`, and
> `templates/cms-decision.md`. V2.5 remains the authority for long-term client
> CMS operations, training, backup/restore, maintenance, cost records, and
> handoff acceptance.

- [ ] Content types and fields match the validated semantic model; no repeated
      entity is duplicated as presentation-coupled markup.
- [ ] Required fields, validation, character limits, relationships, taxonomy,
      SEO fields, media fields, and provenance references are implemented.
- [ ] Editable surfaces and roles are enforced. Editors cannot edit analytics
      event identifiers, structured-data schema, security headers, design
      tokens, canonical lock state, or other system-generated controls.
- [ ] Lifecycle behavior is verified: drafts/review/scheduled/archived content
      is not publicly listed or exposed, and published content resolves.
- [ ] Agent-generated content enters `DRAFT`; no autonomous agent can publish.
- [ ] Preview renders the real route and design system; raw JSON is not used
      as visual preview evidence.
- [ ] If scheduling exists, `SCHEDULED_AT`, `TIMEZONE`, `PUBLISHING_SYSTEM`,
      and `FAILURE_BEHAVIOR` are recorded. No unverified scheduler is claimed.
- [ ] Slugs are normalized and unique. Every published or archived slug change
      has a durable 301 redirect; archive, unpublish, and delete remain distinct.
- [ ] Rich text rejects scripts, inline CSS, unsafe URLs, arbitrary styling,
      and unvalidated embeds.
- [ ] Production media resolves to Asset Director identity and V2.12
      provenance. Research/inspiration references remain `REFERENCE_ONLY`.
- [ ] High-risk claims resolve to evidence; SEO strategy is consumed rather
      than re-authored; affiliate disclosure and freshness fields are present
      where applicable.
- [ ] Portability and migration records are complete, and provider lock-in is
      explicitly accepted rather than presented as an export guarantee.
- [ ] The deterministic result from `content-ops/validator.py` is attached to
      the review. `[CONTENT_OPERATIONS_READY]` is a readiness gate, not a
      sixth owner lock, and `content_ops.complete` does not prove production
      behavior.

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

## 5.3 Security, Privacy & Compliance Verification (V2.7)

Verified against `templates/security-privacy-review.md` under `SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md`. Skip only where `security_privacy.status = "not_required"` or `"exception"` with a recorded justification.

> **This section verifies technical implementation only. Do not mark legal compliance "PASS."** Permitted outcomes are `REQUIREMENTS REVIEWED`, `TECHNICAL CONTROLS IMPLEMENTED`, `KNOWN GAPS DOCUMENTED`, `LEGAL REVIEW REQUIRED`, and `COMPLIANCE_NOT_CERTIFIED`. `security_privacy.compliance_certified` remains permanently `false`.

### 5.3.1 Transport & HTTPS
- [ ] **Production HTTPS enforced.** Site is served over HTTPS.
- [ ] **HTTP redirects to HTTPS** on the production surface.
- [ ] **Zero mixed content** — no script, style, image, font, media, or XHR over plaintext (inspect the network panel, not just the source).
- [ ] **Canonical URLs, `og:url`, sitemap entries, and JSON-LD use HTTPS production origins.**
- [ ] Localhost/development HTTP is **not** recorded as a defect.

### 5.3.2 Security Headers
- [ ] Each header specified in `security-privacy-review.md` §16 is present on the production response with the specified value.
- [ ] **CSP was not widened** to `unsafe-inline`, `unsafe-eval`, or `*` to make the build pass.
- [ ] Every origin allowed by the CSP corresponds to a declared third-party inventory entry.
- [ ] Any header the deployment platform cannot set is **recorded as an escalation**, not silently omitted.

### 5.3.3 Secrets Exposure
- [ ] **Zero secrets in the client bundle** — grep the built output for key/token patterns and the declared secret names.
- [ ] **Zero secrets in source control**, including fixtures, tests, and config files.
- [ ] `.env.example` contains names and placeholders only — no real values.
- [ ] No secret appears in console output, error responses, network payloads, evidence captures, or screenshots.
- [ ] Feature depending on an absent required secret **fails closed**; core content remains functional.

### 5.3.4 Form Security
- [ ] **Server-side validation enforced.** Submit a payload that bypasses client-side validation and confirm the server rejects it.
- [ ] **Client-only trust boundaries absent** — no hidden field, disabled control, or client flag relied upon for authorization or safety.
- [ ] CSRF protection active where specified.
- [ ] Rate limiting / abuse prevention active where specified.
- [ ] Error responses are non-revealing — no stack traces, database errors, or framework internals.
- [ ] **No sensitive values in URLs** — query strings, path segments, fragments, or redirect targets.
- [ ] File-upload restrictions enforced where uploads exist (type allow-list, size limit, content-type validation, safe filename).
- [ ] Duplicate submission does not create duplicate records or duplicate conversion events.
- [ ] **A server-rejected submission renders no success state.**

### 5.3.5 Authentication & Session (where applicable)
- [ ] Session cookies carry `HttpOnly`, `Secure`, and the specified `SameSite` value — verified in the browser, not in source.
- [ ] Logout invalidates the session server-side (a replayed cookie is rejected).
- [ ] Protected resources authorize server-side per request.
- [ ] Brute-force throttling active on credential endpoints.

### 5.3.6 Third-Party Scripts
- [ ] **Every third-party script loaded by the build appears in `security-privacy-review.md` §9.** An undeclared script is a FAIL.
- [ ] Route-scoped scripts do not load globally.
- [ ] **External dependency failure tested:** blocking each third-party origin leaves navigation, content, and forms functional.

### 5.3.7 Cookies & Browser Storage
- [ ] Every cookie and storage key written by the build appears in `security-privacy-review.md` §11.
- [ ] Specified cookie attributes and lifetimes are applied.
- [ ] Nothing outside the essential set is written before consent where consent is `REQUIRED`.

### 5.3.8 Consent Behavior
- [ ] Where consent is `REQUIRED`: consent-dependent scripts do not execute and consent-dependent storage is not written before consent — verified by observing network and storage on first load.
- [ ] **Rejection is as reachable as acceptance** — same interaction count, same discoverability, comparable prominence.
- [ ] No prechecked optional consent, no deceptive wording, no hidden opt-out, no unauthorized consent wall.
- [ ] Consent UI is keyboard operable and focus-managed with no keyboard trap.
- [ ] Consent state survives client-side route transitions without re-prompting or silently re-enabling tracking.

### 5.3.9 Analytics Privacy Dependency
- [ ] **No PII in any analytics payload** — inspect actual network payloads, not source code.
- [ ] Validation-error events carry field category only.
- [ ] Where the specification recorded `ACTIVATION_BLOCKED_PENDING_PRIVACY`, the integration is **not active** in the build.
- [ ] `security_privacy.consent_status` and `measurement.consent_dependency` agree.

### 5.3.10 Disclosures & Legal Surfaces
- [ ] **Affiliate disclosure present** at the specified placement, visible without interaction, legible at body-copy standard.
- [ ] Sponsored units are visually distinguishable from independent editorial content.
- [ ] **Privacy notice route exists and resolves** where the specification requires one.
- [ ] Legal/disclosure links in the footer and inline surfaces resolve — zero 404s, zero `#` placeholders.
- [ ] No unevidenced compliance badge, seal, or certification mark is rendered.

### 5.3.11 Console, Network & Configuration Leakage
- [ ] Console is free of credential material, personal data, and internal detail.
- [ ] Network responses do not leak internal paths, stack traces, or configuration.
- [ ] **Production configuration verified:** debug endpoints, verbose logging, seeded test data, mock services, and development credentials are absent from production.
- [ ] **Environment separation confirmed** — production does not read configuration from committed files.

### 5.3.12 Status Recording
- [ ] `security_privacy.implementation_verified` set **only** on build inspection plus browser/network evidence stored in the project evidence directory.
- [ ] `security_privacy.production_verified` remains `false` unless production evidence exists. Absent evidence is reported as `NOT_YET_VERIFIED`, never as passing.
- [ ] `security_privacy.compliance_certified` is `false`. **No legal compliance claim recorded anywhere in the sign-off.**
- [ ] **Blocked items remain honestly blocked** — `security_privacy.blocked_reason` is present and surfaced in handoff, not quietly cleared.
- [ ] Known gaps and escalations are carried into `templates/production-review.md` and client handoff rather than closed silently.
- [ ] No external side effects occurred: no live site modified, no deployment triggered by this checklist, no consent platform configured, no DNS changed, no payment account touched, no production credentials used, no intrusive testing performed.

---

## 5.4 Browser & Regression QA Evidence (V2.8)

Verified against `templates/browser-qa-plan.md` / `browser-qa-manifest.json` under `BROWSER-REGRESSION-QA-PROTOCOL.md`. Phase 10.5 runs before this checklist. Skip only where `browser_qa.exception.applied = true` with a recorded justification. **A `BLOCKED` result is reported as blocked — never as passing. A `FLAKY` result is not a pass.**

### 5.4.1 Run Integrity
- [ ] `browser_qa.complete = true`, produced by a real-browser `BROWSER_QA_ENGINE` (`browser_qa.engine` names it). A `simulation` dry run does not satisfy this.
- [ ] `browser_qa.frozen_fixture_integrity = "PASS"` — the QA run mutated nothing under `projects/` or any frozen path.
- [ ] `browser_qa.flaky_tests` is empty, or each entry is triaged and owner-acknowledged.
- [ ] Machine evidence manifest (`<run_id>.evidence.json`) and summary stored in the project evidence directory and referenced here.

### 5.4.2 Machine-Verified Requirements (evidence, not assertion)
- [ ] **Horizontal overflow:** zero at every required viewport class — real overflow, not `overflow-x: hidden` masking.
- [ ] **Console cleanliness:** zero `APPLICATION_DEFECT` errors; every ignore is a justified, owned manifest entry.
- [ ] **Network:** zero unexplained 4xx/5xx or aborted critical assets; each allowed third-party failure is justified and the site stays functional when that origin is blocked.
- [ ] **Broken assets:** zero broken images/fonts/scripts/styles; images render with non-zero dimensions; critical hero and mobile/reduced-motion fallback assets load; no accidental placeholder images.
- [ ] **Navigation:** internal routes resolve; no unintentional `#` links; mobile nav opens and closes on route change; Escape/click-outside per spec; custom 404 resolves.
- [ ] **Forms:** labels present; invalid submit shows a visible error; duplicate submit prevented; **a server-rejected submission renders no success state and emits no success conversion event**; keyboard submit works.
- [ ] **Measurement:** required events fire exactly once with required params; no undeclared event; **no PII in any payload or UTM** (network payloads inspected).
- [ ] **Reduced motion:** motion-heavy surfaces remain meaningful under `prefers-reduced-motion: reduce`; no content permanently hidden awaiting animation; evidence screenshots captured.
- [ ] **Keyboard smoke:** primary nav and CTA reachable; visible focus; no obvious keyboard trap; menu/dialog controls operable.
- [ ] **Security (browser-observable):** required headers present; no mixed content; no secret-shaped values in the DOM/bundle; runtime third-party scripts match the approved inventory; where consent is `REQUIRED`, tracking is inactive before consent and rejection is reachable; disclosure/privacy routes resolve.

### 5.4.3 Visual Regression
- [ ] `browser_qa.visual_regression_status` is `"MATCH"`, or every `"DIFF_DETECTED"` surface is owner-reviewed and the baseline update is authorised in `browser-qa-manifest.json`.
- [ ] No baseline was silently overwritten; masks are narrow and justified.

### 5.4.4 Local vs. Production
- [ ] `browser_qa.implementation_verified` set only on real-browser evidence against a local/staging build.
- [ ] `browser_qa.production_verified` remains `false` unless the run executed against the real production URL. Absent evidence is reported as `NOT_YET_VERIFIED`, never as passing.
- [ ] Cross-browser: for a release, the interaction subset was run on Chromium + Firefox + WebKit, or "Chromium only" is explicitly recorded — no unqualified "cross-browser verified" claim.

---

## 5.5 Accessibility Verification (V2.9)

Verified against `templates/accessibility-review.md` / `accessibility-test-manifest.json` under `ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md`. Phase 6.9 produced the spec; Phase 10.5 ran the automated portion. Skip only where `accessibility.exception.applied = true` with a recorded justification.

> **Target: WCAG 2.2 AA (technical).** Permitted wording: `WCAG 2.2 AA TARGET TESTS PASSED`, `MANUAL REVIEW COMPLETED`, `KNOWN ACCESSIBILITY GAPS = NONE OBSERVED`, `BLOCKED_SCREEN_READER_ENVIRONMENT`. Never `ADA COMPLIANT` / `FULLY ACCESSIBLE` / `WCAG COMPLIANT`.

### 5.5.1 Run integrity
- [ ] `accessibility.complete = true` (spec) exists, and the Phase 10.5 accessibility assertion group ran against a real browser.
- [ ] `accessibility.automated_engine` names the engine and version (e.g. `axe-core 4.10.2`), or `BLOCKED_ACCESSIBILITY_ENGINE_UNAVAILABLE` is recorded — **not** reported as a pass.
- [ ] `browser_qa.frozen_fixture_integrity = "PASS"` for the run.
- [ ] Machine evidence manifest and manual notes stored in the project evidence directory.

### 5.5.2 Automated (`AUTO_VERIFIED` — machine evidence)
- [ ] Accessibility engine reports **no violations at or above the configured severity** (default: moderate), or each is a recorded `KNOWN_GAP` / `exception`.
- [ ] Missing accessible names, colour-only state heuristics, computed contrast, focus visibility, keyboard-trap heuristic, landmarks/heading order, page `lang`/`<title>`, reflow at target width, text-spacing override, small/tiny targets, dialog mechanics, and form label/error association all pass.
- [ ] Zero automated violations is **not** recorded as "WCAG conformant" — automated tooling covers a fraction of the criteria.

### 5.5.3 Manual (`MANUAL_VERIFIED` — documented human verification)
- [ ] Keyboard walkthrough per route: tab order, activation, Escape, arrow-key composite widgets, focus return, skip link.
- [ ] Focus-not-obscured cases the engine flagged `MANUAL_REQUIRED`.
- [ ] 200% zoom / 320px reflow / text-spacing review by a human.
- [ ] Media review (captions/transcript/controls) where media exists.
- [ ] Error prevention proportionality on consequential submissions.

### 5.5.4 Screen reader
- [ ] Bounded screen-reader smoke completed against the recorded environment (title, landmarks, headings, navigation, primary CTA, form, error, dialog, dynamic status, media) → `accessibility.screen_reader_verified = true`.
- [ ] **Or** `BLOCKED_SCREEN_READER_ENVIRONMENT` recorded, carried into `known_gaps` and client handoff — never closed silently.

### 5.5.5 Status recording
- [ ] `accessibility.automated_verified` set **only** on real-browser engine evidence.
- [ ] `accessibility.manual_verified` set **only** on documented human verification; an engine-clean run with a failing manual keyboard review is **not** a full PASS.
- [ ] `accessibility.production_verified` remains `false` unless owner-supplied production evidence exists — absent evidence is `NOT_YET_VERIFIED`, never passing.
- [ ] `accessibility.known_gaps` and exceptions carried into `templates/production-review.md` and client handoff.
- [ ] No external side effects: no deploy, no consent-platform change, no intrusive tooling against third-party systems.

---

## 6. Website Gauntlet Verification (V1.3)
- [ ] **Deterministic Browser QA Cleared First:** `browser_qa.complete = true` (or recorded `blocked`/`exception`) before the Gauntlet ran — the Gauntlet does not evaluate a build with broken navigation, JS exceptions, missing assets, failed forms, or obvious responsive overflow.
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

## 9. Final Sign-Off & Release Candidate Readiness
- [ ] **Design Review Score:** $\ge 90$ points achieved in `templates/design-review.md`.
- [ ] **Website Gauntlet Verdict:** `GAUNTLET_PASS` or authorized exception.
- [ ] **Pre-Flight Review Documented:** All items above signed off in `templates/production-review.md`.
- [ ] **Release Worktree Tagged:** Git branch/tag prepared. This produces a **release candidate**, not a deployment — the immutable release identity is recorded in `LAUNCH-OPERATIONS-PROTOCOL.md` §8 / `launch-plan.md` §1.
- [ ] **Candidate is `RELEASE_READY`, not `DEPLOYMENT_AUTHORIZED`.** Deployment authorization is an explicit per-release owner act performed in Phase 12.25 (§11) — never inferred from this checklist passing.

---

## 10. Production Build Integrity (Candidate)
- [ ] **Build Validation:** Production bundle compiles cleanly (`npm run build` or framework equivalent) without warnings or lint errors.
- [ ] **Asset Minification:** CSS and JavaScript bundles are minified and tree-shaken.
- [ ] **Environment Variables:** All development API keys and mock URLs replaced with production configurations, and **no secret value is committed** — see §5.3.3 and §5.3.11.

---

## 11. Launch & Post-Launch Operations Boundary (V2.10)

> Owned by `LAUNCH-OPERATIONS-PROTOCOL.md` (Phase 12.25). This checklist (Phase 12) verifies the **candidate**; Launch Operations verifies the **deployed artifact on production**. Do not duplicate the checkbox sets — the division is:

| Concern | Owner |
| :--- | :--- |
| Candidate compiles, passes QA, Gauntlet, pre-flight, is a tagged release candidate | **Phase 12 (this checklist)** |
| Immutable release identity, release candidate freeze | Phase 12.25 |
| Owner deployment authorization (`RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED`) | Phase 12.25 — explicit owner act |
| Deployment itself | **External** — the owner or an owner-authorised operator; Website Director never deploys |
| Production verification against `deployed_sha == release_sha` on the production surface | Phase 12.25 |
| DNS / TLS realised behaviour, redirect verification, cache/CDN, production assets | Phase 12.25 |
| Production Browser QA (V2.8 harness, `environment = "production"`) | Phase 12.25 |
| Production accessibility / security-privacy / measurement / SEO re-verification | Phase 12.25 (writes the canonical `*.production_verified` fields) |
| Error-monitoring readiness, rollback plan, rollback triggers, rollback testing | Phase 12.25 |
| Post-launch observation window, incident model, stabilization | Phase 12.25 |
| Long-term client operations, CMS, maintenance, documentation, transfer | Phase 12.5 (`CLIENT-CMS-HANDOFF-PROTOCOL.md`) |

- [ ] Phase 12.25 launch plan (`templates/launch-plan.md`) and evidence manifest exist where the project will be deployed or re-launched.
- [ ] `launch_ops.complete` recorded honestly — it means the launch **plan** is complete, never that the site is deployed, production verified, or stabilised.
- [ ] No `production_*_verified` flag was set from a localhost or staging run.

## 5.6 Evidence, Claim & Asset Provenance (V2.12)

- [ ] Every production claim has an EVIDENCE_REF resolving to a recorded
      source, evidence strength, support match, owner, and review date.
- [ ] Every production asset has an asset-level provenance_ref resolving to
      the same ASSET_ID in the evidence ledger.
- [ ] Asset Director assets.provenance_status and cross-cutting
      provenance.complete are both recorded distinctly; one does not imply the
      other.
- [ ] Stock, open-license, public-domain, commissioned, third-party brand,
      font, icon, screenshot, quoted, and AI-generated material has evidence
      of permitted use appropriate to its risk.
- [ ] Required attribution is present. Unknown, stale, contradicted,
      ambiguous, unverified, or hash-mismatched records are BLOCKED or FAIL.
- [ ] Research and showcase references remain REFERENCE_ONLY and are not
      promoted into production assets.
- [ ] The deterministic result from provenance/validator.py is attached to
      the review. implementation_verified and production_verified remain
      separate evidence states.

The canonical provenance gate is EVIDENCE_PROVENANCE_READY. It is a readiness
gate, not a sixth owner lock. Deployment remains governed by Launch Ops and
requires owner authorization.
