# V2.8 Browser & Regression QA — Integration Validation Suite

> Validates that the Phase 10.5 subsystem (`BROWSER-REGRESSION-QA-PROTOCOL.md`) is wired
> into Website Director and that **every major guard actually fails** on a broken input.
> Automated form: `tests/test_v2_8_browser_regression_qa.py` (exit 0 = pass), run with the
> deterministic `simulation` engine and only the Python standard library.

```bash
python tests/test_v2_8_browser_regression_qa.py
```

---

## Part A — Repository wiring invariants

| # | Assertion |
| :-- | :--- |
| A1 | `BROWSER-REGRESSION-QA-PROTOCOL.md` exists and is the **only** canonical browser/regression protocol at repo root. |
| A2 | `templates/browser-qa-plan.md`, `templates/browser-qa-manifest.json`, and the `browser-qa/` harness (`runner.py`, `engine/`, `assertions/`, `guards/`, `config/`, `fixtures/`) exist. |
| A3 | Protocol declares `[BROWSER_QA_PASS]`, `browser_qa.complete`, `BROWSER_QA_ENGINE`, the single-completion-flag invariant, "not an owner lock", `FROZEN_FIXTURE_MUTATION`, `LOCAL_IMPLEMENTATION_VERIFIED` vs `PRODUCTION_VERIFIED`, and the full verdict vocabulary. |
| A4 | `templates/site-profile.json` contains `browser_qa{}` with `complete: false`, `visual_regression_status: "NOT_RUN"`, `frozen_fixture_integrity: "UNVERIFIED"`, `implementation_verified/production_verified: false`, `exception.applied: false`; **exactly 5 owner locks**; no `*_locked` key mentions browser/qa; `browser_qa{}` has no lock boolean; exactly one `browser_qa` completion flag in the schema. |
| A5 | `SKILL.md` (v2.8.0) declares `PHASE 10.5`, `GATE BROWSER`, `[BROWSER_QA_PASS]`, §5.15 single-source-of-truth rule, and restates "Exactly 5 owner locks remain". |
| A6 | `IMPLEMENTATION-CONTRACT.md` §2.7 adds builder testability requirements (stable selectors, no disabling QA, no silent baseline updates). |
| A7 | `PRODUCTION-CHECKLIST.md` §5.4 requires machine evidence for auto-verifiable checks. |
| A8 | `WEBSITE-GAUNTLET-PROTOCOL.md` §4.16 adds the deterministic browser QA entry precondition — **no new critic, no second state machine**. |
| A9 | `IMPECCABLE-ENGINE-PROTOCOL.md` adds the `BROWSER_EXECUTED` method and the static-vs-runtime rule-ownership table (one owner per rule). |
| A10 | `README.md` and `AGENTS.md` (v2.8.0) document the subsystem and its additive governance rules. |
| A11 | No secret-shaped material in any V2.8 file. |
| A12 | Frozen pilots under `projects/` are byte-for-byte unchanged before and after the run. |

---

## Part B — Negative controls (scenario A–L)

Each scenario is a fixture under `browser-qa/fixtures/`. The suite runs it through the
`simulation` engine and asserts the verdict.

| # | Fixture | What it models | Expected verdict |
| :-- | :--- | :--- | :--- |
| **A** | `a_responsive_overflow` | A 520px block inside a 390px viewport | `responsive.horizontal-overflow` → **FAIL** at 390px, **PASS** at 1440px (real overflow detected, not masked) |
| **B** | `b_console_exception` | `throw new Error(...)` in an inline script | `console.no-application-errors` → **FAIL** |
| **C** | `c_broken_hero` | Hero image 404s and renders zero-dimension | asset + `network.no-failed-requests` → **FAIL** |
| **D** | `d_mobile_nav` | Mobile nav opens on toggle, closes on route change | `nav.mobile-*` → **PASS** |
| **E** | `e_failed_form` | Server rejects; site shows a visible error, no success state, no success event | `form.contact.*` → **PASS** |
| **E′** | `e_false_success` | Server rejects but the site shows success and fires `contact_submit_success` | `form.contact.no-false-conversion` + `form.contact.success-state` → **FAIL** |
| **F** | `f_reduced_motion` | Motion-heavy copy stays visible under `prefers-reduced-motion: reduce` | `motion.reduced-content-visible` → **PASS** |
| **F′** | `f_reduced_motion_broken` | A paragraph stuck at `opacity:0` with no reduced-motion fallback | `motion.reduced-content-visible` → **FAIL** |
| **G** | `g_visual_shift` | Render signature differs from the locked baseline (a 20px hero shift) | `visual.regression` → **FAIL / DIFF DETECTED**, method `VISUAL_COMPARISON`, **baseline fixture not overwritten** |
| **H** | `h_dynamic_timestamp` | A timestamp + rotating testimonial pinned by deterministic fixture handling | `visual.regression` → **PASS** (no false regression) |
| **I** | (guard, not a page) | A protected file under `projects/` is deliberately appended to, then restored | `FrozenIntegrityGuard.verify()` → **FAIL**, names the file, flags the git change, and the append-only ledger records it **despite the restore** |
| **J** | `j_flaky` | First run FAILs, retry PASSes | runner records **FLAKY** (not PASS); `flaky_tests` non-empty; runner exit ≠ 0 |
| **K** | `clean_reference` (local plan) | A clean run against a local build | `environment = local`; `production_verified` stays **false** |
| **L** | `l_pii_event` | Analytics event `newsletter_signup` carries `email: visitor@example.com` | `measure.no-pii` → **FAIL** |

Plus a harness self-check: `clean_reference` on a complete plan yields **zero FAIL/BLOCKED**.

---

## Part C — "Test the tests" coverage (protocol §36)

The suite demonstrates each guard can fail: **frozen-fixture mutation** (I), **console error** (B),
**network failure** (C), **visual diff** (G), **PII event** (L), and **obsolete/invalid state schema**
(`examples/test_runner.py` §R — a sixth owner lock and an unknown `schema_version` are rejected).

---

## Result

`V2.8 BROWSER & REGRESSION QA TEST SUITE RESULT: <passed>/<run> ASSERTIONS PASSED` with exit 0,
and `projects/` byte-for-byte unchanged.
