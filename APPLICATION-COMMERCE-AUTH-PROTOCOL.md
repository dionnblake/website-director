# Conditional Application, Commerce and Authentication Architecture Protocol

<!-- FRAMEWORK_VERSION: 2.15.0 -->

> Capability 10, additive to Website Director V2.14. This protocol is the
> architecture authority for authenticated applications, commerce, bookings,
> memberships, and other stateful modules when explicit product behavior
> requires them.

## 1. Purpose and boundary

This protocol answers one question before implementation: does the proposed
site actually require application architecture? It records the evidence,
classifies the surface, activates only justified modules, and defines the
security and verification contract for those modules.

It is conditional. A static marketing site, public brochure, or public content
site remains static when its user stories do not create accounts, private data,
durable state, transactions, bookings, or user-authored content. This protocol
does not turn every website into an application.

The protocol is provider-neutral. It specifies boundaries and behavior, not a
provider account, SDK, production credential, payment account, database
instance, translation provider, or deployment.

## 2. Authority and state model

- The sole readiness state is `application.complete`.
- The sole readiness gate is `[APPLICATION_ARCHITECTURE_READY]`.
- There is no `application_locked`, `auth.complete`, `commerce.complete`,
  `payments.complete`, `i18n.complete`, or parallel application lock.
- The capability adds no owner lock. The framework retains exactly five owner
  locks: `design_direction_locked`, `information_architecture_locked`,
  `content_structure_locked`, `design_system_locked`, and
  `motion_direction_locked`.
- `application.complete` means the architecture contract is complete. It does
  not mean an external provider is configured, a live user exists, a payment
  was processed, the application was deployed, or production was verified.
- Implementation verification and production verification remain separate
  booleans and require their own evidence.

## 3. Phase placement

Run Phase 6.99 after the preceding planning authorities, including provenance,
and before Design System and implementation. It consumes the locked content
and adjacent security, accessibility, localization, measurement, provenance,
and content-operation contracts without replacing their authorities.

`launch_ops{}` remains the deployment and production-verification authority.
V2.5 Client Handoff remains the long-term client-operations authority. Browser
QA extends its existing runner for runtime observations; this capability does
not create a second browser runner.

## 4. Requirement assessment

Requirement assessment must cite explicit user stories, actors, state changes,
data classes, routes, and side effects. The assessor may use:

- an account, private route, role, object, or user-owned record;
- a server mutation, durable database state, search index, file, notification,
  booking, subscription, entitlement, order, refund, or webhook;
- a user-generated submission or an administrative workflow;
- a purchase, recurring charge, inventory constraint, or appointment.

The assessor must not infer a requirement from industry, company name,
geography, IP address, browser language, ethnicity, audience stereotype, or a
generic label such as "modern" or "premium". Ambiguous evidence is
`PARTIALLY_REQUIRED` and `OWNER_REVIEW_REQUIRED`, not a guessed architecture.

## 5. Application classifications

Classifications are behavior labels, not architecture by themselves:

`STATIC_MARKETING`, `CONTENT_PUBLISHER`, `LEAD_GENERATION`, `ECOMMERCE`,
`SUBSCRIPTION_COMMERCE`, `AUTHENTICATED_APP`, `SAAS`, `CLIENT_PORTAL`,
`MEMBERSHIP`, `COMMUNITY`, `MARKETPLACE`, `BOOKING`,
`USER_GENERATED_CONTENT`, `INTERNAL_APPLICATION`, and `HYBRID`.

The classification record must explain the evidence behind each label. A
`HYBRID` label is valid for a public surface with a separately bounded
application area, but it does not authorize application modules on the public
surface without stories that need them.

## 6. Module activation

The canonical module registry is `templates/application-module-registry.json`.
Each module record declares `module_id`, `required`, `status`,
`business_reason`, `data_classes`, `security_risk`, `external_provider`,
`owner`, `dependencies`, `verification_required`, and `exception`.

The registry is a catalogue, not an activation switch. A project activates a
module only in its application architecture manifest and only when a user
story justifies it. Dependencies must also be activated. Unused modules remain
`required: false` and `NOT_REQUIRED`.

