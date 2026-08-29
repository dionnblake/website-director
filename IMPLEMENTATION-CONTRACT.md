# IMPLEMENTATION CONTRACT: THE DESIGN-TO-CODE GOVERNANCE PROTOCOL

> **Version:** 1.4.0
> **Status:** Legally Binding Execution Standard for Coding Agents
> **Rule:** Separation of Design Authority from Implementation Execution.

---

## 1. The Separation Principle

In the Website Director framework, **Design** and **Implementation** are strictly decoupled phases executed under separate authority regimes:

```
┌────────────────────────────────────────────────────────┐
│                   DESIGN AUTHORITY                     │
│  (Website Director Specification & Token Architecture) │
└───────────────────────────┬────────────────────────────┘
                            │
              5 MANDATORY LOCKS ACHIEVED
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                IMPLEMENTATION AUTHORITY                │
│       (Coding Agent: Pixel-Perfect Translation)        │
└────────────────────────────────────────────────────────┘
```

**The Core Law:** An implementation coding agent is a master builder, NOT a visual designer. The coding agent must never improvise colors, margins, fonts, layouts, or visual motifs on the fly.

---

## 2. The Five Mandatory Design & Motion Locks

Implementation may NOT commence until all five gates in `site-profile.json` → `locks{}` evaluate to `true` and the corresponding artifacts are approved. (`research.complete` must also be `true`, or carry a recorded exception, before Gate 1 — see `VISUAL-RESEARCH-PROTOCOL.md` §4–5 — but it is a readiness precondition, not a sixth lock; see `SKILL.md` §5.2.)

| Lock Name | Source Artifact | Description of Lock Requirement |
| :--- | :--- | :--- |
| **Gate 1: `design_direction_locked`** | `templates/design-direction.md` | Archetype blend, brand posture, visual theme, and mood criteria approved. |
| **Gate 2: `information_architecture_locked`**| `templates/information-architecture.md`| Exact page layout, section sequence, content objectives, and conversion flow approved. |
| **Gate 3: `content_structure_locked`** | `templates/content-plan.md` | Real headlines, proof points, copy hierarchy, and CTA text written and locked. |
| **Gate 4: `design_system_locked`** | `templates/design-system.md` | Complete token mapping (colors, typography, spacing, geometry, components) locked. |
| **Gate 5: `motion_direction_locked`** | `templates/motion-direction.md` | Motion level (0–3), hero/scroll/hover behavior, and reduced-motion/mobile fallbacks approved. If a cinematic specialist was engaged, `templates/cinematic-brief.md` must also be complete. |

---

## 2.1 Builder SEO Requirements (V1.2)

Gates 2 and 3 above are additionally sourced from `templates/keyword-map.md` and `templates/seo-content-briefs.md` once `seo.complete` is `true` (`SEO-INTELLIGENCE-PROTOCOL.md` §6). The coding agent implements, per page, exactly what those artifacts specify:

- Approved page list and routes match `keyword-map.md` §1 — no unapproved pages added, no mapped pages dropped.
- Unique `<title>` and meta description per page, following `seo-content-briefs.md`'s Title/Meta Description Direction — not a forced exact-match string.
- One meaningful `<h1>` per page matching the brief's H1 Direction; heading hierarchy (`h2`–`h4`) follows logically without skipping levels.
- Internal links implemented per `keyword-map.md` §2 (Internal Link Targets).
- Structured data (JSON-LD) implemented only where `seo-content-briefs.md` specifies it as genuinely applicable — never a copy-pasted default schema.
- Canonical tags, XML sitemap, and `robots.txt`/meta-robots directives configured correctly; no accidental `noindex` on a page `keyword-map.md` intends to rank.
- Semantic HTML, crawlable navigation (no critical content gated behind client-side-only rendering that a crawler cannot see), and accessible image `alt` text.

---

## 2.2 Builder Motion Engineering Requirements (V1.5)

When `motion.gsap_required = true` is declared in `site-profile.json`, the coding agent must implement motion strictly from `templates/motion-implementation-spec.md` following official GreenSock best practices.

