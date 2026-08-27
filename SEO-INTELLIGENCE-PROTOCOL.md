# SEO INTELLIGENCE PROTOCOL: THE SEO INTELLIGENCE DIRECTOR ROLE

> **Version:** 1.2.0
> **Status:** Mandatory Operating Standard (V1.2 Extension)
> **Rule:** Evidence before architecture. Never invent a search metric. Never let search demand override human clarity, brand voice, or conversion.

---

## 1. Why This Exists

Website Director V1.1 forms information architecture and content strategy from business discovery, commercial psychology, and visual research alone. That prevents generic AI-slop layout, but it does not prove the resulting sitemap targets what the audience actually searches for, or that the business can realistically compete for it. A real growth-literate director does not invent a sitemap and then "SEO it" afterward — they find out what people search for, what intent sits behind it, and who already wins that search market, *before* the sitemap is drawn.

V1.2 closes that gap with a bounded SEO intelligence phase that runs **before** `INFORMATION_ARCHITECTURE_LOCKED` and `CONTENT_STRUCTURE_LOCKED`, not instead of the commercial-psychology approach in `information-architecture.md` §1. Search evidence informs which pages exist and what they target; it does not replace conversion-funnel thinking, and it never overrides `DESIGN-CONSTITUTION.md`.

```
BUSINESS CONTEXT ──► KEYWORD DISCOVERY ──► INTENT ──► COMPETITIVE LANDSCAPE ──► OPPORTUNITY SCORING ──► KEYWORD MAP ──► ARCHITECTURE
```

**Do not confuse this with keyword stuffing.** The objective is never "find popular keywords, repeat them everywhere." The objective is: understand real search demand + search intent + competition + business fit, then build the right architecture. Readability, brand voice, conversion, credibility, UX, and semantic clarity are never sacrificed for mechanical keyword repetition — see §11.

---

## 2. Role Boundary: The SEO Intelligence Director

SEO Intelligence Director is a **bounded role and protocol**, not a separate persistent agent — the same session executes this phase (optionally as one isolated subagent call for context hygiene, never as a standing swarm member). This mirrors how the Visual Research Director role works in `VISUAL-RESEARCH-PROTOCOL.md` §2.

| It DOES | It DOES NOT |
| :--- | :--- |
| Establish required business/audience/market context before any research | Guess at search volume, difficulty, or rankings |
| Discover real keyword demand and classify search intent | Decide the final sitemap or page list unilaterally |
| Identify who wins this search market and why | Design the website or write final production copy |
| Distinguish business competitors from SEO competitors | Copy a competitor's site structure |
| Score keyword opportunities against business fit, not volume alone | Lock `INFORMATION_ARCHITECTURE_LOCKED` or `CONTENT_STRUCTURE_LOCKED` |
| Produce a page-level keyword map and per-page content briefs | Fabricate metrics when tools are unavailable |
| Recommend which pages the evidence supports | Override Website Director's final architecture call |

Website Director reads the evidence package, weighs it against `information-architecture.md` §1 (the `Understand → Believe → Evaluate → Convert` funnel) and this client's actual positioning, and makes the architecture call itself. **SEO evidence informs the sitemap; it does not dictate it.** A keyword with no legitimate page purpose behind it is rejected, not built around.

This mirrors `DESIGN-CONSTITUTION.md` §18 in spirit — see §12 below (Design Research Stays Separate) for the explicit boundary between this protocol and `VISUAL-RESEARCH-PROTOCOL.md`.

---

## 3. Capability Routing: Where SEO Evidence Comes From

Website Director does not invent SEO data itself. It routes to whichever SEO intelligence capability is actually available in the current environment, in this priority order:

