# Website Director Visual-First Architecture

<!-- FRAMEWORK_VERSION: 2.15.0 -->

Status: implemented as a bounded, provider-neutral extension of the existing
design-first flow. This document records the architecture, not a website
generation run.

## Final visual-first architecture

```text
OWNER / CLIENT
  -> WEBSITE DIRECTOR
  -> project-local taste_contract
  -> Visual Direction Studio when the ambition tier requires it
  -> existing visual_prototypes owner selection gate
  -> existing implementation engine
  -> existing Browser QA and qualitative Gauntlet authorities
  -> evidence-bound fidelity and pairwise visual evaluation
  -> owner final review
```

There is no Taste Orchestrator, Taste Agent Manager, Taste state machine,
Visual QA service, replacement build engine, client memory system, database,
dashboard, Figma integration, or new owner lock. The canonical owner-lock set
remains the existing five locks.

## Ambition tiers

| Tier | Visual Direction Studio | Owner selection | Motion and interaction |
| --- | --- | --- | --- |
| `STANDARD` | Optional, 0 to 1 concept | Not required by this flow | CSS and micro-interaction by brief |
| `PREMIUM` | Required, 2 divergent concepts | Required before production | Brief-dependent; no automatic specialist |
| `SHOWCASE` | Required, 3 divergent concepts | Required before production | Storyboard and existing specialists only when justified |
| `EXPERIMENTAL` | Required, dynamic concept plus sandbox where needed | Required before production | Interaction-first evidence may precede full code |

Technical tasks route around the taste flow. The router does not load taste
context for bug fixes, backend work, or trivial edits.

## Project Taste Contract

`site-profile.json` remains the canonical project record. Its optional
`taste_contract` object supports the ambition tier, project category and lane,
emotional character, approved and rejected references and traits, anti-taste,
typography lane and personality, material language, visual-world strategy,
motion appetite, density, variance, composition preferences, signature
requirement, and owner direction selection state.

The contract is project-local. References, captures, extracted traits, palette,
typography, visual-world decisions, concepts, and owner selections cannot be
inherited from another project by default. Global materials remain limited to
general composition, typography, motion, responsive, accessibility,
performance, reference-analysis, and anti-default methods.

Typography is source-neutral. Resolution is client-supplied or licensed font,
approved brand font, verified open font, then a curated system stack. No font
vendor is globally injected and no common font is globally banned.

Material language is an explicit project direction, not a premium preset:
`RAW_FLAT`, `SUBTLE_TACTILE`, `CHROMATIC_DEPTH`, and `INTERACTIVE_CANVAS`.

## Visual Direction Studio

The studio combines visual world, typography, first impression, signature
concept when needed, and concept generation in one bounded capability. It does
not create five separately routed taste agents.

Concept representation is selected from project behavior:

- `RASTER_TARGET` for image-led art direction, fashion, luxury, editorial, and campaigns.
- `HTML_CSS_PROTOTYPE` for layout mechanics, responsive structure, and interface behavior.
- `MOTION_STORYBOARD` for scroll, hover, transition, or kinetic language.
- `INTERACTION_SANDBOX` for signature interaction, WebGL, game-like, or procedural work.

Every selectable concept must decompose into semantic regions, layout tracks,
media layers, typography planes, interaction layers, and responsive
interpretation. Impossible topology, gibberish micro-UI, and unanchored floating
interfaces are blocked before the owner gate.

If every feasible candidate is closer to the rejected/category-slop anchor, one
bounded regeneration is allowed. A second failed attempt returns
`VISUAL_DIRECTION_STUDIO = FAIL` and `OWNER_GATE = NOT_REACHED`.

## Owner visual gate

For `PREMIUM`, `SHOWCASE`, and `EXPERIMENTAL`, production implementation is
blocked until the selected concept is feasible, the pairwise precheck is not
closer to the rejected anchor, and the owner explicitly selects and confirms a
direction. The selected direction is recorded under the existing
`visual_prototypes` authority. This flow never lets a builder or critic choose
for the owner and never creates a sixth lock.

## Hot and cold context

