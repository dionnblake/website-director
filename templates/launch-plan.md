# LAUNCH PLAN — [Project Name]

> **Phase:** 12.25 — Launch & Production Operations
> **Protocol:** `LAUNCH-OPERATIONS-PROTOCOL.md`
> **Readiness gate:** `[RELEASE_READY]` → `site-profile.json` → `launch_ops.complete`
> **This plan is complete ≠ the site is deployed ≠ production verified ≠ stabilised.**
> Where a V2.5 handoff document already owns a concept (environment inventory, ownership register,
> release runbook, backup/restore), **reference it here** — do not copy its data.

---

## 1. Release Identity

| Field | Value |
| :--- | :--- |
| PROJECT | [Project Name] |
| RELEASE_VERSION | `[e.g. 1.0.0]` |
| GIT_SHA | `[full sha]` |
| BRANCH | `[branch]` |
| BUILD_ID | `[build id or NONE]` |
| BUILD_TIMESTAMP | `[ISO 8601]` |
| ENVIRONMENT | `production` |
| DEPLOYMENT_TARGET | `[§2 class]` |
| ASSET_MANIFEST_ID | `[digest or N/A]` |
| BROWSER_QA_RUN_ID | `[run_id or N/A]` |
| ACCESSIBILITY_RUN_ID | `[run_id or N/A]` |
| SECURITY_REVIEW_ID | `[version/digest or N/A]` |
| MEASUREMENT_PLAN_VERSION | `[event_schema_version or N/A]` |

**Release candidate freeze declared:** `[YES / NO]` — freeze date `[…]`. Any change after freeze creates a new
identity or is an explicit pre-authorization candidate update with a recorded reason (protocol §9).

---

## 2. Deployment Target

- **Class:** `STATIC_HOST | NETLIFY | VERCEL | CLOUDFLARE | AWS | AZURE | GCP | TRADITIONAL_WEB_HOST | CONTAINER_PLATFORM | CUSTOM_SERVER | OTHER`
- **Provider (only if known):** `[…]`
- **Build command:** `[…]`
- **Output directory:** `[…]`
- **Runtime version:** `[…]`
- Provider account/region/plan details are **not fabricated** — record only what is known.

---

## 3. Environment Readiness

> Consumes `ENVIRONMENT-INVENTORY.md` (V2.5). Record deltas only.

| Requirement | Status | Notes |
| :--- | :--- | :--- |
| Production environment identified | ☐ | |
| Environment variable names identified (no values) | ☐ | |
| No dev API endpoints / `localhost` / mock services | ☐ | |
| Production API origin known | ☐ | |
| Analytics environment / property known | ☐ | from `measurement{}` |
| Consent configuration known | ☐ | from `security_privacy{}` |
| Email / form destination known | ☐ | |
| Storage / CDN location known | ☐ | |
| Production secrets expected, not embedded | ☐ | |

`launch_ops.environment_ready = [true/false]`

---

## 4. Domain / DNS Plan

| Field | Value |
| :--- | :--- |
| Canonical domain | `[…]` |
| www policy | `[redirect-to-apex / redirect-to-www / N/A]` |
| apex policy | `[…]` |
| DNS provider | `[…]` |
| Required DNS records | `[list]` |
| Ownership / authorization boundary | ref `DIGITAL-OWNERSHIP-REGISTER.md` |

**DNS is not changed in this phase.** Production verification checks resolved behaviour.

---

## 5. HTTPS / TLS

- [ ] HTTPS active on production
- [ ] HTTP → HTTPS redirect to canonical origin
- [ ] No mixed content
- [ ] Correct canonical scheme
- [ ] Certificate valid in browser context; no certificate errors
- [ ] Secure-cookie assumptions hold (where applicable)

---

## 6. Redirect Plan

| Source | Destination | Code | Reason |
| :--- | :--- | :--- | :--- |
| `http://…` | `https://…` | 301 | transport |
| `www` ↔ apex | canonical | 301 | canonical |
| `[old url]` | `[new url]` | 301 | migration |

