# V2.9 Accessibility Intelligence & WCAG 2.2 AA — Integration Validation Suite

> Validates that the Phase 6.9 / Phase 10.5 accessibility subsystem
> (`ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md`) is wired into Website Director and
> that **every accessibility safeguard actually fails** on a broken input.
> Automated form: `tests/test_v2_9_accessibility.py` (exit 0 = pass), run with the
> deterministic `simulation` engine and only the Python standard library.

```bash
python tests/test_v2_9_accessibility.py
```

---

## Part A — Repository wiring invariants

| # | Assertion |
| :-- | :--- |
| A1 | `ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md` exists and is the **only** canonical accessibility protocol at repo root. |
| A2 | `templates/accessibility-review.md` (29 sections) and `templates/accessibility-test-manifest.json` exist. |
| A3 | Protocol declares `[ACCESSIBILITY_READY]`, `accessibility.complete`, `WCAG 2.2 Level AA`, the single-completion-flag invariant, "not a sixth owner" lock, `BLOCKED_SCREEN_READER_ENVIRONMENT`, `BLOCKED_ACCESSIBILITY_ENGINE_UNAVAILABLE`, the `AUTO_VERIFIED / MANUAL_VERIFIED / KNOWN_GAP` classification, and reuse of the V2.8 `FrozenIntegrityGuard`. |
| A4 | `templates/site-profile.json` (schema ≥ 2.9.0) contains `accessibility{}` with `complete:false`, `target:"WCAG_2_2_AA"`, `mode:"not_evaluated"`, `automated_verified/manual_verified/screen_reader_verified/production_verified:false`, `exception.applied:false`; **exactly 5 owner locks**, none mentioning access/a11y/wcag; `accessibility{}` has no lock boolean; exactly one `accessibility` completion flag in the schema. |
| A5 | **No false legal conformance claim** — no framework document asserts `ADA COMPLIANT` / `FULLY ACCESSIBLE` / `ACCESSIBILITY GUARANTEED` / `WCAG COMPLIANT` / `SECTION 508 COMPLIANT` / `EN 301 549 COMPLIANT` outside a prohibition context. |
| A6 | `ACCESSIBILITY_REVIEW` is a traceable `REQUIREMENT_SOURCES` entry; the accessibility assertions live in `browser-qa/assertions/catalog.py` (`check_accessibility`); **no separate accessibility runner** was created. |
| A7 | `SKILL.md` (≥ 2.9.0) declares `PHASE 6.9`, `GATE ACCESSIBILITY`, `[ACCESSIBILITY_READY]`, §5.16 single-source-of-truth rule, and restates "Exactly 5 owner locks remain". |
| A8 | `DESIGN-SYSTEM-PROTOCOL.md` §14 references the canonical protocol and the WCAG 2.2 target (contrast-safe token pairs, focus tokens, `44/24` distinction, colour-independent state). |
| A9 | `IMPLEMENTATION-CONTRACT.md` §2.8 adds builder accessibility requirements and halt-and-escalate on lock conflict. |
| A10 | `PRODUCTION-CHECKLIST.md` §3 upgraded to the WCAG 2.2 target and §5.5 adds full accessibility verification with the `AUTO_VERIFIED / MANUAL_VERIFIED / BLOCKED / NOT_APPLICABLE / KNOWN_GAP` classification. |
| A11 | `WEBSITE-GAUNTLET-PROTOCOL.md` §4.7 Accessibility Critic is preserved and enriched — **no new critic**, no second state machine. |
| A12 | `README.md` and `AGENTS.md` (≥ 2.9.0) document the subsystem and its additive governance. |
| A13 | All repository JSON parses; no secret-shaped material in any V2.9 file. |
| A14 | Frozen pilots under `projects/` are byte-for-byte unchanged before and after the run. |

---

## Part B — Negative controls (scenario A–R)

Each scenario is a fixture under `browser-qa/fixtures/` run through the `simulation` engine with a plan carrying an `accessibility` block.

| # | Fixture | What it models | Expected |
| :-- | :--- | :--- | :--- |
| A | `a11y_missing_name` | icon-only button, no accessible name | `a11y.accessible-name` → **FAIL** |
| B | `a11y_low_contrast` | text at 3.1:1 | `a11y.contrast` → **FAIL**, tagged `DETERMINISTIC` (Impeccable owns the math) |
| C | `a11y_keyboard_trap` | dialog focus cannot leave | `a11y.keyboard-trap` → **FAIL** |
| D | `a11y_focus_obscured` | sticky header covers the focused field | `a11y.focus-not-obscured` → **FAIL** |
| D′ | `a11y_focus_obscured_manual` | engine cannot objectively decide | `a11y.focus-not-obscured` → **BLOCKED** (`MANUAL_REQUIRED`) — never silent PASS |
| E | `a11y_missing_label` | form control with no label | `a11y.form-label` → **FAIL** |
| F | `a11y_error_not_associated` | error text not `aria-describedby` | `a11y.form-error-association` → **FAIL** |
| G | `a11y_reduced_motion_trap` | content stuck at `opacity:0` under reduced motion | `a11y.reduced-motion-trap` → **FAIL** (via the V2.8 §15 assertion) |
| H | `a11y_reflow` (320px) | primary CTA off-canvas at reflow width | `a11y.reflow` → **FAIL** |
| I | `a11y_text_spacing` | `h1` clips after the WCAG 1.4.12 override | `a11y.text-spacing` → **FAIL** |
| J | `a11y_target_size` | 30px adjacent link + 18px chip-close, no exception | `a11y.target-size-project` → **FAIL**; `a11y.target-size-wcag` → **FAIL** |
| K | `a11y_color_only_error` | error shown only as a red border | `a11y.color-independence` → **FAIL** |
| L | `a11y_dialog_good` | correct role/name/initial-focus/Escape/return | `a11y.dialog.contact-modal` → **PASS** |
| M | `a11y_decorative_image` | decorative image hidden correctly | zero FAIL/BLOCKED → **PASS** |
| N | `a11y_meaningful_image_no_alt` | team photo with no alt | `a11y.image-alt` → **FAIL** |
| O | `a11y_sr_unavailable` | no screen-reader environment | `a11y.screen-reader` → **BLOCKED**, never PASS |
| P | `a11y_engine_clean_manual_fail` | axe reports zero violations, manual keyboard review FAILs | `a11y.engine-violations` → PASS **but** `a11y.manual-keyboard` → **FAIL** → overall verification is **not a full PASS** |
| Q | (framework) | a sixth owner lock is introduced | framework validation **FAIL** (exactly the five canonical locks, no `*access*`/`*a11y*`/`*wcag*` key) |
| R | (guard) | a frozen pilot `site-profile.json` is mutated then restored | V2.8 `FrozenIntegrityGuard` **FAILs**, names the file; the recorded violation survives the restore |

Plus a harness self-check: `a11y_clean` yields **zero FAIL/BLOCKED**.

---

## Part C — "Test the tests" coverage (protocol §42)

Each safeguard is proven to fail on a deliberately broken synthetic fixture:
missing accessible name (A) · low contrast (B) · keyboard failure (C) · inaccessible
form (E, F) · reflow failure (H) · reduced-motion failure (G) · an invalid full-PASS
when the manual review is incomplete (P) · frozen-fixture mutation (R). Asserting
that scanners *exist* is not sufficient.

---

## Result

`V2.9 ACCESSIBILITY INTELLIGENCE TEST SUITE RESULT: <passed>/<run> ASSERTIONS PASSED`
with exit 0, and `projects/` byte-for-byte unchanged.
