import os

pilot_dir = r"projects/v2-5-1-signature-choreography-certification-pilot"

# 1. HTML
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ARC//FORGE | Advanced Fabrication & Precision Engineering</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>

  <!-- REGION 1: NORMAL VERTICAL INTRO -->
  <header class="site-header">
    <div class="header-inner">
      <a href="#intro" class="brand-logo">ARC<span>//</span>FORGE</a>
      <nav class="site-nav">
        <a href="#intro">Overview</a>
        <a href="#atelier-track">Atelier Scrollytelling</a>
        <a href="#capabilities">Engineering Systems</a>
        <a href="#contact">Commission</a>
      </nav>
    </div>
  </header>

  <main id="main-content">
    <section id="intro" class="section hero-section">
      <div class="container hero-container">
        <div class="hero-badge">AEROSPACE GRADE METALLURGY</div>
        <h1 class="hero-title">WHERE RAW ELEMENTAL DENSITY MEETS MICRON TOLERANCE.</h1>
        <p class="hero-lead">We design and machine mission-critical structures for suborbital flight, deep marine immersion, and advanced industrial automation.</p>
        <div class="hero-actions">
          <a href="#atelier-track" class="btn btn-primary">Enter the Atelier Journey ↓</a>
          <a href="#capabilities" class="btn btn-secondary">Explore Capabilities</a>
        </div>
      </div>
    </section>

    <!-- REGION 2: PINNED HORIZONTAL SCROLLYTELLING + SCROLL ASSEMBLY (VERTICAL -> HORIZONTAL -> VERTICAL) -->
    <section id="atelier-scrollytelling" class="scrollytelling-outer">
      <div class="scrollytelling-pin" id="pin-target">
        
        <!-- Persistent HUD / Orientation Rail -->
        <div class="hud-rail">
          <div class="hud-title">THE FABRICATION JOURNEY</div>
          <div class="hud-steps">
            <span class="step-indicator active" data-step="0">01 RAW</span>
            <span class="step-indicator" data-step="1">02 FORM</span>
            <span class="step-indicator" data-step="2">03 PRECISION</span>
            <span class="step-indicator" data-step="3">04 ASSEMBLY</span>
            <span class="step-indicator" data-step="4">05 OUTPUT</span>
          </div>
          <div class="hud-progress-bar">
            <div class="hud-progress-fill" id="progress-fill"></div>
          </div>
        </div>

        <!-- Horizontal Track -->
        <div class="horizontal-track" id="atelier-track">
          
          <!-- Chapter 1 -->
          <article class="chapter-panel chapter-01" id="chapter-01">
            <div class="panel-content">
              <span class="chapter-num">01 // SOURCE</span>
              <h2>MONOLITHIC TITANIUM BILLET</h2>
              <p>Aerospace Ti-6Al-4V Grade 5 alloy certified for cryogenic and extreme thermal boundary environments. Zero porosity grain structure.</p>
              <div class="spec-tag">DENSITY: 4.43 g/cm³ · YIELD: 880 MPa</div>
            </div>
            <div class="panel-visual visual-billet">
              <div class="billet-box">
                <div class="billet-mesh"></div>
                <div class="callout">RAW BILLET · 120kg</div>
              </div>
            </div>
          </article>

          <!-- Chapter 2 -->
          <article class="chapter-panel chapter-02" id="chapter-02">
            <div class="panel-content">
              <span class="chapter-num">02 // SUBTRACTION</span>
              <h2>5-AXIS SIMULTANEOUS GANTRY MILLING</h2>
              <p>Rough machining removes 84% of mass to establish aerodynamic rib topology and structural load paths under 18,000 RPM spindle velocity.</p>
              <div class="spec-tag">AXIS SPEED: 60m/min · FLOOD COOLANT: SYNTH-X</div>
            </div>
            <div class="panel-visual visual-milling">
              <div class="mill-spindle">
                <div class="tool-cutter"></div>
                <div class="spark-burst"></div>
              </div>
            </div>
          </article>

          <!-- Chapter 3 -->
          <article class="chapter-panel chapter-03" id="chapter-03">
            <div class="panel-content">
              <span class="chapter-num">03 // MICRO-TOLERANCE</span>
              <h2>OPTICAL INTERFEROMETRY & WIRE EDM</h2>
              <p>Electrical discharge machining carves internal fluid manifolds with ±0.002mm continuous profile repeatability.</p>
              <div class="spec-tag">SURFACE ROUGHNESS: Ra 0.2µm · INSPECTION: ZEISS CMM</div>
            </div>
            <div class="panel-visual visual-edm">
              <div class="edm-wire"></div>
              <div class="tolerance-ring"></div>
            </div>
          </article>

          <!-- Chapter 4: Scroll-Driven Assembly (PAT-04) -->
          <article class="chapter-panel chapter-04" id="chapter-04">
            <div class="panel-content">
              <span class="chapter-num">04 // SYNTHESIS</span>
              <h2>LOCKING MODULAR STRUCTURAL CHASSIS</h2>
              <p>Scroll-driven mechanical alignment. Individual bracket spars and internal core elements lock together into a cohesive structural unit.</p>
              <div class="spec-tag">INTERLOCK FACTOR: 100% · FASTENERS: M6 TITANIUM INCONEL</div>
            </div>
            <div class="panel-visual visual-assembly" id="assembly-container">
              <div class="assembly-part part-top" id="part-top">UPPER COWL</div>
              <div class="assembly-part part-core" id="part-core">STRUCTURAL CORE</div>
              <div class="assembly-part part-bottom" id="part-bottom">LOWER BULKHEAD</div>
              <div class="assembly-status" id="assembly-status">STATUS: DISPERSED</div>
            </div>
          </article>

          <!-- Chapter 5 -->
          <article class="chapter-panel chapter-05" id="chapter-05">
            <div class="panel-content">
              <span class="chapter-num">05 // FLIGHT READY</span>
              <h2>VERIFIED AEROSPACE FLUIDIC MANIFOLD</h2>
              <p>Fully assembled, ultrasonic cleaned, pressure tested to 450 bar, and certified for flight integration.</p>
              <div class="spec-tag">CERT: AS9100D · QA SCORE: 100/100</div>
              <a href="#capabilities" class="btn btn-primary" style="margin-top: 1.5rem;">Continue to Specifications ↓</a>
            </div>
            <div class="panel-visual visual-finished">
              <div class="finished-chassis">
                <div class="glow-indicator">READY FOR INTEGRATION</div>
              </div>
            </div>
          </article>

        </div>
      </div>
    </section>

    <!-- REGION 3: NORMAL VERTICAL RESUMPTION -->
    <section id="capabilities" class="section capabilities-section">
      <div class="container">
        <div class="section-badge">PRODUCTION SPECIFICATIONS</div>
        <h2 class="section-title">CERTIFIED ENGINEERING CAPABILITIES</h2>
        <div class="grid-3">
          <div class="card">
            <h3>01. MULTI-AXIS CNC MACHINING</h3>
            <p>5-axis DMG MORI precision centers capable of handling workpieces up to 2,000mm with active thermal compensation.</p>
          </div>
          <div class="card">
            <h3>02. WIRE & SINKER EDM</h3>
            <p>Non-contact electrical discharge cutting for hardened refractory metals, Inconel 718, and exotic superalloys.</p>
          </div>
          <div class="card">
            <h3>03. METROLOGY & CMM LAB</h3>
            <p>Temperature-controlled Class 10,000 cleanroom CMM scanning with sub-micron volumetric uncertainty.</p>
          </div>
        </div>
      </div>
    </section>

    <section id="contact" class="section contact-section">
      <div class="container contact-container">
        <h2>COMMISSION A HIGH-PRECISION RUN</h2>
        <p>Direct inquiries to our principal engineering team in Zurich & Stuttgart.</p>
        <a href="mailto:engineering@arcforge.ch" class="btn btn-primary">Initiate Confidential Consultation</a>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-inner">
      <div>© 2026 ARC//FORGE Motoren & Raumfahrttechnik. All rights reserved.</div>
      <div class="footer-meta">V2.5.1 Signature Choreography Pilot · Certified Baseline</div>
    </div>
  </footer>

  <!-- Scripts -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
  <script src="js/main.js"></script>
