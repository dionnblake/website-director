# SECURITY, PRIVACY & COMPLIANCE INTELLIGENCE PROTOCOL

> **Version:** 2.7.0  
> **Status:** Authoritative Production Risk Governance, Data Handling, Consent, Disclosure & Technical Safeguard Standard  
> **Governs:** `PHASE 6.75` (Security, Privacy & Compliance Intelligence)  
> **Readiness Gate:** `GATE SECURITY: [SECURITY_PRIVACY_READY]`  
> **Authoritative State:** `site-profile.json` → `security_privacy{}` (single completion flag: `security_privacy.complete`)  
> **Core Principle:** Website Director determines what security, privacy, consent, data-handling, and disclosure obligations the website it is designing actually creates — then converts those findings into implementation requirements and production verification. It is not a lawyer, not a penetration-testing platform, and not an autonomous security operator. Where certainty is unavailable, it escalates. It never certifies legal compliance.

---

## 1. Purpose & Architectural Position

Website Director already governs discovery, positioning, SEO, visual research, design intelligence, information architecture, content, conversion measurement, design systems, motion, implementation, QA, and adversarial Gauntlet refinement. What it lacked was **production risk governance**: a first-class system that answers *"what obligations does this website create, and what must the build actually do about them?"*

This protocol is that layer. It runs after conversion measurement is planned and before the design system and implementation specification are finalized, so safeguards **inform** the build rather than being retrofitted onto a shipped site.

```text
PHASE 6: CONTENT STRUCTURE & EVIDENCE PLAN
        ↓
LOCK 3: CONTENT_STRUCTURE_LOCKED
        ↓
PHASE 6.5: CONVERSION & ANALYTICS INTELLIGENCE
        ↓
GATE MEASUREMENT: CONVERSION_MEASUREMENT_COMPLETE
        ↓
PHASE 6.75: SECURITY, PRIVACY & COMPLIANCE INTELLIGENCE
        ↓
GATE SECURITY: SECURITY_PRIVACY_READY
        ↓
PHASE 7: DESIGN SYSTEM TOKEN ARCHITECTURE
        ↓
PHASE 9: IMPLEMENTATION CONTRACT ISSUANCE
```

**Why here.** Data collection is determined by the locked content structure and the CTA/form inventory; tracking technologies are determined by the locked measurement plan. Both must exist before obligations can be derived. Running earlier would invent data flows that do not exist. Running later would force consent UI, disclosure surfaces, and header policy onto a frozen design.

### The Subsystem's Only Job

```text
DISCOVER RISK
      ↓
CLASSIFY REQUIREMENTS
      ↓
SPECIFY SAFEGUARDS
      ↓
GATE IMPLEMENTATION
      ↓
VERIFY IMPLEMENTATION
      ↓
ESCALATE UNKNOWN / HIGH-RISK CONDITIONS
```

---

## 2. System Invariants & Core Governance

1. **Single Completion Flag Invariant:** `security_privacy.complete` in `site-profile.json` is the **only** authoritative readiness flag for `[SECURITY_PRIVACY_READY]`. No second, independently-writable completion flag may ever be created for security/privacy readiness.
2. **No Sixth Owner Lock:** `[SECURITY_PRIVACY_READY]` is a **readiness gate**, not an owner lock. Exactly 5 owner locks remain immutable (`design_direction_locked`, `information_architecture_locked`, `content_structure_locked`, `design_system_locked`, `motion_direction_locked`).
3. **No Legal Certification Invariant:** Website Director must **never** output `GDPR COMPLIANT`, `CCPA COMPLIANT`, `HIPAA COMPLIANT`, `PCI COMPLIANT`, `COPPA COMPLIANT`, or `LEGAL COMPLIANCE VERIFIED`. See §26. Permitted statements are `REQUIREMENTS REVIEWED`, `TECHNICAL CONTROLS IMPLEMENTED`, `KNOWN GAPS DOCUMENTED`, `LEGAL REVIEW REQUIRED`, and `COMPLIANCE_NOT_CERTIFIED`.
4. **Planning ≠ Verification Invariant:** `security_privacy.complete` certifies that requirements are *specified*. It NEVER means safeguards were observed working. Implementation verification is `security_privacy.implementation_verified`. Production verification is `security_privacy.production_verified`. These three states are permanently distinct and must never be collapsed.
5. **Proportionality Invariant:** Requirements derive from **actual functionality**, never from a template. A static brochure site does not inherit ecommerce, authentication, or payment obligations. An authenticated SaaS application is never treated as a brochure site.
6. **Anti-Fabrication Invariant:** Unknown jurisdiction, unknown retention, unknown provider configuration, and unknown deployment environment are recorded as `UNKNOWN` or `UNASSESSED`. Website Director never guesses applicable law, never infers jurisdiction from an IP address, and never invents a retention period.
7. **Data Minimization Invariant:** Every collected field must have a documented purpose. A field present only because a form template contained it is a defect, not a requirement.
8. **Secrets Invariant:** No secret, API key, token, OAuth client secret, database credential, service-account key, or webhook signing secret may appear in client-side source, source control, examples, generated screenshots, logs, or any Website Director artifact. `.env.example` carries names and placeholders only.
9. **Truthful Disclosure Invariant:** Conversion optimization never overrides truthful disclosure or user autonomy. See §27 and §28.
10. **Escalation Over Assertion:** Where applicability cannot be reliably determined from evidence, the correct output is `OWNER_OR_COUNSEL_REVIEW_REQUIRED` or `SPECIALIST_REVIEW_REQUIRED` — never a confident guess and never silence.
11. **Locks Always Win:** Security/privacy may never silently mutate approved IA, locked copy, CTA wording, design tokens, or motion direction. A structural conflict HALTS and produces a locked-change request. See §28.
12. **No External Side Effects:** This protocol produces specifications. It never modifies live websites, deploys, creates analytics properties, configures consent platforms, changes DNS, touches payment accounts, creates legal documents in external systems, contacts attorneys, uses production credentials, transmits personal data, or performs intrusive testing against external systems.

---

## 3. Derived Inputs (Do Not Re-Interview)

Obligations are derived from artifacts that already exist. The owner is re-engaged **only** for genuinely owner-level facts (§29).

