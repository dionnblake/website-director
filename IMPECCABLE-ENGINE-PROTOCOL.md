# IMPECCABLE QUALITY ENGINE: BOUNDED DETECTION AND CRAFT INTELLIGENCE

> Version: 1.1.0 (Website Director V2.15 maintenance refresh)
> Status: Mandatory design-quality review contract
> Framework version: 2.15.0 (unchanged)
> Engine decision: CURATED_IMPLEMENTATION_RETAINED
> Upstream repository: https://github.com/pbakaus/impeccable
> License: Apache License 2.0

This protocol is the contract for the existing design_qa_impeccable capability.
It does not add a lifecycle phase, readiness gate, state machine, orchestrator,
or owner lock. Website Director retains exactly five owner locks:
design_direction_locked, information_architecture_locked,
content_structure_locked, design_system_locked, and motion_direction_locked.

The audited upstream v4.3.1 runtime is not installed or executed here. The
Website Director implementation is a small, provider-neutral, standard-library
scanner at framework_validation/impeccable.py. It reads explicit source text,
returns normalized findings, and never writes, repairs, starts a browser,
calls a provider, or contacts a network endpoint.

## 1. Audited upstream identity and adoption decision

### 1.1 Verification record

| Field | Verified evidence |
| :--- | :--- |
| Previous upstream tag | skill-v4.1.2 |
| Previous upstream commit | 63b04e2530f5c7b41ea83c133daab24f34912456 |
| Target upstream tag | skill-v4.3.1 |
| Target upstream commit | cd12f8660e2dde57b9615c8a6b8ea674101f9cfc |
| Target release | Published 2026-09-09T02:24:39Z, non-prerelease |
| Target registry | 61 built-in IDs in crates/foundation/src/registry.rs |
| Previous registry | 59 IDs in cli/engine/registry/antipatterns.mjs |
| Registry delta | organic-clip-path and buried-raster added |
| Release artifact | universal.zip, 15,625,571 bytes |
| Release SHA-256 | 1deea4cdfb1608df6d9e08ef359629e7cc866a22ab7c2195a835627b887f190b |
| Signature metadata | Sidecar matched the artifact name, version, size, and SHA-256 |
| License | LICENSE and Cargo workspace identify Apache-2.0 |
| Upstream target verified | YES for tag, peeled commit, release metadata, license, and digest |

The sidecar metadata was checked against the downloaded release artifact. This
repository does not import the upstream release key or execute the downloaded
binary as part of the Website Director proof, so binary execution compatibility
is not claimed.

### 1.2 Option A versus Option B

Option A, adopting the official engine, is rejected for this bounded refresh.
The source and release identity are verifiable, but all integration conditions
were not proven inside the existing Website Director boundary. In particular,
there is no existing Website Director adapter, no approved binary cache or
bootstrap contract, no Windows and Ubuntu end-to-end invocation proof for this
repository, and the upstream package carries a separate runtime, install/update
surface, provider hooks, editing/live capabilities, and PRODUCT.md/DESIGN.md
context workflow. Those surfaces would duplicate or expand existing authorities.

Option B is retained: the Website Director-owned scanner ports the existing
18 contractual entries and adopts only the selected v4.3.1 static rules whose
evidence can be explained and tested without a browser or provider.

ENGINE_DECISION = CURATED_IMPLEMENTATION_RETAINED
ENGINE_ADOPTION = REJECTED
OFFICIAL_ENGINE_EXECUTED = NO
EXTERNAL_NETWORK_REQUIRED = NO
LEGACY_EXECUTABLE_SCANNER_PRESENT = NO

Option A gate evidence:

