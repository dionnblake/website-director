# IMPLEMENTATION CONTRACT: THE DESIGN-TO-CODE GOVERNANCE PROTOCOL

> **Version:** 1.7.0
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

## 2.1 Design-first production entry (V2.15 bounded flow)

The five locks remain necessary but are not the only evidence required to
start the full production implementation. The implementation contract must
also point to a complete Business Understanding Pack, captured owner intent,
identified required assets, interpreted owner references, a real-browser
desktop/mobile full-homepage review, explicit owner approval recorded under
`visual_prototypes.homepage_visual_approved`, and a Design System derived from
that approved homepage.

Missing evidence is `BLOCKED`. A bounded prototype may exist before this
entry point, but prototype code is not permission to begin the full build.
Remaining pages inherit the approved homepage system. Components are
downstream choices selected for stack fit, licensing, accessibility,
performance, maintainability, fidelity, and risk. No particular component
library, framework, Figma workflow, CodeStitch workflow, or model is
mandatory, and none may determine visual direction.

The owner may `APPROVE`, `REVISE`, or `HYBRIDIZE` the homepage. Builder or
internal-critic output cannot set the owner approval field.

---

## 2.0 Builder Content Operations Requirements (V2.13)

When a project uses Capability #8, implementation consumes the validated
`templates/content-model.md`, `templates/content-model.json`, and
`templates/cms-decision.md` from Phase 6.25. The builder must:

- render declared semantic content types and fields without inventing fields,
  duplicating repeated entities, or coupling content to card/column/line,
  breakpoint, color, CSS, design-token, or component-slot names;
- preserve required-field validation, relationships, taxonomy rules, editor
  help, character limits, preview behavior, lifecycle states, and role
  capabilities;
- keep `DRAFT`, `IN_REVIEW`, `APPROVED`, `SCHEDULED`, and `ARCHIVED` content
  out of public listings/routes as specified. `PUBLISHED` content must resolve
  on the intended surface;
- enforce `CAN_EDIT`, `CAN_REVIEW`, `CAN_PUBLISH`, `CAN_ARCHIVE`, and
  `CAN_DELETE` separately. Agent-generated content remains `DRAFT` until human
  review; no agent may publish autonomously;
- preserve normalized unique slugs and create/verify a durable 301 redirect
  for every published or archived slug change. Archive, unpublish, and delete
  remain distinct operations;
- sanitize rich text to the approved semantic allowlist. No scripts, inline
  CSS, arbitrary fonts/colors, event handlers, or unvalidated embeds;
- keep analytics event identifiers, structured-data schema, security headers,
  design tokens, canonical lock state, and other system-generated controls
  outside editor surfaces;
- preserve Asset Director asset identity and V2.12 provenance references,
  canonical SEO strategy, accessibility semantics, security/privacy controls,
  measurement contracts, and V2.5 handoff inputs. Do not create duplicate
  ledgers or substitute provider fields for those authorities;
- implement only the selected architecture recorded in the decision. Unknown
  provider configuration, missing export path, unresolved migration, or
  missing high-risk evidence remains visible as `UNKNOWN`, `BLOCKED`, or
  `FAIL`, never inferred as ready.

If implementation requires changing the locked content structure, approved
copy, or another owner-controlled contract, **HALT** and raise an Owner Change
Request. This section does not authorize CMS installation, production
publishing, deployment, provider installation, or Capability #10 Ecommerce,
Authentication, and Application Modules.

---

## 2.0.1 Builder Localization & Internationalization Requirements (V2.14)

When Capability #9 is required, implementation consumes the validated
`LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md`,
`templates/localization-plan.md`, `templates/localization-manifest.json`,
`templates/locale-registry.json`, and `localization.complete` state. The builder
must:

- use the registered BCP 47-style locale identifiers, exactly one source locale,
  exactly one default locale, the selected route strategy, the explicit default
  URL policy, and the acyclic fallback policy;
- render an accessible text-labelled locale switcher and expose the correct
  `lang` and `dir` values. Flags may supplement labels but cannot be the only
  locale identifier;
- keep localizable content, UI messages, alt text, SEO text, form labels,
  errors, and consent copy in the approved message/content architecture. Do
  not concatenate translated fragments or use English text as message IDs;