| Input Artifact | What Is Extracted |
| :--- | :--- |
| `creative-intent-contract.md` | Business purpose, owner non-negotiables, declared markets |
| `project-brief.md`, `positioning.md` | Business model, audience, commercial posture |
| `information-architecture.md` | Route inventory, form surfaces, authenticated areas, checkout flows |
| `content-plan.md` | Locked copy, CTA labels, marketing claims, testimonials, statistics |
| `measurement-plan.md`, `analytics-event-manifest.json` | Analytics provider, events, parameters, identifiers, `consent_dependency` |
| `site-profile.json` → `measurement{}` | Canonical measurement state (never duplicated here — see §16) |
| `site-profile.json` → `immersive{}`, `rive{}`, `page_experience{}` | Third-party runtime code and embedded services |
| `asset-provenance.md` | Asset licensing and evidence provenance (claim risk input, §22) |
| `ENVIRONMENT-INVENTORY.md`, `DIGITAL-OWNERSHIP-REGISTER.md` (V2.5) | Deployment environments, third-party accounts, secret custody |

---

## 4. Site Risk Classification (`SITE_CLASSIFICATIONS`)

Every project is classified by what it actually does. **A project may carry multiple classifications.** Classification drives which requirement sets activate.

| Classification | Activates |
| :--- | :--- |
| `STATIC_MARKETING` | Transport, headers, third-party inventory, claim risk |
| `CONTENT_PUBLISHER` | Above + storage inventory, embedded media services |
| `AFFILIATE` | Above + affiliate disclosure architecture (§20) |
| `LEAD_GENERATION` | Above + data inventory, form security (§9), consent assessment |
| `ECOMMERCE` | Above + payment boundary (§11), order data handling |
| `AUTHENTICATED_APPLICATION` | Above + authentication/session security (§10) |
| `SAAS` | Above + tenancy/authorization boundaries, account lifecycle |
| `COMMUNITY` | Above + abuse prevention, moderation surface |
| `USER_GENERATED_CONTENT` | Above + upload restrictions, sanitization, hosting exposure |
| `PAYMENT_ENABLED` | Payment provider boundary; raw card handling prohibited (§11) |
| `HEALTH_OR_SENSITIVE_DATA` | Mandatory escalation (§25) |
| `CHILD_DIRECTED_OR_CHILD_ACCESSIBLE` | Mandatory escalation (§24) |
| `INTERNAL_PRIVATE_APPLICATION` | Access boundary, environment separation; public-web obligations may not apply |

**Classification rules:**
- Classify from the built/locked functionality inventory, not from the owner's aspiration or the industry label.
- Do not impose ecommerce requirements on a static brochure site.
- Do not treat an authenticated SaaS application like a static marketing site.
- A classification that *may* apply but cannot be confirmed is recorded and escalated, never silently dropped.

---

## 5. Risk Level Model (`RISK_LEVEL`)

```text
LOW
MODERATE
HIGH
SPECIALIST_REVIEW_REQUIRED
```

Risk level is **derived deterministically** from behavior and data handling, not assigned by feel.

| Level | Deterministic Factors |
| :--- | :--- |
| `LOW` | No personal data collected; no authentication; no payment; no consent-dependent tracking; no UGC; no elevated-risk claims. Typically `STATIC_MARKETING`. |
| `MODERATE` | Collects ordinary contact data (name/email/phone/message) **or** runs consent-dependent analytics/advertising **or** carries affiliate/sponsored relationships. Typically `LEAD_GENERATION`, `AFFILIATE`, `CONTENT_PUBLISHER`. |
| `HIGH` | Authentication, accounts, payments, user-generated content, file uploads, precise location, or third-party data sharing beyond basic analytics. Typically `AUTHENTICATED_APPLICATION`, `SAAS`, `ECOMMERCE`, `COMMUNITY`, `USER_GENERATED_CONTENT`, `PAYMENT_ENABLED`. |
| `SPECIALIST_REVIEW_REQUIRED` | Health/medical data, biometric data, government identifiers, highly sensitive financial data, children's data, or any condition under §24–§25. |

**Rules:**
- A static brochure site does not automatically become `HIGH`.
- A site collecting highly sensitive information never remains `LOW`.
- The factors that produced the level are recorded in `security-privacy-review.md` §1 — the level is auditable, not asserted.
- `SPECIALIST_REVIEW_REQUIRED` is a terminal escalation state, not a severity synonym; it sets `security_privacy.specialist_review_required = true`.

---

## 6. Data Inventory

For **every** data class the site collects, receives, stores, or transmits, record all ten fields. An incomplete row means the inventory is incomplete.

```text
DATA_CLASS            What is collected (e.g. email address)
SOURCE                Where it originates (visitor form, cookie, header, upload)
PURPOSE               Why it is needed, in business language
COLLECTION_POINT      Route + component (e.g. /contact → ConsultationForm)
DESTINATION           Where it goes (server endpoint, inbox, CRM, provider)
THIRD_PARTY           Any external processor, or NONE
RETENTION_KNOWN       TRUE | FALSE (FALSE is honest; a guess is not)
CONSENT_DEPENDENCY    REQUIRED | NOT_REQUIRED | UNASSESSED
SENSITIVITY           ORDINARY | ELEVATED | SENSITIVE
PRODUCTION_REQUIRED   TRUE | FALSE (FALSE is a §7 removal candidate)
```

**Data categories to consider** — name, email, phone, postal address, account identifiers, authentication data, payment-related data, analytics identifiers, cookies, device/browser data, IP-related telemetry, support messages, uploaded files, user-generated content, precise location, health information, minors' information, and any other sensitive personal data.

> **Never assume a field is harmless simply because it is common.** A phone number, an IP address, and a free-text "how can we help?" box each carry obligations that a template will not tell you about.

Inventory completion sets `security_privacy.data_inventory_complete = true`.

---

## 7. Data Minimization

Before any field is accepted into the specification, Website Director asks: **do we actually need to collect this?**

Enforced rules:

1. **Necessity:** Collect only what a documented purpose requires.
2. **No template inheritance:** A field is never included because a form library, starter template, or competitor form contained it.
3. **No sensitive-by-default:** Sensitive categories are never collected unless the business function genuinely requires them and the owner has confirmed the purpose.
4. **No speculative collection:** "We might want it for marketing later" is not a purpose. Unless a legitimate present purpose is documented, the field is removed.
5. **No duplicate collection:** The same data class is not collected twice across surfaces without a distinct purpose.
6. **Required vs optional is explicit:** Every retained field is marked `REQUIRED` or `OPTIONAL` in the specification and implemented that way.
7. **Free-text discipline:** Open message fields are minimized in number, never pre-populated with personal data, and never forwarded to analytics.

