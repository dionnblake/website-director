---
name: website-director
description: "Routes Website Director work through seven conceptual stages while preserving the existing specialist authorities, state objects, readiness gates, and five owner locks."
---

# WEBSITE DIRECTOR: SEVEN-STAGE KERNEL

> **Version:** 2.15.0
> **Status:** Active Production Skill
> **Mission:** Give an agent a short, stable route to the existing Website Director authorities without replacing them or creating a second control plane.

<!-- FRAMEWORK_VERSION: 2.15.0 -->

Website Director is a design-governance system for turning a business request into
an evidenced, owner-controlled website release. This file is the operator-facing
router. Deep rules remain in the specialist protocols and their existing
validators, templates, registries, and project artifacts.

The kernel is a mental model, not a runtime subsystem:

```text
UNDERSTAND -> RESEARCH -> DESIGN -> ASSETS -> BUILD -> VERIFY -> RELEASE
```

The kernel creates no `kernel{}` object, no kernel completion flag, no kernel
readiness gate, no registry, and no owner lock. Existing authorities own state
and gates. Exactly 5 owner locks remain immutable.

## Invocation

Invoke the system with:

```text
Activate Website Director for [Company Name].
```

Start with the smallest relevant reading set: this router, the applicable
specialist protocol, the referenced template or registry, and the project-local
DOX. Do not make an agent learn the historical version sequence before it can
locate an authority.

## 1. UNDERSTAND

**Question:** What are we building, for whom, why, and under what owner
constraints?

**Routes to existing authorities:**

- [DISCOVERY-PROTOCOL.md](DISCOVERY-PROTOCOL.md) for progressive business
  understanding, positioning, boundaries, and the Creative Intent Contract.
- Owner intent evidence and the existing Visual Prototype owner-selection
  authority for explicit owner constraints and change requests.
- [IMPLEMENTATION-CONTRACT.md](IMPLEMENTATION-CONTRACT.md) only where it
  records the already-approved information and content contracts.

**Exit condition:** The business purpose, audience, outcome, constraints, and
owner interpretation are recorded. The owner has confirmed the interpretation
before external research begins. Information architecture and content structure
are designed and locked during the DESIGN stage, after the selected direction,
so the existing dependency order is preserved.

**Owner stop:** An unclear or disputed assignment stops for owner clarification;
an agent must not fill a material business or brand gap by guessing.

## 2. RESEARCH

**Question:** What external evidence, references, market context, and visual
intelligence inform the work?

**Routes to existing authorities:**

- [SEO-INTELLIGENCE-PROTOCOL.md](SEO-INTELLIGENCE-PROTOCOL.md) for search and
  competitive intelligence.
- [VISUAL-RESEARCH-PROTOCOL.md](VISUAL-RESEARCH-PROTOCOL.md),
  [RESEARCH-SOURCES.md](RESEARCH-SOURCES.md), and
  [REFERENCE-RECON-PROTOCOL.md](REFERENCE-RECON-PROTOCOL.md) for visual and
  reference research.
- [integrations/design-inspiration/ADAPTER.md](integrations/design-inspiration/ADAPTER.md)
  for bounded, reference-only discovery transport.
- [AWWWARDS-SHOWCASE-INTELLIGENCE.md](AWWWARDS-SHOWCASE-INTELLIGENCE.md) only
  when the project's ambition requires showcase benchmarking.
- [DESIGN-INTELLIGENCE-PROTOCOL.md](DESIGN-INTELLIGENCE-PROTOCOL.md) for
  candidate synthesis from the existing UI/UX Pro Max intelligence.

**Exit condition:** Required research artifacts are complete, source identity
and reference-only boundaries are explicit, and research findings are ready to
inform DESIGN. Research can recommend; it cannot silently select a direction,
change locked copy, or become production provenance.

## 3. DESIGN

**Question:** What does the site look, feel, and behave like, and what did the
owner select?

