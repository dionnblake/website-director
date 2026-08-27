/**
 * Alpha Starts Now — Discipline Calibration Engine
 * Signature Interactive Element (Decade Protocol Matrix)
 */

(function () {
  'use strict';

  const DECADE_DATA = {
    '30s': {
      badge: '// CALIBRATION PROTOCOL: DECADE 30S',
      headline: 'VELOCITY & METABOLIC HYPERTROPHY',
      description: 'In your 30s, biological elasticity remains high, but executive demands and family obligations peak. The protocol emphasizes high-density compound training, fast metabolic recovery, and ruthless cognitive prioritization to establish irreversible career and physical dominance.',
      specs: [
        {
          index: '01',
          title: 'Training Architecture: Hypertrophy & Density',
          detail: '4-day upper/lower split focusing on progressive barbell overload (RPE 8-9) with high-density supersets to maximize testosterone and muscle cross-sectional area in under 55 minutes.'
        },
        {
          index: '02',
          title: 'Metabolic & Nutrition Protocol',
          detail: '1.0g protein per lb of bodyweight. Strategic carbohydrate cycling aligned around heavy training sessions. Elimination of liquid sugars and evening alcohol to protect REM sleep.'
        },
        {
          index: '03',
          title: 'Cognitive & Time Defense',
          detail: 'Two 90-minute morning deep work blocks prior to checking communications. Delegation matrix designed to strip low-leverage operational tasks.'
        },
        {
          index: '04',
          title: 'Primary Arsenal Recommended',
          detail: 'Rogue Stainless Barbell + Concept2 Rower + Automatic Field Tool Watch for analog timeboxing.'
        }
      ]
    },
    '40s': {
      badge: '// CALIBRATION PROTOCOL: DECADE 40S',
      headline: 'STRENGTH PRESERVATION & JOINT INTEGRITY',
      description: 'In your 40s, wisdom meets peak earning power, but connective tissue recovery demands calculated precision. The protocol transitions from reckless volume to maximum mechanical tension with strict joint preservation, circadian temperature regulation, and executive boundary architecture.',
      specs: [
        {
          index: '01',
          title: 'Training Architecture: Heavy Low-Frequency Loading',
          detail: '3-day full-body compound split. Heavy top sets (80-85% 1RM) followed by unilateral dumbbell stability work and rotator cuff armor to eliminate shoulder and lumbar wear.'
        },
        {
          index: '02',
          title: 'Hormonal & Circadian Optimization',
          detail: 'Strict 68°F sleep environment with dual-zone active thermal cooling. Daily 15-minute natural sunlight exposure within 30 minutes of waking to anchor cortisol and melatonin rhythms.'
        },
        {
          index: '03',
          title: 'Cardiovascular Foundation: Zone 2',
          detail: '150 minutes weekly of dedicated Zone 2 aerobic base work (nasal breathing only) to preserve mitochondrial density and arterial elasticity without taxing systemic recovery.'
        },
        {
          index: '04',
          title: 'Primary Arsenal Recommended',
          detail: 'Eight Sleep Pod 4 Pro + Eleiko Kettlebells + Titanium Mechanical Chronograph.'
        }
      ]
    },
    '50s': {
      badge: '// CALIBRATION PROTOCOL: DECADE 50S+',
      headline: 'BIOLOGICAL LONGEVITY & SOVEREIGN MASTERY',
      description: 'In your 50s and beyond, the objective is uncompromising vitality, grip strength, cognitive sharpness, and sovereign legacy. You command your time, eliminate unnecessary friction, and maintain physical capabilities that outperform men half your age.',
      specs: [
        {
          index: '01',
          title: 'Training Architecture: Power, Grip & Bone Density',
          detail: 'Heavy loaded carries (trap bar farmer walks), explosive medicine ball throws, and axial spinal loading to preserve peak bone mineral density and elite grip force.'
        },
        {
          index: '02',
          title: 'Cellular Health & Mobility Armor',
          detail: 'Daily 20-minute hip and thoracic mobility flow. Time-restricted feeding window with high leucine pulsing to prevent age-related sarcopenia and maintain insulin sensitivity.'
        },
        {
          index: '03',
          title: 'Sovereign Capital & Mentorship Codex',
          detail: 'Allocating capital to unassailable hard assets. Transitioning from active tactical execution to high-leverage architectural governance and legacy stewardship.'
        },
        {
          index: '04',
          title: 'Primary Arsenal Recommended',
          detail: 'Sinn Pilot Tool Watch + Rogue Trap Bar + Oura Ring Horizon Gen 3.'
        }
      ]
    }
  };

  function initCalibrationEngine() {
    const tabs = document.querySelectorAll('.decade-tab-btn');
    const badgeEl = document.getElementById('cal-badge');
    const headlineEl = document.getElementById('cal-headline');
    const descEl = document.getElementById('cal-desc');
    const specListEl = document.getElementById('cal-specs');

    if (!tabs.length || !headlineEl) return;

    function renderDecade(decadeKey) {
      const data = DECADE_DATA[decadeKey];
      if (!data) return;

      tabs.forEach(tab => {
        const isActive = tab.getAttribute('data-decade') === decadeKey;
        tab.classList.toggle('active', isActive);
        tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });

      if (badgeEl) badgeEl.textContent = data.badge;
      headlineEl.textContent = data.headline;
      descEl.textContent = data.description;

      if (specListEl) {
        specListEl.innerHTML = '';
        data.specs.forEach(spec => {
          const li = document.createElement('li');
          li.className = 'protocol-spec-item';
          li.innerHTML = `
            <span class="spec-index">${spec.index}</span>
            <div class="spec-content">
              <h4>${spec.title}</h4>
              <p>${spec.detail}</p>
            </div>
          `;
          specListEl.appendChild(li);
        });
      }

      // If GSAP is available, trigger a clean mechanical reveal
      if (window.gsap && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        gsap.fromTo(
          '.calibration-display-panel',
          { opacity: 0.85, y: 6 },
          { opacity: 1, y: 0, duration: 0.25, ease: 'power2.out' }
        );
      }
    }

    tabs.forEach(tab => {
      tab.addEventListener('click', function () {
        const decadeKey = this.getAttribute('data-decade');
        renderDecade(decadeKey);
      });
    });

    // Initial render
    renderDecade('40s');
  }

  document.addEventListener('DOMContentLoaded', initCalibrationEngine);
})();