**Data minimization is a design and architecture requirement, not a footer concern.** Removing a field is a legitimate — and preferred — outcome of this phase, subject to §28 (a locked-copy or locked-IA change requires an owner change request, never a silent edit).

---

## 8. Secret & Credential Governance

Governs API keys, access tokens, private credentials, OAuth client secrets, database credentials, analytics administration credentials, payment provider secrets, service-account credentials, and webhook signing secrets.

**Requirements:**

1. **No secrets in client-side source.** Anything shipped to the browser is public. A key that must remain private cannot live in front-end code, inline script, data attribute, or bundled config.
2. **No secrets committed to Git.** Ever, including in history, fixtures, and test files.
3. **No production credentials in examples**, documentation, validation artifacts, or worked examples.
4. **Environment/configuration boundary.** Secrets are supplied via environment or platform secret storage, read server-side only.
5. **`.env.example` carries names and placeholders only** — never a real value.
6. **Redact secrets from logs**, error messages, and stack traces.
7. **Never expose secrets in generated screenshots, evidence captures, or reports.** Evidence capture must mask credential-bearing surfaces.
8. **Fail closed where feasible.** Where a required secret is absent, the dependent feature refuses to operate rather than silently degrading into an insecure or misleading state. The site's core content must remain functional.

**Boundary:** Website Director **identifies** which secrets the architecture requires and where they must live. It **never** requests that a real credential be pasted into a documentation artifact, a template, a project file, or a chat message. Public configuration identifiers that are legitimately non-secret (e.g. a GA4 measurement ID, a publishable payment key) are recorded as *configuration references*, clearly distinguished from secrets.

---

## 9. Form Security

Applies wherever the locked IA contains a form. Specify each applicable control:

1. **Server-side validation is the trust boundary.** Every constraint enforced client-side is re-enforced server-side.
2. **Client-side validation is UX only.** It is never relied upon for safety, authorization, or data integrity.
3. **Sanitization & output encoding.** User input is encoded for the context in which it is rendered; never interpolated raw into HTML, SQL, shell, or templates.
4. **CSRF protection** for state-changing requests on session-authenticated surfaces.
5. **Bot/spam mitigation** proportionate to the surface (honeypot, timing heuristic, provider challenge). Any challenge must satisfy §23 accessibility dependency.
6. **Abuse prevention** for surfaces that send mail, create records, or consume paid third-party quota.
7. **Rate limiting** on submission endpoints.
8. **Safe error handling.** Errors are helpful to the user and non-revealing about internals — no stack traces, no database errors, no framework internals surfaced to the visitor.
9. **No sensitive values in URLs.** Never in query strings, path segments, fragments, redirects, or referrer-leaking links.
10. **File-upload restrictions** where uploads exist: allow-list of types, enforced size limits, validated content type (not merely the extension), non-executable storage location, and filenames that cannot traverse paths.
11. **Safe email handling.** No header injection from user input; no unvalidated recipient control; no reflected user content in outbound mail without encoding.
12. **Duplicate-submit protection.** Submit controls guard against rapid repeat submission — aligning with the measurement plan's deduplication rules (§16).
13. **Success-event correctness.** A success state — visual *and* instrumented — is shown only on confirmed server success. A server-rejected submission never renders success and never emits a success conversion event.

> The Browser / Regression QA subsystem will exercise these behaviors. **This subsystem defines the requirements**; it does not itself run the tests.

---

## 10. Authentication & Session Security

Applies **only** where the locked IA contains authentication. Do not specify authentication architecture for a website that does not require authentication.

Where applicable, specify:

1. **Secure password handling** — modern, salted, slow password hashing. **Never store plaintext passwords.** Never store a reversible encryption of a password.
2. **Secure session cookies** — `HttpOnly`, `Secure`, and an appropriate `SameSite` value justified by the actual cross-site flows the site requires.
3. **Session expiration** — idle and absolute lifetimes defined.
4. **Logout behavior** — server-side session invalidation, not merely clearing a client cookie.
5. **Authorization boundaries** — every protected resource authorizes on the server per request. Hiding a link in the UI is not authorization.
6. **Account recovery** — single-use, expiring tokens; no account enumeration through differential responses or timing.
7. **Brute-force protections** — throttling and lockout/backoff on credential endpoints.
8. **MFA capability where risk justifies it** — specified, not assumed, based on `RISK_LEVEL` and data sensitivity.
9. **Reauthentication for sensitive actions** — email/password change, payment method change, data export, account deletion.

---

## 11. Payment Boundary

Applies where `PAYMENT_ENABLED` or `ECOMMERCE` is classified.

```text
PAYMENT PROVIDER INTEGRATION
        ≠
STORING PAYMENT CARD DATA
```

**Rules:**

1. **Strongly prefer an established payment provider** with a hosted or provider-controlled card entry surface. Card data should never traverse the project's own application code.
2. **Website Director must never instruct a normal website build to store raw card numbers, CVV/CVC values, full magnetic-stripe data, or PINs.** This prohibition is absolute for ordinary website builds.
3. **Provider secrets** follow §8. Publishable/public keys are configuration references; secret keys are secrets.
4. **Webhook integrity** — payment webhooks verify provider signatures; order state is never trusted from a client-supplied redirect alone.
5. **Where PCI-related obligations may apply, flag them for qualified review.** Record `legal_review_required = true` or `specialist_review_required = true` as appropriate.
6. **Do not claim PCI compliance merely because Stripe, PayPal, Adyen, or any other provider is used.** Using a compliant provider reduces scope; it does not certify the merchant. See §26.

---

## 12. Security Headers

For deployed public web surfaces, assess and specify the applicable headers:

- `Content-Security-Policy`
- `Strict-Transport-Security`
- `X-Content-Type-Options`
- `Referrer-Policy`
- `Permissions-Policy`
- Frame-ancestor / clickjacking protection (`frame-ancestors` in CSP; `X-Frame-Options` where legacy support is required)
- Cross-origin policies (`Cross-Origin-Opener-Policy`, `Cross-Origin-Resource-Policy`, `Cross-Origin-Embedder-Policy`) **where justified** by the actual isolation requirement

**Rules:**

