# Offline Website Outcome Replay (V0.1)

The replay pilot is an explicit adapter to the existing Browser QA evidence
contract. It evaluates a case manifest against already-recorded local files and
receipts. It does not rerun Browser QA, open a site, fetch a reference, call an
evaluator, generate a site, replace a baseline, or authorize an owner or
production decision.

Run it from the repository root with a new empty output directory outside the
repository:

```powershell
python browser-qa/runner.py --mode artifact-replay `
  --case-manifest templates/website-outcome-case-manifest.json `
  --evidence "$env:TEMP\website-director-outcome-replay-01"
```

The command writes `outcome-replay.json` and `outcome-replay.md` in that output
directory. Exit code `0` means every applicable mandatory result passed
provisionally. Exit code `1` means at least one mandatory result failed. Exit
code `2` means one or more cases remain blocked or incomplete. Exit code `3`
means the manifest or its integrity/path contract is invalid. All non-zero
results are non-success, even when another case passed.

Requirement statuses are `PASS`, `FAIL`, `BLOCKED`, and `NOT_APPLICABLE`.
Missing evidence never becomes a pass. Imported Browser QA, motion, screenshot,
and critique files are labeled as historical/imported evidence. A critique's
independence is declared provenance, not ground truth; builder-self-issued or
unknown provenance cannot become owner approval. Synthetic cases are reported
with `SYNTHETIC_FIXTURE_ONLY` and are excluded from real website-quality
claims.

## V0.1 rendered-quality repair

The replay has two separate qualitative surfaces:

- `DESIGN_PROPOSAL_COMPLETENESS` checks declared brief, direction, and
  proposal artifacts. Keywords such as `subject_world`, `hero_thesis`, or
  `signature_element` can support that proposal check only.
- `RENDERED_DESIGN_DISTINCTIVENESS` is the public-facing name for the premium
  rendered-quality path. It requires the exact `WD-QUALITY-V0.1` rubric, a
  specimen/evidence identity, a complete criterion breakdown and findings,
  critic context, reviewer provenance, limitations, timestamp, and
  hash-bound rendered evidence.

Rendered evidence must be an actual image captured by `REAL_BROWSER`, with a
positive viewport and named surface. Browser QA receipts must independently
prove the real-browser screenshot set. Source HTML/CSS, simulation, prose,
declarations, or stale screenshots cannot satisfy a rendered criterion. The
imagery dimension also requires a resolvable local image asset unless an
explicit owner-approved exception is recorded. Missing evidence or incomplete
provenance is `BLOCKED`; a criterion below the minimum is `FAIL` and has no
averaging escape hatch.

The premium rubric dimensions are `BRIEF_AND_BRAND_FIDELITY`,
`VISUAL_HIERARCHY`, `TYPOGRAPHY`, `COMPOSITION_AND_ART_DIRECTION`,
`IMAGERY_AND_VISUAL_WORLD`, `PREMIUM_DISTINCTIVENESS`, `MEMORABILITY`,
`POLISH_AND_CRAFT`, `RESPONSIVE_QUALITY`, `CONVERSION_CLARITY`, and
conditional `MOTION_QUALITY`. Every applicable required dimension must meet
`8/10`; hard-gate failures make the quality result `FAIL`.

Technical verification, quality evaluation, owner acceptance, and production
certification remain separate. A replayed quality result is never owner
approval, a production release, a rights clearance, or a deployment
authorization. Historical scores and verdicts are preserved as
`LEGACY_UNSUBSTANTIATED_QUALITY_CLAIM` or another explicit historical
classification and are never silently rewritten into current evidence.

The pilot manifest is
`templates/website-outcome-case-manifest.json`; its report shape is
`schemas/website-outcome-report.schema.json`. The manifest is deliberately
blocked for the exact rejected Alpha Starts Now cinematic/reference specimen
because that specimen and a fresh independent critique are not locally
traceable. The current candidate receipt is not relabeled as that rejection.