| # | Requirement | Result | Evidence or failure reason |
| :---: | :--- | :--- | :--- |
| 1 | Exact version can be pinned | YES | `skill-v4.3.1` resolves to the audited peeled commit |
| 2 | Release identity can be verified | YES | Release metadata, artifact size, SHA-256, and sidecar agree |
| 3 | Deterministic scan behavior is reproducible | NOT_PROVEN | The official binary was not executed in this bounded refresh |
| 4 | Windows operation works | NOT_PROVEN | No official binary invocation was authorized or run |
| 5 | Linux operation works | NOT_PROVEN | No official binary invocation was authorized or run |
| 6 | No persistent daemon is required | SOURCE_SUPPORTED | The CLI has per-run commands; no daemon was enabled |
| 7 | Hooks are optional | SOURCE_SUPPORTED | Hook integration is a separate upstream surface and was not enabled |
| 8 | Edit hooks are not required for audit | SOURCE_SUPPORTED | Read-only detection is separate from edit-hook installation |
| 9 | Read-only invocation is available | NOT_PROVEN | The upstream package was not run against fixtures |
| 10 | Failures are detectable | NOT_PROVEN | No Website Director adapter mapped upstream exit/failure results |
| 11 | Unavailable engine cannot silently pass | NOT_PROVEN | No adapter-level missing-engine behavior exists to verify |
| 12 | Output normalizes reliably | NO | Upstream output was not proven to satisfy the nine-field Website Director contract |
| 13 | No duplicate PRODUCT.md/DESIGN.md ownership | NO | Upstream context and provider workflows include those surfaces |
| 14 | Runtime responsibilities remain excluded | NOT_PROVEN | The 61-rule runtime/static split was not proven through an adapter |
| 15 | Network and cache behavior is explicit and acceptable | NO | Bootstrap/cache/download behavior would require a new controlled contract |
| 16 | Protected-project integrity is guaranteed | NOT_PROVEN | No official adapter was run behind the existing frozen-integrity guard |
| 17 | Licensing and provenance are satisfied | YES | Upstream `LICENSE` and workspace metadata identify Apache-2.0 |

Because requirements 3-5, 9-12, 14-16 were not proven and 12, 13, and 15
failed the existing boundary, Option A is not eligible. This is why
`ENGINE_ADOPTION = REJECTED`; the verified upstream source is reference
material, not an installed Website Director provider.

## 2. Finding taxonomy and normalized record

Website Director findings preserve the distinction between a machine-checkable
observation, a structural heuristic, a qualitative Gauntlet judgment, a visual
comparison, and a live browser assertion.

| Method | Meaning | Primary owner |
| :--- | :--- | :--- |
| DETERMINISTIC | Reproducible source or mathematical check | Impeccable scanner |
| HEURISTIC | Explainable structural pattern that needs context | Impeccable scanner |
| LLM_CRITIQUE | Qualitative brand, hierarchy, or conversion judgment | Website Gauntlet |
| VISUAL_COMPARISON | Fresh comparison against an approved Reference Bar | Visual review and Gauntlet |
| BROWSER_EXECUTED | Assertion against a real rendered page | Browser QA harness |

Every scanner finding serializes exactly these fields:

FINDING_ID: unique deterministic identifier
SOURCE: IMPECCABLE_DETECTOR
METHOD: DETERMINISTIC or HEURISTIC
RULE: audited upstream or Website Director rule ID
LOCATION: normalized path and one-based source line
SEVERITY: CRITICAL, MAJOR, or MINOR
EVIDENCE: exact observed source or computed measurement
REMEDIATION: bounded corrective guidance
LOCK_IMPACT: NONE or LOCKED_CHANGE_REQUIRED

The scanner never calls a repair callback. If the caller marks a rule as
locked, the finding reports LOCKED_CHANGE_REQUIRED. If the caller provides both
design_direction_locked = true and an explicit authorized_heuristics list, the
heuristic is retained as AUTHORIZED_BY_LOCK and does not block that scan result.
Authorization is input evidence, not a mutation of the lock registry.

## 3. Existing Website Director contract: 18 entries preserved

The original Website Director contract remains intact. The side-tab and
border-accent-on-rounded IDs are two upstream IDs represented by one existing
contract entry. The 18 contractual entries therefore cover 18 upstream IDs
plus one Website Director-owned `touch-target-undersized` extension, for 19
executable IDs in the retained contract.

### 3.1 Universal technical checks

1. low-contrast: compute WCAG contrast from explicit source colors.
2. gray-on-color: flag neutral gray text on a non-neutral surface.
3. layout-transition: flag transitions of layout-triggering properties.
4. bounce-easing: flag overshooting cubic-bezier curves.
5. dark-glow: flag saturated colored shadows on explicit dark surfaces.
6. touch-target-undersized: flag declared interactive dimensions below 44px.

