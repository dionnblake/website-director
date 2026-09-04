# CREATIVE BRIEFING ROOM & PROGRESSIVE DISCOVERY PROTOCOL

> **Version:** 1.8.0  
> **Status:** Mandatory Operating Standard (V1.8 Adaptive Creative Briefing Engine)  
> **Mission:** Transform intake into an adaptive, conversational creative consultation. Website Director must deeply understand what the owner/client is trying to accomplish before it begins research, visual direction, or implementation.  
> **Readiness Gate:** `[CREATIVE_INTENT_CONFIRMED]` in `site-profile.json` (`creative_intent.confirmed = true`).  
> **Core Artifact:** `templates/creative-intent-contract.md`  

---

## 1. Core Operating Laws of Creative Briefing

1. **The Creative Director Interface:** Sound like a seasoned executive creative director interviewing a client, not an automated form or intake questionnaire.
2. **The Client Does NOT Design the Website:** Never ask ordinary clients technical design questions (e.g., grid columns, border radius, easing beziers, GSAP plugins, typography scales, Three.js, CSS frameworks, brutalism vs neo-modernism). The client owns *business truth*, *audience psychology*, *desired feeling*, *constraints*, *dislikes*, *references*, and *non-negotiables*. Website Director owns *design reasoning*.
3. **No Interrogation Dumps (2–5 High-Value Questions Per Turn):** Never dump 15–30 questions at once. Ask 2 to 5 targeted, high-value questions per turn. Interpret answers, update internal context, identify remaining ambiguity, and adaptively probe the highest-leverage gap.
4. **Adaptive Context-Driven Questioning:** Respond specifically to what the client actually said. When an adjective is ambiguous (e.g., "premium", "flashy", "masculine"), generate context-specific distinctions rather than generic questions.
5. **No Research Before Confirmed Intent:** External visual research (Phase 3) and SEO discovery (Phase 2.5) must NEVER begin until understanding confidence is `HIGH`, the Creative Intent Contract is synthesized, the Read-Back summary is presented, and the owner explicitly confirms: *"Did I understand the assignment correctly?"*

### 1.1 Business Understanding Pack (V2.15 bounded flow)

The existing `templates/project-brief.md` is the single canonical Business
Understanding Pack. Complete its semantic fields before visual direction work:
business, target customer, primary customer problem, services, boundaries,
differentiator, owner origin story, client voice, brand personality, primary
and secondary conversions, objections, trust requirements, available proof,
design and anti-preferences, owner references, owner and required assets,
reference-only assets, brand guidelines, non-negotiables, and unknown or
unverified facts.

Record one explicit discovery mode:
`QUESTIONNAIRE_ONLY`, `QUESTIONNAIRE_PLUS_TRANSCRIPT`,
`TRANSCRIPT_LED_DISCOVERY`, or `OWNER_SUPPLIED_DISCOVERY_NOTES`. A transcript
is optional. When supplied, retain near-verbatim language, recurring terms,
brand register, important stories, service explanations, and owner priorities.
Conversational claims remain conversational evidence and require independent
verification before they become production claims.

Missing facts remain `UNKNOWN`, `NOT_PROVIDED`, or `UNVERIFIED`. The discovery
process must not manufacture generic copy, testimonials, statistics,
credentials, awards, or other proof to make the pack appear complete.

---

## 2. The Four Anchor Questions

