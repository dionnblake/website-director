# RESEARCH SOURCES: VISUAL INTELLIGENCE ACQUISITION CHANNELS

> **Version:** 1.1.0
> **Status:** Mandatory Operating Standard (V1.1 Extension)
> **Purpose:** Define what each research channel is for, what it may never be used for, and what provenance every finding must carry.

---

## 1. The Four Channels

```
┌────────────────────────────────────────────────────────────────┐
│ CHANNEL 1: INDUSTRY LANDSCAPE   — what does this market expect? │
├────────────────────────────────────────────────────────────────┤
│ CHANNEL 2: LANDBOOK             — what should we study?         │
├────────────────────────────────────────────────────────────────┤
│ CHANNEL 3: CROSS-INDUSTRY       — who expresses this better?    │
├────────────────────────────────────────────────────────────────┤
│ CHANNEL 4: JCODESMORE RECON     — how exactly does it work?     │
└────────────────────────────────────────────────────────────────┘
```

No channel is optional by default. A channel may be skipped only under the bounded exception defined in `VISUAL-RESEARCH-PROTOCOL.md` §5, and the skip must be recorded in `site-profile.json` → `research.exception`, never applied silently.

---

## 2. Channel 1: Industry Landscape

**Purpose:** Establish what a visitor to this industry already expects, so Website Director can decide deliberately what to keep (comprehension aid) and what to break (visual sameness).

**Target volume:** 10–15 real businesses operating in the client's actual category.

**Answers, not artifacts:** The goal is never "here are 12 links." The goal is answers to:
- What does this industry usually look like?
- What visual patterns have become generic?
- What does a visitor expect, and which of those expectations aid comprehension vs. exist only by convention?
- Which credibility cues actually matter here?
- Where is the visual whitespace — the differentiation this industry hasn't claimed?

**Output:** `templates/competitor-landscape.md`.

---

## 3. Channel 2: Landbook

**What it is:** A curated gallery of current, high-quality landing pages and website sections, browsable by industry, style, and component type (hero, navigation, pricing, testimonial, footer, animation, etc.).

**Role in the pipeline:** Landbook answers `WHAT SHOULD WE STUDY?` — it is a discovery catalog, not a source of finished direction. It is used to widen the candidate pool of references beyond the client's direct competitors, across hero types, navigation patterns, typography treatments, animation styles, and section-level composition.

**Hard rule:** A Landbook entry is a candidate, never a template. Every candidate pulled from Landbook must carry a stated reason — *why this is relevant to this client* — before it advances past the shortlist. A reference with no stated relevance is discarded, no matter how polished it looks.

**Output:** Feeds `templates/inspiration-board.md`.

---

## 4. Channel 3: Cross-Industry Discovery

**Purpose:** Prevent Website Director from being trapped inside the visual conventions of the client's own industry when an adjacent or aspirational sector expresses the desired brand quality better.

**Rule:** A cross-industry reference is only valid if it has an explicit, stated strategic relationship to the client's desired brand posture (e.g., a law firm sourcing restraint and precision from architecture and editorial publishing, not because those sites are impressive in isolation). Visually impressive references with no relevance to the client's posture are discarded.

**Output:** Feeds `templates/inspiration-board.md` and `templates/research-synthesis.md` (Cross-Industry Lessons section).

---

## 5. Channel 4: JCodesMore Reconnaissance Methodology

**Source repository:** `https://github.com/JCodesMore/ai-website-cloner-template`

**What is borrowed:** Only the reconnaissance methodology — its Stage 1 pipeline of screenshot capture, computed-style extraction, design-token identification, and interaction sweep (scroll, hover, click, responsive breakpoints). This is the most forensic tool available for understanding *why* a specific reference works at the implementation level, and it is reserved for the small number of references that survive progressive filtering (see §6).

**What is never borrowed:** Its default behavior — component-spec generation for parallel-agent rebuilding, asset downloading for reuse, and full-site reconstruction. Website Director invokes this methodology only in the bounded `RESEARCH_ONLY_MODE` defined in `REFERENCE-RECON-PROTOCOL.md`. The cloner's own build/assembly stages (2–5 of its pipeline) are never triggered.

**Output:** Feeds `templates/reference-deconstruction.md`.

---

## 6. Progressive Filtering (Cost & Quality Discipline)

Deep reconnaissance is expensive in time, context, and — when live browsing tools are used — compute. It is reserved for references that have already proven their relevance.

```
INDUSTRY LANDSCAPE + LANDBOOK + CROSS-INDUSTRY RESEARCH
                    │
                    ▼
          10–15 CANDIDATES (competitor-landscape.md + inspiration-board.md)
                    │
                    ▼
             5 STRONG REFERENCES (shortlisted, reason stated for each)
                    │
                    ▼
          2–3 DEEP RECON TARGETS (reference-deconstruction.md via REFERENCE-RECON-PROTOCOL.md)
                    │
                    ▼
              RESEARCH SYNTHESIS (research-synthesis.md)
```

Do not run deep reconnaissance on every candidate. Reserve it for references that contain a genuinely transferable design or behavioral idea — the ones where a shallow look already tells you there's something specific worth extracting.

---

## 7. Provenance — Mandatory for Every Finding

Every reference recorded in `competitor-landscape.md`, `inspiration-board.md`, or `reference-deconstruction.md` must carry:

| Field | Requirement |
| :--- | :--- |
| **Source URL** | The exact page studied. |
| **Source Type** | `industry_competitor` \| `landbook` \| `cross_industry` \| `jcodesmore_deep_recon` |
| **Access / Research Date** | The date the reference was studied. |
| **Reason Selected** | Why this reference is relevant to this client — never "it looked good." |
| **What Was Extracted** | The conceptual principle(s) taken, not the composition. |
| **Deep Recon Performed** | `Yes` / `No` — whether `REFERENCE-RECON-PROTOCOL.md` was invoked on this reference. |

This is markdown/JSON provenance, not a database. Do not build tracking infrastructure beyond these fields.
