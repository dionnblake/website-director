# DESIGN CONSTITUTION: THE ANTI-AI-SLOP DIRECTIVE

> **Version:** 1.2.0  
> **Status:** Mandatory Enforceable Standard  
> **Applicability:** All Website Director specifications, design systems, and implementation contracts.  
> **Quality Engine:** Enforced via `IMPECCABLE-ENGINE-PROTOCOL.md`, Anthropic Distinctiveness Discipline, and Phase 11 / Phase 11.5 verification.

---

## 1. The Governing Law

```
EVERY DESIGN CHOICE MUST HAVE A REASON.
```

In the Website Director ecosystem, no element exists simply to populate whitespace, simulate modern software aesthetics, or follow default framework templates. Every single color value, typographic choice, spatial interval, container border, animation curve, and layout structure must directly serve at least one of the **Seven Pillars of Justification**:

1. **Hierarchy:** Directing the human eye in exact order of cognitive priority.
2. **Comprehension:** Making complex value propositions intuitively clear in under 5 seconds.
3. **Navigation:** Guiding the visitor seamlessly toward their intended destination.
4. **Conversion:** Eliminating friction between interest and commercial action.
5. **Credibility:** Establishing incontrovertible visual and contextual proof of quality.
6. **Brand Expression:** Embodying the distinct emotional and aesthetic soul of the business.
7. **Emotional Impact:** Creating visceral resonance (e.g., trust, authority, delight, exclusivity, urgency).

**If an element, wrapper, ornament, or animation does not serve at least one pillar, it must be eliminated.**

---

## 2. Prohibited AI-Slop Design Patterns (The Default Bans)

AI coding models defaulting to generic web templates universally generate predictable, uncurated aesthetic tropes ("AI slop"). The following patterns are **banned by default** across all Website Director builds unless explicitly justified by the chosen archetype:

| Anti-Pattern | Description of Slop | Required Website Director Alternative |
| :--- | :--- | :--- |
| **Pill Card Spam** | Endless `border-radius: 1.5rem` cards with faint gray borders nested inside each other. | Intentional geometry: Clean architectural lines, razor-sharp edges, asymmetrical rule lines, or purpose-fitted containers. |
| **The 3-Card Feature Loop** | Repeating 3 equal-width column cards with an icon in a colored circle, a bold title, and two lines of filler text. | Morphological variety: Staggered horizontal rows, asymmetric editorial splits, comparison data matrices, or narrative step flows. |
| **Purple/Blue SaaS Gradients** | Generic `#6366F1` to `#A855F7` linear gradients across buttons, text fills, and background blurs. | Curated brand palettes derived from industry positioning, physical materials, bespoke contrast tokens, or monochromatic mastery. |
| **The Floating Decorator UI** | Fictional dashboard snippets, fake graphs with glowing SVG curves, floating badges with checkmarks hovering in empty margins. | Concrete business evidence: Real interface screenshots, authentic data tables, client artifact proofs, or verified case study metrics. |
| **Centered Hero Paralysis** | Centered small pill tag (`"Announcing v2.0 ->"`), centered huge generic sans-serif headline, centered vague subhead, two centered pill buttons. | Asymmetrical art-directed composition: Off-center typography, cinematic horizontal spreads, split editorial layouts, or dynamic focal anchors. |
| **Glassmorphism Without Function** | Indiscriminate `backdrop-filter: blur(12px)` and transparent white backgrounds on cards that have nothing underneath them to blur. | Layered depth with purpose: Optical background separation, deliberate elevation planes, tactile material contrast, or solid high-contrast planes. |
| **Generic Inter Monoculture** | Defaulting everything to `font-family: 'Inter', sans-serif` at `font-weight: 400/600` for every brand regardless of personality. | Expressive typographic pairing: Contrasting editorial serifs, technical grotesque mono-accents, distinctive modern display faces, and curated scales. |
| **Random Micro-Animations** | Elements sliding up and fading in from every direction upon scrolling, with arbitrary delays and bounce curves. | Purposeful physics & choreographies: Cohesive page-load choreography, subtle interaction feedback, micro-transitions, or scroll-coupled narrative pacing. |
| **Fake Metric Badges** | Floating cards saying `"99.9% Satisfaction"` or `"Trusted by 10,000+ teams"` with generic placeholder stars or stock logos. | Specific, audit-grade proof: Verifiable client quotes, case-study performance numbers, industry credentials, and audited stats. |
| **Pill-Button Abuse** | Defaulting every button to `border-radius: 9999px` regardless of brand personality. | Purpose-matched radius: Razor 0px for industrial/luxury, crisp 4-6px for corporate/modernist, rounded only when brand is organic/playful. |
| **Excessive Diffuse Shadows & Halos** | Giant blurry `box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25)` or 0-offset neon dark glow halos. | Structured depth: Multi-layered subtle ambient elevation, hairline border separation, or crisp directional offset shadows. |
| **Repetitive Section Morphology** | Stacking identical 3-column card grids or centered text blocks down the entire page. | Asymmetric cadence: Alternating between split heroes, horizontal tickers, data matrices, and editorial pull-quotes. |
| **Layout Property Transitions** | Animating layout triggers (`transition: all`, `transition: width`, `transition: height`, `transition: top`, `transition: margin`). | Compositor-only performance: Animate exclusively `transform` and `opacity` to guarantee $\ge 60\text{ FPS}$. |
| **Toy Bounce Physics** | Exaggerated bouncy spring curves (`cubic-bezier(0.68, -0.55, 0.265, 1.55)`). | Restrained physical curves: Smooth exponential ease-out or crisp snappiness (`cubic-bezier(0.16, 1, 0.3, 1)`). |
| **Gray-on-Color Washes** | Neutral gray secondary text (`#6b7280`) rendered on colored backgrounds. | Harmonious surface tinting: Tint secondary copy from the background hue or foreground color value. |
| **Decorative Numbering Spasm** | Slapping `01 / 02 / 03` numbered badges on unordered features solely to look "designed". | Information-encoding structure: Numbering only when ordinal sequence or chronological process matters. |

