# MOTION DIRECTION PROTOCOL: HOW ALIVE SHOULD THIS SITE FEEL?

> **Version:** 1.2.0
> **Status:** Mandatory Operating Standard (V1.1 Extension; V2.15 cinematic production intelligence additive)
> **Rule:** Motion is an art-direction decision, made deliberately, every time — including the decision to use none.

---

## 1. Why This Exists

`design-system.md` §13 already defines the token-level mechanics of motion (`--transition-fast/normal/smooth`, the `prefers-reduced-motion` reset). This protocol sits one level above that: it decides *how much* motion a given site should have and *why*, before any token is written. Website Director chooses the level — the operator is never asked to understand animation engineering.

---

## 2. The Four Motion Levels

| Level | Name | Character | Example Techniques |
| :--- | :--- | :--- | :--- |
| **MOTION_LEVEL_0** | Static / Editorial | Restraint is essential to the brand's credibility. | No animation beyond native browser behavior. |
| **MOTION_LEVEL_1** | Subtle | Motion supports comprehension without calling attention to itself. | Section reveals, nav transitions, hover feedback, image masks, restrained micro-interactions. |
| **MOTION_LEVEL_2** | Cinematic Enhancement | Motion actively strengthens storytelling and hierarchy. | Selective parallax, sticky narratives, image reveals, kinetic typography, scroll-driven transitions, cinematic section sequences. |
| **MOTION_LEVEL_3** | Cinematic Centerpiece | Motion is a primary brand expression, not an accent. | Scroll-driven canvas hero, generated hero animation, major narrative scrolling sequences, advanced GSAP choreography, immersive product/environment reveal. |

**Appropriate defaults by context** (a starting hypothesis, not a rule — the Motion Level Decision Framework in §4 makes the actual call):
- Legal, institutional, long-form editorial, information-heavy utilities → typically Level 0.
- Most local/home-service and B2B trust-building sites → typically Level 1.
- Architecture, design studios, hospitality, premium consumer brands with genuine visual material → often Level 2.
- Brand-as-product, flagship launches, entertainment, or cases where the motion *is* the product story → potentially Level 3.

---

## 3. The Motion Justification Rule

Every motion behavior must serve at least one of:
1. **Hierarchy** — directs attention to what matters most.
2. **Orientation** — helps the visitor understand where they are or where they're going.
3. **Storytelling** — advances a narrative the static layout could not tell.
4. **Feedback** — confirms an action was received.
5. **Atmosphere** — establishes mood consistent with brand posture.
6. **Brand Expression** — is itself a recognizable signature of this brand.

**If a motion behavior serves none of these: remove it.** This is the motion-specific instance of the Design Constitution's governing law (`DESIGN-CONSTITUTION.md` §1) — animation must never be added merely because the capability exists.

---

## 4. Motion Level Decision Framework

