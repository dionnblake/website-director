# SECURITY, PRIVACY & COMPLIANCE REVIEW: [Project Name]

> **Template Version:** 2.7.0  
> **Governance:** `SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md`  
> **Phase:** 6.75 — Security, Privacy & Compliance Intelligence  
> **Readiness Gate:** `[SECURITY_PRIVACY_READY]` → `site-profile.json` → `security_privacy.complete`  
> **Status:** `NOT_EVALUATED | ASSESSING | REQUIREMENTS_READY | BLOCKED | ESCALATED | EXCEPTION | NOT_REQUIRED`

> **Compliance boundary (mandatory, do not remove):** This document is a technical requirements review. It is **not** legal advice and **not** a compliance certification. Website Director never records `GDPR COMPLIANT`, `CCPA COMPLIANT`, `HIPAA COMPLIANT`, `PCI COMPLIANT`, `COPPA COMPLIANT`, or `LEGAL COMPLIANCE VERIFIED`. Permitted statuses are `REQUIREMENTS REVIEWED`, `TECHNICAL CONTROLS IMPLEMENTED`, `KNOWN GAPS DOCUMENTED`, `LEGAL REVIEW REQUIRED`, and `COMPLIANCE_NOT_CERTIFIED`.

---

## 1. Project Risk Classification

**Site classifications (may be more than one):**

| Classification | Applies | Evidence / Reason |
| :--- | :--- | :--- |
| `STATIC_MARKETING` | ☐ | |
| `CONTENT_PUBLISHER` | ☐ | |
| `AFFILIATE` | ☐ | |
| `LEAD_GENERATION` | ☐ | |
| `ECOMMERCE` | ☐ | |
| `AUTHENTICATED_APPLICATION` | ☐ | |
| `SAAS` | ☐ | |
| `COMMUNITY` | ☐ | |
| `USER_GENERATED_CONTENT` | ☐ | |
| `PAYMENT_ENABLED` | ☐ | |
| `HEALTH_OR_SENSITIVE_DATA` | ☐ | |
| `CHILD_DIRECTED_OR_CHILD_ACCESSIBLE` | ☐ | |
| `INTERNAL_PRIVATE_APPLICATION` | ☐ | |

**Assigned risk level:** `LOW | MODERATE | HIGH | SPECIALIST_REVIEW_REQUIRED`

**Deterministic factors that produced this level** (protocol §5 — the level must be auditable, not asserted):

1. [factor]
2. [factor]

**Functionality inventory used for classification** (routes, forms, authenticated areas, checkout, uploads, embeds), sourced from `information-architecture.md` and `content-plan.md`:

| Surface | Route | What It Does | Risk Contribution |
| :--- | :--- | :--- | :--- |
| | | | |

---

## 2. Data Inventory

One row per data class. All ten fields required (protocol §6). `RETENTION_KNOWN = FALSE` is honest; a guessed retention period is not.

| DATA_CLASS | SOURCE | PURPOSE | COLLECTION_POINT | DESTINATION | THIRD_PARTY | RETENTION_KNOWN | CONSENT_DEPENDENCY | SENSITIVITY | PRODUCTION_REQUIRED |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| | | | | | | | | | |

**Categories explicitly considered and found absent** (record so the absence is deliberate, not overlooked):
- [e.g. precise location — not collected; no geolocation API in the build]

**Inventory complete:** `TRUE | FALSE` → `security_privacy.data_inventory_complete`

---

## 3. Data Minimization

| Field | Surface | Documented Purpose | Required / Optional | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| | | | | `KEEP` / `MAKE_OPTIONAL` / `REMOVE` |

**Fields removed and why:**
- [field] — [no documented purpose / template inheritance / speculative future marketing]

**Fields retained without a documented purpose:** must be zero. Any entry here is a gate failure.

**Locked-artifact impact:** If minimization requires changing locked copy, locked IA, or a locked CTA, record the locked-change request here and **halt** — never silently edit (protocol §28).

- Locked-change request required: `YES | NO`
- Request reference: [id / description]

**Reviewed:** `TRUE | FALSE` → `security_privacy.data_minimization_reviewed`

---

## 4. Forms

**Applicable:** `YES | NOT_APPLICABLE`

