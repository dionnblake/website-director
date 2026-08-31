# ACCESSIBILITY INTELLIGENCE & WCAG 2.2 AA VERIFICATION PROTOCOL

> **Version:** 1.0.0 (Website Director V2.9.0 Subsystem)
> **Status:** Mandatory — pre-build accessibility specification (Phase 6.9) and post-build verification (Phase 10.5 + Phase 12)
> **Governance:** Website Director Orchestration Rail (`SKILL.md` §2)
> **Readiness Gate:** `[ACCESSIBILITY_READY]` — a readiness gate, **not** a sixth owner/design lock.
> **Design/verification target:** `WCAG 2.2 Level AA` for applicable public production websites. This is a **technical** target. Website Director never claims legal accessibility compliance or ADA conformance from automated testing.

---

## 1. Why this exists — one authority for scattered rules

Accessibility requirements already live in many places: `PRODUCTION-CHECKLIST.md` §3, `QA-RUBRIC.md` category 10 and §5.x, `WEBSITE-GAUNTLET-PROTOCOL.md` §4.7 Accessibility Critic, `IMPECCABLE-ENGINE-PROTOCOL.md` §3.1 (`low-contrast`, `gray-on-color`, `touch-target-undersized`) and §4.3, `BROWSER-REGRESSION-QA-PROTOCOL.md` §16 keyboard smoke and §15 reduced motion, `SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md` consent-UI accessibility, `DESIGN-SYSTEM-PROTOCOL.md` §14, `MOTION-DIRECTION-PROTOCOL.md` §7, and the UI/UX Pro Max UX guidelines.

This protocol is the single canonical authority that **reconciles** those, not a parallel system:

```
DERIVES REQUIREMENTS  →  INFORMS DESIGN  →  BINDS IMPLEMENTATION  →  PROVIDES AUTOMATED TEST REQUIREMENTS
    →  PROVIDES MANUAL TEST REQUIREMENTS  →  COLLECTS EVIDENCE  →  DISTINGUISHES VERIFIED / PARTIAL / BLOCKED
```

- Deterministic contrast **math** stays owned by Impeccable (`IMPECCABLE-ENGINE-PROTOCOL.md`). This protocol *consumes* it.
- Runtime browser-observable accessibility checks are **executed** by the V2.8 `browser-qa/` harness (one runner, one evidence system, one frozen-project guard). This protocol adds assertions and a manifest; it creates **no** second runner and **no** second post-build state machine.
- The Gauntlet **Accessibility Critic** (§4.7) is preserved and enriched — no new critic.
- Motion policy stays owned by `MOTION-DIRECTION-PROTOCOL.md`; consent-requirement determination stays owned by `SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md`.

---

## 2. Two states, kept explicitly separate

| State | Meaning |
| :--- | :--- |
| **Pre-build specification** (Phase 6.9) | The accessibility requirements for *this* project are derived from its real functionality, translated into design-token and implementation requirements, and an automated + manual test plan is written. Ends at `[ACCESSIBILITY_READY]` / `accessibility.complete = true`. |
| **Post-build verification** (Phase 10.5 + Phase 12) | Automated checks run in the V2.8 harness; the bounded manual smoke protocol (§30) is executed; evidence is collected; each criterion is classified `AUTO_VERIFIED` / `MANUAL_VERIFIED` / `BLOCKED` / `NOT_APPLICABLE` / `KNOWN_GAP`. |

`accessibility.complete` is the **sole** readiness field for `[ACCESSIBILITY_READY]`. It means the *specification* is complete enough to implement. **It does not mean the implementation passed accessibility testing.**

---

## 3. Phase placement & the gate

```
PHASE 6.5  CONVERSION & ANALYTICS INTELLIGENCE      ──► [CONVERSION_MEASUREMENT_COMPLETE]
   ↓
PHASE 6.75 SECURITY, PRIVACY & COMPLIANCE           ──► [SECURITY_PRIVACY_READY]
   ↓
PHASE 6.9  ACCESSIBILITY INTELLIGENCE               ──► GATE ACCESSIBILITY: [ACCESSIBILITY_READY]
   ↓
PHASE 7    DESIGN SYSTEM TOKEN ARCHITECTURE         ──► Lock 4: [DESIGN_SYSTEM_LOCKED]
   ...
PHASE 10   BUILD
   ↓
PHASE 10.5 BROWSER & REGRESSION QA (+ accessibility assertions)  ──► [BROWSER_QA_PASS]
   ↓
PHASE 12   PRODUCTION PRE-FLIGHT (accessibility classification §36)
```