---

## 2.3 Builder Visual Asset Requirements (V2.0)

Once `assets.status` reaches `"production_ready"` (`ASSET-DIRECTOR-PROTOCOL.md` §15), the coding agent implements visual assets strictly from `templates/asset-manifest.json` and `templates/asset-intent-brief.md`:

- **Path Integrity:** Use only optimized web delivery assets from `assets/web/` declared in `asset-manifest.json`. Never link directly to unoptimized master files in `assets/source/`.
- **Responsive Art Direction:** Implement `<picture>` elements with declared `media` queries and multi-density `srcset` attributes matching the locked responsive crop plan for all Hero and key editorial media.
- **Performance & LCP:** Add `fetchpriority="high"` and `loading="eager"` exclusively to the primary Hero LCP image. All other below-the-fold media must carry `loading="lazy"` and explicit `width` and `height` attributes to prevent Cumulative Layout Shift (CLS).
- **Accessibility:** Populate `alt` attributes strictly according to the asset's accessibility classification in `asset-manifest.json` (`INFORMATIVE`, `DECORATIVE`, `FUNCTIONAL`, `COMPLEX`). Never leave `alt` undefined or keyword-stuffed.
- **Format Delivery:** Serve modern formats (`.avif` primary with `.webp` / `.png` fallback).

---

## 2.4 Builder Immersive 3D Requirements (V2.1)

When `immersive.status = "implementation_ready"` is declared in `site-profile.json` (`IMMERSIVE-WEB-PROTOCOL.md`), the coding agent implements 3D experiences strictly from `templates/immersive-implementation-brief.md`:

- **Engine Fidelity:** Use strictly the approved technical engine (`THREE_JS_VANILLA` or `REACT_THREE_FIBER`).
- **Semantic DOM Parity:** Implement all primary headlines, CTAs, conversion flows, and product data in semantic HTML/DOM outside the WebGL canvas. Never trap critical content exclusively in WebGL pixels.
- **Universal 2D Fallback:** Implement a zero-CLS 2D fallback image/graphic that activates immediately if WebGL context fails, GPU initialization errors out, or when `?forceWebGLFallback=1` is provided.
- **Reduced Motion Support:** Wire `window.matchMedia('(prefers-reduced-motion: reduce)')` to freeze auto-rotation, halt scroll-linked camera zoom, and snap scenes to resting states.
- **Bounded DPR & Responsive Mobile Policy:** Enforce `Math.min(window.devicePixelRatio, 2.0)` on desktop and `Math.min(window.devicePixelRatio, 1.5)` on mobile. Implement `MOBILE_3D_POLICY` (`FULL`, `SIMPLIFIED`, `STATIC_RENDER`, or `DISABLED`).
- **Lifecycle & Resource Disposal:** Implement explicit teardown functions (`geometry.dispose()`, `material.dispose()`, `renderer.dispose()`, `cancelAnimationFrame()`) upon component unmount or view transitions.
- **Visibility Throttling:** Pause animation rendering loop whenever `document.hidden === true` or when the canvas is off-screen.

## 2.5 Builder Measurement Requirements (V2.6)

When `measurement.complete = true` is declared in `site-profile.json` (`CONVERSION-ANALYTICS-PROTOCOL.md`), the coding agent implements measurement **strictly** from `templates/measurement-plan.md`.

> **Prime Directive:** The coding agent MUST NOT invent tracking events during implementation. The measurement plan is the complete and exclusive event vocabulary for the build.

### 2.5.1 Event Names
- Implement **exactly** the events listed in the plan's Event Dictionary, spelled **exactly** as written.
- Do not add events. Do not rename events. Do not "helpfully" instrument extra interactions.
- Do not substitute a vendor's event name for the canonical name in application code. Where a vendor requires a different name, apply the plan's **Vendor Naming Mapping** at the provider integration boundary only.

### 2.5.2 Triggers
- Each event fires on precisely the trigger specified — no earlier, no broader.
- A `MACRO` conversion event fires on **confirmed success**, never on button click, wherever success is technically determinable.
- Viewport-based events use the specified intersection threshold, not an arbitrary one.