1. **A skill or MCP explicitly named `seo-intelligence`** (conceptually backed by an OpenSEO-style MCP surfacing Google Search Console, DataForSEO, SERP evidence, keyword metrics, rankings, and backlinks) — use it first if present.
2. **The installed `claude-seo` plugin** — route market/competitor/keyword evidence through its specialist skills as needed: `claude-seo:seo-plan` (orchestration), `claude-seo:seo-cluster` (keyword clustering via SERP overlap), `claude-seo:seo-competitor-pages` (competitor page analysis), `claude-seo:seo-dataforseo` (live SERP, keyword metrics, backlinks), `claude-seo:seo-google` (GSC/GA4/CrUX), `claude-seo:seo-technical` (crawlability/indexability for QA).
3. **The installed `seo-ops` skill** — for first-party evidence: `gsc_client.py` (Search Console queries, striking-distance keywords, positions) and `content_attack_brief.py` (keyword intelligence, competitor gap analysis, decaying-content alerts) where API credentials are configured.
4. **None available.** Record `SEO_INTELLIGENCE_STATUS = BLOCKED` per §8. Do not fabricate.

Website Director interprets the evidence returned by whichever capability answered. The capability does not make the final website decision — Website Director does, per §2.

---

## 4. Required Business Context (Precondition for Any Research)

Before any keyword research, establish and record in `templates/seo-business-context.md`:

```text
BUSINESS =                  PRIMARY DOMAIN =
PRODUCT / SERVICE =         TARGET AUDIENCE =
PRIMARY CUSTOMER PROBLEM =  BUSINESS GOAL =
PRIMARY CONVERSION =        TARGET MARKET =
TARGET LOCATION / COUNTRY = LANGUAGE =
KNOWN COMPETITORS =         EXISTING WEBSITE =
```

Most of this is already captured in `templates/project-brief.md` (Discovery Stage 1) and `templates/positioning.md` (Discovery Stage 2) — do not re-interview the owner for information already on file; carry it forward into `seo-business-context.md`. **Do not run generic keyword research without this context.** Search volume without business relevance is not useful evidence.

---

## 5. The Research Pipeline

```
┌──────────────────────────────────────────────────────────┐
│ STEP 1: BUSINESS CONTEXT                                  │
│   → templates/seo-business-context.md                     │
├──────────────────────────────────────────────────────────┤
│ STEP 2: FIRST-PARTY SEARCH DATA (if a live site + GSC     │
│   exist) — queries with impressions, striking-distance     │
│   positions (~5–20), cannibalization, pages to improve     │
│   rather than replace. Priority order: GSC opportunity     │
│   → current-ranking opportunity → net-new keyword.         │
│   → templates/keyword-research.md §1                       │
├──────────────────────────────────────────────────────────┤
│ STEP 3: KEYWORD DISCOVERY                                  │
│   Seed topics from products, services, problems,           │
│   questions, category terms, use cases, buying/comparison/ │
│   informational/geographic intent → expanded via §3.       │
│   → templates/keyword-research.md §2                       │
├──────────────────────────────────────────────────────────┤
│ STEP 4: SEARCH INTENT CLASSIFICATION                        │
│   Informational / Commercial Investigation / Transactional/ │
│   Navigational / Local / Comparison — per keyword.          │
│   → templates/keyword-research.md §2                        │
├──────────────────────────────────────────────────────────┤
│ STEP 5: COMPETITIVE LANDSCAPE                                │
│   Who wins this search market; classify each competitor      │
│   (§9); analyze their winning pages, formats, gaps.           │
│   → templates/seo-competitive-landscape.md                    │
├──────────────────────────────────────────────────────────┤
│ STEP 6: KEYWORD OPPORTUNITY SCORING & CLUSTERING              │
│   Business fit + audience fit + intent + conversion +         │
│   volume + difficulty + current rank + SERP competition +     │
│   competitor weakness + authority fit → PRIMARY/SECONDARY/    │
│   SUPPORTING/FUTURE/REJECT. Cluster related queries onto      │
│   one page rather than one page per keyword.                  │
│   → templates/keyword-research.md §3                          │
├──────────────────────────────────────────────────────────┤
│ STEP 7: KEYWORD MAP                                            │
│   Page-level mapping, no keyword assigned to two pages         │
│   without a deliberate reason (no cannibalization).            │
│   → templates/keyword-map.md                                   │
├──────────────────────────────────────────────────────────┤
│ STEP 8: CONTENT BRIEFS (high-priority pages only)               │
│   → templates/seo-content-briefs.md                             │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
                    [ SEO_COMPLETE ]
                            │
                            ▼
     Hand off to templates/information-architecture.md
        and templates/content-plan.md for the actual
        INFORMATION_ARCHITECTURE_LOCKED / CONTENT_STRUCTURE_LOCKED
```