- use standards-aware plural categories, safe named interpolation, locale-aware
  date/time/number/currency/unit formatting, explicit currency codes, and an
  explicit timezone and conversion policy. Never infer currency from language
  or ship a universal `MM/DD/YYYY` display mask;
- implement RTL direction, bidirectional text handling, and logical CSS where
  practical. Do not mechanically mirror logos or brand marks. Document
  directional icon exceptions;
- verify script and glyph coverage, CJK and Arabic-derived support where
  applicable, font licensing and redistribution status, V2.12 provenance, and
  30 percent and 50 percent text expansion before release review;
- consume V2.13 Content Operations models and classify localizable versus
  non-localizable fields. Preserve stable IDs, evidence references, hashes,
  slugs, redirect records, editorial status, portability, and review history;
- keep translation statuses explicit. Machine output is draft-only; human or
  explicitly authorized review is required before publication. Source changes
  mark translations `STALE`. Machine-translated legal content is never
  automatically legally approved, and translated claims cannot strengthen
  source claims;
- implement localized self-canonicals, intentional reciprocal hreflang and
  x-default behavior, localized sitemap and structured-data inputs, and
  locale-aware Open Graph metadata according to the SEO authority;
- reuse the existing measurement event names and add locale as a parameter.
  Do not create one event taxonomy per language. Preserve Security & Privacy,
  Accessibility, Provenance, Browser QA, Launch Ops, and V2.5 Handoff contracts;
- treat an absent or blocked provider as explicit state. No provider account,
  translation API, production credential, publication, deployment, DNS change,
  live analytics mutation, or external side effect is authorized by this
  contract.

`localization.complete` means the localization plan and contract are complete.
It does not mean linguistic quality, provider configuration, implementation
verification, production verification, legal approval, publishing, or deployment.
`[LOCALIZATION_READY]` is a readiness gate and does not create a sixth owner
lock. If implementation requires changing locked IA, content, copy, design
tokens, motion, measurement, SEO, accessibility, security/privacy, or
provenance requirements, **HALT** and raise an Owner Change Request.

---

## 2.0.2 Builder Conditional Application Architecture Requirements (V2.15)

When Capability #10 is required, implementation consumes the reviewed
`APPLICATION-COMMERCE-AUTH-PROTOCOL.md`,
`templates/application-architecture-plan.md`,
`templates/application-architecture-manifest.json`, the selected module
records, and the `application.complete` state. The builder must:

- implement only the modules justified by explicit user stories and include
  their declared dependency closure. A static marketing or public content
  site must not receive authentication, database, payment, or other
  application infrastructure merely because the registry exists;
- keep authentication, sessions, recovery, password hashing, MFA, and email
  verification explicit where required. Plaintext passwords and exposed
  password hashes are forbidden;
- enforce authorization, roles, tenant boundaries, and object ownership on the
  server. Client role flags, hidden admin controls, route obscurity, and
  disabled buttons are never access controls;
- keep the server authoritative for data, price, tax, inventory, payment,
  order, entitlement, booking, upload, and user-content state. Payment and
  order status machines remain separate;
- use hosted or tokenized payment collection, never store raw card data, and
  show success or grant entitlements only after authoritative payment
  confirmation. Webhooks verify signatures and idempotency before side effects;
- define subscription failure/entitlement behavior, booking conflict and
  timezone behavior, upload allowlists/private storage, UGC sanitization,
  transactional-message failure, integration inventory, and high-risk
  verification when those modules are active;
- keep secrets server-side and out of source, bundles, fixtures, logs,
  screenshots, analytics, and handoff artifacts. No provider account, live
  user, live payment, production credential, publish, deploy, or production
  verification is authorized by this contract;
- reuse Content Operations, Localization, Provenance, Measurement, Security
  and Privacy, Accessibility, Browser QA, Launch Ops, and V2.5 Handoff
  authorities without creating parallel state or a sixth owner lock.

`application.complete` means the architecture contract is complete. It does
not mean a provider is configured, a live user or payment exists, the build is
implemented, or production is verified. `[APPLICATION_ARCHITECTURE_READY]` is
a readiness gate, not an owner lock. Missing or unavailable evidence remains
`FAIL` or `BLOCKED`. If an application requirement conflicts with locked IA,
copy, design, motion, measurement, SEO, accessibility, security/privacy,
localization, provenance, or content structure, **HALT** and raise an Owner
Change Request.

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

## 2.4 Builder Cinematic and Rendered-Evidence Requirements (V2.15)

