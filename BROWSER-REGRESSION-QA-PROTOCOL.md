# BROWSER & REGRESSION QA PROTOCOL: MACHINE-EXECUTED VERIFICATION & REGRESSION BASELINE GOVERNANCE

> **Version:** 1.0.0 (Website Director V2.8.0 Subsystem)
> **Status:** Mandatory Post-Build Verification Standard
> **Governance:** Website Director Orchestration Rail (`SKILL.md` §2, Phase 10.5)
> **Readiness Gate:** `[BROWSER_QA_PASS]` — a verification gate, **not** a sixth owner lock.

---

## 1. Mission

Website Director specifies dozens of behaviours an agent is expected to verify — responsive layout, navigation, menus, forms, links, keyboard interaction, reduced motion, viewport behaviour, console cleanliness, Core Web Vitals, security/privacy behaviours, measurement events, route transitions, dynamic states. Historically some pilots wrote their own one-off browser runners and screenshot scripts. This protocol replaces *"the agent says it checked the browser"* with:

```
REQUIREMENT  →  MACHINE-EXECUTED BROWSER TEST  →  EVIDENCE ARTIFACT  →  PASS / FAIL / FLAKY / BLOCKED / NOT_APPLICABLE  →  REGRESSION BASELINE
```

**Browser QA answers one question:** *Did the implementation behave as specified?*
It does **not** answer *"is the result good enough?"* — that is the qualitative **Website Gauntlet** (`WEBSITE-GAUNTLET-PROTOCOL.md`). The two are distinct and are never merged (§16).

---

## 2. Policy vs. Engine (the replaceable-engine principle)

```
┌──────────────────────────────────────────────────────────────────────┐
│ CANONICAL & PERMANENT (this protocol)                                │
│   the assertion catalogue, requirement traceability, the plan/       │
│   manifest templates, the state object, the flake policy, the        │
│   evidence schema, baseline governance, the frozen-project guard     │
├──────────────────────────────────────────────────────────────────────┤
│ REPLACEABLE (BROWSER_QA_ENGINE)                                      │
│   the thing that actually drives a browser                           │
└──────────────────────────────────────────────────────────────────────┘
```

The reusable harness lives at **`browser-qa/`** and ships two engines:

| Engine | Real browser | Use |
| :--- | :--- | :--- |
| `playwright` | yes (Chromium / Firefox / WebKit) | Verifying generated Website Director projects. Requires `playwright` + browsers. |
| `simulation` | no | Deterministic, dependency-free. Drives fixture directories from declared observation data. Used for this framework's own negative-control validation and for dry-running a plan before a real engine is available. |

An engine that is unavailable produces `BLOCKED` with a specific reason (§13). It is **never** silently downgraded to `PASS`. Adding a third engine (Puppeteer/CDP, Selenium, a hosted grid) means implementing the `BrowserQAEngine.observe()` contract in `browser-qa/engine/base.py` — no policy changes.

Persistent background browser daemons remain `REJECTED_FOR_NOW` (`IMPECCABLE-ENGINE-PROTOCOL.md` §8): an engine launches per run and tears everything down in `stop()`.

---

## 3. What this protocol governs

Browser execution · viewport verification · functional smoke testing · navigation testing · form behaviour · JavaScript / console / network errors · visual screenshot evidence · visual regression · reduced-motion testing · keyboard interaction smoke testing · route-transition testing · responsive breakpoints · deterministic evidence storage · baseline management · false-positive prevention · test isolation · local vs. production verification.

It **consumes** and never re-authors: `measurement-plan.md` / `analytics-event-manifest.json` (§13), `security-privacy-review.md` / `security_privacy{}` (§14), `PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md` navigation rules (§8), `MOTION-DIRECTION-PROTOCOL.md` reduced-motion policy (§15), and the locked design spec.

---

## 4. Phase placement & the gate

```
PHASE 10   BUILD
   ↓
PHASE 10.5 AUTOMATED BROWSER & REGRESSION QA   ──►  GATE BROWSER: [BROWSER_QA_PASS]
   ↓
PHASE 11   100-POINT DESIGN QA / IMPECCABLE
   ↓
PHASE 11.5 WEBSITE GAUNTLET
   ↓
PHASE 12   PRODUCTION PRE-FLIGHT
```

