# CLEAN-ROOM CREATIVE MODE PROTOCOL

> **Version:** 2.11.1
> **Status:** Mandatory Operating Standard (Website Director Subsystem)  
> **Governance:** Website Director Orchestration Rail ([SKILL.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/SKILL.md) Phase 4 & Phase 4.5)  
> **Mission:** Enforce structural clean-room boundaries around creative concept generation so historical generated output cannot contaminate fresh designs.

---

## 1. Core Operating Principles

1. **STRUCTURAL QUARANTINE**: Prompt instructions alone are insufficient to prevent historical contamination. Unapproved historical generated output is structurally inaccessible to the concept generation engine.
2. **POSITIVE VS NEGATIVE ROLE SEPARATION**: Historical website output from prior runs may ONLY be consumed AFTER candidate rendering as a negative baseline to evaluate visual divergence. It is strictly prohibited as a positive input for inspiration, layout, typography, or assets.
3. **ALLOWLISTED REUSABLE ASSETS**: Brand assets (logos, primary marks) are NOT bulk-imported from old projects. Each asset must be explicitly authorized on an itemized allowlist.
4. **PROVENANCE FOR POSITIVE REFERENCES**: All positive creative references must be external or owner-supplied external references with verifiable provenance.
5. **CHEAP CONCEPT GATE**: Early clean-room concept evaluation is initially restricted to one desktop hero viewport and one signature device before full homepage design/implementation begins.
6. **MORPHOLOGY DIVERGENCE OVER SEMANTICS**: Divergence is judged on visible geometry, spatial rhythm, and layout morphology—not component or class renaming.

---

## 2. Clean-Room Creative Input Pack (Phase 2)

When `CREATIVE_MODE = CLEAN_ROOM`, concept generation receives ONLY the clean-room input manifest:

- Current Business Understanding Pack (`project-brief.md`)
- Current Owner Intent Contract (`creative-intent-contract.md`)
- Current Approved Brand Constants
- Owner-Allowlisted Reusable Assets
- Current Conversion Requirements (`measurement-plan.md`)
- Current Factual Content
- External Design References / Owner-Supplied External References
- Explicit Owner Non-Negotiables

### Clean-Room Creative Manifest Structure

```yaml
CREATIVE_INPUT_MANIFEST:
  mode: CLEAN_ROOM
  business_understanding_ref: project-brief.md
  owner_intent_ref: creative-intent-contract.md
  brand_constants:
    primary_color: "var(--brand-primary)"
  reusable_assets:
    - asset_id: ASN_LOGO
      authorized: true
  external_references:
    - reference_id: REF_EXT_01
      url: https://example.com/reference
      classification: EXTERNAL_GOLD_STANDARD
  conversion_requirements_ref: measurement-plan.md
  content_truth_ref: content-plan.md
```

---

## 3. Historical Input Quarantine Rules (Phase 3)

In `CLEAN_ROOM` mode, any access attempt by the concept generator to historical paths is structurally blocked:

### Quarantined Paths:
- `projects/**`
- `review-workspaces/**`
- Prior generated HTML / CSS / JS
- Prior visual prototypes / screenshots
- Prior design systems
- Prior generated hero / section imagery
- Prior Website Director outputs for the same business entity

If an unauthorized path read is requested:
`CLEAN_ROOM_INPUT_VIOLATION = BLOCKED` with the exact offending path logged.

---

## 4. Reusable Asset Allowlist (Phase 4)

Historical project directories cannot be bulk-copied. Each asset must be individually allowlisted in `OWNER_REUSABLE_ASSETS`.

```yaml
OWNER_REUSABLE_ASSETS:
  - asset_id: ASN_LOGO
    source_path: assets/source/brand-logo.svg
    authorized: true
```

Bulk requests such as `copy all assets from projects/alpha-starts-now-*` fail with:
`HISTORICAL_ASSET_BULK_REUSE = BLOCKED`.

---

## 5. External Reference Provenance (Phase 5)

Every positive visual reference must carry one of the allowed classifications:

1. `EXTERNAL_GOLD_STANDARD`
2. `OWNER_SUPPLIED_EXTERNAL_REFERENCE`
3. `OWNER_APPROVED_BRAND_ASSET`

Forbidden as positive references:
- `PREVIOUS_WEBSITE_DIRECTOR_OUTPUT`
- `PREVIOUS_ASN_PROTOTYPE`
- `PREVIOUS_ASN_SCREENSHOT`
- `PREVIOUS_GENERATED_DIRECTION`
- `PREVIOUS_GENERATED_DESIGN_SYSTEM`