When a cinematic journey is selected, the builder consumes the approved
`cinematic-brief.md` and `motion-direction.md`. The builder must not choose a
media strategy from personal or tool defaults. `DENSE_KEYFRAME_VIDEO_SCRUB`
and `CANVAS_FRAME_SEQUENCE` are both valid only when the brief records the
choice and Browser QA proves the measured behavior.

For applicable production candidates, the builder must expose the named
`visual_evidence` surfaces in `templates/browser-qa-manifest.json` and keep
the semantic content complete without media. Posters, mobile and
reduced-motion fallbacks, text-safe zones, ending rest, seek coalescing,
delta-gated DOM updates, compositor isolation, and teardown must be
implemented where the selected strategy requires them.

The builder may create the initial render evidence, but it is never the sole
visual authority. `NO_RENDERED_VISUAL_EVIDENCE = NO_VISUAL_QA_PASS` and
`BUILDER != CRITIC`: the Gauntlet must inspect the actual screenshot set,
rendered DOM, rendered CSS, approved direction, design system, owner intent,
and assigned Reference Bars in a fresh context. Any repair requires a new
render and new screenshots; stale pre-repair evidence cannot support a pass.

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

## 2.7 Builder Testability & Browser QA Requirements (V2.8)

The build is verified in Phase 10.5 by machine-executed browser tests (`BROWSER-REGRESSION-QA-PROTOCOL.md`). The coding agent must keep the build testable and must never defeat that verification.

### 2.7.1 Testable Surface
- **Expose stable selectors where they are needed for verification** — a stable `id`, a semantic role, or a `data-qa="…"` hook on: the primary CTA, each form and its success/error regions, the mobile nav toggle and panel, dialogs, and any route-transition container. Prefer semantics and roles; use `data-qa-*` only where semantics are insufficient.
- **Test-only semantics must not leak into user-facing UI** — no `data-qa-*` attribute changes layout, style, or copy; no visible "test mode" affordance ships.
- Where the plan requires a deterministic mode for dynamic content (frozen clock, pinned rotation), gate it behind a build/query flag that is inert in production.

### 2.7.2 Do Not Defeat QA
- **Do not disable, skip, or comment out a browser QA check to ship.**
- **Do not delete a failing test** or narrow its assertions to pass.
- **Do not silently update a visual baseline.** A diff is reported; a baseline change requires the owner authorisation recorded in `browser-qa-manifest.json`.
- **Do not add a broad console/network ignore.** Every ignore is a justified, owned, expiring entry in the manifest. An empty ignore list is the default.
- **Do not mask a broken region** (page-wide masks, `overflow-x: hidden` over real overflow, hiding a failing element). Fix the implementation or escalate the specification conflict.

### 2.7.3 Conflict Escalation
If a browser QA failure can only be resolved by changing locked IA, copy, design system, or motion direction, the coding agent **HALTS and escalates** with an Owner Change Request. Browser QA authorises only implementation repairs that leave locked design intent intact.

---

## 2.8 Builder Accessibility Requirements (V2.9)

When `accessibility.complete = true` is declared in `site-profile.json` (`ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md`), the coding agent implements accessibility **strictly** from `templates/accessibility-review.md` §27 (Implementation Requirements) toward the recorded target (`WCAG 2.2 AA` by default).

> **Prime Directive:** The builder does not invent accessibility policy. Where the specification is silent on an accessibility-relevant decision, the builder **escalates** rather than choosing a default.

### 2.8.1 Semantics & Names
- **Native semantic HTML first.** `<button>` for actions, `<a href>` for navigation, real `<h1>`–`<h6>` hierarchy (no skipped levels, one meaningful primary heading), lists as lists, tables as tables, landmark elements (`header`/`nav`/`main`/`footer`).
- **No ARIA is better than bad ARIA.** Do not add `role`/`aria-*` where native semantics already provide the role, state, and keyboard behaviour. No redundant or conflicting ARIA.
- Every interactive control exposes an accessible **name**, correct **role**, and current **value/state**. The visible label is contained in the accessible name (WCAG 2.5.3). Icon-only controls carry `aria-label` or visually-hidden text.
- `<html lang>` is set; every page has a non-empty, unique `<title>`.