**Routes to existing authorities:**

- [VISUAL-PROTOTYPE-PROTOCOL.md](VISUAL-PROTOTYPE-PROTOCOL.md) for rendered
  concepts, comparison, owner selection, and progression.
- [DESIGN-ARCHETYPES.md](DESIGN-ARCHETYPES.md),
  [DESIGN-CONSTITUTION.md](DESIGN-CONSTITUTION.md), and
  [IMPLEMENTATION-CONTRACT.md](IMPLEMENTATION-CONTRACT.md) for derived
  information architecture, content structure, and implementation constraints.
- [DESIGN-SYSTEM-PROTOCOL.md](DESIGN-SYSTEM-PROTOCOL.md) for derived tokens,
  typography, geometry, and component rules.
- [MOTION-DIRECTION-PROTOCOL.md](MOTION-DIRECTION-PROTOCOL.md) for deliberate
  motion direction, including a valid static outcome.
- During content-structure and production-copy finalization, use
  `framework_validation/copy_quality.py` for a bounded pre-lock review of
  supplied known-locale English copy before `content_structure_locked`.
  Provenance verifies applicable claims, then the owner reviews final
  production copy. The scanner emits review evidence only; it does not score,
  rewrite, observe rendered text, or add lifecycle authority.
- [CONVERSION-ANALYTICS-PROTOCOL.md](CONVERSION-ANALYTICS-PROTOCOL.md),
  [SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md](SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md),
  and [ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md](ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md)
  for requirements that inform the design and build contracts. Their
  existing `templates/security-privacy-review.md`, `[SECURITY_PRIVACY_READY]`
  (`GATE SECURITY`), and `[ACCESSIBILITY_READY]` (`GATE ACCESSIBILITY`) gates
  remain specialist readiness contracts; their post-build checks remain in
  VERIFY.

**Owner selection and locks:** Rendered evidence must precede a material visual
  direction choice. `APPROVED_HOMEPAGE_DEFINES_THE_SITE_SYSTEM` and
  `visual_prototypes.homepage_visual_approved` remain existing project evidence,
  not kernel state. The five existing locks are engaged by their owning
  authority; a change to an engaged decision becomes an owner change request.

**Exit condition:** The selected direction, IA, content structure, design
system, motion direction, and applicable planning requirements are recorded
with the existing five locks and specialist readiness states. No kernel lock
is added.

## 4. ASSETS

**Question:** What production assets are required, and are they usable,
authentic, and provenanced?

**Routes to existing authorities:**

- [ASSET-DIRECTOR-PROTOCOL.md](ASSET-DIRECTOR-PROTOCOL.md) for art direction,
  asset intent, production readiness, responsive crops, authenticity, and
  master-versus-web separation.
- [EVIDENCE-PROVENANCE-PROTOCOL.md](EVIDENCE-PROVENANCE-PROTOCOL.md) and
  [provenance/validator.py](provenance/validator.py) for claim, source, rights,
  attribution, reference-only, and hash identity.

**Exit condition:** Required assets have an existing Asset Director readiness
  result and required claims, sources, and rights are recorded by Provenance.
  A missing or unverified asset is blocked or explicitly `PROTOTYPE_ONLY`; it is
  never silently treated as production-ready.

## 5. BUILD

**Question:** How is the approved system implemented, including only the
conditional functionality the evidence requires?

**Routes to existing authorities:**

- [IMPLEMENTATION-CONTRACT.md](IMPLEMENTATION-CONTRACT.md) for the binding
  builder contract and [templates/implementation-contract.md](templates/implementation-contract.md)
  for the project artifact.
- The project implementation for the actual site build.
- Conditional specialist dispatch below for content operations, localization,
  application behavior, page experience, immersive WebGL, Rive, cinematic
  production, signature choreography, and GSAP implementation.

**Exit condition:** The approved design, content, asset, motion, security,
accessibility, measurement, and conditional-functionality contracts are
implemented in a local release candidate. A build does not authorize
publishing, deployment, or production verification.

