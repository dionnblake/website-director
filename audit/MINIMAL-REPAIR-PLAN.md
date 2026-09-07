# Minimal Repair Plan

**Nothing in this file has been applied.** No diff was committed, merged, pushed, or deployed.
**PRODUCTION_CHANGES: NONE.** This stops at an owner-reviewable proposal.

**Constraints honoured:** no new protocol, critic, orchestration layer, prototype system, Gauntlet,
browser runner, asset pipeline, approval service, global taste profile, or sixth lock. Every repair
reuses an existing authority and an existing call site. All five locks
(`design_direction_locked`, `information_architecture_locked`, `content_structure_locked`,
`design_system_locked`, `motion_direction_locked`) are untouched;
`visual_prototypes.homepage_visual_approved` remains the only homepage-approval evidence location.

---

## R-1 — Let a current owner requirement arm its own check *(highest impact)*

**Root cause:** F2 — `check_motion` returns `None` before the owner-intent branch is reachable, so an
explicit `MOTION_LEVEL_3` requirement produces no check and no block.

**File / call site:** `browser-qa/assertions/catalog.py:492-494`, inside `check_motion`.

**Proposed change** — move the existing owner-intent resolution *above* the early return, and let a
resolved owner level arm the check. This adds no new authority; it makes the code at lines 506-513
reachable.

```diff
     cfg = _runtime_observation_cfg(plan, obs.route, "motion")
-    if not cfg.get("required") and not cfg.get("exercise"):
-        return None
+    # A current owner motion contract is itself a requirement.  A silent plan
+    # still infers nothing (legacy manifests are preserved), but an explicit
+    # owner level must not be escapable by omitting the plan's motion block.
+    owner_level = None
+    if plan.get("owner_intent"):
+        try:
+            from framework_validation.owner_intent import resolve_motion_requirement
+            resolved = resolve_motion_requirement(
+                plan["owner_intent"], heuristic_level="MOTION_LEVEL_1")
+            owner_level = (resolved.get("owner_required_level")
+                           or resolved.get("execution_level"))
+        except Exception:  # noqa: BLE001 - stays fail-closed below
+            owner_level = None
+    if not cfg.get("required") and not cfg.get("exercise") and not owner_level:
+        return None
```

…and at the existing resolution site, prefer the value already computed rather than resolving twice:

```diff
-    required_level = cfg.get("minimum_motion_level", cfg.get("required_level", cfg.get("motion_level")))
-    if required_level is None and plan.get("owner_intent"):
-        try:
-            from framework_validation.owner_intent import resolve_motion_requirement
-            resolved = resolve_motion_requirement(plan["owner_intent"], heuristic_level="MOTION_LEVEL_1")
-            required_level = resolved.get("owner_required_level") or resolved.get("execution_level")
-        except Exception:  # noqa: BLE001 - missing optional owner contract stays fail-closed below
-            required_level = None
+    required_level = cfg.get("minimum_motion_level", cfg.get("required_level", cfg.get("motion_level")))
+    if required_level is None:
+        required_level = owner_level
```

**Authority reused:** `framework_validation/owner_intent.resolve_motion_requirement` — already imported
here; no new module, no new state.

**Regression tests:** extend `tests/test_owner_intent_enforcement.py` with two cases —
(a) `owner_intent` demanding `MOTION_LEVEL_3` + **no** plan `motion` block → expect a `BLOCKED`
`motion.observation-coverage` finding, **not** `None`;
(b) **no** `owner_intent` and no `motion` block → still `None`, proving legacy manifests are preserved.

**Expected visible effect:** a build that promises cinematic motion and ships a fade can no longer
report a clean sweep. It reports a truthful block instead.

**Rollback / approval:** single-function change, revert by reverting the diff. Requires owner
awareness that previously-green ASN runs will go red — **that redness is the correct answer**, not a
regression.

---

## R-2 — Do not let ordinary scrolling prove motion

**Root cause:** F4 — `scroll_delta` counts toward "meaningful state change", so a static page that
merely scrolls satisfies `motion.runtime-state-change`. Measured on the real build:
`scrollDelta = 6156` with **0 keyframes**.

**File / call site:** `browser-qa/assertions/catalog.py:530-535`.

**Proposed change** — drop `scroll_delta` from the meaningfulness keys. Scroll position is an input to
motion, not evidence of it. Geometry and opacity deltas remain, so genuine scroll-driven
camera/scene motion still qualifies — it moves geometry.

```diff
     meaningful = [row for row in rows if row.get("meaningful_state_change") is True
                   or row.get("state_changed") is True
                   or row.get("observed_state_change") is True
                   or row.get("changed_properties")
                   or any(float(row.get(key, 0) or 0) > 0.01
-                         for key in ("max_geometry_delta", "max_opacity_delta", "scroll_delta")
+                         # scroll_delta is the *stimulus*, not the response: any tall
+                         # static page produces one.  Geometry/opacity deltas still
+                         # capture legitimate scroll-driven camera and scene motion.
+                         for key in ("max_geometry_delta", "max_opacity_delta")
                          if isinstance(row.get(key, 0), (int, float)))]
```

**Authority reused:** the existing `MOTION_SPEC` assertion group. No new critic, no new counter.

**Regression tests:** add to `tests/test_v2_8_browser_regression_qa.py` — a synthetic observation with
`scroll_delta: 6156` and zero geometry/opacity delta must now yield
`motion.runtime-state-change = FAIL`; a scroll-driven observation carrying `max_geometry_delta > 0.01`
must still PASS.

