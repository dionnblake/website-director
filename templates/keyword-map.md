# KEYWORD MAP: [PROJECT NAME]

> **Date Created:** YYYY-MM-DD
> **Status:** DRAFT | LOCKED (feeds `INFORMATION_ARCHITECTURE_LOCKED` / `CONTENT_STRUCTURE_LOCKED`)
> **Stage:** SEO Intelligence Director — Step 7 (`SEO-INTELLIGENCE-PROTOCOL.md` §5)
> **Rule:** Every page in the sitemap appears here. No keyword assigned to two pages without a deliberate, stated reason.

---

## 1. Page / Keyword Map

| Page | Role | Primary Keyword | Secondary Keywords | Intent | Priority | Existing / New |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `/` | Homepage | [High-level brand/category term, or "none — navigational only"] | [...] | [...] | [...] | [Existing / New] |
| [route] | [Money page / Hub / Guide / FAQ / Location / etc.] | [keyword] | [...] | [...] | [...] | [...] |

**Homepage discipline:** the homepage does not attempt to rank for every keyword. It communicates who the business is, what it does, who it serves, why it matters, and what to do next — see `SKILL.md` Phase 5 §Homepage Rule. More specific intents map to dedicated pages below.

---

## 2. Per-Page Detail (Required for Every `PRIMARY`-Priority Page)

### [Page Name] — `[route]`
- **PAGE PURPOSE =** [Why this page exists]
- **TARGET AUDIENCE =** [Who lands here]
- **PRIMARY SEARCH INTENT =** [From `keyword-research.md` §2]
- **PRIMARY KEYWORD =**
- **SECONDARY KEYWORDS =**
- **SUPPORTING ENTITIES / TOPICS =** [Semantic coverage beyond exact-match terms]
- **PRIMARY CONVERSION =** [Ties to `project-brief.md` primary/secondary conversion]
- **INTERNAL LINK TARGETS =** [Which other mapped pages this links to/from]
- **EVIDENCE =** [Cite `keyword-research.md` row(s) and/or `seo-competitive-landscape.md` finding]

*(repeat per `PRIMARY` page; `SECONDARY`/`SUPPORTING` pages may use an abbreviated version of the same fields)*

---

## 3. Cannibalization Check

| Keyword | Pages Considered | Resolution |
| :--- | :--- | :--- |
| [keyword appearing on multiple candidate pages] | [Page A, Page B] | [Which page owns it, and why] |

---

## 4. Information Architecture Influence

State explicitly how this map changed or confirmed the sitemap versus a purely commercial-psychology-driven draft: [what SEO evidence added, subtracted, or reordered — e.g. "added /guides hub for informational cluster X", "rejected a dedicated /pricing-comparison page — no search demand found"].

---

## 5. Keyword Map Sign-Off
- [ ] Every page in the intended sitemap appears in §1.
- [ ] Every `PRIMARY` page has full detail in §2.
- [ ] No keyword duplicated across pages without a resolution in §3.
- [ ] Homepage discipline (§1) respected — not every keyword forced onto `/`.
- [ ] Thin pages were not created merely because a keyword existed — every page has a stated purpose beyond ranking.
- [ ] `seo.complete` may now be set to `true` in `site-profile.json` (or the bounded exception in `SEO-INTELLIGENCE-PROTOCOL.md` §7 was recorded instead).