---

## 3. Visual Repetition Control (Section Morphology)

A website is a sequential cognitive journey. Consecutive sections that share identical visual morphology cause cognitive fatigue and trigger user skimming.

### The Morphology Rules:
1. **No Consecutive Identical Layouts:** A 3-column grid section must never be followed by another 3-column grid section.
2. **Rhythm Variation:** Alternate between dense analytical sections, spacious editorial statements, asymmetric split-screens, and high-impact visual anchors.
3. **Contrast Modulation:** Transition deliberately between light/dark tonal zones, background textures, and structural margins to demarcate conceptual shifts.
4. **Focal Point Shifts:** Move the user's primary eye anchor across sections (e.g., Left-aligned headline $\rightarrow$ Full-bleed image canvas $\rightarrow$ Right-aligned case metric $\rightarrow$ Centered decision matrix).

---

## 4. The Premium Perception Test

Every Website Director design specification must pass the **Seven Vectors of Perceived Craft**:

### Vector 1: Customness (Art Direction)
- *Test Question:* Does this interface look like a master art director crafted this specific layout for this specific company, or does it look like a theme template populated with copy?
- *Requirement:* Bespoke typographic scale, tailored grid alignments, and unique compositional accents.

### Vector 2: Specificity (Non-Replaceability)
- *Test Question:* If you swapped the logo and company name with a competitor, would the website still work?
- *Requirement:* If yes, the design is too generic. The visual language must directly express the exact domain, material quality, and posture of this specific business.

### Vector 3: Memorability (The Signature Anchor)
- *Test Question:* What is the one visual or structural signature a user will remember 24 hours after visiting?
- *Requirement:* Every site must possess at least one distinct signature (e.g., an architectural grid line system, an unusual editorial typographic contrast, an interactive calculation engine, or a tactile material texture).

### Vector 4: Craft (Micro-Refinement)
- *Test Question:* Are line-heights, letter-spacing (tracking), border radiuses, optical alignments, and hover transitions executed with typographic precision?
- *Requirement:* Zero typographic collisions, optical baseline alignment, consistent spatial cadence (`4px`/`8px` strict baseline grid), and unified easing physics.

### Vector 5: Consistency (Sustained Rigor)
- *Test Question:* Is the footer, FAQ, and pricing table treated with the exact same visual refinement and bespoke detail as the hero section?
- *Requirement:* No "hero fatigue." Lower sections must exhibit identical density rules, token discipline, and graphic integrity.

