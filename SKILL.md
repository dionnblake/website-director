---
name: website-director
description: "Owner-controlled website specification and implementation through seven gates, explicit specialist activation, and inspectable evidence."
---

# Website Director resident kernel

> **Version:** 2.15.0
<!-- FRAMEWORK_VERSION: 2.15.0 -->

## Mission and scope

Use a small resident kernel, one lifecycle router, and explicitly activated specialists.
FEATURE_FREEZE = ACTIVE. This branch is refactor/kernel: reduction only.
No new capability, specialist, protocol, readiness gate, design engine, or feature version.
Website generation, ASN generation, and production changes are frozen during this refactor.
Regression uses synthetic fixtures only. Do not integrate external creative engines.
The resident kernel is this file. Do not preload the protocol catalog, README history,
specialist manuals, old projects, or another consolidated operating manual.

## Seven-gate lifecycle

BRIEF → DIRECTION → IA → CONTENT → BUILD → VERIFY → LAUNCH

| Gate | Required handoff | Owner boundary |
| --- | --- | --- |
| BRIEF | Business truth, owner intent, approved brand constants, assets, references, unknowns | Confirm creative intent; no invented facts |
| DIRECTION | Three desktop hero plus signature-device concepts from actual external screenshots | Owner selects; record design_direction_locked |
| IA | Selected direction, route/section purpose and navigation | Owner records information_architecture_locked |
| CONTENT | Factual copy, evidence plan, applicable internal requirement assessments | Owner records content_structure_locked |
| BUILD | Expand selected direction to homepage; review desktop/mobile; derive tokens and motion; implement | Owner approves homepage, design_system_locked and motion_direction_locked before full-site implementation |
| VERIFY | Requirement-traced static, browser, manual and post-render findings | Repairs affecting a lock return to owner; no silent re-lock |
| LAUNCH | Known release identity, release checklist, authorization request, operations handoff | Explicit per-release authorization before consequential action |

Decimal phases in specialist documents and schemas/phases.json are internal activity
identifiers for compatibility. They are not additional top-level gates or a mandatory
sequence of specialist loads. schemas/phases.json records their containing gate.
Internal readiness does not create owner approval or grow this lifecycle.
Framework self-validation is VERIFY work on the framework, outside site-profile state.

## Owner authority

Exactly 5 owner locks remain immutable:
design_direction_locked, information_architecture_locked, content_structure_locked,
design_system_locked, motion_direction_locked. Only the owner writes these locks.
The canonical names and writers live in schemas/state-ownership.json.
Current owner intent controls; historical output is evidence, never current authority.
Approved brand/locks, required safety/accessibility, and factual evidence constrain work.
Conflicts requiring a changed lock produce an owner change request, never silent override.
Critics, modules, a score, silence, and passing tests cannot approve a direction or release.
Never deploy/push/merge/DNS without explicit authorization. Also require authorization
for publishing, purchases, credentials, live accounts/payments, real messages, and deletion.
This task authorizes one certified branch commit and push; it does not authorize merge.

## Canonical evidence and state semantics

Reuse schemas/state-ownership.json; do not invent an additional state system.
Each existing module retains its domain record and one canonical completion owner.
complete != implementation_verified; implementation_verified != production_verified.
Planning complete means required planning artifacts exist, not that execution occurred.
Implementation verification requires the actual target implementation and named evidence.
Production verification requires the known deployed release on its production surface.
Localhost, staging, synthetic adapters and simulation never establish production verification.
Never fabricate sources, evidence, benchmarks, metrics, screenshots, tests, or certification.
BASELINE = UNKNOWN until an explicit baseline is supplied and verified. Missing is not PASS.
FLAKY != PASS. Unavailable engine = BLOCKED. Unknown or incomplete evidence fails closed.
Use PASS, FAIL, FLAKY, BLOCKED, NOT_APPLICABLE as existing per-check verdicts.
NOT_APPLICABLE requires an evidence-backed applicability decision; omission is not exemption.
Preserve evidence methods: DETERMINISTIC, HEURISTIC, LLM_CRITIQUE, VISUAL_COMPARISON,
and BROWSER_EXECUTED. A method label never proves an execution happened.
Owner review, manual review, simulation, and production evidence remain distinguishable.
Never assert "GDPR COMPLIANT", "WCAG COMPLIANT", or "ADA COMPLIANT" from these checks.
State exactly which criteria, surface, engine, limitations, and evidence were evaluated.
No provider is required by default. Preserve offline/provider-neutral execution;
unavailable required integrations remain BLOCKED, not replaced with invented results.

