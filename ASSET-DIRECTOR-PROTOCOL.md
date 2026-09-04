# ASSET DIRECTOR PROTOCOL: ART DIRECTION & VISUAL ASSET PRODUCTION SYSTEM

> **Version:** 2.0.0 (Website Director V2.0.0 Core Subsystem)  
> **Status:** Mandatory Art Direction, Visual Asset Strategy & Production Standard  
> **Governance:** Website Director Orchestration Rail (SKILL.md §2, Phase 8.5 & Gate ASSET)  
> **Mission:** Transform web visual assets from miscellaneous files gathered during implementation into a professionally governed, legally verified, visually coherent, and brand-authentic asset ecosystem.

---

## 1. Core Principle & Governance Boundaries

A world-class website cannot be rescued by layout and animation if its visual assets are mediocre, generic, or visually disjointed.

`
┌──────────────────────────────────────────────────────────────────────────┐
│                       THE ASSET DIRECTOR PRINCIPLE                       │
│                                                                          │
│  Visual assets are not decorative filler gathered during implementation. │
│  They are primary carriers of brand authority, cognitive clarity, and    │
│  screenshot memorability. Every asset must be intentional, verified,     │
│  and art-directed.                                                       │
└──────────────────────────────────────────────────────────────────────────┘
`

### What Asset Director OWNS:
- Visual asset strategy and art direction language
- Asset Intent Briefs (ASSET_INTENT_BRIEF) and asset taxonomy mapping
- Sourcing strategy (Owner, Client Photography, Licensed Stock, Custom Generation, SVG/Illustration, 3D, Video)
- Owner-supplied asset classification and authenticity verification
- Visual quality audits, resolution standards, and AI artifact detection
- Hero asset standard and signature visual asset development
- Responsive art direction, text-over-image safety, and focal point preservation
- Performance optimization budgets, modern delivery formats (AVIF, WebP), and master/web separation
- Legal provenance tracking, license verification, and accessibility classification
- Asset Readiness Gate (ASSET_DIRECTION_READY) prior to Phase 10 implementation

### What Asset Director DOES NOT Own:
- Information Architecture (Phase 5 / Gate 2)
- Copywriting and narrative hierarchy (Phase 6 / Gate 3)
- Design token architecture and typography pairing (Phase 7 / Gate 4)
- Motion physics and interaction engineering (Phase 8 / Gate 5)
- Implementation engineering architecture (Phase 9 & 10)
- The Five Owner Design Locks (Locks 1–5 remain immutable)

---

## 2. Asset Director Lifecycle & Two-Stage Activation

Asset Director activates immediately after **[CREATIVE_INTENT_CONFIRMED]** (Phase 1) and becomes deeply engaged through two deterministic stages:

`
                                [CREATIVE_INTENT_CONFIRMED]
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ STAGE A: PROTOTYPE ASSET STRATEGY             │
                    │ - Lightweight asset intent definition         │
                    │ - Synthetic fixtures & prototype placeholders │
                    │ - Labeling of PROTOTYPE_ASSET_LIMITATION      │
                    │ - Zero expensive custom production before lock│
                    └───────────────────────┬───────────────────────┘
                                            │
                                [OWNER DIRECTION SELECTION]
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ STAGE B: SELECTED-DIRECTION PRODUCTION        │
                    │ - Full Asset Intent Brief & Visual Bible      │
                    │ - Authentic owner asset audit & classification│
                    │ - Governed custom generation / shot list      │
                    │ - Master / Web asset production & optimization│
                    │ - Provenance & license verification           │
                    │ - GATE ASSET: [ASSET_DIRECTION_READY]         │
                    └───────────────────────────────────────────────┘
`

### Stage A — Prototype Asset Strategy:
During the Phase 4.5 Visual Prototype Gate, Asset Director provides sufficient visual material for the owner to evaluate competing visual directions. High-cost bespoke asset production (e.g. expensive custom 3D modeling, paid shoots, extensive generation) is strictly deferred. Temporary placeholders are permitted but MUST be visibly labeled PROTOTYPE_ONLY and recorded as PROTOTYPE_ASSET_LIMITATION in isual-prototype-review.md.

### Stage B — Selected-Direction Production:
Once the human owner selects a visual direction and Gate 1 (DESIGN_DIRECTION_LOCKED) engages, Asset Director produces the authoritative asset family for the selected direction prior to Phase 10 implementation.

---

## 3. Creative Ambition Calibration

Asset Director calibrates its art direction requirements directly against CREATIVE_AMBITION:

| Creative Ambition | Asset Requirements & Standards | Stock & Generation Discipline |
| :--- | :--- | :--- |
| **STANDARD** | High-resolution, crisp crops, strong web optimization, consistent color temperature. | Clean stock photography permitted. Avoid complex bespoke pipelines. |
| **PREMIUM** | Bespoke art direction, deliberate color grade profile, custom SVG/textures, signature macro details. | Generic stock rejected. Curated/retouched photography or bespoke 3D/renders. |
| **SHOWCASE** | Primary quality dimension. Exceptional Hero Asset required. Signature Asset mandatory. Visual Bible enforced. | Generic stock fails completely. Bespoke imagery, custom compositing, or governed AI generation. |
| **EXPERIMENTAL** | Non-standard media formats, interactive visual assets, generative media, image sequences. | Provenance, performance, and accessibility remain strict hard gates. |

---

## 4. The Asset Intent Brief (ASSET_INTENT_BRIEF)

Before sourcing or generating any visual asset, an ASSET_INTENT_BRIEF must be established.

`	ext
ASSET_ID = [e.g. hero-hadal-vessel-01]
ASSET_ROLE = [HERO_IMAGE | DETAIL_MACRO | EDITORIAL_IMAGE | ...]
SUBJECT = [Precise description of the primary visual subject]
EMOTIONAL_JOB = [What emotional reaction or cognitive proof this asset must deliver]
COMPOSITION = [Rule of thirds, centered symmetry, dynamic diagonal, split canvas]
CAMERA_PERSPECTIVE = [Eye-level macro, low-angle heroic, isometric technical, 35mm documentary]
FOCAL_POINT = [Coordinates or relative position of primary interest]
NEGATIVE_SPACE_REQUIREMENT = [Required text-safe zone: e.g. Upper-Left 40% clean for H1 overlay]
LIGHTING_LANGUAGE = [Raking grazing light, diffused oceanic luminescence, high-contrast studio rim]
COLOR_TEMPERATURE = [Cool 6500K deep cyan / Warm 3200K tungsten / Milled neutral charcoal]
MATERIAL_LANGUAGE = [Machined Ti-6Al-4V titanium, bead-blasted ceramic, optical quartz]
TEXTURE = [Fine brushed grain, matte anodized, crystalline hydrostatic lattice]
DEPTH = [Shallow depth-of-field f/1.8 macro / Deep infinite hyper-focal sharpness]
MOVEMENT = [Static architectural stillness / Subtle atmospheric particle drift]
BRAND_CONNECTION = [Direct physical proof of hadal engineering capability]
RESPONSIVE_CROP_REQUIREMENT = [Desktop 16:9 -> Tablet 4:3 -> Mobile 9:16 vertical crop centered on focal point]
MOBILE_PRIORITY = [HIGH - focal subject must remain legible at 320px viewport width]
SOURCE_STRATEGY = [OWNER_SUPPLIED | CLIENT_PHOTOGRAPHY | LICENSED_STOCK | GENERATED_IMAGE | ...]
PROVENANCE_REQUIREMENT = [Proprietary brand CAD render / Certified Creative Commons / Generated with seed log]
`

---

## 5. Asset Taxonomy & Roles

Asset Director categorizes assets into explicit functional roles:

1. **Hero Media:** HERO_IMAGE, HERO_VIDEO, HERO_SEQUENCE
2. **Product & Detail:** PRODUCT_IMAGE, DETAIL_MACRO, PRODUCT_RENDER, 3D_RENDER
3. **Editorial & Environment:** EDITORIAL_IMAGE, ENVIRONMENTAL_PHOTOGRAPHY, CASE_STUDY_IMAGE
4. **Human & Proof:** PORTRAIT, FOUNDER_IMAGE, TEAM_IMAGE, SOCIAL_PROOF_ASSET
5. **Brand & Structure:** BACKGROUND_TEXTURE, MATERIAL_TEXTURE, BRAND_GEOMETRY, PATTERN
6. **Information Graphics:** ILLUSTRATION, DIAGRAM, INFOGRAPHIC, SVG_ARTWORK, ICON
7. **Support Media:** POSTER_FRAME, COMMERCE_ASSET, DECORATIVE_MEDIA

### 5.1 Design-first asset intent classification (V2.15 bounded flow)

For the full homepage review and its production handoff, record the intent of
each referenced visual as exactly one of:

- `REQUIRED_ASSET` — the approved design depends on this asset; source,
  rights, accessibility, crop, and provenance must be resolved before release.
