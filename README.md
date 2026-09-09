# WEBSITE DIRECTOR

> **Version:** 2.15.0
> **Status:** Active production governance framework
> **Purpose:** Route website work from business understanding to an owner-controlled release while preserving the existing specialist authorities.

<!-- FRAMEWORK_VERSION: 2.15.0 -->

## What it is

Website Director is the repository's design-governance system. It gives an
agent a short operating route, then sends each decision to the existing
protocol, validator, template, registry, and project artifact that owns it.
It is not a website generator, a replacement runtime, or a second approval
system.

The operator-facing route is deliberately seven stages:

```text
UNDERSTAND -> RESEARCH -> DESIGN -> ASSETS -> BUILD -> VERIFY -> RELEASE
```

## Seven-stage operating model

| Stage | Core question | Existing authority family |
| :--- | :--- | :--- |
| UNDERSTAND | What are we building, for whom, why, and under what constraints? | Discovery, Creative Intent, and owner intent |
| RESEARCH | What evidence, market context, and references inform the work? | SEO, Visual Research, bounded inspiration/reference research, and Design Intelligence |
| DESIGN | What does the system look, feel, and behave like, and what did the owner select? | Visual Prototype, IA/content structure, Design System, Motion Direction, Measurement, Security/Privacy, and Accessibility |
| ASSETS | Which assets are usable, authentic, and provenanced? | Asset Director and Evidence Provenance |
| BUILD | How is the approved system implemented? | Implementation Contract, project build, and conditional specialists |
| VERIFY | Does it work, preserve protected work, and survive independent critique? | Framework Validation, Browser & Regression QA, Impeccable, and Website Gauntlet |
| RELEASE | Is the candidate ready for owner-controlled deployment and handoff? | Production preflight, Launch Operations, and Client Handoff |

## Default path

The default path has exactly seven top-level route bundles. A conditional
specialist is dispatched only when actual behavior, content, route, asset, or
ambition evidence requires it.

| Route bundle | Required outcome |
| :--- | :--- |
| UNDERSTAND | Business purpose, audience, outcome, constraints, and owner interpretation recorded |
| RESEARCH | Required evidence and reference-only boundaries recorded |
| DESIGN | Selected direction and derived IA, content, tokens, motion, and planning requirements recorded |
| ASSETS | Required production assets and rights/source evidence recorded |
| BUILD | Local release candidate implements the approved contracts |
| VERIFY | Deterministic behavior and fresh qualitative critique are resolved or honestly blocked |
| RELEASE | Existing launch and handoff authorities record the release boundary |

`DEFAULT_PATH_AUTHORITY_COUNT = 7`. This is a navigation count, not a count
of specialist authorities or registries.

## Conditional capability dispatch

Content Operations and CMS, Localization, Application/Commerce/Authentication,
Immersive Web, Rive, cinematic integration, Page Experience, and signature
choreography remain conditional. `NOT_REQUIRED`, `blocked`, and exception
results stay in their existing authority state. No conditional branch creates
a new protocol, runtime, state object, readiness gate, registry, owner lock,
provider account, or external side effect.

Application behavior is assessed from explicit actors, stories, data, routes,
state changes, and side effects. Industry, company name, geography, IP address,
or stereotype is not a requirement signal.

## Five owner locks

These are the only owner locks, and they remain unchanged:

1. `design_direction_locked`
2. `information_architecture_locked`
3. `content_structure_locked`
4. `design_system_locked`
5. `motion_direction_locked`

Rendered Visual Prototype evidence precedes material direction selection.
`APPROVED_HOMEPAGE_DEFINES_THE_SITE_SYSTEM` remains an existing design-first
invariant, and `visual_prototypes.homepage_visual_approved` remains approval
evidence under the existing Visual Prototype authority, not a new lock or
kernel state. A change to a locked decision requires an explicit owner change
request.

## Verification boundary

Verification has one intentional boundary:

1. Deterministic [Browser & Regression QA](BROWSER-REGRESSION-QA-PROTOCOL.md)
   runs first. It owns machine-observable behavior, accessibility assertions,
   keyboard smoke, responsive behavior, forms, console/network observations,
   measurement observations, and frozen-project integrity.
2. [Website Gauntlet](WEBSITE-GAUNTLET-PROTOCOL.md) runs second. It owns fresh
   qualitative rendered critique against approved Reference Bars and bounded
   refinement.

`browser_qa.complete` and `[BROWSER_QA_PASS]` remain Browser QA's existing
authority. `gauntlet.status` remains the qualitative authority. Browser QA does
not become Gauntlet, and Gauntlet does not duplicate Browser QA. `BUILDER !=
CRITIC` remains mandatory.

## Release boundary

[Launch Operations](LAUNCH-OPERATIONS-PROTOCOL.md) is the single launch
authority. The existing sequence is:

```text
release candidate
  -> [RELEASE_READY]
  -> explicit owner deployment authorization
  -> authorized external deployment
  -> production verification against the known release identity
  -> stabilization
  -> client handoff
```

`launch_ops.complete` is readiness, not deployment. `RELEASE_READY !=
DEPLOYMENT_AUTHORIZED` and `RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED` express the
same boundary. Website Director does not infer authorization, deploy, publish,
change DNS, merge production work, or claim production verification from local
or staging evidence.

## Existing authorities

The seven-stage router points to the deep authorities; it does not absorb
their contracts:

