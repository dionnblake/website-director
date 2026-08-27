# DISCOVERY PROTOCOL: PROGRESSIVE BUSINESS-TO-DESIGN EXTRACTION

> **Version:** 1.1.0
> **Status:** Mandatory Operating Standard
> **Purpose:** Extract complete commercial truth, brand posture, and evidence from non-designers without cognitive overload.

---

## 1. Core Operating Principles of Discovery

1. **Non-Designer Interface:** Never ask clients or stakeholders to specify font sizes, CSS grid parameters, hex codes, or layout terminology. Ask about business realities, commercial positioning, customer psychology, and visceral feelings.
2. **Progressive Revelation:** Never dump 30 questions at once. Conduct discovery in **four sequential stages**, digesting each response before initiating the next.
3. **Inference Over Interrogation:** The user owns **Business Truth** (what they do, who they sell to, why they win) and **Brand Boundaries** (what they hate, what they aspire to). **Website Director owns Design Reasoning.** Infer design systems from commercial context rather than asking the user to design the website.
4. **Validation Checkpoints:** After each stage, synthesize findings into structured markdown artifacts before progressing.

---

## 2. The Four Stages of Progressive Discovery

```
┌────────────────────────────────────────────────────────┐
│ STAGE 1: BUSINESS ESSENCE & COMMERCIAL GOALS           │
├────────────────────────────────────────────────────────┤
│ STAGE 2: BRAND IDENTITY & EMOTIONAL POSTURE            │
├────────────────────────────────────────────────────────┤
│ STAGE 3: EVIDENCE INVENTORY & PROOF ASSETS             │
├────────────────────────────────────────────────────────┤
│ STAGE 4: VISUAL DIRECTION & ARCHETYPE SELECTION        │
└────────────────────────────────────────────────────────┘
```

---

### STAGE 1: Business Essence & Commercial Goals

**Objective:** Understand what the business actually does, who pays them, and what constitutes a winning conversion.

#### Standard Questions:
1. **Core Proposition:** What does your company do in one crystal-clear sentence, and what specific problem does it solve for customers?
2. **Offerings / Products:** What are the exact products, packages, or services you sell?
3. **Target Audience:** Who is the exact decision-maker visiting this site (e.g., enterprise CTOs, boutique homeowners, solo founders, procurement managers)?
4. **Primary Conversion Action:** When a visitor reaches the site, what is the single most valuable action they must take (e.g., Book a demo, Buy now, Request audit, Call directly, Schedule a consultation)?
5. **The Unfair Advantage (Why Choose You):** Why would someone choose you over established market competitors? What is your actual superpower?
6. **Scope / Page Footprint:** Is this a focused single-page landing experience or a multi-page site (e.g., Home, Solutions, Pricing, About, Case Studies, Contact)?

*Output Artifact Generated:* `templates/project-brief.md` (Stage 1 section).

---

### STAGE 2: Brand Identity & Emotional Posture

**Objective:** Map existing brand assets and calibrate the psychological impression the website must leave.

#### Standard Questions:
1. **Existing Brand Assets:** Do you have an existing logo (SVG/PNG), defined brand colors, specific fonts, or an official brand style guide? (If yes, please provide or describe them; if no, we will generate a bespoke system).
2. **Desired Emotional Impression:** When a qualified prospect lands on the page, what should they subconsciously feel in the first 3 seconds?
   - *Options in Plain English:*
     - Ultra-premium & exclusive (high barrier to entry, luxurious)
     - Highly technical & rigorous (data-driven, engineered, infallible)
     - Authoritative & institutional (safe, trusted by giants, established)
     - Cutting-edge & disruptive (visionary, fast-moving, innovative)
     - Warm, human & boutique (artisan, bespoke, high-touch)
3. **The Anti-Brand (What to Avoid):** What websites or aesthetic styles in your industry do you **hate** or definitely NOT want to look like? (e.g., *"Don't look like a generic silicon valley AI startup"*, *"Don't look like a dated corporate insurance company"*).

