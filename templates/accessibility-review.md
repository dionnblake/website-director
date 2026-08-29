# Accessibility Review — [Project Name]

> Authority: `ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md`. Machine form: `accessibility-test-manifest.json`.
> Pre-build specification is filled in **Phase 6.9** (before Lock 4). Post-build verification
> columns are completed in **Phase 10.5** and **Phase 12**.
>
> **Boundary notice:** This review records a **technical WCAG 2.2 AA design/verification target**.
> It is not legal advice and is not a statement of ADA / Section 508 / EN 301 549 conformance.
> Website Director must not write `ADA COMPLIANT`, `FULLY ACCESSIBLE`, `ACCESSIBILITY GUARANTEED`,
> or `WCAG COMPLIANT`. Permitted evidence-based wording: `WCAG 2.2 AA TARGET TESTS PASSED`,
> `KNOWN ACCESSIBILITY GAPS = NONE OBSERVED`, `MANUAL REVIEW COMPLETED`,
> `BLOCKED_SCREEN_READER_ENVIRONMENT`.

Verification classification for every row: `AUTO_VERIFIED` / `MANUAL_VERIFIED` / `BLOCKED` / `NOT_APPLICABLE` / `KNOWN_GAP`.

## 1. Accessibility Target

- Target: `WCAG_2_2_AA` (default) / `WCAG_2_1_AA` (grandfathered) / project-specific: `[…]`
- Mode: `STANDARD` / `blocked` / `exception` / `not_required` — reason: `[…]`
- Legal/jurisdiction note (owner/counsel owns this, not Website Director): `[…]`

## 2. Applicable Component Inventory

Only what this project actually contains (`ACCESSIBILITY-INTELLIGENCE-PROTOCOL.md` §6).

| Component | Present? | Routes | Accessibility pattern to apply |
| :--- | :--- | :--- | :--- |
| Navigation / menus | | | |
| Forms | | | |
| Dialogs / drawers | | | |
| Tabs / accordions / carousels | | | |
| Tables / data viz | | | |
| Authentication | | | |
| Payment | | | |
| Consent interface | | | |
| Video / audio | | | |
| Images / interactive SVG | | | |
| Rive / Three.js | | | |
| Route transitions | | | |
| Drag / drop / uploads | | | |
| Custom controls | | | |
| Notifications / live updates | | | |

## 3. Semantic Structure
- Landmarks (`header`/`nav`/`main`/`footer`/complementary): `[…]`
- Primary page heading + heading hierarchy per route: `[…]`
- Lists as lists, tables as tables, buttons for actions, links for navigation: `[…]`
- "No ARIA better than bad ARIA" — native controls used where they suffice: `[…]`

## 4. Names / Roles / Values
- Icon-only buttons, menu buttons, toggles, tabs, sliders, custom selects, disclosure controls: `[…]`
- Visible label ⊆ accessible name (WCAG 2.5.3): `[…]`
- Canvas / WebGL / Rive control alternatives: `[…]`

## 5. Keyboard Interaction
- Tab order, no traps, Enter/Space, Escape, arrow keys for composite widgets: `[…]`
- Skip navigation; keyboard path to every primary conversion action: `[…]`
- Focus return after dialogs; focus movement after route change where specified: `[…]`

## 6. Focus
- Visible focus indicator on all interactive elements; focus token (`--focus-ring`): `[…]`
- Focus not obscured by sticky header / consent banner / drawer (WCAG 2.4.11): `[…]`
- Focus indicator area/contrast (WCAG 2.4.13): `[…]`

## 7. Contrast (consumes Impeccable contrast math)
- Contrast-safe token pairs (foreground/background, computed ratio): `[…]`
- UI component / graphical object contrast (≥ 3:1): `[…]`
- Text over images / gradients / video; hover & focus states; disabled interpretation: `[…]`

## 8. Colour Independence
- Errors, status, selected state, required fields, charts, warnings/success carry a non-colour indicator: `[…]`

## 9. Resize / Reflow
- 200% text zoom; reflow at 320 CSS px without 2-D scrolling (legitimate exceptions listed): `[…]`
- No clipped text, lost controls, overlap, or hidden conversion path: `[…]`

## 10. Text Spacing
- Tolerates line-height 1.5×, paragraph 2×, letter 0.12×, word 0.16× with no loss (WCAG 1.4.12): `[…]`

## 11. Target Size
- Project ergonomic requirement: `44 × 44 px` (default) / recorded exception: `[…]`
- WCAG 2.2 AA floor `24 × 24 px` (with exceptions) — adjacent small targets tested: `[…]`

## 12. Dragging
- Drag interactions present? If yes, non-drag alternative for each (WCAG 2.5.7): `[…]` / `NOT_APPLICABLE`

## 13. Motion (consumes `MOTION-DIRECTION-PROTOCOL.md` — no competing policy)
- `prefers-reduced-motion`; no meaning only in animation; autoplay > 5s pausable; no >3 flashes/s: `[…]`
- Scroll-linked movement does not block core content: `[…]`

