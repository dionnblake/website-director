# Reproduction Results

**Evidence tiers are kept strictly separate.** A unit-test PASS is never reported as browser
verification. Nothing here was manufactured; where execution failed or was unreliable, it says so.

**Isolation:** all reproductions ran from a disposable export
(`git archive` → `%TEMP%\wda-fb`) and a scratchpad copy of `framework_validation/` +
`browser-qa/`. The browser review served a **copy** of the shipped site from `%TEMP%\wda-site`.
No repository file, protected project, or approval record was written.

---

## Tier 1 — UNIT TESTS (registered suites)

Run from the audit worktree at `416f95d` unless noted.

| Suite | Command | Result |
|---|---|---|
| Owner intent enforcement | `python tests/test_owner_intent_enforcement.py` | **OK — 18 tests** |
| Cinematic inspiration | `python tests/test_cinematic_inspiration.py` | **OK — 20 tests** |
| V2.8 Browser & Regression QA | `python tests/test_v2_8_browser_regression_qa.py` | **89/89 ASSERTIONS PASSED**; `FROZEN_FIXTURE_INTEGRITY = PASS (465 files unchanged)` |
| Design-first production flow | `python tests/test_design_first_production_flow.py` (in `%TEMP%\wda-fb`, feature branch export) | **OK — 24 tests** |

The design-first suite **is registered** — `schemas/test-suites.json:292`, id
`design_first_production_flow`. It is not unregistered and is not reported as such.

> **Environment note, reported for honesty:** the first three attempts to run the design-first suite
> failed with `FileNotFoundError` on `projects/alpha-starts-now/implementation-contract.md`. Root cause
> was the Windows `MAX_PATH` limit — the scratchpad export path reached **exactly 260 characters**.
> Re-exporting to a shorter path made all 24 tests pass. **This was an environment artifact, not a
> defect in the suite.**

**These results prove metadata shapes and negative controls. They prove nothing about visual quality,
motion craft, or owner acceptance.**

---

## Tier 2 — INTEGRATION REPRODUCTIONS

### R1 — Surface-name → capture-mode mapping
`repro/r1_surface_capture.py` · exercises `browser-qa/runner.py::_matrix()`

Input: a minimal plan with one route and `visual_evidence.required = true`, varying only the
surface list.

| Case | Input | Generated capture |
|---|---|---|
| **A** canonical cinematic names (strings) | `DESKTOP_FULL_PAGE` | `FULL_PAGE` |
| | `MOBILE_FULL_PAGE` | `FULL_PAGE` |
| | `DESKTOP_HERO`, `DESKTOP_MID_PAGE`, `DESKTOP_PRIMARY_CONVERSION`, `MOBILE_HERO`, `MOBILE_NAV_OPEN`, `PRIMARY_INTERACTIVE_STATE`, `REDUCED_MOTION_STATE` | `VIEWPORT` *(correct by design)* |
| **B** design-first homepage names (strings) | `DESKTOP_FULL_HOMEPAGE` | **`VIEWPORT`** |
| | `MOBILE_FULL_HOMEPAGE` | **`VIEWPORT`** |
| **C** same names as explicit objects with `capture: "FULL_PAGE"` | both | `FULL_PAGE` |

**Expected:** a surface whose identity is "full homepage" produces a full-page capture.
**Actual:** case B produces viewport-only captures — **2 of 2**.
**Verdict: REPRODUCED.**

Boundary: case C proves an escape hatch exists, but `design_first_flow.HOMEPAGE_REVIEW_SURFACES` is a
tuple of **bare strings**, so nothing in the design-first flow emits the object form. A pre-check
confirmed **no alias or translation** for `FULL_HOMEPAGE` exists in `runner.py`,
`cinematic_inspiration.py` or `catalog.py` on either branch.

---

### R2 — Silent skip of owner-required motion and brand
`repro/r2_silent_skip.py` · exercises `catalog.check_motion` / `catalog.check_brand_tokens`
· input = **the real shipped ASN manifest**