Never invent a value for search volume, difficulty, CPC, trend, or current rank. Where a capability cannot supply a metric, record it literally as `unknown` in `keyword-research.md` — an `unknown` is honest evidence; a guess is not.

---

## 6. `SEO_COMPLETE` — A Readiness Gate, Not a Design Lock

`seo.complete` in `site-profile.json` is a **readiness gate**, semantically distinct from the five design-approval locks in `locks{}` — the same category of state `research.complete` already occupies (see `SKILL.md` §5.2). It answers "is there enough search evidence to architect responsibly?" — not "has the owner approved a design."

**Precondition scope:** `seo.complete` (or a recorded exception) must be `true` before `locks.information_architecture_locked` **and** `locks.content_structure_locked` may engage. It is **not** a precondition for `locks.design_direction_locked` — visual direction and SEO evidence are independent streams (§12). Website Director may run this protocol and `VISUAL-RESEARCH-PROTOCOL.md` in either order, or in parallel.

**Required for `seo.complete: true` (via real research):**
- `templates/seo-business-context.md` populated.
- `templates/keyword-research.md` populated, including intent classification and opportunity scoring for every shortlisted keyword.
- `templates/seo-competitive-landscape.md` populated, with competitors classified per §9.
- `templates/keyword-map.md` populated — every page in the intended sitemap has a role, primary keyword (or explicit "no keyword target — navigational/utility page"), and evidence citation.
- `templates/seo-content-briefs.md` populated for every `PRIMARY` priority page.
- `RESEARCH_DATE`, `DATA_SOURCE`, and `TARGET_MARKET` recorded per §10.

**`seo.mode` values:** `"full"` (GSC + keyword discovery + competitive landscape all run), `"gsc_only"` (existing site, first-party GSC evidence sufficient to answer the architecture question, broader discovery not warranted), `"bounded"` (scoped down for project size, see §7), `"exception"` (not applicable, see §7), `"blocked"` (tooling unavailable — see §8; `complete` stays `false`).

---

## 7. The Bounded Exception

Website Director may permit SEO discovery to be skipped only for genuinely non-public-facing sites:
- Private internal application or authenticated operations console.
- Non-indexed prototype or internal tool.
- Explicit owner opt-out for a project with no meaningful organic-search audience.

**The exception must be recorded, never silently applied:**
```json
"seo": {
  "complete": true,
  "mode": "exception",
  "exception": { "applied": true, "reason": "Internal ops console — not public-facing, no organic search audience." }
}
```
Public marketing websites should normally require SEO intelligence. A missing or vague reason is treated as an unrecorded skip and blocks `INFORMATION_ARCHITECTURE_LOCKED` and `CONTENT_STRUCTURE_LOCKED`.

---

## 8. Failure Mode: `BLOCKED`

If no capability from §3 is available and the site is public-facing (SEO is materially important):
```json
"seo": { "complete": false, "mode": "blocked", "blocked_reason": "No seo-intelligence, claude-seo, or seo-ops capability reachable in this environment." }
```
Do not fabricate keyword or competitor data to work around this. Do not pretend discovery is complete. Report `SEO_INTELLIGENCE_STATUS = BLOCKED` to the owner and stop before `INFORMATION_ARCHITECTURE_LOCKED` — this is a genuine blocker, not a phase to improvise past.

---

## 9. Two Types of Competitors — Never Conflate Them

