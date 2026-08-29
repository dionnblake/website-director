# browser-qa/evidence/

Run artifacts land here (and in a project's own `evidence/browser-qa/` when the
runner is pointed there). **Git-ignored by default** — see the repository
`.gitignore`.

## What lives here

- `<run_id>.evidence.json` — machine-readable evidence manifest (protocol §25).
- `<run_id>.summary.md` — human summary of failures / flakes.
- `*.png` — deterministic screenshots, named `route__viewport[__state].png`.
- `frozen-integrity-violations.log` — append-only ledger written by
  `guards/frozen_integrity_guard.py` the moment a protected file changes. It is
  git-ignored (transient), but within a run a recorded violation survives a later
  restore — the guard returns the drift in its result object and the ledger entry
  is written before any cleanup runs.

## Retention

- A project commits only the *current baseline set* it explicitly nominates in
  its `browser-qa-manifest.json`, plus the evidence manifest for the run that
  set `browser_qa.complete = true`.
- Everything else is transient and regenerated on the next run.
- Do not commit unlimited screenshots or Playwright traces.