Blocks present in `qa/browser-qa-manifest.json`:

| Block | Present |
|---|---|
| `owner_intent` | **ABSENT** |
| `motion` | **ABSENT** |
| `visual_evidence` | **ABSENT** |
| `runtime_observations` / `observations` | **ABSENT** |
| `brand_implementation` | **ABSENT** |

| Case | `check_motion` | `check_brand_tokens` |
|---|---|---|
| **1** Real manifest as shipped | **`None`** (silent skip) | **`None`** (silent skip) |
| **2** `owner_intent` added demanding `MOTION_LEVEL_3`, `motion` block still omitted | **`None`** — owner requirement **ignored** | runs |
| **3** Control: `motion: {required: true}` | 1 finding — `motion.observation-coverage` **BLOCKED** | — |

**Expected integrated outcome:** required verification, or a truthful block.
**Actual:** silent skip. Case 2 is the defect — an explicit owner `MOTION_LEVEL_3` requirement produces
**no check and no block** because the plan omitted its own `motion` block. Case 3 proves the machinery
works correctly once armed.
**Verdict: REPRODUCED, and PROJECT_CONFIRMED against the shipped manifest.**

> **Scope correction — R2 ran against `main`'s `catalog.py`, not the build's.**
> A later integrity check (below) found the ASN worktree runs a **different** `catalog.py`
> (31,838 bytes, `44a23319…`) than the one audited on `main` (65,580 bytes, `b3e19340…`).
> The build's copy has **no `check_motion`, no `check_brand_tokens`, and no
> `check_observation_coverage` at all.** R2 therefore correctly demonstrates the live defect on
> current `main`, but **understates** the project reality: for this build the checks were not merely
> unarmed, they were absent. See the harness-identity table below.

---

### R3 — Real owner contract vs real built palette
`repro/r3_real_contract.py` · inputs = `templates/alpha-starts-now-owner-intent.json` (real) and the
rendered roles of the real build

```
validate_brand_tokens  -> status: FAIL
  UNAPPROVED_DOMINANT_BRAND_HUE: paper cream (role=page background)   blocking: false
  UNAPPROVED_DOMINANT_BRAND_HUE: ink        (role=text)               blocking: false
  approved_families: ["BLUE", "YELLOW"]

resolve_motion_requirement -> status: PASS
  owner_required_level: MOTION_LEVEL_3
  execution_level:      MOTION_LEVEL_3
  downgrade_blocked:    false
  approved_downgrade:   false
```

**Verdict: REPRODUCED** — the contract resolves to `MOTION_LEVEL_3` and the brand validator produces a
non-empty result, yet neither is reachable from the shipped manifest.

**Boundary — do not over-read the brand FAIL.** Area-weighted measurement of the actually-rendered
homepage (below) shows navy/ink surfaces slightly **dominant** over the cream family, and cream
plausibly qualifies as a "restrained light neutral", which the contract permits. The reproduced fact
is that **the check never ran**; a brand breach is **NOT_VERIFIED**.

---

### R4 — Declarations accepted where evidence is implied
`repro/r4_gate_evidence.py` · feature-branch `design_first_flow` + `cinematic_inspiration`

**C1 — production gate with garbage design evidence behind true flags**

Input: all seven completion flags `True`; a schema-valid `HOMEPAGE_APPROVAL` whose
`RENDERED_SURFACES` are **bare strings with zero screenshot receipts**.

```
validate_production_gate                    -> PASS   can_start_production: True

  same evidence, if any validator had been asked:
  validate_homepage_design(garbage)         -> FAIL
      FULL_HOMEPAGE_VISUAL_DESIGN_REQUIRED
      FULL_HOMEPAGE_SECTIONS_INCOMPLETE
      FULL_HOMEPAGE_VISUAL_SIGNALS_INCOMPLETE
  validate_design_system_derivation(garbage)-> BLOCKED
      DESIGN_SYSTEM_SOURCE_NOT_APPROVED_HOMEPAGE
      DESIGN_SYSTEM_DERIVATION_INCOMPLETE
```