Before selecting a level, evaluate against:
- The business and what it actually sells.
- The audience and how they arrive (are they scanning quickly, or settling in to read?).
- The desired emotion from `positioning.md`.
- The amount and quality of real content/imagery available (motion cannot manufacture substance that doesn't exist).
- Mobile network conditions and device diversity of the actual audience.
- Accessibility — does any part of the audience rely on reduced motion?
- Conversion — does motion clarify the path to the primary CTA, or add friction before it?
- Technical architecture — is there a build pipeline that can support the chosen level, or is this a single-file static delivery?

**The most technologically impressive option is not automatically the correct option.** A plumbing company and an architecture studio can both legitimately justify different levels from the same framework — that divergence is the proof the framework is working, not an inconsistency to fix. See `examples/V1.1-VALIDATION-SIMULATIONS.md` for worked contrasts.

These are starting hypotheses only. An explicit current owner requirement for
cinematic, immersive, animation-heavy, or scroll-driven motion takes precedence
over this heuristic and resolves to `MOTION_LEVEL_3`. It cannot be silently
downgraded to Level 1. Any approved downgrade must be explicit and recorded
with the owner-intent compliance evidence described in
`FRAMEWORK-VALIDATION-PROTOCOL.md`.

---

## 5. Cinematic Hero Decision Framework

When a hero treatment is being decided (any motion level, but especially relevant at Level 2–3), Website Director chooses among:

- Static editorial hero
- Cinematic photographic hero
- Background video hero
- Scroll-driven canvas hero
- Kinetic typographic hero
- Parallax hero
- Interactive hero
- Product-demonstration hero
- 3D / WebGL hero

Evaluate the same list as §4 (business, audience, desired emotion, content, performance, mobile, accessibility, conversion, technical architecture) before choosing. A scroll-driven canvas hero is a legitimate answer for a design studio and a wrong answer for a plumber, not because canvas heroes are inherently bad, but because the framework, applied honestly, produces different answers for different businesses.

### 5.1 Cinematic render strategy decision

For a scroll-linked hero or Cinematic Journey, record one of the following
strategies in `motion-direction.md` and `cinematic-brief.md`:

| Strategy | Decision rule |
| :--- | :--- |
| `DENSE_KEYFRAME_VIDEO_SCRUB` | Select only when a real-browser run proves dense-keyframe video scrubbing, scroll alignment, ending rest, mobile behavior, reduced motion, and performance within budget. |
| `CANVAS_FRAME_SEQUENCE` | Select when exact frame synchronization or measured browser behavior makes a frame sequence the safer implementation. |

The framework makes no global claim that video or canvas is superior. The
record must name the rejected alternative, the evidence run, the measured
reason, the poster, the mobile fallback, and the complete-without-video path.
The implementation may use Blob loading, `requestAnimationFrame` smoothing,
seek coalescing, delta-gated DOM updates, and compositor isolation when the
selected strategy requires them. These are engineering techniques, not a
creative override.

---

## 6. `MOTION_DIRECTION_LOCKED` — Requirements

Implementation may not begin until motion is explicitly classified and `locks.motion_direction_locked` is `true` in `site-profile.json`. **`locks.motion_direction_locked` is the single, authoritative flag for this gate.** No other field records lock state — see §8.

Even a Level 0 site must go through this gate: recording `MOTION_LEVEL_0` and locking it proves the absence of animation was a deliberate art-direction decision, not an oversight.

The lock covers, and `templates/motion-direction.md` must document:
- Motion level (0–3) and rationale.
- Hero behavior.
- Scroll behavior.
- Section-transition philosophy.
- Hover behavior.
- Selected advanced modules (if any — see `CINEMATIC-INTEGRATION-PROTOCOL.md` for Level 2–3 specialist modules).
- Easing and durations (must resolve to the tokens in `design-system.md` §13, not ad-hoc values).
- Mobile reduction strategy.
- Reduced-motion behavior (§7).
- Performance constraints (§8 of `PRODUCTION-CHECKLIST.md`, extended for Level 2–3 in that document).

---

## 7. Accessibility: `prefers-reduced-motion` Is Mandatory

Every project, regardless of motion level, must implement the `prefers-reduced-motion` reset already specified in `design-system.md` §13. For Level 2–3 projects specifically:
- Where motion communicates information (a scroll-driven reveal sequencing content, a sticky narrative), the reduced-motion fallback must preserve **equivalent meaning** through static layout — never hide content inside an animation state with no static equivalent.
- Keyboard and screen-reader workflows must remain fully intact regardless of motion level; motion must never be the only path to content or navigation.

For Level 2 and Level 3, policy completion additionally requires a named
sequence trace from this direction to its implementation location and a
meaningful `REAL_BROWSER` runtime state change. Source-only animation claims,
GSAP or CSS presence, and static screenshots are not motion evidence.

**This protocol owns the motion *policy*.** `ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md` (Phase 6.9) and the Phase 10.5 reduced-motion assertion **consume** it — they verify that the policy holds (no content trapped behind motion, no meaning only in animation, autoplay > 5s pausable, no strobing), they do not create a competing motion policy. A reduced-motion content-trap detected in Phase 10.5 is the same finding whether reported under `MOTION_SPEC` or `ACCESSIBILITY_REVIEW`.

---

## 8. Source-of-Truth Rule (Motion State)

`site-profile.json` → `motion{}` holds **descriptive execution state only**: `level`, `cinematic_specialist_required`, `cinematic_brief_complete`. It does not contain a lock field. The gate itself — whether motion direction is approved and binding — lives exclusively at `locks.motion_direction_locked`. Never introduce a second boolean (e.g., a `motion.direction_locked`) that could drift out of sync with `locks.motion_direction_locked`. See `SKILL.md` §5 for the full state-authority rule shared with the research gate.