- [ ] No redirect chains
- [ ] No redirect loops
- [ ] Custom 404 resolves and matches design system

---

## 7. Production Configuration

- [ ] Debug endpoints / verbose logging / seeded data / mock services absent
- [ ] Environment separation confirmed (production config not from committed files)
- [ ] Public config identifiers (GA4 id, publishable keys) distinguished from secrets
- [ ] Logging boundary respected (protocol §24)

---

## 8. Production Browser QA Plan

> V2.8 harness, `environment: "production"`. **No destructive actions.** Health-checks only.

- Manifest: `[project]/browser-qa-manifest.json` with `"environment": "production"`
- Command: `python browser-qa/runner.py --plan [project]/browser-qa-manifest.json --engine playwright --mode smoke`
- Production-safe subset: `[routes / checks]`
- Real form submission: **NOT PERFORMED** unless §13 authorization recorded
- Result → `launch_ops.production_browser_verified`; `browser_qa.production_verified` set only by this run

---

## 9. Accessibility Production Verification

> Consumes V2.9. Re-check only browser-observable surfaces that can differ after deployment.

| Surface | Re-checked? | Result |
| :--- | :--- | :--- |
| Fonts / production rendering | ☐ | |
| Focus behaviour / route transitions | ☐ | |
| Consent UI | ☐ | |
| Media / third-party widgets | ☐ | |

Result → `launch_ops.production_accessibility_verified` **and** `accessibility.production_verified`.

---

## 10. Security / Privacy Production Verification

> Consumes V2.7. Verifies realisation only. **No intrusive testing. No compliance claim.**

- [ ] Security headers present with specified values
- [ ] HTTPS / no mixed content
- [ ] Cookie behaviour matches `security-privacy-review.md` §11
- [ ] Runtime third-party scripts match approved inventory §9
- [ ] Consent behaviour correct (nothing before consent where `REQUIRED`)
- [ ] Privacy / disclosure routes resolve
- [ ] No secret-shaped values in client surfaces

Result → `launch_ops.production_security_privacy_verified` **and** `security_privacy.production_verified`.
`security_privacy.compliance_certified` stays `false`.

---

## 11. Measurement Production Verification

> Consumes `measurement{}`. Synthetic / non-customer test data only.

- [ ] Analytics library loads
- [ ] Correct environment / property / config
- [ ] One `page_view` per route settle
- [ ] Critical CTA events fire
- [ ] **No duplicate events**
- [ ] No PII in any payload
- [ ] Affiliate: click ≠ conversion ≠ commission
- [ ] Conversion success is server-confirmed, not click
- [ ] UTM preserved across route transitions
- [ ] Consent gating: nothing fires before consent where `REQUIRED`

Result → `launch_ops.production_measurement_verified` **and** `measurement.production_verified`.

---

## 12. SEO Production Verification

> Define readiness only. **No Search Console submission.**

- [ ] Production `<title>` / description / canonical correct
- [ ] Robots / meta-robots correct — **no accidental staging `noindex`**
- [ ] Sitemap correct
- [ ] Structured data valid
- [ ] Production URLs (no `localhost` / staging canonical)
- [ ] Open Graph URLs / images resolve
- [ ] 404 handling

Result → `launch_ops.production_seo_verified`.

---

## 13. Forms / External Integrations

| Check | Status |
| :--- | :--- |
| `ENDPOINT_EXISTS` | ☐ |
| `CONFIG_PRESENT` | ☐ |
| `VALIDATION_ACTIVE` | ☐ |
| `ANTI_SPAM_PRESENT` | ☐ |
| `SUCCESS_PATH_CONFIGURED` | ☐ |
| `FAILURE_PATH_CONFIGURED` | ☐ |

**Real production submission authorization:** `[NOT AUTHORIZED / authorized by … on … ]`
Applies where a submission would send email / CRM / tickets / orders / conversions / third-party API actions.
Result → `launch_ops.production_forms_verified`.

