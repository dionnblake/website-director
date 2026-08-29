# LAUNCH & POST-LAUNCH OPERATIONS PROTOCOL

> **Version:** 1.0.0 (Website Director V2.10.0 Subsystem)
> **Status:** Mandatory — governs the transition from production candidate to verified, stabilised launch.
> **Governance:** Website Director Orchestration Rail (`SKILL.md` §2), Phase 12.25.
> **Readiness Gate:** `[RELEASE_READY]` — a readiness gate, **not** a sixth owner/design lock.
> **Boundary with V2.5:** `CLIENT-CMS-HANDOFF-PROTOCOL.md` remains the authority for long-term client ownership, CMS operations, maintenance, documentation, and transfer. This protocol owns only release planning, launch authorization boundaries, deployment readiness, production verification, early post-launch observation, rollback readiness, and launch closeout — then hands its outputs to V2.5.
> **Website Director does not deploy.** It prepares plans, manifests, commands, and verification steps. Deployment is an external side effect performed by the owner or an owner-authorised operator.

---

## 1. Why this exists — states Website Director used to conflate

Website Director could already take a project to a strong **production candidate**. It could not distinguish that candidate from a *deployed* site, a deployed site from a *production-verified* site, or a production-verified site from a *stabilised* one. Those are different facts:

```text
LOCAL BUILD
    ↓  (Phase 10 + Phase 10.5 + Phase 11 + Phase 11.5 + Phase 12)
RELEASE CANDIDATE
    ↓  GATE LAUNCH: [RELEASE_READY]   (launch_ops.complete — a PLAN is complete)
DEPLOYMENT AUTHORIZATION             (explicit owner act, per release)
    ↓
PRODUCTION DEPLOYMENT                (external side effect — not performed here)
    ↓
PRODUCTION VERIFICATION              (against a known release identity, on the production surface)
    ↓
POST-LAUNCH STABILITY               (early observation window; incidents; rollback readiness)
    ↓
OPERATIONS / HANDOFF                (Phase 12.5 — V2.5 owns this)
```

**A local build passing QA does NOT mean the site is deployed. A deployed site does NOT mean production verification passed. A production verification pass does NOT mean the site is stable after launch.** This protocol makes each of those a separately recorded state.

---

## 2. Overlap reconciliation — one canonical authority

Release/deployment/launch logic previously lived, partially, in several places. This protocol is now the **single canonical authority** for the launch boundary; the others are reconciled to consume or defer to it:

| Existing surface | Was | Now |
| :--- | :--- | :--- |
| `PRODUCTION-CHECKLIST.md` §9–§10 ("Deployment Authorization", "Deployment Integrity") | Pre-flight checklist implied deployment sign-off | Phase 12 stays **pre-deployment readiness**. "Authorized for deployment" in Phase 12 means the candidate is `RELEASE_READY` — it is **not** `DEPLOYMENT_AUTHORIZED`. See `PRODUCTION-CHECKLIST.md` §11. |
| `CLIENT-CMS-HANDOFF-PROTOCOL.md` `RELEASE-RUNBOOK.md`, `ENVIRONMENT-INVENTORY.md`, `DIGITAL-OWNERSHIP-REGISTER.md`, backup/restore proof | V2.5 handoff documents | **Consumed, not duplicated.** Launch Operations reads the environment inventory and ownership register; it does not create a second inventory. It hands the final launch record into V2.5 intake (`CLIENT-CMS-HANDOFF-PROTOCOL.md` §13). |
| `BROWSER-REGRESSION-QA-PROTOCOL.md` (V2.8) | `environment = "local"` / `"production"` already supported by `browser-qa/runner.py` | **Reused as-is.** Production Browser QA is the same harness in `environment = "production"` mode. No second runner. |
| `SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md` (V2.7), `ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md` (V2.9), `CONVERSION-ANALYTICS-PROTOCOL.md` (V2.6), `SEO-INTELLIGENCE-PROTOCOL.md` (V1.2) | Define requirements; carry `implementation_verified` / `production_verified` fields | **Owning specs unchanged.** Launch Operations verifies *deployment realisation* of their requirements and writes only its own launch-side evidence references. A production discrepancy returns to the owning specification (§45). |
| Historical release worktree / release-notes conventions in `projects/` | Ad hoc per pilot | Superseded for materially reopened / new projects by `templates/launch-plan.md` and `templates/launch-evidence-manifest.json`. Historical artifacts remain valid historical evidence (§52). |

**Boundary rule (explicit):** V2.5 Handoff owns *long-term* operations. Launch Operations owns the *launch event and its immediate aftermath*. They meet exactly once, at Phase 12.25 → Phase 12.5 intake.

---

## 3. Phase placement & the gate

