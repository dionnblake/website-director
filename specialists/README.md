# Website Director external specialist library

This is a local, dependency-free control plane for bounded capability expansion. It does not redesign the Alpha Starts Now prototype or replace Website Director's lifecycle.

## Runtime boundary

```text
OWNER
  ↓
WEBSITE DIRECTOR
  ↓
CURRENT DECISION / PHASE
  ↓
CAPABILITY ROUTER
  ↓
NORMALIZED WEBSITE DIRECTOR ADAPTER
  ↓
PINNED UPSTREAM KNOWLEDGE
```

Only `adapters/` is executable specialist code. Upstream instructions are represented as inert reference knowledge. An adapter returns bounded guidance or findings; it cannot select another specialist, mutate the stack, publish, deploy, or override Website Director.

## What is included

- `config/baseline.json` records the frozen pre-change static prototype and its unchanged difference report. Historical benchmark receipts retain the original reference name for auditability.
- `config/sources.json` records seven upstream URLs, exact commit pins, licenses, inventory timestamps, and local snapshot locations.
- `config/skill-inventory.json` inventories every discovered `SKILL.md` path from those pins.
- `config/registry.json` normalizes all 268 discovered definitions and classifies them as core, conditional-core, on-demand, or library-inactive.
- `config/capability-map.json` defines deterministic capability classes and primary/secondary/validator routing.
- `adapters/` contains six core adapters plus the conditional UX/IA validator.
- `router.js` enforces current-decision routing, page eligibility, specialist budgets, and receipts.
- `receipts.js` defines the required routing-receipt fields.
- `benchmark/harness.js` freezes comparable baseline/specialist pairs and preserves the acceptance-note rubric without certifying outcomes by itself.
- `benchmark/run.js` executes the four benchmark classes, captures routing-only evidence, and fails closed when paired website outputs are missing.
- `validate.js` performs fail-closed technical checks.
- `tests/architecture.test.js` covers routing, dormancy, budget exceptions, adapter boundaries, and benchmark freeze behavior.
- `upstream/` contains local pinned provenance manifests and license text for each source. The full upstream content is not vendored into the prototype; skill paths and blob identities are preserved in the inventory for compatibility review.

## Commands

From the project root:

    node specialists/validate.js
    node --test specialists/tests/architecture.test.js
    npm run benchmark

The expected implementation status is:

    WEBSITE_DIRECTOR_SPECIALIST_ARCHITECTURE_IMPLEMENTED

That status does not mean the external library is outcome-certified. `npm run benchmark` writes the manifest, baseline results, specialist results, routing receipts, comparison data, screenshots, and Markdown report under `benchmark/results/<date>/`. The outcome verdict remains fail-closed until frozen comparisons produce evidence of material improvement without meaningful regression.

## Current V1 counts

The counts below are tied to the inventory timestamp in `config/sources.json`:

- 7 upstream repositories
- 268 discovered and registered skill definitions
- 6 core adapters
- 1 conditional-core adapter
- 40 on-demand mapping records, all dormant
- 38 unique on-demand skill entries
- 223 library-inactive skill entries
- 11 router capability classes

Upstream changes require a fresh inventory and adapter compatibility review. Do not overwrite normalized adapters automatically.