- **Precondition for Phase 6.9:** `locks.content_structure_locked` is `true`, and Phase 6.5 + 6.75 have produced their state. Accessibility obligations derive from locked IA/content and real data flows — never from a template.
- **`[ACCESSIBILITY_READY]` is a readiness gate, NOT a sixth owner/design lock.** Exactly **five** owner locks remain immutable. `accessibility{}` contains no lock boolean.
- Accessibility requirements **must inform** the design system (§34) before Lock 4 engages.

---

## 4. Canonical state — `site-profile.json` → `accessibility{}`

```json
"accessibility": {
  "complete": false,
  "target": "WCAG_2_2_AA",
  "mode": "STANDARD",
  "requirements_defined": false,
  "component_inventory_complete": false,
  "automated_test_plan_ready": false,
  "manual_test_plan_ready": false,
  "screen_reader_review_required": true,
  "keyboard_review_required": true,
  "contrast_review_required": true,
  "reflow_review_required": true,
  "text_spacing_review_required": true,
  "target_size_review_required": true,
  "reduced_motion_dependency": true,
  "authentication_accessibility_required": false,
  "media_accessibility_required": false,
  "automated_engine": null,
  "automated_verified": false,
  "manual_verified": false,
  "screen_reader_verified": false,
  "production_verified": false,
  "known_gaps": [],
  "blocked_reason": null,
  "exception": { "applied": false, "reason": null }
}
```

- `accessibility.mode` values: `"not_evaluated"`, `"planning"`, `"STANDARD"`, `"blocked"`, `"exception"`, `"not_required"`.
- `accessibility.target` values: `"WCAG_2_2_AA"` (default), `"WCAG_2_1_AA"` (grandfathered projects only), or a documented project-specific target.
- **Four permanently distinct states** (§5): `requirements_defined` → `automated_verified` → `manual_verified` → `production_verified`. Setting a later one never implies an earlier one.
- `screen_reader_verified` is separate from `manual_verified`: manual keyboard/zoom review can pass while screen-reader review is `BLOCKED` (§30).
- Single source of truth: `accessibility.complete` — see `SKILL.md` §5.16. No second, independently-writable completion flag. `[ACCESSIBILITY_READY]` is a readiness gate and is **not a sixth owner or design lock** — exactly five owner locks remain immutable, and `accessibility{}` holds no lock boolean.

---

## 5. No false conformance claims

These are **not interchangeable**:

```
ACCESSIBILITY_REQUIREMENTS_DEFINED   ≠   AUTOMATED_CHECKS_PASS   ≠   MANUAL_CHECKS_PASS   ≠   PRODUCTION_VERIFIED
```

**Prohibited** unless the defined verification scope has genuinely been completed *and* the wording accurately reflects the evidence:

```
ADA COMPLIANT · FULLY ACCESSIBLE · ACCESSIBILITY GUARANTEED · WCAG COMPLIANT · SECTION 508 COMPLIANT · EN 301 549 COMPLIANT
```

**Permitted, evidence-based** statements:

```
WCAG 2.2 AA TARGET TESTS PASSED          (automated + defined manual scope executed and passed)
KNOWN ACCESSIBILITY GAPS = NONE OBSERVED
MANUAL REVIEW COMPLETED                  (with the manual scope enumerated)
AUTOMATED ACCESSIBILITY CHECKS PASSED    (engine + version recorded)
SCREEN-READER SMOKE COMPLETED / BLOCKED_SCREEN_READER_ENVIRONMENT
```

Website Director never implies legal certification. `accessibility.production_verified` requires owner-supplied evidence from the deployed production surface.

---

## 6. Accessibility requirement inventory (derive from real functionality)

Inspect the locked IA, content plan, page-experience brief, measurement plan, security/privacy review, asset manifest, immersive/rive briefs, and motion direction. Build the **Applicable Component Inventory** covering only what the project actually contains:

routes · navigation · forms · dialogs · drawers · menus · carousels · tabs · accordions · tables · data visualizations · authentication · payment · consent interfaces · video/audio · images · interactive SVG · Rive · Three.js · route transitions · drag/drop · uploads · custom controls · notifications · errors · live updates.