If no valid external reference package exists:
`EXTERNAL_REFERENCE_PACKAGE = MISSING` -> Concept generation HALTS. No silent substitution of old projects is permitted.

---

## 6. Historical Work as Negative Baseline Only (Phase 6)

Previous output is re-classified as `NEGATIVE_BASELINE_ONLY`.

### Mandatory Workflow Sequence:
```text
EXTERNAL REFERENCES / CLEAN MANIFEST
       │
       ▼
CLEAN-ROOM CONCEPT GENERATION
       │
       ▼
CANDIDATE RENDER (Hero + Signature Device)
       │
       ▼
NEGATIVE BASELINE COMPARISON (Morphology Divergence Check)
```

Attempting to read historical output BEFORE candidate render results in:
`NEGATIVE_BASELINE_PRE_RENDER_ACCESS = BLOCKED`.

---

## 7. Cheap Owner Concept Gate (Phase 7)

Clean-room runs must not construct a full homepage initially.

1. Generate exactly THREE concept directions.
2. Initial scope for each concept:
   - **A. One desktop hero viewport (1440px)**
   - **B. One signature visual device / representative second section**
3. Excluded from initial concept evaluation:
   - Full homepage sitemap / lower sections
   - Mobile responsive implementations
   - Complete footers & full nav menus
   - Production motion suites
   - Multi-device screenshot suites
4. Initial status: `OWNER_CONCEPT_SELECTION = PENDING`.
5. Full homepage build begins ONLY after explicit owner selection.

---

## 8. Blind Reference Critic (Phase 8)

The existing Website Gauntlet critic receives ONLY:
- Rendered Candidate Screenshot(s)
- External Gold-Standard Reference Screenshots
- Business Brief & Brand Brief

The critic does NOT receive:
- Source code / HTML / CSS / class names
- Direction names (e.g. "cinematic chapter")
- Builder self-ratings or commentary
- Historical ASN screenshots or scores

Evaluated dimensions:
- `VISUAL_DISTINCTIVENESS`
- `REFERENCE_CRAFT_LEVEL`
- `HERO_COMPOSITION`
- `SPATIAL_COMPOSITION`
- `MEDIA_LANGUAGE`
- `TYPOGRAPHIC_CHARACTER`
- `SIGNATURE_VISUAL_DEVICE`
- `VISUAL_RHYTHM`
- `PREMIUM_PERCEPTION`

---

## 9. Morphology Divergence Check (Phase 9)

Post-render comparison evaluates physical layout geometry against historical negative baselines across 10 vectors:

1. `HERO_SILHOUETTE`
2. `SECTION_GEOMETRY`
3. `TWO_COLUMN_REPETITION`
4. `CARD_CONTAINER_DENSITY`
5. `MEDIA_DOMINANCE`
6. `TYPOGRAPHIC_SILHOUETTE`
7. `WHITESPACE_DENSITY`
8. `PAGE_RHYTHM`
9. `SIGNATURE_DEVICE`
10. `CTA_MORPHOLOGY`

Semantic component renaming (e.g., renaming a `card` to a `cinematic chapter`) while keeping identical geometry triggers:
`MORPHOLOGY_DIVERGENCE = FAIL`.

### Stage applicability

At `HERO_PLUS_SIGNATURE_DEVICE_ONLY`, the denominator contains exactly seven
vectors: hero silhouette, normalized card/container density, normalized media
dominance, computed typography silhouette, internal whitespace occupancy, the
designated signature-device region, and CTA morphology. `SECTION_GEOMETRY`,
`TWO_COLUMN_REPETITION`, and `PAGE_RHYTHM` are `NOT_APPLICABLE`; they do not
count as matches or divergences. All ten vectors become applicable when a full
homepage is authorized and enough repeated page grammar exists.

### Evidence and verdict contract

- Every compared render uses the same browser-measurement schema: viewport and
  document dimensions; hero, surface, child, media, bordered-container,
  heading, signature-device, and CTA geometry; computed layout and typography;
  and normalized internal occupancy.
- A run may supply an explicit selector to identify a pre-existing signature
  device for measurement. The selector only locates the region and never
  becomes scoring evidence.
- Missing, null, incomplete, or unconfirmed scan evidence for an applicable
  vector is `INSUFFICIENT_EVIDENCE`. It blocks the overall verdict as
  `BLOCKED_INSUFFICIENT_EVIDENCE`; missing evidence is never a match.