`[BROWSER_QA_PASS]` is a **readiness / verification gate**, categorically the same as `[SEO_COMPLETE]`, `[CONVERSION_MEASUREMENT_COMPLETE]`, and `[SECURITY_PRIVACY_READY]` — it is **not an owner lock**. Exactly **five** owner locks remain immutable. `browser_qa{}` contains no lock boolean.

---

## 5. The reusable harness (`browser-qa/`)

```
browser-qa/
  README.md            AGENTS.md
  runner.py            manifest-driven orchestrator + evidence manifest emitter
  config/              viewports.json · browser-policy.json · ignore-justifications.example.json
  engine/              base.py (BROWSER_QA_ENGINE contract) · playwright_engine.py · simulation_engine.py
  assertions/          catalog.py — every check traces to one requirement source (§17)
  guards/              frozen_integrity_guard.py — reusable protected-path guard (§12)
  fixtures/            synthetic scenario pages for the framework's own validation
  evidence/            run artifacts — GIT-IGNORED except this protocol's retention notes
```

**Consumable by generated projects.** A Website Director project ships a `browser-qa-manifest.json` (from `templates/browser-qa-manifest.json`) and runs:

```bash
python browser-qa/runner.py --plan <project>/browser-qa-manifest.json --engine playwright --mode smoke
```

Generated browser profiles, caches, `node_modules`, traces, and ephemeral screenshots are **never** committed by default (`.gitignore`). Project-specific historical QA scripts remain as historical evidence; new and materially reopened builds use this harness.

---

## 6. Viewport matrix

Canonical viewport classes (`browser-qa/config/viewports.json`). Every project must cover one width in **each** class: small mobile, standard mobile, tablet, laptop, desktop.

| Class | Widths | Required |
| :--- | :--- | :--- |
| small mobile | 360 | yes |
| standard mobile | 375, 390 | yes |
| large mobile | 428 | optional |
| tablet | 768 | yes |
| laptop | 1024, 1280 | yes |
| desktop | 1440 | yes |

- **Required smoke matrix:** `360* / 390 / 768 / 1440` (`*` optional if a standard-mobile width is covered). Runs on every build and every reopened build.
- **Extended regression matrix:** `360 / 375 / 390 / 428 / 768 / 1024 / 1280 / 1440`. Runs before Gauntlet entry, before production pre-flight, and on any change to layout, tokens, IA, or motion.
- **Project overrides:** a manifest may narrow or extend the matrix with a recorded reason; it may never drop a required class.

Do not run every assertion at every width when it multiplies cost without signal: responsive invariants and screenshots run across the class set; console / network / measurement / form assertions run on the smoke matrix unless a route is viewport-conditional.

---

## 7. Responsive invariants

Detected where technically possible: horizontal overflow · content clipped outside the viewport · overlapping fixed/sticky navigation · unusable menus · off-screen controls · zero-sized interactive targets · broken grid collapse · hidden primary CTA · viewport-dependent JavaScript errors · modal/dialog overflow · unexpected `body` width · layout instability after hydration/load.

> `overflow-x: hidden` is **not** the universal solution to overflow. The test detects the underlying overflow (`documentElement.scrollWidth > clientWidth`, `body` width beyond viewport) — it must not be satisfied by clipping the symptom.

---

## 8. Navigation QA

Verified where applicable: internal links resolve · current route loads · no placeholder `#` links unless explicitly intentional · mobile navigation opens · mobile navigation closes · click-outside where specified · Escape where specified · body-scroll policy · route-change closing behaviour · browser back/forward · hash navigation where applicable · external-link `target`/`rel` policy · custom 404.

Navigation rules are **owned by** `PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md`. Browser QA executes and checks the browser-observable portion; it defines no competing navigation rules.

---

## 9. Console & page-error capture

Captured: uncaught JavaScript errors · unhandled promise rejections · console errors · framework hydration errors · failed runtime initialisation · critical warnings explicitly promoted to blockers.

Every message is classified:

| Class | Meaning |
| :--- | :--- |
| `KNOWN_NON_BLOCKING_WARNING` | Documented, justified, expiry noted. |
| `TEST_ENVIRONMENT_NOISE` | Present only under automation / dev build; absent from production build (verified). |
| `APPLICATION_DEFECT` | Blocks `[BROWSER_QA_PASS]`. |
| `THIRD_PARTY_DEFECT` | Investigated, owner named; not silently ignored. |

