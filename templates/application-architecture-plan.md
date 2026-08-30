# Conditional Application, Commerce and Authentication Architecture Plan

> Authority: `APPLICATION-COMMERCE-AUTH-PROTOCOL.md`. Machine form:
> `application-architecture-manifest.json`. Complete in Phase 6.99 only when
> explicit behavior requires application architecture.

## 1. Requirement assessment

- Required: `true` / `false` / `PARTIALLY_REQUIRED`
- Evidence source IDs: `[user-story / route / data-flow IDs]`
- State changes, private data, transactions, bookings, uploads, or user-authored content: `[list / none]`
- Requirement decision and unresolved evidence: `[rationale]`

## 2. Classification

- Selected classifications: `[STATIC_MARKETING / CONTENT_PUBLISHER / LEAD_GENERATION / ECOMMERCE / SUBSCRIPTION_COMMERCE / AUTHENTICATED_APP / SAAS / CLIENT_PORTAL / MEMBERSHIP / COMMUNITY / MARKETPLACE / BOOKING / USER_GENERATED_CONTENT / INTERNAL_APPLICATION / HYBRID]`
- Evidence for each classification: `[story IDs]`
- Public surface and application surface boundaries: `[routes / none]`

## 3. User stories

| Story ID | Actor | Preconditions | Action | Server-authoritative result | Data / side effect | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[id]` | `[actor]` | `[precondition]` | `[action]` | `[result]` | `[data]` | `[evidence]` |

## 4. Actors and trust boundaries

| Actor / boundary | Capabilities | Untrusted inputs | Allowed data | Server boundary |
| :--- | :--- | :--- | :--- | :--- |
| `[actor]` | `[capabilities]` | `[inputs]` | `[data]` | `[API / server rule]` |

## 5. Module inventory

- Registry: `templates/application-module-registry.json`
- Activated module IDs: `[only story-justified modules]`
- Unused modules remain `required: false` and `NOT_REQUIRED`.
- Dependency closure: `[dependency IDs]`

## 6. Module activation and ownership

| Module | Required | Business reason | Dependencies | Data classes | Risk | Owner | Verification |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| `[MODULE_ID]` | `[yes/no]` | `[story]` | `[IDs]` | `[classes]` | `[risk]` | `[owner]` | `[evidence]` |

## 7. Authentication

- Identity lifecycle: `[registration / invited / none]`
- Password policy: `[hash family / passwordless / not applicable]`; plaintext storage: `FORBIDDEN`
- Email verification, recovery, deletion, abuse and provider failure: `[contract]`
- MFA: `[required / not required / policy]`

## 8. Authorization

- Server-side enforcement: `[contract]`
- Default deny: `[yes / no / gap]`
- Protected routes and mutations: `[list]`
- Object-level ownership and tenant checks: `[contract]`

## 9. Roles and permissions

| Role | Permissions | Object scope | Administrative actions | Audit requirement |
| :--- | :--- | :--- | :--- | :--- |
| `[role]` | `[permissions]` | `[scope]` | `[actions]` | `[events]` |

Client role flags and hidden controls are never authoritative.

## 10. Session and token lifecycle

- Cookies: Secure / HttpOnly / SameSite `[values]`
- Rotation, expiry, revocation and logout: `[contract]`
- CSRF and token placement: `[contract]`
- URL, log, client bundle and analytics token exposure: `FORBIDDEN`

## 11. Data model and personal data

| Entity / field group | Purpose | Owner | Data class | Minimum fields | Retention | Deletion / export |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[entity]` | `[purpose]` | `[actor]` | `[class]` | `[fields]` | `[period]` | `[behavior]` |

## 12. Database and migrations

- Database required: `[yes/no]`
- Constraints, indexes and ownership: `[contract]`
- Migration, rollback, backup and restore plan: `[contract]`
- Transaction boundaries and consistency model: `[contract]`
- Credentials and production connection strings: never stored in this repository.

## 13. API and server contract

- Routes and methods: `[inventory]`
- Input validation and normalization: `[contract]`
- Output allowlists and error shape: `[contract]`
- Rate limiting, abuse control, pagination and idempotency: `[contract]`
- Authentication and authorization boundary: `[contract]`

## 14. Ecommerce requirement

- Commerce required: `[yes/no]`
- Product behavior: `[digital / physical / service / mixed / none]`
- Buyer, seller, fulfillment and support stories: `[IDs]`
- Provider and payment account status: `NOT_SELECTED / BLOCKED / owner-controlled`

## 15. Catalog and price authority

- Product, variant, availability and currency identities: `[contract]`
- Canonical price source: `[server catalog]`
- Client-submitted price, discount, tax, total and inventory: `UNTRUSTED`
- Tax, currency, unit and rounding rules: `[contract]`

## 16. Cart

- Cart ownership and anonymous-cart policy: `[contract]`
- Line-item, quantity, availability and expiration rules: `[contract]`
- Price refresh and server recomputation: `[contract]`
- Duplicate submit and concurrent update behavior: `[contract]`

## 17. Checkout

- Review, confirmation, validation and failure states: `[contract]`
- Payment confirmation source: `[server/provider confirmation or BLOCKED]`
- Success route behavior after refresh or delayed provider event: `[contract]`
- A click never marks paid or grants an entitlement.

## 18. Payments

- Collection boundary: `[hosted / tokenized / not applicable]`
- Raw card storage: `FORBIDDEN`
- Payment statuses and transitions: `[REQUIRES_PAYMENT / PROCESSING / SUCCEEDED / FAILED / CANCELED / REFUNDED / contract]`
- Provider availability, refunds, disputes, tax and failure handling: `[contract / BLOCKED]`

