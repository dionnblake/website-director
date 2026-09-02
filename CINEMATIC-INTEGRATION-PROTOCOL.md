# CINEMATIC INTEGRATION PROTOCOL: BINDING THE SPECIALIST TO THE BRIEF

> **Version:** 1.2.0
> **Status:** Mandatory Operating Standard (V1.1 Extension; V2.15 cinematic production intelligence additive)
> **Rule:** A selected cinematic implementation adapter executes an approved brief. It does not set direction and it never runs by default.

---

## 1. When This Protocol Activates

Run this protocol only when Website Director selects `MOTION_LEVEL_2` or
`MOTION_LEVEL_3` and the project genuinely needs a cinematic journey, a
scroll-linked visual sequence, governed generated media, or a specialist
interaction module. Level 0 and Level 1 projects do not invoke this protocol.
Level 2 or Level 3 alone is not sufficient; standard CSS or GSAP may be the
correct implementation.

**Sequencing:** motion level selected, then this protocol produces
`templates/cinematic-brief.md`, then `motion.cinematic_brief_complete` may be
set to `true`, then `locks.motion_direction_locked` may engage. The motion lock
is never a precondition for writing the brief.

`site-profile.json` keeps the existing descriptive fields
`motion.cinematic_specialist_required` and `motion.cinematic_brief_complete`.
No new state, gate, or owner lock is created.

---

## 2. Authority Boundary

```
WEBSITE DIRECTOR
  business truth, design direction, design system, motion level,
  hero composition, text behavior, modules, fallbacks, and approval rules
                         |
                         | issues binding cinematic-brief.md
                         v
CINEMATIC IMPLEMENTATION ADAPTER
  executes the approved creative contract using the selected stack and tools
                         |
                         v
ASSET_GENERATION_PROVIDER or local asset workflow, when explicitly approved
```

The adapter adapts to Website Director. If the rendered build uses the wrong
type, composition, typography, palette, timing, or module, that is an
implementation defect. A tool or model cannot override the locked brief.

The workflow is model and provider neutral. Conceptual roles are
`RESEARCH_AGENT`, `BUILDER_AGENT`, `CRITIC_AGENT`,
`ASSET_GENERATION_PROVIDER`, and `DEPLOYMENT_PROVIDER`. Any capable model may
fill a role. No named model, generation vendor, or hosting vendor is a
required architecture dependency.

---

## 3. Cinematic Render Strategy

Website Director must choose a render strategy for every scroll-linked hero or
journey. Neither option is globally superior.

| Strategy | Use when | Required proof |
| :--- | :--- | :--- |
| `DENSE_KEYFRAME_VIDEO_SCRUB` | A compact video provides the right visual behavior and the browser can scrub it without visible drift or unacceptable decode cost. | Real-browser evidence for poster load, seek response, scroll-motion alignment, ending rest, reduced motion, mobile fallback, and performance. |
| `CANVAS_FRAME_SEQUENCE` | Exact frame synchronization, deterministic art direction, or measured browser performance makes decoded frames the safer choice. | Real-browser evidence for frame loading, memory/performance budget, scroll alignment, mobile fallback, reduced motion, and teardown. |

`DENSE_KEYFRAME_VIDEO_SCRUB` is not a loophole for ordinary compressed video.
It requires dense keyframe encoding, short GOP settings, Blob loading, a
`requestAnimationFrame` smoothing loop with delta-time normalization,
seek coalescing, compositor isolation, a poster, and complete-without-video
behavior. A video strategy is rejected when browser evidence shows seek
drift, stutter, runaway memory, or an unreadable text layer.

`CANVAS_FRAME_SEQUENCE` remains available for exact synchronization. It is
rejected when the measured frame count, memory, decode time, or mobile behavior
exceeds the project budget. The chosen strategy, rejected alternative, test
run, and measured reason belong in `cinematic-brief.md` and
`templates/motion-direction.md`.

Shared implementation rules:

- `SCROLL_MOTION_ALIGNMENT` is measured at the start, middle, and settle frame,
  not inferred from source code.
- `SEEK_COALESCING` prevents a backlog of seeks when scroll input outruns the
  decoder.
- `DELTA_GATED_DOM_UPDATES` keeps text and metadata updates off the hot path
  unless their value changed.
- `BLOB_VIDEO_LOADING` avoids an early visible seek against an incomplete
  resource; object URLs are revoked during teardown.
- `STATIC_HERO_DESIGN` and `COMPLETE_WITHOUT_VIDEO` are mandatory fallbacks,
  not emergency copy added after a failure.
- `MOVING_BACKGROUND_LEGIBILITY_AUDIT` and the `FLICK_TEST` judge the worst
  rendered frame, including text over motion, not only a still poster.

---

## 4. Production Intelligence Reconciled Into Existing Authorities

The following extracted intelligence is an execution aid inside existing
Website Director authorities. It is not a competing skill or a new lifecycle.

### 4.1 `CREATIVE_DIRECTOR_LOOP` and `DESIGN_PACKAGE_DISCIPLINE`

Before generation or implementation, the brief records:

1. project truth, audience, conversion job, and owner intent;
2. the single visual thesis and the approved cinematic shot list;
3. the end frame, transition, negative-space composition, and text-safe zones;
4. the selected render strategy, asset plan, fallbacks, and cost preflight;
5. segment-level approval and the rendered evidence plan.

This is the `DESIGN_PACKAGE_DISCIPLINE` boundary. A loose prompt or a gallery
link is not a production package.

### 4.2 `CINEMATIC_SHOT_LAWS`

Every shot or segment records these laws where applicable:

- `PLAN_END_FRAME_FIRST`: define the settled destination before designing the
  transition into it;
- `NEGATIVE_SPACE_COMPOSITION`: preserve a deliberate text-safe and
  comprehension-safe region;
- `BOUNDARY_CROSSING_REALISM`: use a meaningful foreground, edge, or material
  crossing only when the subject supports it;
- `CHAINED_JOURNEY_METHOD`: connect segments through a physical or visual seam
  rather than unrelated clips;
- `SEAM_LAW`: every cut, blend, or transition has a declared continuity reason;
- `ENDING_REST_MEASUREMENT`: the last frame holds long enough to read and
  understand the next action;
- no text, logo, or claim is delegated to generated footage when it belongs in
  the semantic DOM.

### 4.3 Cost and approval discipline

`SHOT_COST_PREFLIGHT` happens before any paid generation or expensive render.
Use a `CHEAP_GATE_BEFORE_EXPENSIVE_GENERATION`: validate composition, prompt
structure, frame safety, and the static fallback with low-cost local or
synthetic checks first. `SEGMENT_LEVEL_VIDEO_APPROVAL` is required before a
segment enters the production build. A rejected segment is not silently
stitched into the final journey.

`FFMPEG_SCRUB_RECIPES` may be used in a disposable raw/review workspace for
dense-keyframe encoding, poster/end-frame extraction, tail trimming, and
review assembly. `TAIL_TRIM_BEFORE_REROLL` is the default repair for unwanted
trailing motion when the core shot is sound. Raw intermediates do not enter the
deployment asset directory without independent Asset Director approval.

`CINEMATIC_FAILURE_KNOWLEDGE` is recorded as a repair decision: resource
loading, keyframe density, timing, legibility, mobile fallback, or browser
environment. A failed provider call is not treated as evidence of a successful
render.

---

## 5. The `cinematic-brief.md` Contract

Website Director generates the brief before implementation. It records the
project, positioning, motion level, hero subject and action, environment,
camera language, lighting, color grade, scroll relationship, text behavior,
transition philosophy, approved and prohibited modules, production
intelligence decisions, render strategy, asset requirements, performance
budget, mobile and reduced-motion fallbacks, source provenance, segment
approval, and owner approval points.

The implementation adapter stops when the brief is incomplete. It does not
fill a creative gap with a house style, force a framework because a reference
used it, or treat a source image, prompt, or video as licensed by observation.

---

## 6. Cost Boundary and Provider Neutrality

Paid generation, asset services, browser infrastructure, or deployment
services may be considered only after the exact operation, expected cost,
owner authorization, and fallback have been recorded. Website Director never
pre-authorizes a paid operation on the owner's behalf.

Before a paid operation:

1. identify the selected provider adapter and operation;
2. state the approximate cost and the number of segments or attempts;
3. obtain explicit owner authorization;
4. keep credentials in secure environment configuration only;
5. record the resulting asset identity, provenance, rights status, and hash.

No provider account, model, deployment host, or credential is required by this
protocol. An unavailable provider remains `BLOCKED`; it is not replaced by a
fabricated success.

---

## 7. Module Selection Stays With Website Director

Website Director selects cinematic modules, informed by research but not
dictated by a library or reference site. The brief lists approved and
prohibited modules with a one-line reason tied to the client's story.

External references provide transferable principles only. A reference cannot
set the hero composition, design tokens, locked copy, accessibility policy,
conversion decision, or production asset inventory. Owner-selected references
may become dimensional Reference Bars when the Gauntlet assigns a specific
dimension and records `REFERENCE_ONLY` provenance.

---

## 8. Fallbacks and Accessibility Are Non-Negotiable

Every cinematic build specifies:

- a poster or `STATIC_HERO_DESIGN` for the initial and failed-media state;
- a mobile/constrained-network fallback;
- a reduced-motion equivalent that preserves meaning;
- a complete-without-video path that keeps semantic text, navigation, CTA,
  and content available;
- worst-frame contrast and `FLICK_TEST` evidence for moving backgrounds;
- teardown for animation loops, object URLs, listeners, and decoded resources.

`prefers-reduced-motion` never hides content while waiting for a cinematic
sequence. Browser QA verifies the runtime behavior, Accessibility owns the
accessibility requirements, and the Gauntlet judges the rendered experience.

---

## 9. State

`site-profile.json` → `motion.cinematic_specialist_required` and
`motion.cinematic_brief_complete` remain the only cinematic descriptive state.
Neither is a lock. `locks.motion_direction_locked` remains the single
authoritative motion lock, and the existing five-lock invariant is unchanged.
Rendered screenshot receipts belong to the Browser QA evidence manifest and
Gauntlet review artifact, not to a second cinematic completion flag.
