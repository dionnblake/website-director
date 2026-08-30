# CLIENT CMS, OPERATIONS & HANDOFF PROTOCOL

> **Website Director System Specification**  
> **Version:** 2.5.0  
> **Status:** Authoritative Architectural Standard  
> **Scope:** Governs CMS selection, content modeling, editable surface contracts, client roles & permissions, digital ownership registers, credential security, backup & restore verification, release & rollback runbooks, post-launch maintenance, training plans, and operational handoff acceptance.

---

## 1. Core Mission & First Principles

A website build is not complete merely because the initial codebase, art direction, and animations are excellent.

> **The Core V2.5 Principle:**  
> *A professionally built website must remain understandable, maintainable, editable where appropriate, and recoverable after the builder leaves.*

**The Cardinal Prohibition:**  
*Never hand the client a repository and call the project finished.*

Website Director V2.5 guarantees operational maturity:
1. **Understandable:** Architecture, dependencies, and environment variables are explicitly documented without tribal knowledge.
2. **Maintainable:** Clear division of responsibilities across content edits, dependency updates, DNS, and hosting.
3. **Editable where appropriate:** Client-editable surfaces are strictly decoupled from design system architecture and motion engineering.
4. **Recoverable:** Backups are validated through actual restore procedures; ownership of domains, repositories, and hosting resides with the client.

---

## 2. CMS Requirement Evaluation & Justification Gate

CMS installation is **NOT** automatic. Unmotivated CMS integration introduces unnecessary vendor subscription fees, security attack surfaces, API latency, and editorial fragility.

#c# 2.1 The Four CMS Requirement Levels

1. `NOT_REQUIRED`:
   - Content changes rarely (quarterly or less) and developer-managed updates are fast, safe, and cost-effective.
   - *Examples:* High-impact landing page, static portfolio, campaign microsite, brochure site.
   - `CMS_REQUIRED = false`, `CMS_PROVIDER = "NONE"`, `CMS_ARCHITECTURE = "no_cms"`.
2. `LIGHTWEIGHT`:
   - Client requires routine editing of basic, non-relational content items (team bios, articles, FAQs, testimonials, company notices).
   - *Examples:* Boutique agency, corporate advisory firm, single-location consultancy.
   - `CMS_REQUIRED = true`, `CMS_ARCHITECTURE = "local_content_files"` or `"git_based_content"` or `"lightweight_headless"`.
3. `STRUCTURED`:
   - Content types exhibit strong relational properties (case studies linking to team members, industries, deliverables; filterable project catalogs; structured service offerings).
   - *Examples:* Architecture practice, engineering consultancy, design studio.
   - `CMS_REQUIRED = true`, `CMS_ARCHITECTURE = "headless_cms"` or `"structured_content_api"`.
4. `ADVANCED`:
   - Complex business operations require multi-role editorial workflows, content scheduling, localization, granular permissions, commerce catalogs, or live omnichannel integrations.
   - *Examples:* Global enterprise, e-commerce brand, multi-regional publication.
   - `CMS_REQUIRED = true`, `CMS_ARCHITECTURE = "headless_cms"` or `"commerce_platform"` or `"custom_admin"`.

### 2.2 The 15-Question CMS Justification Gate

Before any CMS architecture or provider is selected, the 15-question evaluation must be documented:

| # | Justification Question | Evaluation Criteria |
|---|---|---|
| 1 | How often does content change? | Rare -> NO_CMS; Weekly/Monthly -> LIGHTWEIGHT/STRUCTURED |
| 2 | Who changes it? | Developer -> NO_CMS; Non-technical client -> CMS required |
| 3 | How technical are editors? | Markdown/Git capable vs WYSIWYG / Form-field dependent |
| 4 | How many content types exist? | 1-2 flat types vs 3+ relational schemas |
| 5 | Are relationships between content important? | Yes -> requires structured schema references |
| 6 | Are drafts/previews required? | Yes -> requires draft preview environment/pipeline |
| 7 | Is localization (i18n) required? | Yes -> requires multi-locale content modeling |
| 8 | Are editorial approval workflows required? | Single editor vs Author -> Editor -> Publisher queue |
| 9 | Is scheduled publishing required? | Yes -> requires webhook cron / scheduled publishing engine |
| 10 | How many concurrent editors exist? | 1 person vs distributed multi-user team |
| 11 | Does commerce require a dedicated platform? | Content-only vs Shopify / Commerce API integration |
| 12 | Does the site require real-time application data? | Static content vs live database / authenticated user state |
| 13 | What is the client ongoing maintenance budget? | $0/mo self-hosted/flat vs $50-$500+/mo SaaS CMS tiers |
| 14 | Who will maintain CMS integrations & API updates? | Client technical team vs Developer SLA vs Vendor managed |
| 15 | What happens if the CMS vendor changes pricing/API? | Export portability and migration risk assessment |

### 2.3 Provider Neutrality & Selection Logic

Website Director remains strictly vendor-neutral. Supported architectural strategies include:
- `NO_CMS` (Static files / Developer managed)
- `LOCAL_CONTENT_FILES` (JSON / YAML / Markdown managed locally or in version control)
- `GIT_BASED_CONTENT` (Decap CMS / Frontmatter / TinaCMS / MDX)
- `HEADLESS_CMS` (Sanity, Contentful, Storyblok, Strapi, Payload, Directus)
- `TRADITIONAL_CMS` (WordPress, Webflow CMS)
- `COMMERCE_PLATFORM` (Shopify, BigCommerce)
- `CUSTOM_ADMI6` (Tailored administrative dashboard)

---

## 3. Editable Surface Contract & Design Protection

> **The Design Preservation Law:**  
> *Editable content does NOT mean editable design architecture.*

Clients must **never** be handed a "design destroyer" (arbitrary canvas tools, uncontrolled inline typography pickers, unconstrained color pickers, or raw HTML script injection).

| Surface Classification | Description & Scope |
|---|---|
| 1. CLIENT_EDITABLE | Text copy, validated imagery, structured field data, SEO titles & descriptions. |
| 2. CLIENT_SELECTABLE | Pre-approved theme modes (e.g. Light/Dark), curated badge styles, layout variant flags. |
| 3. DEVELOPER_CONTROLLED | Grid geometry, breakpoint logic, GSAP motion choreography, View Transitions. |
| 4. SYSTEM_GENERATED | XML sitemaps, structured JSON-LD schemas, asset srcsets, responsive picture tags. |
| 5. LOCKED_BRAND_ELEMENT | Brand signatures, logotype SVGs, protected legal disclaimers, core design tokens. |

### 3.1 Content Constraints & Layout Protection Rules