- `REFERENCE_INSPIRATION_ONLY` — a research or owner reference used to learn a
  principle; it is not a production asset and must never be promoted or ship
  implicitly.
- `SUPPORTING_MATERIAL` — useful context or optional material that does not
  become factual proof or silently change the approved visual direction.

This classification extends Asset Director's existing taxonomy and provenance
authority. It does not create an asset lock or replace the evidence ledger.

---

## 6. Primary Visual Language & The Generation Bible

### Visual Language Dimensions:
Asset Director defines a coherent PRIMARY_VISUAL_LANGUAGE derived from brand positioning:
- Documentary (Unfiltered, authentic grain, natural light)
- Technical / Architectural (Orthographic, surgical precision, exploded schematics)
- Cinematic Luxury (Moody directional light, rich shadow depth, refined material speculars)
- Minimalist Studio (Pristine isolation, soft gradient wash, tactile material focus)
- Industrial Brutalist (Raw unpolished surfaces, high-contrast monochrome, structural honesty)

### The Generation Bible (GENERATION_BIBLE):
When synthetic or AI-generated media is authorized, all images must share an identical visual DNA:
- SUBJECT_STYLE: Shared physical realism and material integrity
- CAMERA_STYLE: Consistent lens focal length (e.g. 50mm / 85mm prime) and aperture
- LIGHTING_STYLE: Unified key/fill ratio and light source angle across all views
- COLOR_GRADE: Consistent color LUT (e.g. muted cyan shadows with warm specular highlights)
- GRAIN_AND_CONTRAST: Unified film stock or digital sensor profile
- NEGATIVE_SPACE_RULES: Consistent margins for typography integration

---

## 7. Owner Assets First & Authenticity Boundary

### Owner Asset Audit:
Existing authentic client assets (logos, founder portraits, factory/facility photos, genuine product hardware, case study documentation) must ALWAYS be audited before replacement.
- **Classification Taxonomy:** KEEP, RETOUCH, CROP, COLOR_GRADE, UPSCALE, REPLACE, UNUSABLE, PROTOTYPE_ONLY.
- **The Authenticity Rule:** Never replace authentic brand evidence with prettier synthetic/AI media without an explicit strategic justification approved by the owner.

### The Authenticity Boundary:
`
┌──────────────────────────────────────────────────────────────────────────┐
│                       THE AUTHENTICITY INVARIANT                         │
│                                                                          │
│  Synthetic or AI-generated media must NEVER be presented as factual     │
│  documentary evidence.                                                   │
└──────────────────────────────────────────────────────────────────────────┘
`
- **Strictly Prohibited:** Generating fake customer portraits, fake facilities, fake executive teams, fake customer testimonials, or fake clinical/laboratory performance results and presenting them as genuine proof.
- **Taxonomy Enforcement:** Every asset must be classified as either FACTUAL_EVIDENCE_MEDIA (must be 100% authentic) or DECORATIVE_GENERATED_MEDIA (artistic/conceptual illustration).

---

## 8. Quality Audits, AI Artifact Checks & Stock Discipline

### Asset Quality Audit Criteria:
Every production candidate asset must pass the 16-point Quality Audit:
1. RESOLUTION: $\ge 2\times$ display density for target viewport without digital pixelation.
2. FOCUS & SHARPNESS: Crisp optical focus on intended subject without algorithmic over-sharpening halos.
3. COMPRESSION_DAMAGE: Zero visible JPEG blocking, banding, or ringing artifacts.
4. LIGHTING: Natural light falloff matching declared lighting language.
5. COLOR INTEGRITY: Natural skin tones, faithful product color accuracy.
6. COMPOSITION: Deliberate framing adhering to the Intent Brief.
7. SUBJECT_RELEVANCE: Inherent connection to specific brand operations.
8. AUTHENTICITY: Feels genuine and believable within its market tier.
9. BRAND_FIT: Reinforces the five locked brand attributes.
10. CROP_FLEXIBILITY: Allows multi-ratio reflow (16:9, 4:3, 1:1, 9:16).
11. MOBILE_USABILITY: Subject identifiable and impactful at small scale.
12. TEXT_OVERLAY_SAFETY: Certified negative space or contrast safety.
13. PROVENANCE: Clear acquisition trail and source author.
14. LICENSE: Verified commercial web distribution rights.
15. PERFORMANCE_COST: File size within performance budget.
16. VISUAL_DISTINCTIVENESS: Passes the Swap Test against competitors.

