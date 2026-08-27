# DESIGN ARCHETYPES SPECIFICATION

> **Version:** 1.1.0
> **Status:** Mandatory Design Catalog & Blending Framework
> **Purpose:** Provide rigorous, pre-calibrated aesthetic foundations to eliminate generic AI guesswork.

---

## 1. Archetype Catalog

---

### 1. Editorial
- **Visual Soul:** Literary, intellectual, bookish, authoritative. Evokes high-end printed journals (*The New Yorker*, *Kinfolk*, *Aperture*).
- **Typography:** Refined transitional or modern serifs (e.g., Newsreader, Cormorant Garamond, Fraunces, Playfair Display) paired with clean geometric or grotesque sans (Inter, DM Sans) for captions and metadata. High contrast type hierarchy, strict leading (line-height).
- **Spacing:** Generous, rhythmic vertical margins, wide column gutters, deliberate whitespace framing long-form thought.
- **Geometry:** Traditional rectangular framing, delicate hairline separators (`1px solid var(--border)`), minimal to zero border-radius (`0px` to `2px`).
- **Composition:** Asymmetrical editorial spreads, pull-quotes, multi-column body text, drop caps, offset captions.
- **Imagery:** Expressive photojournalism, duotone portraits, textured black-and-white photography, artistic studio stills.
- **Density:** Medium-low density. Focused on readability and sustained focus.
- **Motion:** Subtle, literary fades (`fade-in-up`, 300ms ease-out), smooth reading progress indicators, quiet page transitions.
- **Color Behavior:** Warm parchment/paper backgrounds (`#FBF9F5`), deep ink blacks (`#111111`), sepia/warm gray secondary tones, muted crimson or forest green accents.
- **Appropriate Industries:** High-end consultancies, media companies, literary publications, boutique law firms, research institutes, thought leaders.
- **Inappropriate Uses:** High-frequency SaaS dashboards, fast-paced consumer e-commerce, gamer hardware.
- **Common Failure Modes:** Overcrowding text without sufficient leading; using cheap decorative display serifs; looking like an unstyled Word document.

---

### 2. Luxury
- **Visual Soul:** Exclusive, quiet wealth, bespoke craftsmanship, unhurried elegance.
- **Typography:** High-contrast Didone serifs (e.g., Bodoni, Playfair, Cormorant) or ultra-spaced geometric uppercase sans (e.g., Tenor Sans, Syncopate, Cinzel). Wide tracking on uppercase labels (`letter-spacing: 0.15em` to `0.25em`).
- **Spacing:** Vast negative space, ultra-wide margins (up to 120px+ on desktop), breathing room around every asset.
- **Geometry:** Razor-sharp corners (`0px` border-radius), whisper-thin metallic or tonal borders, perfectly balanced symmetrical proportions.
- **Composition:** Monumental centered or split-screen heroes, isolated product centerpieces, minimal interface clutter.
- **Imagery:** High-contrast studio photography, dramatic chiaroscuro lighting, macro material textures (gold, marble, leather, cashmere, brushed titanium).
- **Density:** Very low density. Less is unmistakably more.
- **Motion:** Slow, frictionless easing (`transition: all 600ms cubic-bezier(0.16, 1, 0.3, 1)`), parallax depth reveals, cinematic curtain dissolves.
- **Color Behavior:** Deep obsidian (`#080808`), rich charcoal, warm ivory, champagnes, brushed gold, and platinum accents.
- **Appropriate Industries:** Haute horlogerie, private wealth management, luxury real estate, fine jewelry, private aviation, Michelin-starred hospitality.
- **Inappropriate Uses:** Discount e-commerce, developer tooling, high-volume consumer utilities.
- **Common Failure Modes:** Gaudy bright yellow "gold" colors; cheesy glitter animations; excessive decorative borders that look like 2000s award certificates.

---

