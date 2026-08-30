# Application Architecture Review

> Review authority: `APPLICATION-COMMERCE-AUTH-PROTOCOL.md`.
> This review records architecture evidence. It does not authorize providers,
> payments, deployment, publishing, or production verification.

## Decision

- Requirement status: `NOT_REQUIRED` / `PARTIALLY_REQUIRED` / `REQUIRED`
- Classifications: `[labels]`
- Architecture status: `PLANNING` / `READY` / `BLOCKED` / `EXCEPTION_APPLIED`
- Readiness gate: `[APPLICATION_ARCHITECTURE_READY]` only when the contract and
  evidence pass.
- `application.complete`: `false` until the canonical project state is
  explicitly updated from this reviewed artifact.

## Evidence and scope

| Evidence | What it proves | Owner | Status |
| :--- | :--- | :--- | :--- |
| `[story / route / data-flow]` | `[requirement]` | `[owner]` | `[status]` |

The review must show why each activated module is required and why each
unactivated module is not required. Industry, company name, geography, IP,
browser language, and stereotype are not acceptable evidence.

## Security and correctness review

- [ ] Authentication recovery, session, password, MFA and provider failure are defined when required.
- [ ] Authorization is server-enforced, default deny, and object-level where needed.
- [ ] Client roles, prices, payment state, entitlements and admin visibility are not trusted.
- [ ] Database migrations, transactions, retention, deletion and recovery are defined.
- [ ] Payment collection is hosted or tokenized; raw cards and secrets are absent.
- [ ] Payment and order state machines are distinct.
- [ ] Webhooks verify signatures and are idempotent.
- [ ] Subscription entitlements, booking conflicts, uploads, UGC and required messaging are bounded when applicable.
- [ ] Integrations and high-risk operations have explicit verification states.
- [ ] Private routes are not indexable; measurement follows authoritative events.

## Verification result

- Deterministic validator: `[PASS / FAIL / BLOCKED]`
- Synthetic controls A-AV: `[PASS / FAIL / BLOCKED]`
- Browser QA application assertions: `[PASS / FAIL / NOT_REQUIRED / BLOCKED]`
- Framework validation: `[PASS / FAIL / BLOCKED]`
- Implementation verified: `false` / `[owner evidence]`
- Production verified: `false` / `[Launch Operations evidence]`

## Gaps and owner decisions

| ID | Finding | Consequence | Required owner decision |
| :--- | :--- | :--- | :--- |
| `[id]` | `[gap]` | `[risk]` | `[decision]` |

## Review sign-off

- Reviewer: `[name / role]`
- Review date: `[date]`
- Evidence references: `[paths / IDs]`
- Status: `UNREVIEWED` / `REVIEWED` / `OWNER_APPROVED` / `BLOCKED`

framework_version=2.15.0
framework_phase=6.99:Conditional Application Architecture:ACTIVE
framework_gate=APPLICATION_ARCHITECTURE_READY
owner_locks=design_direction_locked,information_architecture_locked,content_structure_locked,design_system_locked,motion_direction_locked