1. **Do not blindly apply one CSP template to every stack.** A CSP is derived from this project's real runtime dependency graph.
2. **CSP must account for required** analytics, fonts, CDNs, media, APIs, payment providers, and embedded services — every origin traced to an entry in the §15 third-party inventory.
3. **Every allowed origin needs a reason.** An origin in the policy with no corresponding inventory entry is a defect.
4. **Security configuration must be evidence-driven.** Where the deployment platform's header capability is unknown, that is a §32 blocker (`unknown deployment environment`), not an assumed default.
5. **Report-only first is acceptable** as a specified rollout step, provided the enforcement target is documented.
6. Where `immersive{}`, `rive{}`, embedded video, or map services are active, their origins, worker/WASM requirements, and `blob:` needs are reconciled into the policy rather than resolved by widening it to `unsafe-*`.

---

## 13. HTTPS / Transport

Production HTTPS is required for any public production website with meaningful user interaction.

Verify (at the appropriate verification stage, §35):

1. **HTTPS redirect behavior** — HTTP requests redirect to HTTPS.
2. **Mixed-content absence** — no scripts, styles, images, fonts, media, or XHR loaded over plaintext.
3. **Secure asset loading** — all first- and third-party assets over HTTPS.
4. **Production canonical URLs use HTTPS** — canonical tags, `og:url`, sitemap entries, and structured data all agree with the SEO specification.
5. **Secure-cookie assumptions align with deployment** — a `Secure` cookie requires an HTTPS origin in the environment where it is set.

> **Local development over HTTP is not a production failure.** `localhost`/development origins are explicitly out of scope for this requirement. Do not report a development server as a transport defect.

---

## 14. Dependency & Supply Chain Governance

Applies to projects with package dependencies.

1. **Record major production dependencies** — name, purpose, and whether the code executes on the client, the server, or both.
2. **Avoid unnecessary packages.** A dependency added for one utility function is a supply-chain surface; prefer the platform.
3. **Identify the vulnerability scanning mechanism** available for the stack (e.g. the package manager's audit command, the host's dependency alerts) and record it. Where none is available, record `UNKNOWN` — do not imply scanning occurred.
4. **Prohibit abandoned or unvetted packages** where a reasonable maintained alternative exists.
5. **Document third-party scripts** — every externally loaded runtime script is inventoried under §15.
6. **Distinguish first-party code from externally loaded runtime code.** Externally hosted code can change after review; first-party bundled code cannot.
7. **Avoid duplicate libraries** — one animation library, one analytics runtime, one framework instance.
8. **Pin/lock dependencies appropriately for the stack** — a lockfile is committed where the ecosystem provides one.

> **Do not claim a dependency is safe merely because installation succeeded.** Installation proves resolution, not safety.

---

## 15. Third-Party Script Inventory

**Every production third-party runtime script must have a reason.** Typical services: analytics, tag managers, advertising pixels, chat widgets, embedded video, payment services, maps, social widgets, A/B testing platforms, customer-support tools.

For each, record:

```text
SERVICE               Vendor and product
PURPOSE               The business reason it exists
DATA_EXPOSED          What the vendor can observe
PAGE_SCOPE            Which routes load it (never "all" by default)
CONSENT_DEPENDENCY    REQUIRED | NOT_REQUIRED | UNASSESSED
SECURITY_IMPLICATION  What its compromise or change would mean
REMOVAL_IMPACT        What breaks if it is removed
```

**Rules:**
- **Unexplained third-party scripts are prohibited.** A script present in the build but absent from this inventory is a gate failure and a Gauntlet defect.
- Scripts default to the narrowest `PAGE_SCOPE` that satisfies their purpose.
- Every inventory entry's origins must reconcile with the §12 CSP.
- Consent-dependent services must not load before consent where §17 records consent as `REQUIRED`.

Inventory completion sets `security_privacy.third_party_inventory_complete = true`.

---

## 16. Analytics & Measurement Privacy Integration

**This subsystem does not create a second analytics model.** `site-profile.json` → `measurement{}` and `templates/measurement-plan.md` remain the canonical measurement authority (`CONVERSION-ANALYTICS-PROTOCOL.md`). Security/Privacy **consumes** that state and reviews it.

Reviewed:

- Analytics provider and hosting model
- Cookies and storage the provider sets
- Identifiers (client IDs, user IDs, advertising IDs)
- Event payloads and parameter registry
- PII risk in every parameter
- Advertising features (remarketing, conversion linking, ad personalization)
- Cross-domain behavior and linker configuration
- Consent dependencies per event and per service
- Retention configuration where the provider exposes it
- Third-party data sharing implied by the provider's own terms

**Maintained invariant — no PII in analytics by default.** Forbidden in any payload or UTM parameter: email, phone, full name, postal address, free-text message bodies, passwords, payment card data, medical information, government identifiers, date of birth. Validation-error events carry a field **category**, never a field **value**.

**Authority boundary:**

- Security/Privacy **may block activation** of a measurement integration until privacy requirements are satisfied. It records the block; the measurement plan itself remains complete and usable.
- Security/Privacy **must not rewrite measurement strategy silently.** A required change to the KPI hierarchy, event taxonomy, or funnel model is raised back to `CONVERSION-ANALYTICS-PROTOCOL.md` as a measurement change request, decided there, and reflected in `measurement{}`.
- Where this review resolves a consent question, the resolution is written to **both** `security_privacy.consent_status` (authoritative for the obligation) and `measurement.consent_dependency` (authoritative for the tracking integration). The two must agree; where they cannot, the phase is blocked, not reconciled by guesswork.
- Session replay remains `DISABLED` unless the owner explicitly justifies it *and* a strict masking policy is specified.

---

## 17. Consent Classification (`CONSENT_STATUS`)

```text
NOT_REQUIRED
REQUIRED
CONDITIONALLY_REQUIRED
UNASSESSED
OWNER_OR_COUNSEL_REVIEW_REQUIRED
```

**Do not guess applicable law from an IP address or assumed geography.**

Factors considered:

- Business location(s)
- Target audience and owner-declared markets
- Actual tracking technologies present (from §15 and §18)
- Advertising use, remarketing, and data sharing
- Cookies and client-side storage in use
- Sensitive data categories in the §6 inventory
- Children/minors exposure (§24)

**Rules:**

