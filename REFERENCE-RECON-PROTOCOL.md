# REFERENCE RECON PROTOCOL: BOUNDED FORENSIC ANALYSIS

> **Version:** 1.1.0
> **Status:** Mandatory Operating Standard (V1.1 Extension)
> **Rule:** Reconnaissance, never reconstruction. Default cloning behavior is explicitly disabled.

---

## 1. Source and Boundary

**Source methodology:** `https://github.com/JCodesMore/ai-website-cloner-template` — a 5-stage pipeline (Reconnaissance → Foundation → Component Specs → Parallel Build → Assembly & QA) built to produce pixel-perfect clones.

**What Website Director borrows:** Stage 1 only — its reconnaissance methodology (screenshot capture, computed-style extraction, design-token identification, and an interaction sweep across scroll, hover, click, and responsive breakpoints).

**What Website Director never triggers:** Stages 2–5 (foundation setup, component-spec generation for parallel-agent rebuilding, distributed build, assembly/visual-diff QA against the original). These stages exist to reconstruct the target site. Website Director has no reconstruction goal.

This distinction is enforced through a single operating mode:

```
                    JCODESMORE DEFAULT MODE
                    (pixel-perfect cloning)
                              │
                              ✕  NEVER USED BY WEBSITE DIRECTOR
                              │
                    RESEARCH_ONLY_MODE
              (Website Director's bounded adaptation)
```

---

## 2. `RESEARCH_ONLY_MODE`

**Trigger:** Invoked only on the 2–3 deep-recon targets that survive progressive filtering (`RESEARCH-SOURCES.md` §6) — never on the full 10–15 candidate pool.

### Allowed
- Screenshots (full page, key sections, key interaction states)
- DOM inspection
- Computed style extraction (`getComputedStyle()` values: colors, spacing, typography)
- Spacing-relationship analysis (base unit, rhythm, container widths)
- Responsive behavior across breakpoints
- Interaction analysis (hover, click, scroll-triggered states)
- Animation analysis (easing, duration, trigger thresholds — the mechanics, not the asset)
- State analysis (nav open/closed, active/inactive, loading states)
- Navigation behavior (sticky/shrink/blur behavior, menu architecture)
- Component morphology (how a section is structured, not its literal content)
- Grid analysis (column count, gutter ratios, alignment anchors)
- Asset-*type* identification (e.g., "uses a looping background video," not downloading that video)
- Typography behavior (scale ratios, pairing logic, tracking rules)

### Not Allowed
- Rebuilding the target website
- Downloading source brand photography, illustrations, or logos for reuse
- Copying exact copy/text
- Reproducing exact section composition
- Generating a pixel-perfect clone of any part of the site
- Transferring distinctive branded assets (custom icon sets, signature illustrations, proprietary 3D renders)

---

## 3. The Transformation Pipeline

```
REFERENCE WEBSITE
      │
      ▼
FORENSIC RECONNAISSANCE   (§2 Allowed list only)
      │
      ▼
DESIGN PRINCIPLES          (what structural/visual mechanic is at work)
      │
      ▼
BEHAVIOR PRINCIPLES        (what interaction/motion mechanic is at work)
      │
      ▼
WHY IT WORKS                (which of the Seven Pillars of Justification it serves)
      │
      ▼
APPLICATION TO CLIENT       (how it translates to this client's actual brand/content)
      │
      ▼
ORIGINAL DESIGN
```

**Never:** `REFERENCE WEBSITE → COPY IT`. If a step in this pipeline cannot be completed honestly — if the "application to client" column would just be the reference's own composition with the client's logo swapped in — the finding is discarded, not forced into the synthesis.

---

## 4. Operational Steps

1. **Capture.** Take representative screenshots (desktop + mobile) and, where a live browsing/automation tool is available, inspect the DOM and computed styles of the sections relevant to the study's purpose. State the purpose before capturing (e.g., "studying this site's sticky-nav shrink behavior and hero typography scale" — not "look at everything").
2. **Extract.** Fill `templates/reference-deconstruction.md` — one file per deep-recon target. Every row must separate the *observed mechanic* from the *extracted principle*.
3. **Separate transferable from non-transferable.** Explicitly list what is distinctive to the source brand and must not transfer (its logo, its illustration style, its literal copy, its unique compositional signature) alongside what is a transferable principle (its spacing rhythm, its interaction model, its responsive strategy).
4. **Interpret for the client.** Cross-reference extracted principles against the client's actual brand posture from `DISCOVERY-PROTOCOL.md`, the same way `REFERENCE-PROTOCOL.md` §3 (Step 3: Brand Interpretation) already does for user-supplied references. This protocol does not replace that interpretation step — it feeds it with agent-discovered rather than user-supplied material.

---

## 5. Copyright / Originality Constitution

**The primary rule:** `STEAL THE REASONING, NEVER THE COMPOSITION.`

Every borrowed principle must survive two questions:
1. **Why does this work?** (mechanically — what pillar of justification does it serve)
2. **Why is it appropriate for this client?** (specifically — not "it looks premium," but tied to this client's actual positioning)

If either question cannot be answered concretely, the principle is not used.

### May Extract
Hierarchy principles, proportions, spacing relationships, navigation concepts, information-architecture principles, interaction concepts, motion concepts, responsive strategies, typography relationships, image-treatment concepts, section-sequencing principles, density, visual rhythm.

### May Not Transfer
Logos, exact copy, proprietary photography, illustrations, branded visual assets, entire component trees, exact layouts, distinctive source-brand graphics, trademarked visual identity, unique creative compositions reproduced materially unchanged.

This list is identical in spirit to the Anti-Cloning Rules already in `REFERENCE-PROTOCOL.md` §4 — deep reconnaissance does not loosen those rules, it just gives Website Director a more forensic way to honor them.

---

## 6. Output

Populated `templates/reference-deconstruction.md` per deep-recon target, feeding `templates/research-synthesis.md`. Record provenance per `RESEARCH-SOURCES.md` §7, with `Deep Recon Performed: Yes` and the study's stated purpose.
