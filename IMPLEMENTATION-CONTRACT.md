# IMPLEMENTATION CONTRACT: THE DESIGN-TO-CODE GOVERNANCE PROTOCOL

> **Version:** 1.3.0
> **Status:** Legally Binding Execution Standard for Coding Agents
> **Rule:** Separation of Design Authority from Implementation Execution.

---

## 1. The Separation Principle

In the Website Director framework, **Design** and **Implementation** are strictly decoupled phases executed under separate authority regimes:

```
┌────────────────────────────────────────────────────────┐
│                   DESIGN AUTHORITY                     │
│  (Website Director Specification & Token Architecture) │
└───────────────────────────┬────────────────────────────┘
                            │
              5 MANDATORY LOCKS ACHIEVED
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                IMPLEMENTATION AUTHORITY                │
│       (Coding Agent: Pixel-Perfect Translation)        │
└────────────────────────────────────────────────────────┘
```

**The Core Law:** An implementation coding agent is a master builder, NOT a visual designer. The coding agent must never improvise colors, margins, fonts, layouts, or visual motifs on the fly.

---

## 2. The Five Mandatory Design & Motion Locks

Implementation may NOT commence until all five gates in `site-profile.json` → `locks{}` evaluate to `true` and the corresponding artifacts are approved. (`research.complete` must also be `true`, or carry a recorded exception, before Gate 1 — see `VISUAL-RESEARCH-PROTOCOL.md` §4–5 — but it is a readiness precondition, not a sixth lock; see `SKILL.md` §5.2.)

| Lock Name | Source Artifact | Description of Lock Requirement |
| :--- | :--- | :--- |
| **Gate 1: `design_direction_locked`** | `templates/design-direction.md` | Archetype blend, brand posture, visual theme, and mood criteria approved. |
| **Gate 2: `information_architecture_locked`**| `templates/information-architecture.md`| Exact page layout, section sequence, content objectives, and conversion flow approved. |
| **Gate 3: `content_structure_locked`** | `templates/content-plan.md` | Real headlines, proof points, copy hierarchy, and CTA text written and locked. |
| **Gate 4: `design_system_locked`** | `templates/design-system.md` | Complete token mapping (colors, typography, spacing, geometry, components) locked. |
| **Gate 5: `motion_direction_locked`** | `templates/motion-direction.md` | Motion level (0–3), hero/scroll/hover behavior, and reduced-motion/mobile fallbacks approved. If a cinematic specialist was engaged, `templates/cinematic-brief.md` must also be complete. |

---

## 2.1 Builder SEO Requirements (V1.2)

Gates 2 and 3 above are additionally sourced from `templates/keyword-map.md` and `templates/seo-content-briefs.md` once `seo.complete` is `true` (`SEO-INTELLIGENCE-PROTOCOL.md` §6). The coding agent implements, per page, exactly what those artifacts specify:

- Approved page list and routes match `keyword-map.md` §1 — no unapproved pages added, no mapped pages dropped.
- Unique `<title>` and meta description per page, following `seo-content-briefs.md`'s Title/Meta Description Direction — not a forced exact-match string.
- One meaningful `<h1>` per page matching the brief's H1 Direction; heading hierarchy (`h2`–`h4`) follows logically without skipping levels.
- Internal links implemented per `keyword-map.md` §2 (Internal Link Targets).
- Structured data (JSON-LD) implemented only where `seo-content-briefs.md` specifies it as genuinely applicable — never a copy-pasted default schema.
- Canonical tags, XML sitemap, and `robots.txt`/meta-robots directives configured correctly; no accidental `noindex` on a page `keyword-map.md` intends to rank.
- Semantic HTML, crawlable navigation (no critical content gated behind client-side-only rendering that a crawler cannot see), and accessible image `alt` text.

---

## 3. Strict Prohibitions During Implementation

Once all locks are engaged, the coding agent is strictly prohibited from introducing:

1. **Unregistered Colors:** No inline hex codes (`#123456`), RGB values, or ad-hoc Tailwind color utilities (e.g., `bg-indigo-500` if the design token is `--accent-primary`). Every color MUST resolve to a design system variable.
2. **Unregistered Typography:** No ad-hoc font families, arbitrary font sizes (e.g., `text-[27px]`), or unapproved font weights.
3. **Arbitrary Spacing:** No random margins or paddings (e.g., `mt-[37px]`). All spatial values must snap to the 8-point scale (`space-1` through `space-32`).
4. **Improvised Component Styles:** No inventing new card borders, floating decorative badges, random gradients, or glassmorphic backdrops that are not specified in `design-system.md`.
5. **Structural Layout Deviations:** No altering the sequence of sections, skipping proof elements, or turning an asymmetrical split into a generic 3-column card grid.
6. **Unapproved Animation:** No adding random bouncy scroll reveals or uncoordinated hover transforms. No motion beyond what `templates/motion-direction.md` specifies for the locked Motion Level — including on a `MOTION_LEVEL_0` project, where the contract is exactly zero added animation.
7. **Corner Radius Drift:** No mixing `rounded-none`, `rounded-lg`, and `rounded-full` arbitrarily. All geometry must strictly adhere to the token tier.
8. **Independent SEO Strategy:** No creating new pages, meta-title/description strategies, or keyword targets not present in `templates/keyword-map.md` / `templates/seo-content-briefs.md` merely because the coding agent notices search-relevant terms during the build. No exact-match keyword repetition beyond what §2.1's briefs direct. If the coding agent believes the SEO specification itself is wrong, it halts and flags Website Director to reopen `SEO-INTELLIGENCE-PROTOCOL.md` — it does not silently deviate (see `SEO-INTELLIGENCE-PROTOCOL.md` §14).

---

## 4. Change Management Procedure (The Spec-First Rule)

If during the coding phase a technical constraint or unforeseen aesthetic collision occurs:

```
TECHNICAL / DESIGN COLLISION ENCOUNTERED
                    │
                    ▼
          HALT IMPLEMENTATION
                    │
                    ▼
     UPDATE SPECIFICATION ARTIFACT
  (e.g., templates/design-system.md)
                    │
                    ▼
       RE-VERIFY DESIGN LOCKS
                    │
                    ▼
          RESUME IMPLEMENTATION
```

**Never fix a design issue by hacking custom CSS in the component without updating the design system specification first.**

### 4.1 Gauntlet Targeted Repair Governance (V1.3)

During Phase 11.5 (Website Gauntlet Subsystem), when an independent critic identifies `BIGGEST_REMAINING_GAP`:
- The builder agent executes the **smallest safe repair** strictly within locked tokens and layout specifications.
- **No Full-Site Wipes:** Repair only the specific CSS rule, markup structure, or token application identified.
- **Lock Boundary Enforcement:** If resolving the gap is impossible without modifying a locked token, copy string, or motion behavior, the builder is **strictly prohibited from silently making the change**. It must set status to `GAUNTLET_LOCKED_CHANGE_REQUIRED` and generate a formal Change Request for Owner Review.

---

## 5. Implementation Verification Protocol

Before submitting code for review, the coding agent must verify:
- [ ] Every color in the stylesheet maps to a CSS custom property from `design-system.md`.
- [ ] All font sizes and line heights strictly match the mathematical type scale.
- [ ] Every section layout strictly matches the section morphology in `information-architecture.md`.
- [ ] All copy matches the locked copy in `content-plan.md` (no `Lorem Ipsum` or placeholder text).
- [ ] All interactive elements include defined hover, active, and focus states.
- [ ] Mobile responsive views maintain exact design intent without horizontal overflow.
- [ ] Every implemented motion behavior traces to a specific line in `templates/motion-direction.md`; nothing was added because the capability existed.
- [ ] `prefers-reduced-motion` fallback is implemented and preserves equivalent meaning, per `MOTION-DIRECTION-PROTOCOL.md` §7.
- [ ] If a cinematic specialist was engaged, the build matches `templates/cinematic-brief.md` — typography, composition, and module selection were not overridden by the specialist's own creative defaults (see `CINEMATIC-INTEGRATION-PROTOCOL.md` §3).
- [ ] Every page in `templates/keyword-map.md` §1 exists; no unapproved page was added. Full detail: `PRODUCTION-CHECKLIST.md` §5.1.
- [ ] Phase 11.5 Website Gauntlet pass achieved `GAUNTLET_PASS` (or owner-accepted `GAUNTLET_CAP_REACHED` / exception).

