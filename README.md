# Alpha Starts Now / Website Director

Review-ready premium homepage prototype for Alpha Starts Now, a practical transformation and lifestyle brand for men 35+.

## Run locally

From this folder, run:

    py -m http.server 4173

Open http://localhost:4173.

The page is dependency-light: semantic HTML, project-local generated imagery, CSS tokens, and small vanilla JavaScript. The newsletter form is a local review interaction only. No publishing, deployment, email delivery, or production integrations are configured.

## Page structure

The homepage follows a transformation arc:

- Hero: start where you are, build from here
- Turning point: recognition before instruction
- The Alpha frame: interactive body, health, style, mind, work, and life areas
- Start here: choose a practical first move
- Field notes and recommendations: editorial discovery with affiliate disclosure
- Momentum: a user-controlled progress sequence
- Manifesto and Alpha Briefing: brand memory plus local lead-capture demo

## Local assets

- `assets/asn-hero-cinematic.png` - generated cinematic hero image
- `assets/asn-hero.png` - original hero portrait, retained as a fallback
- `assets/asn-stairwell.png` - framework image
- `assets/asn-reset.png` - editorial still life
- `tokens.css` - portable design tokens
- `favicon.svg` - local Alpha Starts Now mark

The previous `glow-*.png` assets remain in the workspace as historical prototype material and are not referenced by the Alpha Starts Now page.

## Specialist architecture

The bounded control plane remains additive and Website Director remains the authority:

```text
OWNER → WEBSITE DIRECTOR → CURRENT DECISION → ROUTER → NORMALIZED ADAPTER → PINNED KNOWLEDGE
```

Run the implementation checks from the project root:

    node specialists/validate.js
    node --test specialists/tests/architecture.test.js
    npm run benchmark

Do not claim deployment or production readiness. This is isolated local review work.