The supported module set is AUTHENTICATION, AUTHORIZATION, USER_PROFILE,
DATABASE, API, CATALOG, CART, CHECKOUT, PAYMENT, ORDER_MANAGEMENT,
SUBSCRIPTION, BOOKING, MEMBERSHIP, USER_GENERATED_CONTENT, FILE_UPLOAD,
TRANSACTIONAL_EMAIL, NOTIFICATIONS, WEBHOOKS, SEARCH, BACKGROUND_JOBS,
AUDIT_LOG, ADMIN_INTERFACE, THIRD_PARTY_INTEGRATION, STORAGE, and ENTITLEMENT.

## 7. User stories and actors

Every required architecture names a stable story ID, actor, precondition,
action, authoritative server result, data touched, failure behavior, and
verification evidence. Actors include anonymous users, authenticated users,
resource owners, staff, administrators, service workers, and external
providers when applicable.

Trust boundaries must identify the browser, application server, database,
storage, email service, payment boundary, webhook receiver, and administrative
surface. A browser is never an authority for identity, role, price, payment,
entitlement, or object ownership.

## 8. Authentication

When authentication is required, define the identity lifecycle, registration,
login, logout, email verification, recovery, account deletion, abuse controls,
and provider failure behavior. Passwords use a modern password-hash family
such as Argon2id, scrypt, bcrypt, or PBKDF2 with reviewed parameters. Plaintext
passwords and reversible password encryption are forbidden.

Passwordless links and recovery tokens are single-use, expiring, scoped, and
must not disclose account existence. MFA requirements, enrollment, recovery,
and lockout behavior are explicit when risk requires them. Authentication
provider unavailability is `BLOCKED`, never a passing implementation result.

## 9. Sessions

Define session creation, rotation after privilege changes, expiration,
revocation, concurrent-session behavior, and logout semantics. Browser session
cookies are Secure, HttpOnly, and use an explicit SameSite policy. Tokens are
not placed in URLs, logs, client bundles, screenshots, or analytics payloads.
CSRF protection is explicit for cookie-authenticated mutations. Refresh and
access token boundaries are separate when tokens are used.

## 10. Authorization and object access

Authorization is enforced on the server for every protected route, mutation,
record, file, order, booking, entitlement, and administrative action. Define
roles, permissions, default deny, ownership rules, tenant boundaries, and
resource-level checks. Object-level authorization is required even when a
route itself is authenticated.

Client role flags, hidden buttons, disabled controls, route obscurity, and
client-side filters are never security controls. Administrative routes require
server-side authorization, audit coverage, and explicit impersonation rules.

## 11. User profiles and personal data

Collect the minimum profile fields needed by a story. Record purpose, owner,
retention, deletion, export, correction, recovery, and access rules. Do not
collect a name, phone, address, date of birth, government identifier, or
payment field merely because a form can store it. Sensitive data escalates to
specialist and owner review under the Security and Privacy authority.

## 12. Database, migrations, and transactions

Define entities, ownership, keys, constraints, indexes, retention, deletion,
backup, recovery, migrations, rollback, and transaction boundaries. Migrations
are repeatable, reviewed, and safe against partial application. Multi-record
state changes use an explicit transaction or an equivalent consistency model.
Database credentials and production connection strings never enter source,
fixtures, logs, or client code.

## 13. API and server boundary

Every API contract defines authenticated and anonymous access, input schema,
normalization, authorization, output allowlists, error shape, status codes,
rate limits, abuse controls, pagination, idempotency, and observability.
Validation is repeated at the server boundary even when the UI validates the
same fields. Errors do not disclose credentials, hashes, provider secrets,
internal stack traces, or object existence without authorization.

## 14. Catalog and pricing

Catalog identity, variant identity, availability, tax treatment, currency,
unit rules, and canonical prices are server-owned. The server resolves price
from trusted catalog state at checkout. A client-submitted price, discount,
tax, currency conversion, inventory count, or total is an input to validate,
never the source of truth.

## 15. Cart

