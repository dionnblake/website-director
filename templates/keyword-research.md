# KEYWORD RESEARCH & SEARCH INTENT: [PROJECT NAME]

> **Date Created:** YYYY-MM-DD
> **Status:** DRAFT | APPROVED
> **Stage:** SEO Intelligence Director — Steps 2–4, 6 (`SEO-INTELLIGENCE-PROTOCOL.md` §5)
> **Rule:** Unknown metrics stay `unknown`. Never invent a number. Rank by opportunity, not volume alone.

---

## 1. First-Party Search Console Opportunity (if applicable)

Skip this section with a one-line reason if no existing site / no GSC access.

| Query | Page | Impressions | Position | Opportunity Type |
| :--- | :--- | :--- | :--- | :--- |
| [query] | [URL] | [n] | [pos] | `striking_distance` (4–20) / `cannibalization` / `improve_existing` / `unintended_ranking` |

**Priority logic applied:** first-party GSC opportunity → current-ranking opportunity → net-new keyword. Note here where an existing page should be improved rather than a new page created.

---

## 2. Keyword Universe

One row per shortlisted keyword. Expand from `seo-business-context.md` §3 seed topics via the capability routed in `SEO-INTELLIGENCE-PROTOCOL.md` §3.

| Keyword | Intent | Volume | Difficulty | CPC / Commercial Signal | Trend | Current Rank | SERP Characteristics | Business Fit |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [keyword] | Informational / Commercial Investigation / Transactional / Navigational / Local / Comparison | [n or `unknown`] | [n or `unknown`] | [$ or `unknown`] | [↑/↓/flat or `unknown`] | [n or `unknown`] | [e.g. AI Overview present, 3 local packs, forum-dominated] | [High / Medium / Low + why] |

**Intent ↔ page-type discipline:** informational queries map to guides/hubs, not sales pages. Transactional queries map to service/product/category pages, not generic blog posts. Navigational queries (brand terms) map to the homepage. Local queries map to location pages where the business has a real physical/service presence — never fabricated for markets not served.

---

## 3. Opportunity Scoring & Clustering

Score = business fit + audience fit + search intent + conversion potential + volume + difficulty + current rank + SERP competition + competitor weakness (from `seo-competitive-landscape.md`) + content-authority fit. A high-volume, irrelevant, or unrealistically difficult keyword is rejected regardless of volume; a smaller keyword with strong commercial intent and realistic difficulty can outrank it.

| Keyword / Cluster | Priority | Rationale | Assigned Page (from `keyword-map.md`) |
| :--- | :--- | :--- | :--- |
| [keyword or cluster of related queries] | `PRIMARY` / `SECONDARY` / `SUPPORTING` / `FUTURE` / `REJECT` | [Why] | [Page, or "TBD — see keyword-map.md"] |

**Clustering rule:** group semantically/strategically related queries onto one comprehensive page rather than one page per keyword. Only split into separate pages where the underlying intents are genuinely distinct.

---

## 4. Rejected Keywords

| Keyword | Volume (if known) | Reason for Rejection |
| :--- | :--- | :--- |
| [keyword] | [n / unknown] | [Irrelevant to business / unrealistic difficulty / wrong market / etc.] |

---

## 5. Research Sign-Off
- [ ] Every keyword carries an intent classification.
- [ ] No metric was invented — unknowns are marked `unknown`, not guessed.
- [ ] GSC opportunities (§1) were prioritized over net-new discovery where applicable.
- [ ] Opportunity scoring (§3) used more than volume alone.
- [ ] `RESEARCH_DATE`, `DATA_SOURCE`, `TARGET_MARKET` recorded (see `SEO-INTELLIGENCE-PROTOCOL.md` §10).
- [ ] Ready to feed `templates/keyword-map.md`.