### 3.2 Context-dependent heuristics

7. ai-color-palette: flag the recognizable uncurated indigo, violet, and cyan
   gradient pairing.
8. hero-eyebrow-chip: flag a small eyebrow or chip immediately before a hero
   heading.
9. icon-tile-stack: flag three or more repeated feature icon containers.
10. radial-halo: flag an ungrounded transparent radial gradient wash.
11. side-tab and border-accent-on-rounded: flag a colored side accent on a
    rounded card without status semantics.
12. pulsing-dot: flag decorative pulse or ping animation without live data.
13. marquee: flag infinite marquee motion without pause or editorial purpose.
14. shape-assembled-illustration: flag repeated absolute primitive decorators.
15. monotonous-spacing: flag four or more section rules sharing one spacing.
16. gradient-text: flag clipped transparent glyphs used for a gradient.
17. kicker-above-heading: flag repeated mechanical labels above headings.
18. italic-serif-display: flag a single italic display word without context.

## 4. Selected v4.3.1 additions

The following nine IDs are newly executable in the curated scanner:

| Rule | Method | Bounded evidence |
| :--- | :--- | :--- |
| flat-type-hierarchy | HEURISTIC | Three or more explicit heading/body roles have less than a 1.25x range |
| organic-clip-path | HEURISTIC | A curved path or a 10-plus-vertex off-grid polygon approximates a produced silhouette |
| buried-raster | HEURISTIC | A URL-backed raster is covered by a pre-raster gradient whose sampled stops are all at least 0.9 alpha |
| extreme-negative-tracking | DETERMINISTIC | Heading tracking is at or below -0.08em |
| broken-image | DETERMINISTIC | Image source is missing, empty, or a placeholder |
| justified-text | DETERMINISTIC | text-align: justify has no declared safe hyphenation contract |
| tiny-text | DETERMINISTIC | Body or content text is below 12px, excluding legal smallprint |
| undersized-ui-text | DETERMINISTIC | Functional UI text is below 11px |
| repeating-stripes-gradient | HEURISTIC | Repeating gradient is used without material-purpose evidence |

The additions are intentionally source-bounded. They do not claim to replace
the upstream HTML cascade, browser snapshot, visual, text, or design-system
engines.

## 5. Complete v4.3.1 rule classification matrix

The matrix accounts for every one of the 61 current upstream built-in IDs.
Each row has exactly one disposition:

| Code | Disposition |
| :--- | :--- |
| A | ADOPT_EXISTING_EQUIVALENT |
| B | ADOPT_NEW_STATIC |
| C | ADOPT_NEW_HEURISTIC |
| D | EXISTING_OWNER_BROWSER_QA |
| E | EXISTING_OWNER_ACCESSIBILITY |
| F | EXISTING_OWNER_DESIGN_CONSTITUTION |
| G | EXISTING_OWNER_GAUNTLET |
| H | DUPLICATE |
| I | CONFLICTING |
| J | REJECT |

The method column is an audit classification derived from the upstream source
layout. It is not asserted as a new Website Director finding method.
Website Director keeps one owner for each rule. A consumer may reuse evidence,
but it may not reimplement another owner's detector.

