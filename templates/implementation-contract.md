# IMPLEMENTATION CONTRACT SPECIFICATION: [PROJECT NAME]

> **Date Generated:** YYYY-MM-DD  
> **Status:** READY FOR CODING | ACTIVE IMPLEMENTATION  
> **Governance Authority:** Website Director V1.1 Specification

---

## 1. Design Lock Verification Matrix

Implementation is strictly blocked until all five locks in `site-profile.json` → `locks{}` evaluate to `LOCKED (true)`:

| Gate | Status | Verified Artifact | Locked Timestamp |
| :--- | :---: | :--- | :--- |
| **`design_direction_locked`** | [LOCKED / PENDING] | `templates/design-direction.md` | [Timestamp] |
| **`information_architecture_locked`** | [LOCKED / PENDING] | `templates/information-architecture.md` | [Timestamp] |
| **`content_structure_locked`** | [LOCKED / PENDING] | `templates/content-plan.md` | [Timestamp] |
| **`design_system_locked`** | [LOCKED / PENDING] | `templates/design-system.md` | [Timestamp] |
| **`motion_direction_locked`** | [LOCKED / PENDING] | `templates/motion-direction.md` (+ `templates/cinematic-brief.md` if `motion.cinematic_specialist_required` is true) | [Timestamp] |

*Precondition (not a sixth lock): `research.complete` was `true` (or carried a recorded exception) before Gate 1 locked — see `SKILL.md` §5.2.*

---

## 2. Technical Stack Constraints
- **Core Markup & Architecture:** [HTML5 / Vanilla CSS / React / Next.js / Astro / Vite]
- **Styling Architecture:** [Pure CSS Custom Properties / Tailwind CSS strictly mapped to token variables]
- **Typography Sourcing:** [Google Fonts CDN / Local WOFF2 fonts]
- **Icons Library:** [Lucide Icons / Heroicons (Single unified stroke weight)]

---

## 3. Code Generation Guardrails for Coding Agent
1. **Zero Aesthetic Improvisation:** You are building strictly to the locked specifications. Do not invent new colors, spacing classes, or card borders.
2. **Exact Variable Mapping:** Use `var(--token-name)` or configured Tailwind aliases for all color, spacing, radius, and font assignments.
3. **No Inline Styling Hacks:** No `style="..."` attributes with custom hex values or magic pixel numbers.
4. **Responsive Reflow:** Adhere strictly to the breakpoint container behavior defined in `design-system.md`.
5. **Zero Motion Improvisation:** Do not invent animation, easing, scroll behavior, or hero motion. Every motion behavior must trace to a specific line in `motion-direction.md` (and `cinematic-brief.md` if a specialist was engaged). A `MOTION_LEVEL_0` lock means zero added animation, not a suggestion.
6. **Change Management:** If an unexpected technical obstacle arises, update `design-system.md` or `motion-direction.md` first before writing code.

## 4. Evidence and asset provenance guardrails

1. Every production claim and production asset must resolve to an
   EVIDENCE_REF or asset provenance reference in the project ledger.
2. Asset Director remains responsible for visual readiness; the cross-cutting
   provenance ledger remains responsible for source identity, rights evidence,
   attribution, permitted use, and hashes.
3. Research references, competitor screenshots, and showcase imagery are
   REFERENCE_ONLY and cannot become production assets.
4. Unknown, stale, contradictory, or high-risk unresolved records block
   production. Prototype exceptions remain PROTOTYPE_ONLY.
5. Do not represent a hash as proof of ownership, exclusivity, copyright, or
   legal compliance.