### 2.5.3 Parameter Contracts
- Every `required_parameter` must be present on every emission.
- No parameter may carry PII: no email, phone, full name, address, free-text message body, password, payment card data, medical information, SSN, or date of birth.
- Validation-error events carry a field **category**, never a field **value**.
- No parameter may be added that is absent from the plan's Parameter Registry.

### 2.5.4 Component Traceability
- Each event is owned by the component named in the plan's `page_or_component` field.
- Instrumentation lives with the component it measures; it is not scattered into unrelated global handlers.

### 2.5.5 Data Attributes
- Where the plan specifies declarative instrumentation, use the specified data attributes (e.g. `data-analytics-event`, `data-analytics-*` for parameters).
- Data attributes are the preferred binding mechanism for CTA click events — they keep the event name adjacent to the control and reviewable in markup.

### 2.5.6 Provider Integration Boundaries
- Provider SDK code is confined to a single integration module. Application components emit canonical events; the module translates and dispatches.
- **No credentials, API keys, tokens, or service-account material** are written into source control, the measurement plan, or the build.
- The site must remain 100% functional (navigation, forms, CTAs, motion, styling) when analytics fails, is blocked, or is disabled. Analytics is never application-critical.

### 2.5.7 UTM Handling
- Implement the preservation rules in the plan's Attribution / UTM Strategy section.
- Campaign parameters required for legitimate business measurement must not be silently dropped across client-side route transitions.
- **Never** write PII into a UTM parameter, and never construct campaign values at runtime from user data.

### 2.5.8 Duplicate Event Prevention
- Implement the `deduplication_rule` specified for each event.
- Submit handlers must be guarded so rapid or repeated clicks cannot emit multiple conversion events.
- No event may be bound twice through both a delegated and a direct listener.
- Verify no duplicate analytics library is loaded.

### 2.5.9 SPA Route-Change Behavior
- A single route transition emits **exactly one** `page_view`. `PAGE_VIEW_SOURCE_OF_TRUTH = ROUTE_SETTLED`.
- Document navigation, View Transitions callbacks (`pagereveal`, `pageswap`), and `popstate` history must all deduplicate against the same source of truth.

### 2.5.10 Form Start vs. Form Success
- `lead_form_start` (or its project equivalent) fires once, on first meaningful interaction with the form.
- The success conversion event fires **only** on confirmed successful completion.
- **A server-rejected submission MUST NOT emit a success conversion event.** It emits `form_validation_error` or the specified failure event. Firing a conversion on click while the server rejected the submission is a contract violation and a QA failure.

### 2.5.11 Affiliate Outbound Handling
- `affiliate_outbound_click` fires only for links whose destination host is genuinely external **and** which carry an affiliate relationship.
- Host comparison is by **resolved hostname**, never substring matching.
- **Internal navigation must never be labelled as outbound affiliate activity.**
- The builder never emits an `affiliate_conversion` or `affiliate_commission` event from a click. Those states originate only from affiliate platform reporting.

### 2.5.12 Production Verification Expectations
- The builder's obligation ends at `measurement.implementation_verified`, evidenced by browser interaction plus analytics debug/network capture stored in the project's evidence directory.
- The builder **never** sets `measurement.production_verified`. That flag requires owner-supplied evidence from the real production analytics environment.
- The builder never creates analytics properties, modifies tag manager containers or advertising accounts, installs pixels on live sites, deploys, or uses owner credentials.

### 2.5.13 Conflict Escalation
If the implementation conflicts with the locked measurement specification — an event cannot be triggered as specified, a required parameter is unavailable, success is not server-determinable, or a CTA does not exist as described — the coding agent **HALTS and escalates**. It does not improvise an alternative event, silently relax a trigger, or edit locked copy or IA to make instrumentation easier.

---

## 2.6 Builder Security & Privacy Requirements (V2.7)