## 6. VERIFY

**Question:** Does the implementation work deterministically, preserve the
protected corpus, and survive independent rendered critique?

**Sequence and ownership:**

1. [FRAMEWORK-VALIDATION-PROTOCOL.md](FRAMEWORK-VALIDATION-PROTOCOL.md) and
   `framework_validation/` verify framework structure, registries, schemas,
   compatibility, isolation, and protected-project integrity.
2. [BROWSER-REGRESSION-QA-PROTOCOL.md](BROWSER-REGRESSION-QA-PROTOCOL.md) and
   `browser-qa/` own deterministic browser execution, evidence, responsive
   behavior, forms, console/network, measurement, security-observable behavior,
   accessibility assertions, reduced motion, keyboard smoke, and visual
   regression. This is the `GATE BROWSER` boundary and `[BROWSER_QA_PASS]` is
   still `browser_qa.complete`.
3. Specialist deterministic validators contribute their own checks. They do
   not create a second verification state machine or duplicate another owner.
4. [QA-RUBRIC.md](QA-RUBRIC.md) and [IMPECCABLE-ENGINE-PROTOCOL.md](IMPECCABLE-ENGINE-PROTOCOL.md)
   own deterministic design scans and design-quality review.
5. [WEBSITE-GAUNTLET-PROTOCOL.md](WEBSITE-GAUNTLET-PROTOCOL.md) owns fresh,
   qualitative rendered critique against approved Reference Bars and targeted
   refinement. `BUILDER != CRITIC` remains mandatory.

**Boundary:** Browser QA proves machine-observable behavior first. Gauntlet
  critiques rendered quality second. Browser QA must not become Gauntlet, and
  Gauntlet must not duplicate Browser QA. A missing engine or evidence is
  `BLOCKED`, and a flaky run is not a pass.

**Exit condition:** Required deterministic checks pass with protected-project
  integrity intact, then the fresh qualitative review is resolved or recorded
  with its allowed exception. Verification never changes an owner lock silently.

## 7. RELEASE

**Question:** Is the candidate ready for an explicit owner-controlled launch
boundary and durable handoff?

**Sequence and ownership:**

```text
candidate ready
  -> launch readiness
  -> explicit owner deployment authority
  -> external deployment by an authorized actor
  -> production verification against the known release identity
  -> stabilization
  -> client handoff
```

- [PRODUCTION-CHECKLIST.md](PRODUCTION-CHECKLIST.md) establishes the release
  candidate preflight.
- [LAUNCH-OPERATIONS-PROTOCOL.md](LAUNCH-OPERATIONS-PROTOCOL.md) and
  [launch-ops/validator.py](launch-ops/validator.py) are the one canonical
  launch authority. This is the `GATE LAUNCH` boundary, and `[RELEASE_READY]`
  is `launch_ops.complete`.
- `RELEASE_READY != DEPLOYMENT_AUTHORIZED` and `RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED` express the same boundary. Website Director does not infer authorization and does not deploy, push, merge, change DNS, or alter a live system. An authorized external actor performs deployment after the explicit owner decision.
- Production verification must prove the known release identity on the
  production surface. Local or staging evidence is not production proof.
- [CLIENT-CMS-HANDOFF-PROTOCOL.md](CLIENT-CMS-HANDOFF-PROTOCOL.md) owns durable
  client operations and handoff acceptance after Launch Operations transfers
  its record.

**Exit condition:** Release state, deployment authorization, production
verification, stabilization, and handoff are each recorded by their existing
authorities. The kernel never creates a release state machine.

## Default path

For a normal static marketing site, the top-level route is:

```text
UNDERSTAND -> RESEARCH -> DESIGN -> ASSETS -> BUILD -> VERIFY -> RELEASE
```

`DEFAULT_PATH_AUTHORITY_COUNT = 7` counts route bundles, not specialists.
Conditional specialists are dispatched only when their activation evidence exists.