1. A site with **no** cookies, no client-side storage beyond strictly necessary function, and no tracking may legitimately be `NOT_REQUIRED` — recorded with the reasoning.
2. Consent-dependent tracking present + confirmed relevant market ⇒ `REQUIRED`.
3. Consent obligation depends on a market or feature decision the owner has not made ⇒ `CONDITIONALLY_REQUIRED`, with the deciding condition stated.
4. Not yet assessed ⇒ `UNASSESSED`. Never default to `NOT_REQUIRED`.
5. **If legal applicability cannot be reliably determined, `OWNER_OR_COUNSEL_REVIEW_REQUIRED` is the correct outcome.** It is a valid, complete answer — not a failure.
6. Where consent is `REQUIRED`, consent-dependent scripts and storage must not execute or be written before consent is given, and the consent UI must satisfy §23 and §27.

---

## 18. Cookie & Browser Storage Inventory

Wherever cookies, `localStorage`, `sessionStorage`, IndexedDB, cache-based persistence, or fingerprinting-adjacent techniques are used, record:

```text
NAME_OR_CATEGORY
PURPOSE
OWNER                     First-party name or third-party vendor
FIRST_OR_THIRD_PARTY
LIFETIME                  Session | duration | UNKNOWN
ESSENTIAL_OR_OPTIONAL
CONSENT_DEPENDENCY        REQUIRED | NOT_REQUIRED | UNASSESSED
```

**Rules:**
- **Do not label advertising or analytics storage "essential" merely because the business wants it.** "Essential" means the site's requested functionality genuinely cannot operate without it.
- Storage with no inventory entry is a defect.
- `LIFETIME = UNKNOWN` is honest for third-party storage whose duration is vendor-controlled; a fabricated duration is not.
- Fingerprinting-adjacent techniques (canvas, font enumeration, device-signal hashing) are never introduced for measurement convenience and require explicit owner authorization plus consent assessment.

---

## 19. Privacy Notice Requirements

Website Director determines whether the site's **functionality** creates a likely requirement for a privacy notice — and, where it does, specifies the **categories of disclosure** the notice must cover:

- What is collected
- Why it is collected
- Third parties involved
- Cookies and tracking technologies
- User choices and how to exercise them
- A contact method

**Boundary:**

- Website Director specifies **requirements and placement**, and may draft plain-language explanatory content grounded in the §6/§15/§18 inventories.
- Website Director does **not** provide jurisdiction-specific legal certification and does not represent drafted text as legally sufficient.
- Where drafting or sufficiency goes beyond available evidence, set `legal_review_required = true` and record `OWNER_OR_COUNSEL_REVIEW_REQUIRED`.
- Where a notice is required, the route must exist in the locked IA. If it does not, that is a locked-change request to the owner (§28), not a silent page addition.

---

## 20. Affiliate Disclosure

For affiliate websites and any page containing compensated links, visible disclosure architecture is required where applicable.

```text
AFFILIATE DISCLOSURE
        ≠
PRIVACY POLICY
        ≠
TERMS
        ≠
ADVERTISING CONSENT
```

These are four distinct obligations with distinct surfaces. Satisfying one never satisfies another.

**Placement requirements:**
- Disclosure must be **discoverable at the point of the recommendation**, not exclusively in a remote footer page, wherever the applicable disclosure must be near the recommendation.
- Disclosure must be visible without interaction — not hidden behind a collapsed accordion, a tooltip, or a hover state.
- Disclosure must be styled to be legible: it may be restrained, but it may not be visually suppressed (see §27).
- The design system must accommodate the disclosure surface. "There is no room in the layout" is a design problem to solve, never a reason to omit disclosure.

**Boundary:** Website Director defines **placement, prominence, and presence requirements**. Exact legal wording may require owner review; where the owner has no approved wording, record it as an owner decision rather than shipping invented legal language.

---

## 21. Advertising & Sponsored Content

Where sponsored placements, paid reviews, or promotional partnerships exist:

1. Identify the disclosure need for each placement.
2. **Visual design must never obscure sponsorship or affiliate relationships.** Sponsored units must be distinguishable from editorial content.
3. Disguised advertising — sponsored content styled to be indistinguishable from independent editorial — is prohibited (§27).
4. **Trust and conversion goals never override truthful disclosure** (§28).

---

## 22. Marketing Claim & Testimonial Risk

Where marketing claims, testimonials, ratings, statistics, certifications, or performance claims appear in locked copy, each requires recorded evidence/provenance.

**Elevated-risk claim patterns:** "best", "#1", "clinically proven", "guaranteed", income claims, performance claims, customer counts, percentage improvements, named certifications, and testimonial attribution.

**Rules:**
1. Each flagged claim records: the claim text, its location, the evidence supporting it, and the evidence's provenance.
2. **Do not fabricate supporting evidence.** No invented statistics, no invented customers, no invented certifications, no invented review counts.
3. **Do not allow design polish to turn a hypothesis into a factual claim.** A confident typographic treatment does not create evidence.
4. An unsupported claim is recorded as a **known gap** and escalated to the owner. Website Director does not silently rewrite locked copy to remove it (§28) — it raises a locked-change request.
5. Testimonials must be attributable and real; `DESIGN-CONSTITUTION.md` §7.7 (Absolute Factual Integrity) and `ASSET-DIRECTOR-PROTOCOL.md` provenance rules continue to apply unchanged.

> **Forward boundary:** A dedicated Evidence & Asset Provenance subsystem is future work. This section defines the **safety boundary only** — flag, record, escalate. It does not implement a provenance subsystem, and it does not duplicate `asset-provenance.md`.

---

## 23. Accessibility Dependency

A dedicated Accessibility subsystem is **future work** and is not implemented or duplicated here. However, security and privacy UI must not introduce inaccessible patterns.

Recorded as an accessibility dependency wherever this subsystem introduces UI:

- Consent dialogs must be keyboard operable, focus-managed, and screen-reader announced.
- No keyboard traps in consent, cookie, or disclosure surfaces.
- Disclosures must meet the same legibility and contrast standard as body copy — never a low-contrast micro-type footnote.
- **Rejecting optional processing must be as reachable as accepting it** — same number of interactions, same discoverability (see §27).
- Bot challenges must offer an accessible path.

Where such UI exists, `security_privacy.accessibility_dependency_recorded` is set `true` and the specific dependencies are listed in `security-privacy-review.md` for the future accessibility subsystem to consume. Existing `PRODUCTION-CHECKLIST.md` §3 and the Gauntlet Accessibility Critic continue to govern accessibility itself.

---

## 24. Children & Minors

If the site is intentionally directed toward children, or knowingly handles children's data, **escalate automatically**.