| Concern | Canonical entry point |
| :--- | :--- |
| Core discovery and design | [SKILL.md](SKILL.md), [DISCOVERY-PROTOCOL.md](DISCOVERY-PROTOCOL.md), [VISUAL-PROTOTYPE-PROTOCOL.md](VISUAL-PROTOTYPE-PROTOCOL.md) |
| Research and inspiration | [VISUAL-RESEARCH-PROTOCOL.md](VISUAL-RESEARCH-PROTOCOL.md), [REFERENCE-RECON-PROTOCOL.md](REFERENCE-RECON-PROTOCOL.md), [DESIGN-INTELLIGENCE-PROTOCOL.md](DESIGN-INTELLIGENCE-PROTOCOL.md), [integrations/design-inspiration/ADAPTER.md](integrations/design-inspiration/ADAPTER.md) |
| Design constraints | [CONVERSION-ANALYTICS-PROTOCOL.md](CONVERSION-ANALYTICS-PROTOCOL.md), [SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md](SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md), and [ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md](ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md) |
| Assets and provenance | [ASSET-DIRECTOR-PROTOCOL.md](ASSET-DIRECTOR-PROTOCOL.md), [EVIDENCE-PROVENANCE-PROTOCOL.md](EVIDENCE-PROVENANCE-PROTOCOL.md), [provenance/validator.py](provenance/validator.py) |
| Conditional build architecture | [CONTENT-OPERATIONS-CMS-PROTOCOL.md](CONTENT-OPERATIONS-CMS-PROTOCOL.md), [LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md](LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md), [APPLICATION-COMMERCE-AUTH-PROTOCOL.md](APPLICATION-COMMERCE-AUTH-PROTOCOL.md), [IMMERSIVE-WEB-PROTOCOL.md](IMMERSIVE-WEB-PROTOCOL.md), [RIVE-INTERACTIVE-MOTION-PROTOCOL.md](RIVE-INTERACTIVE-MOTION-PROTOCOL.md), [PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md](PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md) |
| Verification and critique | [FRAMEWORK-VALIDATION-PROTOCOL.md](FRAMEWORK-VALIDATION-PROTOCOL.md), [BROWSER-REGRESSION-QA-PROTOCOL.md](BROWSER-REGRESSION-QA-PROTOCOL.md), [QA-RUBRIC.md](QA-RUBRIC.md), [IMPECCABLE-ENGINE-PROTOCOL.md](IMPECCABLE-ENGINE-PROTOCOL.md), [WEBSITE-GAUNTLET-PROTOCOL.md](WEBSITE-GAUNTLET-PROTOCOL.md) |
| Release and handoff | [PRODUCTION-CHECKLIST.md](PRODUCTION-CHECKLIST.md), [LAUNCH-OPERATIONS-PROTOCOL.md](LAUNCH-OPERATIONS-PROTOCOL.md), [CLIENT-CMS-HANDOFF-PROTOCOL.md](CLIENT-CMS-HANDOFF-PROTOCOL.md) |

Security, Privacy & Compliance remains the canonical design-risk authority.
Its existing `security-privacy-review.md` artifact and
`[SECURITY_PRIVACY_READY]` gate remain intact; Accessibility Intelligence
likewise retains `[ACCESSIBILITY_READY]`. These are specialist readiness
contracts, not owner locks.

## Compatibility and non-goals

The seven stages are a conceptual router. Existing numeric phase metadata,
protocol metadata, state ownership, readiness gates, registries, historical
profiles, and frozen project contracts remain where validators or specialist
authorities consume them. They are not a second top-level workflow.

The current framework version remains 2.15.0. This wave adds no V2.16 or V3,
no new capability, no sixth owner lock, no duplicate runner, and no fields
under a kernel namespace. Version-era detail belongs in the specialist
protocols and compatibility fixtures, not in the active operator route.

## Repository map

- `SKILL.md` is the canonical seven-stage operator router.
- `AGENTS.md` is the repository and execution contract.
- Specialist `*-PROTOCOL.md` files, `schemas/`, `templates/`, and validators
  remain the source of truth for their own authorities.
- `tests/` contains the existing 13-suite framework and governance registry;
  this wave adds routing assertions to that existing framework suite and does
  not increase the suite count.
- `projects/` contains protected fixtures and project work. Framework tests
  must not mutate them.

## Verification

Run from the repository root:

```text
python -m framework_validation --run-suites
node "C:\Users\ALPHA\.context\scripts\verify.js" "<project dir>"
```

Completion claims must distinguish `VERIFIED`, `FAILED`, `UNRUNNABLE`, and
`UNVERIFIED`. A local browser result is not production verification.

## Framework governance marker

<!-- FRAMEWORK_GOVERNANCE
framework_version_source=framework-version.json
owner_locks=design_direction_locked,information_architecture_locked,content_structure_locked,design_system_locked,motion_direction_locked
deployment_authority=OWNER_APPROVAL_REQUIRED
external_side_effects=NONE
state_ownership=schemas/state-ownership.json
browser_qa=browser-qa/guards/frozen_integrity_guard.py
accessibility=owner-controlled historical protocol state
security_privacy=owner-controlled historical protocol state
provenance=provenance.complete
framework_phase=0:Framework Self-Validation:ACTIVE
framework_gate=FRAMEWORK_VALIDATION_PASS
framework_validation_state=EXTERNAL_TO_SITE_PROFILE
localization=localization.complete
application=application.complete
-->
