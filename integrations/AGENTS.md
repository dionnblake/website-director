# Integrations

> **Version:** 2.11.1

## 1. Purpose

This directory owns bounded, replaceable integrations that supply external
evidence to Website Director. Integrations are transport or normalization
helpers, not design authorities.

## 2. Ownership

The integration owner maintains source audits, immutable pins, credential
boundaries, normalized schemas, deterministic fixtures, and integration
verification. Visual Research, Design Constitution, Asset Director,
Accessibility, Conversion, Security, and Launch Operations remain the
authorities for their own decisions.

## 3. Local Contracts

- No integration may add an owner lock, lifecycle phase, completion flag, or
  project state object without an explicit framework decision.
- External credentials are environment-only and never enter source, fixtures,
  logs, or generated artifacts.
- Network, subprocess, image download, deployment, and global configuration
  side effects must be explicit, bounded, audited, and owner-controlled.
- Evidence must remain attributable, reference-only, and replaceable.
- The frozen `projects/` corpus is read-only.

## 4. Work Guidance

Prefer small adapters over provider-specific architecture. Pin upstream source
to an immutable commit, record the audit, normalize only the fields needed by
the owning protocol, and keep live smoke optional and bounded.

## 5. Verification

Every active integration has a deterministic fixture suite registered in
`schemas/test-suites.json`. Missing credentials are a blocked state, not a
passing live test. Run the framework validator and the registered integration
suite before completion.

## 6. Child DOX Index

- [design-inspiration/](design-inspiration/): research-only unified Design
  Inspiration MCP adapter and its source audit, schema, and fixtures.