**Console output is never blanket-ignored.** Every ignored pattern is an entry in the manifest `console_ignore` list with a `justification` and an `owner`; an empty list is the correct default.

---

## 10. Network QA

Captured and classified: 4xx · 5xx · aborted critical assets · failed fonts · failed scripts · missing images · broken API calls · redirect loops · mixed-content failures · CORS failures where observable.

A deliberately blocked/optional third-party request fails a check only if it is **not** in the manifest `allowed_third_party_failures` allow-list. Every allow-list entry requires a `justification` and must assert `site_still_functional`. Blocking each declared third-party origin and confirming navigation, content, and forms still work is part of the regression matrix.

---

## 11. Image / asset QA

Verified where applicable: image response success · non-zero rendered dimensions · missing/broken assets · responsive image behaviour · lazy-loaded content eventually resolves · critical hero asset loads · mobile fallback asset loads · reduced-motion fallback asset loads · no accidental placeholder images.

Pixel-quality and art-direction judgement stay with Asset Director / the Gauntlet — Browser QA only checks that the right asset loaded and rendered.

---

## 11.1 Content Operations & CMS runtime QA (V2.13)

Browser QA consumes the validated Capability #8 content model and
`content_ops{}` state; it does not create a second content runner or CMS
authority. Where the project exposes these surfaces, the existing harness
verifies:

- required semantic fields render and repeated entities resolve through the
  model rather than duplicated presentation markup;
- draft, review, scheduled, and archived records are not publicly visible or
  listed, while published records resolve on the intended route;
- preview uses the real route composition and design system, not raw JSON;
- editor-facing controls cannot change analytics identifiers, structured-data
  schema, security headers, design tokens, or owner lock state;
- rich-text script/style/event-handler/unsafe-embed inputs are rejected;
- published or archived slug changes preserve their declared 301 redirects;
- production media references resolve to Asset Director identity and V2.12
  provenance, and research/inspiration references remain `REFERENCE_ONLY`;
- agent-generated content cannot skip the human-review boundary into
  `PUBLISHED`.

Failures are traced back to `CONTENT-OPERATIONS-CMS-PROTOCOL.md` and recorded
as `FAIL`, `BLOCKED`, or `NOT_APPLICABLE` according to the manifest. A local
browser run does not set production verification, and no browser test may
write under `projects/`.

---

## 11.2 Localization & Internationalization runtime QA (V2.14)

Browser QA consumes the provider-neutral Capability #9 localization plan and
`localization{}` contract through this same runner. It does not create a second
localization runner, translation state machine, CMS, or production authority.
Where a project requires localization, the existing assertion catalogue uses
the `LOCALIZATION_PLAN` requirement source to verify the runtime-observable
subset:

- locale routes resolve and map to equivalent content routes;
- the rendered `html lang` and direction match the locale contract;
- a locale switcher is present where required, has text labels rather than
  flag-only labels, identifies the current locale, and is keyboard operable;
- untranslated system strings are absent and explicit fallback behaviour is
  observable;
- localized `hreflang` entries are present, covered, reciprocal, and include
  the current locale; localized pages use a self-referencing canonical;
- localized title, description, Open Graph, alt text, and form labels/errors
  are present where the plan requires them;
- pseudo-localized text meets the declared expansion target without overflow;
- RTL direction, focus, navigation, directional-icon policy, forms, and
  overflow remain functional where an RTL locale is required.

The `simulation` engine accepts deterministic fixture observations for these
checks. The `playwright` adapter collects DOM, metadata, route, fallback,
expansion, and RTL facts when the plan enables localization. Simulation is a
dry run and never sets implementation or production verification. No browser
test may write under `projects/`.

---

## 11.3 Conditional Application, Commerce & Authentication runtime QA (V2.15)

Browser QA consumes the provider-neutral Capability #10 application plan
through this same runner. It does not create a second application runner,
authentication harness, payment harness, or production authority. The group
is `NOT_APPLICABLE` when `application.required` is false, and is `BLOCKED`
when a required application observation is unavailable.

Where the plan activates application modules, the assertion catalogue checks
only explicit browser-observable evidence and leaves server authority to the
application validator and the real integration environment:

- protected routes do not become usable through client-controlled roles,
  object identifiers, or hidden UI alone;
- checkout and purchase UI do not claim payment, fulfillment, entitlement, or
  conversion before authoritative confirmation;
- payment, order, subscription, booking, webhook, upload, UGC, email, and
  integration observations satisfy the active module contract;
- private routes and private resources are not publicly indexable or exposed;
- canonical measurement events carry locale context without duplicate
  localized purchase events;
- provider unavailability, live payment attempts, real-user creation, and
  missing evidence remain `BLOCKED` or `FAIL`, never a pass.

The `simulation` engine accepts explicit application facts for deterministic
negative controls. The `playwright` adapter reads only declared
`data-qa-application` observations and does not infer security, payment, or
authorization correctness from visual state. Production application
verification remains owned by Launch Operations, and long-term operational
transfer remains owned by V2.5 Handoff.

---

## 12. Test isolation & the Frozen Project Integrity Guard

**Hard invariant.** Browser and QA tests:

- use temporary directories for mutable fixtures and disposable copies;
- use temporary browser profiles and isolated ports;
- never modify canonical project artifacts or frozen certification projects;
- never touch real customer data or production;
- clean up every child process and test server;
- do not depend on previous test order.

A passing test that mutates a frozen project is a **failed QA architecture**.

`browser-qa/guards/frozen_integrity_guard.py` snapshots and hash-checks protected paths (default: `projects/`) before and after every run. On any change:

```
FROZEN_FIXTURE_MUTATION = FAIL
```

Restoring the file afterwards does **not** convert the run into a PASS — the guard writes an append-only violation ledger (`browser-qa/evidence/frozen-integrity-violations.log`) the moment drift is observed, and also reports the git working-tree change. Every release of this subsystem negative-controls the guard (deliberate mutation → guard must FAIL → restore → the recorded violation survives).

---

## 13. Measurement event QA

Consumes canonical `measurement-plan.md`, `analytics-event-manifest.json`, and `measurement{}`. Verified where technically possible: required event fires · correct event name · fires once · correct trigger · required parameters present · prohibited PII absent · a successful-conversion event requires actual success · internal links not mislabelled as affiliate outbound clicks · UTM preservation · route/page-view tracking where required · duplicate instrumentation absent.

**Browser QA invents no events.** If the specification is wrong, HALT and escalate to the measurement owner — never patch instrumentation to make a check green.

---

## 14. Security / privacy browser QA

Consumes canonical `security_privacy{}`. Verified where browser-observable: HTTPS in a production context · mixed content · security headers · secure cookie attributes where observable · consent-UI behaviour · analytics blocked before required consent · analytics active only after appropriate consent · reject path functions · no deceptive consent interaction · no obvious secret values in DOM / client bundle · third-party script inventory matches observed runtime · privacy/disclosure routes resolve · affiliate disclosure present where specified.

> Browser QA does **not** claim legal compliance. `security_privacy.compliance_certified` stays permanently `false`. Findings flow to the security/privacy owner; Browser QA never rewrites the review.

---

## 15. Reduced motion

Every run exercises `prefers-reduced-motion: reduce`. Verified: motion-heavy behaviours disable/reduce as specified · essential content stays visible · no content permanently hidden awaiting animation · fallback visuals exist · navigation stays functional · scroll-driven sequences do not block content · Rive / GSAP / Three.js / transition systems honour the canonical motion policy. Evidence (screenshots) captured.

---

## 16. Keyboard smoke QA — and the V2.9 accessibility assertion group

Browser QA's baseline keyboard smoke: primary navigation reachable · visible focus exists · mobile/menu controls operable · dialogs Escape correctly where specified · form controls operable · no obvious keyboard trap · primary CTA reachable.