**Verdict: REPRODUCED.** *Partial mitigation noted:* the gate **does** call
`validate_homepage_approval()` (`design_first_flow.py:551`), so approval shape is genuinely checked.
It does not call the homepage-design or derivation validators.

**C2 — fabricated screenshot receipts**

Input: 9 receipts, `actual_rendered: true`, `engine_identity: "REAL_BROWSER"`, paths under
`/nonexistent/`, digests = 64 zeros.

```
validate_rendered_visual_evidence -> PASS    issues: NONE
any file actually on disk         -> False
```

**Verdict: REPRODUCED.** `_actual_screenshot()` (`cinematic_inspiration.py:340-347`) checks metadata
shape only.

**Mitigation, stated fairly:** runner-produced evidence is genuine — `runner.py:414` computes
`hashlib.sha256(bytes(shot)).hexdigest()` over real image bytes. The gap is that the validator cannot
tell runner-produced from hand-authored receipts.

**Fixture hygiene:** every owner/approval record used above is synthetic, lives only in the scratchpad,
and was never written into any project or approval history.

---

## Tier 3 — REAL BROWSER REVIEW

**Setup:** shipped `site/` copied to `%TEMP%\wda-site`, served at `127.0.0.1:8731`
(`python -m http.server`). Chromium via the in-app browser pane, viewport 1440×900.
**Server stopped and port 8731 released at completion** (verified `HTTP 000`).

### Measured page facts

| Metric | Value |
|---|---|
| `document.scrollHeight` @ 1440 | **9,763 px** (viewport capture = ~9% of page) |
| Sections | 8 (`hero`, `thesis`, `rituals`, `path`, `values`, `vitality`, `notes`, `join`) |
| `body` background | `rgb(244,239,230)` — cream |
| `h1` | *"THE 5 MORNING RITUALS // ALPHA STARTS NOW."* @ **172.8 px**, Bebas Neue |

### Motion — runtime measurement

| Probe | Result |
|---|---|
| CSS `@keyframes` rules (`CSSRule.type === 7`) | **0** |
| Distinct runtime families | **3** — `TRANS:all`, `TRANS:opacity`, `TRANS:transform` |
| `window.gsap` / `window.ScrollTrigger` | `false` / `false` |
| `.reveal` nodes | 32 (one pattern) |
| `scrollTo(bottom)` delta | **6,156 px** |

**The F4 consequence, demonstrated:** this page yields `scroll_delta = 6156` while containing zero
animations. Under `catalog.py:530-535` that alone marks an observation "meaningful", so
`motion.runtime-state-change` would have **PASSED** a static page.

### Typography — verified, not declared

| Probe | Result |
|---|---|
| `document.fonts.check('100px "Bebas Neue"')` | **true** |
| `…'16px "Plus Jakarta Sans"'` / `…'16px "Space Mono"'` | **true** / **true** |
| Canvas width probe, same string | Bebas Neue **587 px** vs Impact fallback **769 px** — genuinely distinct |

Real fonts, really loading, really rendering.

### Palette — area-weighted

| Surface | Painted area |
|---|---|
| `rgb(3,9,20)` | 5.75 M px² |
| `rgb(244,239,230)` | 3.49 M px² |
| `rgb(251,248,242)` | 2.72 M px² |
| `rgb(11,24,48)` | 2.60 M px² |
| `rgb(227,218,203)` | 1.03 M px² |
| `rgb(7,17,36)` | 0.45 M px² |

Navy/ink ≈ **8.79 M** vs cream family ≈ **7.24 M**. Navy is dominant.

### Capture-dimension check on the project's own evidence

