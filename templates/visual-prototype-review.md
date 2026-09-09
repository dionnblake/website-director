# VISUAL PROTOTYPE PROTOCOL: THE PRE-LOCK VISUAL VERIFICATION GATE

> **Version:** 1.9.0  
> **Status:** Mandatory Operating Standard (Website Director V1.9.0 Subsystem)  
> **Governance:** Website Director Orchestration Rail ([SKILL.md](file:///c:/Users/ALPHA/Desktop/VIBE%20CODING%20PROJECTS/WEBSITE-DIRECTOR/SKILL.md) §2, Phase 4 & Phase 4.5)  
> **Mission:** Ensure the project owner never has to select a major visual direction from prose alone by presenting bounded, high-fidelity, browser-rendered visual prototypes before Design Direction Lock.

---

## 1. Core Operating Law: No Prose-Only Direction Selection

``
┌──────────────────────────────────────────────────────────────────────────┐
│                   THE VISUAL PROTOTYPE GOVERNANCE INVARIANT              │
│                                                                          │
│                 NO PROSE-ONLY DIRECTION SELECTION                        │
│                                                                          │
│  The owner must NEVER be asked to select or approve a major visual       │
│  direction based solely on textual descriptions or abstract prose when   │
│  visual prototyping is feasible. The owner selects from what they SEE.   │
└──────────────────────────────────────────────────────────────────────────┘
``

Website Director may write design direction concepts and rationale, but every viable candidate direction presented to the owner must be backed by a bounded, browser-rendered visual prototype.

---

## 2. Visual Prototype Definition & Boundaries

A **Visual Prototype** is:
> A bounded, high-fidelity browser-rendered slice of a proposed design direction used for creative evaluation and art direction comparison before full-site implementation.

### What a Visual Prototype Is and Is NOT:

| It IS | It IS NOT |
| :--- | :--- |
| A high-fidelity, browser-rendered slice of the proposed art direction | A wireframe, moodboard, or gray-box approximation |
| Polished enough to judge typography, palette, hero, and visual craft | A complete website or sitemap build |
| Responsive proof demonstrating desktop (1440px) and mobile (390px) behavior | A production candidate |
| A decision aid prior to Design Direction Lock | An automatic Design Direction Lock |
| An isolated experimental artifact (PROTOTYPE_STATUS = EXPERIMENTAL_VISUAL_DIRECTION) | Production deployment authorization |

---

## 3. Required Prototype Content & Anatomy

Each prototype direction must represent a complete, polished slice containing:

1. **Global Nav / Brand Header:** Real typography, brand marks/wordmarks, authentic navigation structure.
2. **Complete Hero:** The full art-directed above-the-fold experience executing the proposed HERO_THESIS.
3. **One Representative Content Section:** Demonstrating typographic rhythm, structural rules, content density, and card/list/narrative styling.
4. **Signature Element (SIGNATURE_ELEMENT):** The memorable physical/structural/interactive device that embodies the creative point of view.
5. **Representative CTA:** Action-descriptive primary conversion point demonstrating button geometry, contrast, and hover physics.
6. **Responsive Mobile Evidence:** Proving the layout, touch ergonomics, and typography reflow at 390px viewport width.

### Content & Evidence Integrity Rules:
- Use realistic, authentic project content whenever available.
- Explicitly ban Lorem Ipsum filler.
- **Absolute Factual Integrity:** Never fabricate testimonials, metrics, client logos, certifications, awards, or product capabilities (DESIGN-CONSTITUTION.md §7.7).
- If placeholder facts are unavoidable, mark them visibly as placeholders (e.g., [Metric to be verified]).

---

## 4. Direction Count Policy by Creative Ambition

The number of visual prototypes required is governed by CREATIVE_AMBITION (calibrated during Phase 1 Creative Briefing) to balance design rigor against development cost:

``
┌─────────────────┬───────────────────┬─────────────────────────────────────────────────┐
│ CREATIVE        │ PROTOTYPE COUNT   │ DIVERGENCE & RESEARCH REQUIREMENT               │
│ AMBITION        │ REQUIREMENT       │                                                 │
├─────────────────┼───────────────────┼─────────────────────────────────────────────────┤
│ STANDARD        │ 1 strong prototype│ High-fidelity prototype proving the single      │
│                 │ (or 2 lightweight)│ recommended direction without over-engineering. │
├─────────────────┼───────────────────┼─────────────────────────────────────────────────┤
│ PREMIUM         │ 2–3 prototypes    │ High-fidelity prototypes exploring distinct     │
│                 │                   │ aesthetic postures and spatial approaches.      │
├─────────────────┼───────────────────┼─────────────────────────────────────────────────┤
│ SHOWCASE        │ 3 prototypes      │ 3 high-fidelity, GENUINELY DISTINCT creative    │
│                 │ (MANDATORY)       │ directions evaluated against Awwwards bars.     │
├─────────────────┼───────────────────┼─────────────────────────────────────────────────┤
│ EXPERIMENTAL    │ 2–3 prototypes    │ 2–3 avant-garde prototypes with explicit risk   │
│                 │                   │ documentation and boundary exploration.         │
└─────────────────┴───────────────────┴─────────────────────────────────────────────────┘
``

> [!IMPORTANT]
> For CREATIVE_AMBITION = SHOWCASE, Website Director must NEVER silently collapse to 1 or 2 directions unless the owner gives an explicit, documented single-direction directive.

---

## 5. The True Divergence Mandate (Direction Divergence Test)

For multi-direction presentations (especially SHOWCASE), candidate directions must represent genuinely different creative points of view. They must not be "Dark Version A, Dark Version B, Dark Version C" or superficial color/font swaps.

### Divergence Vectors:
1. **HERO_COMPOSITION:** Different viewport geometry, focal weight, and entrance narrative.
2. **TYPOGRAPHIC_PERSONALITY:** Distinctive display/body pairings and hierarchy ratios.
3. **IMAGE_LANGUAGE:** Divergent art direction, cropping, color grading, and treatment.
4. **COLOR_BEHAVIOR:** Different tonal relationships, contrast strategies, and material hues.
5. **GRID / LAYOUT PHILOSOPHY:** Varied structural tension, column cadence, and rule lines.
6. **EDITORIAL_DENSITY:** Contrasting information pacing (spacious vs high-density).
7. **SIGNATURE_ELEMENT:** Completely different memorable anchors.
8. **MOTION_CHARACTER:** Divergent kinetic personalities (e.g., razor-sharp mechanical snap vs unhurried editorial ease).
9. **INTERACTION_PHILOSOPHY:** Distinct tactile feedback and interactive mechanics.
10. **SPATIAL RHYTHM & METAPHOR:** Grounded in different authentic facets of the subject's world.

``
┌──────────────────────────────────────────────────────────────────────────┐
│                     DIRECTION DIVERGENCE TEST RULE                       │
│                                                                          │
│  If Candidate Directions could be transformed into one another merely    │
│  by swapping CSS hex colors and font-family strings:                     │
│                                                                          │
│                     DIRECTION_DIVERGENCE = FAIL                          │
│                                                                          │
│  The directions must be reconceptualized before owner presentation.      │
└──────────────────────────────────────────────────────────────────────────┘
``

---

## 6. Distinctiveness, Trend Contamination & Anti-Copying Checks

Before presenting prototypes to the owner, each prototype must pass three mandatory art direction tests:

### 6.1 The 5-Competitor Interchangeability Test
- **Question:** *If the client's logo and name were removed, could this prototype belong to five direct competitors?*
- **Verdict:** If YES → DISTINCTIVENESS_CHECK = FAIL. The prototype must be revised with deeper subject-grounded truth.

### 6.2 The Awwwards Trend Contamination Test
- **Question:** *Does this prototype blindly adopt popular gallery tropes without project-specific justification?*
  - Giant neutral grotesk + tiny mono labels on every element
  - Gratuitous WebGL fluid blobs or floating 3D shapes without brand meaning
  - Forced horizontal scrolling or intrusive custom cursor circles
  - Gratuitous preloader screens on lightweight static content
- **Verdict:** If unmotivated → TREND_CONTAMINATION_CHECK = FAIL. Reject fashionable tropes that do not serve commercial truth or subject grounding.

### 6.3 Anti-Copying Rule
- Prototypes must never be "Client Y built in the skin of Awwwards Site X."
- External references provide *transferable principles* (pacing, grid tension, material depth), which Website Director synthesizes into an original, client-grounded creation.

---

## 7. Motion & Technology Boundaries in Prototypes

### Motion Proof Policy:
Prototypes must demonstrate **Motion Character** without requiring the full production motion codebase.
- Implement: Hero reveal choreography, one key scroll interaction, primary button hover/focus micro-physics, or signature transition.
- Explicitly record in prototype metadata:
  `yaml
  MOTION_CHARACTER: "Mechanical chronometric snap with 0.16s ease-out"
  SIGNATURE_MOTION_CONCEPT: "Gimbal dial stabilization on scroll"
  PROTOTYPE_MOTION_IMPLEMENTED: "Hero clip-path mask + dial rotation on hover"
  `

### Asset & Technology Boundaries:
- **Asset Boundary (Pre-V2.0):** Use authentic client assets, licensed research imagery, or clean temporary placeholders. If assets limit the design expression, record PROTOTYPE_ASSET_LIMITATION = TRUE—never let weak imagery disguise a strong art direction.
- **Specialist Technology Boundary:** Prototypes may use existing GSAP capabilities. Do not build new Three.js, WebGL, or Rive specialist engines during prototyping. Record advisory notes in FUTURE_SPECIALIST_RECOMMENDATION (NONE | GSAP | CINEMATIC_SITES | IMMERSIVE_WEB_FUTURE | RIVE_FUTURE).

---

## 8. Directory & File Isolation Standard

Visual prototypes must be isolated from production code in a dedicated directory:

`	ext
projects/[project-id]/
└── prototypes/
    ├── direction-01/
    │   ├── index.html
    │   ├── style.css
    │   └── main.js
    ├── direction-02/
    │   ├── index.html
    │   ├── style.css
    │   └── main.js
    └── direction-03/
        ├── index.html
        ├── style.css
        └── main.js
`

Each prototype must carry metadata declaring:
`	ext
PROTOTYPE_STATUS = EXPERIMENTAL_VISUAL_DIRECTION
`
Prototypes must NEVER be placed in production release directories or treated as production candidates.

---

## 9. The Owner Presentation, Comparison & Selection Gate

When prototypes meet the quality floor, Website Director compiles the **Visual Prototype Comparison Package** (	emplates/visual-prototype-review.md) and presents it to the owner.

### Prototype Comparison Package Content:
For each direction:
- DIRECTION_NAME
- CORE_IDEA
- CREATIVE_INTENT_FIT
- HERO_THESIS & SUBJECT_WORLD
- SIGNATURE_ELEMENT
- TYPOGRAPHY & COLOR_BEHAVIOR
- LAYOUT_PHILOSOPHY
- MOTION_CHARACTER
- AWWWARDS_REFERENCE_BARS
- DISTINCTIVENESS_RESULT & TREND_CONTAMINATION_RESULT
- DESKTOP_PROTOTYPE link & MOBILE_PROTOTYPE link
- STRENGTHS & RISKS
- CROSS_DIRECTION_DIFFERENCES

``
┌──────────────────────────────────────────────────────────────────────────┐
│                 THE VISUAL SELECTION HARD STOP INVARIANT                 │
│                                                                          │
│  Upon delivering the Visual Prototype Review:                            │
│                                                                          │
│                                  STOP.                                   │
│                                                                          │
│  System Status: VISUAL_PROTOTYPES_OWNER_REVIEW_READY                     │
│                                                                          │
│  Website Director MUST NOT:                                              │
│  1. Pick a favorite for the owner                                        │
│  2. Automatically engage locks.design_direction_locked = true            │
│  3. Advance to Phase 5 (Information Architecture)                        │
│  4. Advance to Phase 7 (Design System)                                   │
│  5. Begin production build code                                          │
└──────────────────────────────────────────────────────────────────────────┘
``

### Owner Actions at the Gate:
1. **Select Direction:** Owner chooses DIRECTION_1, DIRECTION_2, or DIRECTION_3.
2. **Request Revisions:** Owner requests specific aesthetic or compositional adjustments on a direction.
3. **Request Hybridization:** Owner requests combining specific elements (e.g., "Direction 1 typography with Direction 3 hero layout"). Website Director produces a reconciled direction prototype for re-review.

### 9.1 Selected Direction → Full Homepage Review

Selection of a bounded direction is not approval of a full website. After the
owner selects or hybridizes a direction, expand the selected direction into a
complete browser-rendered homepage before deriving the Design System or
starting the full production build.

- **Required review surfaces:** `DESKTOP_FULL_HOMEPAGE` and
  `MOBILE_FULL_HOMEPAGE`, with applicable interactive and reduced-motion
  states.
- **Required content:** navigation, hero, value proposition, offers, proof and
  trust, differentiation, process, media language, authentic testimonial
  treatment where applicable, objections, CTA progression, FAQ, final CTA,
  footer, and responsive mobile behavior.
- **Required visual evidence:** real typography, spacing, grid, color,
  imagery, geometry, motion, rhythm, density, and conversion hierarchy. No
  Lorem Ipsum, fake proof, or generic filler below an elite hero.
- **Bounded approval record:** record
  `visual_prototypes.homepage_visual_approved = true` only after an explicit
  owner `APPROVE` action tied to the rendered review. This is an evidence
  field under the existing Visual Prototype authority, not a new gate, phase,
  or owner lock.
- Internal critics may recommend revision, rejection, or improvement. They
  cannot set the owner approval field.

---

## 10. Design Direction Lock Transition Protocol

Once the owner explicitly selects or confirms a visual direction:

1. Record isual_prototypes.owner_selected_direction = "direction-XX".
2. Record isual_prototypes.owner_selection_confirmed = true.
3. Synthesize the final 	emplates/design-direction.md from the selected prototype.
4. Expand the selected direction into the complete rendered homepage and
   present its desktop/mobile review package.
5. Record the explicit owner homepage approval under the existing
   `visual_prototypes.homepage_visual_approved` evidence field.
6. Present the formal Design Direction Lock confirmation package.
7. Obtain explicit owner confirmation for the lock.
8. Only then set site-profile.json → locks.design_direction_locked = true.
