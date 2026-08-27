# DESIGN QA RUBRIC & EVALUATION SYSTEM

> **Version:** 1.3.0  
> **Status:** Mandatory Design Quality Standard  
> **Total Score:** 100 Points (unchanged from V1 — see §5 for additive V1.1 supplemental dimensions)  
> **Rule:** Every review must identify specific areas for refinement, even on scores $\ge 95$.  
> **V1.1 Note:** The 100-point matrix below and its scoring remain exactly as validated in V1, so scores stay comparable across V1 and V1.1 projects. §5 adds V1.1-specific qualitative dimensions reported *alongside* the 100-point score — they are never folded into it.  
> **V1.3 Note:** Phase 11 Design QA outputs feed directly into Phase 11.5 (Website Gauntlet Subsystem), which subjects candidate builds to independent, fresh-context adversarial critics and dimensional Reference Bars.

---

## 1. 100-Point Design Evaluation Matrix

| Category | Weight | Evaluation Criteria |
| :--- | :---: | :--- |
| **1. Visual Hierarchy** | **15 pts** | - Instant primary focal point per viewport.<br>- Effortless eye-path through secondary and tertiary elements.<br>- Scale and contrast relationships are unmistakable. |
| **2. Brand Differentiation** | **15 pts** | - Visual language uniquely embodies this specific business.<br>- Zero generic template feel.<br>- Passes the "Swap Test" (would fail if placed on a competitor). |
| **3. Typography Execution** | **10 pts** | - Disciplined type pairing with clear classification contrast.<br>- Flawless line-height (leading) and letter-spacing (tracking).<br>- Strict adherence to mathematical type scale without rogue sizes. |
| **4. Composition & Spatial Cadence** | **10 pts** | - Mathematical grid integrity with balanced negative space.<br>- Asymmetric tension and visual breathing room.<br>- Zero visual crowding or arbitrary spatial gaps. |
| **5. Content Hierarchy & Clarity** | **10 pts** | - Value proposition understood in under 5 seconds.<br>- Scannable headings, subheads, and structured proof points.<br>- Zero dense, unformatted blocks of generic marketing text. |
| **6. Conversion Clarity & Flow** | **10 pts** | - Single primary conversion objective is visually dominant.<br>- Frictionless CTAs placed at natural decision points.<br>- Zero competing or confusing call-to-actions. |
| **7. Mobile Execution & Ergonomics** | **10 pts** | - Flawless reflow on small viewports without horizontal scroll.<br>- Touch targets $\ge 44\text{px} \times 44\text{px}$.<br>- Typography scales down gracefully while maintaining readability. |
| **8. Interaction Quality & Physics** | **5 pts** | - Cohesive, responsive hover, focus, and active states.<br>- Easing curves feel organic and premium (no jarring linear jumps).<br>- Micro-interactions reinforce user intent. |
| **9. Imagery & Art Direction** | **5 pts** | - High-resolution, art-directed assets with unified color grading.<br>- Zero generic corporate stock photos.<br>- Visual assets directly support comprehension or credibility. |
| **10. Accessibility & Usability** | **5 pts** | - WCAG AA contrast compliance across all text/background tokens.<br>- Clear, high-contrast keyboard focus indicators.<br>- Semantic HTML landmarks and alt attributes. |
| **11. AI-Slop Resistance** | **5 pts** | - Zero unmotivated purple gradients, floating pill cards, or 3-card loops.<br>- Every visual element satisfies the Seven Pillars of Justification.<br>- Passes all anti-slop checks from `DESIGN-CONSTITUTION.md`. |

---

## 1.1 Deterministic Pre-Scan Protocol (Impeccable Quality Engine)

Before scoring the 100-point matrix or conducting qualitative critique, execute the deterministic scan suite from `IMPECCABLE-ENGINE-PROTOCOL.md` §3. Record findings using the strict 4-method taxonomy (`DETERMINISTIC`, `HEURISTIC`, `LLM_CRITIQUE`, `VISUAL_COMPARISON`):

- **Deterministic Contrast Audit:** Mathematically verify that all text tokens satisfy WCAG AA ($\ge 4.5:1$ body, $\ge 3:1$ large). Flag any `gray-on-color` muddy contrast failures.
- **Transition Performance Audit:** Scan stylesheets for illegal layout-triggering properties (`transition: all`, `transition: width`, `transition: height`, `transition: margin`, `transition: top`).
- **Physics Audit:** Verify that easing curves snap to locked physics tokens; flag any `bounce-easing` curves.
- **Browser Surfaces Audit:** Verify that `::selection`, custom scrollbars, carets, and focus rings are explicitly themed from tokens.
- **Data Typography Audit:** Verify `font-variant-numeric: tabular-nums` on all metrics, stats, and pricing figures.

---

## 2. Quality Thresholds & Action Triggers