### Vector 6: Positioning (Value Alignment)
- *Test Question:* Does the perceived visual weight, craftsmanship, and tone match or exceed the actual pricing tier and market authority of the company?
- *Requirement:* High-ticket or enterprise services must project unshakeable institutional solidity and prestige.

### Vector 7: AI Detection Invariance
- *Test Question:* Does the site trigger subconscious "AI template" alarms in experienced web users?
- *Requirement:* Zero unmotivated gradients, zero floating pill cards, zero generic stock iconography, zero empty marketing platitudes.

---

## 5. The Top 3 Impact Upgrades (The "More Expensive" Filter)

When reviewing any design draft or proposed specification, the reviewer must identify and apply the **Three Highest-Impact Upgrades to Increase Perceived Value**:

1. **Tighten Spatial Cadence & Negative Space:** Replace bloated card padding with precise, intentional negative space and rigorous architectural gutters.
2. **Elevate Typographic Drama & Contrast:** Enhance the scale differential between display titles and body copy; introduce precise tracking and optical kerning tokens.
3. **Deepen Material & Proof Realism:** Replace generic icons or illustrations with concrete data artifacts, high-resolution bespoke product details, and audited case evidence.

---

## 6. The Craft Floor & Surface Polish (Impeccable Intelligence)

To guarantee that the build feels engineered rather than assembled from templates, every implementation must satisfy the **Craft Floor Standards**:

1. **Browser Surface Theming:** Default un-styled browser primitives reveal template builds. Theme text selection (`::selection`), input carets, custom scrollbars, and high-contrast `:focus-visible` rings directly from design system tokens.
2. **Tabular Numerals on Data:** All pricing tables, metrics, stats, and countdowns must declare `font-variant-numeric: tabular-nums` to prevent layout jitter during data updates.
3. **Reading Measure:** Body copy measure must be constrained between `65ch` and `75ch` (`max-width: 65-75ch`) to ensure optimal reading ergonomics.
4. **Spatial Asymmetry on Headings:** Content hierarchy requires greater whitespace *above* a section heading than *below* it, maintaining clear visual grouping with its child content.

---

## 7. Subject-Grounded Distinctiveness & Intentionality Discipline (Anthropic Intelligence)

To prevent AI coding agents from generating bland, interchangeable interfaces, every design direction must be governed by the **Intentional Distinctiveness Standards**:

### 7.1 Ground Design in the Subject's World
The visual identity of a project must originate from the actual subject, product, company, audience, materials, instruments, artifacts, and vernacular of the business:
- Ask during synthesis: **"WHAT EXISTS IN THIS SUBJECT'S WORLD THAT CAN INFORM THE DESIGN?"**
- Derive visual metaphors, spatial structures, and texture from real physical context (e.g., architectural blueprints, automotive engineering calipers, financial ledgers, raw stone textures, terminal logs).
- **Prohibition:** Do NOT invent fictional brand history, fake tools, or synthetic artifacts. Ground decisions exclusively in real project evidence.

### 7.2 The Hero is a Thesis
The opening viewport must communicate the page's strongest visual and strategic argument (`HERO_THESIS`):
- Open with the single most characteristic encounter in the subject's world: a definitive image, an unusual editorial composition, an interactive demonstration, or a bold thesis statement.
- **Trope Rejection:** Reject the automatic template default: *Headline + paragraph + two buttons + three statistics + background gradient glow*. Use this structure only if explicitly justified by conversion architecture.

### 7.3 Structure Must Encode Information (`STRUCTURE_MUST_ENCODE_INFORMATION`)
Every structural device—dividers, eyebrows, kicker tags, badges, tabs, and numbered markers—must represent genuine hierarchical or categorical meaning:
- **Numbering Rule:** Markers like `01 / 02 / 03` are permitted **only** when the content represents an ordered sequence, a chronological timeline, or a step-by-step workflow. Numbering unrelated feature cards solely for visual decoration is strictly prohibited.
- **Eyebrows & Dividers:** Use eyebrows only to establish semantic taxonomy; use dividers only to isolate disparate cognitive domains.

