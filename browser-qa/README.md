# browser-qa/ — Website Director Browser & Regression QA Harness (V2.8)

Reusable, framework-level machine-executed browser verification. The **policy** is
canonical (`../BROWSER-REGRESSION-QA-PROTOCOL.md`); the **engine** that drives a
browser is replaceable.

```
runner.py            manifest-driven orchestrator + evidence manifest emitter
config/              viewports.json · browser-policy.json · ignore-justifications.example.json
engine/
  base.py            BROWSER_QA_ENGINE contract + PageObservation shape + verdict vocabulary
  simulation_engine.py   deterministic, dependency-free (fixture-driven)
  playwright_engine.py   reference real-browser adapter (Chromium / Firefox / WebKit)
assertions/
  __init__.py        Finding dataclass, requirement-source enforcement, evaluate()
  catalog.py         every check, grouped by protocol section, each requirement-traced
guards/
  frozen_integrity_guard.py   protected-path snapshot/verify (default: projects/)
fixtures/            synthetic scenario pages for the framework's own negative controls
evidence/            run artifacts — git-ignored (see evidence/README.md)
```

## Run against a generated project

```bash
python browser-qa/runner.py \
  --plan   path/to/project/browser-qa-manifest.json \
  --engine playwright \
  --mode   smoke \
  --evidence path/to/project/evidence/browser-qa
```

`--mode regression` runs the extended viewport + cross-browser matrix. `--engine
simulation` dry-runs the plan with no browser (never sets
`implementation_verified` / `production_verified`).

Install the real engine once:

```bash
pip install playwright && python -m playwright install chromium firefox webkit
```

## Verdicts

`PASS` · `FAIL` · `FLAKY` (fail-then-pass on retry — never laundered to PASS) ·
`BLOCKED` (engine/site unavailable — never a PASS) · `NOT_APPLICABLE`.

The runner exits non-zero on any `FAIL`, `BLOCKED`, `FLAKY`, or frozen-fixture
mutation, and prints the `browser_qa{}` block to apply to `site-profile.json`
(it never writes the profile itself).

## Add an engine

Implement `BrowserQAEngine.observe()` in a new module and register it in
`engine/base.load_engine()`. No policy change is required — the assertion
catalogue and runner only depend on `PageObservation`.

## Framework self-validation

```bash
python tests/test_v2_8_browser_regression_qa.py
```

runs the repo-level invariants plus the scenario A–L negative controls on the
`simulation` engine with only the standard library.