```text
PHASE 10     IMPLEMENTATION BUILD
   ↓
PHASE 10.5   BROWSER / REGRESSION QA            → [BROWSER_QA_PASS]
   ↓
PHASE 11     DESIGN QA / IMPECCABLE
   ↓
PHASE 11.5   WEBSITE GAUNTLET                   → [GAUNTLET_PASS | CAP_REACHED]
   ↓
PHASE 12     PRODUCTION PRE-FLIGHT VERIFICATION (candidate readiness)
   ↓
PHASE 12.25  LAUNCH & PRODUCTION OPERATIONS
   ↓         GATE LAUNCH: [RELEASE_READY]       (launch_ops.complete)
   ↓
             DEPLOYMENT AUTHORIZATION            (explicit owner act — external)
   ↓
             PRODUCTION DEPLOYMENT               (external — not performed here)
   ↓
             PRODUCTION VERIFICATION             (browser-qa environment=production + delegated re-checks)
   ↓
             POST-LAUNCH OBSERVATION / STABILIZATION
   ↓
PHASE 12.5   CLIENT CMS / OPERATIONS / HANDOFF  → [CLIENT_HANDOFF_READY | NOT_REQ]
```

`[RELEASE_READY]` is a **readiness gate**, categorically like `[BROWSER_QA_PASS]` and `[ACCESSIBILITY_READY]` — not a member of `locks{}`. It certifies: *the release/launch plan is complete and the candidate is ready to request deployment authorization.* It does **not** mean deployed. It does **not** mean production verified.

Historical phases are **not** renumbered. `12.25` is chosen so it slots cleanly after Phase 12 pre-flight and before Phase 12.5 handoff.

---

## 4. Owner deployment authority

Deployment is an external side effect. Website Director distinguishes:

```text
RELEASE_READY   ≠   DEPLOYMENT_AUTHORIZED
```

**Only explicit owner authorization permits deployment.** The framework may prepare commands, manifests, plans, and verification steps. It may **not** infer deployment permission from:

- passing QA (Phase 10.5, Phase 11, Phase 11.5)
- a completed implementation
- an approved design
- an owner saying *"looks good"* about the candidate
- prior authorization on another project
- a previous release of this project

Each production deployment requires its own explicit authorization **unless a separate durable deployment policy exists** — recorded, owner-approved, and scoped (e.g. *"pushes to `main` auto-deploy to production for this project"*). Absent that policy, `launch_ops.deployment_authorized` may be set `true` only with an authorization reference (`deployment_authorization_ref` / `authorized_by` + timestamp).

`launch-ops/validator.py` → `evaluate_deployment_authorization()` enforces this: an `explicit=true` flag with no reference and no durable policy is a **FAIL**; a request that leans on any non-authorizing signal is a **FAIL**; the absence of authorization is **BLOCKED**.

**Website Director performs no deployment in this phase, ever.**

---

## 5. Canonical protocol scope

This protocol governs:

release candidate preparation · deployment planning · environment readiness · owner authorization boundary · launch freeze · release identity · production deployment verification · DNS/domain verification · TLS/HTTPS · redirects · cache/CDN behaviour · production browser QA · production accessibility verification · production security/privacy verification · production analytics verification · SEO launch verification · form/integration verification · error monitoring readiness · rollback plan · post-launch observation · incident triage · stabilization · handoff transition.

It does **not** make Website Director an autonomous deployment platform, a monitoring vendor, an uptime service, or a legal-compliance authority.

---

## 6. Canonical state — `site-profile.json` → `launch_ops{}`

```jsonc
"launch_ops": {
  "complete": false,                         // SOLE readiness flag for [RELEASE_READY]
  "status": "NOT_EVALUATED",                 // §7 status model
  "release_candidate_ready": false,
  "release_sha": null,
  "release_version": null,
  "build_id": null,
  "build_timestamp": null,
  "deployment_target": null,                 // §10 vendor-neutral class
  "deployment_provider": null,               // concrete provider, only if known
  "production_domain": null,                 // §38 single canonical production URL
  "environment_ready": false,
  "deployment_authorized": false,            // §4 — explicit owner act only
  "deployment_authorization_ref": null,
  "durable_deployment_policy": false,
  "deployed": false,
  "deployed_at": null,
  "deployed_sha": null,                      // §36 — actual deployed identity
  "production_browser_verified": false,
  "production_accessibility_verified": false,
  "production_security_privacy_verified": false,
  "production_measurement_verified": false,
  "production_seo_verified": false,
  "production_forms_verified": false,
  "monitoring_requirement": "NOT_EVALUATED", // NOT_REQUIRED | BASIC_REQUIRED | APPLICATION_MONITORING_REQUIRED
  "monitoring_ready": false,
  "rollback_ready": false,                   // §25 — plan defined
  "rollback_tested": false,                  // §26 — separate, stronger state
  "post_launch_status": "NOT_STARTED",       // NOT_STARTED | OBSERVING | STABLE | INCIDENT_OPEN
  "observation_window": { "policy": null, "start": null, "expected_end": null },
  "known_incidents": [],                     // §30 append-only
  "stabilization_complete": false,
  "release_notes_ref": null,
  "handoff_transferred": false,
  "blocked_reason": null,
  "exception": { "applied": false, "reason": null }
}
```

