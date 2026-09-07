# Owner change request — Alpha Starts Now motion contract

**Status: `MOTION_CHANGE_REQUEST = PREPARED_NOT_APPROVED`.**
Nothing in this file has been applied. No choreography was implemented, no locked artifact was
edited, no approval was recorded, and `approved_downgrade` was not set.

| Field | Value |
|---|---|
| Project | `alpha-starts-now-visual-first-production` |
| Requested by | Website Director candidate repair (bounded) |
| Decision owner | Project owner |
| Owner requirement at issue | `motion.owner-cinematic` — `MOTION_LEVEL_3`, `required_sequences: true` |
| Conflicting project text | `VISUAL-CONTRACT.md` § *Motion contract* |
| Existing approval state | `OWNER_FINAL_ACCEPTANCE = PENDING`, `PRODUCTION_CERTIFICATION = NOT_GRANTED` |

---

## 1. The decision being asked for

The owner's standing contract requires cinematic, animation-heavy, sequence-driven motion at
`MOTION_LEVEL_3`. The project-local `VISUAL-CONTRACT.md` § *Motion contract* instead states that
motion is limited to transform/opacity reveals. No approved downgrade exists — the resolver returns
`approved_downgrade: false` against the real contract.

**The owner is asked to choose one of two things, not to approve this proposal by default:**

- **A — raise the build to the standing requirement.** Approve the four sequences in §3, which are
  scoped to what the demonstrated gap requires and nothing more.
- **B — formally approve a downgrade.** Record a genuine, scope-correct owner downgrade record for
  `motion.owner-cinematic`. This is a real option; it is simply not the current state, and it cannot
  be created by a builder, a critic, or this request.

This request exists because option B was taken *in effect* without ever being taken *explicitly*.

### What is not in dispute

The sentence *"no animation is required to understand the content"* is correct and stays. Semantic
completeness and reduced-motion accessibility are requirements, not concessions. The conflict is
narrower: the **normal-motion** experience was limited to one generic reveal while the contract
promised cinematic sequences.

### What this request does not touch

Visual direction, business, audience, offer, copy, typography, layout, navigation, imagery,
accessibility, and the usable static / reduced-motion version are all preserved exactly. No font
selector, media vendor, animation library, motion framework, gallery search, or paid generation is
proposed or required.

---

## 2. The measured gap this addresses

Real-browser reassessment of an unchanged isolated copy of the current build (candidate harness,
Chrome 152, homepage at 1440 and 390):

| Measurement | Desktop 1440 | Mobile 390 | Reduced motion |
|---|---|---|---|
| Response of the `.reveal` sweep | opacity Δ 0.845, geometry Δ 15.2 px, transform changed | **no response** (`changed_properties: []`) | no response *(correct)* |
| Distinct **proven** motion families | **0 of 1** | 0 of 1 | n/a |
| Named sequences in the project motion brief | **0** | 0 | n/a |
| `motion.generic-fade-diversity` | **FAIL** | FAIL | not applicable |
| Owner requirement `motion.owner-cinematic` | **BLOCKED_WITH_EXPLANATION** | — | — |

The reveal is real: a 18 px translate plus opacity over 550 ms, applied to 32 nodes. It is one
pattern used 32 times, and on mobile it had already settled before the sweep. That is the gap —
not an absence of motion, but an absence of *sequence identity*.

---

## 3. Proposed sequences

Four sequences. Each names its own target region, so each can be verified — and can fail — on its
own. Selectors below are the build's current classes; none is invented.

### 3.1 `hero-route-ignition`

| | |
|---|---|
| **Business / narrative purpose** | The yellow route is the brand's progression device. The homepage should open by *starting* the route, not by fading a headline in. This is the entry event for "Alpha starts now". |
| **Region / selectors** | `.hero` — `.hero-rail`, `.hero-line`, `.hero-title`, `.hero-kicker` |
| **Trigger** | Page load (once), after fonts are ready |
| **Start** | `.hero-rail` at zero drawn length; `.hero-title` lines masked from below |
| **Change** | Rail draws downward; title lines unmask line-by-line on a short stagger; `.hero-kicker` settles last |
| **Settle** | Rail at full length, title fully unmasked, no residual transform — identical to today's static hero |
| **Family** | `ROUTE_DRAW` |
| **Mobile ≤767 px** | Same sequence, shorter travel and stagger; no pinning |
| **Reduced motion** | Settled state rendered immediately — byte-for-byte today's hero |
| **Assets** | None. Existing `.hero-rail` and type. |

### 3.2 `route-map-progression`

| | |
|---|---|
| **Business / narrative purpose** | The approved reference's transferable principle is the yellow route as a *progression device* connecting stage → ritual → threshold → CTA. Today that route is a static graphic. This makes it advance as the reader advances. |
| **Region / selectors** | `.path-section` — `.route-map`, `.route-map-svg`, `.route-svg`, `.path-stage`, `.path-stage-label` |
| **Trigger** | Scroll position within the section |
| **Start** | Route stroke at 0 % `stroke-dashoffset`; stage labels at rest weight |
| **Change** | While the section holds the viewport, the stroke advances with scroll progress and each `.path-stage` takes emphasis as the route reaches it |
| **Settle** | Route fully drawn, final stage emphasised, section releases |
| **Family** | `PINNED_SCRUB` |
| **Mobile ≤767 px** | No pinning. The route advances with normal scroll; stages emphasise on entry |
| **Reduced motion** | Route rendered fully drawn, all stages at final weight, no pin |
| **Assets** | None. The `.route-svg` path already exists. |

### 3.3 `ritual-plate-parallax`

