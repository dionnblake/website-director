/**
 * VALENTIN & HESSE ARCHITECTS — PRODUCTION APP ENGINE
 * Handles portfolio filtering, dual-mode case study drawer,
 * material lab daylight simulation, and consultation intake.
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initProjectFilters();
  initCaseStudyDrawer();
  initMaterialLab();
  initInquiryForm();
  initHeaderScroll();
});

/* ==========================================================================
   1. MOBILE MENU TOGGLE
   ========================================================================== */
function initMobileMenu() {
  const toggleBtn = document.getElementById('mobile-menu-toggle');
  const closeBtn = document.getElementById('mobile-close-btn');
  const drawer = document.getElementById('mobile-nav-drawer');
  const links = document.querySelectorAll('.mobile-link');

  if (!toggleBtn || !drawer) return;

  function openMenu() {
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
    toggleBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    toggleBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  toggleBtn.addEventListener('click', openMenu);
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  drawer.addEventListener('click', (e) => {
    if (e.target === drawer) closeMenu();
  });

  links.forEach(link => {
    link.addEventListener('click', closeMenu);
  });
}

/* ==========================================================================
   2. SELECTED WORKS FILTER TABS
   ========================================================================== */
function initProjectFilters() {
  const tabs = document.querySelectorAll('.filter-tab');
  const cards = document.querySelectorAll('.project-card');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');

      const filter = tab.getAttribute('data-filter');

      cards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filter === 'all' || category === filter) {
          card.style.display = '';
          card.style.opacity = '1';
        } else {
          card.style.display = 'none';
          card.style.opacity = '0';
        }
      });
    });
  });
}

/* ==========================================================================
   3. DUAL-MODE PROJECT CASE STUDY DRAWER
   ========================================================================== */
