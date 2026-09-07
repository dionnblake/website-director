# Website Director — Reference-to-Render Disconnect Audit

**Audit date:** 2026-09-06
**Scope:** Read-only source inspection, isolated local reproduction, isolated local browser capture.
**PRODUCTION_CHANGES: NONE.** No repository source, protected project, installed skill, approval record, or production system was modified.

---

## 0. Answer first

**The first broken handoff is the owner-intent → project-contract handoff**, at
`projects/alpha-starts-now-visual-first-production/VISUAL-CONTRACT.md` § *Motion contract*.

A project-local document silently restated the owner's standing **`MOTION_LEVEL_3` cinematic,
animation-heavy, sequence-driven** requirement as *"Motion is limited to transform/opacity reveals…
no animation is required to understand the content."* Everything downstream then executed that
downgraded contract faithfully. Nothing detected the substitution, because the build branch did not
contain the enforcement modules and the QA manifest did not declare the blocks that would have
activated them.

**Confidence: HIGH.** The owner requirement, the contradicting project contract, the resulting
implementation, and the clean-sweep QA report are all present on disk and quoted below.

**Limiting factor:** **stale distribution first**, then **disconnected enforcement** — together they
permitted a **creative-direction downgrade** to pass unchallenged. Implementation fidelity to the
(downgraded) contract is good. Review is inadequate *for motion and brand only* — it is genuinely
thorough elsewhere.

Stale distribution is ranked first because it is doubly proven: the build branch lacks the
enforcement *modules* (F1), **and** the QA harness binary it actually executed is a v2-10-era file
missing `check_motion`, `check_brand_tokens` and `check_observation_coverage` outright (F1b).
Fixing the enforcement code alone will not reach this project.

---

## 1. LOCAL_RUNTIME_IDENTITY

| Field | Value |
|---|---|
| Audit worktree | `.claude/worktrees/website-director-audit-78d528` |
| Audit branch / HEAD | `claude/website-director-audit-78d528` @ `416f95d3c1f71521bdaea475ab456514c7f6e50d` |
| Audit worktree dirty | **clean** (0 entries at audit start) |
| Framework version | `2.15.0` (root `AGENTS.md`) |
| Python | 3.13.13 |

### Worktrees present

| Path | Branch | HEAD |
|---|---|---|
| `WEBSITE-DIRECTOR` (owner's main checkout) | `feat/v2-10-launch-post-launch-operations` | `3a01c0d` |
| `…/.claude/worktrees/website-director-audit-78d528` (this audit) | `claude/website-director-audit-78d528` | `416f95d` |
| `WEBSITE-DIRECTOR-asn-visual-first-production` | `feature/asn-visual-first-production` | `ab91263` |

The owner's main checkout carries 11 uncommitted entries (modified `AGENTS.md`, `SKILL.md`,
`DESIGN-CONSTITUTION.md`, `README.md`, `templates/site-profile.json`; untracked
`GENERATIVE-TASTE-PROTOCOL.md`, `intelligence/generative-taste/`,
`projects/alpha-starts-now-visual-convergence/`, and three related template/test files).
**Left untouched by this audit.**

### Reviewed snapshots — verified, zero drift

| Ref | Expected | Actual | Result |
|---|---|---|---|
| `origin/main` | `416f95d3c1f715…` | `416f95d3c1f715…` | **MATCH** |
| `origin/feature/design-first-production-flow` | `d732a0ec657746…` | `d732a0ec657746…` | **MATCH** |
| feature ahead/behind main | 3 ahead / 0 behind | `0  3` (`rev-list --left-right --count`) | **MATCH** |

`projects/` inventory recalculated: **17 registered projects, 465 files** — matches the reviewed
figure. Frozen-integrity guard reported `465 files unchanged` on every suite run.

### The SKILL.md / module set actually available to the build

There is **no separate installed skill copy**; `SKILL.md` is repository-resident, so the effective
"loaded skill" is whatever the checked-out branch contains. That is the crux of Finding 1.

### Active project selection

Two non-frozen ASN efforts exist. Lineage established before use:

| Project | Location | Last write | State |
|---|---|---|---|
| `alpha-starts-now-visual-convergence` | owner's main checkout, **untracked** | 2026-09-05 22:15 | Screen prototypes; `OWNER_ACCEPTANCE = PENDING` |
| `alpha-starts-now-visual-first-production` | ASN worktree, committed `ab91263` | 2026-09-06 02:00 | **Latest — full 17-route production candidate** |

The production candidate is the audited build. It inherits the same owner-approved reference images
(identical SHA-256) from the convergence experiment. `WD-CURRENT-PREMIUM-001` was **not** used: no
such benchmark is present in either checkout, and no frozen pilot was substituted.

---

## 2. Video comparison basis — stated limitation

The transcript `Pasted text(20260907-020523).txt` was **not present** in the task attachments or the
authorized workspace. This audit therefore used **the supplied four-level synopsis only**.

**I did not watch the video and did not inspect its final site.** No claim below rests on anything
beyond the synopsis. The synopsis is used only as a workflow comparison (reference-led system →
custom graphics with a reference loop → typography in context → specific copy), never as a source of
required vendors, models, phase order, or conversion claims.

| Synopsis level | Website Director equivalent | State in the audited build |
|---|---|---|
| 1. Reference-led design system | `REFERENCE-PROTOCOL.md`, `DESIGN-SYSTEM-PROTOCOL.md` | Present and used — owner references captured with hashes |
| 2. Custom graphics + reference loop | `ASSET-DIRECTOR-PROTOCOL.md`, `WEBSITE-GAUNTLET-PROTOCOL.md` | Partially used; hero provenanced, 5 ritual plates unprovenanced |
| 3. Typography in context | `DESIGN-SYSTEM-PROTOCOL.md` | **Working well** — verified rendering, not just declared |
| 4. Specific copy | `content-truth-audit.md` | Audited, `PASS_WITH_OWNER_REVIEW` |

---

## 3. Ranked findings

Labels are report labels only, not lifecycle states.

---

### F1 — The active build branch never received the enforcement system
**`PROJECT_CONFIRMED`** · impact: critical · first-order cause of F2

The ASN production build branch descends from `feat/v2-10…` (`575e6b7`), **not** from `main`.

```
git rev-list --left-right --count origin/main...feat/v2-10-launch-post-launch-operations
17      1        # main has 17 commits v2-10 lacks; v2-10 has 1 doc commit

git merge-base --is-ancestor origin/feature/design-first-production-flow \
                             feature/asn-visual-first-production   -> false
```

Module presence by ref (`git ls-tree -r --name-only`):

| File | `origin/main` | `…/design-first-production-flow` | `feat/v2-10…` | `feature/asn-visual-first-production` |
|---|:--:|:--:|:--:|:--:|
| `framework_validation/owner_intent.py` | yes | yes | **no** | **no** |
| `framework_validation/cinematic_inspiration.py` | yes | yes | **no** | **no** |
| `framework_validation/design_first_flow.py` | no | yes | **no** | **no** |
| `schemas/owner-intent.schema.json` | yes | yes | **no** | **no** |
| `templates/alpha-starts-now-owner-intent.json` | yes | yes | **no** | **no** |

The ASN build tree contained **none** of the owner-intent, brand-authority, cinematic-inspiration or
design-first machinery. PR #5's enforcement and the full-homepage flow were not "bypassed" — they
were **physically absent**.

#### F1b — The QA harness the build actually ran is missing five checks outright

Following the audit instruction not to assume all copies match, the **working file** in the ASN
worktree was hashed rather than trusted. It is not the file audited on `main`:

| Copy | Bytes | sha256 (first 16) |
|---|---|---|
| ASN worktree `browser-qa/assertions/catalog.py` (**what the build ran**) | **31,838** | `44a23319f119198f` |
| `origin/main` `browser-qa/assertions/catalog.py` (what this audit read) | **65,580** | `b3e193405c3430bb` |

