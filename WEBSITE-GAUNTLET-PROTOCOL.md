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

### 4.2 Brand Critic (Enhanced with Intent Fidelity)
- **Focus:** Brand distinctiveness, emotional posture, visual identity, anti-brand compliance, and **Intent Fidelity** (`creative-intent-contract.md`).
- **Key Questions & Intent Fidelity Checks:**
  - Does this finished design solve the declared business purpose and primary conversion goal?
  - Does it feel the way the client requested in their desired first-3-second emotional posture?
  - Does it strictly respect all anti-brand boundaries, banned clichés, and competitor negative constraints?
  - Does it satisfy the project's selected `CREATIVE_AMBITION` (`STANDARD`, `PREMIUM`, `SHOWCASE`, `EXPERIMENTAL`) and visual intensity?
  - Does it satisfy all declared `OWNER_NON_NEGOTIABLES`?
  - Does it pass the **Swap Test** (would it fail if placed on a competitor)?
- **Defects:** Generic SaaS styling for an artisanal luxury brand, sterile corporate look for an energetic startup, violation of owner non-negotiables, failure to satisfy selected creative ambition, identity drift.

### 4.3 Conversion Critic
- **Focus:** Primary/secondary conversion clarity, CTA dominance, visitor friction, and objection handling.
- **Key Questions:**
  - Is the primary conversion goal obvious within 5 seconds of scanning?
  - Are CTAs placed at natural cognitive decision points (`Understand` $\rightarrow$ `Believe` $\rightarrow$ `Evaluate` $\rightarrow$ `Convert`)?
  - Are primary objections addressed before the main conversion commitment?
  - *(V2.6)* Does the measurement architecture actually support the intended business outcome, or does it measure activity that no business decision depends on?
  - *(V2.6)* Does any critical CTA lack a measurement definition in `measurement-plan.md`?
  - *(V2.6)* Is the declared funnel genuinely observable end-to-end, or are stages asserted that nothing on the built site can evidence?
  - *(V2.7)* Does conversion pressure override a required disclosure, a consent obligation, or user autonomy anywhere on the page?
  - *(V2.7)* Does any form collect fields with no documented purpose in the approved data inventory?
- **Defects:** Competing CTAs, buried action buttons, unclear value exchange, premature asks before establishing value, critical CTAs with no measurement definition, funnel stages that cannot be observed, conversion pressure overriding disclosure or consent, unjustified form fields.

### 4.4 Trust Critic
- **Focus:** Evidence placement, claims verification, proof density, credentials, and risk reduction.
- **Key Questions:**
  - Is every major marketing claim supported by verifiable evidence or concrete data?
  - Are customer testimonials specific, attributed, and credible (vs generic praise)?
  - Are institutional credentials, security assurances, or guarantees visible at friction points?
  - *(V2.7)* Are security or compliance claims implied without evidence — padlock iconography, "bank-level security", "GDPR compliant", or an unevidenced certification badge or seal?
  - *(V2.7)* Is affiliate or sponsorship compensation disclosed where the recommendation actually appears, rather than only in a remote footer page?
  - *(V2.7)* Is any sponsored or affiliate unit styled to be indistinguishable from independent editorial content?
  - *(V2.7)* Does any marketing claim, statistic, certification, or testimonial in the build lack recorded evidence and provenance?
- **Defects:** Unattributed quotes, floating checkmarks without context, fake statistics, missing reassurance near CTAs, unevidenced security or compliance claims, missing or buried affiliate/sponsorship disclosure, disguised advertising, claims with no recorded provenance.

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
- **Key Questions (V2.7 privacy-surface extension):**
  - *Is the consent dialog keyboard operable, focus-managed, and free of keyboard traps?*
  - *Is rejecting optional processing as reachable as accepting it — same interaction count, same discoverability?*
  - *Are privacy, cookie, and affiliate disclosures legible at body-copy contrast, or suppressed into unreadable micro-type?*
  - *Does any bot challenge or consent wall leave a keyboard or screen-reader user with no path forward?*
