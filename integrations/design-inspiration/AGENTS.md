# Design Inspiration Integration

> **Version:** 2.11.1

## 1. Purpose

Provide a bounded Visual Research adapter for the audited
`YonasValentin/design-inspiration-mcp-server`. It converts structured search
evidence into attributable, reference-only candidates for the existing
Visual Research pipeline.

## 2. Ownership

This directory owns the upstream audit record, immutable commit pin, adapter
normalization and heuristics, query and credential policy, token-extraction
boundary, normalized result schema, and synthetic fixtures. It does not own
design direction, copy, information architecture, design tokens, production
assets, analytics, accessibility certification, or deployment.

## 3. Local Contracts

- The upstream source is accepted only at commit
  `2935c0775fb1cfe3d95503615901e1fa743430e8`.
- The adapter exposes the three search tools only. `design_extract_tokens` is
  not part of the ordinary integration surface and is off by default.
- `SERPER_API_KEY` is environment-only. No real credential is permitted in
  this directory or its tests.
- MCP output is evidence, not authority. `copyright_boundary` is always
  `REFERENCE_ONLY`, and image URLs are never downloaded or promoted to
  production assets.
- Research patterns may be extracted; compositions, exact copy, and branded
  assets may not be cloned.
- The adapter itself performs no network access, subprocess execution, or
  filesystem mutation.
- No child state, gate, lock, phase, site profile field, or Capability 7
  evidence/provenance system is introduced here.

## 4. Work Guidance

Keep platform recognition unified for Dribbble, Behance, Awwwards, Mobbin, and
Pinterest. Preserve Awwwards as the policy and interpretation authority while
using the MCP only as discovery transport. Query specificity, search budgets,
canonical URL deduplication, provenance, and fail-closed statuses are part of
the adapter contract in `ADAPTER.md`.

## 5. Verification

Run `python tests/test_v2_11_design_inspiration_mcp.py` for the deterministic
A–R controls. Then run `python -m framework_validation --run-suites` and the
registered historical suites. Tests may use disposable temporary fixtures but
must not mutate `projects/`.

## 6. Child DOX Index

No child DOX documents.