---

## 14. Assets

### Evidence and provenance intake (V2.12)

- [ ] Every release asset resolves to an asset provenance_ref in the
      cross-cutting evidence ledger.
- [ ] Every production claim used by launch copy, metadata, structured data,
      or disclosures resolves to an EVIDENCE_REF.
- [ ] Required attribution, license evidence, permitted uses, AI metadata,
      source dates, and handoff restrictions are present.
- [ ] provenance/validator.py result is attached as PASS, or the launch stays
      BLOCKED / FAIL. This does not authorize deployment.

- [ ] Hero / logos / fonts / favicon / social preview / critical video / generated imagery / responsive assets present on production
- [ ] No `file://` / `assets/source/…` / unresolved dev paths shipped
- [ ] No accidental placeholder images

---

## 15. Cache / CDN

- [ ] Fingerprinted assets
- [ ] Correct cache headers
- [ ] HTML cache behaviour appropriate
- [ ] Old JS/CSS not served unexpectedly
- [ ] Invalidation / purge plan known
- [ ] CDN origin correct

---

## 16. Monitoring

- **Requirement:** `NOT_REQUIRED | BASIC_REQUIRED | APPLICATION_MONITORING_REQUIRED`
- **Coverage in place / planned:** `[runtime errors / server errors / failed requests / form failures / deploy health / uptime / perf regressions]`
- **Owner of monitoring:** `[…]`
- Vendor choice is conditional and owner-decided. `launch_ops.monitoring_ready = [true/false]`

---

## 17. Rollback Plan

| Field | Value |
| :--- | :--- |
| Last known good release | `[sha / version]` |
| Rollback mechanism | `[redeploy previous / platform revert / git revert + redeploy / …]` |
| Rollback owner | `[…]` |
| Required credentials / location (names only) | `[…]` |
| Data-migration implications | `[none / …]` |
| Cache implications | `[…]` |
| DNS implications | `[none / …]` |
| Rollback verification procedure | `[…]` |

`launch_ops.rollback_ready = [true/false]` · `launch_ops.rollback_tested = [true/false]`
Testing environment: `[local / staging / platform preview / synthetic]`. **No destructive production rollback here.**

---

## 18. Rollback Triggers

| Trigger | Severity | Action |
| :--- | :--- | :--- |
| Site unavailable | SEV0_CRITICAL | ROLLBACK_REQUIRED |
| Critical route failure | SEV0_CRITICAL | ROLLBACK_REQUIRED |
| Checkout / payment failure | SEV0_CRITICAL | ROLLBACK_REQUIRED |
| Authentication failure | SEV0_CRITICAL | ROLLBACK_REQUIRED |
| Sensitive-data exposure | SEV0_CRITICAL | ROLLBACK_REQUIRED |
| Broken primary conversion | SEV1_HIGH | ROLLBACK_REQUIRED |
| Severe / widespread JS errors | SEV1_HIGH | ROLLBACK_REQUIRED |
| Privacy / security regression | SEV1_HIGH | ROLLBACK_REQUIRED |
| Accessibility blocker introduced | SEV1_HIGH | ROLLBACK_REQUIRED |
| Severe visual break across core routes | SEV1_HIGH | ROLLBACK_REQUIRED |
| Production build identity mismatch | SEV1_HIGH | ROLLBACK_REQUIRED |
| Secondary feature failure | SEV2_MODERATE | triage |
| Isolated route issue | SEV2_MODERATE | triage |
| Cosmetic discrepancy | SEV3_LOW | backlog |

Project-specific overrides: `[…]`

---

## 19. Owner Deployment Authorization

> `RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED`. Explicit, per-release, owner act.

| Field | Value |
| :--- | :--- |
| Durable deployment policy exists? | `[NO / YES — ref …]` |
| Authorized for this release? | `[NOT AUTHORIZED / AUTHORIZED]` |
| Authorized by | `[owner name/role]` |
| Authorization reference | `[link / message id / signed note]` |
| Timestamp | `[ISO 8601]` |