## Conditional capability dispatch

Conditional work is assessed from actual behavior, stories, assets, route
requirements, or selected ambition. Use the existing authority's
`NOT_REQUIRED`, `blocked`, or exception result; never invent a shared skip state
or install a provider merely because a capability exists.

Read the linked specialist only when its evidence activates it:

- Content operations/CMS: `CONTENT-OPERATIONS-CMS-PROTOCOL.md` and `content-ops/`.
- Localization: `LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md` and `localization/`.
- Application, commerce, or authentication: `APPLICATION-COMMERCE-AUTH-PROTOCOL.md` and `application/`.
- Immersive Web, Rive, cinematic integration, page experience, or signature
  choreography: the corresponding BUILD protocol and child authority.

No conditional branch creates a protocol, registry, capability, state object,
readiness gate, owner lock, or second runner.

## Existing capability routing map

Each surviving capability has exactly one primary kernel stage. Secondary
dependencies describe existing cross-stage consumption; they do not transfer
state ownership.

<!-- KERNEL_CAPABILITY_ROUTING_START -->
| Capability | Current authority | Primary stage | Secondary dependencies | Required or conditional | Current state object | Current gate | Owner-lock interaction | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| framework_validation | `framework_validation/` and `FRAMEWORK-VALIDATION-PROTOCOL.md` | VERIFY | All repository authorities and protected paths | Required for framework certification | `framework_validation.status` | `FRAMEWORK_VALIDATION_PASS` | None | Proves framework integrity. |
| website_director_core | `README.md` and the existing five-lock contract | DESIGN | UNDERSTAND; Visual Prototype; Design System; Motion Direction; RELEASE | Required | `locks.*` | Existing owner-lock gates | Owns all five existing owner locks and owner approval | Cross-cutting lifecycle and lock authority. |
| discovery_business_understanding | `DISCOVERY-PROTOCOL.md` | UNDERSTAND | Owner intent; later research | Required | `creative_intent.confirmed` | `CREATIVE_INTENT_CONFIRMED` | None | Defines the business problem before research. |
| owner_intent | Existing owner-intent contract and Visual Prototype owner review | UNDERSTAND | DESIGN selection and all locks | Required owner action | Owner-intent artifact; no kernel state | None | Owner authority is preserved; no new lock | Owner constraints are the input boundary. |
| information_architecture | `IMPLEMENTATION-CONTRACT.md` and IA project artifact | DESIGN | UNDERSTAND; selected visual direction | Required | `locks.information_architecture_locked` | `INFORMATION_ARCHITECTURE_LOCKED` | Lock 2, owner approval | Derived design lock. |
| content_structure | `IMPLEMENTATION-CONTRACT.md` and content project artifact | DESIGN | UNDERSTAND; IA; Provenance | Required | `locks.content_structure_locked` | `CONTENT_STRUCTURE_LOCKED` | Lock 3, owner approval | Approved experience and evidence chain. |
| seo | `SEO-INTELLIGENCE-PROTOCOL.md` | RESEARCH | UNDERSTAND; DESIGN; RELEASE | Required for current production planning | `seo.complete` | `SEO_COMPLETE` | None | Search and market evidence informs the experience. |
| visual_research | `VISUAL-RESEARCH-PROTOCOL.md` | RESEARCH | UNDERSTAND; DESIGN; Provenance | Required | `research.complete` | `RESEARCH_COMPLETE` | None | Research evidence, not design authority. |
| external_inspiration_reference_research | `REFERENCE-PROTOCOL.md` and `REFERENCE-RECON-PROTOCOL.md` | RESEARCH | Provenance; DESIGN | Conditional to reference work | `research.complete` and reference artifacts | Existing research readiness | None | Research-only; no copied composition or asset. |
| design_inspiration_adapter | `integrations/design-inspiration/ADAPTER.md` | RESEARCH | Visual Research; Awwwards interpretation; Provenance | Conditional transport | `research.complete` | Existing research readiness | None | Acquires bounded evidence; no design choice. |
| awwwards_showcase_benchmarking | `AWWWARDS-SHOWCASE-INTELLIGENCE.md` | RESEARCH | Visual Research; Visual Prototype | Conditional to SHOWCASE ambition | `visual_prototypes.showcase_research` | None | None | Craft benchmark; not direction selection. |
| design_intelligence | `DESIGN-INTELLIGENCE-PROTOCOL.md` and `intelligence/ui-ux-pro-max/` | RESEARCH | Visual Research; DESIGN | Required for current synthesis | `design_intelligence.complete` | `DESIGN_INTELLIGENCE_COMPLETE` | None | Research intelligence; not a sixth lock. |
| archetype_synthesis | `DESIGN-ARCHETYPES.md` and `DESIGN-CONSTITUTION.md` | DESIGN | Research; owner intent | Required for a deliberate direction | No independent state object | None | Feeds Lock 1 | Design reasoning aid; not lifecycle authority. |
| visual_direction | `DESIGN-CONSTITUTION.md` and existing direction artifact | DESIGN | Research; owner intent; Visual Prototype | Required | `locks.design_direction_locked` | `DESIGN_DIRECTION_LOCKED` | Lock 1, owner approval | Records the selected visual language. |
| visual_prototype | `VISUAL-PROTOTYPE-PROTOCOL.md` | DESIGN | Research; owner intent; assets; design system | Required before material direction selection | `visual_prototypes.owner_selection_confirmed` | `VISUAL_PROTOTYPES_OWNER_READY` | Engages Lock 1 after owner selection | Owner selects from rendered evidence. |
| design_system | `DESIGN-SYSTEM-PROTOCOL.md` | DESIGN | IA; content; security; accessibility; provenance; motion | Required | `locks.design_system_locked` | `DESIGN_SYSTEM_LOCKED` | Lock 4, owner approval | Tokens derive from approved constraints. |
| motion_direction | `MOTION-DIRECTION-PROTOCOL.md` | DESIGN | Owner intent; design system; accessibility; Build | Required, including a static verdict | `locks.motion_direction_locked` | `MOTION_DIRECTION_LOCKED` | Lock 5, owner approval | Intentional design direction, not convenience. |
| measurement_analytics | `CONVERSION-ANALYTICS-PROTOCOL.md` | DESIGN | UNDERSTAND; Build; VERIFY; Release | Required when goals have observable conversion behavior | `measurement.complete` | `CONVERSION_MEASUREMENT_COMPLETE` | None | Measurement informs experience and verification. |
| security_privacy | `SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md` | DESIGN | UNDERSTAND; Build; VERIFY; Release | Required by actual site risk and data flows | `security_privacy.complete` | `SECURITY_PRIVACY_READY` | None | Risk and safeguards constrain design and build. |
| accessibility | `ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md` | DESIGN | Design System; Motion; Build; VERIFY | Required for applicable public functionality | `accessibility.complete` | `ACCESSIBILITY_READY` | None | Requirements shape the system; runtime checks stay in VERIFY. |
| asset_director | `ASSET-DIRECTOR-PROTOCOL.md` | ASSETS | DESIGN; Provenance; Build | Required when visual assets exist | `assets.status` | `ASSET_DIRECTION_READY` | None | Owns art-directed production assets. |
| provenance | `EVIDENCE-PROVENANCE-PROTOCOL.md` and `provenance/validator.py` | ASSETS | Research; Asset Director; VERIFY; Release | Required for claims, assets, and references in scope | `provenance.complete` | `EVIDENCE_PROVENANCE_READY` | None | Owns rights, source, claim, and hash identity. |
| implementation_contract | `IMPLEMENTATION-CONTRACT.md` | BUILD | DESIGN; Assets; conditional dispatch | Required | `implementation.contract` artifact | None | Consumes all engaged locks | Turns approvals into build constraints. |
| build_execution | Project implementation surface | BUILD | Implementation Contract; Assets; conditional specialists | Required | Project build state | None | Cannot silently change an engaged lock | Implements the approved system and creates the candidate. |
| gsap_motion_engineering | `GSAP-IMPLEMENTATION-PROTOCOL.md` and `intelligence/gsap-skills/` | BUILD | Motion Direction; Design System; Browser QA | Conditional when JavaScript motion is required | `motion.gsap_required` | None | Consumes Lock 5 | Implementation engine under motion authority. |
| cinematic_integration | `CINEMATIC-INTEGRATION-PROTOCOL.md` | BUILD | Motion Direction; Assets; Provenance; VERIFY | Conditional | `motion.cinematic_brief_complete` | None | Consumes Locks 1, 4, and 5 | Bounded builder specialist. |
| signature_choreography | Existing signature choreography registry and motion authority | BUILD | Motion Direction; Build; VERIFY | Conditional | `signature_choreography.status` | None | Consumes Lock 5 | Meaningful spatial choreography under motion authority. |
| content_cms_operations | `CONTENT-OPERATIONS-CMS-PROTOCOL.md` and `content-ops/validator.py` | BUILD | Content Structure; Provenance; Localization; Handoff | Conditional | `content_ops.complete` | `CONTENT_OPERATIONS_READY` | None | Provider-neutral editorial architecture. |
| localization | `LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md` and `localization/validator.py` | BUILD | Content Operations; SEO; Accessibility; Measurement; Provenance; Handoff | Conditional | `localization.complete` | `LOCALIZATION_READY` | None | Explicit requirements dispatch locale behavior. |
| application_commerce_auth | `APPLICATION-COMMERCE-AUTH-PROTOCOL.md` and `application/validator.py` | BUILD | UNDERSTAND; Security; Measurement; Accessibility; Release | Conditional | `application.complete` | `APPLICATION_ARCHITECTURE_READY` | None | Assesses stateful behavior before build. |
| immersive_web | `IMMERSIVE-WEB-PROTOCOL.md` | BUILD | Assets; Motion; Accessibility; Browser QA; Provenance | Conditional | `immersive.status` | `IMMERSIVE_IMPLEMENTATION_READY` | None | Spatial specialist only when justified. |
| rive | `RIVE-INTERACTIVE-MOTION-PROTOCOL.md` | BUILD | Motion; Accessibility; Assets; Browser QA | Conditional | `rive.status` | `RIVE_IMPLEMENTATION_READY` | None | State-machine specialist, not a top-level route. |
| page_experience | `PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md` | BUILD | IA; Motion; Browser QA; Release | Conditional | `page_experience.status` | `TRANSITION_READY` | None | Route continuity only when needed. |
| browser_qa | `BROWSER-REGRESSION-QA-PROTOCOL.md` and `browser-qa/` | VERIFY | Measurement; Security; Accessibility; Assets; Build | Required for the built artifact | `browser_qa.complete` | `BROWSER_QA_PASS` | None | Deterministic browser evidence and frozen integrity. |
| design_qa_impeccable | `QA-RUBRIC.md` and `IMPECCABLE-ENGINE-PROTOCOL.md` | VERIFY | Design System; Motion; Browser QA; Gauntlet | Required quality review | `qa_status.design_qa_verdict` | None | Reviews, never adds a lock | Deterministic design scan, not runtime authority. |
| website_gauntlet | `WEBSITE-GAUNTLET-PROTOCOL.md` | VERIFY | Browser QA; owner intent; references; design system | Required for governed quality review | `gauntlet.status` | `GAUNTLET_PASS` | Respects all five locks | Fresh qualitative critique after deterministic checks. |
| production_preflight | `PRODUCTION-CHECKLIST.md` | RELEASE | Verify; Launch Operations; Provenance | Required for a release candidate | `qa_status.production_preflight_passed` | None | No deployment authority | Prepares the candidate for release. |
| launch_operations | `LAUNCH-OPERATIONS-PROTOCOL.md` and `launch-ops/validator.py` | RELEASE | Verify; Security; Accessibility; Measurement; Browser QA; Handoff | Required for launch planning | `launch_ops.complete` and `launch_ops.status` | `RELEASE_READY` | None | Single release and production-state owner. |
| client_handoff | `CLIENT-CMS-HANDOFF-PROTOCOL.md` | RELEASE | Content Operations; Localization; Launch Operations; owner acceptance | Conditional to durable client operations | `handoff.status` | `CLIENT_HANDOFF_READY` | None | Transfers durable operations without deployment authority. |
<!-- KERNEL_CAPABILITY_ROUTING_END -->