- **Defects (V2.7):** Inaccessible consent dialogs, keyboard traps in privacy UI, unreadable disclosures, impossible or unreachable cookie rejection, inaccessible bot challenges.

### 4.8 Reference Critic (Benchmarking Bar Fidelity)
- **Focus:** Direct side-by-side comparison against named `REFERENCE_BAR` entries across assigned dimensions.

### 4.9 Portfolio Art Director Critic (SHOWCASE Tier V1.9 Extension)
- **Focus:** World-class digital studio portfolio standards, visual distinction, authored composition, and Awwwards-inspired craft rigor. Activated especially when `CREATIVE_AMBITION = SHOWCASE` or `EXPERIMENTAL`.
- **The 11 Portfolio Director Scrutiny Questions:**
  1. *Would a respected international digital design studio put this work in its public portfolio?*
  2. *Is there an above-the-fold or signature screenshot immediately worth sharing publicly?*
  3. *Does this design have a sharp, recognizable creative point of view rather than safe consensus?*
  4. *Can the brand and subject world be recognized if the company logo and name are removed?*
  5. *Is the composition authored and tailored rather than assembled from popular UI kits or theme templates?*
  6. *Does the visual tension, typographic craft, and spatial discipline hold consistently below the hero?*
  7. *Is there at least one memorable tactile, structural, or interactive moment?*
  8. *Does the visual weight and art direction feel appropriate to the client's actual commercial positioning?*
  9. *What specific detail still looks machine-generated, generic, or AI-templated?*
  10. *What is the single weakest section on the page, and what specific change would elevate it?*
  11. *What is preventing this build from feeling exceptional?*
- **Defects:** Predictable layout rhythm, hero fatigue in lower sections, lack of identifiable creative point of view, generic gallery trend contamination, absence of a memorable signature moment.

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

### 4.10 Visual Asset & Art Direction Critic (V2.0 Asset Director Lens)
- **Focus:** Evaluation of the website's complete visual asset ecosystem under `ASSET-DIRECTOR-PROTOCOL.md`.
- **Key Questions:**
  - *Are visual assets specific to this company and subject world, or could they belong to any competitor?*
  - *Does the Hero Asset possess undeniable screenshot value and cognitive anchor power?*
  - *Is the visual family coherent across the entire page (shared color grade LUT, lighting language, and material physics)?*
  - *Does the lower half of the page maintain the same high asset craft as the hero (`MEDIA_QUALITY_BELOW_HERO`), or does asset quality degrade into generic icons and empty boxes?*
  - *Are generated images 100% free of AI artifacts (`AI_ARTIFACT_CHECK = PASS`), and are factual claims authenticated?*
  - *Are responsive crops (`picture` elements) deliberate on mobile viewports rather than relying solely on naive `object-fit: cover` center-cropping?*
- **Defects:** Generic stock photos, unauthenticated AI customer/facility imagery, inconsistent visual styles, missing mobile crops, low-resolution below-fold media.

### 4.11 Immersive Web & Spatial 3D Critic (V2.1 Immersive Specialist Lens)
- **Focus:** Evaluation of Three.js / WebGL runtime execution under `IMMERSIVE-WEB-PROTOCOL.md`.
- **Key Questions:**
  - *Does the 3D scene solve a genuine spatial communication problem, or does it feel like an unmotivated Three.js template demo?*
  - *Is the camera choreography disciplined (bounded angles, smooth easing) or does it wander uncontrollably?*
  - *Are primary conversion CTAs, headlines, and specifications 100% accessible in semantic DOM outside the WebGL canvas?*
  - *Does the zero-CLS 2D fallback work cleanly when WebGL fails or is disabled?*
  - *Is mobile performance smooth (DPR bounded `<= 1.5`, touch interactions safe, no layout trapping)?*
  - *Does `prefers-reduced-motion` cleanly freeze continuous spinning/flying without informational loss?*
