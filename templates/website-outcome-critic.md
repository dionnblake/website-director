# Website Director Quality Critique Receipt V0.1

This template is an import contract, not a request to run a model. Save one
review as a local JSON artifact, bind its SHA-256 in the case manifest, and
replay it only against the exact specimen and rendered evidence it names.

## Quality boundary

`DESIGN_PROPOSAL_COMPLETENESS` evaluates declared brief, direction, and
proposal structure. It does not prove `RENDERED_DESIGN_DISTINCTIVENESS` or
premium visual quality. A rendered-quality finding requires hash-bound,
actual `REAL_BROWSER` image evidence with a named surface and viewport. Source
text, CSS declarations, keywords, a signature declaration, simulation output,
or an unresolved asset claim cannot satisfy that requirement.

The core dimensions are:

`BRIEF_AND_BRAND_FIDELITY`, `VISUAL_HIERARCHY`, `TYPOGRAPHY`,
`COMPOSITION_AND_ART_DIRECTION`, `IMAGERY_AND_VISUAL_WORLD`,
`PREMIUM_DISTINCTIVENESS`, `MEMORABILITY`, `POLISH_AND_CRAFT`,
`RESPONSIVE_QUALITY`, `CONVERSION_CLARITY`, and conditional
`MOTION_QUALITY`.

Every applicable required dimension must score at least `8/10`. Scores are
not averaged to hide a weak dimension. A hard-gate failure makes the quality
result `FAIL`; missing evidence or provenance makes it `BLOCKED`. Do not
invent a score for a blocked finding.

## Required JSON shape

```json
{
  "critique_version": "0.1.0",
  "rubric_version": "WD-QUALITY-V0.1",
  "case_id": "...",
  "case_version": "0.1.0",
  "specimen_id": "...",
  "specimen_hash": "sha256-or-other-evidence-identity",
  "evidence_files": ["desktop-full-page", "mobile-full-page", "hero-asset"],
  "criterion_breakdown": [
    "brand-fidelity",
    "visual-hierarchy",
    "typography"
  ],
  "criterion_findings": [
    {
      "criterion_id": "brand-fidelity",
      "status": "PASS",
      "score": 8,
      "observation": "What is visibly established in the cited render.",
      "evidence_refs": ["desktop-full-page", "mobile-full-page"],
      "limitation": "Any material uncertainty."
    }
  ],
  "hard_gate_findings": [
    {
      "gate_id": "generic-template",
      "status": "PASS",
      "observation": "Evidence-bound reason for the gate result.",
      "evidence_refs": ["desktop-full-page"]
    }
  ],
  "critic_context": {
    "context_id": "separate-critic-context-01",
    "builder_context_id": "builder-context-01",
    "input_scope": "brief, rubric, and hash-bound rendered evidence only"
  },
  "reviewer": {
    "role": "independent_quality_critic",
    "independence": "INDEPENDENT"
  },
  "limitations": ["No owner acceptance was performed."],
  "timestamp": "2026-09-05T00:00:00Z"
}
```

`criterion_findings` may also be named `findings`; the canonical name is
preferred. `evidence_refs` must resolve to manifest-bound artifacts or
evidence. Render findings should cite the actual screenshot surfaces. The
imagery dimension additionally requires a hash-bound local image asset unless
the case records an explicit owner-approved exception.

The reviewer and critic context are provenance fields, not proof by
themselves. A builder-self-issued or provenance-unknown critique remains
blocked when independent review is required. A valid imported critique is
calibration input, not owner acceptance, production certification, or a license
or rights decision. Synthetic fixtures must be labeled and cannot support a
real website-quality claim.
