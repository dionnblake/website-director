# V2.10 Launch & Post-Launch Operations — Integration Validation Suite

> Companion to `tests/test_v2_10_launch_operations.py`. Every scenario below is a
> **negative control** executed by that suite against synthetic in-memory fixtures
> and the deterministic validators in `launch-ops/validator.py`. No project under
> `projects/` is read or written; a `FrozenIntegrityGuard` wraps the run.
>
> **Run:** `python tests/test_v2_10_launch_operations.py` (exit 0 = pass)

---

## 1. What this proves

1. **One canonical launch authority.** `LAUNCH-OPERATIONS-PROTOCOL.md` is the only
   `*PROTOCOL.md` at the repo root matching `LAUNCH|DEPLOY|RELEASE`. Release/deployment
   logic in `PRODUCTION-CHECKLIST.md`, `CLIENT-CMS-HANDOFF-PROTOCOL.md`, and
   `BROWSER-REGRESSION-QA-PROTOCOL.md` is reconciled to consume or defer to it.
2. **One completion flag.** `launch_ops.complete` is the sole readiness flag for
   `[RELEASE_READY]`. `launch_ops{}` carries no lock boolean. Exactly five owner
   locks remain; none contains `launch` / `deploy` / `rollback` / `release`.
3. **Four permanently distinct facts.** `complete` (plan done) ≠ `deployed` ≠
   `production_*_verified` ≠ `stabilization_complete`.
4. **`RELEASE_READY` is not `DEPLOYMENT_AUTHORIZED`.** Deployment authorization is
   an explicit per-release owner act; it is never inferred from QA, a build, a
   design approval, "looks good", a prior project, or a previous release.
5. **Production verification verifies a known release identity on the production
   surface.** A localhost or staging manifest never sets `production_verified`.
6. **The state machine rejects impossible transitions.**
7. **Website Director deploys nothing.** No launch/deploy runner was created;
   production Browser QA reuses the V2.8 harness in `environment = "production"`.

---

## 2. State machine

| Transition | Expected | Observed |
| :-- | :-- | :-- |
| `NOT_EVALUATED → PLANNING` | legal | PASS |
| `NOT_EVALUATED → STABILIZED` | rejected | FAIL (impossible jump) |
| `RELEASE_READY → PRODUCTION_VERIFIED` | rejected | FAIL |
| `PLANNING → DEPLOYED` | rejected | FAIL |
| Full forward path `NOT_EVALUATED → … → STABILIZED` | legal end-to-end | PASS |
| `DEPLOYED → ROLLBACK_REQUIRED` | legal | PASS |
| `ROLLBACK_REQUIRED → ROLLED_BACK` | legal | PASS |

---

## 3. Scenario matrix (A–R)

| # | Scenario | Expected | Observed |
| :-- | :--- | :--- | :--- |
| A | Local QA passed, never deployed | `release_candidate_ready = true`, `deployed = false`, `production_verified` unreachable (`BLOCKED` — no authorization yet) | PASS |
| B | Deployment inferred from QA / Gauntlet pass | **FAIL** | FAIL |
| B′ | `deployment_authorized = true` with no reference / durable policy | **FAIL** | FAIL |
| B″ | Explicit per-release owner authorization reference | **PASS** | PASS |
| C | `deployed_sha != release_sha` | production verification **FAIL** | FAIL |
| C′ | Deployed identity unprovable | **BLOCKED** (`DEPLOYED_IDENTITY = UNVERIFIED`), never assumed | BLOCKED |
| D | HTTPS failure on production | **FAIL** | FAIL |
| E | HTTP → HTTPS redirect correct | **PASS** | PASS |
| F | Production still carries staging `noindex` | SEO launch **FAIL** | FAIL |
| G | Production canonical points to `localhost` | **FAIL** | FAIL |
| H | Analytics missing in production | measurement production verification **FAIL** | FAIL |
| I | Analytics fires a duplicate conversion | **FAIL** | FAIL |
| J | Consent-dependent analytics fires before consent | **FAIL** | FAIL |
| K | Production form endpoint misconfigured | **FAIL** without sending a real customer submission | FAIL |
| K′ | Real production submission with no production-test authorization | **FAIL** | FAIL |
| L | Critical asset missing on production | **FAIL** | FAIL |
| M | Staging passes every check | `production_verified = false`; staging manifest flagged not-production | PASS |
| N | Rollback plan absent where rollback is required | release readiness **FAIL** (`launch.rollback_ready`) | FAIL |
| N′ | Rollback genuinely not required | `NOT_APPLICABLE`, gate not blocked | PASS |
| O | Post-launch `SEV0` incident (`site_unavailable`) | `ROLLBACK_REQUIRED` per explicit trigger | FAIL → ROLLBACK_REQUIRED |
| O′ | Cosmetic production discrepancy | below threshold — triage, not rollback | PASS |
| P | Browser QA evidence tagged `environment=local` inside a production manifest | framework validation **FAIL** | FAIL |
| Q | Sixth owner lock (`launch`/`deploy`/`rollback`) | **FAIL** — exactly five canonical locks | FAIL (rejected) |
| R | Frozen fixture mutation during the run | V2.8 `FrozenIntegrityGuard` **FAIL**; a later restore does not launder it | FAIL, file named |

---

## 4. Cross-document wiring verified

- `SKILL.md` — Phase 12.25, `GATE LAUNCH: [RELEASE_READY]`, §5.17 SoT rule, version ≥ 2.10.0, `RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED`, five-lock invariant restated.
- `IMPLEMENTATION-CONTRACT.md` — §2.9 Builder & Release-Operator Launch Requirements, prohibitions 40–46, version ≥ 1.7.0.
- `PRODUCTION-CHECKLIST.md` — §11 Launch & Post-Launch Operations Boundary, Phase 12 = candidate readiness only, version ≥ 1.7.0.
- `CLIENT-CMS-HANDOFF-PROTOCOL.md` — §13 Launch Operations Intake; `handoff_transferred`.
- `BROWSER-REGRESSION-QA-PROTOCOL.md` §22 — V2.10 production-mode reuse note (no second runner).
- `README.md`, `AGENTS.md` — V2.10 subsystem documented; AGENTS.md version ≥ 2.10.0.
- `templates/site-profile.json` — `schema_version = 2.10.0`, `launch_ops{}` ships neutral.
- `examples/test_runner.py` — `2.10.0` recognised; `launch`/`deploy`/`rollback`/`release` added to the forbidden-lock substrings; `launch_ops{}` neutrality asserted.

---

## 5. No external side effects

The suite and the validators perform no network access, launch no browser,
deploy nothing, alter no DNS, submit no forms, send no email, create no
analytics conversions, and write nothing under `projects/`. All fixtures are
in-memory dicts and temp state.