Cart ownership, anonymous-cart policy, merge behavior, line-item constraints,
availability, quantity limits, price refresh, expiration, and duplicate-submit
behavior are explicit. A cart is not an order and does not imply payment. The
server recomputes totals and records the price snapshot used for checkout.

## 16. Checkout

Checkout is a stateful boundary with review, confirmation, validation, payment
authorization, and failure states. A button click cannot mark an order paid,
grant an entitlement, or emit a purchase event. A success route is shown only
after server/provider confirmation tied to the order, with safe retry and
refresh behavior.

## 17. Payment

The application never stores raw card numbers, security codes, magnetic-stripe
data, or equivalent sensitive payment credentials. Use a hosted or tokenized
boundary, with the exact custody boundary recorded for owner and specialist
review. Payment states remain distinct from order states: `REQUIRES_PAYMENT`,
`PROCESSING`, `SUCCEEDED`, `FAILED`, `CANCELED`, and `REFUNDED` are examples,
not a substitute for a provider contract.

Provider unavailable, uncertain, duplicate, reversed, or delayed events remain
blocked or pending. The architecture never simulates a real charge against a
live account. Tax and shipping rules are explicit where they apply.

## 18. Orders and fulfillment

Orders have a separate lifecycle such as DRAFT, PENDING_PAYMENT, PAID,
FULFILLING, FULFILLED, CANCELED, and REFUNDED. Payment success alone does not
imply fulfillment. Define cancellation, partial failure, refund, support,
inventory, digital delivery, and physical shipping behavior.

Digital goods and services must not collect unnecessary shipping data. Physical
goods require shipping address, region, carrier, rate, fulfillment, and failure
rules appropriate to the actual product. Mixed catalogs document which lines
require shipping.

## 19. Subscriptions and entitlements

Subscription billing state is separate from entitlement state. Define trial,
active, past-due, paused, canceled, expired, grace, refund, and provider-event
behavior. A failed or reversed payment cannot silently leave a paid
entitlement active. Access checks read authoritative entitlements, not a
client boolean or a stale local cache.

## 20. Booking

Booking architecture defines resource identity, availability, duration,
buffer, capacity, cancellation, rescheduling, conflict checking, and race
handling. Overlapping reservations must be prevented at the authoritative
boundary. Timezone, daylight-saving behavior, display locale, and storage
format are explicit. "Local time" or an inferred browser timezone is not a
complete contract.

## 21. User-generated content

UGC defines authorship, moderation, reporting, edit/delete, rate limits,
retention, abuse response, and visibility. User content is sanitized and
encoded for its output context. Arbitrary HTML, script, event handlers, unsafe
URLs, and stored XSS are rejected or safely transformed. Moderation is not
claimed merely because a text box exists.

## 22. File uploads and storage

Uploads use an allowlist of extensions, MIME types, size limits, count limits,
and content inspection appropriate to risk. Executable or active content is
not accepted by an unrestricted upload path. Private files use private storage
and authorization before download; object IDs and signed URLs are scoped and
expiring. Public URLs never expose a file intended to be private.

## 23. Transactional email and notifications

Account recovery, verification, order, payment, booking, and entitlement
messages are transactional when the story requires them. Delivery status,
retry, suppression, rate limits, template ownership, localized variants, and
failure UI are explicit. A failed required email must not be reported as
success. Notification content contains no secrets or unnecessary personal data.

## 24. Webhooks and background jobs

Webhook endpoints verify signatures against the raw request, enforce replay
windows where applicable, reject unknown event types, and perform idempotent
side effects keyed by a provider event identity. Duplicate delivery must not
duplicate an order, entitlement, email, booking, or refund. Background jobs
are authenticated, retryable, bounded, observable, and safe against duplicate
execution. Dead-letter and operator recovery behavior are explicit.

## 25. Admin and audit

Admin interfaces use server-side role and object authorization, least
privilege, reauthentication or step-up controls for high-risk actions, and
audit events that exclude secrets. Impersonation, if required, is explicit,
time-bounded, visible to the operator and affected user where appropriate,
and recorded. Hidden admin routes are not protected routes.

## 26. Third-party integrations and secrets

