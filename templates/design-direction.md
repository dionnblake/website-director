# DESIGN DIRECTION SPECIFICATION: [PROJECT NAME]

> **Date Created:** YYYY-MM-DD  
> **Status:** DRAFT | LOCKED (`DESIGN_DIRECTION_LOCKED: true`)  
> **Stage:** Phase 4 (Visual Direction Formulation & Distinctiveness Synthesis)  
> **Governance:** `DESIGN-CONSTITUTION.md` §7, `DESIGN-INTELLIGENCE-PROTOCOL.md`, Anthropic Distinctiveness Discipline  

---

## 1. Selected Prototype Provenance & Blending Formula
- **Selected Prototype Direction:** `[projects/[project]/prototypes/direction-XX/]` (`visual_prototypes.owner_selected_direction`)
- **Owner Visual Selection Confirmed:** `YES` (`visual_prototypes.owner_selection_confirmed: true`)
- **Selected Direction Expanded to Full Homepage:** `YES | NO` (`artifact_kind = FULL_HOMEPAGE` or `SELECTED_DIRECTION_PLUS_COMPLETE_HOMEPAGE`)
- **Homepage Visual Approval Evidence:** `visual_prototypes.homepage_visual_approved = true | false` (bounded evidence field; not a new gate or owner lock)
- **Homepage Approval Record:** `[owner review ID / evidence path / NOT_APPROVED]`
- **Primary Archetype (60%):** [e.g., Modernist / Technical / Editorial / Luxury]
- **Secondary Modifier (30%):** [e.g., Industrial / Architectural / Boutique]
- **Kinetic / Accent Flavor (10%):** [e.g., Cinematic / Playful / Experimental]
- **Design Intelligence Source Prior:** [UI/UX Pro Max Matched Product Profile & Style Candidates]
- **Awwwards Reference Bars Benchmarked:** [Specific Awwwards dimensional bars used, e.g., AWWWARDS_TYPOGRAPHY_BAR, AWWWARDS_HERO_BAR]

---

## 2. Subject-World Grounding & Narrative
- **What Exists in This Subject's World?:** [Specific physical materials, tools, instruments, vernacular, environments, and artifacts that inform this design (e.g., architectural tracing paper, automotive calipers, obsidian terminal glass)]
- **Art Direction Narrative:** [2-3 paragraphs describing the visual posture, layout rhythm, material quality, and sensory feeling the visitor experiences]
- **Target Aesthetic Character:**
  - **Atmosphere:** [e.g., High-contrast obsidian workstation / Warm sunlit architectural studio / Stately minimalist monograph]
  - **Pacing:** [e.g., Unhurried and spacious / High-frequency data-dense / Cinematic widescreen drama]
  - **Structure:** [e.g., Asymmetric 12-column Swiss grid with hairline structural rules]

---

## 3. Hero Thesis & Signature Composition
- **Hero Thesis (`HERO_THESIS`):** [What is the single most characteristic thing this visitor should encounter first? Explain how the opening viewport presents the central thesis rather than generic headline+buttons+stats tropes]
- **Signature Element (`SIGNATURE_ELEMENT`):** [The memorable physical, structural, or interactive device the visitor will remember 24 hours later]
- **Boldness Budget Allocation (`BOLDNESS_BUDGET`):** [Where boldness is concentrated (the signature), and how surrounding sections remain quiet, disciplined, and supporting]
- **Aesthetic Risk Justification (`AESTHETIC_RISK`):** [Deliberate, explainable, and accessible aesthetic risk taken to prevent generic homogeneity]

---

## 4. Direction Rationale vs. Seven Pillars of Justification
1. **Hierarchy Rationale:** [Why this visual approach directs attention to high-value propositions]
2. **Comprehension Rationale:** [How this design style clarifies complex offerings]
3. **Navigation Rationale:** [How wayfinding is streamlined]
4. **Conversion Rationale:** [Why this aesthetic drives the primary conversion CTA]
5. **Credibility Rationale:** [How visual craft proves institutional quality]
6. **Brand Expression Rationale:** [How this embodies the company's authentic position]
7. **Emotional Impact Rationale:** [The exact psychological resonance created]

---

## 5. Two-Pass Distinctiveness Pre-Check & Trend Filter (Pass 2 Critique)

| Evaluation Question | Assessment & Evidence | Status |
| :--- | :--- | :---: |
| **5-Competitor Interchangeability Test** | *Could this design plan fit 5 competitors with only logo and copy swapped?* | `PASS (Bespoke to subject)` |
| **Structural Meaning Test** | *Does every structural device (dividers, eyebrows, numbers) encode true hierarchy/sequence?* | `PASS (Zero decorative numbering)` |
| **Default Awareness Test** | *Has the design avoided falling lazily into known AI clusters without brief justification?* | `PASS (Intentional choice)` |
| **Trend Contamination Test** | *Are all visual and interaction techniques justified by subject truth rather than award gallery fashion?* | `PASS (Zero unmotivated tropes)` |
| **Portfolio Art Director Audit** | *Does the composition possess authored studio-grade craft with a memorable signature?* | `PASS (Portfolio caliber)` |
| **Typography Personality Test** | *Does typography embody the subject's voice rather than generic neutral Inter?* | `PASS (Pairing fits subject)` |
| **Factual Integrity Test** | *Are all proof points, metrics, and case artifacts drawn from real project evidence?* | `PASS (Zero fictional proof)` |

---

## 6. Design Lock Declaration
- [ ] Visual prototype slice generated and rendered in browser (`projects/[project]/prototypes/`).
- [ ] Owner has visually reviewed rendered desktop & mobile prototypes and explicitly selected this direction (`visual_prototypes.owner_selection_confirmed = true`).
- [ ] The selected direction has been expanded into a complete rendered homepage before the Design System is derived.
- [ ] Owner has explicitly approved the rendered desktop and mobile full homepage (`visual_prototypes.homepage_visual_approved = true`); approval is not inferred from silence, prose, builder output, or critic output.
- [ ] Archetype blend aligns with market positioning and audience expectations.
- [ ] Two-pass distinctiveness and trend contamination critiques completed and signed off.
- [ ] Ready to lock `DESIGN_DIRECTION_LOCKED` (`locks.design_direction_locked = true`) in `site-profile.json`.

