# VISUAL RESEARCH PROTOCOL: THE VISUAL RESEARCH DIRECTOR ROLE

> **Version:** 1.1.0
> **Status:** Mandatory Operating Standard (V1.1 Extension)
> **Rule:** See, investigate, compare, deconstruct, synthesize — then hand off. Never design, never build, never clone.

---

## 1. Why This Exists

Website Director V1 formed visual direction from business discovery, internal design archetypes, and the Design Constitution alone. That is sufficient to prevent AI-slop improvisation, but it is not sufficient to prove that the resulting design reflects genuine awareness of the current visual landscape. A real senior design director has seen thousands of sites; Website Director V1 had not looked at any before choosing a direction.

V1.1 closes that gap with a bounded research phase that runs **before** `DESIGN_DIRECTION_LOCKED`, not instead of the archetype system in `DESIGN-ARCHETYPES.md`. Research informs which archetype/blend is selected and why; it does not replace the catalog.

```
SEE ──► INVESTIGATE ──► COMPARE ──► DECONSTRUCT ──► SYNTHESIZE ──► DESIGN
```

---

## 2. Role Boundary: The Visual Research Director

Visual Research Director is a **bounded role and protocol**, not a separate persistent agent. Website Director remains the sole orchestration authority end to end; the same session executes this phase (optionally as one isolated subagent call for context hygiene when the harness supports it — never as a standing swarm member). This mirrors how "Independent QA" in V1 is a role, not new infrastructure.

**Its job ends before final design direction is created.**

| It DOES | It DOES NOT |
| :--- | :--- |
| Research industry, competitor, and cross-industry references | Build the website |
| Discover candidates via Landbook | Select final design unilaterally |
| Run bounded deep reconnaissance on shortlisted references | Copy websites |
| Extract and document transferable principles | Lock `DESIGN_DIRECTION_LOCKED` |
| Produce `research-synthesis.md` with explicit recommendations | Implement components |
| Recommend a motion level with rationale | Override Website Director's final call |

Website Director reads the synthesis, weighs it against `DESIGN-ARCHETYPES.md` and the client's actual positioning, and makes the design-direction call itself.

---

## 3. The Research Pipeline

```
┌──────────────────────────────────────────────────────────┐
│ STEP 1: RESEARCH BRIEF                                    │
│   Derived from DISCOVERY-PROTOCOL.md Stages 1–2            │
│   → templates/research-brief.md                            │
├──────────────────────────────────────────────────────────┤
│ STEP 2: INDUSTRY LANDSCAPE RECONNAISSANCE                  │
│   10–15 real competitors/peers, per RESEARCH-SOURCES.md §2 │
│   → templates/competitor-landscape.md                      │
├──────────────────────────────────────────────────────────┤
│ STEP 3: LANDBOOK + CROSS-INDUSTRY DISCOVERY                │
│   Candidate references organized by design purpose         │
│   → templates/inspiration-board.md                         │
├──────────────────────────────────────────────────────────┤
│ STEP 4: PROGRESSIVE FILTERING                               │
│   10–15 candidates → 5 strong references → 2–3 deep targets│
│   Per RESEARCH-SOURCES.md §6                                │
├──────────────────────────────────────────────────────────┤
│ STEP 5: DEEP RECONNAISSANCE (bounded targets only)          │
│   Per REFERENCE-RECON-PROTOCOL.md, RESEARCH_ONLY_MODE       │
│   → templates/reference-deconstruction.md                  │
├──────────────────────────────────────────────────────────┤
│ STEP 6: MOTION RESEARCH                                     │
│   Per MOTION-DIRECTION-PROTOCOL.md                          │
│   → feeds templates/motion-direction.md (Phase 8, later)    │
├──────────────────────────────────────────────────────────┤
│ STEP 7: RESEARCH SYNTHESIS                                  │
│   Turns findings into decisions, not a summary of websites  │
│   → templates/research-synthesis.md                        │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
                  [ RESEARCH_COMPLETE ]
                            │
                            ▼
     Hand off to REFERENCE-PROTOCOL.md / DESIGN-ARCHETYPES.md
        for actual DESIGN_DIRECTION_LOCKED formation
```

`research-synthesis.md` is the hand-off artifact. It must populate `templates/reference-analysis.md`'s 12-vector matrix (if the client's direction ultimately draws on specific references) or inform archetype/blend selection in `DESIGN-ARCHETYPES.md` (if it does not) — it does not create a third, parallel design-selection path.

---

## 4. `RESEARCH_COMPLETE` — A Readiness Gate, Not a Design Lock

`research.complete` in `site-profile.json` is a **readiness gate**, semantically distinct from the four (now five) design-approval locks in `locks{}`. It answers "is there enough visual intelligence to design responsibly?" — not "has the owner approved a design." Website Director may not issue `DESIGN_DIRECTION_LOCKED` until `research.complete` is `true`, but flipping `research.complete` to `true` requires no owner sign-off the way a lock does; it requires the research artifacts below to exist and be populated.

**Required for `research.complete: true`:**
- `templates/competitor-landscape.md` populated (industry landscape research exists).
- `templates/inspiration-board.md` populated (Landbook + cross-industry discovery exists).
- Deep reconnaissance completed on the identified 2–3 targets where the shortlist warranted it (`reference-deconstruction.md` populated, or explicitly noted as "no target warranted deep recon").
- `templates/research-synthesis.md` populated, including its Originality Check section.
- Source provenance recorded per `RESEARCH-SOURCES.md` §7 for every reference cited.

**`research.mode` values:** `"full"` (all four channels run), `"bounded"` (scoped down for project size, see §5), `"exception"` (skipped, see §5).

---

## 5. The Bounded Exception

Website Director may permit research to be skipped or scoped down only for:
- **Extremely small projects** (e.g., a single-page site with no meaningful competitive landscape to study).
- **Explicit user opt-out** (the owner states they do not want research performed).
- **Unavailable internet access** (no live browsing/search tool available in the current environment).

**The exception must be recorded, never silently applied.** Set:
```json
"research": {
  "complete": true,
  "mode": "exception",
  "exception": { "applied": true, "reason": "Owner opt-out — single-page portfolio, no competitive set to study." }
}
```
`research.complete` may be set to `true` under an exception, but the reason must name which of the three conditions above applied and why. A missing or vague reason is treated as an unrecorded skip and blocks `DESIGN_DIRECTION_LOCKED`.

---

## 6. Anti-Homogenization Discipline (Applied During Research, Not Just at QA)

Research is the stage where homogenization risk is created, even though it is caught at QA (`QA-RUBRIC.md` §5). While running this protocol, continuously ask:
- Is this finding pointing toward something specific to this client, or toward whatever is fashionable right now?
- If three unrelated clients ran this same research pipeline, would they end up recommending the same archetype blend and motion level? If yes, the research questions were too generic — go back and re-ask them against this client's actual positioning.

Research must increase specificity. If a research pass produces a *less* differentiated recommendation than the client's own discovery answers already implied, the synthesis has failed and must be redone.