| File | Dimensions | Kind |
|---|---|---|
| `evidence/screenshots/final/homepage-desktop.png` | **1440 × 9781** | FULL_PAGE |
| `evidence/screenshots/final/homepage-mobile.png` | **390 × 14311** | FULL_PAGE |
| `evidence/screenshots/homepage-1440.png` | 1440 × 900 | VIEWPORT |
| `evidence/screenshots/final/homepage-belowfold-1-desktop.png` | 1440 × 900 | VIEWPORT (intentional) |

The project's full-homepage captures are **genuinely full-page**. F5 did not affect it.

### Asset serving

All served `HTTP 200` from the isolated copy: `ritual-1..5.jpg` (808 KB / 672 KB / 725 KB / 787 KB /
719 KB), `asn-logo.jpg`, `hero-brutalist-ascent.jpg`.

---

## Harness identity — the build did not run the code this audit read

Per the instruction to compare loaded file hashes rather than trust version claims, the **working
file** in the ASN worktree was hashed instead of assumed.

| Copy | Bytes | sha256 (first 16) |
|---|---|---|
| ASN worktree `browser-qa/assertions/catalog.py` — **what the build ran** | **31,838** | `44a23319f119198f` |
| `origin/main` — what this audit read | **65,580** | `b3e193405c3430bb` |
| committed `feat/v2-10-launch-post-launch-operations` blob | — | `32ee945fe82c2e64` |

Provenance: the working file descends from the v2-10 blob and differs by only **3 lines**
(`git diff --stat HEAD`), plus a 29-line change to `playwright_engine.py`. The diff contains **no
added or removed `def check_*` lines** — nothing was stripped; the checks were never on that branch.

Check functions present in each copy:

| Function | ASN build harness | `main` |
|---|:--:|:--:|
| `check_reduced_motion` | present | present |
| `check_motion` | **ABSENT** | present |
| `check_brand_tokens` | **ABSENT** | present |
| `check_observation_coverage` | **ABSENT** | present |
| `check_application`, `check_localization` | **ABSENT** | present |

**Consequence:** the `{'PASS': 3332}` result was produced by a harness with no runtime-motion check,
no brand check, and **no fail-closed observation-coverage guard**. A correctly authored manifest
would not have helped.

**Not caused by this audit:** file mtimes are `2026-09-06 00:53:59`, from the original build session
roughly a day before this audit ran. This audit performed no writes to that worktree — only reads and
outward copies.

---

## Withdrawn observations — corrected, not reported as findings

Recorded because an audit that hides its own false starts is not trustworthy.

| Initial observation | Verification | Outcome |
|---|---|---|
| `8/9 images loaded` — suspected broken `ritual-3.jpg` | File present (725,010 bytes); serves `HTTP 200`; `loading="lazy"` and below fold at measurement time | **WITHDRAWN** — measurement artifact |
| Blank cream viewport at `y=4200` — suspected empty section | DOM query found **13 real elements** in that band (ritual rows, plates, `PROGRESS IS A ROUTE.` heading) | **WITHDRAWN** — paint-timing artifact of the headless pane |
| "Cream is the dominant surface" (inferred from CSS variable counts) | Area-weighted runtime measurement shows navy/ink dominant | **CORRECTED** — see F7 |

---

## NOT_RUN / BLOCKED

| Item | Status | Reason |
|---|---|---|
| Video transcript comparison | **BLOCKED** | `Pasted text(20260907-020523).txt` not present in attachments or authorized workspace. Supplied synopsis used instead; no claim made about the video or its site. |
| Static screenshot capture of lower sections | **PARTIAL / UNRELIABLE** | Repeated 5 s paint timeouts in the headless pane. DOM + computed-style measurement used instead. **No screenshot is offered as approval evidence.** |
| Motion recordings / verified sequence samples | **NOT_RUN** | Moot — the build contains no sequences to record (0 keyframes, no GSAP). |
| Re-running the project's own browser-qa harness | **NOT_RUN** | Would require the enforcement modules the build branch lacks (F1); its existing evidence was read instead. |
| External reference inspection | **NOT_RUN** | No new inspiration search, gallery scraping, or reference cloning was performed, per scope. |