| Requirement | Status | Specification / Note |
| :--- | :--- | :--- |
| Server-side validation is the trust boundary | ☐ | |
| Client-side validation treated as UX only | ☐ | |
| Sanitization / contextual output encoding | ☐ | |
| CSRF protection (session-authenticated state changes) | ☐ | |
| Bot / spam mitigation (accessible — see §22) | ☐ | |
| Abuse prevention (mail, records, paid quota) | ☐ | |
| Rate limiting on submission endpoints | ☐ | |
| Safe error handling (no internals leaked) | ☐ | |
| No sensitive values in URLs | ☐ | |
| File-upload restrictions (type, size, content, storage, filename) | ☐ / `N/A` | |
| Safe email handling (no header injection) | ☐ | |
| Duplicate-submit protection | ☐ | |
| Success state only on confirmed server success | ☐ | |

---

## 5. Authentication

**Applicable:** `YES | NOT_APPLICABLE` — *do not specify authentication architecture for a site that does not require it.*

| Requirement | Status | Specification / Note |
| :--- | :--- | :--- |
| Modern salted slow password hashing; never plaintext | ☐ | |
| Session cookies: `HttpOnly` | ☐ | |
| Session cookies: `Secure` | ☐ | |
| Session cookies: `SameSite` value + justification | ☐ | |
| Session expiration (idle + absolute) | ☐ | |
| Logout invalidates server-side session | ☐ | |
| Server-side authorization on every protected resource | ☐ | |
| Account recovery: single-use expiring tokens, no enumeration | ☐ | |
| Brute-force throttling / backoff | ☐ | |
| MFA capability where risk justifies | ☐ / `N/A` | |
| Reauthentication for sensitive actions | ☐ / `N/A` | |

---

## 6. Payment Boundary

**Applicable:** `YES | NOT_APPLICABLE`

**`payment_model`:** `NOT_APPLICABLE | HOSTED_PROVIDER | PROVIDER_ELEMENTS | UNRESOLVED`

```text
PAYMENT PROVIDER INTEGRATION  ≠  STORING PAYMENT CARD DATA
```

| Requirement | Status | Note |
| :--- | :--- | :--- |
| Established provider handles card entry | ☐ | |
| **No raw card number / CVV / PIN storage specified anywhere** | ☐ | Mandatory |
| Secret keys governed under §7; publishable keys marked as configuration references | ☐ | |
| Webhook signature verification | ☐ | |
| Order state not trusted from client redirect alone | ☐ | |
| PCI-related obligations flagged for qualified review | ☐ / `N/A` | |

**Compliance statement:** `COMPLIANCE_NOT_CERTIFIED`. Using a compliant provider reduces scope; it does not certify the merchant. **Do not write "PCI compliant".**

---

## 7. Secrets

**Secrets the architecture requires** — names and locations only. **Never paste a real credential into this document.**

| Secret Name | Purpose | Where It Must Live | Client-Exposed? | Present in `.env.example` as placeholder |
| :--- | :--- | :--- | :--- | :--- |
| | | Server env / platform secret store | Must be `NO` | ☐ |

**Configuration references that are legitimately public** (not secrets):

| Identifier | Purpose |
| :--- | :--- |
| | |

| Rule | Status |
| :--- | :--- |
| No secrets in client-side source | ☐ |
| No secrets committed to Git (including history, fixtures, tests) | ☐ |
| No production credentials in examples or documentation | ☐ |
| Environment / configuration boundary defined | ☐ |
| `.env.example` contains names and placeholders only | ☐ |
| Secrets redacted from logs and error output | ☐ |
| Secrets excluded from screenshots, evidence captures, reports | ☐ |
| Fail-closed behavior specified where a required secret is absent | ☐ |

**Policy defined:** `TRUE | FALSE` → `security_privacy.secrets_policy_defined`

---

## 8. Third-Party Services

Accounts, processors, and platforms the site depends on (distinct from §9 runtime scripts).

| Service | Purpose | Data Shared | Owner of Account | Secret Custody | Handoff Disclosure |
| :--- | :--- | :--- | :--- | :--- | :--- |
| | | | | | ☐ |

---

## 9. Third-Party Scripts

**Every production third-party runtime script must have a reason.** A script in the build with no row here is a gate failure.

| SERVICE | PURPOSE | DATA_EXPOSED | PAGE_SCOPE | CONSENT_DEPENDENCY | SECURITY_IMPLICATION | REMOVAL_IMPACT |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| | | | | | | |

**Origins required by these scripts** (must reconcile with the §16 CSP):

| Origin | Required By | Directive |
| :--- | :--- | :--- |
| | | |

**Inventory complete:** `TRUE | FALSE` → `security_privacy.third_party_inventory_complete`

---

## 10. Analytics / Measurement Privacy

**Canonical measurement authority remains `measurement{}` and `measurement-plan.md`.** This section reviews; it never creates a second analytics model and never silently rewrites measurement strategy (protocol §16).