When `security_privacy.complete = true` is declared in `site-profile.json` (`SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md`), the coding agent implements safeguards **strictly** from `templates/security-privacy-review.md` §21 (Implementation Requirements).

> **Prime Directive:** The builder does not invent security policy. It implements the approved specification. Where the specification is silent on a security-relevant decision, the builder **escalates** rather than choosing a default.

### 2.6.1 Secrets
- **No API keys, access tokens, OAuth secrets, database credentials, service-account keys, or webhook signing secrets in client-side source** — not in JS, inline script, data attributes, or bundled config. Anything shipped to the browser is public.
- **No secrets committed to source control**, including fixtures, tests, and history.
- `.env.example` carries **names and placeholders only** — never a real value.
- Secrets are read server-side from environment or platform secret storage.
- Secrets are redacted from logs, error messages, and stack traces, and excluded from screenshots and evidence captures.
- Where a required secret is absent, the dependent feature **fails closed** rather than degrading into an insecure or misleading state. Core site content remains functional.
- Public configuration identifiers (e.g. a GA4 measurement ID, a publishable payment key) are implemented as configuration references, clearly distinguished from secrets.

### 2.6.2 Security Headers
- Implement exactly the headers specified in `security-privacy-review.md` §16, with the specified values.
- **The CSP is project-specific.** Do not substitute a generic template, and do not widen a directive to `unsafe-inline`/`unsafe-eval`/`*` to make a build pass. Every allowed origin must correspond to a declared third-party inventory entry.
- Where the deployment platform cannot set a specified header, **HALT and escalate** — do not silently omit it.

### 2.6.3 Transport
- Production builds emit HTTPS canonical URLs, `og:url`, sitemap entries, and structured data.
- No mixed content: every script, style, image, font, media, and XHR loads over HTTPS in production.
- HTTP→HTTPS redirect behavior is implemented where the stack controls it.
- Local development over HTTP is expected and is not a contract violation.

### 2.6.4 Forms
- **Server-side validation is the trust boundary.** Every client-side constraint is re-enforced on the server.
- Sanitize and contextually encode all user input before rendering, querying, or templating.
- Implement CSRF protection on state-changing requests for session-authenticated surfaces.
- Implement the specified bot/spam mitigation, abuse prevention, and rate limiting.
- Error handling is helpful to the user and non-revealing about internals — no stack traces, database errors, or framework internals surfaced to the visitor.
- **No sensitive values in URLs** — not in query strings, path segments, fragments, or redirects.
- Where uploads exist: enforce an allow-list of types, size limits, validated content type (not extension alone), non-executable storage, and path-traversal-safe filenames.
- No email header injection from user input; no unvalidated recipient control.
- Guard submit handlers against duplicate submission.
- **A success state — visual and instrumented — renders only on confirmed server success.**

### 2.6.5 Authentication & Sessions
Applies only where the specification declares authentication. Do not build authentication for a site that does not require it.
- Never store plaintext or reversibly-encrypted passwords; use modern salted slow hashing.
- Session cookies carry `HttpOnly`, `Secure`, and the specified `SameSite` value.
- Implement the specified idle and absolute session lifetimes; logout invalidates the session server-side.
- **Authorize every protected resource on the server, per request.** Hiding a link in the UI is not authorization.
- Account recovery uses single-use expiring tokens and avoids account enumeration.
- Implement the specified brute-force throttling, MFA capability, and reauthentication for sensitive actions.

### 2.6.6 Payment Boundary
- **Never write code that stores raw card numbers, CVV/CVC values, full magnetic-stripe data, or PINs.** This is absolute.
- Card entry is handled by the approved provider's hosted or provider-controlled surface.
- Verify provider webhook signatures; never trust order state from a client-supplied redirect alone.
- **Never emit a claim of PCI compliance** in code comments, documentation, or UI because a provider is used.

### 2.6.7 Third-Party Scripts
- **Load only third-party scripts declared in `security-privacy-review.md` §9.** An undeclared third-party script is a contract violation.
- Respect the declared `PAGE_SCOPE` — do not load a route-scoped script globally.
- Consent-dependent scripts must not execute before consent where consent is recorded `REQUIRED`.
- Do not add a chat widget, pixel, map, font host, A/B platform, or support tool because it seemed useful.

