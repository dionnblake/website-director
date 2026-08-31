# RESEARCH SYNTHESIS: [PROJECT NAME]

> **Date Created:** YYYY-MM-DD
> **Status:** DRAFT | APPROVED
> **Stage:** Visual Research Director — Step 7 (Hand-off to Design Direction)
> **Rule:** Turn research into decisions. This is not a summary of websites.

---

## 1. Industry Reality
[What visitors to this industry actually expect on arrival — synthesized from `competitor-landscape.md` §2.]

---

## 2. Industry Clichés
[What should be deliberately avoided — synthesized from `competitor-landscape.md` §2.]

---

## 3. Best-in-Class Lessons
[What the strongest studied references (`inspiration-board.md`, `reference-deconstruction.md`) do better than the industry average, and why.]

---

## 4. Cross-Industry Lessons
[What useful, strategically-justified ideas come from adjacent/aspirational sectors — from `inspiration-board.md` §2.]

---

## 5. Design Opportunity
[How this specific client can stand apart, tying directly to `competitor-landscape.md` §3 (Differentiation Whitespace) and this client's actual business truth — not aspiration alone.]

---

## 6. Visual Principles to Carry Forward

| Principle | Source | Why It Applies to This Client |
| :--- | :--- | :--- |
| [Specific principle] | [Which reference/study it came from] | [Concrete tie to this client's positioning] |

---

## 6.5. Reference Evidence Ledger

Record every external candidate that materially informs this synthesis. MCP
rows use `Source Type: design_inspiration_mcp`; other research channels retain
their existing source type. This ledger records evidence and interpretation,
not production assets or implementation tokens.

| Platform | Source URL | Query | Grade | Why Selected | Pattern to Learn | What Not To Copy | Production Plausibility | Accessibility Risk | Implementation Risk | Retrieved At | Upstream Commit | Copyright Boundary |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [Platform or NOT_APPLICABLE] | [Exact URL] | [Exact query or NOT_APPLICABLE] | [A/B/C/D/UNASSESSED] | [Client-specific reason] | [Transferable mechanic] | [Composition/assets/copy] | [HIGH/MEDIUM/LOW/UNASSESSED] | [Risk or UNASSESSED] | [LOW/MEDIUM/HIGH/UNASSESSED] | [ISO timestamp] | [SHA or NOT_APPLICABLE] | `REFERENCE_ONLY` |

MCP image URLs remain research pointers. Asset Director controls all
production image selection, licensing, provenance, and optimization.

---

## 7. Motion Principles to Carry Forward

| Principle | Source | Why It Applies to This Client |
| :--- | :--- | :--- |
| [Specific principle] | [Which reference/study it came from] | [Concrete tie to this client's positioning] |

*(Feeds `templates/motion-direction.md` — this section recommends, it does not lock the motion level.)*

---

## 8. Principles Rejected
[Interesting ideas encountered during research that do not fit this client, and why — this section proves the research was filtered, not adopted wholesale.]

---

## 9. Recommended Archetype Input
- **Suggested Primary / Secondary / Accent (per `DESIGN-ARCHETYPES.md` 60/30/10):** [Recommendation, not a lock]
- **Rationale:** [Why this blend, tied to §5 and §6 above]
- *This is an input to `templates/design-direction.md` / `REFERENCE-PROTOCOL.md` — Website Director makes the final call there, not here.*

---

## 10. Recommended Motion Level
- **Suggested Level (0–3):** [Recommendation, not a lock]
- **Rationale:** [Tied to §7 above and `MOTION-DIRECTION-PROTOCOL.md` §4]
- *This is an input to `templates/motion-direction.md` — the actual lock happens there.*

---

## 11. Originality Check
- **How does the proposed synthesis remain distinct from every reference studied?** [Explicit answer — not "it's inspired by many sources so it's fine"]
- **Swap Test:** If every reference URL were revealed to the client, would they recognize any single one as "the site we copied"? [Must be no]
- **Convergence Check:** Does this synthesis land on the same archetype/motion combination that other unrelated clients researched under this protocol would also land on? If yes, return to `VISUAL-RESEARCH-PROTOCOL.md` §6 and re-run with more specific questions.

---

## 12. Synthesis Sign-Off
- [ ] Every section above is a decision or a rejection, not a restated fact.
- [ ] Originality Check (§11) completed honestly.
- [ ] Source provenance for every cited reference recorded per `RESEARCH-SOURCES.md` §7.
- [ ] The Reference Evidence Ledger (§6.5) is complete for every external candidate used.
- [ ] No reference has been cloned, and no MCP image or token has entered production implementation.
- [ ] `research.complete` may now be set to `true` in `site-profile.json`.