- Set `security_privacy.sensitive_data_detected = true` and `security_privacy.specialist_review_required = true`.
- Set `RISK_LEVEL = SPECIALIST_REVIEW_REQUIRED`.
- Record `SPECIALIST_OR_COUNSEL_REVIEW_REQUIRED`.
- **Do not attempt to self-certify COPPA or any equivalent jurisdictional obligation.**
- Do not design age gates, parental-consent flows, or data practices for this category on Website Director's own authority; specify that qualified review determines the requirements.

---

## 25. Health & High-Sensitivity Data

Escalate where the project handles medical information, health records, diagnoses, biometric data, highly sensitive financial information, government identifiers, or other high-risk data.

- Set `security_privacy.sensitive_data_detected = true` and `security_privacy.specialist_review_required = true`.
- Set `RISK_LEVEL = SPECIALIST_REVIEW_REQUIRED`.
- Record `COMPLIANCE_NOT_CERTIFIED` and `SPECIALIST_REVIEW_REQUIRED`.
- **Never claim HIPAA, GDPR, GLBA, state-law, or any other compliance from the presence of generic security controls.** Encryption in transit, a privacy policy, and secure cookies are not a compliance program.
- Technical controls may still be specified and implemented; they are reported as **technical controls implemented**, never as compliance achieved.

---

## 26. Legal Claim Boundary

Website Director must **NEVER** output:

```text
GDPR COMPLIANT
CCPA COMPLIANT
HIPAA COMPLIANT
PCI COMPLIANT
COPPA COMPLIANT
LEGAL COMPLIANCE VERIFIED
```

— unless such status originates from an appropriate external qualified process that Website Director can actually evidence and cite.

Permitted, evidence-supported statements:

```text
REQUIREMENTS REVIEWED
TECHNICAL CONTROLS IMPLEMENTED
KNOWN GAPS DOCUMENTED
LEGAL REVIEW REQUIRED
COMPLIANCE_NOT_CERTIFIED
SPECIALIST_REVIEW_REQUIRED
```

This boundary applies to every Website Director surface: the review artifact, QA reports, the production checklist, client handoff documents, commit messages, and conversational summaries.

---

## 27. Dark Pattern Prohibition

Security and privacy UI must not manipulate users. Prohibited:

1. **Intentionally difficult rejection** — "Reject" requiring more clicks, more scrolling, or a submenu that "Accept" does not.
2. **Misleading button hierarchy** — the privacy-preserving choice visually demoted to near-invisibility while the data-maximizing choice is a primary button.
3. **Deceptive consent wording** — ambiguous labels, double negatives, or copy that misstates what is being agreed to.
4. **Prechecked optional consent** without justification.
5. **False urgency** — countdown timers, fake scarcity, or invented deadlines around a privacy or purchase decision.
6. **Hidden opt-out mechanisms.**
7. **Obstructive unsubscribe mechanisms.**
8. **Consent walls where inappropriate** — blocking all content behind acceptance of non-essential processing.
9. **Disguised advertising** — sponsored or affiliate content presented as independent editorial.

**Website Director conversion optimization must never override user autonomy.** This extends `CONVERSION-ANALYTICS-PROTOCOL.md` §2.6 (`DARK_PATTERN_CHECK`) to the privacy surface specifically; it does not create a competing check. The status remains recorded at `measurement.dark_pattern_check` for measurement surfaces and at `security_privacy.dark_pattern_review` for privacy/disclosure surfaces, with the same `PASS`/`FAIL` semantics.

---

## 28. Precedence: Security & Privacy Over Conversion

**Security and privacy requirements override conversion optimization where they conflict.**

| Conversion Wants | Privacy/Security Requires | Winner |
| :--- | :--- | :--- |
| Silent tracking from first paint | Consent before consent-dependent tracking | **Privacy** |
| Affiliate disclosure hidden or footer-only | Disclosure near the recommendation | **Truthful disclosure** |
| Extra form fields for future marketing | Documented purpose per field | **Data minimization**, unless a legitimate purpose is documented |
| Prominent "Accept", suppressed "Reject" | Symmetrical choice | **User autonomy** |
| Fire conversion on click for cleaner funnels | Success only on confirmed server success | **Correctness** |
| Session replay for UX insight | Disabled by default, masking policy required | **Privacy** |
| Sponsored unit styled as editorial | Distinguishable sponsorship | **Truthful disclosure** |

**Locks still win over both.** Where a required safeguard cannot be implemented without changing locked IA, locked copy, CTA wording, design tokens, or motion direction:

```text
HALT.
Generate a locked-change request.
Present it to the owner with the obligation, the evidence, and the consequence of not changing.
Do not silently edit the website.
```

---

## 29. Owner Authority

This subsystem must not make owner-level legal or business decisions silently. **Owner review is required** for:

- Which markets and jurisdictions the business serves
- Accepting a documented legal or security risk
- Selecting analytics, advertising, or consent providers
- Materially changing what data is collected
- Escalating to specialist or legal counsel
- Approving privacy notice content where appropriate
- Authorizing any exception (§33)

Technical defaults **may be recommended** — clearly labelled as `WEBSITE_DIRECTOR_RECOMMENDED` — but a recommendation is never recorded as owner approval. Owner decisions are recorded with what was decided and that the owner decided it.

---

## 30. State Model & Semantics

### 30.1 The `security_privacy{}` Object

`security_privacy{}` in `site-profile.json` is the sole authoritative security/privacy/compliance state. See §31 for the schema. No other object, file, or flag may record security/privacy readiness.

### 30.2 What `security_privacy.complete = true` Means

It means **all** of the following:

- Risk classification is completed (`site_classifications` + `risk_level`)
- The data inventory is completed
- Applicable technical requirements are identified (forms, auth, payment, secrets, headers, transport, dependencies, third-party scripts — each either specified or recorded `NOT_APPLICABLE`)
- Consent and privacy dependencies are identified
- Required disclosures are identified
- High-risk unknowns are escalated
- Implementation requirements are specified well enough for the builder to execute

### 30.3 What It Does NOT Mean

`security_privacy.complete = true` **NEVER** means any of:

- Legal compliance is certified
- Production implementation is verified
- A penetration test was performed
- The site is vulnerability-free
- Production privacy configuration is verified