## Initial DIRECTION contract

Clean-Room Manifest + actual external reference screenshots + business brief + owner intent
+ approved brand constants/assets → DIRECT_REFERENCE_BUILDER → three cheap concepts
→ owner selection. Each concept contains one desktop hero and one signature device.
CREATIVE_AUTHORITIES_ACTIVE_AT_DIRECTION = 1. No extra creative skill is active by default.
The controller calls framework_validation.clean_room.prepare_clean_room_concept_run.
It validates and stages the allowlisted pack before invoking the builder. The active
builder receives actual staged reference screenshots, not only URLs or textual summaries.
Historical source, generated screenshots, old design systems and project folders stay
quarantined. Approved assets require individual allowlisting; never bulk-copy a project.
Staged isolation is structural context isolation, not an OS filesystem sandbox.
Morphology and blind-critic review occur after rendering in separate context and never
feed initial generation. No Gauntlet instructions are sent to the concept builder.
Initial generation excludes UI/UX Pro Max, Anthropic Frontend Design, Awwwards synthesis,
Asset Director, Cinematic Integration, GSAP, Rive, Three.js/Immersive, Lenis, Page Experience,
Gauntlet, morphology feedback, CRO/analytics and SEO design guidance, accessibility and
security/privacy implementation guidance, and launch/handoff guidance.
The business brief may state conversion goals and non-negotiables without loading modules.
After selection, preserve APPROVED_HOMEPAGE_DEFINES_THE_SITE_SYSTEM:
BUILD expands the selected concept to a complete browser-rendered homepage, obtains
visual_prototypes.homepage_visual_approved, and derives the Design System before the rest.
Use Website Director's browser-rendered Visual Prototype system.
FIGMA_IN_DESIGN_FIRST_FLOW = NO.

## Authoritative activation table

All modules default INACTIVE. This is the only activation table; inventories are evidence.
Activate by explicit request at the listed gate only when every predicate fact is true.
Facts are literal booleans backed by the input contract, not strings or inferred approval.
`&` means all facts; `-` means no module exclusion. No dynamic imports or provider calls
occur during routing. Read only the returned module document when executing that module.
Omitted requirement assessment is UNKNOWN: assess content, SEO, accessibility, security,
provenance, measurement, localization and application needs before BUILD locks; an
evidence-backed NOT_REQUIRED keeps an optional module inactive. Inactivity is not readiness.
Unload means close the specialist context and retain only its bounded output/evidence
in the canonical domain record. Re-evaluate activation at every handoff; no sticky activation.
GSAP and Rive exclude one another. One creative advisor at a time, after direction selection.