## 14. Images
- Meaningful alt / decorative empty alt / complex-image extended description / image-link purpose: `[…]`
- No keyword-stuffed alt (SEO does not override accessibility): `[…]`

## 15. Media
- Captions / transcript / audio description / controls / keyboard / autoplay-off / pause-stop: `[…]` / `NOT_APPLICABLE`
- Auto-generated captions human-reviewed where accuracy matters: `[…]`

## 16. Forms
- Persistent labels, instructions, required communication, input-purpose autocomplete: `[…]`
- Programmatic error association, error summary, focus-to-first-error, non-colour error id: `[…]`
- Consent checkboxes, grouped controls / fieldset-legend, password rules stated: `[…]`
- An accessibility repair must not cause a false conversion success (`BROWSER-REGRESSION-QA-PROTOCOL.md` §12): `[…]`

## 17. Dynamic Status
- Which status changes need a programmatic announcement; politeness chosen intentionally (WCAG 4.1.3): `[…]`
- No unnecessary `aria-live` regions: `[…]`

## 18. Dialogs / Menus / Tabs
- Dialog role, name, initial focus, containment, Escape, close, focus restoration, background policy: `[…]`
- Menu/tab/accordion roles only when needed; state attributes; native disclosure preferred: `[…]`

## 19. Tables / Visualizations
- Header associations, captions, responsive reading strategy, chart text alternatives, colour-independent encoding: `[…]` / `NOT_APPLICABLE`

## 20. Authentication (WCAG 3.3.8)
- Present? Password-manager compatible; paste allowed into password/OTP; accessible CAPTCHA alternative; recovery flow: `[…]` / `NOT_APPLICABLE`
- Security ↔ accessibility conflicts escalated to an explicit owner decision (never silently degraded): `[…]`

## 21. Consent UI
- Keyboard accessible, screen-reader understandable, readable, non-deceptive, operable at zoom/reflow, reject reachable: `[…]` / `NOT_APPLICABLE`
- (Security/Privacy owns *whether* consent is required; this section owns *whether the interaction is accessible*.)

## 22. Screen Reader Plan
- Environment(s): NVDA+Chromium/Firefox (Windows) / VoiceOver+Safari / Orca+Firefox / `BLOCKED_SCREEN_READER_ENVIRONMENT`
- Minimum coverage: title, landmarks, headings, navigation, primary CTA, form, error, dialog, dynamic status, media controls.

## 23. Automated Testing Plan
- Engine: `axe-core` (recommended) / other — name + version: `[…]` / `BLOCKED_ACCESSIBILITY_ENGINE_UNAVAILABLE`
- Routes, viewports, and states to scan; violation severity classification.
- Note: zero automated violations does not establish WCAG conformance.

## 24. Manual Testing Plan
- Keyboard walkthrough per route; zoom/reflow/text-spacing checks; focus-not-obscured cases; media review; each mapped to a criterion.

## 25. Known Gaps
| WCAG SC | Description | User impact | Severity | Remediation plan / owner |
| :--- | :--- | :--- | :--- | :--- |

## 26. Exceptions
| WCAG SC | Reason (not "design preference" / "too hard") | User impact | Alternatives attempted | Owner decision | Remediation if deferred |
| :--- | :--- | :--- | :--- | :--- | :--- |

## 27. Implementation Requirements
Bullet list handed to the builder (`IMPLEMENTATION-CONTRACT.md` §2.8). Native semantics first; accessible names; labels; focus management; keyboard behaviour; state attributes; error associations; reduced motion; zoom/reflow tolerance; no unjustified custom control; stable QA selectors without test-only UI leakage.

## 28. Production Verification
| Scope | Method | Status | Evidence ref |
| :--- | :--- | :--- | :--- |
| Automated engine | axe-core vX.Y in `browser-qa/` | `AUTO_VERIFIED` / `BLOCKED` | |
| Keyboard | manual walkthrough | `MANUAL_VERIFIED` / `KNOWN_GAP` | |
| Zoom / reflow / text spacing | browser QA + manual | | |
| Screen reader | §22 environment | `MANUAL_VERIFIED` / `BLOCKED_SCREEN_READER_ENVIRONMENT` | |
| Production surface | owner-supplied evidence | `accessibility.production_verified` | |

## 29. Evidence
- Evidence directory: `[<project>/evidence/accessibility]`
- Automated run: `python browser-qa/runner.py --plan <project>/browser-qa-manifest.json --engine playwright --mode regression`
- Manual notes / recordings / screen-reader transcript: `[…]`

---

### Result (site-profile.json → accessibility{})

| Field | Value |
| :--- | :--- |
| `complete` | `false` |
| `target` | `WCAG_2_2_AA` |
| `mode` | `not_evaluated` |
| `requirements_defined` | `false` |
| `automated_test_plan_ready` / `manual_test_plan_ready` | `false` / `false` |
| `automated_engine` | `null` |
| `automated_verified` (post-build) | `false` |
| `manual_verified` (post-build) | `false` |
| `screen_reader_verified` (post-build) | `false` |
| `production_verified` (owner evidence) | `false` |
| `known_gaps` | `[]` |
| `blocked_reason` | `null` |
| `exception.applied` | `false` |