| Review Item | Finding |
| :--- | :--- |
| Analytics provider / hosting model | |
| Cookies & storage set by provider | |
| Identifiers used (client ID, user ID, advertising ID) | |
| Event payload PII review | `PASS | FAIL` |
| Advertising features (remarketing, ad personalization) | |
| Cross-domain behavior | |
| Retention configuration | `[value] | UNKNOWN` |
| Third-party data sharing implied by provider terms | |
| Session replay | `DISABLED | JUSTIFIED_WITH_MASKING_POLICY` |

**PII prohibition verified across every parameter and UTM value:** ☐  
*(email, phone, full name, postal address, free-text message bodies, passwords, payment card data, medical information, government identifiers, date of birth)*

**Validation-error events carry field category, never field value:** ☐

**Activation decision:**
- `ACTIVATION_PERMITTED` — privacy requirements satisfied
- `ACTIVATION_BLOCKED_PENDING_PRIVACY` — reason: [.....]

**Consent alignment check:** `security_privacy.consent_status` and `measurement.consent_dependency` agree: `YES | NO (→ BLOCKED)`

---

## 11. Cookies / Browser Storage

| NAME_OR_CATEGORY | PURPOSE | OWNER | FIRST_OR_THIRD_PARTY | LIFETIME | ESSENTIAL_OR_OPTIONAL | CONSENT_DEPENDENCY |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| | | | | | | |

**Essential classification justification** — for each entry marked `ESSENTIAL`, state why the requested functionality genuinely cannot operate without it. Advertising and analytics storage is not essential merely because the business wants it.

**Fingerprinting-adjacent techniques used:** `NONE | [describe + owner authorization reference]`

**Inventory complete:** `TRUE | FALSE` → `security_privacy.storage_inventory_complete`

---

## 12. Consent Assessment

**`CONSENT_STATUS`:** `NOT_REQUIRED | REQUIRED | CONDITIONALLY_REQUIRED | UNASSESSED | OWNER_OR_COUNSEL_REVIEW_REQUIRED`

**Do not guess applicable law from an IP address or assumed geography.**

| Factor | Finding |
| :--- | :--- |
| Business location(s) | |
| Owner-declared target markets | |
| Tracking technologies actually present | |
| Advertising / remarketing use | |
| Cookies & client-side storage in use | |
| Sensitive data categories present | |
| Children / minors exposure | |

**Reasoning for the recorded status:**

[Plain-language reasoning. If applicability cannot be reliably determined, `OWNER_OR_COUNSEL_REVIEW_REQUIRED` is the correct and complete outcome.]

**If `REQUIRED`, consent behavior requirements:**
- Consent-dependent scripts must not execute before consent: ☐
- Consent-dependent storage must not be written before consent: ☐
- Consent state survives client-side route transitions without re-prompting or silently re-enabling: ☐
- Consent UI satisfies §22 accessibility and §14 non-manipulation requirements: ☐

---

## 13. Privacy Notice Requirements

**Likely required:** `YES | NO | UNASSESSED | OWNER_OR_COUNSEL_REVIEW_REQUIRED`

**Basis:** [what functionality creates the likely requirement]

**Required disclosure categories:**

| Category | Required | Source Inventory |
| :--- | :--- | :--- |
| What is collected | ☐ | §2 |
| Why it is collected | ☐ | §2 |
| Third parties involved | ☐ | §8, §9 |
| Cookies / tracking technologies | ☐ | §11 |
| User choices and how to exercise them | ☐ | §12 |
| Contact method | ☐ | |

**Route exists in locked IA:** `YES | NO (→ locked-change request required)`

**Legal sufficiency:** Not certified. `LEGAL REVIEW REQUIRED` where drafting or sufficiency exceeds available evidence.

---

## 14. Affiliate / Sponsored Disclosure

**Applicable:** `YES | NOT_APPLICABLE`

```text
AFFILIATE DISCLOSURE ≠ PRIVACY POLICY ≠ TERMS ≠ ADVERTISING CONSENT
```

| Placement | Route / Component | Requirement | Status |
| :--- | :--- | :--- | :--- |
| | | Visible at the point of the recommendation | ☐ |
| | | Visible without interaction (no accordion/tooltip/hover) | ☐ |
| | | Legible — same standard as body copy, not suppressed | ☐ |
| | | Design system accommodates the surface | ☐ |

**Sponsored placements:**

| Placement | Disclosure Need | Distinguishable From Editorial |
| :--- | :--- | :--- |
| | | ☐ |