**V2.9 (`ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md`)** formalises this and adds an **accessibility assertion group** to this same harness, gated on the plan carrying an `accessibility` block. Source: `ACCESSIBILITY_REVIEW`. It covers the machine-verifiable subset of WCAG 2.2 AA — automated-engine violations (axe-core or a replaceable engine), missing accessible names, computed contrast (consuming Impeccable's math), focus visibility, focus-not-obscured (feasible cases only — the rest `MANUAL_REQUIRED`), keyboard traps, landmarks and heading order, page `lang` and `<title>`, colour-only state heuristics, reflow at the target width, text spacing, target size (project minimum + the WCAG 24px floor), dialog mechanics, and form label/error association. Screen-reader review and deep manual criteria stay **explicitly manual** and never auto-PASS. An unavailable engine is `BLOCKED_ACCESSIBILITY_ENGINE_UNAVAILABLE`. No second runner and no second post-build state machine — one harness, one evidence system, one frozen-project guard.

**V2.14 (`LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md`)** adds the
`LOCALIZATION_PLAN` assertion group to this same harness. It consumes the
canonical localization plan and checks locale routes, equivalent routes,
`html lang`, text-labelled switchers, fallback, `hreflang`, localized
canonicals and metadata, localized forms, pseudo-localized expansion, and RTL
runtime behaviour where applicable. It does not create a second runner or set
`localization.complete`; simulation remains a dry run and production
verification remains owned by Launch Operations.

---

## 17. Visual screenshot evidence

Deterministic screenshots for selected critical surfaces: full page · hero · navigation open · form states · modal states · mobile · desktop · reduced motion · error/success states.

**Deterministic file names**, e.g. `home__desktop_1440.png`, `home__mobile_390.png`, `nav__mobile_390__open.png`, `contact__desktop__validation-error.png`, `home__desktop__reduced-motion.png`.

**Retention:** screenshots and traces live in the project evidence directory and are git-ignored by default. A project commits only the *current baseline set* it explicitly nominates in the manifest, plus the machine-readable evidence manifest (§18). Unlimited screenshot commits are prohibited.

---

## 18. Visual regression

```
BASELINE   the locked reference render for (route, viewport, [reduced-motion])
CURRENT    this run's render
DIFF       the delta
THRESHOLD  the tolerated delta (default: exact; documented per project)
VERDICT    MATCH | DIFF_DETECTED | BASELINE_MISSING
```

Rules:

- **Baseline creation is explicit** — a missing baseline is `BLOCKED` (`visual_regression_status = BASELINE_MISSING`), never an auto-accept.
- Agents may **not** silently overwrite a baseline because a diff occurred. Baseline updates require the authorisation defined by project governance (an owner change note in the manifest).
- Dynamic regions may use **explicit, narrowly-scoped masks**. Excessive masking is prohibited — prefer deterministic fixtures/test mode (§19).
- Threshold changes require a recorded justification.
- **A visual diff is evidence of change, not automatically evidence of defect.** Regression QA answers "did it change unexpectedly?"; the Gauntlet answers "is the change good?"

---

## 19. Dynamic content stability

Deterministic handling for timestamps · random IDs · rotating testimonials · animations · live counters · async content · ads · third-party widgets. Prefer deterministic fixtures / a test mode that pins the clock and rotation. Do **not** solve instability by masking the entire page.

---

## 20. Waiting / synchronisation policy

Arbitrary long sleeps as the primary synchronisation technique are prohibited. Prefer DOM state · network idle where appropriate · explicit selector readiness · animation completion · framework-specific stable conditions. Fixed delays are permitted only with a recorded justification. This is a flake-reduction requirement.

---

## 21. Flake policy

```
PASS · FAIL · FLAKY · BLOCKED · NOT_APPLICABLE
```

- A test that fails then passes on retry is **`FLAKY`**, not `PASS`. Flake evidence is recorded in `browser_qa.flaky_tests`.
- Retries are **bounded** (default budget: 2). Unlimited retries to bury a flake are prohibited.
- Repeated flaky behaviour on the same check across runs is a **defect** and blocks the gate until resolved or explicitly owner-waived.
- A `FLAKY` verdict never produces a green runner exit.

---

## 22. Local vs. production verification

```
LOCAL_IMPLEMENTATION_VERIFIED   real browser, local/staging build, all checks PASS
PRODUCTION_VERIFIED             the same, executed against the real production URL
```

A local browser test does **not** prove production DNS, CDN behaviour, production headers, real TLS, production third-party configuration, or deployed environment variables. `browser_qa.implementation_verified` and `browser_qa.production_verified` are **permanently distinct**. A localhost run never sets `production_verified`. The non-browser `simulation` engine sets **neither**.

**Launch Operations (V2.10) reuses this harness — no second runner.** Phase 12.25 (`LAUNCH-OPERATIONS-PROTOCOL.md` §15, §40) runs `browser-qa/runner.py` with the manifest's `"environment": "production"` (or `https://` routes) as its **Production Browser QA** step, after an owner has deployed. The launch-mode manifest restricts `interactions` to non-destructive health-checks (no real form submission without explicit production-test authorization). The result feeds `launch_ops.production_browser_verified` alongside `browser_qa.production_verified`; the gating rules above are unchanged.

---

## 23. Regression manifest

`templates/browser-qa-plan.md` (human) and `templates/browser-qa-manifest.json` (machine) track: pages/routes · critical components · required viewports · interactions · screenshot surfaces · measurement assertions · security/privacy assertions · reduced-motion assertions · expected network behaviour · allowed third-party exceptions · baseline version · evidence path.

---

## 24. Canonical state

`site-profile.json` → `browser_qa{}`:

```json
"browser_qa": {
  "complete": false,
  "engine": null,
  "plan_ready": false,
  "smoke_passed": false,
  "responsive_passed": false,
  "console_passed": false,
  "network_passed": false,
  "form_passed": null,
  "measurement_passed": null,
  "security_privacy_passed": null,
  "reduced_motion_passed": null,
  "keyboard_smoke_passed": null,
  "visual_regression_status": "NOT_RUN",
  "frozen_fixture_integrity": "UNVERIFIED",
  "flaky_tests": [],
  "blocked_reason": null,
  "implementation_verified": false,
  "production_verified": false,
  "exception": { "applied": false, "reason": null }
}
```

`browser_qa.complete` is the **single** authoritative readiness flag for `[BROWSER_QA_PASS]`. No second, independently-writable completion flag may be created. `null` fields mean "not applicable to this project" (e.g. no forms). `browser_qa.complete = true` never means production was verified — see §22 and `SKILL.md` §5.15.

---

## 25. Evidence manifest

Every run writes `<evidence>/<run_id>.evidence.json` and `<run_id>.summary.md` containing where applicable: run ID · timestamp · git SHA · environment · browser/version · route · viewport · test · result · screenshot · console findings · network findings · visual diff · trace · failure reason. Machine-readable JSON plus a human summary. Evidence is reproducible.

---

## 26. Traceability

Every assertion traces to exactly one requirement source:

```
LOCKED_SPEC · PRODUCTION_CHECKLIST · MEASUREMENT_PLAN · SECURITY_PRIVACY_REVIEW · ACCESSIBILITY_REVIEW · MOTION_SPEC · PAGE_EXPERIENCE_SPEC · BROWSER_QA_PLAN
```

Assertions with no requirement source are prohibited. A new detection method tag, `BROWSER_EXECUTED`, joins Impeccable's `DETERMINISTIC / HEURISTIC / LLM_CRITIQUE / VISUAL_COMPARISON` (`IMPECCABLE-ENGINE-PROTOCOL.md` §2) for machine-run browser checks; visual-regression findings are tagged `VISUAL_COMPARISON`.

---

## 27. Failure governance

On failure the run records: exact route · exact viewport · exact interaction · exact assertion · relevant evidence · likely owning specification · whether repair is within locks.

Browser QA may authorise **implementation repairs** only where they do not alter locked design intent. If a fix requires changing locked IA, copy, design system, or motion direction, **HALT** and produce an owner change request — never a silent edit.

---

## 28. Rule ownership vs. Impeccable

| Concern | Owner |
| :--- | :--- |
| `transition: all` / raw hex / unmapped token **in a stylesheet** (static) | Impeccable (`DETERMINISTIC`) |
| Actual horizontal overflow at 390px **in a live viewport** | Browser QA (`BROWSER_EXECUTED`) |
| A banned bounce easing **string** in CSS | Impeccable |
| A scroll sequence that **actually** hides content under reduced motion | Browser QA |
| Console error **at runtime** | Browser QA |
| AI-slop structural pattern in markup | Impeccable |

One owner per rule. Browser QA reuses Impeccable's static findings; it does not re-implement static detectors.

---

## 29. Relationship to the Website Gauntlet

```
DETERMINISTIC BROWSER QA  →  PASS  →  HEURISTIC / QUALITATIVE GAUNTLET
```

The Gauntlet does not spend cycles on a build with broken navigation, JavaScript exceptions, missing assets, failed forms, or obvious responsive overflow — those are deterministic and belong here first. `WEBSITE-GAUNTLET-PROTOCOL.md` adds a **Deterministic Browser QA Entry Precondition**: Gauntlet STEP 1 does not begin until `browser_qa.complete` is `true` (or a recorded `blocked` / `exception`). **No new Gauntlet critic and no second Gauntlet state machine are created** — Browser QA is an upstream phase, not a Gauntlet lens.

---

## 30. Cross-browser policy

- **Primary smoke:** Chromium only is acceptable.
- **Release-critical interaction subset** (navigation, forms, consent UI, route transitions, reduced motion) before production pre-flight: Chromium + Firefox + WebKit.
- **Project override:** an explicit browser set with a recorded reason.

Do not multiply runtime cost without value. Do not claim `cross-browser verified` after testing only Chromium.

---

## 31. Performance boundary

Browser QA collects performance evidence for thresholds Website Director **already** defines (`PRODUCTION-CHECKLIST.md` §4): LCP, CLS, INP where measurable, and animation frame/runtime problems where the engine supports it. It does not implement a separate performance-intelligence subsystem. Synthetic (lab) measurements are labelled `SYNTHETIC`; they are never presented as real-user field data.

---

## 32. Exceptions / BLOCKED mode

Legitimate non-PASS statuses: browser engine unavailable · site cannot start · auth fixture unavailable · third-party sandbox unavailable · production URL unavailable · explicit non-interactive artifact. Unavailable testing is **never** converted to `PASS` — it is `BLOCKED` with a specific `blocked_reason`, or an owner-recorded `exception` (private prototypes, offline demos, disposable experiments only). A public commercial build never receives a blanket browser-QA exception.

---

## 33. Backward compatibility

Historical projects without `browser_qa{}` remain valid and are not retrofitted. Frozen certification pilots are never reopened by this tooling. Project-specific historical QA scripts remain historical evidence. New or materially reopened builds use this protocol.

---

## 34. Implementation contract obligations (builders)

`IMPLEMENTATION-CONTRACT.md` §2.7 binds builders to: expose testable, stable selectors where needed; keep test-only semantics out of user-facing UI; preserve testability; never disable QA to ship; never delete failing tests; never silently update a visual baseline; never add broad ignores; never mask a broken region; fix the implementation or escalate the specification conflict.

---

## 35. Validation scenarios (negative controls)

`tests/test_v2_8_browser_regression_qa.py` and `examples/BROWSER-REGRESSION-QA-INTEGRATION-VALIDATION.md` prove each guard actually fails:

| # | Scenario | Expected |
| :-- | :--- | :--- |
| A | Element wider than the viewport | responsive overflow → **FAIL** |
| B | Injected uncaught JS error | console → **FAIL** |
| C | Broken hero image | asset + network → **FAIL** |
| D | Mobile navigation open/close works | nav → **PASS** |
| E | Server-rejected form done right | visible failure, no success state, no success conversion → **PASS** |
| E′ | Server-rejected form shows success + fires conversion | → **FAIL** |
| F | Motion-heavy content meaningful under reduced motion | → **PASS** |
| F′ | Content trapped behind animation under reduced motion | → **FAIL** |
| G | Intentional 20px layout shift vs locked baseline | **DIFF detected**, baseline not overwritten |
| H | Dynamic timestamp with deterministic fixture handling | no false regression → **PASS** |
| I | Deliberate mutation of a protected frozen fixture | integrity guard **FAIL**; ledger survives restore |
| J | First run fails, retry passes | status **FLAKY**, not PASS; non-green exit |
| K | Local verification | `production_verified` stays **false** |
| L | Email address in an analytics payload | measurement/privacy → **FAIL** |

---

## 36. Test the tests

This subsystem contains negative controls proving its major guards fail on: frozen-fixture mutation, console error, network failure, visual diff, PII event, and obsolete/invalid state schema. A guard that has never demonstrated it can fail is insufficient evidence.

---

## 37. No external side effects

Never browse or test arbitrary external websites, submit real forms, send email, transmit customer data, create real analytics events, mutate production, deploy, change DNS, modify third-party accounts, or run destructive security tests. Framework validation uses local synthetic fixtures only.
