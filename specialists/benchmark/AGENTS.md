# Benchmark Control Plane

## Purpose

Own the evidence-gated outcome benchmark for the Website Director specialist architecture.

## Ownership

- `harness.js` owns the frozen criteria, comparison fields, metric schema, and fail-closed certification logic.
- `run.js` owns local benchmark execution, routing evidence collection, and report generation.
- `results/` owns preserved manifests, results, receipts, screenshots, and reports.

## Local Contracts

- Use the acceptance-note criteria in `specialists/config/benchmark-plan.json` as the frozen rubric before each run.
- Keep baseline and specialist freeze fields identical.
- Do not modify core adapters, the conditional UX/IA validator, Website Director lifecycle controls, or benchmark criteria to influence a result.
- Routing-only evidence is not an outcome result. A pass requires paired completed website outputs, objective verification, independent judgment, owner-friction metrics, and material specialist contribution.
- Keep the worktree local-only. Do not deploy, publish, or transmit benchmark artifacts.
- Preserve prior result directories. Re-running a date creates a new run directory instead of overwriting an existing report.

## Verification

- `npm run benchmark`
- `node --test specialists/tests/architecture.test.js specialists/tests/benchmark.test.js`
- `node C:\Users\ALPHA\.context\scripts\verify.js C:\Users\ALPHA\Documents\ChatGPT\WEBSITE DIRECTOR`

## Child DOX Index

- None.
