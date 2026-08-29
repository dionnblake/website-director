# browser-qa/vendor/

Third-party runtimes the browser QA engines inject at test time. **Not vendored
in the framework repo by default** (size + license hygiene) — a project drops
them here, and they are git-ignored.

## axe-core (accessibility engine — V2.9)

`ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md` §31: axe-core is a *replaceable
implementation engine*, not the policy authority.

To enable the automated accessibility scan in `PlaywrightEngine`:

```bash
# option A — drop the standalone bundle here
curl -L -o browser-qa/vendor/axe.min.js \
  https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js

# option B — install the Python wrapper
pip install axe-playwright-python
```

If neither is present, the engine records
`BLOCKED_ACCESSIBILITY_ENGINE_UNAVAILABLE` for the affected checks — **never a
PASS**. The deterministic `simulation` engine does not need axe: it reads
declared violations from each fixture's `qa-fixture.json` `a11y` block.

Record the engine name and version in `accessibility.automated_engine` and the
evidence manifest. Zero automated violations never establishes WCAG conformance.
