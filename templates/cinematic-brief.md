# CINEMATIC BRIEF: [PROJECT NAME]

> **Date Created:** YYYY-MM-DD
> **Status:** DRAFT | COMPLETE (`motion.cinematic_brief_complete: true`)
> **Stage:** Motion / Cinematic Direction — Specialist Hand-off
> **Rule:** This brief is binding. The specialist adapts to it; it does not adapt to the specialist's defaults. See `CINEMATIC-INTEGRATION-PROTOCOL.md`.

---

## 1. Project & Positioning
- **Project:** [Name]
- **Brand Positioning:** [From `positioning.md`]
- **Motion Level:** `MOTION_LEVEL_[2/3]` [Reference to `motion-direction.md`]

---

## 2. Hero Specification
- **Hero Type:** [From `MOTION-DIRECTION-PROTOCOL.md` §5 list]
- **Hero Subject:** [What is depicted]
- **Hero Action:** [What movement/action occurs]
- **Environment:** [Setting]
- **Camera Language:** [Angle, movement, framing]
- **Lighting:** [Direction, quality, mood]
- **Color Grade:** [Must resolve to `design-system.md` color tokens — not the specialist's default grade]

---

## 3. Behavior Specification
- **Scroll Relationship:** [How the hero/scene responds to scroll]
- **Text Behavior:** [Placement, reveal, fade — must resolve to `design-system.md` typography tokens, not the specialist's default centered-stack composition]
- **Transition Philosophy:** [How this scene hands off to the next section]

---

## 4. Module Governance
- **Approved Cinematic Modules:** [Explicit list, from `CINEMATIC-INTEGRATION-PROTOCOL.md` §6 — each with a one-line reason tied to this brand's story]
- **Prohibited Modules:** [Explicit list — modules that exist in the library but do not serve this client]

---

## 5. Performance & Fallback (Non-Negotiable — see `CINEMATIC-INTEGRATION-PROTOCOL.md` §7)
- **Performance Budget:** [Hero asset size ceiling, frame count, preload strategy]
- **Mobile Fallback:** [What replaces the desktop treatment on constrained devices/networks]
- **Reduced-Motion Fallback:** [Static equivalent preserving meaning]

---

## 6. Asset Requirements
- **Assets Needed:** [Source photography, generated imagery, video, or existing brand assets]
- **Assets Explicitly Excluded:** [Any source-brand asset from research that must not be reused — cross-reference `REFERENCE-RECON-PROTOCOL.md` §5 "May Not Transfer"]

---

## 7. Cost Authorization (see `CINEMATIC-INTEGRATION-PROTOCOL.md` §5)
- **Paid Services Required:** [e.g., "Kling video generation via WaveSpeed"] or "None"
- **Approximate Cost:** [$X, stated before any paid call]
- **Owner Authorization:** [ ] Obtained — Date: YYYY-MM-DD  \| [ ] Not yet obtained (build must not proceed past this point)

---

## 8. User Approval Points
- [ ] Brand/scene concept approved before generation.
- [ ] Generated image/video approved before frame extraction and site integration.
- [ ] Final built site reviewed in browser before handoff to QA.

---

## 9. Brief Completion Declaration
- [ ] Every field above resolves to Website Director's locked design-system tokens, not the specialist's defaults, except where `CINEMATIC-INTEGRATION-PROTOCOL.md` §3 designates an engineering necessity.
- [ ] Mobile and reduced-motion fallbacks documented (§5).
- [ ] Cost authorization obtained if paid services are required (§7).
- [ ] Ready to set `motion.cinematic_brief_complete: true` in `site-profile.json`.