**Expected visible effect:** "the page scrolled" stops being accepted as "the page animated".
Legitimate scroll choreography is unaffected.

**Rollback:** one-line revert. Preserves reduced-motion behaviour and every frozen profile.

---

## R-3 — Make a "full homepage" surface actually capture the full homepage

**Root cause:** F5 — `DESKTOP_FULL_HOMEPAGE` / `MOBILE_FULL_HOMEPAGE` do not end in `FULL_PAGE`, so
they default to `VIEWPORT`. On the audited page that is ~9% of a 9,763 px homepage under a label
asserting the whole thing. No alias exists anywhere.

**File / call site:** `browser-qa/runner.py:96`, inside `_matrix()`.

**Proposed change** — one shared naming convention in the existing capture path. No second screenshot
system.

```diff
-            default_capture = "FULL_PAGE" if surface_id.endswith("FULL_PAGE") else "VIEWPORT"
+            # One convention for both surface vocabularies: cinematic_inspiration
+            # uses *_FULL_PAGE, design_first_flow uses *_FULL_HOMEPAGE.  A surface
+            # that claims the whole page must capture the whole page.
+            default_capture = ("FULL_PAGE"
+                               if surface_id.endswith(("FULL_PAGE", "FULL_HOMEPAGE"))
+                               else "VIEWPORT")
```

**Authority reused:** the existing `visual_evidence` surface path and
`design_first_flow.HOMEPAGE_REVIEW_SURFACES`. Nothing new is introduced.

**Regression tests:** promote reproduction **R1** into
`tests/test_design_first_production_flow.py` — assert that every id in `HOMEPAGE_REVIEW_SURFACES`
generates `capture == "FULL_PAGE"`, and that `DESKTOP_HERO` still generates `VIEWPORT`.

**Expected visible effect:** the first project to adopt the design-first flow gets a real full-homepage
review instead of a hero crop labelled as one.

**Rollback:** one-line revert. **Note the sequencing constraint:** this repair only reaches a project
once that project's branch actually contains `design_first_flow.py` — see the deferred item D-1.

---

## Deferred — identified, deliberately not implemented

| # | Item | Why deferred |
|---|---|---|
| **D-1** | **Branch distribution (F1 + F1b).** The ASN build branch is 17 commits behind `main` and contains none of the enforcement modules. Worse, the QA harness it actually executed (`catalog.py`, 31,838 bytes, `44a23319…`) is a v2-10-era file with **no `check_motion`, no `check_brand_tokens`, and no `check_observation_coverage`** — see the harness-identity table in `REPRODUCTION-RESULTS.md`. | This is an owner branch-strategy decision, not a code fix. Merging or rebasing is explicitly out of scope for this audit. **D-1 outranks R-1–R-3 in practical impact: those repairs are correct but cannot reach ASN until the build runs a harness that contains the checks at all.** |
| **D-2** | **Motion-contract conflict (F3).** `VISUAL-CONTRACT.md` § Motion contract contradicts owner requirement `motion.owner-cinematic`. | Changing an approved design/motion decision requires the **existing owner change-request path**, not an audit edit. The owner must decide: raise the build to `MOTION_LEVEL_3`, or formally approve a downgrade (`approved_downgrade`), which is currently `false`. |
| **D-3** | **Wire `audit_owner_requirement_compliance()` into the runner.** It exists at `owner_intent.py:929` and `runner.py` never calls it. | Larger integration change; R-1 addresses the acute motion path with far less surface area. Revisit once D-1 lands. |
| **D-4** | **Evidence-reader hardening (F6).** `_actual_screenshot()` could `os.path.exists()` and recompute the digest; `validate_production_gate()` could invoke the design/derivation validators it currently trusts as flags. | Real but second-order: runner-produced evidence is already genuinely hashed (`runner.py:414`). Hand-authored evidence is the exposure. Not on the ASN critical path. |
| **D-5** | **Brand-validator sensitivity (F7).** `validate_brand_tokens` flags `paper cream` as an unapproved dominant hue although measurement shows navy dominant and cream plausibly a permitted "restrained light neutral". | Needs an owner ruling on whether cream-as-supporting-neutral is in contract before any code is tuned. Tuning it first would risk weakening a real brand guard. |
| **D-6** | **Ritual-plate provenance.** 5 plates lack provenance records (already disclosed as `ASSET_PROVENANCE: PARTIAL`). | Requires human review, not a code repair. |

---

## Sequencing

```
D-1  branch distribution (owner decision)
  |
  +--> R-1, R-2, R-3 become effective for ASN
         |
         +--> re-run the project's browser-qa harness with owner_intent + motion
                declared in qa/browser-qa-manifest.json
                |
                +--> D-2 owner change request on the motion contract
                       (raise to MOTION_LEVEL_3, or formally approve a downgrade)
```

Repairing code before D-1 is decided produces correct code that the ASN build still cannot see.

---

## Verification after any repair

1. Re-run all four registered suites; expect no new failures and
   `FROZEN_FIXTURE_INTEGRITY = PASS (465 files unchanged)`.
2. Re-run reproductions R1, R2, R4 — R1 case B must become `FULL_PAGE`; R2 case 2 must become a
   truthful `BLOCKED`.
3. Confirm legacy manifests without `owner_intent` still infer nothing (the R2 case-1 control), so
   historical compatibility and frozen profiles are preserved.
4. Confirm `OWNER_FINAL_ACCEPTANCE` remains `PENDING` and `PRODUCTION_CERTIFICATION` remains
   `NOT_GRANTED` — no repair may promote owner status.
