# RESEARCH SOURCES: VISUAL INTELLIGENCE ACQUISITION CHANNELS

> **Version:** 1.3.0
> **Status:** Mandatory Operating Standard (V1.1 Extension; V2.11.1 adapter and V2.15 cinematic intelligence additive)
> **Purpose:** Define what each research channel is for, what it may never be used for, and what provenance every finding must carry.

---

## 1. The Visual Intelligence Acquisition Channels

```
┌────────────────────────────────────────────────────────────────┐
│ CHANNEL 1: INDUSTRY LANDSCAPE   — what does this market expect? │
├────────────────────────────────────────────────────────────────┤
│ CHANNEL 2: LANDBOOK             — what should we study?         │
├────────────────────────────────────────────────────────────────┤
│ CHANNEL 2.25: DESIGN INSPIRATION MCP — bounded discovery signal │
├────────────────────────────────────────────────────────────────┤
│ CHANNEL 2.5: AWWWARDS SHOWCASE  — what is the world-class bar?  │
├────────────────────────────────────────────────────────────────┤
│ CHANNEL 3: CROSS-INDUSTRY       — who expresses this better?    │
├────────────────────────────────────────────────────────────────┤
│ CHANNEL 4: JCODESMORE RECON     — how exactly does it work?     │
└────────────────────────────────────────────────────────────────┘
```

No core research channel is optional by default for ambitious projects. The
Design Inspiration MCP is an optional transport layered onto discovery, not a
replacement for a channel. Awwwards research is mandatory for
`CREATIVE_AMBITION = SHOWCASE` per `AWWWARDS-SHOWCASE-INTELLIGENCE.md`. A
channel may be skipped only under the bounded exception defined in
`VISUAL-RESEARCH-PROTOCOL.md` §5, and the skip must be recorded in
`site-profile.json` → `research.exception`, never applied silently.

### 1.1 Inspiration Source Registry (V2.15 additive)

`templates/inspiration-source-registry.json` is the bounded registry for
owner-selected inspiration. It formalizes four useful discovery roles without
creating a new research authority, state, phase, gate, or lock:

| Source ID | Role | Use |
| :--- | :--- | :--- |
| `21ST_DEV` | `COMPONENT_PATTERN_LIBRARY` | Study component mechanics and interaction ideas. Source reuse requires license, provenance, stack, and design-system checks. |
| `GODLY` | `CURATED_SITE_AND_SECTION_DISCOVERY` | Widen site and section candidates, including cross-industry atmosphere and rhythm. |
| `AWWWARDS` | `WORLD_CLASS_DIMENSIONAL_REFERENCE_BAR` | Use the existing `AWWWARDS-SHOWCASE-INTELLIGENCE.md` authority and assign explicit benchmark dimensions. |
| `MOTIONSITES` | `MOTION_PATTERN_AND_BACKGROUND_LIBRARY` | Study motion, layering, and atmosphere; premium or unavailable material remains `REFERENCE_ONLY`. |

`LANDBOOK`, `DESIGN_INSPIRATION_MCP`, `INDUSTRY_LANDSCAPE`,
`CROSS_INDUSTRY`, and `REFERENCE_RECON` remain preserved entries in the same
registry and keep their existing authorities. The registry is a research
index, not a provider integration.

An owner request is recorded in the existing `research{}` state as an
`owner_selected_references` record. The record must preserve the raw source,
URL, reference type, element or section, what the owner likes, and what the
owner does not want, then add `PATTERN_TO_LEARN`, `ASSIGNED_DIMENSION`,
`WHAT_NOT_TO_COPY`, relevance, risk, license, and provenance fields. A source
selected only because it “looks cool” is not a valid research rationale.

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

## 3.25. Channel 2.25: Unified Design Inspiration MCP

**Adapter contract:** `integrations/design-inspiration/ADAPTER.md`.

**What it is:** One pinned, audited discovery transport for structured search
evidence from Dribbble, Behance, Awwwards, Mobbin, and Pinterest. It is useful
for widening the initial candidate pool and comparing platform-specific
signals, but the normalized evidence is not a design decision.

**What it is not:** A fifth design authority, five separate integrations, a
website cloner, an asset source, or a token-generation authority. Awwwards
policy and interpretation remain owned by
`AWWWARDS-SHOWCASE-INTELLIGENCE.md`; this adapter only supplies discovery
transport.