`PRIMARY_STAGE` is a routing label only. It does not rename a protocol, move a
state writer, or authorize a specialist to write another authority's state.

## Five owner locks

The kernel exposes no owner lock of its own. The existing five locks remain the
only owner authority:

| Owner lock | Kernel stage | Lock owner | Engagement point | Unlock or change rule |
| :--- | :--- | :--- | :--- | :--- |
| `design_direction_locked` | DESIGN | Website Director Core and owner | After rendered Visual Prototype comparison and owner selection | Only an explicit owner change request can reopen or replace it. |
| `information_architecture_locked` | DESIGN | Website Director Core and owner | After IA is derived from the selected direction | Locked IA changes halt the current work and require owner review. |
| `content_structure_locked` | DESIGN | Website Director Core and owner | After content structure and evidence plan are approved | Locked content changes halt the current work and require owner review. |
| `design_system_locked` | DESIGN | Website Director Core and owner | After tokens are derived from approved direction and requirements | Locked token changes require an owner change request. |
| `motion_direction_locked` | DESIGN | Website Director Core and owner | After deliberate motion direction and implementation requirements | Locked motion changes require an owner change request. |

`OWNER_LOCK_COUNT = 5`. Readiness and verification gates are not owner locks.

## State and authority boundaries

- The authorities in the routing map retain their existing protocols, validators,
  state objects, gates, registries, and templates. The kernel has no namespace or
  completion fields.
