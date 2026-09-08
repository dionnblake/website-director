# Kernel refactor evidence

## Purpose
Preserve inspectable reduction and certification evidence for refactor/kernel.

## Ownership
Inventories, baseline/final reports, reduction metrics, independent review and handoff.

## Local Contracts
- FEATURE_FREEZE = ACTIVE. Evidence is not a new runtime authority or capability.
- Never generate websites, alter frozen projects, or create production evidence here.
- Preserve the failed concurrent baseline attempt and the isolated successful rerun.
- Worktree inventories contain paths and Git facts, not credential contents.
- SAFE_TO_PRUNE is advisory only; this task authorizes no pruning or evidence deletion.

## Work Guidance
Derive counts from the named checkout, preserve exact sources, and distinguish
unreproduced historical reports from verified current facts.

## Verification
Retain suite exits, the framework-generated report, verify.js output and frozen
hash inventory. No waived failures or invented production certification.

## Child DOX Index
None.
