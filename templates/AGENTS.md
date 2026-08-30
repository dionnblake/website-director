# Website Director Templates

## Purpose

Own current and review-only template artifacts consumed by the isolated
Website Director prototype and its framework validator.

## Ownership

site-profile.json is the current V2.13-compatible site-profile fixture with
the V2.13 framework version recorded explicitly. content-model.md and
content-model.json own the Capability #8 semantic content-model contract;
cms-decision.md owns the vendor-neutral CMS necessity and provider decision
record. inspiration-board.md and
research-synthesis.md own the reference-evidence fields consumed by the
bounded V2.11.1 Design Inspiration MCP adapter. evidence-ledger.md and
evidence-ledger.json own the Capability 7 claim, source, rights, attribution,
asset, and research-reference recording templates. framework-validation-review.md
is the human review record template.

## Local Contracts

- The current profile must match `schemas/site-profile.schema.json` and the
  canonical framework version.
- It must contain exactly the five approved owner locks.
- Framework-validation status, reports, and release certification do not belong
  inside the site profile.
- MCP-discovered references remain `REFERENCE_ONLY`; template fields must not
  turn them into production assets, implementation tokens, or a new state
  object.
- Evidence-ledger records are the cross-cutting provenance source of truth;
  asset-provenance.md and asset-manifest.json consume it without replacing
  Asset Director ownership or creating a sixth lock.
- Production claims and assets require traceable evidence, permitted-use
  records, attribution where required, and SHA-256 identity where applicable.
  Missing or unresolved evidence remains blocked. Hashes do not establish
  ownership or legal clearance.
- Content Operations templates define entities, fields, editorial lifecycle,
  editable surfaces, portability, migration, and provider decisions without
  duplicating V2.5 handoff operations or creating a sixth lock.
- Historical templates may be referenced by compatibility records but must not
  be silently regenerated or promoted to current.

## Work Guidance

Keep templates dependency-free, explicit, and neutral. Add a new template only
when its manifest and registry ownership are clear.

## Verification

Run `python -m framework_validation --run-suites` and inspect schema, reference,
content-operations, provenance, and five-lock findings. The synthetic
Capability 7 A-V suite plus W-AK fail-closed regression edges and Capability 8
A-V suite must remain isolated from projects/ and external systems.

## Child DOX Index

- None.