Every integration has a purpose, data classes, owner, page or server scope,
failure behavior, provider availability state, and verification plan. Unknown
or undeclared integrations block the architecture. Secrets remain in an
owner-controlled secure runtime boundary and are never placed in client
bundles, source control, examples, logs, screenshots, or telemetry.

Future provider-specific implementations fit behind replaceable boundaries
such as `AUTH_PROVIDER_ADAPTER`, `PAYMENT_PROVIDER_ADAPTER`,
`EMAIL_PROVIDER_ADAPTER`, and `STORAGE_PROVIDER_ADAPTER`. Capability #10 does
not implement a provider marketplace or select an account on the owner's
behalf.

## 27. Retention, deletion, and recovery

For each application data class, define collection purpose, retention, user
deletion behavior, legal hold handling when applicable, backup expiry,
restore testing, account recovery, and support access. A deletion request must
not be claimed complete until the authoritative records and relevant derived
records have a documented result.

## 28. Accessibility and localization

Authenticated and transactional flows use the existing Accessibility authority
for keyboard, focus, errors, status announcements, target size, reflow, and
screen-reader behavior. Localization consumes the existing locale contract:
semantic message IDs, safe interpolation, plural categories, locale-aware
dates/numbers/currency/units, logical CSS, RTL behavior, expansion testing,
localized metadata, and reviewed translations. Application architecture does
not create a second accessibility or localization state.

## 29. Content operations, provenance, SEO, and measurement

Content models, editorial authority, rich text, media references, slugs, and
redirects remain owned by Content Operations. Claims, source materials, rights,
hashes, and production assets remain owned by Provenance. Private application
routes are not indexable; public catalog/content routes follow SEO authority.

Measurement reuses canonical event names and adds a locale parameter where
needed. A purchase event follows authoritative confirmed purchase state, not a
button click. No PII or secrets enter events. Application state does not
override the adjacent Security and Privacy or Conversion and Analytics
requirements.

## 30. Browser, API, and synthetic QA

The existing Browser QA runner consumes an `application` plan block and
runtime `ApplicationObservation`. It checks browser-observable role trust,
protected routes, pricing, payment confirmation, webhook and idempotency
facts, private routes, purchase events, and other declared requirements. It is
not a second runner and does not certify a provider integration by inference.

API checks use deterministic contract fixtures with no real provider calls,
real user creation, raw card data, live webhook delivery, or production data.
Unknown observations are `BLOCKED` or `FAIL` as appropriate; missing evidence
is never promoted to a pass.

## 31. Launch and handoff

Launch Operations alone decides release readiness, deployment authorization,
known release identity, production verification, rollback, and stabilization.
Application readiness never authorizes deployment. Client Handoff transfers
durable runbooks, roles, secrets custody instructions, migrations, backups,
provider procedures, support, incident response, and recovery without placing
credentials in the repository.

## 32. Exceptions and blocked states

An exception requires an owner, reason, scope, expiry or review point, affected
module, residual risk, and evidence. It cannot hide a missing control or create
a new lock. Provider account or environment unavailability is `BLOCKED`, not
`VERIFIED`. Unknown requirement evidence is `PARTIALLY_REQUIRED` and requires
owner review.

## 33. Required artifacts

- `templates/application-architecture-plan.md`
- `templates/application-architecture-manifest.json`
- `templates/application-module-registry.json`
- `templates/application-architecture-review.md`
- `schemas/application-module-registry.schema.json`
- `application/validator.py`
- `tests/test_v2_15_application_architecture.py`

## 34. Completion contract

Phase 6.99 is complete only when the architecture plan, manifest, module
registry, review, deterministic validator, synthetic A-AV controls, adjacent
Browser QA extension, and registered framework checks pass. This is
`APPLICATION_ARCHITECTURE_READY`; it is not an owner lock and it does not
authorize implementation, provider setup, payment, deployment, or production
verification.

framework_version=2.15.0
framework_phase=6.99:Conditional Application Architecture:ACTIVE
framework_gate=APPLICATION_ARCHITECTURE_READY
owner_locks=design_direction_locked,information_architecture_locked,content_structure_locked,design_system_locked,motion_direction_locked