### 3. Cinematic
- **Visual Soul:** Immersive, dramatic, narrative-driven, widescreen blockbuster mood.
- **Typography:** Bold extended grotesques (e.g., Syne, PP Neue Montreal, Cabinet Grotesk, Anton) paired with compact technical sans or clean subtitles.
- **Spacing:** Full-bleed viewports, edge-to-edge video or canvas containers, controlled cinematic letterboxing (`aspect-ratio: 21/9` or `16/9`).
- **Geometry:** Strict panoramic grids, flush container edges, sharp or subtle 4px corner curves.
- **Composition:** Dynamic horizontal focal flows, layered typography over heavy visual canvases, deep vignette focal centers.
- **Imagery:** Atmospheric full-bleed video backgrounds, anamorphic lens flares, moody grading, motion blur captures, film grain overlays.
- **Density:** Low interface density, high visual impact.
- **Motion:** Scroll-triggered parallax, scale-down zooms on hero exit, reveal wipes, glowing ambient flares.
- **Color Behavior:** Deep pitch darks (`#050507`), neon volumetric rim-lights, rich electric amber, cyan, or crimson highlights.
- **Appropriate Industries:** Film & entertainment, video production, gaming studios, sensory consumer electronics, event launches.
- **Inappropriate Uses:** Text-heavy documentation, compliance software, medical records.
- **Common Failure Modes:** Heavy video files causing 5-second lag; unreadable text over busy video backgrounds; obnoxious autoplay audio.

---

### 4. Industrial
- **Visual Soul:** Utilitarian, heavy-duty, robust, mechanical, uncompromising.
- **Typography:** Heavy condensed sans-serifs (e.g., Bebas Neue, Impact, Barlow Condensed, DIN 1451) paired with rugged monospace (JetBrains Mono, Roboto Mono).
- **Spacing:** Compact, dense modular grids, structural gridlines visible like steel scaffolding.
- **Geometry:** Sharp angular edges (`0px` radius), hazard diagonal striping, technical crosshairs, visible structural bounding boxes (`2px solid var(--industrial-border)`).
- **Composition:** Heavy modular compartments, technical spec sheets, schematic overlays, badge stamps.
- **Imagery:** Raw manufacturing photography, CNC machinery, steel textures, exploded CAD drawings, blueprint diagrams.
- **Density:** High density. Maximum utility and functional clarity.
- **Motion:** Snappy, instantaneous linear transitions (150ms ease or step-timing), ratchet-style micro-interactions.
- **Color Behavior:** Matte industrial safety colors: Safety orange (`#FF5500`), caution yellow (`#FFD000`), machine dark gray (`#1E2022`), galvanized zinc (`#E5E7EB`).
- **Appropriate Industries:** Heavy machinery, robotics, defense tech, industrial logistics, construction, aerospace manufacturing.
- **Inappropriate Uses:** Wellness spas, children's clothing, fine dining, romantic literature.
- **Common Failure Modes:** Looking like an amateur construction site from 1998; overusing caution tape graphics; harsh illegible contrast.

---

### 5. Architectural
- **Visual Soul:** Structural, spatial, disciplined, geometric, balanced.
- **Typography:** Clean geometric sans (e.g., Space Grotesk, Archivo, Neue Haas Grotesk, Manrope). Strict baseline grid alignment.
- **Spacing:** Rigorous 8px/16px spatial rhythm, mathematical proportions (Golden Ratio, Fibonacci subdivisions).
- **Geometry:** Visible structural hair-lines, crisp 90-degree corners, orthogonal grid intersections, elevation coordinates.
- **Composition:** Asymmetric balance, structural column offsets, blueprint grid backdrops, spatial framing.
- **Imagery:** Clean architectural photography, minimalist concrete/glass facades, isometric 3D models, daylight shadow studies.
- **Density:** Medium density. Meticulously organized.
- **Motion:** Structural slide transitions along coordinate axes, clean linear curtain reveals, smooth isometric rotation.
- **Color Behavior:** Concrete tones, limestone (`#EFECE6`), slate, muted terracotta, deep monolithic graphite (`#1A1B1E`).
- **Appropriate Industries:** Architecture studios, interior design, structural engineering, structural design software, modular furniture.
- **Inappropriate Uses:** High-energy gaming sites, children's toys, organic food markets.
- **Common Failure Modes:** Excessive grid lines creating visual noise; overly sterile and cold feeling; lack of clear conversion emphasis.

---