### 6.1 Required invariant

`launch_ops.complete` is the **sole readiness flag** for the planning gate `[RELEASE_READY]`. It means: *the release/launch plan is complete and the candidate is ready to request deployment authorization.*

- It does **NOT** mean deployed. Use `launch_ops.deployed`.
- It does **NOT** mean production verified. Use `production_browser_verified` / `production_security_privacy_verified` / `production_measurement_verified` / `production_seo_verified` / `production_accessibility_verified` / `production_forms_verified`.
- It does **NOT** mean stabilised. Use `stabilization_complete` and `post_launch_status`.

No second, independently-writable completion flag may ever be created for launch readiness. `launch_ops{}` contains **no lock boolean**.

---

## 7. Status model

```text
NOT_EVALUATED
PLANNING
BLOCKED
RELEASE_READY
AWAITING_DEPLOYMENT_AUTHORIZATION
DEPLOYMENT_AUTHORIZED
DEPLOYING
DEPLOYED
PRODUCTION_VERIFICATION_RUNNING
PRODUCTION_VERIFICATION_FAILED
PRODUCTION_VERIFIED
POST_LAUNCH_MONITORING
STABILIZED
ROLLBACK_REQUIRED
ROLLED_BACK
EXCEPTION_APPLIED
```

These are **not** collapsed into a single boolean. `launch_ops.status` is authoritative inside `launch_ops{}` only.

---

## 8. Release identity

Every launch candidate has an **immutable identity**. Record, at minimum:

```text
PROJECT
RELEASE_VERSION
GIT_SHA
BRANCH
BUILD_ID
BUILD_TIMESTAMP
ENVIRONMENT
DEPLOYMENT_TARGET
```

Where applicable also record:

```text
ASSET_MANIFEST_ID        (asset-manifest.json digest)
BROWSER_QA_RUN_ID        (browser_qa evidence run_id)
ACCESSIBILITY_RUN_ID
SECURITY_REVIEW_ID       (security-privacy-register.json digest / review version)
MEASUREMENT_PLAN_VERSION (measurement.event_schema_version)
```

**Production verification traces back to the exact deployed artifact.** Never verify "whatever is currently on the server" — verify a known release identity (§36).

---

## 9. Release candidate freeze

Once a candidate enters final launch verification (`status` = `RELEASE_READY` or later, before authorization):

- no untracked implementation changes
- no silent asset replacement
- no silent copy edits
- no silent analytics changes
- no dependency upgrades
- no new scripts
- no production-only hacks

Any change after freeze **creates a new release candidate identity** (new `release_sha` / `build_id`) or **explicitly updates the release candidate before authorization** with a recorded reason. A dirty release candidate must never be authorised or deployed.

---

## 10. Deployment target inventory (vendor-neutral)

Record the deployment architecture class — only what is known:

```text
STATIC_HOST · NETLIFY · VERCEL · CLOUDFLARE · AWS · AZURE · GCP ·
TRADITIONAL_WEB_HOST · CONTAINER_PLATFORM · CUSTOM_SERVER · OTHER
```

Do not fabricate provider details (regions, plan tiers, account ids). The subsystem is vendor-neutral; provider-specific adapters may exist later but are **not** in scope for V2.10.

---

## 11. Environment readiness

Before `[RELEASE_READY]`, verify applicable environment requirements — **consuming the V2.5 `ENVIRONMENT-INVENTORY.md`, not duplicating it**:

- production environment identified
- required environment variables identified (names only — never values)
- no development API endpoints; no `localhost` references; no mock services
- production API origin known
- analytics environment / property known (from `measurement{}`)
- consent configuration known (from `security_privacy{}`)
- email / form destination known
- storage / CDN location known
- runtime version known
- build command known
- output directory known
- production secrets expected but **not embedded** (§ security)

`launch_ops.environment_ready = true` records this determination.

---

## 12. Domain / DNS plan

Where a custom domain exists, record: canonical domain · www policy · apex policy · DNS provider · deployment target · required DNS records · redirect requirements · ownership/authorization boundary (cross-reference `DIGITAL-OWNERSHIP-REGISTER.md`).