<!-- ACTIVATION_TABLE -->
| MODULE | GATE | ACTIVATION_PREDICATE | MUTUAL_EXCLUSIONS | INPUT CONTRACT | OUTPUT CONTRACT | UNLOAD CONDITION | DOCUMENT |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DISCOVERY | BRIEF | discovery_required | - | Owner facts and questions | Confirmed brief and unknowns | Brief confirmed | DISCOVERY-PROTOCOL.md |
| DIRECT_REFERENCE_BUILDER | DIRECTION | business_brief_available & clean_room_ready & external_screenshots_ready | ALL_OTHER_MODULES | Staged manifest, screenshots, brief, intent, approved assets | Three hero/signature concepts | Concepts rendered | CLEAN-ROOM-CREATIVE-PROTOCOL.md |
| SEO | IA,CONTENT,BUILD | seo_required & direction_selected | - | Business and search intent | Keyword/route/content requirements; seo.complete | Requirements handed off | SEO-INTELLIGENCE-PROTOCOL.md |
| VISUAL_RESEARCH | BRIEF | external_research_required | - | Owner reference request | Actual external screenshots and provenance | References staged | VISUAL-RESEARCH-PROTOCOL.md |
| DESIGN_INTELLIGENCE | BUILD | direction_selected & design_advisor_requested | FRONTEND_DESIGN,AWWWARDS | Selected direction and bounded question | Non-authoritative advice | Question answered | DESIGN-INTELLIGENCE-PROTOCOL.md |
| FRONTEND_DESIGN | BUILD | direction_selected & distinctiveness_advisor_requested | DESIGN_INTELLIGENCE,AWWWARDS | Selected direction and bounded question | Non-authoritative advice | Question answered | DESIGN-CONSTITUTION.md |
| AWWWARDS | BUILD | direction_selected & showcase_comparison_requested | DESIGN_INTELLIGENCE,FRONTEND_DESIGN | Rendered selected direction and references | Reference comparison | Comparison recorded | AWWWARDS-SHOWCASE-INTELLIGENCE.md |
| VISUAL_PROTOTYPE | BUILD | direction_selected & homepage_expansion_required | - | Owner-selected concept | Complete homepage and owner review evidence | Homepage approved | VISUAL-PROTOTYPE-PROTOCOL.md |
| CONTENT_OPS | CONTENT | content_ops_required & direction_selected | - | Content structure and editorial needs | content_ops.complete and CMS necessity decision | Content contracts handed off | CONTENT-OPERATIONS-CMS-PROTOCOL.md |
| LOCALIZATION | CONTENT,BUILD | localization_required & direction_selected | - | Explicit locales and coverage | localization.complete and locale contracts | Locale contracts handed off | LOCALIZATION-INTERNATIONALIZATION-PROTOCOL.md |
| MEASUREMENT | CONTENT,BUILD | measurement_required & direction_selected | - | Business goals and data limits | measurement.complete and event manifest | Measurement contract handed off | CONVERSION-ANALYTICS-PROTOCOL.md |
| SECURITY_PRIVACY | CONTENT,BUILD | security_review_required & direction_selected | - | Applicable risks, data and components | security_privacy.complete and safeguards | Safeguards handed off | SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md |
| ACCESSIBILITY | CONTENT,BUILD | accessibility_review_required & direction_selected | - | Applicable components and user paths | accessibility.complete and requirements | Requirements handed off | ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md |
| PROVENANCE | CONTENT,BUILD | provenance_required & direction_selected | - | Claims, evidence and asset rights | provenance.complete and evidence ledger | Ledger handed off | EVIDENCE-PROVENANCE-PROTOCOL.md |
| APPLICATION | CONTENT,BUILD | application_behavior_required & direction_selected | - | Explicit stateful stories | application.complete and minimal modules | Application contract handed off | APPLICATION-COMMERCE-AUTH-PROTOCOL.md |
| DESIGN_SYSTEM | BUILD | direction_selected & homepage_approved | - | Approved homepage, requirements, owner locks | Derived tokens for owner Lock 4 | Tokens approved | DESIGN-SYSTEM-PROTOCOL.md |
| MOTION_DIRECTION | BUILD | direction_selected & motion_decision_required | - | Explicit motion needs and reduced-motion constraints | Deliberate motion decision for owner Lock 5 | Motion decision approved | MOTION-DIRECTION-PROTOCOL.md |
| ASSET_DIRECTOR | BUILD | direction_selected & custom_assets_required | - | Approved direction and asset gaps | Approved asset manifest | Assets handed off | ASSET-DIRECTOR-PROTOCOL.md |
| GSAP | BUILD | direction_selected & motion_approved & gsap_required | RIVE | Approved motion contract | Bounded implementation and runtime evidence | Motion implemented | GSAP-IMPLEMENTATION-PROTOCOL.md |
| RIVE | BUILD | direction_selected & motion_approved & rive_required | GSAP | Approved vector interaction requirement | Bounded state machine and fallback | Interaction implemented | RIVE-INTERACTIVE-MOTION-PROTOCOL.md |
| IMMERSIVE | BUILD | direction_selected & spatial_interaction_justified | - | Explicit real 3D/spatial need | Immersive contract and fallback | Spatial interaction implemented | IMMERSIVE-WEB-PROTOCOL.md |
| PAGE_EXPERIENCE | BUILD | direction_selected & route_transition_required | - | Navigation and route requirements | Transition contract and fallback | Navigation implemented | PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md |
| CINEMATIC | BUILD | direction_selected & cinematic_requirement_approved | - | Approved cinematic requirement | Bounded implementation contract | Contract handed off | CINEMATIC-INTEGRATION-PROTOCOL.md |
| SIGNATURE_CHOREOGRAPHY | BUILD | direction_selected & motion_approved & signature_motion_required | - | Approved signature device | Bounded choreography | Choreography implemented | SIGNATURE-SCROLL-SPATIAL-CHOREOGRAPHY-LIBRARY.md |
| LENIS | BUILD | direction_selected & motion_approved & smooth_scroll_required | - | Approved smooth-scroll requirement | Accessible scroll implementation | Scroll implemented | MOTION-DIRECTION-PROTOCOL.md |
| IMPLEMENTATION | BUILD | five_locks_confirmed & homepage_approved | - | Locked specification and required module outputs | Working local implementation | Build handed to VERIFY | IMPLEMENTATION-CONTRACT.md |
| IMPECCABLE | VERIFY | implementation_present | - | Actual implementation | Static deterministic findings | Findings recorded | IMPECCABLE-ENGINE-PROTOCOL.md |
| BROWSER_QA | VERIFY | implementation_present & verification_plan_ready | - | Manifest and actual implementation | browser_qa evidence and verification flags | Engine stopped and evidence persisted | BROWSER-REGRESSION-QA-PROTOCOL.md |
| GAUNTLET | VERIFY | rendered_evidence_ready & browser_qa_completed | - | Fresh renders and reference screenshots | Post-render findings; no owner approval | Findings handed off | WEBSITE-GAUNTLET-PROTOCOL.md |
| FRAMEWORK_VALIDATION | VERIFY | framework_change_present | - | Registries, source and synthetic tests | Framework report; frozen integrity | Reports persisted | FRAMEWORK-VALIDATION-PROTOCOL.md |
| PRODUCTION_PREFLIGHT | LAUNCH | verification_complete | - | Verified candidate and evidence | Release checklist | Checklist handed to launch authority | PRODUCTION-CHECKLIST.md |
| LAUNCH_AUTHORITY | LAUNCH | verification_complete & release_identity_known | - | Candidate, release identity, authorization record | Release/production facts in launch_ops | Launch handoff recorded | LAUNCH-OPERATIONS-PROTOCOL.md |
| CLIENT_HANDOFF | LAUNCH | handoff_required & release_identity_known | - | Existing operations and launch record | Handoff package for owner acceptance | Handoff accepted | CLIENT-CMS-HANDOFF-PROTOCOL.md |
<!-- /ACTIVATION_TABLE -->

