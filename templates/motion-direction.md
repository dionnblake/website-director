# MOTION DIRECTION SPECIFICATION: [PROJECT NAME]

> **Date Created:** YYYY-MM-DD
> **Status:** DRAFT | LOCKED (`locks.motion_direction_locked: true`)
> **Stage:** Phase 8 — Motion / Cinematic Direction (after `DESIGN_SYSTEM_LOCKED`)
> **Rule:** Every motion behavior must serve at least one of the Six Motion Justifications, or it is removed.

---

## 1. Selected Motion Level
- **Level:** `MOTION_LEVEL_[0/1/2/3]` — [Name, per `MOTION-DIRECTION-PROTOCOL.md` §2]
- **Rationale:** [Why this level, evaluated against `MOTION-DIRECTION-PROTOCOL.md` §4 — business, audience, content, performance, mobile, accessibility, conversion, technical architecture]
- **Research Input:** [Reference to `research-synthesis.md` §7/§10 if research informed this — or "N/A, research exception applied per `site-profile.json` → research.exception" for bounded/exception projects]

---

## 2. Motion Manifesto
- **Hero Behavior:** [Chosen hero type from `MOTION-DIRECTION-PROTOCOL.md` §5, and its motion treatment]
- **Scroll Behavior:** [Scroll-triggered mechanics, if any]
- **Section-Transition Philosophy:** [How the site moves between sections]
- **Hover Behavior:** [Interaction feedback model]
- **Selected Advanced Modules:** [None, for Level 0–1 — or named modules from `CINEMATIC-INTEGRATION-PROTOCOL.md` §6 for Level 2–3]

---

## 3. Rationale vs. the Six Motion Justifications
1. **Hierarchy:** [How motion directs attention, or "N/A — no motion serves this at Level 0"]
2. **Orientation:** [How motion helps wayfinding]
3. **Storytelling:** [What narrative motion advances]
4. **Feedback:** [What actions motion confirms]
5. **Atmosphere:** [What mood motion establishes]
6. **Brand Expression:** [What signature motion creates]

*Any motion behavior that cannot be justified against at least one of these six is removed before this document is locked.*

---

## 4. Technical Parameters
- **Easing / Durations:** [Must resolve to `design-system.md` §13 tokens — `--transition-fast/normal/smooth` — no ad-hoc values]
- **Mobile Reduction:** [What is simplified or removed on mobile/constrained networks]
- **Reduced-Motion Behavior:** [Static equivalent preserving meaning, per `MOTION-DIRECTION-PROTOCOL.md` §7]
- **Performance Constraints:** [Asset budget, frame count, preload strategy — see `PRODUCTION-CHECKLIST.md` §4]

---

## 5. Cinematic Specialist (only if `motion.cinematic_specialist_required: true`)
- **Specialist Required:** Yes / No
- **`cinematic-brief.md` Status:** DRAFT / COMPLETE
- *If Yes, `motion.cinematic_brief_complete` must be `true` before this document locks — see `CINEMATIC-INTEGRATION-PROTOCOL.md` §8.*

---

## 6. Motion Lock Declaration
- [ ] §1 "Selected Motion Level" names an explicit `MOTION_LEVEL_0/1/2/3` — never left blank or null. A lock with no level selected is invalid regardless of any other field's completeness.
- [ ] Every motion behavior justified against at least one of the Six Motion Justifications (§3).
- [ ] All easing/duration values resolve to `design-system.md` §13 tokens.
- [ ] `prefers-reduced-motion` fallback documented and preserves equivalent meaning.
- [ ] Mobile fallback documented.
- [ ] If a cinematic specialist is required, `cinematic-brief.md` is complete (§5).
- [ ] Ready to lock `motion_direction_locked` in `site-profile.json` → `locks`. (Not `motion.direction_locked` — that field does not exist. See `SKILL.md` §5.)
