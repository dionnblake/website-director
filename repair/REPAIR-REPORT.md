# Website Director — bounded enforcement repair

**PRODUCTION_CHANGES: NONE.** No original checkout was edited, nothing was committed, pushed,
merged, or deployed. The candidate repair is left uncommitted as a reviewable diff.

---

## 0. What changed, in one paragraph

Three handoffs were broken. A current owner requirement could not arm its own check, because the
runtime motion and brand checks returned `None` before any contract was consulted; motion "evidence"
counted the *stimulus* (the page scrolled) as the *response* (something moved); and a full-homepage
review name silently produced a viewport crop while receipts were validated as metadata shapes
rather than as files. All three now resolve through **one** shared owner-authority profile, are
measured against the element's own scroll-compensated response, and are bound to real bytes on disk.
A silent legacy manifest still infers nothing, so historical and frozen work is unaffected.

---

## 1. `CANDIDATE_BASE_AND_RUNTIME_IDENTITY`

Refs were re-checked before selecting a base; no drift from the reviewed snapshots.

| Ref | Reviewed | Observed now | Result |
|---|---|---|---|
| `origin/main` | `416f95d3c1f715…` | `416f95d3c1f715…` | MATCH |
| `origin/feature/design-first-production-flow` | `d732a0ec657746…` | `d732a0ec657746…` | MATCH |
| audit branch | `b59e52c735889…` | `b59e52c735889…` | MATCH |
| `feat/v2-10-launch-post-launch-operations` | `3a01c0d` | `3a01c0d` | MATCH |
| `feature/asn-visual-first-production` | `ab91263` | `ab91263` | MATCH |

**Base chosen:** `d732a0ec657746ca8a738377cfe636c8318aae2f`
(`origin/feature/design-first-production-flow`). `origin/main` is an ancestor of it, so this is the
complete reviewed lineage plus `design_first_flow.py`. The audit branch was **not** used as an
implementation base — it carries the reports, not the lineage.

**Candidate worktree:** `.claude/worktrees/website-director-repair-53f3d1`, branch
`claude/website-director-repair-53f3d1`, working tree dirty by exactly the diff in §9.

### Loaded runtime identity (resolved by the process, not assumed from the repository)

| Item | Value |
|---|---|
| Python | `C:\Users\ALPHA\AppData\Local\Programs\Python\Python313\python.exe` — 3.13.13 |
| Browser | Chrome **152.0.7977.77**, driven through the already-installed system channel |
| `SKILL.md` | `a1dec1fdc82d10f9` *(repository-resident; there is no separate installed skill copy)* |
| `framework_validation/owner_intent.py` | `b9e5388eb6d1bb16` |
| `framework_validation/design_first_flow.py` | `ecd1a4ae07849d70` |
| `framework_validation/cinematic_inspiration.py` | `6472d939285619cd` |
| `browser-qa/runner.py` | `b3b0db5e230f5d5a` |
| `browser-qa/assertions/catalog.py` | `eda784f364536357` |
| `browser-qa/engine/playwright_engine.py` | `0e21fca335e9a2d7` |
| `browser-qa/guards/frozen_integrity_guard.py` | `ef7387d3f9e3f167` *(unchanged)* |
| Owner contract consumed | `templates/alpha-starts-now-owner-intent.json` — `9b3ccab0c9ed0893` |

Every run now records this itself: `manifest.loaded_harness` carries the resolved **path and
SHA-256 of each imported module**, plus the interpreter and import paths. Existence of a file
somewhere in the repository is no longer accepted as evidence of what ran.

> **Note on the browser.** `playwright install` had never been run here, so no bundled Chromium
> exists. Rather than download a new provider, the adapter gained an optional
> `browser_channel` / `browser_executable_path` passthrough and drives the already-installed system
> Chrome. The default launch behaviour is unchanged.

---

## 2. `CANDIDATE_WORKFLOW_WIRED` — observed **YES**

The stale-harness gate, the owner-authority resolution, the repaired motion measurement, the
full-homepage capture convention, and the evidence binding all execute through the ordinary entry
point (`browser-qa/runner.py`) and change its result. Demonstrated on real browser runs in §6–§7.

