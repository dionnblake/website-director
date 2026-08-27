/**
 * KESTREL & ROWE Chronométrie Navale — Interactive Application
 * Official GSAP Motion Implementation Engine Architecture
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Scoped GSAP Context with Reduced Motion Architecture
  const ctx = gsap.context(() => {
    const mm = gsap.matchMedia();

    // Standard Desktop & Motion Enabled
    mm.add('(prefers-reduced-motion: no-preference)', () => {
      // Hero Entrance Timeline
      const heroTl = gsap.timeline({ defaults: { ease: 'power3.out', duration: 0.9 } });
      heroTl
        .from('.hero-copy > *', { y: 25, autoAlpha: 0, stagger: 0.12 })
        .from('.hero-dial', { scale: 0.95, autoAlpha: 0, duration: 1.1 }, '<0.2');

      // Metric Strip Reveal
      gsap.from('.metric-cell', {
        scrollTrigger: {
          trigger: '#telemetry',
          start: 'top 85%'
        },
        y: 20,
        autoAlpha: 0,
        stagger: 0.1,
        duration: 0.7,
        ease: 'power2.out'
      });

      // Feature Architecture Cards
      gsap.from('.feature-card', {
        scrollTrigger: {
          trigger: '#escapement',
          start: 'top 75%'
        },
        y: 30,
        autoAlpha: 0,
        stagger: 0.15,
        duration: 0.8,
        ease: 'power2.out'
      });

      // Continuous Escapement Balance Wheel Ticking
      gsap.to('.balance-wheel-anim', {
        rotation: 360,
        repeat: -1,
        ease: 'none',
        duration: 12
      });

      // Ticking Second Hand
      gsap.to('#secondHand', {
        rotation: '+=360',
        repeat: -1,
        ease: 'steps(60)',
        duration: 60,
        transformOrigin: '50% 50%'
      });
    });

    // Reduced Motion Fallback (Instant Subtle Fade, No Translation)
    mm.add('(prefers-reduced-motion: reduce)', () => {
      gsap.from('.hero-copy, .hero-dial, .metric-cell, .feature-card', {
        autoAlpha: 0,
        duration: 0.2,
        ease: 'none'
      });
    });

  });

  // 2. Live Sea-Motion Gimbal Simulator
  const seaSlider = document.getElementById('seaStateSlider');
  const seaValue = document.getElementById('seaStateValue');
  const outerRing = document.getElementById('outerRing');
  const innerRing = document.getElementById('innerRing');
  const waveHorizon = document.getElementById('waveHorizon');
  const gimbalAngle = document.getElementById('gimbalAngle');
  const driftRate = document.getElementById('driftRate');
  const secondsCounter = document.getElementById('liveSecondsCounter');

  const BEAUFORT_LABELS = [
    "Force 0 (Mirror Calm)",
    "Force 1 (Light Air)",
    "Force 2 (Light Breeze)",
    "Force 3 (Gentle Breeze)",
    "Force 4 (Moderate Sea)",
    "Force 5 (Fresh Sea)",
    "Force 6 (Strong Breeze)",
    "Force 7 (Near Gale)",
    "Force 8 (Gale)",
    "Force 9 (Severe Storm)"
  ];

  if (seaSlider) {
    seaSlider.addEventListener('input', (e) => {
      const val = parseInt(e.target.value, 10);
      seaValue.textContent = BEAUFORT_LABELS[val];
      
      const pitchAngle = val * 3.8;
      const rollAngle = val * -2.6;
      
      gimbalAngle.textContent = `${pitchAngle.toFixed(1)}°`;
      driftRate.textContent = `+${(0.002 + val * 0.002).toFixed(3)} s/day`;
      
      if (outerRing && innerRing && waveHorizon) {
        outerRing.style.transform = `rotate(${rollAngle}deg)`;
        innerRing.style.transform = `rotate(${pitchAngle}deg)`;
        waveHorizon.style.transform = `scale(${1 + val * 0.05}) translateY(${val * 4}px)`;
      }
    });
  }

  // Live Digital Seconds Clock
  setInterval(() => {
    if (secondsCounter) {
      const now = new Date();
      const hrs = String(now.getUTCHours()).padStart(2, '0');
      const mins = String(now.getUTCMinutes()).padStart(2, '0');
      const secs = String(now.getUTCSeconds()).padStart(2, '0');
      secondsCounter.textContent = `${hrs}:${mins}:${secs}Z`;
    }
  }, 1000);

  // 3. Commission Form Handler
  window.handleCommissionSubmit = function() {
    const form = document.getElementById('commissionForm');
    const msg = document.getElementById('formSuccessMessage');
    const btn = document.getElementById('submitBtn');
    
    if (btn) btn.disabled = true;
    if (msg) msg.classList.remove('hidden');
  };

  // Expose Teardown
  window.__KESTREL_CLEANUP__ = () => ctx.revert();
});
