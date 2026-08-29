# Website Director Specialist Control Plane

## Purpose

Own the bounded external-specialist architecture for Website Director. This layer expands available expertise without changing the existing prototype lifecycle, visual page, publishing boundary, or owner authority.

## Ownership

- `config/` owns the baseline, authority contract, upstream provenance, normalized registry, routing map, and benchmark freeze schema.
- `adapters/` owns the only executable specialist surface. Adapters return bounded guidance or findings and do not select other specialists.
- `router.js` owns decision-based selection, deterministic primary/secondary/validator roles, budget enforcement, and routing receipts.
- `benchmark/` owns comparison-pair freezing and metric schemas. It does not certify outcome quality.
- `benchmark/run.js` owns the local outcome-benchmark execution and report artifacts. It must fail closed when paired baseline and specialist outputs are absent.
- `tests/` and `validate.js` own technical architecture checks.
- `upstream/` owns local pinned provenance manifests and read-only snapshot metadata.

## Local Contracts

- Website Director remains the authority. External knowledge cannot change phases, gates, locks, SEO, research, brand rules, publishing, deployment, or the project stack.
- Raw upstream `SKILL.md` instructions are reference knowledge only. They are never loaded as executable orchestration.
- Adapters cannot install dependencies, mutate the stack, publish, deploy, write to external systems, or route another specialist.
- A decision may use one primary and one validator by default, or one primary, one secondary, and one validator for a complex decision. More than three requires a complete `SPECIALIST_BUDGET_EXCEPTION`.
- Every activated adapter receives a routing receipt and material contribution is tracked separately from activation.
- Project-local design memory is allowed. Global Tastemaker profile inheritance is disabled.
- Cinematic and other advanced capabilities remain dormant until Website Director explicitly routes them.

## Work Guidance

- Keep new capability in adapters, registry, or router rules. Do not edit the static page files to simulate specialist integration.
- Preserve upstream attribution, commit pins, licenses, and source paths.
- Prefer plain Node.js and JSON. Do not add dependencies for this control plane.

## Verification

- `node specialists/validate.js`
- `node --test specialists/tests/architecture.test.js`
- `npm run benchmark`
- Preserve benchmark manifests, results, routing receipts, screenshots, and reports under `benchmark/results/`.
- `node C:\Users\ALPHA\.context\scripts\verify.js C:\Users\ALPHA\Documents\ChatGPT\WEBSITE DIRECTOR`

## Child DOX Index

- `benchmark/AGENTS.md` - evidence-gated outcome benchmark execution, frozen comparisons, and preserved reports.