### 7.4 One Memorable Signature & Boldness Budget (`BOLDNESS_BUDGET`)
- **Signature Element (`SIGNATURE_ELEMENT`):** Every major design direction must identify exactly one distinct visual, structural, or interactive signature that a visitor remembers 24 hours later.
- **Boldness Budget:** Spend boldness in **one** place. Keep supporting layout, typography, and containers disciplined, quiet, and refined. Making every section fight for attention with experimental typography, extreme layout, heavy motion, and custom cursors creates visual chaos.
- **Contextual Restraint:** Restraint is not universal minimalism; maximalist briefs may permit richer textures if art-directed, but must still maintain clear cognitive hierarchy.

### 7.5 Default Awareness (The Three AI Design Default Clusters)
AI design models cluster around three predictable aesthetic defaults. Website Director enforces **Default Awareness** (distinguishing *intentional choice* from *lazy default*):
1. **Cluster 1 (Warm Cream / Terracotta):** Cream background (`~#F4F1EA`), high-contrast editorial serif, terracotta/clay accent.
2. **Cluster 2 (Dark Mode Neon Acid):** Near-black background (`#0A0A0A`), bright acid-green, neon cyan, or vermilion glow accents with pill badges.
3. **Cluster 3 (Broadsheet Dense Monospace):** Dense columns, hairline 1px borders everywhere, 0px radius, typewriter/monospace labels.
*Rule:* These looks are legitimate when the brief genuinely calls for them, but must never be selected by default when an axis is unspecified.

### 7.6 Interface Writing as Design Material
Interface copy is a functional design material, not decorative filler:
- **User Perspective:** Name features by what people recognize and control, never by internal engineering architecture (e.g., "Manage Notifications", not "Webhook Dispatcher Configuration").
- **Action-Descriptive Labels:** Buttons and CTAs must state the exact outcome ("Save changes", "Schedule Deep Dive"), avoiding vague labels ("Submit", "Click Here").
- **Directional Errors & Empty States:** Errors must explain what happened and how to resolve it in the brand voice without vague apologies. Empty states must direct the user toward constructive action.
- **Zero Fluff:** Eliminate marketing filler; every phrase must carry informative value.


### 7.7 Absolute Factual Integrity
Distinctiveness must never become fictionalization. Generating fake client testimonials, synthetic metrics, fictional case studies, invented awards, or exaggerated user counts is **strictly prohibited**. Real project evidence is mandatory.

---

## 8. The World-Class Visual Craft Standard (Award Tier)

To ensure websites built under Website Director are worthy of public pride and international design accolades (e.g. Awwwards Site of the Day, FWA, elite design studio caliber), builds must satisfy the **Five Pillars of World-Class Visual Craft**:

### 8.1 Ban on Generic "AI Dark-Mode Dashboard" Tropes
- **The Tropes:** Blanket dark gray cards (`#111116`), indiscriminate electric-cyan borders (`rgba(0,102,255,0.3)`), repetitive green blinking status dots, and cookie-cutter 3-card grids.
- **The Standard:** Rich, atmospheric materiality: subtle organic noise grain textures, bespoke ambient lighting, warm obsidian or deep tinted slate backgrounds, tactile physical material finishes (e.g., brushed titanium, matte obsidian, champagne gold), and asymmetric editorial compositions.

### 8.2 Fluid Momentum & Scroll Physicality
- Standard browser scrolling feels static. Premium digital experiences must feel weighted and fluid via **Lenis smooth inertial scrolling** synchronized with GSAP ScrollTrigger timelines.

### 8.3 Kinetic Masked Typography
- Primary headlines must never pop in with simple opacity transitions. Use nested clip-path or overflow-hidden line and word masks to reveal typography with fluid mathematical ease (`power4.out`).

### 8.4 Pinned Scrollytelling & Stage Transitions
- Key narrative sequences (e.g., protocols, breakdowns, deep dives) should utilize full-screen pinned scroll tracks where content progresses horizontally or morphs seamlessly as the user scrolls.

### 8.5 Micro-Physics & Tactile Interaction
- Interactive triggers, CTAs, and cards should feature subtle magnetic cursor pull, spring-physics return, and optical cursor followers with contrast inversion (`mix-blend-mode: difference`).