**Do not change DNS in this phase.** Production verification (§36+) later checks *actual* resolved behaviour.

---

## 13. HTTPS / TLS

Consume Security/Privacy transport requirements (`SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md`). Production verification must check, on the production surface:

- HTTPS active
- HTTP redirects appropriately (to the canonical HTTPS origin)
- no mixed content
- correct canonical scheme
- certificate valid in a browser context; no obvious certificate errors
- secure-cookie assumptions hold where applicable

**Never claim TLS configuration verification from localhost.** Local development over HTTP is not a defect.

---

## 14. Redirect governance

Create an explicit redirect plan where applicable and verify deployed behaviour:

- HTTP → HTTPS
- www ↔ apex canonical behaviour
- old URL migrations; renamed pages; deleted content routes
- trailing-slash behaviour if relevant
- legacy campaign URLs
- 404 behaviour (custom, helpful, in design system)

Avoid redirect **chains and loops**. SEO authority (`SEO-INTELLIGENCE-PROTOCOL.md`) owns SEO *intent*; Launch Operations owns deployed *redirect verification*.

---

## 15. Production browser QA

Consume the canonical V2.8 Browser QA harness. **Do not create another browser runner.** Production launch verification runs the same `browser-qa/runner.py` with the manifest's `environment` set to `"production"` (or `https://` routes), executing the **production-safe subset**.

```text
LOCAL_BROWSER_QA_PASS   ≠   PRODUCTION_BROWSER_QA_PASS
```

- Production tests avoid destructive actions.
- **Do not submit real forms** unless explicit production-test authorization exists (§20).
- Prefer synthetic / non-destructive health checks.
- `browser_qa.production_verified` is set only by a real-browser run against the real production URL; a localhost run never sets it (V2.8 invariant, unchanged).

`launch_ops.production_browser_verified` mirrors that determination on the launch side.

---

## 16. Production accessibility verification

Consume V2.9 Accessibility Intelligence. Production verification re-checks browser-observable accessibility surfaces that **can differ after deployment**: fonts · focus behaviour · route transitions · consent UI · media · third-party widgets · production rendering · production CSS/assets.

- Do **not** automatically repeat every manual accessibility test if nothing changed.
- Do **not** assume local evidence proves production when production introduces different assets/scripts/configuration.

The result updates only the launch-side `launch_ops.production_accessibility_verified` and the canonical `accessibility.production_verified` field (single source of truth discipline, §41). No second accessibility state machine.

---

## 17. Production security / privacy verification

Consume canonical V2.7 Security/Privacy. Verify production-observable items: security headers · HTTPS · cookie behaviour · third-party scripts (runtime set matches the approved inventory) · consent behaviour · privacy/disclosure routes resolve · analytics activation behaviour · mixed content · secret exposure in client surfaces.

- **Do not perform intrusive security testing.**
- **Do not claim legal compliance.** `security_privacy.compliance_certified` stays permanently `false`.

A production discrepancy returns to `SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md`, not a silent launch-side fix (§45).

---

## 18. Production measurement verification

Consume canonical `measurement{}`. After deployment, verify where applicable:

- analytics library loads
- correct environment / property / config
- page-view behaviour (one `page_view` per route settle)
- critical CTA events
- **no duplicate events**
- no PII
- affiliate events (click ≠ conversion ≠ commission)
- conversion-success correctness (server-confirmed, not click)
- UTM preservation
- consent gating (nothing fires before consent where consent is `REQUIRED`)

Use **synthetic / non-customer test data**. Do not generate misleading real conversions where avoidable; flag test traffic where the provider supports it. Result → `launch_ops.production_measurement_verified` and `measurement.production_verified`.

---

## 19. SEO launch verification

Consume canonical SEO artifacts. Verify where applicable, **on production**:

- production `<title>` / description / canonical
- robots directives / meta-robots
- sitemap correctness
- indexability — **no accidental staging `noindex`**
- structured data validity
- production URLs (no `localhost` / staging canonical)
- redirect behaviour
- Open Graph URLs / images resolve
- 404 handling

**Do not submit Search Console changes or indexing requests in this phase.** Define readiness only. Result → `launch_ops.production_seo_verified`.

---

## 20. Form / integration verification

Verify production configuration **without creating side effects** where possible:

```text
ENDPOINT_EXISTS · CONFIG_PRESENT · VALIDATION_ACTIVE · ANTI_SPAM_PRESENT ·
SUCCESS_PATH_CONFIGURED · FAILURE_PATH_CONFIGURED
```

**Actual production submission requires explicit owner authorization** if it sends: email · CRM records · support tickets · orders · analytics conversions · third-party API actions. Record `production_test_authorized = true` and the authorising reference before any real submission.