- **Defects:** Generic floating 3D demo tropes, trapped canvas text, broken WebGL fallbacks, jank below 30 FPS, missing mobile adaptations.

### 4.12 Rive Interactive Motion Critic (V2.2 Rive Specialist Lens)
- **Focus:** Evaluation of Rive state machines, interactive vector motion, and runtime fallbacks under `RIVE-INTERACTIVE-MOTION-PROTOCOL.md`.
- **Key Questions:**
  - *Does the Rive vector component convey multi-state logic better than simpler CSS or GSAP animations?*
  - *Is the vector motion free of cartoon mascot clichés, unmotivated looping blobs, or fake liquid novelty effects?*
  - *Are all critical interactive states accessible on touch and keyboard (zero hover-only essential behavior)?*
  - *Are all data values and state descriptions mirrored in accessible semantic HTML outside the Rive canvas?*
  - *Does the zero-CLS fallback display seamlessly if WASM or runtime initialization fails?*
  - *Are Rive resources disposed cleanly without memory leaks on unmount?*
- **Defects:** Gratuitous mascot slop, hover-only state traps, missing semantic DOM mirroring, unhandled runtime fallback, memory leaks.

### 4.13 Page Experience & Navigation Continuity Critic (V2.3 Page Experience Specialist Lens)
- **Focus:** Evaluation of route transitions, history parity, scroll restoration, and navigation continuity under `PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md`.
- **Key Questions:**
  - *Does the transition preserve spatial orientation and context between routes, or is it gratuitous animation slop?*
  - *Are real URLs, native browser Back/Forward, deep linking, and hard refresh 100% operational?*
  - *Does the transition avoid blocking user interaction or trapping users behind full-screen loading curtains?*
  - *Does scroll restoration work predictably across route changes and history navigation?*
  - *Are reduced-motion preferences respected with instant or minimal cross-fades?*
  - *Are WebGL and Rive subsystem resources cleanly disposed during route transitions?*
- **Defects:** Fullscreen loading curtains, broken browser history, blank screen on refresh, disorienting navigation wipes, memory leaks.

### 4.14 Conversion Measurement & Analytics Architecture Critic (V2.6 Specialist Lens)
- **Focus:** Evaluation of business outcome alignment, measurement architecture integrity, conversion flow, privacy-first telemetry, and experimentation integrity under `CONVERSION-ANALYTICS-PROTOCOL.md`.
- **Key Questions:**
  - *Is the primary outcome clear and friction-free without turning the page into an aggressive, low-trust hard sell?*
  - *Does the page address visitor objections before demanding commitment?*
  - *Are conversion CTAs descriptive, honest, and appropriately placed?*
  - *Is the build 100% free of deceptive dark patterns (fake urgency, false social proof, manipulative dismissals)?*
  - *Does analytics strictly adhere to data minimization without capturing PII or form field inputs?*
  - *Does the website remain fully functional if analytics scripts are blocked or disabled?*
  - *Are experiment hypotheses paired with firm guardrail metrics (lead quality, trust, brand perception, accessibility)?*
  - *(V2.6) Does measurement support the intended business outcome — can someone name the decision each event informs?*
  - *(V2.6) Are any events meaningless vanity instrumentation that no KPI consumes?*
  - *(V2.6) Is every primary and meaningful secondary CTA traceable to an event, or is a critical CTA unmeasured?*
  - *(V2.6) Is the funnel observable, or does the plan claim stages the build cannot evidence?*
  - *(V2.6) Does a success conversion event fire where the server actually rejected the submission?*
  - *(V2.6) Is an affiliate outbound click being treated as a conversion or commission?*
  - *(V2.6) Are planning, implementation verification, and production verification reported as distinct states — or is a plan being presented as observed success?*
  - *(V2.6) Are baselines and benchmarks fabricated rather than recorded as `UNKNOWN`?*