Its provenance is the v2-10 lineage, not a hand-stripped file: the committed
`feat/v2-10-launch-post-launch-operations` blob hashes `32ee945fe82c2e64`, and the working copy
differs from it by only **3 lines** (plus a 29-line tweak to `playwright_engine.py`). The diff
**adds nothing and removes no check function** — the checks were simply never on that branch.

Check functions **absent** from the harness the build ran:

- `check_motion`
- `check_brand_tokens`
- `check_observation_coverage` — the fail-closed "required plan fact was not emitted" guard
- `check_application`, `check_localization`

**This escalates F2 for this project.** It is not merely that the manifest failed to arm the checks;
**the checks did not exist in the harness that produced the 3332/3332 result.** Even a perfectly
authored manifest declaring `owner_intent` and `motion` would have produced nothing, because there
was no `check_motion` to call and no coverage guard to fail closed. Local file mtimes are
`2026-09-06 00:53:59`, i.e. from the original build session — **not** created by this audit.

---

### F2 — Owner requirements become optional QA when the plan is silent
**`PROJECT_CONFIRMED` + `REPRODUCED`** · impact: critical

Two enforcement entry points return `None` — a silent skip, not a block — before any owner contract
is consulted.

`browser-qa/assertions/catalog.py:492-494` (`check_motion`):
```python
cfg = _runtime_observation_cfg(plan, obs.route, "motion")
if not cfg.get("required") and not cfg.get("exercise"):
    return None
```
The owner-intent motion resolution sits at **lines 506-513, after this return** — so
`resolve_motion_requirement()` is unreachable whenever the plan omits its own `motion` block, **even
when `plan["owner_intent"]` demands `MOTION_LEVEL_3`.**

`browser-qa/assertions/catalog.py:458-460` (`check_brand_tokens`):
```python
owner_contract = plan.get("owner_intent")
if not isinstance(owner_contract, dict):
    return None
```

`_runtime_observation_cfg` states the intent plainly (`catalog.py:39-45`):
> *"No requirement is inferred when the plan is silent, preserving older manifests."*

That legacy-compatibility choice is defensible in isolation. The defect is that **nothing downstream
re-asserts a current owner requirement**, and `audit_owner_requirement_compliance()`
(`framework_validation/owner_intent.py:929`) is **never called by `browser-qa/runner.py`** — grep
confirms the runner imports only `cinematic_inspiration` (`runner.py:35`).

**The active project's manifest** (`qa/browser-qa-manifest.json`) contains **no** `owner_intent`,
`motion`, `visual_evidence`, `runtime_observations` or `observations` block. Consequence, measured
from the project's own final regression evidence:

| Check group | Count in `bqa-20260906T065932Z` |
|---|---|
| `motion.reduced-content-visible` / `reduced-nav-operable` | 238 |
| `motion.runtime-state-change` | **0** |
| `motion.sequence-coverage` | **0** |
| `motion.generic-fade-diversity` | **0** |
| `motion.real-browser-runtime` | **0** |
| `brand.current-palette` | **0** |
| `visual_evidence` block in evidence JSON | **`null`** |
| **Overall verdicts** | **`{'PASS': 3332}`, zero failures** |

The 238 "motion" checks verify only that the page still works **with animation switched off**.
Nothing verified that any animation exists. They come from `check_reduced_motion`, which **is**
present in the v2-10-era harness — see F1b for why `check_motion` and `check_brand_tokens` are not.

**Two independent causes, both proven.** For a *current* branch (`main`) the silent-skip in
`catalog.py:492` is the live defect — reproduced in R2. For *this project* the checks were absent
from the harness altogether (F1b). Repairing the silent skip is necessary but **not sufficient** for
ASN until the branch distribution issue (D-1) is resolved.

---

### F3 — The owner's cinematic requirement was downgraded by a project-local document
**`PROJECT_CONFIRMED`** · impact: critical · **the first broken handoff**

Owner contract — `templates/alpha-starts-now-owner-intent.json`, requirement `motion.owner-cinematic`:
> `"requirement": "The owner-required Alpha Starts Now direction is cinematic, animation-heavy, and sequence-driven."`
> `"minimum_motion_level": "MOTION_LEVEL_3"`, `"required_sequences": true`
> `"rationale": "Heuristic subtle motion cannot silently downgrade an explicit cinematic requirement."`