### 2.6.8 Cookies & Browser Storage
- Write only the cookies and storage keys declared in `security-privacy-review.md` §11.
- Apply the specified cookie security attributes and lifetimes.
- Consent-dependent storage is not written before consent where consent is `REQUIRED`.
- Consent state survives client-side route transitions without re-prompting and without silently re-enabling tracking.

### 2.6.9 Data Minimization
- Implement **exactly** the fields the specification retains, with the specified required/optional status.
- **Do not add form fields** because a component library, starter template, or form service supplies them.
- Do not persist, log, or forward data classes absent from the §2 Data Inventory.

### 2.6.10 Analytics Privacy
- No PII in any analytics payload or UTM parameter: no email, phone, full name, postal address, free-text message body, password, payment card data, medical information, government identifier, or date of birth.
- Validation-error events carry a field **category**, never a field **value**.
- Where the specification records `ACTIVATION_BLOCKED_PENDING_PRIVACY`, the integration is **not activated** in the build.
- Session replay stays disabled unless the specification explicitly authorizes it with a masking policy.

### 2.6.11 Consent Gating
- Where consent is `REQUIRED`, consent-dependent scripts and storage are gated behind consent — verified by behavior, not by intention.
- **Rejecting optional processing must be as reachable as accepting it**: same interaction count, same discoverability, comparable visual prominence.
- Consent UI is keyboard operable, focus-managed, and screen-reader announced, with no keyboard trap.
- No prechecked optional consent, no deceptive wording, no hidden opt-out, no consent wall where the specification does not authorize one.

### 2.6.12 Disclosures
- Implement required affiliate/sponsored disclosure at the specified placement — visible without interaction, legible at body-copy standard, not suppressed by styling.
- Sponsored units remain visually distinguishable from independent editorial content.
- Implement the privacy notice route where the specification requires one and the locked IA contains it.
- **Never invent legal wording.** Where the owner has not approved wording, escalate rather than shipping drafted legal text as final.

### 2.6.13 Production-Only Safeguards & Environment Separation
- Development mocks, debug endpoints, verbose logging, seeded test data, and development credentials must not ship to production.
- Environment configuration is separated; production configuration is never read from committed files.

### 2.6.14 Safe Failure Behavior
- The site remains functional for content and navigation when a third-party service fails, is blocked, or is disabled.
- Security controls fail **closed**; presentation features fail **open**. A missing analytics script never breaks a form; a missing signing secret never lets an unsigned webhook through.

### 2.6.15 No Compliance Claims
- The builder never writes `GDPR COMPLIANT`, `CCPA COMPLIANT`, `HIPAA COMPLIANT`, `PCI COMPLIANT`, `COPPA COMPLIANT`, or `LEGAL COMPLIANCE VERIFIED` into code, comments, documentation, commit messages, or UI.
- The builder never renders a compliance badge, seal, or certification mark that the owner has not supplied and evidenced.

### 2.6.16 Verification Expectations
- The builder's obligation ends at `security_privacy.implementation_verified`, evidenced by build inspection plus browser/network capture stored in the project's evidence directory.
- The builder **never** sets `security_privacy.production_verified`, and never sets `security_privacy.compliance_certified` (permanently `false`).
- The builder performs no intrusive testing against external systems, and never deploys, changes DNS, configures consent platforms, or uses production credentials.

### 2.6.17 Conflict Escalation
If the implementation conflicts with the approved security/privacy specification — a specified header cannot be set, a required control is impossible on the chosen stack, a declared service needs an undeclared origin, or a required disclosure has nowhere to live in the locked layout — the coding agent **HALTS and escalates**. It does not silently omit the control, weaken the policy, invent an alternative, or edit locked copy, IA, or tokens to make the safeguard fit.

**Precedence during implementation:** security and privacy requirements override conversion optimization. Approved locks override both — a conflict with a lock produces an Owner Change Request, never a silent edit.