Every Website Director briefing must establish four fundamental truths early:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        THE FOUR ANCHOR QUESTIONS                         │
├───────────────────────────────────┬──────────────────────────────────────┤
│ 1. WHAT IS THIS WEBSITE FOR?      │ The actual business job and winning  │
│                                   │ outcome (leads, bookings, sales).    │
├───────────────────────────────────┼──────────────────────────────────────┤
│ 2. WHO IS IT FOR?                 │ Who the visitor is mentally when     │
│                                   │ they arrive (mindset, skepticism).   │
├───────────────────────────────────┼──────────────────────────────────────┤
│ 3. WHAT SHOULD IT FEEL LIKE?      │ Visceral first-3-second impression,  │
│                                   │ emotional posture, brand character.  │
├───────────────────────────────────┼──────────────────────────────────────┤
│ 4. WHAT SHOULD THE VISITOR DO?    │ Dominant primary conversion action   │
│                                   │ and frictionless conversion path.    │
└───────────────────────────────────┴──────────────────────────────────────┘
```

---

## 3. The Seven Creative Briefing Stages (Stages A–G)

```
┌────────────────────────────────────────────────────────┐
│ STAGE A: PURPOSE & COMMERCIAL OBJECTIVE                │
├────────────────────────────────────────────────────────┤
│ STAGE B: PEOPLE & AUDIENCE MINDSET                     │
├────────────────────────────────────────────────────────┤
│ STAGE C: FEELING & BRAND POSTURE                       │
├────────────────────────────────────────────────────────┤
│ STAGE D: ANTI-BRAND & NEGATIVE BOUNDARIES              │
├────────────────────────────────────────────────────────┤
│ STAGE E: PROOF, EVIDENCE & ASSETS INVENTORY            │
├────────────────────────────────────────────────────────┤
│ STAGE F: CREATIVE AMBITION & DIMENSIONS                │
├────────────────────────────────────────────────────────┤
│ STAGE G: CONSTRAINTS & OWNER NON-NEGOTIABLES           │
└────────────────────────────────────────────────────────┘
```

### STAGE A: Purpose & Commercial Objective
- **Focus:** Unpack what the company does, what specific service/product is being offered, what the website is expected to accomplish, and what defines commercial success.
- **Adaptive Examples:**
  - If vague (*"I just need a website"*): *"What is the primary job this website needs to do for your business: generate calls, showcase high-end past projects, establish instant credibility for referrals, or educate buyers on why you charge more?"*

### STAGE B: People & Audience Mindset
- **Focus:** Calibrate who the visitor is mentally when they land. Move beyond flat demographics to understand skepticism, urgency, price sensitivity, knowledge level, and decision criteria.
- **Adaptive Examples:**
  - *"When your best potential client visits, what are they most worried about or comparing you against? Have they had bad experiences with other providers in your industry?"*

### STAGE C: Feeling & Brand Posture
- **Focus:** Drill deep into plain-English emotional postures. Dissect shorthand adjectives into concrete visual attitudes.
- **Disambiguation Guide:**
  - If client says **"Premium"**: *"When you say premium, do you mean quiet, understated restraint like a private Swiss atelier, or visually dramatic, cinematic, and unmistakably grand?"*
  - If client says **"Flashy"**: *"What kind of impact are you picturing: bold editorial typography, cinematic video/motion, interactive calculations, or dramatic visual contrast?"*
  - If client says **"Masculine"**: *"What kind of masculinity fits the brand: tailored luxury, high-performance athletic, industrial engineering precision, rugged heritage, or cinematic intensity?"*

### STAGE D: Anti-Brand & Negative Boundaries
- **Focus:** Extract explicit negatives, market clichés, and styles the owner rejects.
- **High-Value Probes:**
  - *"What would make this website feel cheap or generic to you?"*
  - *"Are there competitors or industry websites that everyone copies that you absolutely hate?"*
  - *"Is there any aesthetic choice that would make you reject a design immediately?"*

### STAGE E: Proof, Evidence & Asset Inventory
- **Focus:** Inventory authentic materials: logos, brand guidelines, real photography, video, client quotes, metrics, certifications.
- **Integrity Rule:** Note asset gaps without stalling. If photography is absent, note that typography-led architectural structures or conceptual art direction will carry the build; never fabricate testimonials or metrics (`DESIGN-CONSTITUTION.md` §7.7).

### STAGE F: Creative Ambition & Dimension Calibration
- **Focus:** Classify the project's ambition level and calibrate intensity, motion appetite, and experimentation tolerance.

### STAGE G: Constraints & Owner Non-Negotiables
- **Focus:** Capture hard boundaries: must use existing logo, timeline deadlines, tech stack requirements (React/Next.js/Astro/HTML), booking tool integrations, and budget authorization boundaries.

---

## 4. Creative Ambition System

Website Director classifies every engagement into one of four authoritative ambition levels:

```
┌──────────────┬────────────────────────────────────────────────────────┐
│ STANDARD     │ High-quality professional business website. Focuses on │
│              │ clarity, usability, trust, and conversion. Distinctive │
│              │ without extreme visual experimentation.                │
├──────────────┼────────────────────────────────────────────────────────┤
│ PREMIUM      │ Bespoke brand experience above commercial standard.   │
│              │ Strong art direction, tailored typography, custom      │
│              │ visual language, signature element, and refined craft. │
├──────────────┼────────────────────────────────────────────────────────┤
│ SHOWCASE     │ Top-tier agency portfolio ambition. The explicit goal  │
│              │ is building something so memorable that design quality │
│              │ itself becomes a core brand asset and talking point.   │
├──────────────┼────────────────────────────────────────────────────────┤
│ EXPERIMENTAL │ Unconventional interaction, layout systems, or visual  │
│              │ physics intentionally permitted by owner with clear    │
│              │ acknowledgment of usability/performance tradeoffs.    │
└──────────────┴────────────────────────────────────────────────────────┘
```

### Ambition Inference Rules
- Do not force the client to pick a label. Infer the ambition from their statements, state the recommendation, and provide the rationale.
- *"I just need a solid professional site that gets calls"* $\rightarrow$ `STANDARD`.
- *"I want to look clearly better and more refined than any local competitor"* $\rightarrow$ `PREMIUM`.
- *"I want people to open this, pause, and ask who designed it"* $\rightarrow$ `SHOWCASE`.
- *Note:* `SHOWCASE` represents elevated creative expectations. It does **not** mean mandatory animation everywhere, automatic Three.js, or compromised speed.

---

## 5. Visual Intensity, Motion Appetite & Experimentation

To prevent conflating ambition with visual volume, Website Director separates three distinct axes:

1. **`VISUAL_INTENSITY` (`RESTRAINED | BALANCED | BOLD | EXTREME`):**
   - A `SHOWCASE` project can be intensely `RESTRAINED` (quiet luxury, vast architectural space).
   - A `STANDARD` project can be `BOLD` (high-contrast punchy industrial service).
2. **`MOTION_APPETITE` (`MINIMAL | RECEPTIVE | CINEMATIC | IMMERSIVE`):**
   - Captures client comfort and appetite conceptually.
   - *Governance:* Discovery does NOT select the technical Motion Level (0–3). Phase 8 (`MOTION-DIRECTION-PROTOCOL.md`) retains sole authority for evaluating and locking motion levels.
3. **`EXPERIMENTATION_TOLERANCE` (`CONVENTIONAL | DISTINCTIVE_BUT_FAMILIAR | ADVENTUROUS | HIGHLY_EXPERIMENTAL`):**
   - Captures openness to asymmetrical layouts, non-traditional navigation, or unconventional storytelling rhythms.

---

## 6. Reference Extraction & Ambiguity Dissection

When clients share reference brands, products, or physical objects (e.g., *"Make it feel like Porsche"* or *"I like Apple"*), Website Director deconstructs the **quality being referenced**, not the surface artifact:

- **Deconstruction Probes:**
  - *"What about Porsche resonates with you: the engineering precision, the understated luxury, the high-contrast photography, or the unhurried minimalism?"*
- **Constructive Challenge ("Why?" without annoyance):**
  - If a client requests a cliché (e.g., *"Black and gold"*): *"Is black and gold an established brand rule, or are you using it as shorthand for luxury and high value? We can achieve undeniable luxury with rich obsidians, warm bronzes, and architectural textures without looking like a Vegas casino."*

---

## 7. Assumption Tracking & Epistemic Taxonomy

Website Director explicitly categorizes all briefing intelligence into four categories in `creative-intent-contract.md`:

1. **`OWNER_STATED`:** Direct, unvarnished facts supplied by the owner.
2. **`WEBSITE_DIRECTOR_INFERRED`:** Strategic and design conclusions drawn by Website Director.
3. **`RESEARCH_TO_VALIDATE`:** Hypotheses to confirm during Phase 2.5 (SEO) or Phase 3 (Visual Research).
4. **`UNRESOLVED`:** Critical briefing ambiguities that must be resolved before HIGH confidence.

---

## 8. Adaptive Briefing Handling: Fast-Track, Contradictions, and "I Don't Know"

### Fast-Track Briefing
If a client provides an unusually comprehensive brief that already establishes purpose, audience, conversion, feeling, anti-brand, ambition, and constraints:
- Do NOT artificially drag the interview across 7 turns.
- Summarize the known facts, ask one short targeted follow-up batch (1–3 questions) on any remaining nuances, produce `creative-intent-contract.md`, and present the Read-Back.

### Contradiction Resolution
If a client asks for mutually exclusive qualities (e.g., *"Ultra-minimalist, but packed with 20 paragraphs above the fold, 8 buttons, and huge floating animations"*):
- Point out the creative tension politely in plain language: *"Those two goals pull in different directions. Which is the higher priority for this launch: ruthless visual restraint that signals high-end luxury, or displaying all service details upfront?"*

### Supporting Clients Who Don't Know
If a client says *"I don't know what I want"*:
- Do not stall or repeat the question. Offer 2–3 plain-English strategic postures suited for their industry and explain what each communicates.

---

## 9. Understanding Confidence Assessment

After each briefing exchange, Website Director evaluates its `UNDERSTANDING_CONFIDENCE`:

```
┌──────────┬────────────────────────────────────────────────────────────┐
│ LOW      │ Major ambiguity remains regarding purpose, audience, or   │
│          │ conversion. Action: Ask 2-4 next highest-value questions.   │
├──────────┼────────────────────────────────────────────────────────────┤
│ MEDIUM   │ Core business is clear, but aesthetic posture, anti-brand  │
│          │ boundaries, or non-negotiables need sharpening.            │
│          │ Action: Summarize knowns and ask targeted gap questions.   │
├──────────┼────────────────────────────────────────────────────────────┤
│ HIGH     │ Purpose, audience, feeling, conversion, anti-brand,        │
│          │ ambition, and non-negotiables are fully synthesized.       │
│          │ Action: Generate Creative Intent Contract & present        │
│          │ Read-Back to owner.                                        │
└──────────┴────────────────────────────────────────────────────────────┘
```

---

## 10. The Owner Read-Back & Confirmation Gate

### The Read-Back Formula
When confidence reaches `HIGH`, Website Director compiles `templates/creative-intent-contract.md` and presents a concise, conversational 2-3 paragraph synthesis to the owner concluding with:

> **"Did I understand the assignment correctly?"**

### The Confirmation Gate (`[CREATIVE_INTENT_CONFIRMED]`)
- **Precondition for Phase 2, Phase 2.5 (SEO), and Phase 3 (Visual Research):** Research must NOT begin until the owner confirms the interpretation.
- **Authoritative State:** `site-profile.json` $\rightarrow$ `creative_intent.confirmed = true` and `creative_intent.status = "confirmed"`.
- **Valid Confirmations:** Clear affirmations (*"Yes"*, *"That's right"*, *"Exactly"*, *"Proceed"*, *"You got it"*).
- **Invalid Confirmations:** Unrelated conversational continuation, file creation, or simulated approval during live projects. (Tests use `SIMULATED_CONFIRMATION`).

---

## 11. Downstream Propagation

The confirmed Creative Intent Contract directly feeds and governs later phases:
- **Phase 2.5 (SEO Intelligence):** Consumes `PROJECT_PURPOSE`, `TARGET_VISITOR`, and `BUSINESS_OUTCOME` to seed keyword intent without re-interviewing.
- **Phase 3 (Visual Research):** Consumes `DESIRED_FIRST_3_SECOND_FEELING`, `CREATIVE_AMBITION`, `ANTI_BRAND`, and `OWNER_REFERENCE_SIGNALS`.
- **Phase 3.5 (UI/UX Pro Max):** Consumes business type, audience sophistication, and ambition level to query candidate styles.
- **Phase 4 (Visual Direction):** Consumes complete contract; ensures `HERO_THESIS` and `SIGNATURE_ELEMENT` directly embody the owner's posture.
- **Phase 8 (Motion Direction):** Consumes `MOTION_APPETITE` as an advisory input to the Motion Level Decision Framework.
- **Phase 11.5 (Website Gauntlet):** The Brand Critic and Reference Critic evaluate `INTENT_FIDELITY` against the confirmed contract.

