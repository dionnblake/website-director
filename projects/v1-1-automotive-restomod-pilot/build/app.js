/**
 * KREISLER & VOSS MOTORENWERKE — MASTER APPLICATION ENGINE
 * Version: 1.1.0 (Website Director V1.1 Production Pilot)
 * Protocol: Motion Level 3 Cinematic Assembly + Dual-Perspective Atelier Inspector
 */

(function () {
  'use strict';

  // --- DATA ARCHIVE: COMMISSION CASE STUDIES ---
  const COMMISSIONS_DATA = {
    'kv-01': {
      title: 'KV-01 "Monolith GT"',
      eyebrow: 'ACTIVE COMMISSION 01 • CHASSIS KV-01/08',
      donor: '1989 G-Series Chassis Monocoque',
      desc1: 'Carved from an authentic matching-numbers donor monocoque, the KV-01 Monolith GT represents the absolute pinnacle of air-cooled grand touring. The entire chassis is seam-welded and reinforced with high-tensile titanium gussets, achieving a 65% increase in torsional rigidity.',
      desc2: 'The 4.0-liter naturally aspirated flat-six features custom-ground billet camshafts, titanium connecting rods, twin-plug ignition, and bespoke carbon-composite intake plenums delivering 415 BHP @ 8,400 RPM.',
      specs: [
        { k: 'DISPLACEMENT & ARCHITECTURE', v: '3,996 cc Naturally Aspirated Air-Cooled Flat-Six' },
        { k: 'PEAK POWER', v: '415 BHP (309 kW) @ 8,400 RPM' },
        { k: 'PEAK TORQUE', v: '430 Nm (317 lb-ft) @ 5,800 RPM' },
        { k: 'REDLINE LIMIT', v: '8,600 RPM (Electronic Cutoff)' },
        { k: 'TRANSAXLE', v: '6-Speed Manual with Billet G50 Housing & Mechanical LSD' },
        { k: 'CURB WEIGHT', v: '1,040 kg (Dry) • 40/60 Weight Distribution' },
        { k: 'BRAKING SYSTEM', v: 'Brembo Monobloc 6-Piston Front / 4-Piston Rear with Carbon-Ceramic Rotors' }
      ]
    },
    'kv-02': {
      title: 'KV-02 "Nero Superleggera"',
      eyebrow: 'ACTIVE COMMISSION 02 • CHASSIS KV-02/08',
      donor: '1974 Lightweight Coupe Platform',
      desc1: 'A purist analog performance targa focused on minimal unsprung weight and razor-sharp steering communication. The bodywork is shaped in carbon-kevlar composite with brushed titanium brightwork.',
      desc2: 'Powered by a 3.8-liter high-compression Twin-Spark engine delivering 385 BHP in a chassis weighing exactly 960 kg dry (401 BHP/ton).',
      specs: [
        { k: 'DISPLACEMENT & ARCHITECTURE', v: '3,800 cc Twin-Spark High-Compression Flat-Six' },
        { k: 'PEAK POWER', v: '385 BHP @ 8,200 RPM' },
        { k: 'PEAK TORQUE', v: '405 Nm @ 6,100 RPM' },
        { k: 'CURB WEIGHT', v: '960 kg (Dry)' },
        { k: 'POWER-TO-WEIGHT', v: '401 BHP / Ton' },
        { k: 'SUSPENSION', v: 'Uniball Titanium Double-Wishbone Geometry' }
      ]
    },
    'kv-03': {
      title: 'KV-03 "Modena Gran Turismo"',
      eyebrow: 'ACTIVE COMMISSION 03 • CHASSIS KV-03/08',
      donor: '1968 Fastback Monocoque',
      desc1: 'A celebration of Italian coachbuilding poetry paired with German powertrain precision. Hand-beaten aluminum bodywork shaped over timber bucks in Modena.',
      desc2: 'Features a 5.5L 60° Quad-Cam naturally aspirated V12 producing 510 BHP, paired with an open-gate 6-speed manual transaxle.',
      specs: [
        { k: 'DISPLACEMENT & ARCHITECTURE', v: '5,490 cc 60° Quad-Cam Naturally Aspirated V12' },
        { k: 'PEAK POWER', v: '510 BHP @ 7,800 RPM' },
        { k: 'PEAK TORQUE', v: '560 Nm @ 5,200 RPM' },
        { k: 'CURB WEIGHT', v: '1,220 kg (Dry)' },
        { k: 'COACHWORK', v: '1.2mm Hand-Formed Aerospace Aluminum' }
      ]
    },
    'kv-04': {
      title: 'KV-04 "Alpenjäger Rallye"',
      eyebrow: 'ACTIVE COMMISSION 04 • CHASSIS KV-04/08',
      donor: '1984 All-Wheel-Drive Monocoque',
      desc1: 'Engineered for high-elevation alpine passes in all weather conditions. Equipped with 3-way adjustable long-travel Bilstein motorsport dampers and reinforced titanium underbody skid plates.',
      desc2: '3.6L Twin-Turbo flat-six producing 450 BHP with variable mechanical center differential bias.',
      specs: [
        { k: 'DISPLACEMENT & ARCHITECTURE', v: '3,600 cc Twin-Turbocharged Flat-Six AWD' },
        { k: 'PEAK POWER', v: '450 BHP @ 7,200 RPM' },
        { k: 'PEAK TORQUE', v: '520 Nm @ 4,000 RPM' },
        { k: 'DRIVETRAIN', v: 'Mechanical Variable All-Wheel Drive' }
      ]
    },
    'kv-05': {
      title: 'KV-05 "Atelier Spyder"',
      eyebrow: 'ACTIVE COMMISSION 05 • CHASSIS KV-05/08',
      donor: 'Bespoke Tubular Spaceframe',
      desc1: '1-of-1 open-cockpit barchetta celebrating mechanical minimalism and wind-in-hair analog driving.',
      desc2: '4.2L high-revving naturally aspirated V8 (460 BHP @ 8,600 RPM) nestled in a 910 kg aluminum coachwork.',
      specs: [
        { k: 'DISPLACEMENT & ARCHITECTURE', v: '4,200 cc Naturally Aspirated V8' },
        { k: 'PEAK POWER', v: '460 BHP @ 8,600 RPM' },
        { k: 'CURB WEIGHT', v: '910 kg (Dry)' }
      ]
    }
  };

  // --- DATA ARCHIVE: MECHANICAL SPECIMENS ---
  const SPECIMEN_DATA = {
    intake: {
      title: 'CNC Billet 6061-T6 Velocity Stacks',
      subtitle: 'Aerospace-Grade Billet Aluminum • ±0.005mm Machining Tolerance',
      alloy: '6061-T6 Temper Aerospace Aluminum',
      finish: '0.4 Ra Waterjet Chamfer & Clear Hard-Anodize',
      strength: '310 MPa Yield / 276 MPa Ultimate',
      acoustic: '420 Hz Secondary Harmonic Resonance'
    },
    leather: {
      title: 'Saddle Ochre Bridge of Weir Leather',
      subtitle: 'Vegetable-Tanned Scottish Full-Grain • 1.4mm Thickness',
      alloy: 'Lowland Scottish Cattle Hide (Chromium-Free)',
      finish: 'Aniline Waxed Natural Patina Surface',
      strength: '25 N/mm² Tensile Grain Retention',
      acoustic: 'Acoustic Sound Dampening Coefficient: 0.35 NRC'
    },
    exhaust: {
      title: 'Inconel 625 Equal-Length Manifold',
      subtitle: '0.9mm Aerospace Superalloy • TIG Purge-Welded in Cologne',
      alloy: 'Inconel 625 Nickel-Chromium-Molybdenum',
      finish: 'Ceramic Thermal Barrier Coating (1,050°C Rated)',
      strength: '827 MPa Tensile Strength at Elevated Temperatures',
      acoustic: 'High-Pitch F1 Harmonic Frequency Profile'
    },
    suspension: {
      title: 'Titanium Double-Wishbone Links',
      subtitle: 'Grade 5 Ti-6Al-4V • Teflon-Lined Spherical Uniballs',
      alloy: 'Ti-6Al-4V Grade 5 Aerospace Titanium',
      finish: 'Bead-Blasted Satin with Micro-Polished Bores',
      strength: '880 MPa Yield Strength (42% Lighter than Steel)',
      acoustic: 'Zero Elastic Compliance Under Lateral 1.8G Cornering'
    }
  };

  // --- INITIALIZATION ---
  document.addEventListener('DOMContentLoaded', () => {
    initHeroCinematicScrubber();
    initCommissionFilters();
    initCaseStudyDrawer();
    initMechanicalLab();
    initMobileNav();
    initConsultationForm();
  });

  // 1. HERO CINEMATIC STAGE CONTROLLER (Motion Level 3)
  function initHeroCinematicScrubber() {
    const stageBtns = document.querySelectorAll('.cinematic-step-btn');
    const scrubFill = document.getElementById('scrub-progress-fill');
    const scrubBar = document.getElementById('cinematic-scrub-bar');
    const layerIntake = document.getElementById('layer-intake');
    const layerBody = document.getElementById('layer-body');
    const captionText = document.getElementById('stage-caption-text');

    const captions = [
      'Stage 01: <strong>5-Axis CNC Billet Intake</strong> — Individual throttle bodies and harmonic velocity stacks.',
      'Stage 02: <strong>Hand-Wheeled Coachbuilt Flank</strong> — 1.2mm aerospace aluminum bodywork shaped in Modena.',
      'Stage 03: <strong>Tactile Cockpit Integration</strong> — Saddle Ochre leather and machined titanium switchgear.',
      'Stage 04: <strong>KV-01 "Monolith GT" Masterwork</strong> — 4.0L Air-Cooled Flat-Six (415 BHP • 1,040 KG).'
    ];

    function setStage(stageIndex) {
      stageBtns.forEach((btn, idx) => {
        btn.classList.toggle('active', idx === stageIndex);
      });

      const pct = (stageIndex + 1) * 25;
      if (scrubFill) scrubFill.style.width = `${pct}%`;
      if (scrubBar) scrubBar.setAttribute('aria-valuenow', pct);
      if (captionText) captionText.innerHTML = captions[stageIndex];

      // Layer Transformations
      if (layerIntake && layerBody) {
        if (stageIndex === 0) {
          layerIntake.style.opacity = '1';
          layerIntake.style.transform = 'scale(1.1) translateY(-10px)';
          layerBody.style.opacity = '0.35';
        } else if (stageIndex === 1) {
          layerIntake.style.opacity = '0.6';
          layerIntake.style.transform = 'scale(1) translateY(0)';
          layerBody.style.opacity = '0.85';
        } else if (stageIndex === 2) {
          layerIntake.style.opacity = '0.4';
          layerBody.style.opacity = '0.95';
        } else {
          layerIntake.style.opacity = '0.2';
          layerBody.style.opacity = '1';
          layerBody.style.transform = 'scale(1)';
        }
      }
    }

    stageBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const stage = parseInt(btn.dataset.stage, 10);
        setStage(stage);
      });
    });

    // Window scroll sync for hero
    window.addEventListener('scroll', () => {
      const heroSec = document.getElementById('hero');
      if (!heroSec) return;
      const rect = heroSec.getBoundingClientRect();
      if (rect.top <= 100 && rect.bottom > 200) {
        const scrollPct = Math.min(Math.max((100 - rect.top) / (rect.height * 0.6), 0), 1);
        const stage = Math.min(Math.floor(scrollPct * 4), 3);
        setStage(stage);
      }
    }, { passive: true });
  }

  // 2. COMMISSION CATEGORY FILTERS
  function initCommissionFilters() {
    const filterTabs = document.querySelectorAll('.filter-tab');
    const cards = document.querySelectorAll('.commission-card');

    filterTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        filterTabs.forEach(t => {
          t.classList.remove('active');
          t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('active');
        tab.setAttribute('aria-selected', 'true');

        const filter = tab.dataset.filter;
        cards.forEach(card => {
          if (filter === 'all' || card.dataset.category === filter) {
            card.style.display = 'flex';
            if (card.classList.contains('commission-card-large') && window.innerWidth > 1200) {
              card.style.display = 'grid';
            }
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // 3. DUAL-PERSPECTIVE CASE STUDY DRAWER
  function initCaseStudyDrawer() {
    const drawer = document.getElementById('case-study-drawer');
    const backdrop = document.getElementById('drawer-backdrop');
    const closeBtn = document.getElementById('drawer-close-btn');
    const cardOpenBtns = document.querySelectorAll('.btn-card-open, .commission-card');
    const btnPhoto = document.getElementById('btn-mode-photo');
    const btnCad = document.getElementById('btn-mode-cad');
    const photoLayer = document.getElementById('drawer-photo-layer');
    const cadLayer = document.getElementById('drawer-cad-layer');

    const drawerTitle = document.getElementById('drawer-title');
    const drawerEyebrow = document.getElementById('drawer-eyebrow');
    const drawerDesc1 = document.getElementById('drawer-desc-p1');
    const drawerDesc2 = document.getElementById('drawer-desc-p2');
    const drawerSpecsTable = document.getElementById('drawer-specs-table');

    function openDrawer(projectId) {
      const data = COMMISSIONS_DATA[projectId] || COMMISSIONS_DATA['kv-01'];

      if (drawerTitle) drawerTitle.textContent = data.title;
      if (drawerEyebrow) drawerEyebrow.textContent = data.eyebrow;
      if (drawerDesc1) drawerDesc1.textContent = data.desc1;
      if (drawerDesc2) drawerDesc2.textContent = data.desc2;

      if (drawerSpecsTable) {
        drawerSpecsTable.innerHTML = '';
        data.specs.forEach(spec => {
          const row = document.createElement('div');
          row.className = 'drawer-spec-row';
          row.innerHTML = `
            <span class="d-spec-key">${spec.k}</span>
            <span class="d-spec-val">${spec.v}</span>
          `;
          drawerSpecsTable.appendChild(row);
        });
      }

      setMode('photo');
      drawer.classList.add('open');
      drawer.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
      drawer.classList.remove('open');
      drawer.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    function setMode(mode) {
      if (mode === 'photo') {
        btnPhoto.classList.add('active');
        btnCad.classList.remove('active');
        photoLayer.style.display = 'block';
        cadLayer.style.display = 'none';
      } else {
        btnCad.classList.add('active');
        btnPhoto.classList.remove('active');
        photoLayer.style.display = 'none';
        cadLayer.style.display = 'block';
      }
    }

    if (btnPhoto) btnPhoto.addEventListener('click', () => setMode('photo'));
    if (btnCad) btnCad.addEventListener('click', () => setMode('cad'));

    cardOpenBtns.forEach(el => {
      el.addEventListener('click', (e) => {
        const card = el.closest('.commission-card');
        if (card) {
          const pid = card.dataset.projectId || 'kv-01';
          openDrawer(pid);
        }
      });
    });

    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
    if (backdrop) backdrop.addEventListener('click', closeDrawer);

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && drawer.classList.contains('open')) {
        closeDrawer();
      }
    });
  }

  // 4. MECHANICAL & MATERIAL ATELIER
  function initMechanicalLab() {
    const specimenCards = document.querySelectorAll('.specimen-card');
    const lightBtns = document.querySelectorAll('.lighting-btn');
    const activeTitle = document.getElementById('lab-active-title');
    const activeSubtitle = document.getElementById('lab-active-subtitle');
    const specAlloy = document.getElementById('spec-alloy');
    const specFinish = document.getElementById('spec-finish');
    const specStrength = document.getElementById('spec-strength');
    const specAcoustic = document.getElementById('spec-acoustic');
    const labCanvas = document.getElementById('lab-preview-canvas');

    specimenCards.forEach(card => {
      card.addEventListener('click', () => {
        specimenCards.forEach(c => {
          c.classList.remove('active');
          c.setAttribute('aria-selected', 'false');
        });
        card.classList.add('active');
        card.setAttribute('aria-selected', 'true');

        const key = card.dataset.specimen;
        const data = SPECIMEN_DATA[key];
        if (data) {
          if (activeTitle) activeTitle.textContent = data.title;
          if (activeSubtitle) activeSubtitle.textContent = data.subtitle;
          if (specAlloy) specAlloy.textContent = data.alloy;
          if (specFinish) specFinish.textContent = data.finish;
          if (specStrength) specStrength.textContent = data.strength;
          if (specAcoustic) specAcoustic.textContent = data.acoustic;
        }
      });
    });

    lightBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        lightBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const light = btn.dataset.light;
        if (labCanvas) {
          if (light === 'tungsten') {
            labCanvas.style.filter = 'sepia(0.25) contrast(1.1)';
          } else if (light === 'noon') {
            labCanvas.style.filter = 'brightness(1.15) contrast(1.05)';
          } else {
            labCanvas.style.filter = 'none';
          }
        }
      });
    });
  }

  // 5. MOBILE NAVIGATION DRAWER
  function initMobileNav() {
    const toggleBtn = document.getElementById('mobile-menu-toggle');
    const closeBtn = document.getElementById('mobile-close-btn');
    const drawer = document.getElementById('mobile-nav-drawer');
    const mobileLinks = document.querySelectorAll('.mobile-link');

    function openNav() {
      drawer.classList.add('open');
      drawer.setAttribute('aria-hidden', 'false');
      toggleBtn.setAttribute('aria-expanded', 'true');
    }

    function closeNav() {
      drawer.classList.remove('open');
      drawer.setAttribute('aria-hidden', 'true');
      toggleBtn.setAttribute('aria-expanded', 'false');
    }

    if (toggleBtn) toggleBtn.addEventListener('click', openNav);
    if (closeBtn) closeBtn.addEventListener('click', closeNav);
    mobileLinks.forEach(link => link.addEventListener('click', closeNav));
  }

  // 6. COMMISSION CONSULTATION FORM
  function initConsultationForm() {
    const form = document.getElementById('commission-form');
    const successBox = document.getElementById('form-success-message');
    const triggers = document.querySelectorAll('.btn-inquire-trigger, #drawer-inquire-action');

    triggers.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const inqSec = document.getElementById('commission-inquiry');
        if (inqSec) {
          inqSec.scrollIntoView({ behavior: 'smooth' });
          const firstInput = inqSec.querySelector('input, select');
          if (firstInput) firstInput.focus();
        }
      });
    });

    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        form.style.display = 'none';
        if (successBox) successBox.style.display = 'block';
      });
    }
  }

})();