### 2.8.2 Keyboard & Focus
- All functionality operable by keyboard where the interaction reasonably supports it: logical tab order, Enter/Space activation, Escape to dismiss, arrow keys within composite widgets (tablist, radiogroup, menu), **no keyboard trap**.
- A visible focus indicator on every interactive element, from the `--focus-ring` token. **Do not remove the browser outline** without an equal-or-more-visible replacement.
- Focus is not obscured by sticky/fixed UI (WCAG 2.4.11). A skip-navigation link is provided where the spec requires one.
- Focus is moved into a dialog on open and **restored to the trigger** on close; focus is managed on route change where the spec requires it.

### 2.8.3 Forms
- Persistent programmatic labels; required state communicated in text, not colour or `*` alone; `autocomplete` / input-purpose tokens where appropriate (WCAG 1.3.5).
- Errors are programmatically associated (`aria-describedby`), identified by more than colour, and focus moves to the first error; an error summary where the spec requires one.
- **An accessibility repair must never cause a false conversion success.** A server-rejected submission renders no success state and emits no success conversion event (see §2.5.10, §2.6.4).

### 2.8.4 Contrast, Colour & Reflow
- Ship only the contrast-safe token pairs from `design-system.md` §14. Do not introduce a foreground/background combination below target.
- Meaning never depends on colour alone (WCAG 1.4.1): errors, status, selected, required, and chart series carry a non-colour indicator.
- Content reflows at **320 CSS px** without two-dimensional scrolling except legitimate exceptions (wide tables, maps). Text is not clipped and no control is lost at 200% zoom or under the WCAG 1.4.12 text-spacing override.

### 2.8.5 Target Size, Dragging, Motion, Media, Images
- Interactive targets meet the project minimum (`44 × 44 px` where approved) and never fall below the WCAG 2.2 `24 × 24 px` floor without a recorded exception.
- Every drag interaction has a non-drag alternative (WCAG 2.5.7) unless a genuine exception applies.
- Reduced motion honoured; no meaning exists only in animation; autoplaying content > 5s is pausable; no content flashes more than three times per second.
- Media (where present) has captions/transcript/controls/keyboard access and does not autoplay with sound.
- Meaningful images have meaningful `alt`; decorative images use `alt=""`/`aria-hidden`; **`alt` is never keyword-stuffed** — SEO does not override accessibility.

### 2.8.6 Dialogs, Menus, Status
- Dialogs: correct role (`dialog`/`alertdialog`), accessible name, initial focus, containment where required, Escape, visible close, focus restoration, background made inert.
- Menus/tabs/accordions use established patterns with correct state attributes (`aria-expanded`, `aria-selected`, `aria-current`); prefer native `<details>`/`<summary>`.
- Dynamic status changes that need it are announced via an intentionally-politened live region — and **no unnecessary `aria-live` regions**.

### 2.8.7 Authentication & Consent (only where they exist)
- Do not require a cognitive-function test (transcription CAPTCHA, puzzle) where an accessible alternative exists (WCAG 3.3.8). Allow paste into password/OTP fields; support password managers.
- Consent UI is keyboard operable, screen-reader understandable, readable at zoom/reflow, non-deceptive, with rejection as reachable as acceptance.
- **Security ↔ accessibility conflicts escalate to an explicit owner decision** — never silently weaken a security control, never silently degrade accessibility.

### 2.8.8 Testability & Verification
- Expose stable browser-QA selectors where needed for verification **without test-only UI leakage** (no `data-qa-*` that alters layout, style, or copy).
- **Do not delete an accessibility test.** Do not narrow an assertion to pass.
- **Do not suppress an accessibility-engine finding** (an axe rule disable, an ignore selector) without a documented rationale recorded in `accessibility-review.md` §25/§26.
- The builder's obligation ends at `accessibility.automated_verified` + `accessibility.manual_verified` (evidenced in the project evidence directory). The builder never sets `accessibility.production_verified`, and never writes `ADA COMPLIANT`, `FULLY ACCESSIBLE`, `ACCESSIBILITY GUARANTEED`, or `WCAG COMPLIANT`.

### 2.8.9 Conflict Escalation
If satisfying a required accessibility check needs a change to locked IA, copy, design system, or motion direction, the coding agent **HALTS and produces an Owner Change Request**. It does not silently degrade accessibility to preserve a locked aesthetic, and it does not silently override a lock.