A site that outranks the business for an important query is not automatically a business rival. Classify every competitor found during §5 as exactly one of:

```text
DIRECT BUSINESS COMPETITOR    — sells the same thing to the same buyer
INDIRECT BUSINESS COMPETITOR  — solves the same problem differently
SEO COMPETITOR                — ranks well, is not a business rival (e.g. a trade magazine)
PUBLISHER / MEDIA
MARKETPLACE / DIRECTORY
COMMUNITY / FORUM
AUTHORITATIVE RESOURCE
OTHER
```

Preserve this distinction through scoring, page analysis, and the final report. A magazine outranking the business for a head term is an `SEO_COMPETITOR` insight (there's a content gap worth closing), not evidence that the magazine is stealing customers.

For the most relevant competitors (weighted toward `DIRECT`/`INDIRECT BUSINESS COMPETITOR` and the top `SEO_COMPETITOR`s), examine site architecture, hub/category pages, title/H1 patterns, content depth and format, internal linking, comparison/FAQ coverage, original tools or data, and structured data — to identify **patterns, gaps, and opportunities**, never to copy the structure wholesale. Use `claude-seo:seo-competitor-pages` where available for this step.

---

## 10. Research Freshness

SEO evidence goes stale. Every research pass records:
```text
RESEARCH_DATE =
DATA_SOURCE =
TARGET_MARKET =
```
Before reusing prior SEO research on this project, assess whether it remains current for the decision at hand. For a major new build, a substantial redesign, or a major content-architecture change, refresh keyword and competitor evidence rather than assuming old research still holds — do not silently reuse a stale `keyword-map.md` across unrelated projects or after a long gap.

---

## 11. Copywriting Discipline (No Keyword Stuffing)

Keywords from `keyword-map.md` and `seo-content-briefs.md` are strategic inputs to Phase 6 (`templates/content-plan.md`), not mandatory strings. When Phase 6 writes production copy, priority order is:

```
1. Human clarity
2. Search intent
3. Conversion
4. Brand voice
5. Semantic coverage
6. Appropriate, natural keyword usage
```

Never: keyword stuffing, robotic headings, repeated exact-match phrases, generic SEO filler, or copy written for crawlers instead of humans. This is additive to — never a relaxation of — the "no `Lorem Ipsum` or generic filler copy" rule already in `templates/content-plan.md` §3 and `SKILL.md` Phase 6.

---

## 12. Design Research Stays Separate

Do not confuse this protocol's competitor research with `VISUAL-RESEARCH-PROTOCOL.md`'s design/reference research. This protocol asks *what ranks, why, what search intent is served*. `VISUAL-RESEARCH-PROTOCOL.md` asks *what looks good, what design patterns are appropriate*. A site can be an `SEO_COMPETITOR` (§9) without being a useful visual reference, and vice versa. Keep the two evidence streams and their artifacts (`seo-competitive-landscape.md` vs. `competitor-landscape.md`) distinct — do not merge them into one document.

---

## 13. Cost Control

If the routed capability (§3) incurs API/credit cost:
1. Check for reusable, sufficiently recent evidence first (§10) before re-querying.
2. Prefer GSC first-party evidence where it already answers the question (§5 Step 2) before broad discovery.
3. Use focused seed sets, not exhaustive keyword sweeps.
4. Research the most relevant competitors first (§9), not every ranking domain.
5. Never spend credits without owner authorization where the environment requires it.

---

## 14. Handoff Boundary (Builder Cannot Reopen Strategy)

`keyword-map.md` and `seo-content-briefs.md` are locked inputs to Phase 9 (`IMPLEMENTATION-CONTRACT.md`) once `seo.complete` is `true`. The Website Builder implements the approved page/keyword mapping; it does not independently perform new keyword research or create new SEO-motivated pages merely because it notices search-relevant terms during the build. If new evidence suggests the specification itself was wrong, Website Director reopens this protocol explicitly — the Builder does not silently deviate. See `IMPLEMENTATION-CONTRACT.md` §3.