**Never silently generate production records.** Result → `launch_ops.production_forms_verified`.

---

## 21. Cache / CDN verification

Where applicable, verify: stale asset risk · fingerprinted assets · correct cache headers · HTML cache behaviour · old JS/CSS not served unexpectedly · invalidation/purge plan known · CDN origin correct.

Do **not** impose one universal cache strategy.

---

## 22. Production asset verification

Verify critical deployed assets: hero · logos · fonts · favicon · social preview · critical video · generated imagery · responsive assets. Ensure deployment did not omit assets or ship local filesystem paths (`file://`, `assets/source/…`, unresolved `/@fs/…`).

---

## 23. Error monitoring readiness

Website Director determines **whether monitoring is required** and the **minimum appropriate coverage**. Categories: runtime errors · server errors · failed requests · form failures · deployment health · uptime · performance regressions.

```text
NOT_REQUIRED                       (simple static site)
BASIC_REQUIRED                     (uptime / deploy health / form-failure signal)
APPLICATION_MONITORING_REQUIRED    (auth, payments, dynamic app surfaces)
```

A paid monitoring vendor is **not** required for every small static site. Vendor choice stays conditional and owner-decided. `launch_ops.monitoring_requirement` records the determination; `monitoring_ready` records that the required minimum is in place or planned with an owner.

---

## 24. Logging boundary

Where server/app logging exists: no secrets · no unnecessary personal data · no raw passwords · no payment data · no analytics PII · useful request/error identifiers · retention **UNKNOWN stays UNKNOWN**. `SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md` remains authority over sensitive-logging requirements — Launch Operations only checks realisation.

---

## 25. Rollback plan

Every meaningful production deployment requires a defined rollback approach. Record: last known good release · rollback mechanism · rollback owner · required credentials/location (names, not values) · data-migration implications · cache implications · DNS implications (if any) · rollback verification procedure.

**Rollback readiness (`rollback_ready`) must be established before deployment authorization where practical.** `launch-ops/validator.py` → `evaluate_release_readiness(rollback_required=True)` fails the gate when `rollback_ready` is false.

---

## 26. Rollback testing

```text
ROLLBACK_PLAN_DEFINED   ≠   ROLLBACK_TESTED
```

Testing may be local · staging · platform preview · synthetic. **Do not execute a destructive production rollback in this phase.** For simple immutable static hosting, rollback may be *restoration of the previous deployment/version* — document the exact mechanism. `launch_ops.rollback_tested` is a separate, stronger flag from `rollback_ready`.

---

## 27. Rollback triggers

Define **concrete** criteria — never "rollback if something looks bad":

| Trigger | Default severity |
| :--- | :--- |
| site unavailable | `SEV0_CRITICAL` |
| critical route failure | `SEV0_CRITICAL` |
| checkout / payment failure | `SEV0_CRITICAL` |
| authentication failure | `SEV0_CRITICAL` |
| sensitive-data exposure | `SEV0_CRITICAL` |
| broken primary conversion | `SEV1_HIGH` |
| severe JS errors (widespread) | `SEV1_HIGH` |
| privacy/security regression | `SEV1_HIGH` |
| accessibility blocker introduced | `SEV1_HIGH` |
| severe visual break across core routes | `SEV1_HIGH` |
| production build identity mismatch | `SEV1_HIGH` |
| secondary feature failure | `SEV2_MODERATE` |
| isolated route issue | `SEV2_MODERATE` |
| cosmetic production discrepancy | `SEV3_LOW` |

`evaluate_rollback_trigger()` returns **FAIL → ROLLBACK_REQUIRED** for any `SEV0`/`SEV1` incident; `SEV2`/`SEV3` are triaged, not rolled back. Projects may override the map.

---

## 28. Post-launch observation window

Define an appropriate early observation period — **do not hardcode one duration for every site**:

```text
STATIC_SITE   = short verification window (hours)
LEAD_GEN      = first-meaningful-traffic / first-form window (1–3 days)
SAAS          = extended operational window (1–2 weeks)
ECOMMERCE     = transaction-sensitive window (spanning a full business cycle)
```

Record: start · expected end · signals observed · incidents · conversion anomalies · error anomalies · production performance anomalies. **No background monitoring is required by this architecture task — this is protocol definition.** The window is an owner-observed period with a checklist, not a Website Director daemon.

---

## 29. Incident model

```text
SEV0_CRITICAL · SEV1_HIGH · SEV2_MODERATE · SEV3_LOW
```

