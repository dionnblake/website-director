# Browser & Regression QA Plan — [Project Name]

> Authority: `BROWSER-REGRESSION-QA-PROTOCOL.md`. Machine form: `browser-qa-manifest.json`.
> This plan is filled in Phase 10.5, after Phase 10 build, before Phase 11.

## 1. Scope & engine

- **BROWSER_QA_ENGINE:** `playwright` (real browser) / `simulation` (dry run only).
- **Local build under test:** `[path / dev command / static dir]`
- **Production URL (if verifying production):** `[https://…]` or `NOT_YET_DEPLOYED`
- **Cross-browser policy (§30):** smoke = Chromium; release-critical interaction subset = Chromium + Firefox + WebKit.

## 2. Route inventory

| Route | Purpose | Required viewports | Reduced motion | Critical hero asset | Screenshot surfaces |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/` | … | 360 / 390 / 768 / 1024 / 1280 / 1440 | yes | `[asset]` | full, hero |

## 3. Critical components & interactions

| Component | Route(s) | Interaction to exercise | Expected result |
| :--- | :--- | :--- | :--- |
| Mobile nav | all | open → route-change → close | opens; closes on route change; Escape closes; body scroll locked |
| Contact form | `/contact` | invalid submit → server-reject → success | visible error; **no** success state or success event on reject |

## 4. Measurement assertions (from `measurement-plan.md` — do not invent events)

| Event | Route(s) | Trigger | Required params | Fires once |
| :--- | :--- | :--- | :--- | :--- |
| `page_view` | all | route settled | `page_path` | yes |

- PII prohibition: no `email` / `phone` / `name` / `address` / free-text / `card` / `ssn` / `dob` in any payload or UTM.
- A `MACRO` conversion event fires only on confirmed server success.

## 5. Security / privacy assertions (from `security-privacy-review.md` — do not re-author)

- Required headers: `[list from §16 of the review]`
- Consent: `REQUIRED` / `NOT_REQUIRED` / `UNASSESSED` — if `REQUIRED`, analytics/storage inactive before consent; rejection as reachable as acceptance.
- Third-party script inventory: `[declared origins]` — runtime must match.
- Disclosure/privacy routes that must resolve: `[…]`

## 5.1 Localization / internationalization assertions (from `localization-plan.md` — do not re-author)

- Required: `true` / `false`; source locale: `[locale / N/A]`; default locale: `[locale / N/A]`.
- Locale routes: `[PATH_PREFIX / SUBDOMAIN / SEPARATE_DOMAIN / NO_PUBLIC_LOCALE_ROUTING]`.
- Route checks: locale routes resolve; equivalent content mapping is preserved; fallback behaviour is explicit.
- Locale switcher: `[required / not applicable]` — text-labelled, keyboard operable, and current locale announced.
- SEO runtime checks: localized `html lang`, reciprocal `hreflang`, localized self-canonical, localized metadata, and `x-default` where specified.
- Forms: localized labels, validation messages, and consent/error states where applicable.
- Pseudo-localization / expansion target: `[enabled / not applicable]`; RTL target: `[required / not applicable]`.
- Expected runtime failures are `FAIL` or `BLOCKED`; simulation is not implementation or production verification.

## 5.2 Conditional application architecture assertions (from `application-architecture-plan.md` — do not re-author)

- Required: `true` / `false`; activated modules: `[module IDs / none]`.
- Authentication and authorization: server enforcement, object access, recovery, and client-role trust are explicit where required.
- Commerce: canonical server price, payment confirmation, distinct payment/order state, hosted or tokenized collection, signed idempotent webhooks, and authoritative purchase events.
- Subscription, booking, uploads, UGC, transactional email, integrations, private routes, and high-risk operations are checked only when their modules are activated.
- Missing required observations or unavailable providers are `BLOCKED`; simulation does not establish implementation or production verification.
- Real user creation, live payment attempts, raw card data, provider credentials, and external writes are forbidden in QA.

## 6. Reduced-motion assertions (from `motion-direction.md`)

- Motion-heavy surfaces: `[list]` — each must remain meaningful with `prefers-reduced-motion: reduce`; no content permanently hidden awaiting animation.

## 7. Expected network behaviour & allowed exceptions

| Origin | Purpose | Blocking it breaks | Allowed to fail |
| :--- | :--- | :--- | :--- |
| (first-party) | app assets | yes | no |

Every "allowed to fail" entry needs a justification and must assert the site stays functional.

## 8. Visual regression

- **Baseline version:** `[n]` — authorised by `[owner / N/A first run]`
- **Baseline surfaces & keys:** `route@viewport[+rm]`
- **Masks:** `[selector → reason]` — narrow only.
- **Threshold:** exact / `[documented tolerance + reason]`
- Baseline updates require an owner note here. A diff is evidence of change, not automatically a defect.

## 9. Dynamic content stability (§19)

| Dynamic element | Determinism strategy |
| :--- | :--- |
| timestamps | frozen clock in QA mode |
| rotating testimonials | pinned index |

## 10. Evidence

- Evidence directory: `[<project>/evidence/browser-qa]`
- Run: `python browser-qa/runner.py --plan <project>/browser-qa-manifest.json --engine playwright --mode smoke`
- Committed artifacts: the machine evidence manifest + the nominated baseline set only.

## 11. Result

| Field | Value |
| :--- | :--- |
| `browser_qa.complete` | `false` |
| `browser_qa.engine` | `[…]` |
| smoke / responsive / console / network | |
| form / measurement / security_privacy / application / reduced_motion / keyboard_smoke | |
| `visual_regression_status` | `NOT_RUN` |
| `frozen_fixture_integrity` | `UNVERIFIED` |
| `flaky_tests` | `[]` |
| `implementation_verified` (local, real browser) | `false` |
| `production_verified` (real production URL) | `false` |
| `blocked_reason` | `null` |
| Owning-spec conflicts / change requests raised | `[…]` |

framework_version=2.15.0
framework_phase=6.99:Conditional Application Architecture:ACTIVE
framework_gate=APPLICATION_ARCHITECTURE_READY
owner_locks=design_direction_locked,information_architecture_locked,content_structure_locked,design_system_locked,motion_direction_locked