| Upstream ID | Upstream method class | Disposition | Single Website Director owner | Reason |
| :--- | :--- | :---: | :--- | :--- |
| side-tab | STATIC_HTML_CSS | A | design_qa_impeccable | Existing paired contract |
| border-accent-on-rounded | STATIC_HTML_CSS | A | design_qa_impeccable | Existing paired contract |
| overused-font | STATIC_PAGE_TYPE | F | design_system | Requires approved font identity |
| flat-type-hierarchy | STATIC_PAGE_TYPE | C | design_qa_impeccable | Bounded role-size heuristic |
| gradient-text | STATIC_HTML_CSS | A | design_qa_impeccable | Existing heuristic |
| ai-color-palette | STATIC_HTML_CSS | A | design_qa_impeccable | Existing heuristic |
| cream-palette | STATIC_HTML_CSS | F | design_constitution | Palette is context-dependent |
| nested-cards | STATIC_HTML_DOM | G | website_gauntlet | Composition needs visual context |
| monotonous-spacing | STATIC_PAGE_LAYOUT | A | design_qa_impeccable | Existing page heuristic |
| bounce-easing | STATIC_HTML_CSS | A | design_qa_impeccable | Existing technical check |
| pulsing-dot | STATIC_HTML_CSS | A | design_qa_impeccable | Existing live-status heuristic |
| blinking-cursor | STATIC_HTML_CSS | G | website_gauntlet | Legitimate product/editorial use exists |
| shape-assembled-illustration | STATIC_HTML_SVG | A | design_qa_impeccable | Existing structural heuristic |
| organic-clip-path | STATIC_HTML_CSS | C | design_qa_impeccable | New bounded complex-shape heuristic |
| buried-raster | STATIC_HTML_CSS | C | design_qa_impeccable | New bounded raster-visibility heuristic |
| dark-glow | STATIC_HTML_CSS | A | design_qa_impeccable | Existing technical/visual check |
| radial-halo | STATIC_HTML_CSS | A | design_qa_impeccable | Existing visual heuristic |
| radial-spotlight-glow | STATIC_HTML_CSS | G | website_gauntlet | Lighting intent needs visual judgment |
| marquee | STATIC_HTML_CSS | A | design_qa_impeccable | Existing pause-purpose heuristic |
| icon-tile-stack | STATIC_HTML_DOM | A | design_qa_impeccable | Existing structural heuristic |
| italic-serif-display | STATIC_HTML_DOM | A | design_qa_impeccable | Existing contextual typography heuristic |
| hero-eyebrow-chip | STATIC_HTML_DOM | A | design_qa_impeccable | Existing structural heuristic |
| kicker-above-heading | STATIC_HTML_DOM | A | design_qa_impeccable | Existing repeated-label heuristic |
| numbered-section-labels | STATIC_HTML_DOM | G | website_gauntlet | Editorial sequencing needs context |
| em-dash-overuse | STATIC_TEXT | J | no automatic owner | Voice and language have high false positives |
| marketing-buzzword | STATIC_TEXT | J | no automatic owner | Copy judgment belongs to content review |
| aphoristic-cadence | STATIC_TEXT | J | no automatic owner | Cadence is not a safe static defect |
| oversized-h1 | STATIC_HTML_DOM | G | website_gauntlet | Viewport and copy length need render context |
| extreme-negative-tracking | STATIC_HTML_CSS | B | design_qa_impeccable | New deterministic tracking floor |
| broken-image | STATIC_HTML_DOM | B | design_qa_impeccable | Source-level precheck only; Browser QA owns rendered/runtime asset integrity |
| script-error | BROWSER_RUNTIME | D | browser_qa | Runtime console behavior |
| content-hidden-at-rest | BROWSER_RUNTIME | D | browser_qa | Requires post-reveal rendered state |
| edge-flush-cards | BROWSER_RUNTIME | D | browser_qa | Requires live viewport geometry |
| text-occlusion | BROWSER_RUNTIME | D | browser_qa | Requires painted-layer observation |
| first-viewport-column-overflow | BROWSER_RUNTIME | D | browser_qa | Requires live viewport geometry |
| gray-on-color | STATIC_HTML_CSS | A | design_qa_impeccable | Existing static color check |
| low-contrast | STATIC_HTML_CSS | A | design_qa_impeccable | Existing contrast math |
| layout-transition | STATIC_HTML_CSS | A | design_qa_impeccable | Existing motion source check |
| line-length | STATIC_PAGE_LAYOUT | G | website_gauntlet | Copy measure needs rendered context |
| cramped-padding | STATIC_HTML_DOM | G | website_gauntlet | Optical spacing needs visual context |
| body-text-viewport-edge | BROWSER_RUNTIME | D | browser_qa | Requires actual viewport edge geometry |
| tight-leading | STATIC_HTML_CSS | G | website_gauntlet | Type scale and copy role are contextual |
| skipped-heading | STATIC_HTML_DOM | E | accessibility | Canonical accessibility heading-order requirement; Browser QA executes the canonical heading-order assertion |
| heading-rhythm | STATIC_PAGE_LAYOUT | G | website_gauntlet | Requires rendered vertical rhythm |
| justified-text | STATIC_HTML_CSS | B | design_qa_impeccable | New deterministic source check |
| tiny-text | STATIC_HTML_CSS | B | design_qa_impeccable | New deterministic readable-text floor |
| undersized-ui-text | STATIC_HTML_CSS | B | design_qa_impeccable | New deterministic functional-text floor |
| all-caps-body | STATIC_TEXT | G | website_gauntlet | Brand and editorial voice are contextual |
| wide-tracking | STATIC_HTML_CSS | F | design_system | Approved typography may require it |
| text-overflow | BROWSER_RUNTIME | D | browser_qa | Requires rendered overflow observation |
| repeated-container-text | STATIC_HTML_DOM | G | website_gauntlet | Repetition needs content and composition context |
| clipped-overflow-container | BROWSER_RUNTIME | D | browser_qa | Requires live scroll and clipping behavior |
| design-system-font | DESIGN_SYSTEM_STATIC | F | design_system | Canonical token mapping owns it |
| design-system-color | DESIGN_SYSTEM_STATIC | F | design_system | Canonical token mapping owns it |
| design-system-radius | DESIGN_SYSTEM_STATIC | F | design_system | Canonical token mapping owns it |
| design-system-font-size | DESIGN_SYSTEM_STATIC | F | design_system | Canonical token mapping owns it |
| gpt-thin-border-wide-shadow | STATIC_HTML_CSS | G | website_gauntlet | Visual material judgment is required |
| repeating-stripes-gradient | STATIC_HTML_CSS | C | design_qa_impeccable | New bounded material heuristic |
| codex-grid-background | STATIC_HTML_CSS | G | website_gauntlet | Intentional grid texture needs visual context |
| theater-slop-phrase | STATIC_TEXT | J | no automatic owner | Phrase judgment has high false positives |
| image-hover-transform | STATIC_HTML_CSS | G | website_gauntlet | Interaction intent and reduced motion need context |