---

---

## 3. Strict Prohibitions During Implementation

Once all locks are engaged and readiness gates are achieved, the coding agent is strictly prohibited from introducing:

1. **Unregistered Colors:** No inline hex codes (`#123456`), RGB values, or ad-hoc Tailwind color utilities. Every color MUST resolve to a design system variable.
2. **Unregistered Typography:** No ad-hoc font families, arbitrary font sizes (e.g., `text-[27px]`), or unapproved font weights.
3. **Arbitrary Spacing:** No random margins or paddings (e.g., `mt-[37px]`). All spatial values must snap to the 8-point scale (`space-1` through `space-32`).
4. **Improvised Component Styles:** No inventing new card borders, floating decorative badges, random gradients, or glassmorphic backdrops that are not specified in `design-system.md`.
5. **Structural Layout Deviations:** No altering the sequence of sections, skipping proof elements, or turning an asymmetrical split into a generic 3-column card grid.
6. **Unapproved Animation:** No adding random bouncy scroll reveals or uncoordinated hover transforms. No motion beyond what `templates/motion-direction.md` specifies.
7. **Corner Radius Drift:** No mixing `rounded-none`, `rounded-lg`, and `rounded-full` arbitrarily. All geometry must strictly adhere to the token tier.
8. **Independent SEO Strategy:** No creating new pages, meta-title/description strategies, or keyword targets not present in `templates/keyword-map.md` / `templates/seo-content-briefs.md`.
9. **Un-directed / Un-manifested Visual Assets:** No downloading arbitrary stock photos, scraping competitor media, or improvising visual assets during implementation.
10. **Direct Master File Linking:** No referencing uncompressed source files from `assets/source/` in production HTML/CSS markup.
11. **Unmotivated 3D / Demo Slop:** No adding Three.js canvases, floating 3D toruses, neon grids, or unmotivated particle fields not explicitly approved in `templates/immersive-implementation-brief.md`.
12. **Inaccessible WebGL Traps:** No rendering primary headlines, body text, or CTA buttons exclusively inside WebGL canvas pixels.
13. **Invented Analytics Events:** No adding, renaming, or improvising tracking events not present in `templates/measurement-plan.md`. No vanity instrumentation.
14. **PII in Telemetry:** No email, phone, name, address, free-text input, password, payment card, or medical data in any analytics payload or UTM parameter.
15. **False Conversion Signals:** No firing a success conversion event on button click when the server rejected the submission, and no emitting affiliate conversion or commission events from an outbound click.
16. **Committed Analytics Secrets:** No API keys, tokens, or service-account credentials in source control.
17. **Client-Side Secrets:** No API key, access token, OAuth secret, database credential, service-account key, or webhook signing secret in any code shipped to the browser. Anything the browser receives is public.
18. **Undeclared Third-Party Scripts:** No analytics, pixel, chat widget, map, embed, font host, A/B platform, or support tool loaded that is absent from `templates/security-privacy-review.md` §9.
19. **Undeclared Cookies or Storage:** No cookie, `localStorage`, `sessionStorage`, or IndexedDB key written that is absent from `security-privacy-review.md` §11, and none written before consent where consent is `REQUIRED`.
20. **Invented Form Fields:** No form field added that is absent from the approved data inventory — not because a component library, starter template, or form service supplied it.
21. **Client-Only Trust Boundaries:** No reliance on client-side validation, hidden fields, or a hidden UI control as a security or authorization boundary. Server-side enforcement is mandatory.
22. **Raw Payment Card Storage:** No code that stores raw card numbers, CVV/CVC values, full magnetic-stripe data, or PINs. Absolute.
23. **Plaintext Password Storage:** No plaintext or reversibly-encrypted password storage.
24. **Sensitive Values in URLs:** No personal or sensitive data in query strings, path segments, fragments, or redirect targets.
25. **Weakened Security Policy:** No widening a specified CSP or security header to `unsafe-inline`, `unsafe-eval`, or `*` to make a build pass, and no silently omitting a specified header.
26. **Privacy Dark Patterns:** No consent UI where rejecting is harder than accepting, no misleading button hierarchy, no prechecked optional consent, no hidden opt-out, no obstructive unsubscribe, no disguised advertising.
27. **Suppressed Disclosure:** No hiding, shrinking, or styling-away of a required affiliate, sponsorship, or privacy disclosure to protect visual composition.
28. **Fabricated Compliance Claims:** No `GDPR COMPLIANT`, `CCPA COMPLIANT`, `HIPAA COMPLIANT`, `PCI COMPLIANT`, `COPPA COMPLIANT`, or `LEGAL COMPLIANCE VERIFIED` in code, comments, documentation, commit messages, or UI; no unevidenced compliance badge, seal, or certification mark.
29. **Development Artifacts in Production:** No debug endpoints, verbose logging, seeded test data, mock services, or development credentials shipped to production.