**Credential policy:** `SERPER_API_KEY` is environment-only. The explicit
states are `AVAILABLE`, `BLOCKED_CREDENTIAL_MISSING`, and `DISABLED`. The
deterministic repository suite uses synthetic structured results and does not
need a live key.

**Query and budget policy:** Queries derive from project-specific brief,
positioning, audience, emotion, ambition, conversion, or reference-mode
context. Generic or sensitive queries are rejected or safely rewritten. The
budget is 8/12 initial, 3/6 shortlist, and 1–3 deep candidates. Canonical
source URLs deduplicate repeated evidence.

**Required candidate evidence:** Platform, exact source URL, exact query,
retrieval timestamp, upstream commit, grade, why selected, pattern to learn,
what not to copy, production plausibility, accessibility risk,
implementation risk, and `copyright_boundary = REFERENCE_ONLY`.

**Image boundary:** Remote image URLs remain pointers for research review;
they are never downloaded, committed, or promoted into Asset Director's
production asset inventory.

---

## 3.5. Channel 2.5: Awwwards Showcase Intelligence

**What it is:** Formal external inspiration, craft benchmarking, and dimensional reference extraction from [Awwwards](https://www.awwwards.com/) for appropriately ambitious projects (`PREMIUM`, `SHOWCASE`, `EXPERIMENTAL`).

**Role in the pipeline:** Awwwards answers `WHAT IS THE WORLD-CLASS BENCHMARK?` — it provides dimensional reference bars across typography, layout, interaction, motion, and mobile execution.

**Hard rule:** Awwwards is a quality bar, not a template source or permission to copy. It activates as `REQUIRED` for `CREATIVE_AMBITION = SHOWCASE` per `AWWWARDS-SHOWCASE-INTELLIGENCE.md`.

**Output:** Feeds `templates/inspiration-board.md` and dimensional reference bars in `templates/visual-prototype-review.md`.

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
INDUSTRY LANDSCAPE + LANDBOOK + MCP + CROSS-INDUSTRY RESEARCH
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
| **Source Type** | `industry_competitor` \| `landbook` \| `design_inspiration_mcp` \| `cross_industry` \| `jcodesmore_deep_recon` |
| **Access / Research Date** | The date the reference was studied. |
| **Platform** | For MCP evidence: `Dribbble` \| `Behance` \| `Awwwards` \| `Mobbin` \| `Pinterest`; otherwise `NOT_APPLICABLE`. |
| **Query** | The exact project-specific query used, or `NOT_APPLICABLE` for non-MCP sources. |
| **Reference Grade** | `A` \| `B` \| `C` \| `D` from the bounded heuristic, or `UNASSESSED` while pending review. |
| **Reason Selected** | Why this reference is relevant to this client — never "it looked good." |
| **Pattern to Learn** | The transferable mechanic or principle, not the composition. |
| **What Not To Copy** | Literal copy, branded assets, distinctive composition, or other non-transferable material. |
| **Production Plausibility** | `HIGH` \| `MEDIUM` \| `LOW` \| `UNASSESSED`. |
| **Accessibility Risk** | Known risk, `NONE_OBSERVED`, or `UNASSESSED`; never inferred from visual polish. |
| **Implementation Risk** | Known risk, `LOW`/`MEDIUM`/`HIGH`, or `UNASSESSED`. |
| **What Was Extracted** | The conceptual principle(s) taken, not the composition. |
| **Deep Recon Performed** | `Yes` / `No` — whether `REFERENCE-RECON-PROTOCOL.md` was invoked on this reference. |

This is markdown/JSON provenance, not a database. Do not build tracking infrastructure beyond these fields.

## 8. Cross-cutting Evidence Ledger

The fields in this document remain the research-source authority for research
interpretation. For V2.12 projects, mirror the source identity needed for
traceability into templates/evidence-ledger.json, including platform, source
URL, query, retrieval time, reference grade, upstream SHA-256 where available,
PATTERN_TO_LEARN, WHAT_NOT_TO_COPY, and REFERENCE_ONLY status. The ledger does
not replace this research protocol, and research references do not become
production claims or assets without independent evidence.