**Do not impose component requirements a project does not have.** A static brochure site does not inherit dialog, drag, authentication, or media criteria.

---

## 7. Semantic structure

Specify and verify: landmark structure (`<header>`, `<nav>`, `<main>`, `<footer>`, complementary regions where appropriate); one meaningful primary page heading where appropriate; logical heading hierarchy with no skipped levels; lists as lists; tables as tables; buttons for actions; links for navigation; **native controls preferred over reconstructed ARIA widgets**.

> **No ARIA is better than bad ARIA.** Do not add ARIA where native semantics already provide the correct role, state, and keyboard behaviour. Redundant or conflicting ARIA is a defect.

---

## 8. Accessible name / role / value

Every interactive control exposes an appropriate **name**, **role**, and **value/state**. Verify where applicable: icon-only buttons, menu buttons, toggles, tabs, sliders, dialogs, custom selects, disclosure controls, Rive-powered controls, and canvas/WebGL alternatives.

The visible label and the programmatic name must not conflict (WCAG 2.5.3 — the accessible name must contain the visible label text).

---

## 9. Keyboard access (formalises V2.8 §16 keyboard smoke)

All functionality is operable by keyboard where the underlying interaction reasonably supports it. Verify: logical tab order · no keyboard traps · Enter/Space activation · Escape behaviour · arrow-key behaviour for applicable composite widgets · focus return after dialogs · focus movement after route changes where specified · skip navigation · keyboard access to primary conversion actions · menus · forms · drawers · tabs · accordions · consent controls.

> Do **not** require Tab to enter every radio option or tab in a tablist — the correct native pattern uses arrow keys within the group and a single tab stop for the group.

---

## 10. Focus visibility (WCAG 2.2)

Requirements for: a visible focus indicator on every interactive element; sufficient focus indication (area/contrast — WCAG 2.4.13 target); focus not obscured by sticky/fixed UI; dialogs and overlays; sticky headers; cookie/consent banners; mobile drawers; route transitions.

> Do **not** remove the browser focus outline unless an equally or more visible replacement exists (a token `--focus-ring`, `outline`, or `box-shadow` meeting the indicator-contrast requirement).

---

## 11. Focus not obscured (WCAG 2.2 — 2.4.11)

Browser QA detects common failures where technically feasible: a focused control hidden behind a sticky header; a focused element hidden behind a cookie banner; a focused control outside the visible modal region. Cases automation cannot reliably assess are marked `MANUAL_REQUIRED` — **never silently PASS** (§41 scenario D).

---

## 12. Colour contrast (consumes Impeccable; does not duplicate the math)

Deterministic contrast requirements for: normal text (≥ 4.5:1) · large text (≥ 3:1) · UI components and graphical objects where applicable (≥ 3:1, WCAG 1.4.11) · focus indicators (≥ 3:1 against adjacent colours) · disabled-state interpretation · text over images/video/gradients · hover/focus states · colored surfaces (the Impeccable `gray-on-color` rule).

The mathematical logic is `IMPECCABLE-ENGINE-PROTOCOL.md`'s. This protocol requires the check be *run* (statically by Impeccable, at runtime against computed styles by browser QA) and classifies the result.

---

## 13. Colour independence (WCAG 1.4.1)

Meaning must never depend solely on colour. Provide a second perceivable indicator for: form errors · status · selected state · charts · warnings · success · required fields. (Text, icon, pattern, underline, position, or shape.)

---

## 14. Text resizing / reflow (WCAG 1.4.4, 1.4.10)

Verify at 200% text zoom, high browser zoom, and narrow-viewport reflow toward the WCAG expectation of content at **320 CSS px** width without two-dimensional scrolling — except legitimate exceptions (wide data tables, maps, code blocks, complex diagrams).

Verify: no clipped text · no lost controls · no overlapping UI · **no hidden conversion path** · no inaccessible horizontal-scroll requirement for ordinary reading content.

---

## 15. Text spacing (WCAG 1.4.12)

The interface tolerates: line height ≥ 1.5× font size · paragraph spacing ≥ 2× font size · letter spacing ≥ 0.12× · word spacing ≥ 0.16× — with **no loss of content or functionality**. A synthetic browser fixture applies the WCAG text-spacing override and re-checks reflow/clipping.

---

## 16. Target size (WCAG 2.2 — 2.5.8) vs. Website Director's ergonomic preference

Two distinct standards — **keep them distinct**:

| | Size | Nature |
| :--- | :--- | :--- |
| Website Director ergonomic design target | `44 × 44 px` on mobile viewports | Historic design preference (`DESIGN-SYSTEM-PROTOCOL.md` §14, `QA-RUBRIC.md` §1.7) |
| WCAG 2.2 AA minimum criterion (2.5.8) | `24 × 24 px` (with spacing/inline/essential exceptions) | Conformance floor |

Preserve the **stricter** `44 × 44 px` ergonomic standard where already approved, unless a justified, recorded exception applies. Test small **adjacent** targets against both. A control below 24×24 with no exception is a hard FAIL; a control between 24 and 44 is a FAIL against the project's ergonomic requirement unless an exception is recorded.

---

## 17. Dragging movements (WCAG 2.2 — 2.5.7)

**Activate only when drag interactions exist.** Where they do (sortable lists, sliders, canvases, file-drop zones, spatial builders), provide a non-drag alternative unless a genuine WCAG exception applies. A drop zone normally also exposes a keyboard/file-picker path. Do not activate this requirement when there is no drag interaction.

---

## 18. Motion / animation (integrates canonical motion systems — creates no competing policy)

Consumes `MOTION-DIRECTION-PROTOCOL.md`, `GSAP-IMPLEMENTATION-PROTOCOL.md`, `RIVE-INTERACTIVE-MOTION-PROTOCOL.md`, `IMMERSIVE-WEB-PROTOCOL.md`, `PAGE-EXPERIENCE-TRANSITION-PROTOCOL.md`, and `BROWSER-REGRESSION-QA-PROTOCOL.md` §15.

Verify: `prefers-reduced-motion` honoured · content not trapped behind motion · no required meaning exists **only** in animation · motion can be reduced where required · autoplay behaviour appropriate (WCAG 2.2.2 — moving content > 5s is pausable) · flashing/strobing risk prevented (WCAG 2.3.1 — no more than 3 flashes/second) · scroll-linked movement does not make core content inaccessible.

The reduced-motion-content-trap check is the **same** browser-QA assertion as V2.8 §15 — reused, not re-implemented.

---

## 19. Images / non-text content (WCAG 1.1.1)

Meaningful images have meaningful `alt`; decorative images use `alt=""` / `aria-hidden`; complex images (charts, diagrams) carry an extended description or a textual equivalent; logos are usefully named; image links describe destination/purpose.

> Do not keyword-stuff `alt`. **SEO never overrides accessibility** — where `SEO-INTELLIGENCE-PROTOCOL.md` and this protocol conflict on alt text or heading wording, accessibility wins (§38).

---

## 20. Video / audio (WCAG 1.2.x)

**Only where media exists.** Assess: captions · transcript · audio-description requirements · visible controls · keyboard access · autoplay (default off / muted) · mute behaviour · pause/stop ability · reduced-motion implications. Auto-generated captions must be human-reviewed where accuracy matters. Do not require media artifacts for projects with no relevant media.

---

## 21. Forms (integrates Security/Privacy and Conversion measurement)

Formalise: persistent labels · instructions · required-state communication (not colour/`*` alone) · `autocomplete` / input-purpose where appropriate (WCAG 1.3.5) · programmatic error association (`aria-describedby`) · an error summary where appropriate · focus management to the first error · error identification not by colour alone · helpful correction guidance · status announcements (§22) · password rules stated · consent checkboxes · grouped controls with `fieldset`/`legend` where appropriate.

> An accessibility repair must **never** cause a false conversion success. A server-rejected submission still renders no success state and fires no success conversion event (`BROWSER-REGRESSION-QA-PROTOCOL.md` §12, `IMPLEMENTATION-CONTRACT.md` §2.6). Security-owned form safeguards (server-side validation, CSRF) remain unchanged.

---

## 22. Status messages / live regions (WCAG 4.1.3)

For dynamic status changes (form success, form errors, loading completion, cart changes, filtered result counts, async save state) determine when a programmatic announcement is required and choose politeness (`polite` vs `assertive`) intentionally.

> Do not add `aria-live` regions everywhere. An unnecessary live region that announces on every keystroke is a defect.

---

## 23. Modals / dialogs / drawers