This catalog uses E once, for `skipped-heading`, while H and I remain zero:
the canonical accessibility heading requirement stays with Accessibility and
its Browser QA execution, no row is a duplicate, and no row conflicts with a
Website Director authority. The adopted upstream set is A+B+C: 18 existing
equivalents, 5 new static rules, and 4 new heuristics. The remaining 34 IDs
are D/E/F/G/J delegated or rejected.

### 5.1 Per-rule method, severity, override, and evidence

The disposition matrix above records ownership and rationale. This companion
table records the remaining per-rule metadata. `LOCKED_DIRECTION_ONLY` means
that a retained heuristic can be non-blocking only when the caller supplies an
explicit authorized heuristic and a locked design direction. `OWNER_DEFINED`
means that the delegated owner supplies the applicable context; it is not a
scanner override.

| Upstream ID | Evidence mode (not a new scanner METHOD) | Severity (adopted / owner) | Context override | Evidence required |
| :--- | :--- | :--- | :--- | :--- |
| side-tab | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_CSS |
| border-accent-on-rounded | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_CSS |
| overused-font | NOT_EMITTED | OWNER_SET | OWNER_DEFINED | APPROVED_DESIGN_SYSTEM |
| flat-type-hierarchy | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_CSS |
| gradient-text | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_CSS |
| ai-color-palette | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_CSS |
| cream-palette | NOT_EMITTED | OWNER_SET | OWNER_DEFINED | APPROVED_DESIGN_SYSTEM |
| nested-cards | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |
| monotonous-spacing | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_CSS |
| bounce-easing | DETERMINISTIC | MAJOR | NO | SOURCE_CSS |
| pulsing-dot | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_CSS |
| blinking-cursor | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |
| shape-assembled-illustration | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_HTML_SVG |
| organic-clip-path | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_CSS |
| buried-raster | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_CSS |
| dark-glow | DETERMINISTIC | MAJOR | NO | SOURCE_CSS |
| radial-halo | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_CSS |
| radial-spotlight-glow | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |
| marquee | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_CSS |
| icon-tile-stack | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_HTML |
| italic-serif-display | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_HTML |
| hero-eyebrow-chip | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_HTML |
| kicker-above-heading | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_HTML |
| numbered-section-labels | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |
| em-dash-overuse | NOT_EMITTED | N/A | N/A | HUMAN_COPY_REVIEW |
| marketing-buzzword | NOT_EMITTED | N/A | N/A | HUMAN_COPY_REVIEW |
| aphoristic-cadence | NOT_EMITTED | N/A | N/A | HUMAN_COPY_REVIEW |
| oversized-h1 | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |
| extreme-negative-tracking | DETERMINISTIC | MAJOR | NO | SOURCE_CSS |
| broken-image | DETERMINISTIC | MAJOR | NO | SOURCE_HTML_PRECHECK_ONLY |
| script-error | BROWSER_EXECUTED | CRITICAL | OWNER_DEFINED | BROWSER_RUNTIME |
| content-hidden-at-rest | BROWSER_EXECUTED | CRITICAL | OWNER_DEFINED | BROWSER_RUNTIME |
| edge-flush-cards | BROWSER_EXECUTED | MAJOR | OWNER_DEFINED | BROWSER_RUNTIME |
| text-occlusion | BROWSER_EXECUTED | MAJOR | OWNER_DEFINED | BROWSER_RUNTIME |
| first-viewport-column-overflow | BROWSER_EXECUTED | MAJOR | OWNER_DEFINED | BROWSER_RUNTIME |
| gray-on-color | DETERMINISTIC | MAJOR | NO | SOURCE_CSS |
| low-contrast | DETERMINISTIC | MAJOR | NO | SOURCE_CSS |
| layout-transition | DETERMINISTIC | MAJOR | NO | SOURCE_CSS |
| line-length | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |
| cramped-padding | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |
| body-text-viewport-edge | BROWSER_EXECUTED | MAJOR | OWNER_DEFINED | BROWSER_RUNTIME |
| tight-leading | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |
| skipped-heading | BROWSER_EXECUTED | MAJOR | OWNER_DEFINED | ACCESSIBILITY_REVIEW / BROWSER_RUNTIME |
| heading-rhythm | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |
| justified-text | DETERMINISTIC | MINOR | NO | SOURCE_CSS |
| tiny-text | DETERMINISTIC | MINOR | NO | SOURCE_CSS |
| undersized-ui-text | DETERMINISTIC | MINOR | NO | SOURCE_CSS |
| all-caps-body | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |
| wide-tracking | NOT_EMITTED | OWNER_SET | OWNER_DEFINED | APPROVED_DESIGN_SYSTEM |
| text-overflow | BROWSER_EXECUTED | MAJOR | OWNER_DEFINED | BROWSER_RUNTIME |
| repeated-container-text | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |
| clipped-overflow-container | BROWSER_EXECUTED | MAJOR | OWNER_DEFINED | BROWSER_RUNTIME |
| design-system-font | NOT_EMITTED | OWNER_SET | OWNER_DEFINED | APPROVED_DESIGN_SYSTEM |
| design-system-color | NOT_EMITTED | OWNER_SET | OWNER_DEFINED | APPROVED_DESIGN_SYSTEM |
| design-system-radius | NOT_EMITTED | OWNER_SET | OWNER_DEFINED | APPROVED_DESIGN_SYSTEM |
| design-system-font-size | NOT_EMITTED | OWNER_SET | OWNER_DEFINED | APPROVED_DESIGN_SYSTEM |
| gpt-thin-border-wide-shadow | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |
| repeating-stripes-gradient | HEURISTIC | MINOR | LOCKED_DIRECTION_ONLY | SOURCE_CSS |
| codex-grid-background | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |
| theater-slop-phrase | NOT_EMITTED | N/A | N/A | HUMAN_COPY_REVIEW |
| image-hover-transform | LLM_CRITIQUE | OWNER_SET | OWNER_DEFINED | RENDERED_REVIEW |