**Wording:** Owner-approved wording required where legal language is involved. Do not ship invented legal text.

---

## 15. Marketing Claims Risks

| Claim Text | Location | Claim Type | Evidence | Provenance | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| | | superlative / performance / certification / statistic / testimonial | | | `SUPPORTED` / `UNSUPPORTED → KNOWN GAP` |

**Unsupported claims are recorded as known gaps (§23) and escalated to the owner.** Website Director does not silently rewrite locked copy and does not fabricate supporting evidence.

**Reviewed:** `TRUE | FALSE` → `security_privacy.claim_risk_reviewed`

---

## 16. Security Headers

**Applicable:** `YES | FORMALLY_BLOCKED (deployment environment unknown)`

| Header | Specified Value | Justification |
| :--- | :--- | :--- |
| `Content-Security-Policy` | | Derived from §9 origins — not a template |
| `Strict-Transport-Security` | | |
| `X-Content-Type-Options` | `nosniff` | |
| `Referrer-Policy` | | |
| `Permissions-Policy` | | |
| Frame-ancestors / clickjacking | | |
| Cross-origin policies (`COOP`/`CORP`/`COEP`) | / `N/A` | Only where isolation is genuinely required |

**CSP origin reconciliation:** every allowed origin traces to a §9 inventory row: ☐  
**Rollout:** `ENFORCE | REPORT_ONLY_THEN_ENFORCE` — enforcement target: [date/milestone]

**Defined:** `TRUE | FALSE` → `security_privacy.security_headers_defined`

---

## 17. HTTPS / Transport

| Requirement | Specification | Verification Stage |
| :--- | :--- | :--- |
| HTTPS redirect behavior | | Production |
| No mixed content | | Implementation + Production |
| Secure asset loading (first + third party) | | Implementation |
| Production canonical URLs use HTTPS | | Implementation |
| Secure-cookie assumptions align with deployment | | Production |

> Local development over HTTP is **not** a production failure and is not reported as a defect.

**Defined:** `TRUE | FALSE` → `security_privacy.transport_policy_defined`

---

## 18. Dependency / Supply Chain

**Applicable:** `YES | NOT_APPLICABLE (no package dependencies)`

| Dependency | Purpose | Runs On | First-Party or External Runtime | Pinned / Locked |
| :--- | :--- | :--- | :--- | :--- |
| | | client / server / both | | ☐ |

| Rule | Status |
| :--- | :--- |
| Unnecessary packages avoided | ☐ |
| Vulnerability scanning mechanism identified (or `UNKNOWN`) | |
| No abandoned / unvetted packages where alternatives exist | ☐ |
| Externally loaded runtime code distinguished from bundled code | ☐ |
| No duplicate libraries | ☐ |
| Lockfile committed | ☐ |

> Installation success is not evidence of safety.

**Defined:** `TRUE | FALSE` → `security_privacy.dependency_policy_defined`

---

## 19. Sensitive Data Escalations

**Sensitive data detected:** `YES | NO`

| Category | Present | Action |
| :--- | :--- | :--- |
| Medical / health information | ☐ | `SPECIALIST_REVIEW_REQUIRED` |
| Biometric data | ☐ | `SPECIALIST_REVIEW_REQUIRED` |
| Government identifiers | ☐ | `SPECIALIST_REVIEW_REQUIRED` |
| Highly sensitive financial information | ☐ | `SPECIALIST_REVIEW_REQUIRED` |
| Children's / minors' data | ☐ | `SPECIALIST_OR_COUNSEL_REVIEW_REQUIRED` |
| Precise location | ☐ | Assess |
| Other high-risk data | ☐ | Assess |

**If any row is checked:** `risk_level = SPECIALIST_REVIEW_REQUIRED`, `sensitive_data_detected = true`, `specialist_review_required = true`, status `COMPLIANCE_NOT_CERTIFIED`.

**Do not self-certify HIPAA, COPPA, GDPR, GLBA, or any state-law obligation.** Technical controls may still be specified; they are reported as technical controls, never as compliance achieved.

---

## 20. Legal Review Escalations

**Legal review required:** `YES | NO`

| Item | Why It Exceeds Evidence | Escalated To |
| :--- | :--- | :--- |
| | | Owner / Counsel |

**Permitted status language only:** `REQUIREMENTS REVIEWED`, `TECHNICAL CONTROLS IMPLEMENTED`, `KNOWN GAPS DOCUMENTED`, `LEGAL REVIEW REQUIRED`, `COMPLIANCE_NOT_CERTIFIED`, `SPECIALIST_REVIEW_REQUIRED`.