**Precedence during implementation:** accessibility and safety requirements override SEO and conversion optimisation. Approved locks override both — a conflict with a lock produces an Owner Change Request, never a silent edit in either direction.

---

## 2.9 Builder & Release-Operator Launch Requirements (V2.10)

When `launch_ops.complete = true` is declared in `site-profile.json` (`LAUNCH-OPERATIONS-PROTOCOL.md`), builders and release operators implement launch strictly from `templates/launch-plan.md`.

> **Prime Directive:** Website Director prepares plans, manifests, commands, and verification steps. **It does not deploy, push, merge, alter DNS, configure SSL, create monitoring services, or touch a live website.** Deployment is an external side effect performed by the owner or an owner-authorised operator.

### 2.9.1 Release Identity & Freeze
- Deploy only a build with a recorded immutable identity (`release_sha`, `release_version`, `build_id`, `build_timestamp`). An unidentified build is never deployed.
- Honour the release candidate freeze: no untracked implementation changes, no silent asset/copy/analytics edits, no dependency upgrades, no new scripts, no production-only hacks after freeze. Any post-freeze change creates a new release identity or is an explicit pre-authorization candidate update with a recorded reason.
- A dirty release candidate (uncommitted changes, unresolved drift) is never authorised or deployed.

### 2.9.2 Deployment Authorization Boundary
- `RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED`. Deploy only on explicit per-release owner authorization recorded in `launch-plan.md` §19 (`deployment_authorization_ref`), or under a recorded durable deployment policy.
- **Never infer deployment permission** from passing QA, a completed implementation, an approved design, an owner saying "looks good", a prior project's authorization, or a previous release.

### 2.9.3 Production Configuration
- Never silently change production configuration. Production config is not read from committed files; environment separation is enforced; debug endpoints, verbose logging, seeded data, mock services, and development credentials never ship.
- **No production secret is ever committed** to source control, the launch plan, the evidence manifest, or any artifact.

### 2.9.4 Verification Integrity
- Production verification verifies a **known release identity** on the **production surface**. `deployed_sha` must match `release_sha`; where it cannot be proven, record `DEPLOYED_IDENTITY = UNVERIFIED` and mark the check `BLOCKED` — never assume a match.
- **Never mark staging as production.** **Never claim production verification from localhost.** A `local` or `staging` evidence manifest sets no `production_*_verified` flag.
- Do not bypass, disable, skip, or narrow a failing launch check to proceed. Do not disable Browser QA, disable accessibility verification, suppress security/privacy failures, remove analytics verification, or rewrite a baseline to get green.
- Production Browser QA is the V2.8 harness in `environment = "production"` mode — no destructive actions, no real form submission without the §20 authorization recorded in `launch-plan.md` §13.

### 2.9.5 Rollback & Incidents
- A rollback plan (`rollback_ready`) exists before deployment authorization where practical; the mechanism is documented even for immutable static hosting.
- Do not execute a destructive production rollback as part of this task. Rollback testing is local / staging / preview / synthetic.
- Incidents are recorded append-only in `launch_ops.known_incidents[]`; a `SEV0`/`SEV1` incident meeting a defined trigger sets `ROLLBACK_REQUIRED`.

### 2.9.6 Conflict Escalation
If a production repair requires a change to locked IA, copy, design system, motion direction, or to accessibility / measurement / security-privacy / SEO requirements, the operator **HALTS** (`launch_ops.status = "BLOCKED"`) and routes back to the owning specification with an Owner Change Request. **No invisible production-only fixes that cause design/spec drift.**