| Flag | Certifies | Set When |
| :--- | :--- | :--- |
| `security_privacy.complete` | Requirements are specified and implementable | End of Phase 6.75 |
| `security_privacy.implementation_verified` | Specified controls were verified in the built artifact | Post-build (Phase 11/12), by inspection + browser/network evidence |
| `security_privacy.production_verified` | Controls were verified on the deployed production surface | Post-deployment, by owner-supplied or directly observable production evidence |

These three states are permanently distinct. Setting a later flag never implies an earlier one; setting an earlier one never implies a later one.

### 30.4 `security_privacy.status` Values

| Value | Meaning |
| :--- | :--- |
| `not_evaluated` | Phase 6.75 has not run |
| `assessing` | Phase 6.75 in progress |
| `requirements_ready` | Requirements specified and implementable |
| `blocked` | Strategy known, a required input unavailable (§32) |
| `escalated` | Specialist or counsel review required before proceeding (§24, §25) |
| `exception` | Bounded exception recorded (§33) |
| `not_required` | Surface genuinely outside scope with recorded justification |

---

## 31. `site-profile.json` Schema

```json
"security_privacy": {
  "complete": false,
  "status": "not_evaluated",
  "risk_level": null,
  "site_classifications": [],
  "data_inventory_complete": false,
  "data_minimization_reviewed": false,
  "third_party_inventory_complete": false,
  "storage_inventory_complete": false,
  "consent_status": "UNASSESSED",
  "privacy_notice_required": "UNASSESSED",
  "disclosure_requirements": [],
  "secrets_policy_defined": false,
  "form_security_required": false,
  "authentication_required": false,
  "payment_model": "NOT_APPLICABLE",
  "security_headers_defined": false,
  "transport_policy_defined": false,
  "dependency_policy_defined": false,
  "sensitive_data_detected": false,
  "specialist_review_required": false,
  "legal_review_required": false,
  "dark_pattern_review": "not_evaluated",
  "accessibility_dependency_recorded": false,
  "claim_risk_reviewed": false,
  "known_gaps": [],
  "compliance_certified": false,
  "implementation_verified": false,
  "production_verified": false,
  "blocked_reason": null,
  "exception": {
    "applied": false,
    "reason": null
  }
}
```

**Field notes:**

- `risk_level` — `null` | `"LOW"` | `"MODERATE"` | `"HIGH"` | `"SPECIALIST_REVIEW_REQUIRED"`
- `site_classifications` — array of §4 values; may contain more than one
- `consent_status` — `"NOT_REQUIRED"` | `"REQUIRED"` | `"CONDITIONALLY_REQUIRED"` | `"UNASSESSED"` | `"OWNER_OR_COUNSEL_REVIEW_REQUIRED"`
- `privacy_notice_required` — `"YES"` | `"NO"` | `"UNASSESSED"` | `"OWNER_OR_COUNSEL_REVIEW_REQUIRED"`
- `payment_model` — `"NOT_APPLICABLE"` | `"HOSTED_PROVIDER"` | `"PROVIDER_ELEMENTS"` | `"UNRESOLVED"`. **Raw card storage is not a permitted value.**
- `dark_pattern_review` — `"not_evaluated"` | `"PASS"` | `"FAIL"`
- `compliance_certified` — **permanently `false`.** Website Director has no mechanism to set it `true`. It exists so that any downstream consumer reading for a compliance claim gets an explicit `false` rather than an absent key. See §26.
- `known_gaps` — array of plain-language strings; an empty array means none were found, not that none were looked for.

---

## 32. Blocked Mode

`security_privacy.status = "blocked"` applies where the **requirements are understood** but a required input is genuinely unavailable.

Legitimate blockers:

- Unknown deployment environment (header/transport capability undeterminable)
- Provider configuration unavailable
- Privacy decision unresolved by the owner
- Legal review required and not yet obtained
- Authentication architecture unresolved
- Payment architecture unresolved
- Required credentials unavailable (and must never be requested or used)
- Third-party service unknown or unnamed

**Rules:**

- Everything determinable is still specified — the review artifact remains usable.
- `security_privacy.blocked_reason` records the specific blocker in plain language.
- `security_privacy.complete` MAY be `true` in blocked mode **if and only if** the requirement specification itself is complete and the blocker is purely an implementation-capability blocker. A blocker that leaves an *obligation* unknown (e.g. unresolved consent applicability) keeps `complete = false`.
- `implementation_verified` and `production_verified` remain `false`.
- **Never fabricate completion.** A blocked item stays honestly blocked through QA, the production checklist, and client handoff.

---

## 33. Exception Mode

Bounded exceptions are permitted only for surfaces where production risk governance is genuinely inapplicable:

- Offline prototype
- Static disposable concept
- Internal non-production visual exploration

**Rules:**

- An exception must be **explicit, documented, justified, and visible** in `site-profile.json` (`security_privacy.exception.applied = true` with a substantive `reason`).
- **A public commercial site that collects data may never receive a blanket exception.** If the surface collects data or is publicly reachable, the correct state is `blocked` or `requirements_ready`, never `exception`.
- An exception is never applied because the assessment was difficult, because the deployment target was unknown (that is `blocked`, §32), or because the phase was skipped.
- Exceptions require owner authorization (§29).

---

## 34. Readiness Gate: `[SECURITY_PRIVACY_READY]`

The gate engages when **all** of the following hold:

```text
SITE_CLASSIFICATION_COMPLETE        = TRUE
RISK_LEVEL_ASSIGNED                 = TRUE   (with recorded deterministic factors)
DATA_INVENTORY_COMPLETE             = TRUE   (all 10 fields per data class)
DATA_MINIMIZATION_REVIEWED          = TRUE
SECRETS_POLICY_DEFINED              = TRUE
FORM_SECURITY_SPECIFIED             = TRUE | NOT_APPLICABLE
AUTH_SECURITY_SPECIFIED             = TRUE | NOT_APPLICABLE
PAYMENT_BOUNDARY_SPECIFIED          = TRUE | NOT_APPLICABLE
SECURITY_HEADERS_SPECIFIED          = TRUE | FORMALLY_BLOCKED
TRANSPORT_POLICY_SPECIFIED          = TRUE
DEPENDENCY_POLICY_SPECIFIED         = TRUE | NOT_APPLICABLE
THIRD_PARTY_INVENTORY_COMPLETE      = TRUE   (zero unexplained scripts)
STORAGE_INVENTORY_COMPLETE          = TRUE
ANALYTICS_PRIVACY_REVIEWED          = TRUE | NOT_APPLICABLE
CONSENT_STATUS_RECORDED             = TRUE   (any §17 value; unrecorded is not)
PRIVACY_NOTICE_REQUIREMENT_RECORDED = TRUE
DISCLOSURE_REQUIREMENTS_RECORDED    = TRUE | NOT_APPLICABLE
CLAIM_RISK_REVIEWED                 = TRUE
DARK_PATTERN_REVIEW                 = PASS
ACCESSIBILITY_DEPENDENCY_RECORDED   = TRUE | NOT_APPLICABLE
SENSITIVE_DATA_ESCALATED            = TRUE | NOT_APPLICABLE
LEGAL_ESCALATIONS_RECORDED          = TRUE | NOT_APPLICABLE
IMPLEMENTATION_REQUIREMENTS_SPECIFIED = TRUE
VERIFICATION_REQUIREMENTS_SPECIFIED   = TRUE
KNOWN_GAPS_RECORDED                 = TRUE
COMPLIANCE_CERTIFIED                = FALSE  (invariant — never TRUE)
```

