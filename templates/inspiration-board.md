# INSPIRATION BOARD: [PROJECT NAME]

> **Date Created:** YYYY-MM-DD
> **Status:** DRAFT | APPROVED
> **Stage:** Visual Research Director — Step 3 (Landbook + Design Inspiration MCP + Cross-Industry, `RESEARCH-SOURCES.md` §3–4)
> **Rule:** Organized by design purpose, not a link dump. Every entry earns its place with a stated reason.
> **Registry:** `templates/inspiration-source-registry.json` — all sources default to `REFERENCE_ONLY`.

---

## 1. References by Design Purpose

Repeat this block under each relevant category heading. Not every category needs an entry — only populate categories the research actually surfaced something for.

### HERO
- **Reference:** [URL] — **Source Type:** `landbook` \| `design_inspiration_mcp` \| `cross_industry` — **Access Date:** YYYY-MM-DD
  - **Platform:** `Dribbble` \| `Behance` \| `Awwwards` \| `Mobbin` \| `Pinterest` \| `NOT_APPLICABLE`
  - **Query:** [Exact project-specific query, or `NOT_APPLICABLE`]
  - **Grade:** `A` \| `B` \| `C` \| `D` \| `UNASSESSED`
  - **Why Selected:** [Specific reason tied to this client]
  - **What Works:** [Observed mechanic]
  - **Pattern to Learn:** [Transferable principle, not the composition]
  - **What Not To Copy:** [What is distinctive to the source and stays with the source]
  - **Production Plausibility:** `HIGH` \| `MEDIUM` \| `LOW` \| `UNASSESSED`
  - **Accessibility Risk:** [Known risk, `NONE_OBSERVED`, or `UNASSESSED`]
  - **Implementation Risk:** `LOW` \| `MEDIUM` \| `HIGH` \| `UNASSESSED`
  - **Application to This Client:** [How the principle — not the composition — applies]

### TYPOGRAPHY
*(same fields)*

### NAVIGATION
*(same fields)*

### EDITORIAL STRUCTURE
*(same fields)*

### IMAGERY
*(same fields)*

### SECTION TRANSITIONS
*(same fields)*

### MOBILE
*(same fields)*

### CTA
*(same fields)*

### MOTION
*(same fields)*

### INTERACTION
*(same fields)*

### CONTENT PRESENTATION
*(same fields)*

---

## 2. Cross-Industry Rationale

For every entry above marked `Source Type: cross_industry`, state the explicit strategic relationship to the client's desired brand posture. A visually impressive cross-industry reference with no stated relationship is removed from this board, not kept "just in case."

| Cross-Industry Reference | Sector | Explicit Relationship to Client's Desired Posture |
| :--- | :--- | :--- |
| [URL] | [e.g., Architecture] | [e.g., "Restraint and material precision this law firm wants but legal-industry sites rarely express"] |

---

## 3. Shortlist for Deep Reconnaissance

From all entries above, name the 5 strongest references with their platform,
grade, and selection reason, then the 2–3 that warrant full
`REFERENCE-RECON-PROTOCOL.md` treatment (per `RESEARCH-SOURCES.md` §6
progressive filtering).

- **5 Strong References:** [List]
- **2–3 Deep Recon Targets:** [List] — **Reason each was escalated:** [Specific finding worth forensic study]

## 4. Owner-Selected Reference Record

Use this record when the owner brings a URL or names a specific source idea.
It extends the existing `research{}` state; it is not a new lock or readiness
flag. Preserve the owner's raw request before translating it into the
interpretation fields.

### 4.1 Owner request

```yaml
SOURCE: [21ST_DEV | GODLY | AWWWARDS | MOTIONSITES | LANDBOOK | OTHER_REGISTERED_SOURCE]
REFERENCE_URL: [Exact URL]
REFERENCE_TYPE: [component | site | section | motion | background | interaction | reference_bar]
ELEMENT_OR_SECTION: [Exact element, section, or behavior]
WHAT_I_LIKE: [Owner's words]
WHAT_I_DO_NOT_WANT: [Owner's boundary]
WHY_IS_THIS_RELEVANT: [Specific relationship to this client and goal]
```

### 4.2 Website Director interpretation

```yaml
OWNER_SELECTED_REFERENCE: true
SOURCE: [Registry SOURCE_ID]
URL: [Exact URL]
ASSIGNED_DIMENSION: [Typography | Hero | Layout | Motion | Interaction | Mobile | Conversion | Atmosphere | Other]
PATTERN_TO_LEARN: [Transferable principle, not source composition]
OWNER_REQUESTED_ELEMENT: [Requested behavior or element]
WHY_IS_THIS_RELEVANT: [Specific relationship to this client and goal]
WHAT_NOT_TO_COPY: [Copy, colors, type, assets, composition, or distinctive treatment]
REFERENCE_GRADE: [A | B | C | D | UNASSESSED]
LICENSE_STATUS: [NOT_REQUIRED_STUDY_ONLY | REVIEW_REQUIRED | VERIFIED | BLOCKED]
IMPLEMENTATION_RISK: [LOW | MEDIUM | HIGH | UNASSESSED]
ACCESSIBILITY_RISK: [NONE_OBSERVED | LOW | MEDIUM | HIGH | UNASSESSED]
PRODUCTION_PLAUSIBILITY: [HIGH | MEDIUM | LOW | UNASSESSED]
REFERENCE_ONLY_STATUS: true
WHY_IS_THIS_RELEVANT: [Specific relationship to this client and goal]
WHAT_SPECIFICALLY_WORKS: [Observed mechanic]
TRANSFERABLE_PRINCIPLE: [Mechanic expressed in neutral terms]
BRAND_ADAPTATION: [How the principle changes for this brand and locked system]
IMPLEMENTATION_MODE: STUDY_ONLY
```

If `IMPLEMENTATION_MODE` becomes `SOURCE_REUSE`, set
`LICENSE_CHECK_REQUIRED: true`, record `PROVENANCE_REF`,
`STACK_ADAPTATION`, and `DESIGN_SYSTEM_ADAPTATION`, and do not proceed unless
`LICENSE_STATUS: VERIFIED`. Never force a source component's framework onto a
project. A source selected only because “it looks cool” is rejected.

## 5. Board Sign-Off
- [ ] Every entry has a stated "Why Selected" tied to this client, not general visual appeal.
- [ ] MCP entries carry Platform, Query, Grade, Pattern to Learn, What Not To Copy, Production Plausibility, Accessibility Risk, and Implementation Risk.
- [ ] Every MCP image URL remains `REFERENCE_ONLY` and no MCP result is treated as a production asset or implementation token.
- [ ] Cross-industry entries carry an explicit strategic relationship (§2).
- [ ] Deep-recon shortlist named (§3).
- [ ] Owner-selected records preserve raw input and complete the interpretation contract (§4).
- [ ] Any source reuse has verified license and provenance evidence; study-only references remain `REFERENCE_ONLY`.
- [ ] Ready to feed `templates/reference-deconstruction.md` and `templates/research-synthesis.md`.