### AI Failure & Artifact Detection (AI_ARTIFACT_CHECK):
All generated assets must be inspected for AI failure modes. Reject any asset containing:
- Malformed hands, digits, or unnatural human anatomy
- Nonsense pseudo-text, gibberish lettering, or warped typography
- Impossible architectural geometry or non-Euclidean perspective breaks
- Uncanny, waxy skin textures or dead eyes
- Inconsistent light source directions or missing contact shadows
- Physically impossible machinery, gears, or fluid mechanics

### Stock Photography Discipline:
Generic corporate stock is strictly prohibited. Reject:
- Overly enthusiastic smiling models looking into the camera
- Staged business handshakes, glass whiteboard pointing, or generic meeting rooms
- Cliché generic tech concepts (blue floating wireframe globes, glowing gears)

---

## 9. Hero Asset Standard & Signature Asset System

### Hero Asset Standard (HERO_ASSET_STRENGTH):
The Hero Asset carries the primary visual burden of the website. For PREMIUM and SHOWCASE tiers, the Hero Asset must satisfy:
- **Instant Focal Anchor:** Eye lands on the focal subject within 500ms.
- **Cognitive Thesis Support:** Visually demonstrates the core headline claim.
- **Negative Space Guarantee:** Uncluttered background zone where headline and CTA remain crisp without muddy gradient overlays.
- **Mobile Crop Integrity:** Subject remains intact and powerful when cropped to 9:16 vertical mobile aspect ratio.
- **Screenshot Value:** The hero viewport alone looks like an award-winning portfolio entry.

### Signature Visual Asset (SIGNATURE_ASSET):
For SHOWCASE projects, a Signature Visual Asset is mandatory. It must directly embody the SIGNATURE_ELEMENT declared in the Design Direction (e.g. an interactive 3D exploded view, a high-detail macro cross-section, a bespoke branded sculpture, or a custom dynamic SVG schematic).

### Cinematic production intelligence (V2.15 additive)

When a Cinematic Journey is applicable, Asset Director consumes the existing
`cinematic-brief.md` rather than inventing a media direction. The production
package must declare the shot or segment purpose, `PLAN_END_FRAME_FIRST`,
negative-space and text-safe zones, the transition seam, mobile and
reduced-motion fallback, and the evidence required for approval.

- Run `SHOT_COST_PREFLIGHT` and the `CHEAP_GATE_BEFORE_EXPENSIVE_GENERATION`
  before a paid or high-cost operation.
- Require `SEGMENT_LEVEL_VIDEO_APPROVAL` before any segment enters the selected
  build. Rejected segments remain rejected.
- Keep `FFMPEG_SCRUB_RECIPES`, raw intermediates, and review assemblies outside
  the deployable web asset directory.
- Use `TAIL_TRIM_BEFORE_REROLL` when the core shot is sound but its ending is
  not. Record the repair and new output hash.
- Treat generated media as decorative or conceptual unless its factual status
  is independently supported. Asset identity, source inputs, license, rights,
  and provenance remain mandatory.

No generation provider or model is required by Asset Director. An unavailable
provider is `BLOCKED`, not a reason to fabricate an asset approval.

---

## 10. Photography Shot List (PHOTOGRAPHY_SHOT_LIST.md)

When custom client photography is required or recommended, Asset Director compiles an authoritative shot list for client photographers, containing:
- SHOT_ID: Deterministic identifier
- SUBJECT & ACTION: Exact personnel, hardware, or process to photograph
- COMPOSITION & ORIENTATION: Horizontal (16:9), Vertical (4:5), or Square (1:1)
- LENS & LIGHTING SPEC: Suggested focal length, aperture, and lighting setup
- NEGATIVE SPACE REQUIREMENT: Designated side (left/right/top) for web typography
- WEB USAGE & PRIORITY: Target page section and criticality (P0 Hero, P1 Feature, P2 Supporting)

---

## 11. Responsive Art Direction & Text Safety

### Responsive Multi-Crop Strategy:
Do NOT rely solely on CSS object-fit: cover to solve mobile responsiveness. Asset Director requires deliberate crop specifications and <picture> implementations with explicit mobile variants.

### Text-Over-Image Safety:
Never place text directly over complex photographic detail. Ensure:
- Natural contrast exceeds .5:1$ across the entire text container.
- If contrast is insufficient, utilize a mathematically smooth directional CSS scrim rather than a heavy muddy overlay.

---

## 12. Asset Optimization, Performance & Directory Separation