*Output Artifact Generated:* `templates/positioning.md`.

**V1.1 note:** Stage 1 and Stage 2 answers (business essence, audience, anti-brand boundaries) are the direct inputs to `templates/research-brief.md` in the Visual Research phase that follows Discovery. Do not re-ask the client for information already captured here when scoping research.

---

### STAGE 3: Evidence Inventory & Proof Assets

**Objective:** Collect concrete, verifiable proof elements that establish instant credibility.

#### Standard Questions:
1. **Testimonials & Reviews:** Do you have verified client quotes, executive testimonials, or Trustpilot/Google review ratings?
2. **Case Studies & Metric Proof:** Can you share 1 to 3 specific quantifiable outcomes achieved for clients (e.g., *"Saved $1.4M in cloud spend"*, *"340% increase in qualified pipeline"* )?
3. **Credentials & Partnerships:** Are there certifications, enterprise client logos, security standards (SOC2, ISO), awards, or press features we can showcase?
4. **Visual Assets:** Do you have authentic photography, real product interface screenshots, video demos, or founder portraits? (If not, we will design art-directed conceptual typography and architectural illustrations).
5. **Existing Copy / Content:** Do you have draft copy, whitepapers, or existing brochures, or should Website Director construct high-converting original copy?

*Output Artifact Generated:* `templates/content-plan.md` (Evidence inventory section).

---

### STAGE 4: Visual Direction & Archetype Selection

**Objective:** Align on the visual execution style using plain-English, non-technical descriptions.

#### Operating Rules:
- **Do NOT ask:** *"Do you want a 12-column neo-brutalist grid with 18px Helvetica Neue and glassmorphic elevation?"*
- **DO ask:** Present 3 to 4 tailored archetypal directions curated for their industry and brand goals.

#### Standard Archetype Translation Framework:
Present curated options like this:

> **Option A: "The High-End Editorial"**  
> *Looks like:* A luxury magazine or premium art monograph.  
> *Character:* Elegant serif headlines, generous negative space, warm neutral tones, sophisticated restraint. Perfect for high-touch advisory, architecture, and luxury goods.
>
> **Option B: "The Precision Technical"**  
> *Looks like:* A high-performance engineering workstation or scientific instrument.  
> *Character:* Monospaced data tags, crisp hairline grid borders, high contrast dark theme, dense information density, metric callouts. Perfect for developer tools, fintech, cybersecurity, and deep tech.
>
> **Option C: "The Modernist Corporate"**  
> *Looks like:* An international design institution or global venture firm.  
> *Character:* Razor-sharp Swiss typography, bold asymmetric hierarchy, deep navy/slate accents, structured evidence matrices. Perfect for enterprise B2B SaaS, private equity, and institutional consultancies.

#### Choice of Path:
- **ORIGINAL_MODE:** The user selects an archetype (or a blend, e.g., 70% Precision Technical + 30% Modernist Corporate).
- **REFERENCE_MODE:** The user provides 1 to 3 reference URLs or images they admire, triggering the `REFERENCE-PROTOCOL.md` workflow.

*Output Artifact Generated:* `templates/design-direction.md`.

---

## 3. Discovery Quality Checklist

Before declaring Discovery complete and locking Phase 1:
- [ ] Business offering is defined without jargon.
- [ ] Primary conversion CTA is single-minded and measurable.
- [ ] Target buyer persona is explicit.
- [ ] Brand boundaries (what to avoid) are documented.
- [ ] Verifiable proof points are cataloged.
- [ ] Visual archetype / blend is confirmed.
- [ ] `site-profile.json` has been initialized with preliminary metadata.

**Note:** Archetype/blend confirmation here is preliminary and plain-English (this stage). It is finalized in Phase 4 (`REFERENCE-PROTOCOL.md` / `DESIGN-ARCHETYPES.md`) after the Phase 3 Visual Research pass (`VISUAL-RESEARCH-PROTOCOL.md`) has run — Discovery completing does not itself satisfy `RESEARCH_COMPLETE`.