| Severity | Examples |
| :--- | :--- |
| **Critical** | site unavailable; payment/auth completely broken; sensitive-data exposure |
| **High** | primary conversion unavailable; widespread JS failure; severe accessibility blocker |
| **Moderate** | secondary feature failure; isolated route issue |
| **Low** | cosmetic production discrepancy; minor non-blocking issue |

**Do not inflate every defect into an incident.** A cosmetic discrepancy is a backlog item, not a `SEV`.

---

## 30. Incident evidence

Each launch incident captures (append-only — never overwrite history on resolution):

```text
INCIDENT_ID · RELEASE_SHA · TIME · ENVIRONMENT · ROUTE · SYMPTOM · SEVERITY ·
EVIDENCE · LIKELY_OWNER · ACTION · RESOLUTION · ROLLBACK_REQUIRED
```

Stored in `launch_ops.known_incidents[]` and in `templates/launch-plan.md` §22.

---

## 31. Post-launch conversion sanity

Consume measurement architecture. Post-launch operations may check whether critical signals are **plausible**: events arriving · no duplicate explosion · CTA tracking active · affiliate clicks recorded · form-success events correspond to real success.

- Do **NOT** declare a conversion strategy successful based on tiny early samples.
- Do **NOT** make optimization decisions here — CRO authority (`CONVERSION-ANALYTICS-PROTOCOL.md` §14) remains separate.

---

## 32. Production performance sanity

Consume existing performance requirements (`PRODUCTION-CHECKLIST.md` §4). Verify production **synthetic** evidence where practical: LCP · CLS · INP proxy / synthetic interaction performance · asset weight · route behaviour.

```text
SYNTHETIC   ≠   FIELD_DATA
```

Never represent synthetic measurements as real-user Core Web Vitals.

---

## 33. Release notes

Create a release summary artifact (`templates/launch-plan.md` §25 or a standalone `RELEASE-NOTES.md`), recording: release identity · major changes · known limitations · migrations · operational changes · analytics changes · security/privacy changes · accessibility changes · rollback reference. **Do not expose secrets.**

---

## 34. Working artifacts

| Artifact | Purpose |
| :--- | :--- |
| `templates/launch-plan.md` | 26-section human-readable launch plan (§34.1). References/consumes V2.5, V2.6–V2.9 artifacts rather than duplicating their data. |
| `templates/launch-evidence-manifest.json` | Machine-readable evidence, tied to a release identity (§35). |
| `launch-ops/validator.py` | Deterministic state-machine + readiness + authorization + production-verification + rollback-trigger checks. |
| `browser-qa/` (`environment = "production"`) | Production browser QA — the V2.8 harness, unchanged. |

### 34.1 `launch-plan.md` required sections

1. Release Identity · 2. Deployment Target · 3. Environment Readiness · 4. Domain / DNS Plan · 5. HTTPS / TLS · 6. Redirect Plan · 7. Production Configuration · 8. Production Browser QA Plan · 9. Accessibility Production Verification · 10. Security / Privacy Production Verification · 11. Measurement Production Verification · 12. SEO Production Verification · 13. Forms / External Integrations · 14. Assets · 15. Cache / CDN · 16. Monitoring · 17. Rollback Plan · 18. Rollback Triggers · 19. Owner Deployment Authorization · 20. Production Verification · 21. Post-Launch Observation · 22. Incident Log · 23. Known Gaps · 24. Exceptions · 25. Launch Closeout · 26. Evidence.

Where a V2.5 artifact already owns a concept (environment inventory, ownership register, release runbook, backup/restore), the launch plan **references** it and records only the launch-specific delta.

---

## 35. Launch evidence manifest

Machine-readable, one per production-verification run:

```text
RUN_ID · RELEASE_SHA · RELEASE_VERSION · DEPLOYED_SHA · ENVIRONMENT ·
PRODUCTION_URL · TIMESTAMP · CHECK · RESULT · EVIDENCE_REF · BLOCKER
```

Potential checks: domain · HTTPS · redirects · browser QA · accessibility · security headers · analytics · SEO · forms · critical assets · monitoring · rollback readiness. **Evidence must be tied to a release identity** — a manifest with no `release_sha` is invalid.

---

## 36. Release SHA match

Production verification ensures the **deployed release matches the expected release**. Where the deployment platform exposes a build/deployment identity, record it in `deployed_sha` / `build_id`. If exact SHA cannot be proven:

```text
DEPLOYED_IDENTITY = UNVERIFIED
```

is recorded and the SHA-match check is **BLOCKED** — never silently assumed to match. `evaluate_production_verification()` enforces this.

---

## 37. Preview / staging

Where preview or staging exists:

- distinguish it from production explicitly
- **do not mark `production_verified` from staging**
- verify staging indexability policy (staging should be `noindex`)
- avoid analytics contamination where practical
- avoid accidental production credentials on staging
- keep staging-domain evidence in a separate manifest