### 6. Modernist (Swiss / International Typographic Style)
- **Visual Soul:** Objective, timeless, rational, clear, mathematically ordered.
- **Typography:** Grotesque sans-serifs (e.g., Helvetica Neue, Neue Haas Grotesk, General Sans, Instrument Sans). Strict hierarchy: gigantic display weight contrasting with neat neutral body copy.
- **Spacing:** Rigid 12-column asymmetric grid, uniform gutter spacing, purposeful tension between large type and empty space.
- **Geometry:** Absolute zero radius (`0px`), crisp hairline dividers, rectangular bounding modules.
- **Composition:** Heavy asymmetric grid layouts, massive typography overlapping imagery, diagonal tension anchors.
- **Imagery:** Objective photography, high-contrast monochrome, clean product cutouts on stark white/gray backdrops.
- **Density:** Medium-high functional density with vast typographic hierarchy.
- **Motion:** Crisp mechanical transitions (200ms ease-in-out), instant tab switching, zero bounce physics.
- **Color Behavior:** Stark primary palette: Pure white (`#FFFFFF`), pure black (`#000000`), accented with singular vibrant primary colors (Swiss red `#FF0000`, Klein blue `#002FA7`, or cadmium yellow).
- **Appropriate Industries:** Design agencies, modern SaaS, modern art museums, international consulting, premium hardware.
- **Inappropriate Uses:** Traditional vintage brands, rustic craft goods, children's entertainment.
- **Common Failure Modes:** Forgetting visual hierarchy so everything looks like a raw wireframe; making it too dry and academic.

---

### 7. Technical / Developer Tooling
- **Visual Soul:** Engineered, data-rich, developer-first, terminal-inspired, precise.
- **Typography:** Precision monospaced type (e.g., JetBrains Mono, Fira Code, Space Mono, Berkeley Mono) paired with a high-legibility sans (Inter, Geist Sans).
- **Spacing:** Compact, dense layout, code blocks with exact syntax padding, keyboard shortcut badges (`<kbd>`).
- **Geometry:** Subtle 4px-6px corner radiuses, terminal window chrome (three dot header), dark code panes, hairline borders (`1px solid rgba(255,255,255,0.08)`).
- **Composition:** Split screen with interactive code sandbox on right and feature copy on left; command line interfaces; benchmark comparison tables.
- **Imagery:** Real interactive code snippets, CLI terminal output, architecture topology diagrams, real product UI screenshots.
- **Density:** High density. Rich with technical specifications and benchmarks.
- **Motion:** Terminal typewriter cursor effects, smooth tab toggles, syntax highlight fades, copy-to-clipboard micro-animations.
- **Color Behavior:** Dark IDE canvases (`#0D1117`, `#0A0E14`), neon syntax accents (emerald green `#10B981`, electric purple `#8B5CF6`, solarized amber `#F59E0B`).
- **Appropriate Industries:** Developer tools, APIs, cloud infrastructure, AI models, cybersecurity, data warehousing.
- **Inappropriate Uses:** Luxury fashion, lifestyle blogs, wedding planning.
- **Common Failure Modes:** Fake code snippets that make no sense; unreadable tiny monospace body text; overwhelming non-developers.

---

### 8. Heritage / Traditional
- **Visual Soul:** Timeless, trustworthy, storied, established, historical dignity.
- **Typography:** Classic Old-Style or Venetian serifs (e.g., Garamond, Baskerville, Caslon, EB Garamond) with engraved decorative capitals.
- **Spacing:** Classic centered symmetry, stately margins, ornate framed borders.
- **Geometry:** Traditional framing, subtle arched viewports, double-ruled border lines, ornamental heraldry marks.
- **Composition:** Centered formal layouts, balanced columns, heritage timeline stories, founding year stamps ("Est. 1884").
- **Imagery:** Archival photography, vintage engravings, textured oil paintings, warm copper/leather product details.
- **Density:** Medium density. Measured, calm, dignified pacing.
- **Motion:** Subtle, stately cross-dissolves, slow page turns, zero aggressive popups.
- **Color Behavior:** Rich heritage tones: British racing green (`#004225`), oxblood burgundy (`#4A0E17`), navy blue (`#0B1B3D`), aged antique cream (`#F4EFEA`), gold leaf.
- **Appropriate Industries:** Historic universities, century-old banks, law firms, legacy watchmakers, heritage apparel, distilleries.
- **Inappropriate Uses:** Web3 crypto protocols, fast fashion apps, teenage social networks.
- **Common Failure Modes:** Looking outdated and neglected rather than intentionally classic; poor mobile responsiveness on complex frames.