### Performance Budgets:
- Hero LCP Image: <= 120 KB (AVIF) / <= 180 KB (WebP)
- Supporting Images: <= 80 KB each
- SVG Icons / Graphics: <= 15 KB each (minified and optimized via SVGO)
- Background Video Loops: <= 3 MB (H.264/WebM, <= 8s duration, muted, autoplay, loop, playsinline)

### Deterministic Directory Separation:
`
assets/
├── source/          # High-resolution original master files (uncompressed RAW/TIFF/PNG/SVG) - NEVER OVERWRITTEN
├── working/         # Working design files, multi-layer PSDs, Figma exports, retouched masters
├── web/             # Optimized web-delivery assets (AVIF, WebP, responsive srcset variants)
└── provenance/      # Asset manifests, license certificates, shot lists, and generation seed logs
`

---

## 13. Asset Manifest & Provenance Governance

### Asset Manifest (sset-manifest.json):
Every production asset is indexed in the project manifest with deterministic fields:
- sset_id: Semantic identifier (e.g. hero-titanium-hull-desktop)
- ole: Taxonomy role
- source_type: OWNER_SUPPLIED, CLIENT_PHOTOGRAPHY, LICENSED_STOCK, GENERATED_IMAGE, etc.
- master_path: Relative path to master file in ssets/source/
- web_path: Relative path to delivery file in ssets/web/
- ormat: Delivery format (vif, webp, svg)
- dimensions: Width x Height in pixels
- ile_size_kb: Optimized file size
- license: Explicit license type (proprietary_client, cc_by_4_0, commercial_stock_license, synthetic_generated_internal)
- provenance_ref: Reference in ASSET-PROVENANCE.md
- status: PROTOTYPE_ONLY, PRODUCTION_READY, BLOCKED

### Copyright & Awwwards Boundary:
Reference websites discovered during Phase 3 Visual Research and Phase 3.75 Awwwards Benchmarking are inspiration sources ONLY. Copying photographs, illustrations, videos, 3D models, or brand graphics from external reference websites is strictly prohibited.

---

## 14. Accessibility & Alt-Text Classification

Every visual asset must be assigned an accessibility category:
1. **INFORMATIVE**: Image conveys essential information not present in surrounding copy -> Precise, descriptive lt attribute.
2. **DECORATIVE**: Image provides visual ambiance or mood without unique factual information -> Empty lt=" with ria-hidden= true.
3. **FUNCTIONAL**: Image triggers an interaction (e.g. icon button) -> lt describes the resulting action.
4. **COMPLEX**: Image contains dense data, diagrams, or schematics -> Brief lt summary plus link to full descriptive text or tabular data.

---

## 15. The Asset Readiness Gate ([ASSET_DIRECTION_READY])

Prior to beginning Phase 10 implementation, the project must satisfy the **Asset Readiness Gate**:
- PRIMARY_VISUAL_LANGUAGE is declared and aligned with locked Design Direction.
- HERO_ASSET is certified PRODUCTION_READY (passes HERO_ASSET_STRENGTH).
- SIGNATURE_ASSET is certified PRODUCTION_READY (for SHOWCASE projects).
- Recorded asset provenance is complete for the selected assets, with no
  unresolved UNKNOWN rights records or missing required evidence. This is a
  readiness input, not a legal certification.
- RESPONSIVE_CROP_PLAN is defined for desktop, tablet, and mobile.
- WEB_OPTIMIZATION_PLAN meets Core Web Vitals performance budgets.

> [!IMPORTANT]
> **Readiness Gate Invariant:** [ASSET_DIRECTION_READY] is a quality readiness check, NOT a sixth owner lock. The Five Mandatory Design Locks (Locks 1–5) remain exactly five.

## 16. V2.12 Evidence & Asset Provenance Integration

Asset Director remains the authority for visual asset strategy, generation,
selection, optimization, responsive crops, performance budgets, and visual
readiness. The cross-cutting EVIDENCE-PROVENANCE-PROTOCOL.md owns source
identity, rights evidence, permitted uses, attribution, claim traceability,
and hash identity.

Every production asset in an Asset Director manifest carries provenance_ref
resolving to the same asset record in templates/evidence-ledger.json. An
external, AI-generated, commissioned, third-party brand, font, icon, stock,
quoted, screenshot, or research asset with unresolved high-risk provenance
cannot be marked PRODUCTION_READY. assets.provenance_status remains distinct
from provenance.complete.

Research and showcase imagery remain REFERENCE_ONLY. A matching SHA-256
establishes byte identity only; it does not establish ownership, exclusivity,
copyright, or permitted use. Asset readiness is blocked when the evidence
ledger is blocked or fails.