**Owner decisions recorded** (protocol §29 — a recommendation is never recorded as approval):

| Decision | Owner Decided | Website Director Recommended |
| :--- | :--- | :--- |
| | ☐ | |

---

## 21. Implementation Requirements

The binding list handed to the coding agent under `IMPLEMENTATION-CONTRACT.md` §2.6. The builder implements exactly this and invents no security policy of its own.

| # | Requirement | Surface | Source Section |
| :--- | :--- | :--- | :--- |
| 1 | | | |

**Precedence reminder:** security/privacy overrides conversion optimization where they conflict; locked artifacts override both and require an owner change request.

**Specified:** `TRUE | FALSE`

---

## 22. Production Verification Requirements

**Implementation verification** (`security_privacy.implementation_verified` — post-build, browser + inspection evidence):

- [ ] No secrets in client bundle, source control, or evidence captures
- [ ] Every third-party script in the build appears in §9
- [ ] Every cookie/storage key written appears in §11
- [ ] Consent-dependent scripts/storage do not execute before consent (where consent is `REQUIRED`)
- [ ] Server-side validation enforced, not client-only
- [ ] No sensitive values in URLs
- [ ] Cookie security attributes set as specified
- [ ] No PII in analytics payloads — verified against actual network payloads
- [ ] Required disclosures present at specified placement
- [ ] Consent/disclosure UI keyboard operable; rejection as reachable as acceptance
- [ ] No console/network leakage of internals, credentials, or personal data

**Production verification** (`security_privacy.production_verified` — post-deployment only):

- [ ] HTTPS enforced and redirecting
- [ ] No mixed content
- [ ] Security headers present as specified
- [ ] Production configuration and environment separation confirmed
- [ ] Consent behavior matches specification in production

**Accessibility dependencies recorded for the future accessibility subsystem:**

| Surface | Dependency |
| :--- | :--- |
| | |

> Neither flag establishes legal compliance, vulnerability-freedom, or penetration-test results. Absent production evidence is reported as `NOT_YET_VERIFIED`, never as passing.

---

## 23. Known Gaps

Honest record of what is not satisfied. An empty list means none were found — not that none were looked for.

| Gap | Severity | Why It Is Open | Owner Decision Needed |
| :--- | :--- | :--- | :--- |
| | | | ☐ |

**Blockers** (`security_privacy.status = "blocked"`):

| Blocker | Blocked Reason (plain language) |
| :--- | :--- |
| | |

---

## 24. Exceptions

**Exception applied:** `YES | NO`

**Permitted only for:** offline prototype, static disposable concept, internal non-production visual exploration.

**Never permitted for:** a public commercial site that collects data.

| Field | Value |
| :--- | :--- |
| Reason | |
| Surface scope | |
| Owner authorization | ☐ |
| Date | |

---

## 25. Evidence

| Item | Evidence Location | Date | Verified By |
| :--- | :--- | :--- | :--- |
| Client bundle secret scan | | | |
| Third-party script capture | | | |
| Cookie / storage capture | | | |
| Consent behavior capture | | | |
| Analytics payload capture | | | |
| Disclosure placement screenshots | | | |
| Header response capture (production) | | | |
| HTTPS / mixed-content check (production) | | | |

**Evidence integrity:** captures must not contain credentials or personal data. Redact before storing.

---

## Terminal State

```json
"security_privacy": {
  "complete": false,
  "status": "not_evaluated",
  "risk_level": null,
  "site_classifications": [],
  "data_inventory_complete": false,
  "data_minimization_reviewed": false,
  "third_party_inventory_complete": false,
  "storage_inventory_complete": false,
  "consent_status": "UNASSESSED",
  "privacy_notice_required": "UNASSESSED",
  "disclosure_requirements": [],
  "secrets_policy_defined": false,
  "form_security_required": false,
  "authentication_required": false,
  "payment_model": "NOT_APPLICABLE",
  "security_headers_defined": false,
  "transport_policy_defined": false,
  "dependency_policy_defined": false,
  "sensitive_data_detected": false,
  "specialist_review_required": false,
  "legal_review_required": false,
  "dark_pattern_review": "not_evaluated",
  "accessibility_dependency_recorded": false,
  "claim_risk_reviewed": false,
  "known_gaps": [],
  "compliance_certified": false,
  "implementation_verified": false,
  "production_verified": false,
  "blocked_reason": null,
  "exception": {
    "applied": false,
    "reason": null
  }
}
```

`compliance_certified` is permanently `false`. Website Director has no mechanism to set it `true`.
