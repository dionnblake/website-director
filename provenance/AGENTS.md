# Evidence, Claim & Asset Provenance

## Purpose

Own the cross-cutting evidence ledger and deterministic validator for claim,
research-reference, testimonial, certification, and asset traceability.

## Ownership

This boundary owns source identity, evidence strength, rights evidence,
attribution, permitted-use boundaries, hash identity checks, and release
provenance references. Asset Director remains the authority for visual asset
strategy, generation, selection, optimization, and readiness. Security &
Privacy remains the authority for data-risk and disclosure controls.

## Local Contracts

- Production is fail-closed when required provenance is missing, stale,
  ambiguous, contradicted, or unverified.
- Production evidence and license references must resolve to durable source
  register records; direct URLs and free-text assertions cannot bypass the
  register.
- Prototype, local-demo, and internal exceptions must remain
  PROTOTYPE_ONLY; they never certify production use.
- A SHA-256 hash proves recorded byte identity, not ownership, license,
  exclusivity, or legal clearance.
- Research and screenshot references remain REFERENCE_ONLY and cannot be
  promoted to production assets.
- The validator never uses a network, credentials, external account, or
  projects/ fixture as a mutable test target.
- assets.provenance_status remains Asset Director state. The cross-cutting
  provenance.complete state is separate and has no owner lock.

## Work Guidance

Use provenance/validator.py for deterministic checks and
templates/evidence-ledger.json as the machine-readable authoring shape.
Keep historical project artifacts readable and do not retrofit frozen pilots.

## Verification

Run python tests/test_v2_12_evidence_asset_provenance.py, then
python -m framework_validation. Tests use disposable synthetic fixtures and
must leave projects/ unchanged.

## Child DOX Index

No child DOX documents currently exist.