</body>
</html>
"""

# 2. CSS
css_content = """/* ARC//FORGE DESIGN SYSTEM TOKENS */
:root {
  --bg-primary: #0a0c10;
  --bg-surface: #12161f;
  --bg-card: #181e2b;
  --text-primary: #f0f4f8;
  --text-secondary: #9ba8b7;
  --text-muted: #5e6c7d;
  --accent-cyan: #00e5ff;
  --accent-amber: #ff9100;
  --border-subtle: #242c3d;
  --font-mono: "JetBrains Mono", Consolas, monospace;
  --font-sans: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
  --ease-cinematic: cubic-bezier(0.16, 1, 0.3, 1);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  font-family: var(--font-sans);
  line-height: 1.6;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
}

a {
  color: inherit;
  text-decoration: none;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* Header */
.site-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
  background: rgba(10, 12, 16, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-subtle);
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.25rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand-logo {
  font-family: var(--font-mono);
  font-weight: 800;
  font-size: 1.25rem;
  letter-spacing: 0.15em;
}

.brand-logo span {
  color: var(--accent-cyan);
}

.site-nav {
  display: flex;
  gap: 2rem;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
}

.site-nav a:hover, .site-nav a:focus {
  color: var(--accent-cyan);
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.875rem 1.75rem;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border-radius: 2px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.btn-primary {
  background: var(--accent-cyan);
  color: #000;
  border: 1px solid var(--accent-cyan);
}

.btn-primary:hover {
  background: #fff;
  border-color: #fff;
}

.btn-secondary {
  background: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
}

.btn-secondary:hover {
  border-color: var(--accent-cyan);
  color: var(--accent-cyan);
}

/* Sections */
.section {
  padding: 8rem 0;
  position: relative;
}

.hero-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding-top: 10rem;
}

.hero-badge, .section-badge {
  display: inline-block;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  color: var(--accent-cyan);
  margin-bottom: 1.5rem;
}

.hero-title {
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: 1.5rem;
}

.hero-lead {
  font-size: 1.25rem;
  color: var(--text-secondary);
  max-width: 720px;
  margin-bottom: 2.5rem;
}

.hero-actions {
  display: flex;
  gap: 1.25rem;
}

/* PINNED HORIZONTAL SCROLLYTELLING CONTAINER */
.scrollytelling-outer {
  position: relative;
  background: #06080b;
  border-top: 1px solid var(--border-subtle);
  border-bottom: 1px solid var(--border-subtle);
}

.scrollytelling-pin {
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
}

/* HUD Orientation Rail */
.hud-rail {
  position: absolute;
  top: 6rem;
  left: 3rem;
  right: 3rem;
  z-index: 50;
  display: flex;
  justify-content: space-between;
  align-items: center;
  pointer-events: none;
  font-family: var(--font-mono);
}

.hud-title {
  font-size: 0.8rem;
  letter-spacing: 0.15em;
  color: var(--text-muted);
}

.hud-steps {
  display: flex;
  gap: 1.5rem;
}

.step-indicator {
  font-size: 0.8rem;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  transition: color 0.3s ease;
}

.step-indicator.active {
  color: var(--accent-cyan);
  font-weight: 700;
}

.hud-progress-bar {
  width: 180px;
  height: 3px;
  background: var(--border-subtle);
  position: relative;
}

.hud-progress-fill {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 0%;
  background: var(--accent-cyan);
}

/* Horizontal Track */
.horizontal-track {
  display: flex;
  height: 100vh;
  width: 500vw;
  will-change: transform;
}

.chapter-panel {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8rem 6rem 4rem 6rem;
  flex-shrink: 0;
  border-right: 1px solid var(--border-subtle);
  position: relative;
}

.panel-content {
  max-width: 540px;
  z-index: 10;
}

.chapter-num {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--accent-cyan);
  letter-spacing: 0.2em;
  display: block;
  margin-bottom: 1rem;
}

