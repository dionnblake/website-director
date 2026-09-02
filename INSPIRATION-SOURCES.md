# INSPIRATION SOURCES

Website Director uses outside sites to widen research and sharpen a specific
dimension. They are reference material, not templates, production assets, or
permission to copy another site's composition.

## Where to go for ideas

| Source | Best use | Default boundary |
| :--- | :--- | :--- |
| [21st.dev](https://21st.dev/) | Components and interaction ideas: heroes, navigation, CTAs, forms, galleries, scroll patterns, shaders, text effects, and micro-interactions. | `REFERENCE_ONLY`; source reuse requires a license check, provenance record, stack adaptation, and design-system adaptation. |
| [Godly](https://godly.design/) | Trending sites and section inspiration: hero ideas, navigation, CTA and footer treatment, atmosphere, and layout rhythm. | `REFERENCE_ONLY`. |
| [Awwwards](https://www.awwwards.com/) | World-class benchmark sites and dimensional Reference Bars for craft, motion, interaction, and mobile execution. | Existing authority: `AWWWARDS-SHOWCASE-INTELLIGENCE.md`; not a duplicate integration or a clone source. |
| [MotionSites](https://motionsites.ai/) | Animation, background, layering, transition, cinematic-atmosphere, and interaction concepts. | Premium or unavailable prompts/material stay `REFERENCE_ONLY` unless the owner supplies authorized source material. |
| Landbook | Landing-page structures, section rhythm, and responsive composition. | Existing research channel; candidates remain reference-only. |

The complete machine-readable registry is
`templates/inspiration-source-registry.json`. Existing Landbook,
Design Inspiration MCP, Industry Landscape, Cross-Industry, and Reference
Recon channels remain in `RESEARCH-SOURCES.md`.

## How to give Website Director an idea

Give the URL, the exact element or section, what works for this project, and
what must stay with the source. For example:

> “Use this URL as inspiration for the hero motion. I like the way the image
> expands. Do not copy its colors, copy, or typography.”

Website Director records the request inside the existing `research{}` state as
an owner-selected reference, assigns a dimension and a transferable pattern,
records implementation, accessibility, production, license, and provenance
status, and keeps the source `REFERENCE_ONLY` unless authorized reuse is
actually evidenced. “It looks cool” is not a sufficient reason for selection.

No source dictates the implementation framework, model, asset-generation
provider, or deployment host. The workflow routes conceptual roles through
replaceable adapters: `RESEARCH_AGENT`, `BUILDER_AGENT`, `CRITIC_AGENT`,
`ASSET_GENERATION_PROVIDER`, and `DEPLOYMENT_PROVIDER`.

Website Director still owns the design direction, five owner locks, and all
quality gates. Inspiration does not create a new lock or readiness state.