On engagement: set `security_privacy.complete = true` and `security_privacy.status` to `requirements_ready`, `blocked`, or `escalated`.

For genuinely out-of-scope surfaces with a recorded exception: `security_privacy.status = "exception"` or `"not_required"` with `exception.applied = true`.

**`escalated` is a valid gate-engaged state.** A project requiring specialist review has completed *this subsystem's* job — discover, classify, specify, escalate — even though it must not proceed to production without that review. The escalation itself is the deliverable.

---

## 35. Verification Model

### 35.1 Implementation Verification (`security_privacy.implementation_verified`)

Performed post-build, before production sign-off, against the built artifact:

- No secrets present in client bundle, source control, or evidence captures
- Every third-party script in the build appears in the §15 inventory
- Every cookie/storage key written appears in the §18 inventory
- Consent-dependent scripts and storage do not execute before consent where consent is `REQUIRED`
- Form validation is enforced server-side, not only client-side
- No sensitive values appear in URLs
- Security-relevant cookie attributes are set as specified
- No PII in analytics payloads — verified against actual network payloads, not source
- Required disclosures are present at the specified placement
- Consent/disclosure UI is keyboard operable and rejection is as reachable as acceptance
- No console/network leakage of internal detail, credentials, or personal data

Evidence: build inspection plus browser and network capture, recorded in the project's evidence directory.

### 35.2 Production Verification (`security_privacy.production_verified`)

Performed only after deployment, against the real production surface:

- HTTPS enforced and redirecting
- No mixed content
- Security headers present as specified
- Production configuration and environment separation confirmed
- Consent behavior matches specification in the production environment

Website Director never sets this flag from inference. Where production evidence is unavailable, the flag stays `false` and the status is reported as `NOT_YET_VERIFIED` — never as passing.

### 35.3 What Verification Never Establishes

Neither flag ever establishes legal compliance, absence of vulnerabilities, or the result of a penetration test. Website Director performs **no** intrusive testing against external systems.

---

## 36. Subsystem Integration Boundaries

1. **Conversion & Analytics Intelligence (V2.6):** `measurement{}` remains the canonical measurement authority. This subsystem reviews and may block activation; it never creates a second analytics model and never silently rewrites measurement strategy (§16).
2. **Client CMS & Handoff (V2.5):** `ENVIRONMENT-INVENTORY.md`, `DIGITAL-OWNERSHIP-REGISTER.md`, and the third-party register are inputs and handoff destinations. Secret custody and third-party accounts are disclosed to the client, never hidden. A blocked or escalated security state is a handoff disclosure.
3. **Asset Director (V2.0):** `asset-provenance.md` remains the authority for asset licensing. §22 covers *claim* risk in copy and does not duplicate asset provenance.
4. **Immersive Web (V2.1) / Rive (V2.2):** WebGL/WASM runtimes, worker origins, and CDN-hosted runtime files are third-party inventory entries (§15) and CSP inputs (§12).
5. **Page Experience (V2.3):** Route transitions must not leak sensitive values into history entries or URLs, and consent state must survive client-side navigation without re-prompting or silently re-enabling tracking.
6. **SEO Intelligence (V1.2):** Canonical URLs, `og:url`, and sitemap entries must use production HTTPS origins (§13.4). A required privacy/disclosure route must appear in the approved page set — via owner change request, never a silent addition.
7. **Accessibility (future capability):** Dependencies are recorded, not implemented (§23).
8. **Evidence & Asset Provenance (future capability):** Only the §22 safety boundary is implemented here.

---

## 37. Gauntlet Integration

**No new critic is created.** The existing Website Gauntlet critics are the qualitative authority, enriched to inspect security/privacy surfaces:

| Critic | Enriched To Inspect |
| :--- | :--- |
| **Trust Critic (4.4)** | Fake or implied security claims, unsupported marketing claims, missing affiliate/sponsorship disclosure, disguised advertising, compliance badges without evidence |
| **Conversion Critic (4.3)** | Conversion pressure that overrides disclosure or consent; excessive form fields with no documented purpose |
| **Accessibility Critic (4.7)** | Inaccessible consent dialogs, keyboard traps, unreadable disclosures, impossible rejection paths |
| **Conversion Measurement & Analytics Critic (4.14)** | Unexplained third-party scripts, consent-dependent tracking firing before consent, PII in payloads, privacy dark patterns |

`BUILDER != CRITIC` is maintained. **No second Gauntlet state machine is created**; findings flow through the existing `gauntlet{}` object.

---

## 38. Required Deliverables

| Artifact | Purpose |
| :--- | :--- |
| `templates/security-privacy-review.md` | The authoritative 25-section security, privacy & compliance review |
| `templates/security-privacy-register.json` | Machine-readable data / third-party / storage inventory register |
| `site-profile.json` → `security_privacy{}` | Machine-readable state |

---

## 39. Backward Compatibility

- A pre-V2.7 project whose `site-profile.json` has no `security_privacy{}` object **remains valid**. Tooling treats it as absent without raising a schema exception.
- **Frozen historical pilots are not retrofitted.** Do not mutate existing frozen Website Director pilot outputs merely to make their state files look current.
- New Website Director projects use V2.7 `security_privacy{}` behavior.
- **Reopened work:** If major new implementation occurs on a historical project — new data collection, new forms, authentication, payments, a new third-party service, or a production deployment — security/privacy review may be required as part of that reopened work. That is a deliberate owner-initiated reopening, never an automatic framework migration.