---

### 9. Organic / Botanical
- **Visual Soul:** Natural, holistic, grounded, calming, sustainable, earthy.
- **Typography:** Soft humanist serifs (e.g., Recoleta, Bitter, Lora) or rounded friendly sans (Plus Jakarta Sans, Quicksand).
- **Spacing:** Flowing, asymmetric organic spacing, breathing room inspired by natural landscapes.
- **Geometry:** Smooth, organic pebble curves (`border-radius: 24px` to `48px` or asymmetrical clip-paths), pill tags, flowing wave separators.
- **Composition:** Gentle overlapping cards, asymmetrical botanical collages, conversational testimonial flows.
- **Imagery:** Natural sunlight photography, botanical flora, unbleached linen textures, earthy ingredients, outdoor lifestyle.
- **Density:** Low to medium density. Soothing, uncluttered, gentle.
- **Motion:** Gentle wave swells, soft floating hover states, organic spring physics.
- **Color Behavior:** Earthy palette: Sage green (`#7D9D8B`), warm terracotta (`#C86D51`), sand beige (`#F3EEEA`), forest moss, sunny clay.
- **Appropriate Industries:** Sustainable goods, organic food & beverage, wellness retreats, clean beauty, eco-tech, mental health apps.
- **Inappropriate Uses:** High-frequency trading platforms, industrial mining, cybersecurity firewall monitors.
- **Common Failure Modes:** Over-mushy pastel colors that wash out contrast; illegible soft fonts with insufficient color contrast for WCAG AA.

---

### 10. Boutique / Artisanal
- **Visual Soul:** Handcrafted, bespoke, curated, intimate, high-taste.
- **Typography:** Characterful display serifs (e.g., Ogg, Roslindale, GT Super, Cormorant) with idiosyncratic ligatures, paired with clean minimalist grotesques.
- **Spacing:** Playful yet disciplined offset spacing, gallery-style catalog layouts.
- **Geometry:** Delicate circular badges, bespoke product tags, subtle 8px corners, fine dashed or dotted craftsmanship lines.
- **Composition:** Editorial lookbook grids, staggered photo showcases, curator notes, limited edition counter badges.
- **Imagery:** High-taste flat-lays, tactile macro shots of stitching/ceramics/paper, natural ambient studio lighting.
- **Density:** Medium-low density. Every product treated as an art piece.
- **Motion:** Smooth magnetic cursor tags, image reveal magnifiers, gentle carousel glides.
- **Color Behavior:** Muted designer neutrals: Oatmeal, dusty rose, olive drab, espresso brown, warm matte black.
- **Appropriate Industries:** Specialty coffee roasters, bespoke furniture makers, independent fashion designers, artisan bakeries, design studios.
- **Inappropriate Uses:** High-volume wholesale discount stores, enterprise IT databases.
- **Common Failure Modes:** Overusing quirky display fonts for body copy; making checkout/contact buttons too hard to find.

---

### 11. Premium Corporate / Institutional
- **Visual Soul:** Authoritative, enterprise-scale, dependable, prestigious, solid.
- **Typography:** Crisp neo-grotesque sans (e.g., Plus Jakarta Sans, Inter, General Sans, Sora) with bold numerical stats and clear subheading weights.
- **Spacing:** Structured 12-column grid, disciplined 24px-48px component containers, clean executive summaries.
- **Geometry:** Refined 8px-12px container corners, crisp 1px neutral borders, elevated card shadows with multi-layered ambient diffusion.
- **Composition:** Clear value pillars, verified customer logo clouds, interactive ROI calculators, executive team profiles, compliance badge strips.
- **Imagery:** Modern glass architecture, diverse executive leadership in natural business settings, real high-resolution UI platforms.
- **Density:** Medium-high density. Built for swift evaluation by executive committees.
- **Motion:** Confident, smooth micro-interactions (250ms cubic-bezier), tabbed capability matrices, progressive disclosure accordions.
- **Color Behavior:** Deep navy/slate foundation (`#0F172A`), crisp arctic whites, corporate royal blue (`#2563EB`) or rich emerald (`#059669`) primary CTAs.
- **Appropriate Industries:** Enterprise B2B SaaS, management consultancies, global insurance, fintech platforms, venture capital firms.
- **Inappropriate Uses:** Underground music labels, avant-garde art collectives.
- **Common Failure Modes:** Slipping into generic "AI SaaS template" slop; meaningless floating icons; vague buzzword headlines.