## 3. `DAILY_WORKFLOW_CUTOVER = NOT_PERFORMED`

A working isolated candidate is not adoption. **Not performed here.** The exact later cutover:

1. Land this candidate branch on the framework line the ASN build actually consumes — today that
   build runs a v2-10-era `catalog.py` with no `check_motion`, `check_brand_tokens` or
   `check_observation_coverage` at all. Until then these repairs cannot reach it. *(This is the
   audit's D-1 and remains an owner branch-strategy decision.)*
2. Add the owner-authority declaration to the project's own
   `qa/browser-qa-manifest.json` — either `"owner_intent_ref": "<path to the current contract>"` or
   `"project_currentness": "CURRENT"` plus that reference. **Verified behaviour:** with the shipped
   manifest exactly as it is today, the repaired harness still reports
   `owner_requirement_compliance: NOT_DECLARED` (§7 baseline). Silence is still silence — by design,
   because that is what protects every legacy and frozen manifest. The declaration is the cutover.
3. Re-run the project's harness and act on the result.

Neither step was taken. No original manifest was edited.

---

## 4. `OWNER_REQUIREMENT_ENFORCEMENT`

One shared authority — `owner_intent.resolve_owner_authority()` — normalizes requirements once.
`catalog.owner_authority()`, the runner's completion boundary, and the design-first production entry
all read that profile; none re-implements precedence.

| Required behaviour | How it is met |
|---|---|
| Resolve the authoritative contract **before** a production-entry or completion decision | Resolution runs ahead of every early return in `check_motion` / `check_brand_tokens`, and once more at the runner's completion boundary |
| Derive coverage from the authority, not only from manifest flags | `coverage.{motion,brand,visual_evidence}` comes from the contract's requirement classes. Omitting `owner_intent`, `motion`, `runtime_observations` or `visual_evidence` cannot make a required check NOT_APPLICABLE — it produces execution or a truthful BLOCK naming the missing path/reason |
| A lower plan/route level cannot override a REQUIRED owner level | The effective level is raised to the owner level and the finding records `required_level_source: OWNER` |
| PREFERRED/OPTIONAL never silently becomes REQUIRED | `_coverage_for()` maps them to `OPTIONAL`; regression-tested both ways |
| An approved downgrade must be authentic and scope-correct | `resolve_approved_motion_downgrade()` requires an owner actor, an owner event reference, and a matching scope. A bare `approved_downgrade: true`, a critic-authored one, or a wrong-scope one is rejected and blocks |
| Malformed contracts and resolution exceptions block | Missing file, unreadable file, malformed JSON, non-object contract, and any exception all produce `BLOCKED` with the path and reason — never a swallowed error followed by "no owner level" |
| Missing required sequences produce truthful findings | `motion.sequence-inventory` BLOCKS when the contract requires named sequences and none are declared. **No sequence list is invented** |
| `audit_owner_requirement_compliance()` reaches the decision | Wired at the runner's completion boundary (once per run, not per observation). Its issues become findings that count toward the run verdict |
| Historical/frozen scope preserved | `project_currentness: HISTORICAL / REFERENCE_ONLY / SUPERSEDED` reports requirements and enforces nothing. A silent plan resolves to `NOT_DECLARED` without even importing the framework module |

**Stale/mixed harness gate.** `runner.harness_identity()` resolves the loaded catalogue and
framework modules, hashes them, and blocks the run before any route is judged when a check the
review depends on is missing or unregistered. This is the guard whose absence let a v2-10-era
harness report `{'PASS': 3332}` with no runtime-motion, brand, or coverage check in it.

---

## 5. `REAL_MOTION_NEGATIVE_AND_POSITIVE_CONTROLS`

### Producer (`playwright_engine`)

- Node snapshots now carry **document-space coordinates**, computed style `position`, tag,
  `clip-path`, `filter`, `data-motion-state`, media `currentTime`, and running-animation counts.
- Response is measured **scroll-compensated**: document-space delta for ordinary elements, viewport
  delta for `fixed`/`sticky` elements (a pinned element answers by holding its position). Ancestor
  scrolling therefore cancels.
- `scroll` was removed from `changed_properties`; the scroll amount is reported separately as
  `stimulus_scroll_delta`, and `raw_viewport_geometry_delta` is retained for transparency.
- `state_changed` and `meaningful_state_change` are derived from response signals only.
- A sequence's family is no longer defaulted to `SCROLL_DRIVEN` from its action. It is either
  `DECLARED` by the sequence or a `MEASURED_*` description of the property that actually changed,
  tagged with `family_source`.
- Target count, trigger application, per-sample step measurements and `observed_states`
  (`START` / `CHANGE` / `SETTLE`) are emitted per sequence.
- Unobservable targets are reported as unobservable: a `<canvas>` with no `data-motion-state` and no
  Web Animation yields `observation_supported: false` and a reason, **not** "no motion". Video/audio
  scrub is measured through `currentTime`.

### Consumer (`catalog.check_motion`)

- Meaningfulness accepts only whitelisted **response** properties or numeric response deltas.
  Producer booleans and free-text `changed_properties` can no longer stand in for evidence.
- Per-sequence findings: `motion.sequence-coverage`, `motion.sequence-behavior`,
  `motion.sequence-states`, `motion.sequence-observation`. The runner's flake key was scoped so a
  working sequence can no longer overwrite a stationary sibling.
- `motion.generic-fade-diversity` counts only families that were **declared and observed**.
- Reduced-motion runs assert the usable equivalent (`motion.reduced-motion-counterpart`) and never
  demand choreography; the normal-motion counterpart carries that obligation.

### Real-browser results (Chrome 152, candidate entry point)

**Negative control** — a genuinely tall static page, scrolled 7,766 px:

| Sequence | Measured | Verdict |
|---|---|---|
| `hero-intro` | `raw_viewport_geometry_delta: 7766`, **`max_geometry_delta: 0`**, `changed_properties: []` | `motion.sequence-behavior` **FAIL** |
| `route-progression` | no response | **FAIL** |
| `canvas-scene` | canvas with no state hook | `motion.sequence-observation` **BLOCKED** |
| aggregate | `responding=0/3` | `motion.runtime-state-change` **FAIL** |
| families | `proven_families=[] declared=0/3` | `motion.generic-fade-diversity` **FAIL** |
| reduced-motion counterpart | static fallback correct | **PASS** |

The whole page moved 7,766 px through the viewport and the scroll-compensated response is `0`.
That is F4 closed at the producer, on a real browser.

**Positive control** — genuine masked parallax plus a pinned scrub:

| Sequence | Measured response | Verdict |
|---|---|---|
| `hero-intro` | `['clip','geometry','transform']` | **PASS**, states `START/CHANGE/SETTLE` |
| `route-progression` | `['geometry','motion_state']` | **PASS**, states `START/CHANGE/SETTLE` |
| aggregate | `responding=2/2` | **PASS** |
| families | `['PARALLAX_MASK','PINNED_SCRUB']` | **PASS** |
| brand | navy/yellow field | `brand.current-palette` **PASS** |

Both controls ran through `browser-qa/runner.py --engine playwright`, the same entry point intended
for real work.

---

## 6. `FULL_HOMEPAGE_CAPTURE`

One convention: `default_capture` now honours both `*_FULL_PAGE` and `*_FULL_HOMEPAGE`. Captures
wait for `document.fonts.ready` and network idle, and a full-page capture first walks the document
so lazily loaded below-fold media has its chance to load. Each capture records image dimensions read
from the PNG header, the document height, below-fold element count, and image completeness.

Measured on the capture control:

| Surface | Capture | Image | Document | Verdict |
|---|---|---|---|---|
| `DESKTOP_FULL_HOMEPAGE` *(with a `"capture": "VIEWPORT"` override)* | FULL_PAGE | 1440 × 4564 | 4564 | override rejected → `CAPTURE_LABEL_CONFLICT` **BLOCKED** |
| `MOBILE_FULL_HOMEPAGE` | FULL_PAGE | 552 × 4564 | 4564 | verified |
| `DESKTOP_FULL_PAGE` | FULL_PAGE | 1440 × 4564 | 4564 | verified |
| `DESKTOP_HERO` | VIEWPORT | 1440 × 900 | 4564 | correctly a viewport crop |

A whole-page label carrying a viewport override is normalized to FULL_PAGE **and** reported as a
label conflict, so it cannot quietly establish a homepage review.

On the real ASN homepage the same path produced 1440 × 9781 and 390 × 14311 — matching the audit's
independently measured dimensions — with 9/9 images loaded at capture.

---

## 7. `PRODUCTION_ENTRY_EVIDENCE_BINDING`

- `resolve_screenshot_receipt()` opens the claimed file, recomputes its SHA-256, and rejects missing,
  unreadable, digest-mismatched, and out-of-scope paths. No new cryptographic infrastructure — it
  recomputes the digest the runner already writes.
- `validate_rendered_visual_evidence()` keeps its pure metadata behaviour for unit tests, and
  resolves receipts on disk whenever an `evidence_root` is supplied — which the runner and the
  production-entry boundary now both do.
- `validate_production_gate()` validates the underlying business / homepage-design /
  design-system results whenever they are supplied, so a real failure survives a `True` flag beside
  it, and it requires the owner approval to bind to **screenshot receipts**. Bare surface names now
  return `PRODUCTION_ENTRY_EVIDENCE_NOT_BOUND` and `can_start_production: False`. Project and build
  mismatches are rejected as `EVIDENCE_PROJECT_MISMATCH` / `STALE_EVIDENCE_REJECTED`.
- **Working-tree identity.** `_build_identity()` records the HEAD sha, whether the tree is dirty, and
  a content digest of the served bytes; `build_id` prefers the content digest, because a HEAD sha
  cannot identify a dirty tree. A nonvisual edit does not by itself invalidate identical screenshots.
- `validate_homepage_approval()` is unchanged: approval *shape* is still its own question, and
  `EVIDENCE_VALID` stays distinct from visual quality, rights, and owner acceptance. Nothing in this
  repair creates or sets an approval flag for the real ASN candidate.

**R4 status.** R4-C1 (bare strings behind seven true flags) and R4-C2 (fabricated receipts with
64-zero digests over nonexistent files) are both closed at the acceptance boundary and covered by
new negative controls. No blocked remainder.

---

## 8. `UNIT_TESTS` / `INTEGRATION_TESTS` / `REAL_BROWSER_TESTS`

Kept strictly separate.

### Unit + integration — all 16 registered suites, `SUITES_FAILED: none`

| Suite | Result |
|---|---|
| `owner_intent_brand_motion_enforcement` | **OK — 26 tests** (was 18) |
| `design_first_production_flow` | **OK — 30 tests** (was 24) |
| `v2_8_browser_regression_qa` | **100/100 assertions** (was 89) · `FROZEN_FIXTURE_INTEGRITY = PASS (465 files unchanged)` |
| `v2_9_accessibility` | 80/80 |
| `v2_10_launch_operations` | 100/100 |
| `v2_7_security_privacy` | 121/121 |
| `v2_5_client_handoff` / `v2_5_1_signature_choreography` | 43/43 · 32/32 |
| `framework_validation`, `v2_11`–`v2_15`, `cinematic_inspiration`, `examples_test_runner` | OK |

Framework verifier: `python -m framework_validation --run-suites` →
**`FRAMEWORK_VALIDATION_PASS`, 298 passed / 0 failed / 0 blocked / 1 warning.** The single warning
(`MAIN_DIVERGENCE_STATUS: REMOTE_MAIN_BEHIND_DEVELOPMENT`) is pre-existing branch divergence, not
introduced here.

New regression cases, mapped to the required list:

| Required case | Where |
|---|---|
| Stale/mixed loaded harness detected before verification | `test_owner_intent_enforcement` + v2.8 control **T** (end-to-end through the runner) |
| Level 3 + omitted motion config → execution or BLOCKED, never `None`/PASS | `test_current_level_three_with_omitted_motion_block_is_never_none_or_pass` |
| Removing the owner block cannot remove project requirements | `test_removing_the_owner_block_cannot_remove_project_requirements` |
| Lower plan/route level and resolution error cannot downgrade | `test_lower_plan_level_cannot_downgrade_a_required_owner_level`, `test_contract_resolution_error_blocks_instead_of_downgrading` |
| Historical fixture preserved; genuine approved downgrade honoured (synthetic `TEST_ONLY` records) | `test_historical_scope_preserves_documented_compatibility`, `test_only_a_genuine_owner_downgrade_record_is_honoured` |
| PREFERRED/OPTIONAL never becomes REQUIRED | `test_preferred_or_optional_motion_never_becomes_required` |
| Static tall page scrolled stays non-cinematic despite flags/labels | v2.8 controls **K**, **L** |
| Two promised sequences, one working → per-sequence failure; real sequence as positive control | v2.8 controls **M**, **N**, **O**, **P** |
| Normal vs reduced-motion counterparts distinct, fallback not a failure | v2.8 control **Q** |
| Unsupported observation BLOCKED, inventory not invented | v2.8 controls **R**, **S** |
| Both full-page conventions capture the full page; hero stays a viewport; override rejected | `test_both_full_page_conventions_capture_the_whole_page`, `test_viewport_override_on_a_whole_page_surface_is_rejected` |
| Bare strings, missing files, wrong digests, wrong build/project, inconsistent booleans cannot authorize production entry | `test_bare_surface_names_cannot_authorize_production_entry`, `test_missing_files_wrong_digests_and_wrong_build_are_rejected`, `test_underlying_design_failures_survive_true_flags` |
| Real files and consistent test-only artifacts pass without granting approval | `test_real_files_and_consistent_receipts_pass_without_granting_approval` |

### Real browser — **RAN** (Chrome 152), reported separately

`repair/evidence/negative-control/`, `positive-control/`, `capture-control/`. Not merged into the
unit results. Nothing was simulated in place of a browser.

---

## 9. `EXISTING_ASN_BUILD_REASSESSMENT`

An **unchanged, hash-inventoried isolated copy** of the current ASN candidate
(`projects/alpha-starts-now-visual-first-production`, 137 files) was reassessed with the candidate
harness and the authentic current owner contract. Candidate-only manifests were written **outside**
the original project. The copy was verified byte-for-byte identical before and after the run
(`repair/evidence/asn-copy-inventory.json`).

### Control A — shipped manifest, unmodified

`owner_requirement_compliance: NOT_DECLARED`, all coverage `NOT_REQUIRED`.
8 FAIL: `form.form-1.{dup-submit,keyboard,success-state}` and `responsive.primary-cta-hidden`.
These are present **without** the owner contract and are unrelated to this repair; they are reported,
not claimed as new defects and not investigated here.

### Control B — same build, owner contract declared

`overall: BLOCKED` — `{'PASS': 98, 'FAIL': 38, 'BLOCKED': 5}`.

| Finding | Result |
|---|---|
| `motion.owner-cinematic` (REQUIRED, `MOTION_LEVEL_3`) | **BLOCKED_WITH_EXPLANATION** — `execution_level: MOTION_LEVEL_3`, `approved_downgrade: false` |
| `MOTION_BRIEF_SEQUENCES_MISSING` | **BLOCKED** — Level 3 requires named sequences; the project names none |
| `motion.generic-fade-diversity` | **FAIL** on every normal-motion job — `proven_families=[] declared=0/1` |
| `motion.sequence-behavior` @1440 | **PASS** — the reveal is real: opacity Δ 0.845, geometry Δ 15.2 px, transform changed |
| `motion.sequence-behavior` @390 | **FAIL** — no response; the reveals had already settled |
| `motion.reduced-motion-counterpart` | **PASS** — correct static fallback, not treated as missing animation |
| `brand.current-palette` | **FAIL** — see the caveat below |
| Full-homepage captures | 1440 × 9781 and 390 × 14311, 9/9 images, receipts resolved on disk |

**The control is green in the right direction:** the promised choreography is missing and the
enforcement now says so, without touching the website, relaxing the contract, masking a check, or
changing a requirement class. Typography, hero, copy, layout, navigation and accessibility are
untouched and continue to pass.

> **Brand caveat, preserved deliberately.** `brand.current-palette` now runs — that coverage gap is
> proven closed. It reports `UNAPPROVED_DOMINANT_BRAND_HUE` for the cream field. **A brand breach is
> still `NOT_VERIFIED`**: area-weighted measurement shows navy/ink dominant and cream plausibly a
> permitted supporting neutral. The validator was not tuned and the site was not repainted. This
> needs an owner ruling.

---

## 10. Registers

| Register | Status |
|---|---|
| `CANDIDATE_BASE_AND_RUNTIME_IDENTITY` | COMPLETE — base `d732a0e`; loaded modules hashed and recorded per run |
| `CANDIDATE_WORKFLOW_WIRED` | **YES** — observed through the ordinary entry point on real browser runs |
| `DAILY_WORKFLOW_CUTOVER` | **NOT_PERFORMED** — exact actions documented in §3 |
| `OWNER_REQUIREMENT_ENFORCEMENT` | REPAIRED — one shared authority; blocks are explicit, never silent |
| `REAL_MOTION_NEGATIVE_AND_POSITIVE_CONTROLS` | BOTH PASS — static tall page stays non-cinematic; real choreography passes |
| `FULL_HOMEPAGE_CAPTURE` | REPAIRED — both conventions capture the full page; hero stays a viewport; dishonest override rejected |
| `PRODUCTION_ENTRY_EVIDENCE_BINDING` | REPAIRED — receipts resolved and re-hashed on disk; R4-C1 and R4-C2 closed |
| `UNIT_TESTS` | PASS — 16/16 registered suites; verifier 298/0/0 + 1 pre-existing warning |
| `INTEGRATION_TESTS` | PASS — R1/R2/R4 promoted into registered suites |
| `REAL_BROWSER_TESTS` | RAN — Chrome 152; results kept separate |
| `EXISTING_ASN_BUILD_REASSESSMENT` | COMPLETE — unchanged copy; correct FAIL/BLOCKED on missing choreography |
| `MOTION_CHANGE_REQUEST` | **PREPARED_NOT_APPROVED** — `repair/MOTION-CHANGE-REQUEST.md` |
| `ORIGINAL_DIRTY_WORK_PRESERVED` | YES — owner checkout `3a01c0d` with 11 entries; ASN worktree `ab91263` with 60 entries; audit worktree clean. All unchanged |
| `FROZEN_PROJECT_INTEGRITY` | PASS — `465 files unchanged` on every suite run and every browser run |
| `ASSET_PROVENANCE` | UNRESOLVED — 5 ritual plates still lack provenance records. Preserved, not closed |
| `OWNER_FINAL_ACCEPTANCE` | **PENDING** — unchanged |
| `PRODUCTION_CERTIFICATION` | **NOT_GRANTED** — unchanged |
| `PRODUCTION_CHANGES` | **NONE** |

---

## 11. Candidate diff and evidence paths

Nine framework files changed; `repair/` is new and untracked.

```
browser-qa/assertions/catalog.py
browser-qa/engine/playwright_engine.py
browser-qa/runner.py
framework_validation/cinematic_inspiration.py
framework_validation/design_first_flow.py
framework_validation/owner_intent.py
tests/test_design_first_production_flow.py
tests/test_owner_intent_enforcement.py
tests/test_v2_8_browser_regression_qa.py
```

No new protocol, critic, runner, framework, dashboard, gate, approval service, or owner lock was
created. The five canonical owner locks are untouched and
`visual_prototypes.homepage_visual_approved` remains the only homepage-approval location.

| Artifact | Path |
|---|---|
| Trimmed review evidence | `repair/evidence/` *(per-sample DOM snapshots removed; findings and measurements intact)* |
| Candidate-only QA inputs | `repair/fixtures/` |
| Full evidence + screenshots | `C:\Users\ALPHA\AppData\Local\Temp\wdr\evidence\` (27 PNG receipts) |
| Isolated read-only ASN copy | `C:\Users\ALPHA\AppData\Local\Temp\wdr\asn-ro\` |
| Copy hash inventory | `repair/evidence/asn-copy-inventory.json` |

---

## 12. Honest limits

- This repairs the **measurement and authority path**. It does not make the existing website
  cinematic or premium, and it certifies nothing about visual quality or taste.
- The repairs cannot reach the ASN build until D-1 (branch distribution) is decided by the owner.
- The brand breach remains `NOT_VERIFIED`; only the missing coverage was fixed.
- The form and responsive-CTA failures in §9 Control A are observed and reported, not diagnosed.
- No owner approval was created, implied, or recorded anywhere.