```
┌──────────────┬────────────────────────────────────────────────────────┐
│ 90 - 100 Pts │ PRODUCTION CANDIDATE: Proceed to Website Gauntlet.     │
├──────────────┼────────────────────────────────────────────────────────┤
│ 85 - 89 Pts  │ REFINEMENT REQUIRED: Minor token/spatial polish needed.│
├──────────────┼────────────────────────────────────────────────────────┤
│ 75 - 84 Pts  │ MAJOR REFINEMENT: Significant structural/type overhaul.│
├──────────────┼────────────────────────────────────────────────────────┤
│ Below 75 Pts │ DESIGN FAILURE: Reject build. Return to design phase.   │
└──────────────┴────────────────────────────────────────────────────────┘
```

---

## 3. The Premium Perception Test (Qualitative Audit)

The reviewer must explicitly answer the following 7 diagnostic questions with a qualitative rating (**Pass / Flag / Fail**) and detailed reasoning:

1. **CUSTOMNESS:** Does this interface feel like a master art director crafted this specific layout for this specific company, or does it look like an assembled theme?
2. **SPECIFICITY:** Could this exact site design be used for another company in a different sector simply by changing the logo and text?
3. **MEMORABILITY:** What single visual signature, layout device, or interaction will the visitor remember 24 hours later?
4. **CRAFT:** Are typographic tracking, optical margins, border contrasts, and spatial intervals executed with surgical precision?
5. **CONSISTENCY:** Does the lower half of the page (features, testimonials, FAQ, footer) exhibit the exact same high-standard art direction as the hero?
6. **POSITIONING:** Does the perceived visual quality match or exceed the pricing tier and market authority of the company?
7. **AI DETECTION:** Does the website trigger subconscious "AI template" cues (e.g., generic pill tags, floating dashboard UI, fake statistics)?

---

## 4. The "More Expensive" Action Directive

Every review output (`templates/design-review.md`) MUST conclude with the **Top 3 Highest-Impact Improvements to Make the Website Look More Expensive**:

1. **[Improvement 1]:** (Specific typographic, spatial, or color token enhancement)
2. **[Improvement 2]:** (Specific compositional, grid, or layout hierarchy enhancement)
3. **[Improvement 3]:** (Specific material, imagery, or proof presentation enhancement)

---

## 5. V1.1 Supplemental Dimensions (Reported Alongside the 100-Point Score, Not Folded Into It)

These four dimensions exist because V1.1 introduces two new failure modes V1 could not produce: research-driven imitation, and gratuitous or absent motion. Each is scored **Pass / Flag / Fail** with written reasoning, the same qualitative format as the Premium Perception Test in §3.

### 5.1 Reference Intelligence
- *Test Question:* Did external research (`research-synthesis.md`) materially improve the design, or was research performed and then ignored? Does the result demonstrate awareness of strong current web design without imitating a specific source?
- **Fail condition:** Research artifacts exist but the locked design direction shows no traceable influence from them, or shows influence that is a direct reproduction of one studied reference's composition.

### 5.2 Motion & Life
- *Test Question:* Does the website feel appropriately alive for this specific business? Is every motion behavior intentional and justified against the Six Motion Justifications in `MOTION-DIRECTION-PROTOCOL.md` §3? Is anything static that should move — or anything moving that should remain still?
- **Fail condition:** Unjustified motion is present (fails the justification test), or the locked motion level does not match what actually shipped.

### 5.3 Cinematic Restraint
- *Test Question (only applicable when the `cinematic-sites` specialist was engaged):* Does the cinematic functionality strengthen brand storytelling, or is it simply showing off the technology? Does the build stay inside `cinematic-brief.md`, or did the specialist's own creative defaults leak through (see `CINEMATIC-INTEGRATION-PROTOCOL.md` §3)?
- **Fail condition:** Cinematic modules or hero treatment are present with no traceable tie to brand storytelling, or the build contradicts a value the brief explicitly specified (typography, composition, palette).

### 5.4 Originality & Anti-Homogenization
- *Test Question:* Can the design be traced too directly to a specific researched reference? Could this design belong to another client researched under the same protocol, with only the logo swapped? Did reference research increase specificity, or reduce it?
- **Explicit checks to run:**
  - Does this site's design emerge from the client's actual positioning, or from a fashionable pattern research happened to surface?
  - Is the hero disproportionately complex compared with the business it represents?
  - Would this site's Motion Level and archetype blend be *different* from what an unrelated client in a different industry, researched under the same protocol, would receive? (If every project converges on the same cinematic-dark-editorial-parallax answer, this dimension fails regardless of craft quality elsewhere.)
- **Fail condition:** The design can be traced too directly to one reference, or the diversity check above fails. A site that looks impressive but generic fails this dimension even at a high 100-point score.

**Scoring note:** A `Fail` on any one of §5.1–§5.4 does not automatically zero out the 100-point score, but it blocks the `PRODUCTION CANDIDATE` verdict regardless of the numeric score — remediate the failed dimension and re-review before authorizing production.

---

## 6. Phase 11.5 Handoff: The Website Gauntlet

Achieving a $\ge 90$ score in Phase 11 Design QA qualifies a build as a candidate for **Phase 11.5: Website Gauntlet Subsystem** (`WEBSITE-GAUNTLET-PROTOCOL.md`). The Gauntlet subjects the build to independent adversarial critics under fresh context and compares it against named Reference Bars across specific quality dimensions before Phase 12 pre-flight sign-off.