---

## 4. Change Management Procedure (The Spec-First Rule)

If during the coding phase a technical constraint or unforeseen aesthetic collision occurs:

```
TECHNICAL / DESIGN COLLISION ENCOUNTERED
                    │
                    ▼
          HALT IMPLEMENTATION
                    │
                    ▼
     UPDATE SPECIFICATION ARTIFACT
  (e.g., templates/design-system.md)
                    │
                    ▼
       RE-VERIFY DESIGN LOCKS
                    │
                    ▼
          RESUME IMPLEMENTATION
```

**Never fix a design issue by hacking custom CSS in the component without updating the design system specification first.**

### 4.1 Gauntlet Targeted Repair Governance (V1.3)

During Phase 11.5 (Website Gauntlet Subsystem), when an independent critic identifies `BIGGEST_REMAINING_GAP`:
- The builder agent executes the **smallest safe repair** strictly within locked tokens and layout specifications.
- **No Full-Site Wipes:** Repair only the specific CSS rule, markup structure, or token application identified.
- **Lock Boundary Enforcement:** If resolving the gap is impossible without modifying a locked token, copy string, or motion behavior, the builder is **strictly prohibited from silently making the change**. It must set status to `GAUNTLET_LOCKED_CHANGE_REQUIRED` and generate a formal Change Request for Owner Review.

---

## 5. Implementation Verification Protocol

Before submitting code for review, the coding agent must verify:
- [ ] Every color in the stylesheet maps to a CSS custom property from `design-system.md`.
- [ ] All font sizes and line heights strictly match the mathematical type scale.
- [ ] Every section layout strictly matches the section morphology in `information-architecture.md`.
- [ ] All copy matches the locked copy in `content-plan.md` (no `Lorem Ipsum` or placeholder text).
- [ ] All interactive elements include defined hover, active, and focus states.
- [ ] Mobile responsive views maintain exact design intent without horizontal overflow.
- [ ] Every implemented motion behavior traces to a specific line in `templates/motion-direction.md`; nothing was added because the capability existed.
- [ ] `prefers-reduced-motion` fallback is implemented and preserves equivalent meaning, per `MOTION-DIRECTION-PROTOCOL.md` §7.
- [ ] If a cinematic specialist was engaged, the build matches `templates/cinematic-brief.md` — typography, composition, and module selection were not overridden by the specialist's own creative defaults (see `CINEMATIC-INTEGRATION-PROTOCOL.md` §3).
- [ ] Every page in `templates/keyword-map.md` §1 exists; no unapproved page was added. Full detail: `PRODUCTION-CHECKLIST.md` §5.1.
- [ ] Phase 11.5 Website Gauntlet pass achieved `GAUNTLET_PASS` (or owner-accepted `GAUNTLET_CAP_REACHED` / exception).
- [ ] Every security/privacy requirement in `templates/security-privacy-review.md` §21 is implemented, or an escalation was raised. Full verification detail: `PRODUCTION-CHECKLIST.md` §5.3.
- [ ] Zero secrets in the client bundle or source control; zero undeclared third-party scripts, cookies, or storage keys in the build.