## Verification and launch handoffs

Run the existing BrowserQAEngine.observe() against the actual implementation.
The engine is replaceable; its observation contract and FrozenIntegrityGuard are permanent.
Screenshots require persisted path, SHA-256, surface, viewport, engine and current render identity.
Repairs invalidate affected screenshot/critic evidence; recapture and re-review.
Keep frozen projects read-only. A detected mutation fails even if later restored.
Framework suites use synthetic fixtures; browser fixtures are not generated websites.
Required manual checks stay manual. Unavailable screen-reader or engine checks stay BLOCKED.
Run registered suites through python -m framework_validation --run-suites and the global
verify.js against this exact checkout. A failed required check prevents certification.
Do not weaken a test simply to fit shortened documentation: test the owning contract.

LAUNCH consumes verification; it does not rewrite requirements or approvals.
RELEASE_READY ≠ DEPLOYMENT_AUTHORIZED. launch-ops/validator.py owns the only launch
transition graph; framework validation consumes it. launch_ops.complete is planning
readiness, not deployed, production verified, or stabilized.
Use the existing browser harness for authorized production checks, not a second runner.
Known release identity and explicit authorization are required for consequential actions.
No automated push, merge, deploy, DNS, provider setup, or production mutation follows QA.
Long-term operations remain CLIENT-CMS-HANDOFF-PROTOCOL.md's lazy responsibility.

## Compatibility and handoff discipline

Do not retrofit historical profiles, missing historical state, or frozen pilots.
Keep five owner locks and existing domain state paths; no sixth lock or parallel flag.
Retain only the brief, current gate, lock evidence, applicable requirement decisions,
canonical output references and unresolved blockers between contexts.
Specialist documents own detailed behavior only during their explicit activation.
Their old automatic activation instructions are superseded by this table.
Existing templates and protocols remain available on demand; absence from resident
context is not deletion of required SEO, accessibility, security, evidence, content,
measurement, localization, application, verification, or launch behavior.

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