Specify: correct role (`dialog` / `alertdialog`) · accessible name · initial focus · focus containment where required · Escape behaviour · a visible close mechanism · focus restoration to the trigger · background-interaction policy (`inert` / `aria-hidden` on the rest) · scroll handling · mobile overflow. Browser QA automates the deterministic portions (role, name, initial focus, Escape, focus return); the rest is manual.

---

## 24. Menus / tabs / accordions

Use established interaction patterns. Verify where applicable: roles only when needed · state attributes (`aria-expanded`, `aria-selected`, `aria-current`) · keyboard behaviour · focus behaviour · expanded/collapsed state · selected state. Prefer native `<details>`/`<summary>` disclosure where it meets requirements.

---

## 25. Tables / data visualization

Where present: header associations (`scope` / `headers`) · captions where needed · real table semantics · a responsive reading strategy that does not break associations · chart text alternatives · colour-independent encoding · accessible labels for interactive charts.

> Do not convert tabular data into `div` grids solely for styling.

---

## 26. Authentication accessibility (WCAG 2.2 — 3.3.8)

**Only where authentication exists.** Do not require users to solve cognitive-function tests (transcription, puzzle CAPTCHA) when an accessible alternative exists. Assess: password-manager compatibility · **paste allowed** into password/OTP fields · one-time-code workflows · CAPTCHA alternatives · recovery flows.

Coordinate with `SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md` — never weaken a security control silently. **If security and accessibility conflict, escalate and resolve explicitly** with an owner decision (§38).

---

## 27. Consent / privacy UI

Consumes `SECURITY-PRIVACY-COMPLIANCE-PROTOCOL.md`. Consent interfaces must be keyboard accessible, screen-reader understandable, visually readable, non-deceptive, operable at zoom/reflow, with reject/accept paths genuinely reachable (same interaction count, comparable prominence).

> **Ownership split:** Security/Privacy owns *whether consent is required*; Accessibility owns *whether the consent interaction is accessible*. This protocol creates no second consent policy.

---

## 28. Error prevention (WCAG 3.3.4) — proportionality

Where submissions are legally or financially consequential (payment, account deletion, binding applications), identify appropriate reversible / checked / confirmed behaviour. Do **not** impose confirmation friction on a newsletter signup or contact form. Apply proportionality.

---

## 29. Responsive / orientation (WCAG 1.3.4)

Assess whether functionality unnecessarily restricts orientation. Where orientation is essential (a piano keyboard, a specific game), document why. Verify accessibility across the canonical V2.8 viewport matrix (`browser-qa/config/viewports.json`).

---

## 30. Screen-reader verification (bounded manual smoke protocol)

Automated checks cannot substitute for screen-reader testing. Run a bounded manual smoke, environment-dependent:

- **NVDA + Chromium/Firefox on Windows**
- **VoiceOver + Safari** where available
- **Orca + Firefox on Linux** where available

Minimum coverage (applicable items only): page title · landmarks · headings · navigation · primary CTA · form (labels, required, error) · error announcement · dialog (name, focus, Escape) · dynamic status · media controls.

> If the environment cannot run a screen reader, record `BLOCKED_SCREEN_READER_ENVIRONMENT` and set `accessibility.screen_reader_verified = false` — **never PASS**. `accessibility.manual_verified` may still be `true` for the keyboard/zoom scope with screen-reader explicitly carved out and named in `known_gaps`.

Record evidence (transcript notes, recording, or a structured checklist) in the project evidence directory.

---

## 31. Automated accessibility engine (implementation engine, not policy)

Inspect for an existing mature engine before inventing rules. `axe-core` is the recommended engine.

- Treat the engine as a **replaceable implementation engine**, not the policy authority (same principle as `BROWSER_QA_ENGINE`).
- Record engine **name and version** in `accessibility.automated_engine` and the evidence manifest.
- Classify violations (`critical` / `serious` / `moderate` / `minor`) and map to WCAG SC.
- **Zero automated violations ≠ WCAG conformance.** Automated tooling covers ~30–40% of WCAG criteria.
- Integrate into `browser-qa/` — the Playwright engine injects axe-core when available (`browser-qa/vendor/axe.min.js`, or the `axe-playwright-python` package); the deterministic `simulation` engine reads declared violations from the fixture.
- If the engine dependency is unavailable, record automated accessibility checks as **`BLOCKED_ACCESSIBILITY_ENGINE_UNAVAILABLE`**, not PASS.

---

## 32. Browser QA integration (extend V2.8 — create no separate runner)