- Vector verdicts are derived from raw normalized measurements and continuous
  distance before canonical reporting labels. Each applicable result retains
  candidate measurements, baseline measurements, distance/similarity, labels,
  and the vector verdict.
- Normalized values retain a stable unit scale at zero, and geometric coverage
  uses clipped rectangle union so rounding noise, nested containers,
  overlapping regions, and unpainted full-size wrappers cannot inflate a
  distance or occupied-area result.
- `PASS_DIVERGENCE` requires at least 60 percent of the applicable, sufficiently
  evidenced vectors to be divergent. At the cheap stage this is five of seven.
- Rechecking preserved renders uses
  `python -m framework_validation.morphology_recheck`. It may refresh evidence,
  the owner-review morphology rows, and a stripped blind-critic input package,
  but it never calls the concept generator or executes the Gauntlet. The
  recheck hashes all staged/generated creative artifacts except review and
  evidence outputs, preserves the source execution receipt unchanged, and
  writes a distinct hash-linked morphology recheck receipt.

---

## 10. Execution contract

The canonical runtime boundary is
`framework_validation.clean_room.prepare_clean_room_concept_run`. The
compatibility names `execute_clean_room_workflow` and
`run_clean_room_creative_mode` delegate to that same boundary. It is an
execution coordinator, not a report-only validator. It accepts a
`CleanRoomExecutionRequest` and four provider-neutral adapters plus an
optional stage-ready callback:

1. `generate_concepts(manifest)` returns the three cheap concepts after the
   staged package and pre-generation scope pass.
2. `render_candidate(concept_package)` returns a candidate screenshot and,
   for real proof, browser-derived DOM/CSS/layout evidence.
3. `load_negative_baseline(path)` is callable only after candidate rendering
   and receives no builder or positive-reference context.
4. `run_blind_critic(package)` receives the exact screenshot-and-brief package
   from §8, with no evaluator verdict or measurement payload. There is no
   programmatic Gauntlet entrypoint in the repository;
   the adapter hands off to the existing Website Gauntlet critic authority
   without creating a second critic.

The boundary creates one fresh ignored runtime pack at
`.clean-room-runs/<run_id>/` with `manifest/`, `business/`, `brand/`,
`approved-assets/`, `external-references/`, `candidate-output/`, and
`evidence/`. Only manifest-declared, allowlisted files are copied. The staged
inventory records `run_id`, `source_path`, `staged_path`, `classification`,
`sha256`, and `authorization_basis`; historical staged output must remain zero.

The coordinator executes these stages in order:

```text
INPUT_PREFLIGHT → REFERENCE_PROVENANCE → STAGED_CREATIVE_WORKSPACE
→ PRE_GENERATION_SCOPE → NEGATIVE_BASELINE_PRE_RENDER
→ CONCEPT_GENERATION → CHEAP_CONCEPT_GATE → CANDIDATE_RENDER
→ NEGATIVE_BASELINE_ACCESS → NEGATIVE_BASELINE_LOAD
→ RENDER_DERIVED_MORPHOLOGY → BLIND_CRITIC_PACKAGE → BLIND_CRITIC
→ OWNER_CONCEPT_SELECTION_GATE
```

The pre-generation request is exactly three concepts limited to
`DESKTOP_HERO` and `SIGNATURE_DEVICE`; full homepage, mobile full page,
footer, multi-route, full browser QA, and motion certification surfaces fail
before the builder callback. Browser-derived morphology uses measured layout
facts, not class names or caller-declared divergence labels. The receipt
records pre-render baseline blocking, post-render baseline role, package
sentinels, critic leaks, owner state, project-write count, and production side
effects. Without a valid existing
`visual_prototypes.owner_selection_confirmed` event, full homepage progression
remains `BLOCKED`; a valid owner selection changes it to `AUTHORIZED` without
creating a new lock.

The deterministic local proof is runnable with:

```text
python -m framework_validation.clean_room --synthetic
```

The proof uses synthetic adapters and the existing Playwright engine. It does
not call a provider, inspect a historical project before render, modify a
frozen project, generate ASN, publish, deploy, or write under `projects/`.
Framework isolation is `STAGED_WORKSPACE_ONLY`; the operating system sandbox
is `NONE`, so unrestricted agent path access remains a risk. The operational
mitigation is to launch the creative task from the staged workspace with an
explicit no-repository-source instruction. Provider-specific adapters remain
outside this framework boundary and must preserve the same ordering and
receipt contract.
