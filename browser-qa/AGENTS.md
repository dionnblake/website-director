# DOX — browser-qa/

Local contract for the Browser & Regression QA harness. Parent: root `AGENTS.md`.
Authority for behaviour: `../BROWSER-REGRESSION-QA-PROTOCOL.md`.

## Scope

- This directory is the **reusable, framework-level** harness. It is not coupled
  to any one pilot. Project-specific historical QA scripts stay in their project
  folders as historical evidence.
- The **policy** (protocol, assertion catalogue, plan/manifest templates, state
  object, flake policy, evidence schema, baseline governance) is canonical.
- The **engine** (`engine/*.py`) is replaceable via `BrowserQAEngine.observe()`.

## Rules

- **Never mutate anything under `projects/`.** Every run wraps itself in
  `guards/frozen_integrity_guard.py`; a passing run that changed a frozen file is
  a failed QA architecture. Mutable work happens in temp dirs / disposable copies.
- **No persistent browser daemon** (`IMPECCABLE-ENGINE-PROTOCOL.md` §8). Launch
  per run, tear down every child process, server, and profile in `stop()`.
- **Every assertion traces to one requirement source** (`assertions/__init__.py`
  `REQUIREMENT_SOURCES`). No orphan checks. V2.9 added `ACCESSIBILITY_REVIEW`
  (`catalog.check_accessibility`, gated on `plan["accessibility"]`) — governed by
  `../ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md`, not a separate runner.
- **Unavailable ≠ pass.** A missing engine or unreachable site is `BLOCKED` with a
  reason. `FLAKY` never becomes `PASS`.
- **Do not re-implement Impeccable's static detectors.** Browser QA owns only the
  runtime-observable half (`BROWSER_EXECUTED`). See protocol §28. Accessibility
  contrast math stays Impeccable's; the accessibility group reuses it.
- **Accessibility (V2.9): the automated engine is replaceable.** `axe-core` via
  `PlaywrightEngine._axe_scan` (`vendor/axe.min.js`, git-ignored) or the
  `simulation` engine's declared fixture violations. Unavailable engine ⇒
  `BLOCKED_ACCESSIBILITY_ENGINE_UNAVAILABLE`; no screen reader ⇒
  `BLOCKED_SCREEN_READER_ENVIRONMENT`. Never a PASS. Never claim WCAG conformance
  from zero automated violations.
- **Do not commit** browser profiles, caches, `node_modules`, traces, or ephemeral
  screenshots. `evidence/` is git-ignored except its README and the
  frozen-integrity ledger path.
- New scenario fixtures live under `fixtures/<scenario>/` as `index.html` +
  `qa-fixture.json`. Keep them minimal and deterministic.

## Child DOX Index

_(none — this directory has no sub-contracts)_

## Framework validation integration

The V2.11 framework validator may invoke the canonical frozen-integrity guard
as a read-only boundary around deterministic suites. The guard remains the
single authority for protected `projects/` paths. Framework validation does not
replace the Browser QA protocol, add a second browser runner, or permit writes
to historical project artifacts.