const PROJECT_DATABASE = {
  p1: {
    title: "House of Three Monoliths",
    typology: "Alpine Primary Residence",
    location: "Vals, Grisons, Switzerland • 2024",
    scale: "780 m²",
    struct: "Reinforced Monolithic Concrete with 180mm Cavity Insulation & Valser Quartzite Masonry",
    energy: "Ground-Coupled Geothermal Probes, Controlled Heat Recovery Ventilation",
    joinery: "Custom Alpine Larch, Ceppo di Gré Stone, Acid-Etched Bronze",
    narrative: "Carved directly into a steep glacial slope, House of Three Monoliths is composed of three interlocking stone volumes that shield interior living quarters from alpine winter winds while opening completely to southern valley panoramas through deep recessed bronze glazing.",
    photoCaption: "Exterior South-Facing Elevation: Monolithic Valser Quartzite Massing",
    cadCaption: "Structural Section Drawing AA-1: Subterranean Geothermal & Thermal Core"
  },
  p2: {
    title: "Villa Travertine & Shadow",
    typology: "Lakeside Residence & Sculpture Pavilion",
    location: "Lake Lugano, Ticino, Switzerland • 2023",
    scale: "620 m²",
    struct: "Post-Tensioned White Concrete, Roman Navona Travertine Cladding",
    energy: "Lake-Source Water Heat Exchanger, Deep Shading Colonnades",
    joinery: "Natural Smoked Oak, Cast Fluted Glass, Hand-Finished Gunmetal Bronze",
    narrative: "A sequence of continuous travertine porticos extending toward the lake surface, dissolving the boundary between indoor living rooms and the water horizon. The home is designed around acoustic reflection and raking water light.",
    photoCaption: "Lakeside Portico: Navona Travertine Colonnade with Lake Lugano Reflection",
    cadCaption: "Plan Drawing P-02: Water Horizon Axis & Shading Portico Geometry"
  },
  p3: {
    title: "The Engadin Barn Transformation",
    typology: "Adaptive Historic Heritage",
    location: "Zuoz, Upper Engadin, Switzerland • 2024",
    scale: "490 m²",
    struct: "Restored 17th-Century Glacial Boulder Masonry with Self-Supporting Timber Infill",
    energy: "Passive-House Airtightness Membrane with Lime Plaster Vapor Permeability",
    joinery: "Charred Alpine Fir, Hand-Hewn Larch Beams, Polished Mineral Screed",
    narrative: "A 350-year-old Engadiner barn meticulously restored through a 'box-within-a-box' timber structure, preserving historical sgraffito exterior plaster while introducing contemporary passive-house thermal performance.",
    photoCaption: "Restored Sgraffito Facade: Deep Funnel Splayed Windows in 17th-c Stone",
    cadCaption: "Section BB-3: Self-Supporting Independent Timber Frame Inside Historic Stone"
  },
  p4: {
    title: "Brera Atelier & Penthouse",
    typology: "Urban Interior Architecture",
    location: "Milan, Italy • 2025",
    scale: "340 m²",
    struct: "Historic Brick Masonry Retrofit with Concealed Structural Steel Flitch Plates",
    energy: "Variable Refrigerant Flow Integrated into Custom Millwork Plinths",
    joinery: "Natural Canaletto Walnut, Ceppo di Gré Stone, Waxed Darkened Steel",
    narrative: "A double-height artist residence centered around a monolithic Ceppo di Gré hearth and custom floor-to-ceiling walnut library joinery. Light enters through restored arched windows and fluted glass partitions.",
    photoCaption: "Double-Height Great Room: Ceppo di Gré Hearth & Integrated Walnut Library",
    cadCaption: "Reflected Ceiling & Joinery Plan RC-01: Micro-Aperture Lighting Grid"
  },
  p5: {
    title: "Alpine Pavilion St. Moritz",
    typology: "Alpine Residential Retreat",
    location: "St. Moritz, Engadin, Switzerland • 2026",
    scale: "850 m²",
    struct: "Pre-Cast Engadin Granite Panels on Hybrid CLT Timber Superstructure",
    energy: "Solar Thermal Roof Integration with Biomass Pellet Auxiliary System",
    joinery: "Rough-Sawn Swiss Stone Pine (Arve), Brushed Bronze, Honed Basalt",
    narrative: "Perched above the lake of St. Moritz, this residential retreat features a cantilevered living room framed by rough-sawn pine and panoramic low-iron glass, celebrating the alpine landscape in all seasons.",
    photoCaption: "Winter Elevation: Granite Cantilever Emerging from Alpine Larch Forest",
    cadCaption: "Structural Cantilever Detail CD-04: Tension Tie-Backs into Solid Granite Bedrock"
  },
  p6: {
    title: "Lake Como Boat House",
    typology: "Waterfront Pavilion",
    location: "Bellagio, Lake Como, Italy • 2022",
    scale: "280 m²",
    struct: "Submerged Reinforced Concrete Cradle with Local Moltrasio Stone Masonry",
    energy: "Passive Lake Cooling & Natural Cross-Ventilation Flues",
    joinery: "Marine-Grade Teak, Acid-Treated Gunmetal Hardware",
    narrative: "A private boat shelter and summer living pavilion sitting directly in the waters of Lake Como, celebrating the historical stone boathouse vernacular of Northern Italy.",
    photoCaption: "Water Gate: Moltrasio Stone Arches Meeting the Lake Surface",
    cadCaption: "Submerged Section WS-01: Hydrostatic Water Gate & Mooring Cradle"
  }
};