- `browser_qa.complete` is the sole Browser QA readiness flag;
  `gauntlet.status` owns qualitative refinement; `provenance.complete` owns
  evidence and asset provenance; none becomes an owner lock.
- `launch_ops.complete` and `launch_ops.status` are the sole launch authority;
  `[RELEASE_READY]` never implies deployment authorization.
- Conditional capabilities keep their local `NOT_REQUIRED`, `blocked`, and
  exception behavior. The router creates no common conditional state.

### Single-Source-of-Truth Rule for `security_privacy` State

`security_privacy.complete` and its implementation and production-verification
fields remain owned by Security, Privacy & Compliance. Other stages consume its
contract; none creates a parallel security state.

### Single-Source-of-Truth Rule for `accessibility` State

`accessibility.complete` and its verification fields remain owned by
Accessibility Intelligence. Browser QA consumes applicable runtime assertions;
the kernel creates no accessibility state or owner lock.

### Single-Source-of-Truth Rule for `browser_qa` State

`browser_qa.complete` is the only Browser QA readiness flag. The existing runner
and FrozenIntegrityGuard own its evidence and protected-project integrity;
Gauntlet and Launch Operations consume the result.

### Single-Source-of-Truth Rule for `launch_ops`

`launch_ops.complete` and `launch_ops.status` are the single release and
production-state authority. No kernel field, second launch state machine, or
implicit deployment authorization may be introduced.

