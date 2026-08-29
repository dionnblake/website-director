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

### 5.5 Intent Fidelity (V1.8 Supplemental Dimension)
- *Test Question:* Does the final design and copy execution faithfully satisfy the owner-confirmed Creative Intent Contract (`templates/creative-intent-contract.md`)?
- **Explicit checks to run:**
  - Does the build solve the confirmed primary conversion objective?
  - Does the first-3-second emotional impression match the confirmed desired feeling?
  - Are all anti-brand boundaries, banned clichés, and competitor negative constraints strictly respected?
  - Does the visual craft and density match the confirmed `CREATIVE_AMBITION` (`STANDARD`, `PREMIUM`, `SHOWCASE`, `EXPERIMENTAL`) and visual intensity?
  - Are all `OWNER_NON_NEGOTIABLES` fully honored without exception?
- **Fail condition:** The build violates confirmed anti-brand boundaries, ignores owner non-negotiables, misses the core commercial job, or fails to reach the declared creative ambition level.

### 5.6 Asset Art Direction & Visual Authenticity (V2.0 Supplemental Dimension)
- *Test Question:* Does the website visual asset ecosystem exhibit professional art direction, visual coherence, legal provenance, and factual authenticity per `ASSET-DIRECTOR-PROTOCOL.md`?
- **Explicit checks to run:**
  - Does the Hero Asset satisfy `HERO_ASSET_STRENGTH` (Instant focal anchor, cognitive thesis proof, clean text contrast, and crisp mobile crop)?
  - Is there a dedicated, high-impact `SIGNATURE_ASSET` for `SHOWCASE` tier projects?
  - Do all photographic, 3D, and graphic assets share a unified `PRIMARY_VISUAL_LANGUAGE` and color grade profile?
  - Is all factual brand evidence (founders, facilities, products, clinical results) 100% authentic with zero fake AI-generated evidence?
  - Are all generated images completely free of AI artifacts (`AI_ARTIFACT_CHECK = PASS`)?
  - Is generic corporate stock photography completely absent?
  - Do all assets have verified provenance and commercial web licensing in `asset-provenance.md`?
  - Does the lower half of the page maintain the same high asset quality as the hero (`MEDIA_QUALITY_BELOW_HERO`)?
- **Fail condition:** Generic stock imagery, AI artifacts, unauthenticated factual claims, missing mobile crops, or visual style incoherence between sections.

### 5.7 Immersive 3D Craft & Spatial Restraint (V2.1 Supplemental Dimension)
- *Test Question:* Does the WebGL / Three.js 3D implementation solve a genuine spatial communication problem without generic demo slop, unhandled fallbacks, or performance degradation per `IMMERSIVE-WEB-PROTOCOL.md`?
- **Explicit checks to run:**
  - Does the 3D scene satisfy the **10-Point Immersive Justification Matrix** (spatial necessity, not novelty)?
  - Is the scene completely free of generic demo slop (floating glass blobs, unmotivated neon grids, random glowing toruses)?
  - Are primary headlines, CTAs, navigation, and key specifications 100% accessible in semantic HTML DOM outside the canvas?
  - Is there an operational, zero-CLS 2D fallback (`WEBGL_FALLBACK`) verified when WebGL fails or is disabled?
  - Is the `prefers-reduced-motion` policy active and tested (camera/object motion frozen without informational loss)?
  - Does mobile execution follow `MOBILE_3D_POLICY` with bounded DPR (`<= 1.5`) and touch-safe framing?
  - Are Three.js resource disposal routines (`disposeScene()`) and visibility throttling (`document.hidden`) properly implemented?
- **Fail condition:** Unjustified 3D, generic demo aesthetics, missing 2D fallback, inaccessible content trapped in WebGL, frame drops below 30 FPS, or memory leaks on unmount.

### 5.8 Rive Interactive Motion & State Machine Integrity (V2.2 Supplemental Dimension)
- *Test Question:* Does the Rive interactive vector motion communicate multi-state logic or UI feedback better than simpler CSS/GSAP alternatives without gratuitous mascot slop, hover traps, or unhandled WASM fallbacks per `RIVE-INTERACTIVE-MOTION-PROTOCOL.md`?
- **Explicit checks to run:**
  - Does the Rive component satisfy the **Technology Selection Matrix** (state machine necessity over simple CSS/GSAP)?
  - Is the vector art completely free of generic mascot tropes, random bouncing blobs, or unmotivated eye-tracking?
  - Are all essential interactive states accessible on touch/mobile and keyboard (no hover-only essential behavior)?
  - Are numerical values, state labels, and instructions mirrored in accessible semantic HTML outside the canvas?
  - Is `prefers-reduced-motion` verified (idle loops stopped, state transitions snap cleanly)?
  - Is an operational zero-CLS fallback (`STATIC_SVG`, `STATIC_IMAGE`, or `HTML_COMPONENT`) verified when WASM fails or `?forceRiveFallback=1` is provided?
  - Does the Rive instance implement explicit lifecycle cleanup (`rive.cleanup()`) on unmount?
