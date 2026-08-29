# Website Director / Alpha Starts Now Prototype and Specialist Control Plane

## Purpose

Isolated client-review prototype for testing Website Director's ability to produce a cinematic, editorial website experience for Alpha Starts Now, plus a bounded local architecture for external specialist knowledge.

## Ownership

This workspace owns the static Alpha Starts Now page, local generated imagery, interaction layer, review instructions, and the `specialists/` control plane. It does not own production Alpha Starts Now content, publishing, deployment, or external integrations.

## Local Contracts

- index.html is the review entrypoint.
- styles.css and tokens.css own visual tokens, composition, responsive behavior, and motion styling.
- script.js owns progressive enhancement, interactions, scroll choreography, and accessibility state.
- assets/ contains project-local imagery used by the prototype.
- favicon.svg owns the lightweight local browser mark.
- Keep the prototype isolated. Do not deploy, publish, or connect it to production systems without owner approval.
- Email capture and editorial links are intentionally local demo behaviors.
- `specialists/` is additive capability expansion. Website Director authority, lifecycle, brand controls, SEO, research requirements, publishing boundary, and stack remain unchanged.
- Raw upstream skills are pinned reference knowledge only. `specialists/adapters/` is the only executable specialist surface.

## Work Guidance

- Preserve the Alpha Starts Now direction: mature confidence, reinvention, tactile editorial composition, earned strength, and useful momentum.
- Prefer native HTML, CSS, and small vanilla JavaScript changes over new dependencies.
- Every interaction must have a usable keyboard/touch path and a reduced-motion behavior.
- Keep the previous `glow-*.png` assets as historical prototype material unless the owner explicitly requests cleanup.

## Verification

- Run the site from a local HTTP server and inspect desktop and mobile layouts.
- Run the global verifier when closing meaningful work:
  node C:\Users\ALPHA\.context\scripts\verify.js C:\Users\ALPHA\Documents\ChatGPT\WEBSITE DIRECTOR
- For specialist architecture changes, run `node specialists/validate.js` and `node --test specialists/tests/architecture.test.js`.
- For outcome benchmarking, run `npm run benchmark` and preserve the generated manifest, results, receipts, screenshots, and report under `specialists/benchmark/results/`.
- Do not claim deployment or production readiness. This is review-ready prototype work only.

## Child DOX Index

- `specialists/AGENTS.md` - bounded specialist control plane, provenance, routing, and validation.