---

### 12. Playful / High-Energy
- **Visual Soul:** Vibrant, dynamic, joyful, approachable, spirited.
- **Typography:** Chunky geometric display faces (e.g., Bricolage Grotesque, Outfit, Clash Display, Poppins) with expressive heavy weights.
- **Spacing:** Punchy, compact vertical rhythms, oversized interactive touch targets, prominent floating CTAs.
- **Geometry:** Bold rounded corners (`16px` to `9999px` pill shapes), thick black outlines (`2px-3px solid`), playful sticker badges, pop-art shadows (`box-shadow: 4px 4px 0px #000`).
- **Composition:** Sticker collage heroes, interactive toggle playgrounds, animated mascot avatars, bold contrasting cards.
- **Imagery:** High-saturation product renders, 3D claymorphic elements, vibrant colorful backgrounds, joyful candid portraits.
- **Density:** Medium density. Energetic and interactive.
- **Motion:** Bouncy spring physics (`cubic-bezier(0.34, 1.56, 0.64, 1)`), wobbly hover rotations (`transform: rotate(-2deg)`), confetti triggers, confetti particles.
- **Color Behavior:** Electric dopamine palette: Bubblegum pink, sunny yellow (`#FACC15`), electric lime (`#84CC16`), royal violet, hyper-cyan.
- **Appropriate Industries:** Creator economy tools, casual mobile apps, modern snack/beverage brands, children's educational apps, gamified fitness.
- **Inappropriate Uses:** Mortuaries, cybersecurity forensics, serious wealth preservation, medical oncology.
- **Common Failure Modes:** Overwhelming cognitive load; visual chaos where everything bounces simultaneously; inaccessible color contrast.

---

### 13. Experimental / Neo-Brutalist
- **Visual Soul:** Radical, raw, boundary-pushing, anti-establishment, avant-garde.
- **Typography:** Raw monospace, stretched display type (e.g., Monument Extended, Druk, Syne Mono), inverted capitalization, extreme type size contrasts.
- **Spacing:** Unconventional dense or erratic spacing, overlapping layout coordinates, marquee ticker strips running full width.
- **Geometry:** Raw unpadded 90-degree boxes, exposed raw HTML-like borders, stark high-contrast drop shadows without blur (`box-shadow: 6px 6px 0px #000`).
- **Composition:** Broken grid layouts, horizontal side-scrolling galleries, ASCII art decorations, window-in-window UI.
- **Imagery:** Glitch art, risograph textures, raw raw unretouched photography, 3D wireframes, thermal vision renders.
- **Density:** Variable (can range from hyper-dense information dumps to vast stark voids).
- **Motion:** Kinetic typography, horizontal infinite marquees, cursor-following magnetic trails, glitch hover states.
- **Color Behavior:** High-voltage contrast: Pure black/white with acid neon green (`#22C55E`), radioactive yellow (`#EAB308`), or brutal hot magenta (`#EC4899`).
- **Appropriate Industries:** Creative tech agencies, Web3 protocols, underground music festivals, streetwear drops, digital artists.
- **Inappropriate Uses:** Healthcare patient portals, retirement savings funds, government tax filing.
- **Common Failure Modes:** Sacrificing usability and accessibility for edge; unreadable navigation; alienating regular customers.

---