.chapter-panel h2 {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1.15;
  margin-bottom: 1.25rem;
}

.chapter-panel p {
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  font-size: 1.05rem;
}

.spec-tag {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--accent-amber);
  background: rgba(255, 145, 0, 0.1);
  padding: 0.5rem 0.85rem;
  display: inline-block;
  border: 1px solid rgba(255, 145, 0, 0.3);
}

.panel-visual {
  width: 500px;
  height: 400px;
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

/* Visual Mockups */
.billet-box {
  width: 240px;
  height: 240px;
  border: 2px solid var(--text-muted);
  background: #1c2333;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.callout {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--accent-cyan);
  margin-top: 1rem;
}

/* Assembly Visual (PAT-04) */
.visual-assembly {
  position: relative;
  overflow: hidden;
}

.assembly-part {
  position: absolute;
  padding: 1rem 2rem;
  background: #1f2738;
  border: 1px solid var(--accent-cyan);
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 700;
  color: #fff;
  transition: transform 0.1s linear;
}

.part-top {
  top: 40px;
  transform: translateY(-80px);
}

.part-core {
  top: 170px;
  background: #263248;
}

.part-bottom {
  top: 300px;
  transform: translateY(80px);
}

.assembly-status {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--accent-amber);
}

.finished-chassis {
  width: 320px;
  height: 200px;
  border: 2px solid var(--accent-cyan);
  background: #172a3a;
  display: flex;
  align-items: center;
  justify-content: center;
}

.glow-indicator {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--accent-cyan);
  font-weight: 700;
}

/* Vertical Grids */
.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 3rem;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  padding: 2.5rem;
  border-radius: 2px;
}

.card h3 {
  font-family: var(--font-mono);
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: var(--accent-cyan);
}

.card p {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

/* Contact */
.contact-section {
  background: var(--bg-surface);
  text-align: center;
}

.contact-container h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.contact-container p {
  color: var(--text-secondary);
  margin-bottom: 2rem;
}

/* Footer */
.site-footer {
  padding: 3rem 0;
  border-top: 1px solid var(--border-subtle);
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--text-muted);
}