No row is silently both adopted and delegated. Browser QA may consume static
findings from rows owned by the Impeccable scanner, but it does not reimplement
those checks. Accessibility may consume the scanner's static contrast result,
but its computed rendered assertions remain in the existing Browser QA
accessibility group governed by ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md.
`skipped-heading` is not emitted by Impeccable: Accessibility owns the logical
heading requirement and Browser QA executes the canonical heading-order
assertion.

The `broken-image` boundary is deliberately narrower. Impeccable owns only
the source-level precheck for an obvious missing, empty, or placeholder image
source in source text. Browser QA owns rendered/runtime asset loading and
dimensions, network results, placeholder rendering, and the production asset-
integrity verdict. The static result cannot substitute for Browser QA
asset-integrity PASS.

## 6. Executable boundary and usage

The executable surface is framework_validation/impeccable.py:

* scan_sources(source_map, context) scans an explicit mapping of source paths
  to text.
* scan_path(root, context) reads only supported text files below a caller-owned
  path and delegates to scan_sources.
* An empty source map, empty directory, unsupported-only directory, or
  unsupported-only explicit source map fails closed with
  `ValueError("no supported source files to scan")`; none can produce PASS.
* Ignore-directory checks are relative to the selected root, so a caller may
  explicitly scan a root named `build`, `dist`, or another ignored directory
  while nested ignored directories remain excluded.
