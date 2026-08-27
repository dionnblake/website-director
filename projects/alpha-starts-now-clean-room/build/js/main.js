/**
 * Alpha Starts Now — Main GSAP Motion Engine & HUD Telemetry
 * Level 2 Kinetic Implementation
 */

(function () {
  'use strict';

  function initMotionAndTelemetry() {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Animated Telemetry Counters
    const counterElements = [
      { id: 'metric-sleep', target: 94, suffix: '%' },
      { id: 'metric-strength', target: 4.2, suffix: 'x', decimals: 1 },
      { id: 'metric-focus', target: 180, suffix: 'm' },
      { id: 'metric-command', target: 100, suffix: '%' }
    ];

    if (!prefersReducedMotion && window.gsap) {
      // Register GSAP ScrollTrigger if present
      if (window.ScrollTrigger) {
        gsap.registerPlugin(ScrollTrigger);
      }

      // Hero Timeline Entrance
      const tlHero = gsap.timeline({ defaults: { ease: 'power3.out' } });

      tlHero
        .from('.brand-logo', { opacity: 0, x: -20, duration: 0.5 })
        .from('.nav-link', { opacity: 0, y: -10, stagger: 0.08, duration: 0.4 }, '-=0.3')
        .from('.hero-hud-tag', { opacity: 0, scale: 0.95, duration: 0.4 }, '-=0.2')
        .from('.type-giant', { opacity: 0, y: 30, duration: 0.7 }, '-=0.2')
        .from('.hero-subtext', { opacity: 0, y: 20, duration: 0.5 }, '-=0.3')
        .from('.hero-actions .btn', { opacity: 0, y: 15, stagger: 0.1, duration: 0.4 }, '-=0.2')
        .from('.telemetry-box', { opacity: 0, x: 25, duration: 0.6 }, '-=0.5');

      // Metric Counter Animation
      counterElements.forEach(item => {
        const el = document.getElementById(item.id);
        if (!el) return;

        const obj = { val: 0 };
        gsap.to(obj, {
          val: item.target,
          duration: 1.6,
          ease: 'power2.out',
          scrollTrigger: {
            trigger: '.telemetry-box',
            start: 'top 85%'
          },
          onUpdate: function () {
            if (item.decimals) {
              el.textContent = obj.val.toFixed(item.decimals) + item.suffix;
            } else {
              el.textContent = Math.round(obj.val) + item.suffix;
            }
          }
        });
      });

      // Staggered Pillars ScrollTrigger
      if (window.ScrollTrigger) {
        gsap.from('.pillar-card', {
          scrollTrigger: {
            trigger: '.pillars-grid',
            start: 'top 80%'
          },
          opacity: 0,
          y: 35,
          stagger: 0.15,
          duration: 0.6,
          ease: 'power3.out'
        });

        gsap.from('.spec-sheet-card', {
          scrollTrigger: {
            trigger: '.arsenal-grid',
            start: 'top 80%'
          },
          opacity: 0,
          y: 25,
          stagger: 0.1,
          duration: 0.5,
          ease: 'power3.out'
        });

        gsap.from('.codex-row', {
          scrollTrigger: {
            trigger: '.codex-list',
            start: 'top 80%'
          },
          opacity: 0,
          x: -20,
          stagger: 0.12,
          duration: 0.5,
          ease: 'power2.out'
        });
      }
    } else {
      // Fallback for reduced motion or without GSAP
      counterElements.forEach(item => {
        const el = document.getElementById(item.id);
        if (el) {
          el.textContent = item.target + item.suffix;
        }
      });
    }

    // Form Handling Simulation (Covenant Enrollment)
    const covenantForm = document.getElementById('covenant-form');
    const covenantFeedback = document.getElementById('covenant-feedback');

    if (covenantForm) {
      covenantForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const input = document.getElementById('covenant-email');
        if (input && input.value.trim()) {
          input.value = '';
          if (covenantFeedback) {
            covenantFeedback.textContent = 'PROTOCOL DISPATCH CONFIRMED // ACCESS GRANTED AT 06:00 EST';
            covenantFeedback.style.color = 'var(--accent-amber)';
            covenantFeedback.style.display = 'block';
          }
        }
      });
    }
  }

  document.addEventListener('DOMContentLoaded', initMotionAndTelemetry);
})();