Project contract — `projects/alpha-starts-now-visual-first-production/VISUAL-CONTRACT.md` § *Motion contract*:
> *"Motion is limited to transform/opacity reveals and route/annotation emphasis. The full page remains
> complete with prefers-reduced-motion: reduce; no animation is required to understand the content."*

`resolve_motion_requirement()` run against the real contract returns
`execution_level: MOTION_LEVEL_3`, `downgrade_blocked: false`, `approved_downgrade: false` — i.e. **no
approved downgrade exists**. The scenario named verbatim in the owner's own rationale is exactly what
occurred, and the mechanism built to prevent it was absent from the branch (F1) and unarmed by the
manifest (F2).

**Measured implementation result** (isolated local server, real browser):

| Metric | Observed |
|---|---|
| CSS `@keyframes` rules at runtime | **0** |
| `animation:` declarations in `site.css` | **0** |
| `transition:` declarations | **5** (4 × `transform 180ms` hover, 1 × `.reveal` `opacity/transform 550ms`) |
| Distinct runtime motion families | **3** — `TRANS:all`, `TRANS:opacity`, `TRANS:transform` |
| GSAP / ScrollTrigger present | **false / false** |
| `.reveal` elements | 32 instances of **one** fade-and-translate pattern |

One generic fade/translate reveal, applied 32 times, against a contract requiring cinematic
sequence-driven motion. `motion.generic-fade-diversity` exists precisely to catch this and never ran.

---

### F4 — A static page that merely scrolls satisfies "meaningful state change"
**`REPRODUCED` + `PROJECT_CONFIRMED`** · impact: high

`browser-qa/assertions/catalog.py:530-535`:
```python
meaningful = [row for row in rows if row.get("meaningful_state_change") is True
              ...
              or any(float(row.get(key, 0) or 0) > 0.01
                     for key in ("max_geometry_delta", "max_opacity_delta", "scroll_delta")
```

`scroll_delta` is an ordinary consequence of scrolling any page of non-trivial height. Measured on the
real build: **`scrollDelta: 6156`** on a page with **zero keyframes and zero animations**.

Had `check_motion` run at level ≥ 2, `motion.runtime-state-change` would have reported **PASS** on
scroll position alone. The aggregate `bool(meaningful)` across all observations also means a single
qualifying row satisfies the whole route.

---

### F5 — Full-homepage surface names silently degrade to viewport captures
**`REPRODUCED` (source/integration)** · **not** project-confirmed · impact: high if the design-first flow ships

`browser-qa/runner.py:96`:
```python
default_capture = "FULL_PAGE" if surface_id.endswith("FULL_PAGE") else "VIEWPORT"
```

`framework_validation/design_first_flow.py:127-130` (feature branch):
```python
HOMEPAGE_REVIEW_SURFACES = ("DESKTOP_FULL_HOMEPAGE", "MOBILE_FULL_HOMEPAGE")
```

`"DESKTOP_FULL_HOMEPAGE".endswith("FULL_PAGE")` is **False**. **No alias or translation exists** —
`FULL_HOMEPAGE` appears nowhere in `runner.py`, `cinematic_inspiration.py` or `catalog.py` on either
branch (verified by grep). Reproduced result in R1: both design-first homepage surfaces generate
`capture=VIEWPORT`.

Concretely: the audited homepage is **9,763 px tall at a 1440 px viewport**. A viewport capture labelled
`DESKTOP_FULL_HOMEPAGE` would show **≈9%** of the page while satisfying a "full homepage reviewed" gate.

**Honest scope limit:** the active project is **not** affected. Its manifest sets no `visual_evidence`
block (`visual_evidence: null` in the evidence JSON), so this code path never executed. Its own
captures, produced by bespoke `qa/` scripts, are genuinely full-page — measured
`homepage-desktop.png` **1440×9781** and `homepage-mobile.png` **390×14311**. This is a latent defect
that would bite the first project to actually adopt the design-first flow.

