/**
 * SÖLVIK FJORD RETREAT & THERMAL SANCTUARY
 * Interactive Client-Side Engine
 * Schema Version: 1.1.0 | Website Director V1.1
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. DATA DICTIONARY FOR PAVILIONS
  const pavilionData = {
    cliff: {
      title: 'The Cliff Pavilion',
      specs: '85 m² · 1 King Bed · Maximum 2 Guests · 180° Fjord Panorama',
      badge: '12 Keys · 85 m² · Hovering 14m Above Water',
      image: 'assets/images/pavilion_cliff.jpg',
      desc: 'Hovering 14 meters directly above the fjord with frameless triple-glazed panoramic glass, a hand-carved dark granite wood-fired soaking tub, charred pine millwork, and custom Norwegian wool linens.',
      rate: 'From €2,850 / Night',
      amenities: [
        'Granite Soaking Tub',
        'Open Hearth Fireplace',
        'Triple-Glazed Glass',
        'Private Morning Terrace'
      ]
    },
    villa: {
      title: 'The Fjord Villa',
      specs: '140 m² · Split-Level · 1 King + Daybed · Maximum 3 Guests',
      badge: '10 Keys · 140 m² · Private Cedar Sauna',
      image: 'assets/images/hero_fjord_pavilion.jpg',
      desc: 'Split-level architectural sanctuary anchored into solid granite rock face. Features a private dry cedar sauna, heated slate floors, panoramic double-sided hearth fireplace, and a cantilevered outdoor lounge terrace.',
      rate: 'From €3,950 / Night',
      amenities: [
        'Private Cedar Sauna',
        'Double Granite Hearth',
        'Outdoor Daybed',
        'Climate Wine Storage'
      ]
    },
    sanctuary: {
      title: 'The Sanctuary Residence',
      specs: '260 m² · 2 Master Suites · Maximum 4 Guests · Private Mooring',
      badge: '6 Keys · 260 m² · Dual Geothermal Plunge Pools',
      image: 'assets/images/thermal_springs.jpg',
      desc: 'Our premier multi-suite estate residence featuring dual geothermal outdoor plunge pools, private chef hearth kitchen, dedicated butler pantry, and direct private boat slip into Storfjorden.',
      rate: 'From €6,200 / Night',
      amenities: [
        'Dual Geothermal Plunges',
        'Private Chef Hearth',
        'Direct Fjord Mooring',
        'Dedicated Host Concierge'
      ]
    }
  };

  // 2. PAVILION TAB SWITCHER
  const tabButtons = document.querySelectorAll('.pavilion-tab-btn');
  const pavTitle = document.getElementById('pavilionTitle');
  const pavSpecs = document.getElementById('pavilionSpecs');
  const pavBadge = document.getElementById('pavilionBadge');
  const pavImage = document.getElementById('pavilionImage');
  const pavDesc = document.getElementById('pavilionDesc');
  const pavRate = document.getElementById('pavilionRate');
  const pavAmenities = document.getElementById('pavilionAmenities');
  const drawerPavSelect = document.getElementById('drawerPavilionSelect');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const type = btn.getAttribute('data-pavilion');
      const data = pavilionData[type];
      if (!data) return;

      // Update active tab button
      tabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Update text and specs immediately
      pavTitle.textContent = data.title;
      pavSpecs.textContent = data.specs;
      pavBadge.textContent = data.badge;
      pavDesc.textContent = data.desc;
      pavRate.textContent = data.rate;

      // Render amenities
      pavAmenities.innerHTML = data.amenities.map(item => `
        <div class="amenity-item">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 13l4 4L19 7"/></svg>
          <span>${item}</span>
        </div>
      `).join('');

      // Cross-fade image
      pavImage.style.opacity = '0.4';
      setTimeout(() => {
        pavImage.src = data.image;
        pavImage.style.opacity = '1';
      }, 100);

      // Sync with drawer selector
      if (drawerPavSelect) {
        drawerPavSelect.value = type;
      }
    });
  });

  // 3. PLAN YOUR STAY DRAWER CONTROLS
  const stayDrawer = document.getElementById('stayDrawer');
  const closeDrawerBtn = document.getElementById('closeDrawerBtn');
  const openDrawerTriggers = [
    document.getElementById('openDrawerNavBtn'),
    document.getElementById('heroPlanStayBtn'),
    document.getElementById('reservePavilionTriggerBtn'),
    document.getElementById('footerPlanStayBtn'),
    document.getElementById('openDiningInquiryBtn')
  ].filter(Boolean);

  function openDrawer(pavilionType = null) {
    if (pavilionType && drawerPavSelect) {
      drawerPavSelect.value = pavilionType;
    }
    stayDrawer.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    stayDrawer.classList.remove('open');
    document.body.style.overflow = '';
  }

  openDrawerTriggers.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      // If triggered from pavilion configure button, pass current active tab
      const activeTab = document.querySelector('.pavilion-tab-btn.active');
      const activeType = activeTab ? activeTab.getAttribute('data-pavilion') : 'cliff';
      openDrawer(activeType);
    });
  });

  if (closeDrawerBtn) {
    closeDrawerBtn.addEventListener('click', closeDrawer);
  }

  // Close drawer when clicking outside panel
  if (stayDrawer) {
    stayDrawer.addEventListener('click', (e) => {
      if (e.target === stayDrawer) {
        closeDrawer();
      }
    });
  }

  // 4. SEASON OPTION RADIO SELECTION
  const seasonOptions = document.querySelectorAll('.season-option');
  seasonOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      seasonOptions.forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      const radio = opt.querySelector('input[type="radio"]');
      if (radio) radio.checked = true;
    });
  });

  // 5. INQUIRY FORM SUBMISSION
  const stayForm = document.getElementById('stayInquiryForm');
  const successMsg = document.getElementById('inquirySuccessMsg');

  if (stayForm) {
    stayForm.addEventListener('submit', (e) => {
      e.preventDefault();
      stayForm.style.display = 'none';
      if (successMsg) {
        successMsg.style.display = 'block';
      }
    });
  }

  // 6. STICKY NAV SCROLL EFFECT
  const mainNav = document.getElementById('mainNav');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      mainNav.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.6)';
      mainNav.style.borderBottomColor = 'rgba(200, 131, 70, 0.3)';
    } else {
      mainNav.style.boxShadow = 'none';
      mainNav.style.borderBottomColor = 'rgba(244, 241, 234, 0.08)';
    }
  });

  // 7. MOBILE MENU TOGGLE
  const mobileToggle = document.getElementById('mobileMenuToggle');
  const navLinks = document.querySelector('.nav-links');
  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => {
      const isVisible = navLinks.style.display === 'flex';
      if (isVisible) {
        navLinks.style.display = 'none';
      } else {
        navLinks.style.display = 'flex';
        navLinks.style.flexDirection = 'column';
        navLinks.style.position = 'absolute';
        navLinks.style.top = '84px';
        navLinks.style.left = '0';
        navLinks.style.width = '100%';
        navLinks.style.background = 'rgba(14, 21, 26, 0.98)';
        navLinks.style.padding = '2rem';
        navLinks.style.borderBottom = '1px solid rgba(244, 241, 234, 0.15)';
      }
    });
  }
});