function initCaseStudyDrawer() {
  const drawer = document.getElementById('case-study-drawer');
  const backdrop = document.getElementById('drawer-backdrop');
  const closeBtn = document.getElementById('drawer-close-btn');
  const triggers = document.querySelectorAll('.open-case-study, .project-card');

  const titleEl = document.getElementById('drawer-project-title');
  const typologyEl = document.getElementById('drawer-typology');
  const locationEl = document.getElementById('drawer-location');
  const narrativeEl = document.getElementById('drawer-narrative-p');
  const scaleEl = document.getElementById('drawer-spec-scale');
  const structEl = document.getElementById('drawer-spec-struct');
  const energyEl = document.getElementById('drawer-spec-energy');
  const joineryEl = document.getElementById('drawer-spec-joinery');

  const btnPhoto = document.getElementById('btn-view-photo');
  const btnCad = document.getElementById('btn-view-cad');
  const layerPhoto = document.getElementById('layer-photo');
  const layerCad = document.getElementById('layer-cad');
  const photoCaption = document.getElementById('photo-caption');
  const cadCaption = document.getElementById('cad-caption');

  if (!drawer) return;

  function openDrawer(projectId) {
    const data = PROJECT_DATABASE[projectId] || PROJECT_DATABASE.p1;

    titleEl.textContent = data.title;
    typologyEl.textContent = data.typology;
    locationEl.textContent = data.location;
    narrativeEl.textContent = data.narrative;
    scaleEl.textContent = data.scale;
    structEl.textContent = data.struct;
    energyEl.textContent = data.energy;
    joineryEl.textContent = data.joinery;
    photoCaption.textContent = data.photoCaption;
    cadCaption.textContent = data.cadCaption;

    // Reset to photo view
    setPerspectiveView('photo');

    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  function setPerspectiveView(mode) {
    if (mode === 'photo') {
      btnPhoto.classList.add('active');
      btnCad.classList.remove('active');
      layerPhoto.style.display = 'block';
      layerCad.style.display = 'none';
    } else {
      btnCad.classList.add('active');
      btnPhoto.classList.remove('active');
      layerCad.style.display = 'block';
      layerPhoto.style.display = 'none';
    }
  }

  triggers.forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      // Avoid firing if clicked on inner inquiry link
      if (e.target.closest('.drawer-inquire-link')) return;

      const card = trigger.closest('.project-card') || trigger;
      const id = card.getAttribute('data-id') || 'p1';
      openDrawer(id);
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (backdrop) backdrop.addEventListener('click', closeDrawer);

  if (btnPhoto && btnCad) {
    btnPhoto.addEventListener('click', () => setPerspectiveView('photo'));
    btnCad.addEventListener('click', () => setPerspectiveView('cad'));
  }

  // Escape key closes drawer
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer.classList.contains('open')) {
      closeDrawer();
    }
  });

  // Drawer inquire link smooth close
  const drawerInquireLink = document.getElementById('drawer-inquire-link');
  if (drawerInquireLink) {
    drawerInquireLink.addEventListener('click', () => {
      closeDrawer();
    });
  }
}

/* ==========================================================================
   4. MATERIAL & LIGHT LABORATORY
   ========================================================================== */
const SPECIMEN_DATABASE = {
  quartzite: {
    title: "Valser Quartzite",
    subtitle: "Metamorphic Mica-Schist Quartzite • Waterjet Honed",
    texture: "Dense, mica-flecked metamorphic slate with cool thermal inertia and subtle grey-green veining.",
    role: "Foundation massing walls, monolithic thermal hearths, integrated wet-room basins.",
    sensory: "Acoustic absorption, high thermal storage, velvety honed mineral finish.",
    color: "#6E7574"
  },
  travertine: {
    title: "Travertine Navona",
    subtitle: "Tivoli Open-Pore Limestone • Cross-Cut Honed Matte",
    texture: "Warm bone-white limestone with cellular sediment ribbons; reflects soft, indirect ambient daylight.",
    role: "Monolithic colonnades, interior floor slabs, exterior sheltered courtyards.",
    sensory: "Diffuse daylight dispersion, velvety soft barefoot touch, natural micro-porosity.",
    color: "#D8CEBE"
  },
  larch: {
    title: "End-Grain Alpine Larch",
    subtitle: "High-Altitude Swiss Larix Decidua • Organic Beeswax Sealed",
    texture: "Tight growth rings with dense resinous grain; ages over decades into a dignified silver-grey patina.",
    role: "Structural roof trusses, custom acoustic wall cladding, seamless ceiling planes.",
    sensory: "Subtle natural resin fragrance, high tactile warmth, superior acoustic damping.",
    color: "#B88E5E"
  },
  bronze: {
    title: "Hand-Brushed Bronze",
    subtitle: "Brianza Foundry Alloy • Chemical Liver-of-Sulphur Patina",
    texture: "Deep warm metallic hue with subtle olive-black undertones; velvet-soft tactile touch.",
    role: "Glazing frames, pivot door hardware, custom lighting apertures, structural tension rods.",
    sensory: "Weighty mechanical precision, tactile cool-to-warm touch, living natural oxidation.",
    color: "#594D3E"
  }
};