Accessibility assertions are added to `browser-qa/assertions/catalog.py` under the requirement source **`ACCESSIBILITY_REVIEW`**, gated on the plan carrying an `accessibility` block. Browser QA consumes `accessibility{}` and the project accessibility review.

**Machine-verifiable** (subset — the rest is manual): accessibility-engine violations · keyboard-trap heuristics · missing accessible names · focus visibility · focus-not-obscured (feasible cases) · reduced motion · reflow · text spacing · small targets · dialog mechanics (role/name/initial focus/Escape/focus return) · form labels and error association · headings and landmark structure · contrast (computed) · page `lang` and `<title>` · colour-only state heuristics · DOM semantics where objectively measurable.

**Manual-only criteria remain explicitly manual** and appear in the evidence manifest as `MANUAL_REQUIRED`, never auto-PASS.

The V2.8 `FrozenIntegrityGuard` wraps every run. No second post-build state machine.

---

## 33. Working artifacts

- **`templates/accessibility-review.md`** — the 29-section human review (Target · Applicable Component Inventory · Semantic Structure · Names/Roles/Values · Keyboard · Focus · Contrast · Colour Independence · Resize/Reflow · Text Spacing · Target Size · Dragging · Motion · Images · Media · Forms · Dynamic Status · Dialogs/Menus/Tabs · Tables/Visualizations · Authentication · Consent UI · Screen Reader Plan · Automated Testing Plan · Manual Testing Plan · Known Gaps · Exceptions · Implementation Requirements · Production Verification · Evidence).
- **`templates/accessibility-test-manifest.json`** — machine-readable: target, applicable components, per-route accessibility expectations, engine selection, contrast token pairs, target-size requirement, manual scope, screen-reader plan, known gaps, exceptions. Consumed by `browser-qa/runner.py` (merged into or referenced from `browser-qa-manifest.json`).

---

## 34. Design-system integration (accessibility informs tokens before Lock 4)

`DESIGN-SYSTEM-PROTOCOL.md` §14 is enriched (V1.1.0). Before Lock 4, `templates/design-system.md` §14 must specify where applicable: contrast-safe token **pairs** (every foreground/background combination in use, with computed ratio) · focus tokens (`--focus-ring` colour + width + offset, ≥ 3:1) · minimum interactive geometry (the project target-size rule, §16) · error/success semantics that are not colour-only (§13) · disabled-state semantics (perceivable, not a contrast failure to be "excused") · reduced-motion tokens (already `design-system.md` §13) · readable line length (45–75ch body measure) · text-spacing resilience (§15) · state distinctions independent of colour.

This is **not** an alternate design system — it is the accessibility content of the existing §14.

---

## 35. Implementation contract obligations (builders)

`IMPLEMENTATION-CONTRACT.md` §2.8 (V1.6.0) binds builders to, where applicable: native semantic HTML first · accessible names · labels · focus management · keyboard behaviour · state attributes · programmatic error associations · reduced motion · text zoom / reflow tolerance · no inaccessible custom control without written justification · stable browser-QA selectors without test-only UI leakage · **no deleting accessibility tests** · **no suppressing accessibility-engine findings without a documented rationale** in the review §25.

If fixing accessibility requires reopening a locked design decision → **HALT and produce an owner change request** (§38). Never silently violate a lock.

---

## 36. Production checklist (upgrade to WCAG 2.2; classify, don't rubber-stamp)

`PRODUCTION-CHECKLIST.md` §3 is upgraded to the WCAG 2.2 AA target and §5.5 adds full accessibility verification. Every criterion is classified:

```
AUTO_VERIFIED · MANUAL_VERIFIED · BLOCKED · NOT_APPLICABLE · KNOWN_GAP
```

Automatically testable requirements require **machine evidence** (the Phase 10.5 evidence manifest). Manual requirements require **documented human verification**. **Untested criteria are never marked PASS.**

---

## 37. Gauntlet Accessibility Critic (preserved, enriched — no new critic)

`WEBSITE-GAUNTLET-PROTOCOL.md` §4.7 is enriched to consume the canonical accessibility evidence and focus on **experiential** issues deterministic rules miss: cognitively confusing interaction · misleading visual hierarchy · focus flow that is technically valid but practically poor · a difficult reading experience · excessive motion · inaccessible-*feeling* consent UI · poor error clarity. Deterministic defects fail in Phase 10.5 *before* Gauntlet entry where possible.