The full governance corpus remains intact. The phase compiler emits only the
current phase instruction, current project state, project taste contract,
approved visual target, asset manifest, active tokens, responsive and motion
contract, and current hard constraints. Historical SEO, old benchmark reports,
inactive skills, and unrelated discovery records remain cold unless an
explicit escalation requests them. Character and field counts are recorded;
token counts are left unavailable unless a real measurer is supplied.

## Pairwise visual evaluation

The existing offline evidence-bound evaluator now validates a forced-choice
receipt for each applicable dimension:

```text
A = approved/category-quality anchor
B = rejected/AI-slop anchor
C = candidate browser render
choice = A | B | AMBIGUOUS
discrepancies = exactly 3 observable reasons
```

The dimensions are first impression, typography, composition, visual world and
imagery, craft, memorability, and interaction when applicable. A numeric score
is telemetry only. Pairwise `B` fails, `AMBIGUOUS` blocks, and a missing receipt
never passes. An owner rejection always fails regardless of machine score.

Anchors are category-calibrated. Awwwards references are allowed for a
showcase brief but are not the universal quality bar. Client-approved and
client-rejected references remain the strongest project-local calibration.

## Composition and design-risk policy

The reusable composition primitives are spatial mechanics, not templates. They
do not determine palette, fonts, copy, imagery, section order, brand motifs, or
signature identity. No fixed website layouts were added.

The small structural risk taxonomy emits evidence-bearing `RISK` findings for
default radius uniformity, untracked display typography, generic feature
triads, absent visual worlds or assets, unproven signatures, unobservable
reference traits, target drift, repetitive rhythm, and unmotivated chrome.
Common patterns such as cards, symmetry, flat color, black, white, small type,
rounded corners, and dark mode are not automatic failures when the contract
motivates them.

## Source provenance

Only methods were adapted or recorded. Whole repositories and dependency
graphs were not vendored.

| Source | Commit | Paths and mode | Local capability | License |
| --- | --- | --- | --- | --- |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | `ccbc15639c97057cbfcf32ecebc38ef716e4bb37` | `skills/image-to-code-skill`, `skills/imagegen-frontend-web`, `skills/brandkit` = `CONCEPT_ONLY`; `skills/gpt-tasteskill` = `REJECTED` | Feasibility, realistic web topology, brand-boundary prompts | MIT |
| [MengTo/Skills](https://github.com/MengTo/Skills) | `321c769739b823de5eb94eb3a52aa1974fe783a2` | `design-first-ui-prompting`, `audit-reference-originality` = `ADAPTED`; world generation and capture paths = `CONCEPT_ONLY` or `ON_DEMAND`; universal Awwwards behavior = `REJECTED` | Direction-before-code, trait extraction, originality, rendered evidence | MIT |
| [Imba6/AgentSkills](https://github.com/Imba6/AgentSkills) | `NOT_USED` | Fork of MengTo's source = `REJECTED` | Duplicate skipped; MengTo remains canonical | Not imported |
| [event4u-app/agent-config](https://github.com/event4u-app/agent-config) | `acf1341198a9d9d30c2ba70a3f4b4fad0c8f54f4` | `src/skills/typography-system/SKILL.md` = `CONCEPT_ONLY` | Source-neutral type lane, optical personality, and resolution order | MIT |

Leon defaults such as mandatory AIDA, mandatory GSAP, fixed heroes, mandatory
bento, fixed font lists, and mandatory cinematic motion are not local rules.
MengTo's Awwwards material is not a universal category bar. Event4u's method
does not add a runtime dependency.

## Deferred capabilities

The following remain explicitly deferred: nine-agent Taste bureaucracy, global
font injection, universal texture or shader systems, Figma or Framer, global
taste vectors or embeddings, automatic video-to-code, a new WebGL or motion
engine, a new Browser QA system, a new evaluation database, and a dashboard.

## Alpha Starts Now next experiment specification only

`WD-VISUAL-FIRST-001` is prepared but not executed.

- Project: `ALPHA STARTS NOW`
- Tier: `PREMIUM`
- Work: derive two genuinely divergent directions from the active ASN brief,
  project-local approved and rejected references, owner inspiration, and brand
  constraints.
- Gates: feasibility, category/reference pairwise precheck, then stop for owner
  visual selection.
- No aesthetic labels are predetermined in code.
- No production build, image-generation call, paid provider call, or website
  generation is part of this implementation task.