- **Defects:** Dark patterns, PII in analytics payloads, broken forms when tracking is blocked, premature winner declarations on synthetic data, generic vanity metric tracking, unmeasured critical CTAs, unobservable funnel claims, false conversion signals on rejected submissions, affiliate click treated as commission, fabricated baselines, planning state reported as production success.
  - *(V2.7) Does the build load any third-party script that is absent from the approved third-party inventory?*
  - *(V2.7) Does consent-dependent tracking or storage fire before consent where consent is recorded `REQUIRED`?*
  - *(V2.7) Does any analytics payload or UTM parameter carry PII — verified against actual network payloads, not source?*
  - *(V2.7) Does the consent or privacy UI use a dark pattern — suppressed rejection, misleading hierarchy, deceptive wording, prechecked optional consent, hidden opt-out?*
  - *(V2.7) Is a compliance claim or unevidenced security badge rendered anywhere in the build?*
- **Additional Defects (V2.7):** Unexplained third-party scripts, consent-dependent tracking firing before consent, PII in observed payloads, privacy dark patterns, rendered compliance certification claims.
- **Critic Boundary:** This critic evaluates. It never edits the measurement plan, the security/privacy review, locked copy, or instrumentation. `BUILDER != CRITIC`. Findings flow through the existing `gauntlet{}` object — no parallel measurement or security state is created.

---

### 4.15 Security & Privacy Coverage (V2.7 — No New Critic)

Security, privacy, consent, and disclosure quality is evaluated by **enriching the existing critics above**, not by adding a critic:

| Critic | Owns |
| :--- | :--- |
| **Trust Critic (4.4)** | Unevidenced security/compliance claims, missing or buried affiliate and sponsorship disclosure, disguised advertising, claims without provenance |
| **Conversion Critic (4.3)** | Conversion pressure overriding disclosure or consent; form fields with no documented purpose |
| **Accessibility Critic (4.7)** | Inaccessible consent dialogs, keyboard traps, unreadable disclosures, unreachable rejection |
| **Conversion Measurement & Analytics Critic (4.14)** | Unexplained third-party scripts, consent-dependent tracking before consent, PII in payloads, privacy dark patterns, rendered compliance claims |

`BUILDER != CRITIC` is maintained. **No second Gauntlet state machine is created** — findings flow through the existing `gauntlet{}` object, and no critic writes to `security_privacy{}`.

---

### 4.16 Deterministic Browser QA Entry Precondition (V2.8 — No New Critic)

Website Director V2.8 adds **Phase 10.5 Automated Browser & Regression QA** (`BROWSER-REGRESSION-QA-PROTOCOL.md`), a machine-executed verification phase that runs *before* the Gauntlet.

```
PHASE 10.5  DETERMINISTIC BROWSER QA  →  [BROWSER_QA_PASS]  →  PHASE 11.5  QUALITATIVE GAUNTLET
```

- **Entry precondition:** Gauntlet STEP 1 (Capture Artifact State) does not begin until `site-profile.json` → `browser_qa.complete` is `true` (or a recorded `browser_qa.blocked_reason` / `browser_qa.exception`). The Gauntlet does not spend adversarial-critic cycles on a build with broken navigation, JavaScript exceptions, missing assets, failed forms, or obvious responsive overflow — those are deterministic and are Phase 10.5's job.
- **No new critic, no new state machine.** Browser QA is an upstream phase, not a Gauntlet lens. No critic reads or writes `browser_qa{}`; findings from Phase 10.5 flow through `browser_qa{}`, findings from Phase 11.5 flow through `gauntlet{}`. The distinction is permanent: **Browser QA answers "did it behave as specified?"; the Gauntlet answers "is it good enough?"**
- The Craft, Motion, and Accessibility critics may *reference* the Phase 10.5 evidence manifest (screenshots, reduced-motion captures) as inputs, but they never re-run browser assertions or re-derive their own pass/fail on responsive overflow, console errors, broken assets, or form integrity — those verdicts are owned by Phase 10.5.

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