## Specialist references

Use the deep protocol only after the stage router identifies the authority:

| Authority | Deep rule |
| :--- | :--- |
| Discovery and core locks | [DISCOVERY-PROTOCOL.md](DISCOVERY-PROTOCOL.md), [DESIGN-CONSTITUTION.md](DESIGN-CONSTITUTION.md) |
| SEO and visual research | [SEO-INTELLIGENCE-PROTOCOL.md](SEO-INTELLIGENCE-PROTOCOL.md), [VISUAL-RESEARCH-PROTOCOL.md](VISUAL-RESEARCH-PROTOCOL.md), [REFERENCE-RECON-PROTOCOL.md](REFERENCE-RECON-PROTOCOL.md) |
| Visual prototype and design | [VISUAL-PROTOTYPE-PROTOCOL.md](VISUAL-PROTOTYPE-PROTOCOL.md), [DESIGN-SYSTEM-PROTOCOL.md](DESIGN-SYSTEM-PROTOCOL.md), [MOTION-DIRECTION-PROTOCOL.md](MOTION-DIRECTION-PROTOCOL.md) |
| Assets and evidence | [ASSET-DIRECTOR-PROTOCOL.md](ASSET-DIRECTOR-PROTOCOL.md), [EVIDENCE-PROVENANCE-PROTOCOL.md](EVIDENCE-PROVENANCE-PROTOCOL.md) |
| Conditional build specialists | [CONTENT-OPERATIONS-CMS-PROTOCOL.md](CONTENT-OPERATIONS-CMS-PROTOCOL.md), [LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md](LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md), [APPLICATION-COMMERCE-AUTH-PROTOCOL.md](APPLICATION-COMMERCE-AUTH-PROTOCOL.md), [IMMERSIVE-WEB-PROTOCOL.md](IMMERSIVE-WEB-PROTOCOL.md), [RIVE-INTERACTIVE-MOTION-PROTOCOL.md](RIVE-INTERACTIVE-MOTION-PROTOCOL.md), [PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md](PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md), [CINEMATIC-INTEGRATION-PROTOCOL.md](CINEMATIC-INTEGRATION-PROTOCOL.md) |
| Measurement, security, and accessibility | [CONVERSION-ANALYTICS-PROTOCOL.md](CONVERSION-ANALYTICS-PROTOCOL.md), [SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md](SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md), [ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md](ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md) |
| Verification and critique | [FRAMEWORK-VALIDATION-PROTOCOL.md](FRAMEWORK-VALIDATION-PROTOCOL.md), [BROWSER-REGRESSION-QA-PROTOCOL.md](BROWSER-REGRESSION-QA-PROTOCOL.md), [QA-RUBRIC.md](QA-RUBRIC.md), [IMPECCABLE-ENGINE-PROTOCOL.md](IMPECCABLE-ENGINE-PROTOCOL.md), [WEBSITE-GAUNTLET-PROTOCOL.md](WEBSITE-GAUNTLET-PROTOCOL.md) |
| Release and operations | [PRODUCTION-CHECKLIST.md](PRODUCTION-CHECKLIST.md), [LAUNCH-OPERATIONS-PROTOCOL.md](LAUNCH-OPERATIONS-PROTOCOL.md), [CLIENT-CMS-HANDOFF-PROTOCOL.md](CLIENT-CMS-HANDOFF-PROTOCOL.md) |

## Compatibility

Numeric phases and historical identifiers remain in the canonical schemas,
profiles, validators, and specialist contracts that consume them. They do not
replace the seven-stage operator route or trigger automatic specialist loading.

## Verification contract

Run the existing registered suite path from the repository root:

```text
python -m framework_validation --run-suites
```

This executes the 13 active registered suites. Use the global verifier as a
separate evidence source:

```text
node "C:\Users\ALPHA\.context\scripts\verify.js" "<project dir>"
```

The final claim must distinguish `VERIFIED`, `FAILED`, `UNRUNNABLE`, and
`UNVERIFIED`. A local browser run is not production verification. Never mutate
`projects/`; the existing `FrozenIntegrityGuard` is authoritative for protected
project integrity.

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