---

## 38. Accessibility vs. other authorities — explicit precedence

| Conflict | Resolution |
| :--- | :--- |
| **SEO vs. accessibility** | Keyword strategy never overrides meaningful alt text or human-readable headings. Accessibility wins. |
| **Conversion vs. accessibility** | Conversion optimisation never justifies removing labels, obscuring focus, trapping keyboard users, or deceptive interaction. Accessibility wins. |
| **Security vs. accessibility** | Security controls must remain accessible. A CAPTCHA or auth flow that introduces a barrier must be replaced with an accessible security pattern. Genuine conflicts **escalate** to an explicit owner decision — neither is silently degraded. |
| **Visual design vs. accessibility** | A locked visual choice that fails a required accessibility check requires an **owner change request**. Do not quietly degrade accessibility to preserve aesthetics. |

Precedence overall: `OWNER REQUIREMENT > APPROVED LOCK > A11Y / SAFETY > SEO / CONVERSION > AESTHETIC PREFERENCE` — and a lock that conflicts with A11Y produces a change request, it is never silently overridden in either direction.

---

## 39. Exceptions — narrow and evidence-based

An exception may not say `DESIGN PREFERENCE` or `TOO HARD`. It records: the affected criterion (WCAG SC) · the reason · the user impact · the alternatives attempted · the owner decision where appropriate · a remediation plan if deferred. High-impact blockers stay visible in `accessibility.known_gaps` and the production review — never closed silently.

---

## 40. Backward compatibility

Projects without `accessibility{}` remain valid and are not retrofitted. Frozen certification pilots are never reopened by this tooling. Historical accessibility evidence stays historical evidence. New and materially reopened builds use this subsystem. V2.8 Browser QA compatibility is preserved — the accessibility assertions are additive and gated.

---

## 41. Validation scenarios (negative controls)

`tests/test_v2_9_accessibility.py` and `examples/ACCESSIBILITY-INTELLIGENCE-INTEGRATION-VALIDATION.md` prove each safeguard fails:

| # | Scenario | Expected |
| :-- | :--- | :--- |
| A | Icon-only button with no accessible name | **FAIL** |
| B | Text below target contrast | **FAIL** |
| C | Dialog that cannot release focus (keyboard trap) | **FAIL** |
| D | Sticky header covers the focused control | **FAIL**, or `MANUAL_REQUIRED` if the engine cannot objectively establish it — never silent PASS |
| E | Form control with no label | **FAIL** |
| F | Form error not programmatically associated | **FAIL** |
| G | Reduced-motion content trap | **FAIL** (via the existing V2.8 §15 assertion) |
| H | 400% / narrow reflow makes the primary CTA unreachable | **FAIL** |
| I | Text-spacing override clips content | **FAIL** |
| J | Unjustified tiny adjacent targets | **FAIL** against the canonical project requirement |
| K | Colour-only error state | **FAIL** |
| L | Dialog with correct name, focus, Escape, focus return | **PASS** |
| M | Decorative image with correct empty alt / hidden | **PASS** |
| N | Meaningful image missing alt | **FAIL** |
| O | Screen-reader environment unavailable | **BLOCKED**, never PASS |
| P | Engine reports zero violations **but** manual keyboard review fails | overall verification **NOT full PASS** |
| Q | A sixth owner lock is introduced | framework validation **FAIL** |
| R | A frozen pilot is mutated | the V2.8 `FrozenIntegrityGuard` **FAILs** |

---

## 42. Test the tests

Negative-control, against deliberately broken synthetic fixtures, at minimum: missing accessible name · low contrast · keyboard failure · inaccessible form · reflow failure · reduced-motion failure · an invalid full-PASS when manual review is incomplete · frozen-fixture mutation. Asserting that scanners *exist* is insufficient.

---

## 43. Test isolation

All mutable accessibility testing uses the V2.8 isolation rules. No test mutates canonical `projects/`. Reuse `browser-qa/guards/frozen_integrity_guard.py` `FrozenIntegrityGuard` — no competing guard. Frozen-project integrity is required before and after the suite.

---

## 44. No external side effects

No deploy · no production modification · no testing arbitrary external sites · no real form submissions · no personal data transmitted · no customer credentials · no analytics-account changes · no consent-platform changes · no intrusive accessibility tooling against third-party systems · no pushing or merging branches without owner authorisation. Local and synthetic fixtures only.