---

### F6 — The production gate accepts declarations where evidence is implied
**`REPRODUCED`** · partially **`MITIGATED`** · impact: medium

`design_first_flow.py:528-557` — `validate_production_gate()` checks seven booleans plus the approval
object. It **does** call `validate_homepage_approval()` (line 551) — the source review's concern is
partly mitigated. But it never calls `validate_business_understanding()`,
`validate_homepage_design()` or `validate_design_system_derivation()`; their flags are simply trusted.

R4-C1 result: gate returns **PASS / `can_start_production: True`** with `RENDERED_SURFACES` supplied as
**bare strings and zero screenshot receipts**, while the same run's real design evidence would have
returned `FAIL` (homepage design) and `BLOCKED` (design-system derivation).

`cinematic_inspiration.py:340-347` — `_actual_screenshot()` validates metadata shape only: a truthy
`actual_rendered`, the literal `REAL_BROWSER`, a non-empty path string, and a 64-hex digest. It never
opens the file or recomputes the digest. R4-C2: `validate_rendered_visual_evidence()` returned **PASS**
on nine receipts whose files do not exist, with digests of 64 zeros.

**Mitigation, stated fairly:** when the runner produces the evidence it hashes real bytes
(`runner.py:414`, `hashlib.sha256(bytes(shot)).hexdigest()`), so runner-produced receipts are genuine.
The gap is that the validator cannot distinguish runner-produced from hand-authored evidence.

---

### F7 — Brand authority: never checked; a breach is *not* proven
**`NOT_VERIFIED` as a brand breach** · **`PROJECT_CONFIRMED`** as an absence of checking

Running the real ASN contract against the real built palette (R3) returns:
```
status: FAIL
UNAPPROVED_DOMINANT_BRAND_HUE: paper cream (role=page background)   [blocking: false]
```

**But this does not prove a brand violation, and I am not reporting one.** Area-weighted measurement of
the actually-rendered homepage shows dark navy surfaces slightly **dominant**:

| Rendered surface | Approx. painted area |
|---|---|
| `rgb(3,9,20)` + `rgb(11,24,48)` + `rgb(7,17,36)` — navy/ink | **≈ 8.79 M px²** |
| `rgb(244,239,230)` + `rgb(251,248,242)` + `rgb(227,218,203)` — cream family | ≈ 7.24 M px² |

The composition is a navy-dominant alternating field with a yellow accent (`--yellow: #ffc700`, 56
usages) and cream functioning as a **supporting light neutral** — a category the contract explicitly
permits. Whether that reads as "dominant cream" is an owner judgement, and the validator's
role-based classification may be over-sensitive here.

**The proven defect is the absence of the check, not a proven breach.** `BRAND_ALIGNMENT:
PASS_LOCAL_CANDIDATE` was asserted in `PREPRODUCTION-CERTIFICATION.md` while
`brand.current-palette` ran **zero** times.

---

## 4. What is working — do not "repair" these

Reported so the repair plan stays minimal and does not damage good work.

- **Typography is genuinely good, and verified, not declared.** `document.fonts.check()` confirms
  Bebas Neue, Plus Jakarta Sans and Space Mono all actually load and render; a canvas probe
  distinguishes real Bebas Neue (587 px) from the Impact fallback (769 px). `h1` renders at 172.8 px
  in the intended face. This is exactly synopsis level 3 done right.
- **Asset integrity is sound.** All 5 ritual plates plus logo and hero serve HTTP 200. An initial
  `8/9 images` reading was a lazy-loading measurement artifact, re-verified and **withdrawn** — not a defect.
- **An apparent blank cream section at y=4200 was a paint-timing artifact** of the headless pane.
  DOM inspection found 13 real elements in that band. **Withdrawn, not reported as a finding.**
- **The hero is strong** and faithfully carries the approved reference grammar (navy condensed display
  type, yellow route, brutalist architectural plate, tactile paper accents).