CMS schema definitions must actively constrain inputs to prevent layout breakage:
1. **Title Length Constraints:** Recommend character guidelines (e.g. `max_length: 80` for headlines) with responsive CSS truncation / wrapping fallbacks.
2. **Dimension & Aspect Ratio Guidance:** Require specific aspect ratios (`16:9`, `4:3`, `1:1`) and minimum resolutions (`1920x1080` for hero) on image fields.
3. **Array Bounding:** Cap list fields (e.g. max_items: 6` for featured case studies) so grids do not overflow.
4. **Rich Text Sanitation:** Rich text inputs strictly permit semantic tags (`p`, `h2`, `h3`, `ul`, `ol`, `li`, `blockquote`, `a`). Arbitrary inline CSS styles, <script>, and unchecked <iframe> tags are banned.

---

## 4. Content Modeling & Validation Standards

Every content type within a project must be defined in a strict, typed schema.

### 4.1 Content Model Schema Requirements

Each content model defines:
- `content_type_id`: Unique identifier (e.g., project, team_member, journal_entry).
- `purpose`: Plain-English editorial purpose.
- `fields`: Array of typed field specifications.
  - `field_id`, `label`, `type` (STRING, TEXT, IMAGE_REF, DATE, ENUM, ARRAY, RELATIONSHIP)  
  - `required` (boolean)  
  - `validation`: Regex, min/max length, allowed values, dimension requirements  
  - `editor_help`: Clear guidance text for non-technical editors
- `slug_policy`: Slug generation source, lowercase formatting, regex validation (^[a-z0-9]+(?:-[a-z0-9]+)*d).
- `seo_fields`: seo_title, seo_description, og_image_ref, canonical_override.
- `status_workflow`: DRAFT -> IN_REVIEW -> APPROVED -> PUBLISHED -> ARCHIVED.

### 4.2 Slug Governance & Redirect Automation

- Changing a published content item slug creates an automatic entry in the *Redirect Registry*:
  `{source_path: "/old-slug", destination_path: "/new-slug", status_code: 301, reason: "Slug rename on published project"}`
- Soft-deletion / Archival does not trigger immediate 404s; archived content is removed from public query listings while preserving permalink or issuing intentional 410 / redirect headers.

---

## 5. Client Roles & Least-Privilege Permission Model

Website Director establishes a strict permission hierarchy distinguishing administrative business ownership from editorial drafting.

### 5.1 Synthetic Permission Matrix

| Operation / Capability | `CLIENT_OWNER` | `CLIENT_ADMIN` | `EDITOR` | `AUTHOR` | `VIEW_ONLY` |
|---|:---:\:---:\:---:\:---:\:---:|
| Edit Content Fields | YES | YES | YES | YES (Own) | NO |
| Create Drafts | YES | YES | YES | YES | NO |
| preview Draft Content | YES | YES | YES | YES | YES |
| Publish to Production | YES | YES | YES | NO | NO |
| Archive Content | YES | YES | YES | NO | NO |
| Modify Global Design Tokens | NO (Dev) | NO (Dev) | NO (Dev) | NO (Dev) | NO (Dev) |
| Alter GSAP / Three.js Code | NO (Dev) | NO (Dev) | NO (Dev) | NO (Dev) | NO (Dev) |
| Manage User Roles / Billing | YES | YES | NO | NO | NO |
| Change DNS / Hosting Infra | YES | NO | NO | NO | NO |

---

## 6. Digital Ownership Register & Credential Security

### 6.1 Digital Ownership Principle

> **The Client Ownership Rule:**  
> *The client must ultimately own and control all critical production infrastructure.*

Under no circumstances should the developer retain personal ownership of the client domain, DNS, hosting, master CMS org, or analytics property.

### 6.2 Digital Ownership Register Schema

Every critical system must be recorded in `DIGITAL-OWNERSHIP-REGISTER.md`:
- `SYSTEM`: Domain, DNS, Hosting, CMS, Source Repository, Analytics, Form Provider, Transactional Email, CDN.
- `PROVIDER`: Vendor name.
- `ACCOUNT_OWNER`: Client organization entity.
- `BILLING_OWNER`: Client organization billing department.
- `TECHNICAL_ADMI6`: Client lead technical contact.
- `RECOVERY_CONTACT `: Verified corporate recovery email / secondary administrator.
- `TRANSFER_STATUS`: TRANSFERRED | CLIENT_PROVISIONED | MANAGED_SERVICE_AUTHORIZED | PENDING.

### 6.3 Credential Security Invariant

- **Zero Secret Values in Documentation:** `README.md`, `CLIENT-HANDOFF.md`, runbooks, and git history must **never** contain passwords, API private keys, connection strings, or bearer tokens (`SECRET_VALUES_IN_HANDOFF_DOCS = 0`).
- Documentation records environment variable **names**, descriptions, and rotation procedures, never raw values.
- Credential transfer must occur via secure enterprise secret vaults or direct client self-provisioning.

---

## 7. Backup Strategy & Restore Proof Invariant

> **The Restore Invariant:**  
> *A Backup strategy without a verified restore procedure is not a backup - it is wishful thinking.*

1. **Scope of Backup:** Source code repo, CMS content fixtures/database, media storage, and environment inventory.
2. **Deterministic Restore Verification:** Certification requires executing a physical restore test: backing up state, computing SHA-256 hashes, mutating data, restoring from backup, and proving `RESTORE_HASH_MATCH = true`.

---

## 8. Subsystem Handoff Boundaries

| SUBSYSTEM | EDITORIAL & HANDOFF BOUNDARY |
|---|---|
| SEO (V1.2) | Editors manage page titles, meta descriptions, alt-text, and slug redirects. Canonical architecture and JSON-LD schema generation remain system-controlled. |
| Assets (V2.0) | Editors upload images against strict dimension, ratio, and alt-text rules. Master assets live in repository. |
| Three.js (V2.1) | Scene graph, GLTF geometry, shaders, and lighting rigs are developer-controlled. 2D fallback is guaranteed. |
| Rive (V2.2) | .riv files, state machine inputs, and runtimes are developer-controlled. Editors do not touch runtimes. |
| View Transitions (V2.3) | Route transitions, shared elements, and scroll logic are developer-controlled. Semantic URLs remain stable. |
| CRO & Analytics (V2.4) | Business conversion goals and privacy boundaries are documented. Events follow object_action; PII is banned. |

---

## 9. Handoff Documentation Package Standard

A complete client handoff package consists of modular, purpose-built documents:

1. `CLIENT-HANDOFF.md`: Executive summary of deliverables, account ownership, URLs, support policy, and next steps.
2. `CONTENT-EDITOR-GUIDE.md`: Non-technical, step-by-step editorial guide for content creation, image constraints, previewing, publishing, archiving, and SEO.
3. `CMS-CONTENT-MODEL.md`: Formal schema specification of all content types, field validation rules, and relational mappings.
4. `DIGITAL-OWNERSHIP-REGISTER.md`: Authoritative matrix of infrastructure accounts, billing owners, and recovery contacts.
5. `MAINTENANCE-RESPONSIBILITY-MATRIX.md`: Explicit division of responsibilities across 14 operational vectors.
6. `ENVIRONMENT-INVENTORY.md`: Declaration of Local, Preview, and Production environments and environment variable requirements.
7. `RELEASE-RUNBOOK.md`: Technical guide for local setup, build commands, test verification, release deployment, and rollback execution.
8. `RECURRING-COST-REGISTER.md`: Itemized schedule of infrastructure, software licenses, domain fees, and renewal cadences.
9. `CLIENT-TRAINING-PLAN.md`: Structured curriculum for editorial and administrative training sessions.

---

## 10. Client Independence & Bus-Factor Tests

### 10.1 The Client Independence Test

To pass the `CLIENT_INDEPENDENCE_TEST`, the audit answers seven questions in the affirmative:
1. **Ownership Clarity:** Are all account owners and recovery contacts recorded without mystery accounts?
2. **Setup Clarity:** Can a new developer clone the repository and run the project locally in under 10 minutes from `RELEASE-RUNBOOK.md`?
3. **Content Clarity:** Can a non-technical editor safely draft and publish articles without developer intervention?
4. **Release Clarity:** Is the deployment procedure documented step-by-step?
5. **Rollback Clarity:** Is there a defined, tested rollback procedure for code and content?
6. **Backup Clarity:** Are automated backups configured and the restore script verified?
7. **Integration Clarity:** Are all third-party services, APIs, and licenses cataloged with their respective owners?

### 10.2 The Bus-Factor Invariant

If the original builder is hit by a bus tomorrow:
- The client retains full legal and administrative access to all domains, servers, CMS instances, and repositories.
- Zero credentials reside solely in a developer personal password manager or memory.
- An incoming engineering team can operate and evolve the site with zero downtime.

---

## 11. Handoff Readiness Gate vs. Five Owner Locks

> **The Governance Invariant:**  
> *`[CLIENT_HANDOFF_READY]` is an operational readiness gate, NOT a sixth owner lock. Exactly five owner locks remain immutable.*

The five creative locks remain:
1. `locks.design_direction_locked`
2. `locks.information_architecture_locked`
3. `locks.content_structure_locked`
4. `locks.design_system_locked`. `locks.motion_direction_locked`

Operational handoff state is governed by `site-profile.json` -> `handoff{}`.

---

## 12. Synthetic Certification Invariants

During automated testing and certification:
1. `REAL_CMS_ACCOUNT_CONNECTED = false`
2. `REAL_CREDENTIAL_TRANSFER = false`
3. `REAL_CLIENT_TRAINING_OCCURRED = false`
4. `PAID_APIS_INVOKED = false`
5. `DEPLOYMENT = false`. `PUBLISHING = false`
7. `HANDOFF_ACCEPTANCE_STATUS= "READY_FOR_REVIEW"` (Never fabricate real client acceptance `ACCEPTED` during synthetic validation).

---

## 13. Launch Operations Intake (V2.10)

Phase 12.25 (`LAUNCH-OPERATIONS-PROTOCOL.md`) owns the **launch event and its immediate aftermath**; this protocol owns **long-term operations**. They meet exactly once, at the Phase 12.25 → Phase 12.5 intake.

Launch Operations hands the following into this protocol's documents — it does **not** create parallel copies:

| Handed over | Lands in |
| :--- | :--- |
| Production domain / canonical URL | `DIGITAL-OWNERSHIP-REGISTER.md`, `ENVIRONMENT-INVENTORY.md` |
| Deployment provider / target class | `DIGITAL-OWNERSHIP-REGISTER.md`, `RECURRING-COST-REGISTER.md` |
| Release identity (version, `release_sha`, build id) | `RELEASE-RUNBOOK.md` |
| Rollback mechanism, owner, verification procedure | `RELEASE-RUNBOOK.md` (rollback section) |
| Monitoring requirement + ownership | `MAINTENANCE-RESPONSIBILITY-MATRIX.md` |
| Environment inventory delta | `ENVIRONMENT-INVENTORY.md` |
| Recurring operational dependencies | `RECURRING-COST-REGISTER.md`, `MAINTENANCE-RESPONSIBILITY-MATRIX.md` |
| Known incidents (`launch_ops.known_incidents[]`) | `CLIENT-HANDOFF.md` (known issues) |
| Known limitations / gaps | `CLIENT-HANDOFF.md`, `MAINTENANCE-RESPONSIBILITY-MATRIX.md` |
| Final launch status (`launch_ops.status`) | `CLIENT-HANDOFF.md` executive summary |

On completion of the intake, Launch Operations sets `launch_ops.handoff_transferred = true`. `[CLIENT_HANDOFF_READY]` remains a readiness gate; `[RELEASE_READY]` is a separate readiness gate; neither is a sixth owner lock. Exactly five owner locks remain immutable.

---

## 14. Evidence, Claim & Asset Provenance Handoff (V2.12)

The client handoff transfers the same project evidence ledger consumed by
Launch Ops. It does not create a parallel provenance authority or rewrite
historical project records.

Transfer, where applicable:

- evidence-ledger.json and the human review record
- claim EVIDENCE_REF values, source dates, expiration or review dates, and
  disclosure dependencies
- asset provenance_ref values, origin, license evidence, authorized uses,
  attribution, SHA-256 identity, and handoff restrictions
- testimonial source, consent, authority, edit notes, attribution, and
  production approval
- certification or award issuer, evidence, validity, and display
  authorization
- research and MCP reference records with platform, source URL, query,
  retrieval time, upstream SHA-256, REFERENCE_ONLY status, and
  PATTERN_TO_LEARN / WHAT_NOT_TO_COPY

Open or high-risk records remain visibly BLOCKED or REVIEW_REQUIRED in the
handoff. assets.provenance_status remains Asset Director state;
provenance.complete remains the cross-cutting readiness state; neither is a
deployment authorization.

---
*End of Protocol Specification.*
