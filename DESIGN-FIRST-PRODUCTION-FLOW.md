# Website Director: Design-First Production Flow

> **Framework:** 2.15.0
> **Status:** Active bounded operating contract
> **Purpose:** Make the business and the homepage visible before a full website build begins.

This is an operating-flow enhancement inside the existing Website Director
authorities. It adds no capability, phase, provider, framework requirement,
readiness gate, or owner lock. The five owner locks remain exactly:

`design_direction_locked`, `information_architecture_locked`,
`content_structure_locked`, `design_system_locked`, and
`motion_direction_locked`.

This overlay applies to new or deliberately reopened non-frozen work.
Historical profiles and frozen pilots remain valid and are not retrofitted by
a framework upgrade alone.

## The flow in plain English

1. **Understand the business.** Complete the existing
   [Business Understanding Pack](templates/project-brief.md). Record the
   business, target customer, problem, services, boundaries, differentiator,
   owner story, client voice, personality, conversion goals, objections,
   trust, proof, preferences, references, assets, guidelines,
   non-negotiables, and unknown or unverified facts. Never fill a gap with an
   invented claim. Use `UNKNOWN`, `NOT_PROVIDED`, or `UNVERIFIED`.
2. **Choose a discovery mode.** Use `QUESTIONNAIRE_ONLY`,
   `QUESTIONNAIRE_PLUS_TRANSCRIPT`, `TRANSCRIPT_LED_DISCOVERY`, or
   `OWNER_SUPPLIED_DISCOVERY_NOTES`. A transcript is optional. If supplied,
   extract near-verbatim language, recurring terms, register, stories,
   service explanations, and owner priorities. Conversational claims remain
   unverified unless separately evidenced.
3. **Design before implementation.** Research, positioning, SEO, creative
   intent, and the existing Visual Prototype authority still apply. Do not
   start the production build from a blank template, generic marketing copy,
   or an undefined lower-page visual language.
4. **Show a real homepage.** For `PREMIUM` and `SHOWCASE`,
   `FULL_HOMEPAGE_VISUAL_DESIGN_REQUIRED = TRUE`. `EXPERIMENTAL` follows the
   same rule unless a bounded disposable-artifact exception is documented.
   `STANDARD` requires one strong full homepage, or a selected direction
   followed by a complete homepage, before production implementation.
5. **Make the homepage complete enough to judge.** The rendered design covers
   the applicable navigation, hero, value proposition, offers, proof and
   trust, differentiation, process, media language, authentic testimonial
   treatment, objections, CTA progression, FAQ, final CTA, footer, and mobile
   behavior. It shows real type, spacing, grid, color, imagery, geometry,
   motion, rhythm, density, and conversion hierarchy. It contains no Lorem
   Ipsum, fake proof, fake credentials, or fabricated results.
6. **Let the owner see it.** Present real-browser desktop and mobile full-page
   captures and the applicable interactive or reduced-motion states. Internal
   critics may reject or improve the work, but silence, prose, builder output,
   or critic output is never owner approval.
7. **Record the visual decision.** Keep the existing Visual Prototype state
   and record the bounded evidence field
   `visual_prototypes.homepage_visual_approved = true` only after an explicit
   owner `APPROVE` action. This is not a new gate or lock. `REVISE` and
   `HYBRIDIZE` return the work to design review.
8. **Derive the Design System.** Derive typography, colors, spacing, grid,
   controls, surfaces, borders, imagery, icons, navigation, transitions,
   motion physics, CTAs, responsive behavior, and accessibility from the
   approved homepage. The Design System formalizes the approved language; it
   does not reinterpret it.
9. **Implement the rest.** Remaining pages inherit the approved homepage
   system. Components are downstream implementation choices. Existing
   primitives, 21st.dev, CodeStitch, Figma, custom code, or another suitable
   source may be used when stack, license, accessibility, performance,
   maintainability, fidelity, and risk support the choice. None is mandatory,
   and no component library or model may determine the visual direction.
10. **Verify behavior, then quality.** The existing Browser QA harness remains
    the behavior authority. It runs before the existing Website Gauntlet,
    which remains the fresh-context qualitative and visual authority. Real
    screenshot receipts, fresh critics after repair, provenance, and frozen
    project integrity rules remain in force.
11. **Keep the owner in control.** This flow prepares and verifies local
    artifacts only. It does not publish, deploy, configure providers, create
    live users, charge payments, alter DNS, or make production changes.

## Canonical invariants

```text
UNDERSTANDING_PRECEDES_DESIGN
DESIGN_PRECEDES_IMPLEMENTATION
OWNER_SEES_RENDERED_DESIGN_BEFORE_FULL_BUILD
APPROVED_HOMEPAGE_DEFINES_THE_SITE_SYSTEM
```

The production implementation gate requires all of the following evidence:
business understanding complete, owner intent captured, required assets
identified, references interpreted, homepage rendered and reviewed, explicit
owner approval recorded, and a Design System derived and ready. Missing
evidence is `BLOCKED`, not an inferred pass.

## Approval and authority boundaries

- Multiple directions remain divergent until the owner selects, revises, or
  hybridizes them. The selected direction then expands to the complete
  homepage before the Design System and full production build.
- Owner references remain `REFERENCE_ONLY` unless the existing provenance,
  license, stack-adaptation, and Design System rules authorize bounded reuse.
- Assets remain classified as `REQUIRED_ASSET`,
  `REFERENCE_INSPIRATION_ONLY`, or `SUPPORTING_MATERIAL`. Research sources
  never ship implicitly.
- The existing five-lock sequence and all existing Capability 7–10
  authorities remain intact. This contract creates no parallel Visual
  Prototype, Design System, Browser QA, Gauntlet, CMS, localization,
  application, or provenance system.
