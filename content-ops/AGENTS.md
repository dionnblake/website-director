# Content Operations and CMS Architecture

## Purpose

Own the deterministic Capability #8 Content Operations and CMS Architecture
validator and its bounded content-model, editorial, publishing, portability,
slug, media-reference, and CMS-decision contracts.

## Ownership

`validator.py` is the machine-readable authority for content-model integrity,
CMS-necessity assessment, explicit content ownership, editable-surface safety,
lifecycle and publishing boundaries, preview and scheduling architecture, slug
continuity, rich-text safety, content portability, and content-facing
references to Asset Director and Evidence Provenance.

This directory does not own long-term client training, backups, restore
operations, maintenance, environment inventory, recurring costs, or handoff
acceptance. Those remain owned by the historical V2.5
`CLIENT-CMS-HANDOFF-PROTOCOL.md` authority. It does not own SEO strategy,
accessibility semantics, security/privacy requirements, analytics measurement,
Asset Director production, Evidence Provenance, Localization, Ecommerce, or
Application Modules.

## Local Contracts

- Provider choice remains vendor-neutral until content, editor, workflow,
  preview, relationship, scale, portability, and security facts are recorded.
- A content model describes reusable subject entities and semantic fields. It
  must not encode layout slots, breakpoint behavior, card positions, colors,
  design tokens, analytics identifiers, security headers, or owner lock state.
- `DRAFT` is the default boundary for agent-generated content. Agents never
  receive autonomous `CAN_PUBLISH` authority.
- Published slug changes require durable 301 redirects. Archive, delete, and
  unpublish are distinct operations and must preserve inbound-link evidence.
- Media references consume Asset Director identity and V2.12 provenance; they
  do not create a second media or rights ledger.
- The readiness result is `content_ops.complete` and the gate is
  `[CONTENT_OPERATIONS_READY]`. This capability adds no owner lock.
- The validator performs no network, provider, credential, browser,
  deployment, production write, or external publishing operation.

## Work Guidance

Keep the validator standard-library-only, deterministic, provider-neutral, and
safe to run against synthetic fixtures. Return explicit `PASS`, `FAIL`, and
`BLOCKED` states plus machine-readable issue codes. Use the protocol and JSON
template as the contract, not as a reason to retrofit frozen historical
projects.

## Verification

Run `python tests/test_v2_13_content_operations.py` directly, then run the
registered suite through `python -m framework_validation --run-suites`. The
suite must prove A–V behavior, negative controls, and frozen-project
read-only integrity without writing under `projects/`.

## Child DOX Index

- None.