## 19. Orders and fulfillment

- Order statuses and transitions: `[DRAFT / PENDING_PAYMENT / PAID / FULFILLING / FULFILLED / CANCELED / REFUNDED / contract]`
- Payment state is separate from order state: `[yes / gap]`
- Digital delivery, physical shipping, cancellation and refund: `[contract]`

## 20. Subscriptions and entitlements

- Recurring lifecycle: `[trial / active / past due / paused / canceled / expired]`
- Entitlement state is separate from billing state: `[yes / gap]`
- Failed or reversed payment access behavior: `[contract]`
- Dunning, grace period, cancellation and webhook reconciliation: `[contract]`

## 21. Booking and scheduling

- Resource, capacity, duration, buffer and availability: `[contract]`
- Conflict prevention and race handling: `[contract]`
- Cancellation and rescheduling: `[contract]`
- Timezone and daylight-saving policy: `[explicit IANA / not applicable]`

## 22. User-generated content and uploads

- UGC authorship, moderation, reporting and deletion: `[contract / not applicable]`
- Sanitization and output encoding: `[contract]`
- Upload allowlist, MIME, size, count and inspection: `[contract / not applicable]`
- Executable content: `FORBIDDEN`; private storage and authorized download: `[contract]`

## 23. Transactional messaging

- Required messages: `[verification / recovery / order / booking / entitlement / none]`
- Delivery, retry, suppression, localization and failure UI: `[contract]`
- Failed required delivery is not presented as success.

## 24. Webhooks and event ingestion

- Event types and source identities: `[inventory]`
- Raw-request signature verification: `[contract]`
- Replay, deduplication and idempotency key: `[contract]`
- Unknown events and provider outage: `[reject / BLOCKED / contract]`

## 25. Background jobs

- Jobs, triggers, retries, timeouts and dead-letter handling: `[inventory]`
- Authentication and duplicate execution protection: `[contract]`
- Operator recovery and audit: `[contract]`

## 26. Admin interface and audit

- Admin routes and roles: `[inventory]`
- Server-side authorization and step-up controls: `[contract]`
- Audit events and retention: `[contract]`
- Impersonation: `[not supported / bounded policy / review required]`

## 27. Third-party integrations

| Integration | Purpose | Scope | Data classes | Owner | Failure state | Verification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[provider or NONE]` | `[purpose]` | `[server / route]` | `[classes]` | `[owner]` | `[behavior]` | `[evidence]` |

Unknown integrations block readiness. Provider account setup remains owner-controlled.

## 28. Security and privacy

- Security and Privacy review reference: `[path / status]`
- Secret custody: `[server-side secure runtime / not applicable]`
- Data minimization, consent, headers, transport and dependency inventory: `[status]`
- Sensitive data or high-risk operation escalation: `[status]`
- Legal compliance is not certified by this plan.

## 29. Accessibility

- Accessibility review reference: `[path / status]`
- Keyboard, focus, errors, status announcements, reflow and screen-reader behavior: `[contract]`
- Authenticated, checkout, upload, booking and admin states: `[contract]`

## 30. Localization and internationalization

- Localization plan reference: `[path / NOT_REQUIRED]`
- Message IDs, interpolation, plural categories, formatting and currency: `[contract]`
- RTL/logical CSS, expansion and localized email behavior: `[contract]`
- Translation review status: `[status]`; machine translation is draft only.

## 31. Measurement

- Measurement plan reference: `[path / status]`
- Canonical events and locale parameter: `[manifest]`
- Purchase event trigger: `[authoritative server confirmation / not applicable]`
- PII, secret and button-click event check: `[status]`

## 32. SEO

- Public routes, canonical URLs and structured data: `[contract]`
- Private/authenticated routes: `NOINDEX / not applicable`
- Catalog, booking and UGC indexability: `[contract]`

## 33. Content operations

- Content model and editorial owner: `[path / NOT_REQUIRED]`
- Rich text, media, slugs, redirects and publishing authority: `[contract]`
- Application-generated content boundary: `[contract]`

## 34. Provenance

- Evidence ledger and claim sources: `[path / status]`
- Rights, asset hashes, data sources, generated material and operator evidence: `[contract]`
- Provider responses, payment evidence and personal data: `[custody and redaction policy]`

## 35. Browser and API QA

- Browser QA manifest application block: `[path]`
- Runtime observation fields and routes: `[inventory]`
- Synthetic API fixtures: `[inventory]`; real users, live payments and external writes: `FORBIDDEN`
- Unknown or unavailable provider observations: `BLOCKED`

## 36. Launch operations

- Launch plan reference: `[path / status]`
- Release identity, deployment authorization, production verification and rollback: owned by Launch Operations.
- Application readiness does not authorize deployment or production credentials.

## 37. Handoff

- Handoff package reference: `[path / status]`
- Client runbooks: roles, secrets custody, migrations, backups, provider operations, support and incident response.
- Credentials are transferred through owner-controlled channels, never committed here.

## 38. Gaps and exceptions

| Gap / exception ID | Scope | Risk | Owner | Reason | Review / expiry | Required evidence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `[id]` | `[module]` | `[risk]` | `[owner]` | `[reason]` | `[date / event]` | `[evidence]` |

No exception may create a sixth owner lock, hide a missing control, or promote
an unavailable provider to verified.

framework_version=2.15.0
framework_phase=6.99:Conditional Application Architecture:ACTIVE
framework_gate=APPLICATION_ARCHITECTURE_READY
owner_locks=design_direction_locked,information_architecture_locked,content_structure_locked,design_system_locked,motion_direction_locked
