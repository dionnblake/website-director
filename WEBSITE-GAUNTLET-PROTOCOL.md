# WEBSITE GAUNTLET PROTOCOL: ADVERSARIAL REFINEMENT & QUALITY-BAR GOVERNANCE

> **Version:** 1.0.0 (Website Director V1.3.0 Subsystem)  
> **Status:** Mandatory Quality & Refinement Standard  
> **Governance:** Website Director Orchestration Rail (`SKILL.md` §2, Phase 11.5)  
> **Attribution:** Adapted from the Gauntlet Loop methodology originally conceived by **Matt Shumer** ([Claude of Duty](https://github.com/mshumer/Claude-of-Duty)), packaged and licensed by **Jay E. / RoboNuggets** ([gauntlet-loop](https://github.com/robonuggets/gauntlet-loop)) under the Creative Commons Attribution 4.0 International License ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)).

---

## 1. Core Mission & Philosophy

The **Website Gauntlet** is Website Director's adversarial quality-refinement subsystem. Most AI-generated web builds stall at "good enough" because the builder evaluates its own work against self-inflating rubrics. The Website Gauntlet solves this by establishing a rigorous, adversarial feedback loop:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           THE GAUNTLET INVARIANT                         │
│                                                                          │
│                          BUILDER != CRITIC                               │
│                                                                          │
│  The agent or subagent that produced an artifact must NEVER be the sole │
│  authority deciding whether that artifact meets the quality bar.         │
└──────────────────────────────────────────────────────────────────────────┘
```

### Core Tenets:
1. **Adversarial Defect Discovery:** Praise is useless. The sole objective of a Gauntlet evaluation is finding defects, gaps, and weaknesses.
2. **Fresh-Context Evaluation:** Evaluators inspect the actual rendered output with clean, unpolluted context—unaware of how difficult the build was or what constraints the builder faced.
3. **Single Largest Remaining Gap:** Every failed evaluation must isolate the single highest-priority quality gap (`BIGGEST_REMAINING_GAP`) to focus remediation.
4. **Targeted Repair Discipline:** The builder performs the *smallest safe modification* that closes the identified gap. Full-site rewrites on isolated defects are strictly prohibited.
5. **Strict Lock Immutability:** The Gauntlet has zero authority to silently modify locked decisions. If a locked token or structure prevents reaching the bar, the Gauntlet halts and issues a formal `LOCKED_CHANGE_REQUIRED` Change Request for owner review.
6. **Resource Governance:** Refinement loops are strictly governed by iteration caps and diminishing-return circuit breakers. When the cap is reached without a pass, the system reports `GAUNTLET_CAP_REACHED`—it never fakes a `PASS`.

---

## 2. The Reference Bar Quality Standard

The Gauntlet does not evaluate against subjective abstractions like "award-winning design," "modern aesthetic," or "clean UI." Every Gauntlet comparison is anchored against a concrete **Reference Bar**.

A valid Reference Bar must satisfy the **Three Bar Invariants**:

```
┌──────────────┬────────────────────────────────────────────────────────┐
│ 1. NAMED     │ A specific, identifiable production website, page, or  │
│              │ approved benchmark (e.g., "Linear.app Pricing Page",   │
│              │ "Stripe Checkout", "Polestar 3 Product Overview").     │
├──────────────┼────────────────────────────────────────────────────────┤
│ 2. FETCHABLE │ The evaluator must be capable of inspecting the actual │
│              │ artifact (DOM, screenshot, recording, or live URL).    │
│              │ If the agent cannot fetch it, comparison is invalid.   │
├──────────────┼────────────────────────────────────────────────────────┤
│ 3. COMPARABLE│ The reference and build can sit side-by-side on the    │
│              │ specific dimension being judged for a binary pick.     │
└──────────────┴────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **References are Quality Bars, NOT Templates to Clone.**  
> A reference establishes the required standard of craft, typography, density, rhythm, or motion. It is never an instruction to copy layout, brand assets, copy, or color values.

---

## 3. Dimensional Reference Bars (`REFERENCE_BAR`)

Website builds are multi-dimensional. A single reference rarely exemplifies perfection across every subsystem. Website Director supports **Dimensional Reference Bars**, assigning specific benchmarks to specific evaluation vectors:

| Reference Bar Dimension | Evaluation Focus | Example Benchmark |
| :--- | :--- | :--- |
| **`Typography Bar`** | Typographic scale, tracking, hierarchy, font pairing contrast, optical alignment. | *The New Yorker* editorial archives, *Koto Studio* case studies. |
| **`Motion Bar`** | Choreography, physics, easing, micro-interactions, scroll pacing, restraint. | *Apple Pro Display* scroll narrative, *Stripe Press* page turns. |
| **`Hero Bar`** | Above-the-fold impact, value clarity in < 5s, focal anchor, grid tension. | *Vercel Ship* event hero, *Arc Browser* product canvas. |
| **`Brand Atmosphere Bar`** | Emotional posture, materiality, lighting, distinctiveness, immersion. | *Aesop* skincare flagship, *B&O* sound narrative. |
| **`Conversion Bar`** | Frictionless CTAs, value articulation, cognitive progression, decision velocity. | *Basecamp* signup flow, *Linear* feature conversion funnel. |
| **`Navigation / IA Bar`** | Header footprint, progressive disclosure, menu ergonomics, breadcrumbs. | *Raycast* extensions directory, *GitHub Docs* navigation tree. |
| **`Editorial Bar`** | Narrative flow, scannability, pull-quotes, data presentation, rhythm. | *Stripe Press* monographs, *McKinsey Quarterly* deep dives. |
| **`Mobile Bar`** | Mobile reflow, thumb-zone ergonomics, touch targets $\ge 44\text{px}$, typography scaling. | *Shopify* mobile checkout, *Cash App* landing experience. |

### Reference Bar Rationale Rule:
Every declared `REFERENCE_BAR` in `site-profile.json` must document **why** it exists, its specific assigned dimensions, and its fetchable source URI/artifact.

---

## 4. The Eight Specialized Website Critics (Impeccable-Enhanced)

The Website Gauntlet deploys up to eight specialized, domain-specific adversarial critics. Each critic operates independently, leveraging deterministic scans and craft heuristics from `IMPECCABLE-ENGINE-PROTOCOL.md`:

```
                      ┌────────────────────────────────────────┐
                      │        WEBSITE GAUNTLET ENGINE         │
                      └───────────────────┬────────────────────┘
                                          │
         ┌────────────┬────────────┬──────┴─────┬────────────┬────────────┐
         ▼            ▼            ▼            ▼            ▼            ▼
     ┌───────┐    ┌───────┐    ┌───────┐    ┌───────┐    ┌───────┐    ┌───────┐
     │ CRAFT │    │ BRAND │    │ CONV. │    │ TRUST │    │ MOTION│    │SLOP-QA│
     │CRITIC │    │CRITIC │    │CRITIC │    │CRITIC │    │CRITIC │    │CRITIC │
     └───────┘    └───────┘    └───────┘    └───────┘    └───────┘    └───────┘
                                   ▲            ▲
                                   │            │
                              ┌────┴────┐  ┌────┴────┐
                              │ A11Y    │  │REFERENCE│
                              │ CRITIC  │  │ CRITIC  │
                              └─────────┘  └─────────┘
```

### 4.1 Craft Critic (Enhanced by Impeccable)
- **Focus:** Composition, typography, hierarchy, spacing, density, optical alignment, and aesthetic polish.
- **Key Checks & Deterministic Rules:**
  - Are spatial intervals mathematically consistent with the 8-point baseline grid? (`skill-layout-spacing-rhythm`)
  - Typography floor: Measure 65–75ch for body text, tracking floor -0.04em, balanced headings.
  - Tabular numerals: `font-variant-numeric: tabular-nums` declared on metrics, numbers, and tables.
  - Browser surfaces theming: `::selection`, focus rings, scrollbars, and carets styled from design tokens. (`skill-craft-browser-surfaces`)
- **Defects:** Loose padding, awkward line wraps, unmapped font sizes, misaligned baselines, unthemed browser defaults.

### 4.2 Brand Critic
- **Focus:** Brand distinctiveness, emotional posture, visual identity, and anti-brand compliance.
- **Key Questions:**
  - Does this design instantly project the brand attributes defined in `positioning.md`?
  - Does it pass the **Swap Test** (would it fail if placed on a competitor)?
  - Does it respect all anti-brand boundaries (what NOT to look like)?
- **Defects:** Generic SaaS styling for an artisanal luxury brand, sterile corporate look for an energetic startup, identity drift.

### 4.3 Conversion Critic
- **Focus:** Primary/secondary conversion clarity, CTA dominance, visitor friction, and objection handling.
- **Key Questions:**
  - Is the primary conversion goal obvious within 5 seconds of scanning?
  - Are CTAs placed at natural cognitive decision points (`Understand` $\rightarrow$ `Believe` $\rightarrow$ `Evaluate` $\rightarrow$ `Convert`)?
  - Are primary objections addressed before the main conversion commitment?
- **Defects:** Competing CTAs, buried action buttons, unclear value exchange, premature asks before establishing value.

### 4.4 Trust Critic
- **Focus:** Evidence placement, claims verification, proof density, credentials, and risk reduction.
- **Key Questions:**
  - Is every major marketing claim supported by verifiable evidence or concrete data?
  - Are customer testimonials specific, attributed, and credible (vs generic praise)?
  - Are institutional credentials, security assurances, or guarantees visible at friction points?
- **Defects:** Unattributed quotes, floating checkmarks without context, fake statistics, missing reassurance near CTAs.

### 4.5 Motion Critic (Enhanced by Impeccable)
- **Focus:** Purpose of motion, timing, physics, easing, continuity, performance, and accessibility.
- **Key Checks & Deterministic Rules:**
  - Does every motion behavior satisfy at least one of the **Six Motion Justifications** (`MOTION-DIRECTION-PROTOCOL.md` §3)?
  - Transition performance: Zero animation of layout triggers (`width`, `height`, `margin`, `top`). Compositor-only (`transform`, `opacity`). (`skill-ban-layout-transition`)
  - No toy bounce easing (`cubic-bezier(0.68, -0.55, 0.265, 1.55)`). Smooth exponential ease-out required. (`skill-ban-bounce-easing`)
  - No repetitive section fade-up cascades on every scroll block. (`skill-motion-no-section-fade`)
  - `prefers-reduced-motion` honored with zero broken layout shifts or lost feedback states.
- **Defects:** Gratuitous bouncing cards, uncoordinated fade-ups on every paragraph, layout-triggering transitions, sluggish animation curves.

### 4.6 AI-Slop Critic (Enhanced by Impeccable)
- **Focus:** Detection of recurring machine-generated design clichés and uncurated web templates.
- **Key Checks & Deterministic Rules:**
  - Scans for all 18 detector rules from `IMPECCABLE-ENGINE-PROTOCOL.md` §3 (AI color palettes, radial halos, 3-card loops, dark glow halos, hero eyebrow chips, side-tab borders, pulsing dots).
  - Enforces morphological diversity across sequential sections (preventing template fatigue).
  - Eliminates unmotivated decorative containers, pill tags, and floating fake UI cards.
- **Defects:** Purple/indigo gradient fills, floating fake dashboard widgets, pill button monoculture, uniform card grids.

### 4.7 Accessibility Critic (Enhanced by Impeccable)
- **Focus:** WCAG AA compliance, color contrast, keyboard navigation, focus states, and readability.
- **Key Checks & Deterministic Rules:**
  - Contrast math verification: $\ge 4.5:1$ normal text, $\ge 3:1$ large bold text. (`skill-color-verify-contrast`)
  - Surface tinting: Flags neutral gray secondary text on colored backgrounds (`gray-on-color`).
  - Interactive elements accessible via keyboard with visible, high-contrast `:focus-visible` rings.
  - Touch targets $\ge 44\text{px} \times 44\text{px}$ on mobile viewports. (`skill-touch-target-floor`)
- **Defects:** Low-contrast muted text (`#888` on `#111`), missing focus indicators, inaccessible form inputs, undersized touch targets.

### 4.8 Reference Critic
- **Focus:** Direct dimensional comparison between Website Director build and approved Reference Bars.
- **Key Questions:**
  - When viewed side-by-side on the assigned dimension (e.g., typography or hero composition), does our build match or beat the reference?
  - Where is the quality gap most acute?
- **Defects:** Build fails to reach the level of polish, spatial discipline, or typographic rigor demonstrated by the benchmark.

### 4.9 Award Director / Visual Craft Critic
- **Focus:** Evaluation against international design award benchmarks (Awwwards Site of the Day, FWA of the Day, Webby Awards, Stripe Press, Locomotive/Active Theory caliber).
- **Key Questions:**
  - Does this website create an immediate, visceral emotional reaction of bespoke luxury and undeniable craft?
  - Does it break the generic AI-box-stacking layout rhythm with intentional editorial asymmetry, dynamic whitespace, and dramatic typographic hierarchy?
  - Does the motion feel physical and weighted (Lenis smooth inertia, split-mask text unmasking, horizontal pinned scrollytelling, magnetic micro-physics) rather than basic fade-ups?
  - Are textures and materiality tangible (organic grain noise, ambient mesh lighting, brushed tactile metals) instead of flat dark-mode boxes?
- **Defects:** Predictable box-stacking, flat dark-mode template vibes, uninspired fade-ins, lack of memorable visual anchor.

---

## 5. Conversion Context & Visitor Psychology

The Website Gauntlet grounds its conversion and trust evaluations in the project's commercial objectives. These fields are captured during Discovery / Positioning and recorded in `site-profile.json`:

```json
{
  "conversion_context": {
    "primary_conversion": "Schedule Technical Architecture Deep Dive",
    "secondary_conversion": "Download Technical Whitepaper",
    "target_visitor": "Enterprise CTO / VP Engineering evaluating database migration",
    "visitor_state": "High skepticism, burned by legacy vendor downtime, seeking performance benchmarks",
    "primary_objection": "Migration risk and operational disruption",
    "primary_trust_requirement": "Verified zero-data-loss architecture proof and enterprise case studies"
  }
}
```

---

## 6. Simulated Audience Panel (`SIMULATED_AUDIENCE_EVALUATION`)

To complement specialist critics, the Gauntlet can run a lightweight **Simulated Audience Panel** representing five distinct visitor mindsets:

```
┌──────────────────────────┬────────────────────────────────────────────────────┐
│ Persona                  │ Cognitive Focus & Evaluation Angle                 │
├──────────────────────────┼────────────────────────────────────────────────────┤
│ 1. READY BUYER           │ "How fast can I understand pricing and take        │
│                          │ action? Is the checkout/booking frictionless?"     │
├──────────────────────────┼────────────────────────────────────────────────────┤
│ 2. SKEPTICAL VISITOR     │ "Why should I believe these claims? What proof     │
│                          │ is missing? What smells like marketing hype?"      │
├──────────────────────────┼────────────────────────────────────────────────────┤
│ 3. FIRST-TIME VISITOR    │ "What does this company actually do in plain       │
│                          │ English? Is this built for someone like me?"       │
├──────────────────────────┼────────────────────────────────────────────────────┤
│ 4. COMPARISON SHOPPER    │ "How does this compare to known alternatives? What │
│                          │ is the single defensible differentiator?"          │
├──────────────────────────┼────────────────────────────────────────────────────┤
│ 5. RETURNING VISITOR     │ "Where is the documentation, login, or direct path │
│                          │ without re-reading top-of-funnel marketing?"       │
└──────────────────────────┴────────────────────────────────────────────────────┘
```

> [!CAUTION]
> **Simulated Audience Invariant:**  
> This panel is an analytical heuristic for defect discovery. It must ALWAYS be documented as `SIMULATED_AUDIENCE_EVALUATION` and must **NEVER** be misrepresented as real customer research.

---

## 7. The Gauntlet Execution Lifecycle

The Gauntlet operates in a structured 7-step cycle:

```
┌──────────────────────────────────────────────────────────────────────────┐
│ STEP 1: CAPTURE ARTIFACT STATE                                           │
│         Capture DOM, screenshots (1440px desktop + 390px mobile), CSS.   │
│                                                                          │
│ STEP 2: LOAD APPROVED REFERENCE BARS                                     │
│         Fetch reference benchmarks and isolate assigned dimensions.      │
│                                                                          │
│ STEP 3: ASSIGN INDEPENDENT CRITICS                                       │
│         Dispatch fresh-context critics (Craft, Brand, Conversion, etc.)  │
│                                                                          │
│ STEP 4: ADVERSARIAL EVALUATION & BLIND COMPARISON                        │
│         Strip labels where feasible; identify defects & assess quality.  │
│                                                                          │
│ STEP 5: SYNTHESIZE LARGEST REMAINING GAP                                 │
│         Isolate single highest-priority issue (BIGGEST_REMAINING_GAP).   │
│                                                                          │
│ STEP 6: LOCK BOUNDARY AUDIT & TARGETED REPAIR                            │
│         - If repair stays within tokens/spec: Builder executes fix.      │
│         - If repair requires changing locked token: Issue CHANGE REQUEST.│
│                                                                          │
│ STEP 7: RE-CAPTURE & RE-EVALUATE                                         │
│         Re-evaluate repaired artifact under fresh critic context.        │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 8. Strict Lock Protection & Change Management

The Gauntlet cannot override or alter locked design, IA, content, or motion decisions.

```
                  CRITIC DISCOVERS DEFECT
                            │
            Does remediation require changing
              a locked token or decision?
                            │
               ┌────────────┴────────────┐
               │                         │
              NO                        YES
               │                         │
               ▼                         ▼
      TARGETED CODE REPAIR    HALT GAUNTLET REPAIR
    (Builder applies fix within   Record LOCKED_CHANGE_REQUIRED
      locked specification)              │
                                         ▼
                               GENERATE CHANGE REQUEST
                             (Document defect, proposed
                              spec change, & rationale)
                                         │
                                         ▼
                               OWNER REVIEW & DECISION
                                         │
                        ┌────────────────┴────────────────┐
                        │                                 │
                     REJECT                            APPROVE
                        │                                 │
                        ▼                                 ▼
               Maintain current lock             REOPEN AFFECTED LOCK
             Mark defect as "Owner-Waived"      Update specification artifact
             Resume Gauntlet or exit             Re-engage lock & re-test
```

---

## 9. Resource Controls & Circuit Breakers

To prevent uncontrolled token consumption and infinite loops, the Gauntlet enforces three layers of resource governance:

```
┌──────────────────────────────────────────────────────────────────────────┐
│ 1. ITERATION CAP (max_iterations)                                        │
│    Default: 3 rounds (Configurable up to 5 for complex builds).          │
│    If cap is reached without full resolution -> Return GAUNTLET_CAP_REACHED│
│                                                                          │
│ 2. DIMINISHING RETURNS CIRCUIT BREAKER                                   │
│    If two consecutive rounds produce identical defect scores or trivial  │
│    micro-adjustments without closing the core gap -> Halt immediately.   │
│                                                                          │
│ 3. MANUAL OVERRIDE CIRCUIT BREAKER                                       │
│    Operator may pause or stop the Gauntlet at any turn via standard      │
│    task controls.                                                        │
└──────────────────────────────────────────────────────────────────────────┘
```

> [!IMPORTANT]
> **No Fake Passes:** When `GAUNTLET_CAP_REACHED` triggers, the system documents all unresolved defects and escalates to the Owner for visual sign-off. It NEVER promotes a capped run to `PASS`.

---

## 10. Anti-AI-Slop Audit Matrix

Every Gauntlet pass includes an explicit anti-AI-slop audit. Findings are structured in the following standardized format:

```markdown
### AI-Slop Audit Finding: [SLOP-ID]
- **Pattern Detected:** [e.g., Generic 3-Card Feature Loop / Unmotivated Purple Gradient / Centered Hero Pill]
- **Location:** [File path, section identifier, line range]
- **Severity:** [CRITICAL | MAJOR | MINOR]
- **Evidence:** [Exact markup/CSS demonstrating the anti-pattern]
- **Remediation:** [Concrete architectural or token replacement]
- **Lock Impact:** [NONE (Code fix) | LOCK_REOPEN_REQUIRED (Spec modification)]
```

---

## 11. Blind A/B Comparison Standard

Where feasible, visual comparisons between the build and Reference Bars are conducted **blind**:
- Identifying titles, brand names, and URLs are stripped from the evaluator's prompt context.
- Artifacts are labeled neutrally as `Candidate A` and `Candidate B`.
- The evaluator is asked: *"Which candidate demonstrates superior typographic craft, hierarchy, and spatial cadence, and why?"*

### Honesty Invariant:
If true blindness is not technically feasible (e.g., distinct branded copy or embedded logos cannot be obscured without destroying layout), the evaluation report must state:
```markdown
BLIND_COMPARISON = FALSE (Reason: Branded asset occlusion would distort spatial layout)
```
**Never claim `BLIND_COMPARISON = TRUE` unless it actually occurred.**

---

## 12. Verdict Model & State Integration

### 12.1 Explicit Verdicts
The Gauntlet returns one of six explicit verdicts—scores are supporting telemetry only:

- **`GAUNTLET_PASS`:** All active critics pass; build meets or exceeds reference bars across all evaluated dimensions.
- **`GAUNTLET_FAIL`:** One or more critics find major defects; builder must execute targeted repair on `BIGGEST_REMAINING_GAP`.
- **`GAUNTLET_LOCKED_CHANGE_REQUIRED`:** Remediation blocked by a locked decision; awaiting owner change review.
- **`GAUNTLET_CAP_REACHED`:** Maximum iterations reached; residual defects documented and escalated to Owner.
- **`GAUNTLET_BLOCKED`:** Environment failure, missing fetchable reference, or critical build crash.
- **`GAUNTLET_OWNER_WAIVED`:** Owner reviewed residual defects and authorized production bypass.

### 12.2 State Schema (`site-profile.json`)
The Gauntlet state is maintained strictly under the single-source-of-truth object `gauntlet{}`:

```json
{
  "gauntlet": {
    "status": "GAUNTLET_PASS",
    "iteration_count": 2,
    "max_iterations": 3,
    "verdict": "PASS",
    "largest_remaining_gap": null,
    "residual_defects": [],
    "reference_bars": [
      {
        "dimension": "Typography Bar",
        "name": "Stripe Press Monograph",
        "uri": "https://press.stripe.com",
        "why": "Gold standard for mathematical type scale and macro/micro contrast."
      }
    ],
    "exception": {
      "applied": false,
      "reason": null
    }
  }
}
```

---

## 13. Exceptions & Opt-Out Governance

A project may bypass the Website Gauntlet only under bounded, recorded conditions:
1. **Explicit Owner Opt-Out:** Owner explicitly directs bypass for rapid prototyping or non-public internal tooling.
2. **Offline / Sandboxed Environment:** Reference bars cannot be fetched and no local benchmark fixtures are available.
3. **Micro-Fix Scope:** Maintenance task touches $< 10$ lines of existing verified styling.

When an exception is engaged, it must be recorded in `site-profile.json` → `gauntlet.exception`:
```json
{
  "gauntlet": {
    "status": "GAUNTLET_EXCEPTION_APPLIED",
    "exception": {
      "applied": true,
      "reason": "Explicit owner opt-out for internal proof-of-concept prototype."
    }
  }
}
```
**Never bypass the Gauntlet silently.**