### 14. High Fashion / Avant-Garde
- **Visual Soul:** Striking, dramatic, haute couture, runway-caliber, sculptural.
- **Typography:** Ultra-contrasting modern serifs with extreme vertical stress (e.g., Italianno, Bodoni Poster, Ogg, SangBleu) contrasted with hairline monospaced lookbook numbers.
- **Spacing:** Asymmetrical cinematic spreads, extreme vertical padding, offset image columns.
- **Geometry:** Razor-sharp framing, full-bleed vertical portrait containers (`aspect-ratio: 3/4`), minimal structural lines.
- **Composition:** Asymmetric lookbook galleries, floating runway titles overlapping images, offset editorial columns.
- **Imagery:** High-fashion runway photography, sculptural studio lighting, dramatic model poses, monochrome styling with rich fabric closeups.
- **Density:** Low interface density, maximum visual tension and mood.
- **Motion:** Elegant curtain wipes, slow-motion video loops, image crossfades with gentle scaling.
- **Color Behavior:** Strict monochrome foundation (Pitch black, bone white, graphite) with single seasonal accent notes (e.g., crimson, cobalt, or chartreuse).
- **Appropriate Industries:** Haute couture fashion houses, model agencies, luxury perfume, art biennials, luxury retail flagships.
- **Inappropriate Uses:** B2B accounting software, plumbing services, technical data documentation.
- **Common Failure Modes:** Forgetting e-commerce buttons; extremely slow image loading; prioritizing art over customer purchasing journey.

---

## 1.5 Research-Informed Archetype Selection (V1.1)

This catalog and the 60/30/10 formula remain the sole source of archetype definitions and blending mechanics. As of V1.1, `templates/research-synthesis.md` §9 supplies a *recommended* primary/secondary/accent input — derived from industry-landscape, Landbook, and cross-industry findings — before Website Director makes the final selection below. Research narrows and justifies the choice; it does not add a fifteenth archetype or a competing blending system. If research recommends a blend absent from the Pre-Validated Archetype Blends table, treat it as a new custom blend and validate it against the Blending Restrictions before adopting it.

---

## 2. Archetype Blending Rules (The 60/30/10 Formula)

Pure archetypes can feel rigid. High-end brands frequently blend 2 or 3 archetypes intentionally to create a proprietary visual signature.

### The Blending Formula & Concrete Token Mappings:
- **60% Primary Foundation (Structural Spine):**
  - Dictates base background tokens (`--bg-primary`, `--bg-secondary`, `--bg-surface`).
  - Dictates primary container max-widths and layout grid system.
  - Dictates the primary display typography family and type scale ratio.
  - Establishes the baseline border-radius tier (`0-2px` sharp, `4-8px` refined, `8-12px` modern, or `16-24px` organic).
- **30% Secondary Modifier (Surface & Material Texture):**
  - Dictates imagery art direction, aspect ratios, lighting prompts, and color grading.
  - Dictates surface component borders, divider styles, and shadow elevations (`--border-medium`, `--shadow-md`).
  - Modulates information density and body/interface typographic styling.
- **10% Kinetic / Signature Accent (Visual Punch & Micro-Polish):**
  - Dictates primary CTA button hover physics, cursor interactions, and easing timing curves.
  - Dictates signature accents (e.g., monospace metadata tags, didone drop-caps, technical crosshairs, or subtle noise overlays).
  - Supplies the high-voltage primary accent color (`--accent-primary`).

### Pre-Validated Archetype Blends:

| Blend Formula | Resulting Personality | Ideal Domain |
| :--- | :--- | :--- |
| **60% Cinematic + 30% Industrial + 10% Editorial** | Heavyweight, cinematic, engineering-grade power with rigorous textual depth. | Autonomous robotics, aerospace defense, high-end EV manufacturing. |
| **60% Editorial + 30% Luxury + 10% Modernist** | Cultured, bookish, ultra-premium advisory with razor-sharp Swiss clarity. | M&A advisory, family offices, architectural design consultancies. |
| **60% Technical + 30% Modernist + 10% Playful** | Developer-grade rigor with Swiss precision and delightful micro-interactions. | Modern developer productivity tools, API platforms, OSS dev tooling. |
| **60% Premium Corporate + 30% Architectural + 10% Technical** | Enterprise-grade authority with structured spatial discipline and data credibility. | B2B fintech infrastructure, cloud security, supply chain AI. |
| **60% Architectural + 30% Industrial + 10% Luxury** | Monolithic structural elegance with heavy-duty engineered durability and quiet prestige. | High-end custom construction, luxury garage/workshop design, architectural hardware. |

### Blending Restrictions:
- **Never blend opposing geometric laws:** Do not mix raw Brutalist 90-degree thick black box shadows with 32px squishy Playful pill shapes on the same screen.
- **Single Typography Rule:** Maximum 2 primary font families per website (e.g., 1 Display/Heading family + 1 Body/Interface family, plus an optional Mono utility face for data/code). Never combine three distinct decorative display fonts.