- **Fail condition:** Hover-only critical states, missing semantic DOM mirroring, unhandled runtime fallback, cartoon mascot slop, or memory leaks on navigation.

### 5.9 Page Experience & Navigation Continuity (V2.3 Supplemental Dimension)
- *Test Question:* Does the page transition and route continuity architecture preserve user orientation, reinforce information hierarchy, and support native browser behavior without gratuitous loading slop, history breakage, or accessibility failure per `PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md`?
- **Explicit checks to run:**
  - Does the transition satisfy the **Transition Justification Gate** (meaningful contextual continuity, not decoration for its own sake)?
  - Is the build free of Anti-Transition Slop (no fullscreen black curtains, no 2-second loading spinners, no generic template wipes)?
  - Are real URLs, browser Back/Forward (`popstate`), deep linking, and page refresh fully preserved?
  - Does scroll restoration behave correctly (`TOP_ON_NEW_ROUTE` on forward navigation; reading context restored on Back)?
  - Does `prefers-reduced-motion: reduce` bypass or simplify route animations without breaking navigation?
  - Is failure recovery verified (`TRANSITION_FAILURE_POLICY = STANDARD_NAVIGATION` when scripts fail or `?forceTransitionFallback=1` is used)?
  - Are Three.js render loops and Rive state machine instances cleanly torn down on route departures?
- **Fail condition:** Broken browser history, blank loading screens, disorienting navigation wipes, inaccessible focus on route change, or failure to fall back gracefully.

### 5.10 CRO & Analytics Architecture (V2.4 Supplemental Dimension)
- *Test Question:* Does the website implement a disciplined, data-minimized conversion and analytics architecture that aligns business outcomes with visitor outcomes without dark patterns, surveillance bloat, or brittle runtime dependencies per `CONVERSION-ANALYTICS-PROTOCOL.md` — with every critical CTA traceable to an event, an observable funnel, no fabricated baselines, and planning state never reported as production success?
- **Explicit checks to run:**
  - Are `PRIMARY_BUSINESS_OUTCOME` and `PRIMARY_VISITOR_OUTCOME` clearly defined and mutually aligned?
  - Does the implementation distinguish `MACRO`, `MICRO`, and `DIAGNOSTIC` interactions rather than treating every click as a conversion?
  - Does the event manifest follow semantic naming (`object_action`) with zero forbidden PII fields (`PII_IN_ANALYTICS = 0`)?
  - Is the website 100% functional when analytics is blocked, disabled, or encounters an exception (`ANALYTICS_FAILURE_POLICY = SITE_FUNCTIONAL`)?
  - Are page views deduplicated across View Transitions and browser history navigation?
  - Does conversion submission prevent duplicate firing on rapid clicks?
  - Is the site 100% free of deceptive dark patterns (`DARK_PATTERN_CHECK = PASS` — zero fake scarcity, countdowns, confirmshaming, hidden opt-outs)?
  - Are experiment hypotheses structured with clear guardrail metrics (lead quality, brand perception, accessibility, performance)?
  - Are synthetic or inconclusive test samples properly recorded as `INSUFFICIENT_EVIDENCE` without declaring premature winners?
  - Is high-sensitivity session replay disabled by default (`SESSION_REPLAY = DISABLED`)?
- **Fail condition:** Capturing PII in analytics, deceptive dark patterns, duplicate conversion events, broken site functionality when analytics is blocked, fake experiment winner claims, or unmotivated surveillance tracking.

**Scoring note:** A `Fail` on any one of §5.1–§5.10 does not automatically zero out the 100-point score, but it blocks the `PRODUCTION CANDIDATE` verdict regardless of the numeric score — remediate the failed dimension and re-review before authorizing production.

---

## 6. Phase 11.5 Handoff: The Website Gauntlet

Achieving a $\ge 90$ score in Phase 11 Design QA qualifies a build as a candidate for **Phase 11.5: Website Gauntlet Subsystem** (`WEBSITE-GAUNTLET-PROTOCOL.md`). The Gauntlet subjects the build to independent adversarial critics under fresh context and compares it against named Reference Bars across specific quality dimensions before Phase 12 pre-flight sign-off.