function initMaterialLab() {
  const buttons = document.querySelectorAll('.specimen-button');
  const titleEl = document.getElementById('display-spec-title');
  const subtitleEl = document.getElementById('display-spec-subtitle');
  const textureEl = document.getElementById('spec-val-texture');
  const roleEl = document.getElementById('spec-val-role');
  const sensoryEl = document.getElementById('spec-val-sensory');
  const baseFill = document.getElementById('spec-base-fill');
  const visualBox = document.getElementById('specimen-visual-box');
  const lightButtons = document.querySelectorAll('.btn-daylight');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      const key = btn.getAttribute('data-specimen');
      const data = SPECIMEN_DATABASE[key];
      if (!data) return;

      titleEl.textContent = data.title;
      subtitleEl.textContent = data.subtitle;
      textureEl.textContent = data.texture;
      roleEl.textContent = data.role;
      sensoryEl.textContent = data.sensory;

      if (baseFill) {
        baseFill.setAttribute('fill', data.color);
      }
    });
  });

  lightButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      lightButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const light = btn.getAttribute('data-light');
      if (!visualBox) return;

      visualBox.classList.remove('daylight-morning', 'daylight-noon', 'daylight-sunset');
      visualBox.classList.add(`daylight-${light}`);

      const overlay = document.getElementById('spec-light-overlay');
      if (!overlay) return;

      if (light === 'morning') {
        visualBox.style.filter = 'brightness(1.02) contrast(1.05) sepia(0.08)';
      } else if (light === 'noon') {
        visualBox.style.filter = 'brightness(1.15) contrast(1.1) sepia(0)';
      } else if (light === 'sunset') {
        visualBox.style.filter = 'brightness(0.92) contrast(1.12) sepia(0.28) saturate(1.2)';
      }
    });
  });
}

/* ==========================================================================
   5. PRIVATE CONSULTATION INTAKE FORM
   ========================================================================== */
function initInquiryForm() {
  const form = document.getElementById('consultation-form');
  const banner = document.getElementById('form-success-banner');
  const submitBtn = document.getElementById('submit-inquiry-btn');

  // Trigger buttons that scroll to consultation
  const inqTriggers = document.querySelectorAll('.btn-inquire-trigger');
  inqTriggers.forEach(btn => {
    btn.addEventListener('click', () => {
      const inqSection = document.getElementById('inquiry');
      if (inqSection) {
        inqSection.scrollIntoView({ behavior: 'smooth' });
        const firstInput = inqSection.querySelector('input[type="text"]');
        if (firstInput) firstInput.focus();
      }
    });
  });

  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    let isValid = true;
    const requiredFields = [
      { id: 'inquiry-location', errId: 'err-location' },
      { id: 'inquiry-timeline', errId: 'err-timeline' },
      { id: 'inquiry-name', errId: 'err-name' },
      { id: 'inquiry-email', errId: 'err-email', isEmail: true }
    ];

    requiredFields.forEach(field => {
      const input = document.getElementById(field.id);
      const err = document.getElementById(field.errId);
      const group = input.closest('.form-group');

      let val = input.value.trim();
      let fieldValid = val.length > 0;

      if (field.isEmail && fieldValid) {
        fieldValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
      }

      if (!fieldValid) {
        isValid = false;
        if (group) group.classList.add('has-error');
      } else {
        if (group) group.classList.remove('has-error');
      }
    });

    if (isValid) {
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Transmitting Brief...";
      }

      setTimeout(() => {
        if (banner) banner.style.display = 'flex';
        form.reset();
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = "Submit Spatial Brief for Review →";
        }
      }, 600);
    }
  });
}

/* ==========================================================================
   6. HEADER SCROLL BEHAVIOR
   ========================================================================== */
function initHeaderScroll() {
  const header = document.getElementById('atelier-header');
  let lastScroll = 0;

  window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    if (currentScroll > 120 && currentScroll > lastScroll) {
      // Scrolling down -> hide header
      header.style.transform = 'translateY(-100%)';
    } else {
      // Scrolling up -> show header
      header.style.transform = 'translateY(0)';
    }
    lastScroll = currentScroll;
  }, { passive: true });
}
