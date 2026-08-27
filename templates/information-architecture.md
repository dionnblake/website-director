# INFORMATION ARCHITECTURE SPECIFICATION: [PROJECT NAME]

> **Date Created:** YYYY-MM-DD  
> **Status:** DRAFT | LOCKED (`INFORMATION_ARCHITECTURE_LOCKED: true`)  
> **Rule:** Architecture follows commercial psychology, not generic templates.

---

## 1. Visitor Psychology & Conversion Funnel

```
VISITOR ARRIVAL
      │
      ▼
UNDERSTAND (What is this and what pain does it solve?)
      │
      ▼
BELIEVE (Why is this company credible and superior to alternatives?)
      │
      ▼
EVALUATE (How does it work, what are the mechanics, what is the ROI?)
      │
      ▼
CONVERT (Frictionless commitment to primary CTA)
```

---

## 2. Page Footprint & Global Sitemap

| Page | Route | Purpose | Primary Conversion Target |
| :--- | :--- | :--- | :--- |
| **Home / Landing** | `/` | Comprehensive value proposition, credibility proof & primary conversion | Book Demo / Get Started |
| **Solutions / Product** | `/solutions` | In-depth breakdown of features, workflows, and technical specs | Start Trial / Schedule Walkthrough |
| **Case Studies** | `/case-studies`| Quantifiable customer transformation stories & ROI evidence | Read Case Study $\rightarrow$ Book Call |
| **Pricing** | `/pricing` | Transparent tier comparison, FAQ, ROI calculator | Select Plan / Talk to Sales |
| **Company / About** | `/about` | Leadership, vision, mission, and career openings | Contact Us / Apply |

---

## 3. Section Morphology & Layout Rhythm (Home Page Example)

To prevent visual fatigue, consecutive sections must alternate layout morphology and visual density.

```
┌────────────────────────────────────────────────────────────────────────┐
│ SECTION 1: ASYMMETRIC HERO                                              │
│ Morphology: Left-heavy headline + dynamic visual anchor canvas (Right) │
│ Cognitive Purpose: Immediate comprehension of core value (< 5 sec).     │
├────────────────────────────────────────────────────────────────────────┤
│ SECTION 2: PROOF MATRIX & CLIENT CREDIBILITY STRIP                      │
│ Morphology: Compact horizontal ticker & audited quantitative metrics  │
│ Cognitive Purpose: Incontrovertible validation before scrolling deeper.│
├────────────────────────────────────────────────────────────────────────┤
│ SECTION 3: CORE CAPABILITIES & DIFFERENTIATION                         │
│ Morphology: Staggered alternating 2-column feature blocks              │
│ Cognitive Purpose: Explain unique superpower vs competitors.          │
├────────────────────────────────────────────────────────────────────────┤
│ SECTION 4: DEEP DIVE / TECHNICAL ARCHITECTURE                          │
│ Morphology: Interactive tabbed console / dense comparison matrix       │
│ Cognitive Purpose: Fulfill technical diligence for decision-makers.    │
├────────────────────────────────────────────────────────────────────────┤
│ SECTION 5: CUSTOMER EVIDENCE / CASE STUDY SPOTLIGHT                    │
│ Morphology: Single large editorial pull-quote + verified ROI metrics   │
│ Cognitive Purpose: Emotional resonance & peer proof.                   │
├────────────────────────────────────────────────────────────────────────┤
│ SECTION 6: HIGH-IMPACT CONVERSION FINALE (CTA)                         │
│ Morphology: High-contrast bounded container with minimal friction form │
│ Cognitive Purpose: Direct, decisive commitment action.                 │
├────────────────────────────────────────────────────────────────────────┤
│ SECTION 7: ARCHITECTURAL FOOTER                                         │
│ Morphology: Structured multi-column sitemap + legal + live status badge│
│ Cognitive Purpose: Navigation completion, compliance, and wayfinding.  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Section Morphology Review & Anti-Repetition Audit
- [ ] No two consecutive sections use the same column grid structure.
- [ ] Visual weight alternates between dense analytical data and spacious editorial breathing room.
- [ ] Mobile reflow has been mapped for each section.
- [ ] Every section has a defined cognitive conversion objective.
- [ ] Ready to lock `INFORMATION_ARCHITECTURE_LOCKED` in `site-profile.json`.