.footer-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* RESPONSIVE REFLOW (<= 768px) */
@media (max-width: 768px) {
  .site-nav {
    display: none;
  }

  .hud-rail {
    display: none;
  }

  .scrollytelling-pin {
    height: auto;
    overflow: visible;
  }

  .horizontal-track {
    display: block;
    width: 100%;
    height: auto;
    transform: none !important;
  }

  .chapter-panel {
    width: 100%;
    height: auto;
    padding: 4rem 1.5rem;
    flex-direction: column;
    border-right: none;
    border-bottom: 1px solid var(--border-subtle);
  }

  .panel-content {
    max-width: 100%;
    margin-bottom: 2rem;
  }

  .panel-visual {
    width: 100%;
    height: 280px;
  }

  .grid-3 {
    grid-template-columns: 1fr;
  }

  .footer-inner {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}

/* REDUCED MOTION */
@media (prefers-reduced-motion: reduce) {
  .horizontal-track {
    display: block !important;
    width: 100% !important;
    height: auto !important;
    transform: none !important;
  }

  .scrollytelling-pin {
    height: auto !important;
    overflow: visible !important;
  }

  .chapter-panel {
    width: 100% !important;
    height: auto !important;
    padding: 4rem 2rem !important;
    flex-direction: column !important;
  }

  .assembly-part {
    position: static !important;
    transform: none !important;
    margin-bottom: 0.5rem !important;
  }
}
"""

# 3. JavaScript
js_content = """// ARC//FORGE SIGNATURE CHOREOGRAPHY ENGINE (V2.5.1)
document.addEventListener('DOMContentLoaded', () => {
  if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
    console.warn('GSAP or ScrollTrigger missing; falling back to standard vertical layout.');
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isMobile = window.innerWidth <= 768;

  if (isReducedMotion || isMobile) {
    console.log('Mobile or Reduced Motion detected; running in REFLOWED static mode.');
    return;
  }

  const pinTarget = document.getElementById('pin-target');
  const track = document.getElementById('atelier-track');
  const progressFill = document.getElementById('progress-fill');
  const indicators = document.querySelectorAll('.step-indicator');

  const partTop = document.getElementById('part-top');
  const partBottom = document.getElementById('part-bottom');
  const assemblyStatus = document.getElementById('assembly-status');

  // Total horizontal distance to translate: (5 panels - 1) * 100vw = 400vw
  const getScrollAmount = () => -(track.scrollWidth - window.innerWidth);

  const horizontalTween = gsap.to(track, {
    x: getScrollAmount,
    ease: 'none',
    paused: true
  });

  ScrollTrigger.create({
    trigger: '#atelier-scrollytelling',
    start: 'top top',
    end: () => `+=${track.scrollWidth - window.innerWidth}`,
    pin: true,
    scrub: 1,
    animation: horizontalTween,
    invalidateOnRefresh: true,
    onUpdate: (self) => {
      // 1. Update Progress Bar
      if (progressFill) {
        progressFill.style.width = `${self.progress * 100}%`;
      }

      // 2. Update Active HUD Chapter
      const stepIdx = Math.min(4, Math.floor(self.progress * 5));
      indicators.forEach((ind, i) => {
        if (i === stepIdx) ind.classList.add('active');
        else ind.classList.remove('active');
      });

      // 3. Scroll-Driven Assembly Trigger (PAT-04) inside Chapter 4 (progress 0.6 to 0.8)
      if (self.progress >= 0.55 && self.progress <= 0.85) {
        const assemblyProg = (self.progress - 0.55) / 0.3; // 0 to 1
        const clampedProg = Math.max(0, Math.min(1, assemblyProg));

        if (partTop && partBottom) {
          partTop.style.transform = `translateY(${(-80 * (1 - clampedProg))}px)`;
          partBottom.style.transform = `translateY(${(80 * (1 - clampedProg))}px)`;
        }

        if (assemblyStatus) {
          if (clampedProg > 0.9) {
            assemblyStatus.textContent = 'STATUS: INTERLOCKED (100%)';
            assemblyStatus.style.color = '#00e5ff';
          } else {
            assemblyStatus.textContent = `STATUS: ALIGNING (${Math.round(clampedProg * 100)}%)`;
            assemblyStatus.style.color = '#ff9100';
          }
        }
      }
    }
  });

  window.addEventListener('resize', () => {
    ScrollTrigger.refresh();
  });
});
"""

with open(os.path.join(pilot_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

with open(os.path.join(pilot_dir, "css", "style.css"), "w", encoding="utf-8") as f:
    f.write(css_content)

with open(os.path.join(pilot_dir, "js", "main.js"), "w", encoding="utf-8") as f:
    f.write(js_content)

print("Created complete pilot web source (HTML, CSS, JS).")