A perfect staging pass **does not equal** production verification. `production_verified()` returns `false` for any manifest whose `environment != "production"` or whose URL matches a staging marker.

---

## 38. Production URL authority

Store **one** canonical production URL/domain in `launch_ops.production_domain`. It must not contradict: SEO canonical · analytics config · Open Graph · sitemap · canonical tags · CMS · documentation. If the production domain changes, **update the specification before verification** — never verify against a domain the spec does not name.

---

## 39. Handoff integration

V2.5 Client CMS / Operations / Handoff remains the **long-term** operations authority. Launch Operations hands off, at Phase 12.25 → 12.5 intake:

production domain · deployment provider · release identity · rollback mechanism · monitoring ownership · environment inventory delta · recurring operational dependencies · known incidents · known limitations · final launch status.

**Do not duplicate V2.5 maintenance documentation.** Set `launch_ops.handoff_transferred = true` when the intake is recorded in `CLIENT-CMS-HANDOFF-PROTOCOL.md` §13.

---

## 40. Browser QA integration

Extend V2.8 Browser QA **only where necessary** for production mode — which the harness already supports:

```text
"environment": "production"      // in browser-qa-manifest.json (or https:// routes)
```

`browser-qa/runner.py` already:
- records `"environment": "production" | "local"` in every evidence manifest,
- gates `browser_qa.production_verified` on a **real-browser** run against a **production** surface,
- refuses to set it from `simulation` or from a localhost run.

Production Browser QA prohibits **destructive production actions by default** (no real form submissions, no state-changing requests) — the launch-mode manifest sets `interactions` to health-checks only. No second harness, no new state machine.

---

## 41. Accessibility / Security / Measurement / SEO integration (single source of truth)

Launch Operations **consumes** `accessibility{}`, `security_privacy{}`, `measurement{}`, and the SEO artifacts. It verifies *deployment realisation* and writes:

- its own launch-side fields (`launch_ops.production_*_verified`), **and**
- the appropriate canonical production-verification field (`accessibility.production_verified`, `security_privacy.production_verified`, `measurement.production_verified`) — the fields those specs already defined for exactly this purpose.

It **re-authors none** of them. It defines no KPI strategy, no event taxonomy, no security requirement, no SEO strategy phase.

---

## 42. Security / privacy integration

Launch Operations verifies deployment realisation of `security_privacy{}`. It does not redefine security/privacy requirements. A production discrepancy returns to the owning specification (§45). Website Director never outputs a legal-compliance claim from this phase.

---

## 43. Measurement integration

Launch Operations verifies production instrumentation against `measurement{}`. It does not redefine KPI strategy or event taxonomy, and it does not run a CRO optimization pass.

---

## 44. SEO integration

Launch Operations verifies production realisation of the locked SEO artifacts. It does not perform a new SEO strategy phase and submits nothing to Search Console.

---

## 45. Owner change / release change governance

If launch verification reveals that repairing production requires changes to: IA · copy · design tokens · motion · accessibility requirements · measurement strategy · security/privacy requirements —

**route back to the owning specification** and produce an Owner Change Request. **Do not make invisible production-only fixes that cause design/spec drift.** A production hotfix that changes locked intent HALTS; `launch_ops.status = "BLOCKED"` with a `blocked_reason`.

---

## 46. Implementation contract obligations

`IMPLEMENTATION-CONTRACT.md` §2.9 binds builders / release operators. They must not:

deploy an unidentified build · deploy with a dirty release candidate · silently change production configuration · commit production secrets · bypass failing launch checks · disable browser QA · disable accessibility verification · suppress security/privacy failures · remove analytics verification · rewrite baselines to get green · mark staging as production · claim production verification from localhost · deploy without required owner authorization.

---

## 47. Production checklist reconciliation

`PRODUCTION-CHECKLIST.md` Phase 12 remains **pre-deployment production readiness**. Launch Operations owns **deployment and production-realization verification**. `PRODUCTION-CHECKLIST.md` §11 states the division explicitly and avoids duplicating checkbox sets: pre-flight checks the *candidate*; Launch Operations checks the *deployed artifact on production*.

---

## 48. State transition rules

Allowed forward path:

```text
NOT_EVALUATED → PLANNING → RELEASE_READY → AWAITING_DEPLOYMENT_AUTHORIZATION
  → DEPLOYMENT_AUTHORIZED → DEPLOYING → DEPLOYED → PRODUCTION_VERIFICATION_RUNNING
  → PRODUCTION_VERIFIED → POST_LAUNCH_MONITORING → STABILIZED
```

Failure / rollback edges:

```text
* → BLOCKED (from PLANNING, RELEASE_READY, AWAITING_…, DEPLOYMENT_AUTHORIZED, DEPLOYING, DEPLOYED, PRODUCTION_VERIFICATION_FAILED, ROLLBACK_REQUIRED)
PRODUCTION_VERIFICATION_RUNNING → PRODUCTION_VERIFICATION_FAILED
DEPLOYED | DEPLOYING | PRODUCTION_VERIFICATION_* | PRODUCTION_VERIFIED | POST_LAUNCH_MONITORING | STABILIZED → ROLLBACK_REQUIRED
ROLLBACK_REQUIRED → ROLLED_BACK → (PLANNING | RELEASE_READY)
```

**Impossible transitions are rejected**, e.g. `NOT_EVALUATED → STABILIZED`, `PLANNING → DEPLOYED`, `RELEASE_READY → PRODUCTION_VERIFIED`. The full graph is `launch-ops/validator.py` → `STATE_TRANSITIONS`; `validate_transition()` / `validate_transition_path()` enforce it deterministically.

---

## 49. Validation scenarios (negative controls)

`tests/test_v2_10_launch_operations.py` and `examples/LAUNCH-OPERATIONS-INTEGRATION-VALIDATION.md` prove each scenario:

| # | Scenario | Expected |
| :-- | :--- | :--- |
| A | Local QA passed, never deployed | `release_candidate_ready = true`, `deployed = false`, `production_verified = false` |
| B | Deployment without owner authorization | **FAIL** |
| C | Release SHA mismatch | production verification **FAIL / BLOCKED** |
| D | HTTPS failure | **FAIL** |
| E | HTTP → HTTPS redirect correct | **PASS** |
| F | Production has staging `noindex` | SEO launch **FAIL** |
| G | Production canonical points to localhost/staging | **FAIL** |
| H | Analytics missing in production | measurement production verification **FAIL** |
| I | Analytics fires duplicate conversion | **FAIL** |
| J | Consent-dependent analytics fires before consent | **FAIL** |
| K | Production form endpoint misconfigured | **FAIL** without sending a real customer submission |
| L | Critical asset missing | **FAIL** |
| M | Staging passes all checks | `production_verified = false` |
| N | Rollback plan absent (where required) | release readiness **FAIL** |
| O | Post-launch critical incident | `ROLLBACK_REQUIRED` per explicit trigger |
| P | Production Browser QA local/production confusion | framework validation **FAIL** |
| Q | Sixth owner lock | **FAIL** |
| R | Frozen fixture mutation | V2.8 `FrozenIntegrityGuard` **FAIL** |

---

## 50. Test the tests

Negative controls prove the guards *fail* against deliberately broken synthetic fixtures — not merely that checks exist: unauthorized deployment transition · SHA mismatch · HTTPS failure · bad canonical · staging marked production · duplicate conversion · consent violation · missing critical asset · frozen-project mutation.

---

## 51. Test isolation

Use the V2.8 isolation architecture. Reuse `browser-qa/guards/frozen_integrity_guard.py` (`FrozenIntegrityGuard`). All launch framework validation operates on **synthetic / local fixtures** (in-memory dicts and temp directories). Do not mutate production. Do not mutate frozen pilots. **No suite writes anything under `projects/`.**

---

## 52. Backward compatibility

- Historical projects lacking `launch_ops{}` remain valid — tooling treats the object as absent without raising schema exceptions.
- Frozen certification pilots are **never** retrofitted.
- Existing release/deployment artifacts in `projects/` remain historical evidence.
- Materially reopened projects (new deployment, new domain, re-launch) use the canonical Launch Operations subsystem; framework upgrade alone never triggers Phase 12.25.

---

## 53. Versioning

V2.9.0 was current; no later legitimate local release existed. This subsystem is **additive** → **`V2.10.0`**. `2.10.0` is a valid semantic version and follows `2.9.0` — the minor version reaching `9` does not force a major bump to `3.0.0`.

---

## 54. No external side effects

This subsystem implements Website Director architecture only. It never: deploys · pushes · merges · alters DNS · modifies hosting · configures SSL · creates monitoring services · submits production forms · sends email · generates real leads · creates analytics conversions · modifies Search Console · modifies analytics accounts · modifies consent platforms · accesses customer data · uses production credentials · performs rollback on a live system.

---

## 55. Exceptions — narrow and evidence-based

`launch_ops.exception.applied = true` (with a recorded `reason`) is valid **only** for: offline prototypes · static disposable concepts · internal non-production exploration · an owner explicitly deferring deployment indefinitely on a local candidate (as several historical pilots did). A public commercial site that will be deployed **may never** receive a blanket exception to skip production verification.

---

*End of Protocol Specification.*