- **The certification is honest about deployment.** `OWNER_FINAL_ACCEPTANCE: PENDING`,
  `PRODUCTION_CERTIFICATION: NOT_GRANTED`, `DEPLOYMENT_READINESS: BLOCKED…`, `LIVE_SITE_CHANGED: NO`,
  `DEPLOYMENTS: 0`. **This truthful owner status is preserved by this audit.**
- **Accessibility, links, SEO, security and responsive QA are real and thorough** — 490 links checked,
  0 broken; 34 semantic checks across 17 routes.

---

## 5. Reference-fidelity trace — largest visible gap

```
reference/source observation   Owner-selected concept art: tactile field-manual collage,
                               navy condensed display type, yellow route, brutalist plate
                               (evidence/approved-references/, sha256 56dfc0cf…, 5ebff859…)
        |
        v
transferable principle         Editorial asymmetry; the yellow route as a *progression device*
                               that connects stage -> ritual -> threshold -> CTA
        |
        v
client interpretation          VISUAL-CONTRACT.md § Section translation — a per-section route
                               meaning table. Faithful and specific.
        |
        v
approved homepage region       Hero + 7 sections, all mapped in that table
        |
        v
implementation                 site/styles/site.css + site/scripts/site.js
                               -> one IntersectionObserver adding .is-visible to 32 .reveal nodes
        |
        v
current browser evidence       0 keyframes · 3 transition families · no GSAP · scrollDelta 6156
        |
        v
critic finding                 NONE — motion.* runtime checks never ran (F2)
        |
        v
owner decision                 PENDING; owner never shown that the route "progression device"
                               is static, nor that MOTION_LEVEL_3 was reduced to a fade
```

**Gap assignment:** briefing — clear · reference interpretation — clear · concept quality — clear ·
asset production — partial (5 unprovenanced ritual plates, already disclosed) ·
typography/copy — clear · **implementation drift — clear; the build is faithful to its contract** ·
**review evidence — AT FAULT; the contract itself was wrong and nothing compared it to owner intent** ·
acceptance — correctly withheld.

The concept is good and the implementation is faithful. **The failure is a contract substitution that
no review stage compared back to the owner's standing requirement.**

---

## 6. Status register

| Register | Status |
|---|---|
| `SOURCE_REVIEW` | COMPLETE — snapshots verified, zero drift |
| `LOCAL_RUNTIME_IDENTITY` | COMPLETE — 3 worktrees mapped; build branch 17 commits behind main |
| `UNIT_TESTS` | PASS — `owner_intent` 18/18, `cinematic_inspiration` 20/20, `v2_8_browser_qa` 89/89, `design_first_production_flow` **24/24** (registered at `schemas/test-suites.json:292`) |
| `INTEGRATION_REPRODUCTIONS` | 4 of 4 reproduced (R1, R2, R3, R4) |
| `REAL_BROWSER_REVIEW` | PARTIAL — DOM/runtime/font/asset measurement complete; **static screenshot capture was unreliable** in the headless pane (paint timeouts). No screenshot is presented as approval evidence. |
| `REFERENCE_FIDELITY` | Traced; largest gap = motion contract substitution |
| `OWNER_VISUAL_ACCEPTANCE` | **PENDING — unchanged.** Owner approved *visual direction preference only* (per `reference-manifest.json` `approval_scope`). No implementation acceptance exists or was created. |
| `PROTECTED_PATH_INTEGRITY` | **PASS — 465 files unchanged**, confirmed by `FrozenIntegrityGuard` on every suite run |
| `PRODUCTION_CHANGES` | **NONE** |

---

## 7. Deferred / not investigated

- The owner's main checkout contains an untracked `GENERATIVE-TASTE-PROTOCOL.md` and
  `intelligence/generative-taste/` subsystem plus a modified `SKILL.md`. Not in scope; not read
  beyond `git status`. It may already address parts of F3.
- The 5 ritual plates lack provenance records (`ASSET_PROVENANCE: PARTIAL`). Already disclosed by
  the project; requires human review, not a code repair.
- `projects/alpha-starts-now-visual-convergence` (untracked) was used only to establish lineage.
