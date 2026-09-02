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
- **Journey / Seam:** [How this scene connects to the next segment; record `SEAM_LAW` or `NOT_APPLICABLE`]
- **Ending Rest:** [How long the settled frame remains readable; record `ENDING_REST_MEASUREMENT`]

---

## 4. Production Intelligence Package

- **Creative Director Loop:** [Project truth → visual thesis → end frame → render strategy → evidence review]
- **Design Package:** [Required shot/segment package, text-safe zones, content ownership, and approval scope]
- **Shot Laws:** [`PLAN_END_FRAME_FIRST` | `NEGATIVE_SPACE_COMPOSITION` | `BOUNDARY_CROSSING_REALISM` | `CHAINED_JOURNEY_METHOD` | `SEAM_LAW` — mark each `APPLIED` or `NOT_APPLICABLE` with a reason]
- **Segment Inventory:** [Segment IDs, purpose, transition, fallback, and owner approval status]
- **Cheap Gate:** [Low-cost local or synthetic checks completed before expensive generation]
- **Failure / Repair Notes:** [`CINEMATIC_FAILURE_KNOWLEDGE` — loading, keyframes, timing, legibility, mobile, or environment]

### 4.1 Owner-required sequence trace

| Sequence ID | Owner requirement / approved direction | Implementation location | Runtime evidence receipt | Meaningful state change | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [ID] | [owner-intent or motion-direction reference] | [file/module/selector] | [browser QA run and receipt] | [measured PASS / FAIL / BLOCKED] | [PASS / FAIL / BLOCKED] |

Level 2/3 completion requires every promised sequence to be represented. A
static screenshot, GSAP/CSS declaration, or simulation result is not a runtime
receipt. See `FRAMEWORK-VALIDATION-PROTOCOL.md` for the authority and
compliance audit.

---

## 5. Render Strategy Decision

- **Selected Strategy:** `DENSE_KEYFRAME_VIDEO_SCRUB` | `CANVAS_FRAME_SEQUENCE` | `STATIC_HERO_DESIGN`
- **Rejected Alternative:** [Strategy and evidence-based reason]
- **Browser Proof Run:** [Browser QA run ID / `NOT_RUN`]
- **Dense-Keyframe Encoding:** [GOP/keyframe decision if video is selected]
- **Loading Strategy:** [Blob/object URL lifecycle or frame preload strategy]
- **Runtime Controls:** [rAF smoothing, delta-time normalization, seek coalescing, delta-gated DOM updates, compositor isolation]
- **Scrub Proof:** [Start/mid/settle alignment, stutter, memory, and performance observations]
- **Video Tooling:** [`FFMPEG_SCRUB_RECIPES` in raw/review workspace only | `NOT_APPLICABLE`]

---

## 6. Module Governance
- **Approved Cinematic Modules:** [Explicit list, from `CINEMATIC-INTEGRATION-PROTOCOL.md` §6 — each with a one-line reason tied to this brand's story]
- **Prohibited Modules:** [Explicit list — modules that exist in the library but do not serve this client]

---

## 7. Performance & Fallback (Non-Negotiable — see `CINEMATIC-INTEGRATION-PROTOCOL.md` §8)
- **Performance Budget:** [Hero asset size ceiling, frame count, preload strategy]
- **Mobile Fallback:** [What replaces the desktop treatment on constrained devices/networks]
- **Reduced-Motion Fallback:** [Static equivalent preserving meaning]
- **Complete Without Video:** [Semantic content, navigation, CTA, and visual meaning remain available]
- **Moving Background Legibility:** [`MOVING_BACKGROUND_LEGIBILITY_AUDIT` result and worst-frame contrast evidence]
- **Flick Test:** [`FLICK_TEST` result across the required render set]

---

## 8. Asset Requirements
- **Assets Needed:** [Source photography, generated imagery, video, or existing brand assets]
- **Assets Explicitly Excluded:** [Any source-brand asset from research that must not be reused — cross-reference `REFERENCE-RECON-PROTOCOL.md` §5 "May Not Transfer"]
- **Provenance / Rights:** [Evidence ledger refs, license status, source inputs, and output hashes]
- **Segment Approval:** [Each generated or edited segment: `APPROVED` | `REJECTED` | `BLOCKED`]

---

## 9. Cost Authorization (see `CINEMATIC-INTEGRATION-PROTOCOL.md` §6)
- **Paid Services Required:** [Provider-neutral operation description] or "None"
- **Approximate Cost:** [$X or `UNKNOWN_PENDING_PROVIDER_SELECTION`, stated before any paid call]
- **Cheap Gate Result:** [`PASS` | `FAIL` | `BLOCKED`]
- **Owner Authorization:** [ ] Obtained — Date: YYYY-MM-DD  \| [ ] Not yet obtained (build must not proceed past this point)

---

## 10. User Approval Points
- [ ] Brand/scene concept approved before generation.
- [ ] Each generated image/video segment approved before frame extraction and site integration.
- [ ] Final built site reviewed in browser before handoff to QA.
- [ ] Rejected segments and tail-trim/reroll decisions recorded.

---

## 11. Brief Completion Declaration
- [ ] Every field above resolves to Website Director's locked design-system tokens, not the specialist's defaults, except where `CINEMATIC-INTEGRATION-PROTOCOL.md` §3 designates an engineering necessity.
- [ ] Mobile and reduced-motion fallbacks documented (§7).
- [ ] A render strategy is selected and real-browser proof is recorded where a cinematic strategy is used (§5).
- [ ] Cost authorization obtained if paid services are required (§9).
- [ ] Segment-level approvals, provenance, and rights status are complete (§8 and §10).
- [ ] Ready to set `motion.cinematic_brief_complete: true` in `site-profile.json`.
