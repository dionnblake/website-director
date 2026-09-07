# CLEAN-ROOM CREATIVE MODE PROTOCOL

> **Version:** 2.11.0  
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
