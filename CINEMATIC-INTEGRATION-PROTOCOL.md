# CINEMATIC INTEGRATION PROTOCOL: BINDING THE SPECIALIST TO THE BRIEF

> **Version:** 1.1.0
> **Status:** Mandatory Operating Standard (V1.1 Extension)
> **Rule:** Cinematic Sites executes an approved cinematic brief. It does not set direction. It never runs by default.

---

## 1. When This Protocol Activates

Only when Website Director has **selected** (not yet locked) `MOTION_LEVEL_2` or `MOTION_LEVEL_3` within Phase 8, and that selection specifically calls for capabilities the Robonuggets `cinematic-sites` skill provides (AI-generated hero animation, scroll-driven canvas frame sequences, the Cinematic Modules interaction library). Level 0–1 projects never invoke this protocol. Reaching Level 2–3 does not automatically invoke it either — many Level 2 sites are fully served by standard GSAP ScrollTrigger work with no specialist needed.

**Sequencing (do not invert):** motion level is selected → this protocol runs and produces `cinematic-brief.md` → `motion.cinematic_brief_complete` is set `true` → only then does `locks.motion_direction_locked` engage (`MOTION-DIRECTION-PROTOCOL.md` §6, `CINEMATIC-INTEGRATION-PROTOCOL.md` §8). The motion lock can never be a precondition for invoking this protocol — it is the other way around. If any document is ever read as requiring `motion_direction_locked: true` before the specialist can be engaged, that reading is wrong; this section is the authority on ordering.

`site-profile.json` → `motion.cinematic_specialist_required` records whether this protocol is in play for the current project.

---

## 2. Authority Boundary

```
┌────────────────────────────────────────────────────────┐
│              WEBSITE DIRECTOR (Design Authority)        │
│   business • positioning • UX • design direction •      │
│   design system • motion level • module selection •     │
│   hero composition • typography • palette • text        │
└───────────────────────────┬──────────────────────────────┘
                            │  issues
                            ▼
                  cinematic-brief.md
                    (BINDING CONTRACT)
                            │  consumed by
                            ▼
┌────────────────────────────────────────────────────────┐
│         CINEMATIC SITES (Implementation Specialist)      │
│   executes the brief using its generation pipeline and   │
│   Cinematic Modules library                              │
└──────────────────────────────────────────────────────────┘
```

Cinematic Sites adapts to the Website Director brief. Not the other way around. If a build produces output that contradicts the brief (wrong fonts, wrong composition, an unapproved module), that is a defect in the build, not a valid specialist override.

---

## 3. Engineering Necessity vs. Creative Default

`cinematic-sites`'s own SKILL.md states several "HARD RULES." They fall into two categories that must be handled differently:

### Keep — Engineering Necessities
These exist because the alternative is technically broken, not because they are Website Director's creative choice. Website Director does not relitigate these:
- Scroll-driven hero via canvas + JPEG frame sequence, never `<video>` + `video.currentTime` (browsers only seek to keyframes in compressed MP4s — this causes visible stutter regardless of brand).
- Inline SVGs instead of emoji for icons/illustrations.
- Font-contrast minimums (body text `#555`/`#999` floors, explicit button text contrast).
- No dark vignettes / no single shared backdrop wrapper around hero content (a rendering-quality rule, not a layout-direction rule).

### Overridable — Creative Defaults
These are `cinematic-sites`' own house style, calibrated for its example builds. They are **not** automatically Website Director design law and must be supplied by the brief instead:
- Font pairing (its default is Outfit + JetBrains Mono — Website Director's locked `design-system.md` typography tokens govern instead).
- Centered hero text stack composition.
- Specific backdrop treatments and color grade.
- Which Cinematic Modules are selected (its "Module Selection Guide by Industry" table is a starting suggestion list, not a binding choice).
- The specific hero subject/action/environment.

**Rule:** If `cinematic-brief.md` specifies a value, that value wins. If it is silent on a purely technical execution detail covered under "Keep," the specialist's engineering default applies.

---

## 4. The `cinematic-brief.md` Contract

Website Director generates `templates/cinematic-brief.md` before invoking the specialist. It specifies: project, brand positioning, motion level, hero type (from `MOTION-DIRECTION-PROTOCOL.md` §5), hero subject, hero action, environment, camera language, lighting, color grade, scroll relationship, text behavior, transition philosophy, approved cinematic modules, prohibited modules, performance budget, mobile fallback, reduced-motion fallback, asset requirements, and user approval points.

The specialist receives this brief and does not invent a competing brand direction. If the brief is incomplete for a decision the specialist must make, the specialist stops and asks Website Director — it does not fill the gap with its own default aesthetic.

---

## 5. Cost Boundary (Paid External Services)

`cinematic-sites` may call paid external generation services (Nano Banana Pro image generation is free; Kling video generation via WaveSpeed costs roughly $0.42–$0.56 per 5-second clip at time of writing, doubling for 10s). This is real money and must never be triggered merely because a cinematic build is in progress.

**Before any paid operation:**
1. Identify the exact service being called.
2. State the approximate cost.
3. Get explicit owner authorization — the specialist's own pause point ("Ready to proceed? This will cost approximately $X") satisfies this, but Website Director must never pre-authorize it on the owner's behalf or suppress that prompt.

**Never:**
- Expose API keys/credentials in conversation or logs.
- Write API keys into client-facing frontend code.
- Proceed past a cost-confirmation pause without an explicit yes.

---

## 6. Module Selection Stays With Website Director

Website Director selects which Cinematic Modules (if any) are used, informed by — but not dictated by — `cinematic-sites`' industry-suggestion table. The brief must list both **approved modules** and **prohibited modules** explicitly. A module that exists in the library is not automatically appropriate for this client; the same anti-homogenization discipline from `VISUAL-RESEARCH-PROTOCOL.md` §6 applies: if the module is being chosen because it's impressive rather than because it strengthens this specific brand's story, it is prohibited.

---

## 7. Fallbacks Are Non-Negotiable

Every cinematic build must specify, in the brief itself:
- **Mobile fallback** — what replaces the desktop-grade hero treatment on constrained devices/networks.
- **Reduced-motion fallback** — a static equivalent that preserves meaning, per `MOTION-DIRECTION-PROTOCOL.md` §7.

A cinematic build without both fallbacks documented is not eligible for `cinematic_brief_complete: true`.

---

## 8. State

`site-profile.json` → `motion.cinematic_specialist_required` (bool) and `motion.cinematic_brief_complete` (bool) are the only state this protocol writes. Neither is a lock; `locks.motion_direction_locked` remains the single authoritative gate for whether motion/build may proceed, per `MOTION-DIRECTION-PROTOCOL.md` §8. `cinematic_brief_complete` must be `true` before `motion_direction_locked` is set when `cinematic_specialist_required` is `true`.