**Precedence during launch:** owner deployment authority is absolute — nothing deploys without it. Owning specifications win over launch-side convenience; approved locks win over both.

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
30. **Disabled or Deleted QA:** No disabling, skipping, or removing a Phase 10.5 browser QA check, and no narrowing an assertion, to make a build pass.
31. **Silent Baseline Updates:** No overwriting a locked visual-regression baseline because a diff appeared. A baseline change requires the owner authorisation recorded in `browser-qa-manifest.json`.
32. **Broad QA Ignores:** No blanket console or network ignore. Every ignore is a justified, owned, expiring entry in the manifest.
33. **Masked Defects:** No page-wide screenshot masks, no `overflow-x: hidden` over genuine overflow, no hiding a failing element to green a check.
34. **Missing Test Hooks:** No shipping a primary CTA, form, mobile-nav control, dialog, or route-transition container with no stable selector or semantic role for verification — and no test-only attribute that alters user-facing layout, style, or copy.
35. **Reconstructed ARIA Over Native:** No custom `role`/`aria-*` widget where a native control (`<button>`, `<a>`, `<select>`, `<details>`, `<input type>`) provides the correct role, state, and keyboard behaviour; no redundant or conflicting ARIA.
36. **Removed Focus Indicator:** No `outline: none` (or equivalent) without an equal-or-more-visible token replacement meeting indicator contrast.
37. **Colour-Only Meaning:** No error, status, selected, required, or chart-series state conveyed by colour alone.
38. **Suppressed Accessibility Findings:** No disabling an accessibility-engine rule, adding an ignore selector, deleting an accessibility test, or narrowing an accessibility assertion without a documented rationale in `accessibility-review.md`.
39. **Fabricated Accessibility Claims:** No `ADA COMPLIANT`, `FULLY ACCESSIBLE`, `ACCESSIBILITY GUARANTEED`, `WCAG COMPLIANT`, `SECTION 508 COMPLIANT`, or `EN 301 549 COMPLIANT` in code, comments, documentation, commit messages, or UI; no unevidenced accessibility badge or certification mark.
40. **Unidentified or Dirty Deployment:** No deploying a build with no recorded release identity, and no deploying a dirty release candidate (uncommitted changes, unresolved drift, post-freeze silent edits).
41. **Unauthorized Deployment:** No deploying without an explicit per-release owner authorization reference (or a recorded durable deployment policy). Passing QA, a completed build, an approved design, "looks good", a prior project, or a previous release never authorize deployment.
42. **Silent Production Configuration Change:** No changing production configuration, environment variables, headers, redirects, DNS, or third-party wiring outside the approved `launch-plan.md` — and no committed production secrets anywhere.
43. **Bypassed Launch Checks:** No disabling, skipping, or narrowing a launch verification check — Browser QA, accessibility verification, security/privacy verification, or analytics verification — to proceed to or through deployment; no baseline rewrite to get green.
44. **Staging Marked Production / Localhost Production Claims:** No recording a staging or preview pass as production verification; no setting any `production_*_verified` flag from a `local` or `staging` evidence manifest; no assuming `deployed_sha` matches `release_sha` when it cannot be proven.
45. **Destructive Launch Actions:** No production rollback executed on a live system as part of the build task; no real production form submission, order, email, CRM record, or analytics conversion generated without the recorded §20 production-test authorization.
46. **Invisible Production-Only Fixes:** No production hotfix that changes locked IA, copy, design tokens, motion, or accessibility / measurement / security-privacy / SEO requirements without HALTing and raising an Owner Change Request.

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
- [ ] Phase 10.5 Browser & Regression QA passed (`browser_qa.complete = true`), or a recorded `blocked_reason` / `exception`. Full detail: `PRODUCTION-CHECKLIST.md` §5.4 and `BROWSER-REGRESSION-QA-PROTOCOL.md`.
- [ ] Every accessibility requirement in `templates/accessibility-review.md` §27 is implemented, or an escalation was raised. `accessibility.automated_verified` and `accessibility.manual_verified` are set on evidence; no accessibility-engine finding is suppressed without a documented rationale. Full detail: `PRODUCTION-CHECKLIST.md` §3 and §5.5, and `ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md`.
- [ ] Every primary CTA, form, mobile-nav control, dialog, and route-transition container carries a stable selector or semantic role for verification; no test-only attribute alters user-facing UI.
- [ ] If `launch_ops.complete = true`: the release has a recorded immutable identity; deployment (if any) carries an explicit per-release owner authorization reference or a durable policy; production verification traced `deployed_sha` to `release_sha` on the production surface; no `production_*_verified` flag was set from localhost/staging. Full detail: `PRODUCTION-CHECKLIST.md` §11 and `LAUNCH-OPERATIONS-PROTOCOL.md`.
- [ ] Every production claim resolves to EVIDENCE_REF and every production
      asset resolves to an asset provenance_ref in the cross-cutting ledger.
      Run provenance/validator.py in production mode; missing, stale,
      contradictory, ambiguous, unverified, or hash-mismatched records block
      the release.
- [ ] Research and screenshot references remain REFERENCE_ONLY. AI-generated
      media records provider, date, source inputs, edit history, and SHA-256;
      the hash is identity evidence only.