Passing QA, completed implementation, approved design, "looks good", or prior/previous authorization
**do not** authorize deployment. `launch_ops.deployment_authorized` may be `true` only with a reference
or a durable policy.

---

## 20. Production Verification

| Domain | Result | Evidence ref |
| :--- | :--- | :--- |
| Release SHA match (`deployed_sha` == `release_sha`) | ☐ | |
| Environment is production (not staging/preview) | ☐ | |
| HTTPS / redirects / mixed content | ☐ | |
| DNS / canonical redirect | ☐ | |
| Production Browser QA (`environment=production`) | ☐ | |
| Production accessibility re-check | ☐ | |
| Security headers / third-party / consent | ☐ | |
| Analytics loads / environment / no duplicates / consent | ☐ | |
| SEO title/canonical/robots/sitemap/OG/404 | ☐ | |
| Forms config (no real submission) | ☐ | |
| Cache / CDN | ☐ | |
| Critical assets present | ☐ | |
| Monitoring active / rollback ready confirmed | ☐ | |

If `deployed_sha` cannot be proven: `DEPLOYED_IDENTITY = UNVERIFIED` and the SHA-match check is **BLOCKED**.

---

## 21. Post-Launch Observation

- **Policy:** `STATIC_SITE | LEAD_GEN | SAAS | ECOMMERCE` → window `[duration]`
- **Start:** `[…]` · **Expected end:** `[…]`
- **Signals observed:** `[…]`
- **Conversion anomalies:** `[none / …]`
- **Error anomalies:** `[none / …]`
- **Production performance anomalies (synthetic):** `[none / …]`
- No background monitoring daemon — this is an owner-observed checklist window.

---

## 22. Incident Log (append-only)

| INCIDENT_ID | RELEASE_SHA | TIME | ENVIRONMENT | ROUTE | SYMPTOM | SEVERITY | EVIDENCE | LIKELY_OWNER | ACTION | RESOLUTION | ROLLBACK_REQUIRED |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| | | | | | | | | | | | |

Resolved incidents are **not** deleted.

---

## 23. Known Gaps

- `[gap]` — owner, impact, plan
- Carried into `templates/production-review.md` and `CLIENT-CMS-HANDOFF-PROTOCOL.md` §13 intake.

---

## 24. Exceptions

`launch_ops.exception.applied = [false/true]` — reason: `[…]`
Valid only for offline prototypes, disposable concepts, internal exploration, or an owner explicitly
deferring deployment on a local candidate. **Never** a blanket skip for a commercial site that will deploy.

---

## 25. Launch Closeout

- [ ] `launch_ops.status` reflects reality (`RELEASE_READY` / `DEPLOYED` / `PRODUCTION_VERIFIED` / `STABILIZED` / …)
- [ ] Release notes written (§33) — `release_notes_ref`
- [ ] All production verification domains PASS / NOT_APPLICABLE / recorded gap
- [ ] `stabilization_complete` set only after the observation window closed with no open `SEV0`/`SEV1`
- [ ] Handoff intake recorded → `launch_ops.handoff_transferred = true` → Phase 12.5

**RELEASE NOTES**

- Release identity: `[…]`
- Major changes: `[…]`
- Known limitations: `[…]`
- Migrations: `[none / …]`
- Operational changes: `[…]`
- Analytics changes: `[…]`
- Security / privacy changes: `[…]`
- Accessibility changes: `[…]`
- Rollback reference: `[…]`
- No secrets in this document.

---

## 26. Evidence

- Launch evidence manifest(s): `[project]/evidence/launch/[run_id].evidence.json`
- Browser QA production evidence: `[project]/evidence/browser-qa/[run_id].evidence.json`
- Frozen-integrity: `FROZEN_FIXTURE_INTEGRITY = [PASS/FAIL]`
- Every check ties to a `release_sha`.