| | |
|---|---|
| **Business / narrative purpose** | Five rituals currently share one uniform fade, so they read as a list rather than a sequence. Differential reveal gives each ritual its own moment and carries the tactile field-manual grammar of the approved reference. |
| **Region / selectors** | `.rituals-section` — `.ritual-row`, `.ritual-image`, `.ritual-node`, `.ritual-copy`, `.plate-label` |
| **Trigger** | Each `.ritual-row` entering the viewport |
| **Start** | `.ritual-image` masked to a horizontal band; copy offset below its rest position |
| **Change** | Mask opens across the plate while `.ritual-copy` rises at a different rate; `.ritual-node` marks the row on the route |
| **Settle** | Mask fully open, copy at rest — today's rendered layout exactly |
| **Family** | `PARALLAX_MASK` |
| **Mobile ≤767 px** | Mask opens; differential travel reduced to a single rate |
| **Reduced motion** | Plates and copy at settled state on load |
| **Assets** | **None new.** Uses the five existing ritual plates. See the open provenance item in §6. |

### 3.4 `threshold-commit`

| | |
|---|---|
| **Business / narrative purpose** | The route should terminate in the conversion, not merely stop near it. The primary CTA is where the progression device pays off. |
| **Region / selectors** | `.join-section` — `.join-copy`, `.join-form-wrap`, `.primary-cta` |
| **Trigger** | `.join-section` entering the viewport |
| **Start** | Route segment short of the CTA; form panel offset |
| **Change** | Route segment extends to meet the CTA; panel settles into place |
| **Settle** | Route meets the CTA; CTA at rest and immediately operable throughout |
| **Family** | `THRESHOLD_LANDING` |
| **Mobile ≤767 px** | Same, shorter travel |
| **Reduced motion** | Settled state on load |
| **Assets** | None. |

**Distinct families proposed: 4** (`ROUTE_DRAW`, `PINNED_SCRUB`, `PARALLAX_MASK`,
`THRESHOLD_LANDING`). Four is what the four regions need; it is not a quota. Motion *craft* remains
the existing Gauntlet's judgement — the checks in §5 verify that the promised behaviour happens, not
that it is good.

---

## 4. Cost and dependency implications

| Item | Implication |
|---|---|
| New imagery or generation | **None.** Every sequence uses existing approved assets. |
| New vendor, model, or animation library | **None required.** CSS transitions/animations plus the site's existing vanilla `site.js` module are sufficient; scroll-driven behaviour has a documented JS fallback path. No named library is a dependency of this request. |
| New framework, critic, runner, gate, or lock | **None.** Verification uses the existing browser-QA runner and assertion catalogue. |
| Build size | One additional module in the existing `site/scripts/site.js`; no new network request. |
| Accessibility | Neutral by construction — every settled state equals today's rendered page, and the reduced-motion path is unchanged. |
| Performance | Transform/opacity/clip-path only; no layout-thrashing properties. LCP element (hero) is not gated behind the sequence. |
| Effort | Four scoped sequences in existing regions. No restyle, no re-layout, no copy change. |

---

## 5. Evidence required before this can be called done

If the owner approves option A, completion requires all of the following, produced by the existing
runner — not by declaration:

1. A motion brief naming exactly these four `sequence_id`s, so the promise is auditable.
2. Real-browser runtime observation per sequence at 1440 and 390, each reaching its declared
   `START` / `CHANGE` / `SETTLE` states, with `family_source: DECLARED`.
3. `motion.sequence-behavior` PASS for **every** sequence — one working sequence does not carry the
   others.
4. `motion.runtime-state-change` PASS and `motion.generic-fade-diversity` PASS with at least one
   proven non-generic family.
5. Reduced-motion counterparts at both viewports confirming the usable static equivalent, with
   `motion.reduced-content-visible` and `motion.reduced-nav-operable` still PASS.
6. Full-homepage captures (`DESKTOP_FULL_HOMEPAGE`, `MOBILE_FULL_HOMEPAGE`) at the reviewed build
   identity, with receipts resolved on disk and digests recomputed.
7. Owner review of those captures, bound to that exact artifact set.

---

## 6. Deliberately left open

| Item | Why it stays open |
|---|---|
| **Palette / brand ruling** | The brand check now runs and reports `UNAPPROVED_DOMINANT_BRAND_HUE` for the cream field. A breach is **NOT_VERIFIED**: area-weighted measurement shows navy dominant and cream plausibly a permitted supporting neutral. This needs an owner ruling, not a code change, and the validator must not be tuned to force a pass. |
| **Ritual-plate provenance** | Five plates still lack provenance records (`ASSET_PROVENANCE: PARTIAL`). Loading correctly and being cleared for use are different facts. This request adds no new imagery and does not resolve it. |
| **`VISUAL-CONTRACT.md` § Motion contract** | Left untouched. Whichever option the owner chooses, editing that section is an owner action taken after this decision — not part of this request. |

---

## 7. If approved — the exact next actions (not performed)

1. Owner records the decision through the existing owner event path (option A or option B).
2. If **A**: the four sequence ids are added to the project's motion brief, `VISUAL-CONTRACT.md`
   § *Motion contract* is updated by the owner to match, implementation proceeds, and §5 evidence is
   produced.
3. If **B**: a genuine downgrade record is created naming the owner as approving actor, citing the
   owner event, and scoped to `ALPHA_STARTS_NOW_CURRENT_CANDIDATE`. The repaired resolver accepts
   only such a record; it rejects an unsigned, unscoped, or critic-authored one.
4. Either way, `OWNER_FINAL_ACCEPTANCE` and `PRODUCTION_CERTIFICATION` remain owner decisions that
   this request does not touch.