* Finding.as_dict() emits the nine normalized fields above.
* ScanResult.passed excludes heuristic findings explicitly authorized by a
  locked design direction.
* assess_official_engine_artifact(path, expected_sha256, expected_version)
  checks a future owner-approved artifact identity and returns BLOCKED for
  missing or corrupt artifacts. It never executes the artifact or downloads it.

The scanner does not:

* call npx, Cargo, Bun, a provider, an MCP server, a browser, or a daemon;
* install upstream skills or hooks;
* create PRODUCT.md or DESIGN.md;
* write a report, lock, project, generated website, or external account;
* infer semantic design approval from lexical overlap;
* replace Browser QA, Accessibility, Design Constitution, or Gauntlet.

The existing design_qa_impeccable state and Phase 11 remain the authority.
No new state, phase, gate, registry, or orchestrator was introduced.

## 7. Gauntlet enrichment, hardening, and creative playbooks

The Website Gauntlet remains the owner of fresh qualitative critique. It may
consume the scanner's evidence for AI-slop, craft, typography, spacing,
accessibility, and motion discussions, but it does not create a second critic.

Impeccable hardening guidance remains applicable as review guidance:

1. Long content must wrap or clamp with a usable fallback.
2. Translation expansion must not collide with controls or headings.
3. Interactive controls need default, hover, active, focus-visible, disabled,
   loading, and error states where those states apply.
4. Hover treatment must not be the only path for coarse pointers.

The bolder, delight, and overdrive playbooks remain opt-in. Bolder requires
locked design-direction justification, delight requires the existing motion
justifications, and overdrive requires the existing Motion Level 3 and
cinematic evidence contract. This protocol does not authorize their use.

## 8. Canonical context mapping and tooling policy

Upstream context concepts map to existing Website Director artifacts:

| Upstream concept | Website Director artifact | Authority |
| :--- | :--- | :--- |
| PRODUCT.md | project-brief.md, positioning.md, site-profile.json | Discovery |
| DESIGN.md | design-direction.md, design-system.md, DESIGN-CONSTITUTION.md | Design and tokens |
| Surface briefs | information-architecture.md, content-plan.md | Page and content strategy |
| Hardening guidance | PRODUCTION-CHECKLIST.md, QA-RUBRIC.md | Pre-flight and QA |

No duplicate context files are added. The audited upstream package's provider
hook, install, update, live-browser, and edit surfaces are not part of this
integration. Persistent browser daemons remain REJECTED_FOR_NOW. The existing
Browser QA engine remains ephemeral and owns real-browser evidence.

## 9. Historical validation truth and release boundary

The previous validation example described an executable Node script that is not
present in the historical Website Director checkout. That claim is corrected
in examples/IMPECCABLE-INTEGRATION-VALIDATION.md:

LEGACY_EXECUTABLE_SCANNER_PRESENT = NO
LEGACY_VALIDATION_DOCUMENT_ACCURATE = YES after this refresh
LEGACY_VALIDATION_DOCUMENT_ACCURATE_BEFORE_REFRESH = PARTIAL

The corrected example records the actual Python module and registered test
command. It does not retroactively certify old scans or frozen projects.

This refresh is a local candidate only. It does not publish, deploy, merge,
modify the main branch, modify the protected projects corpus, create a pull
request, or authorize production use. Promotion remains an owner decision
after the evidence and independent review are available.
