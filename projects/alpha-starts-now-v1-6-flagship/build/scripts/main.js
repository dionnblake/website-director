/**
 * Alpha Starts Now — Luxury Editorial Atelier (V1.7 Elite)
 * Lenis Inertial Momentum + GSAP 3 Kinetic Choreography Engine
 */

(function () {
  'use strict';

  // Check user motion preferences
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ==========================================================================
  // 1. LENIS SMOOTH INERTIAL SCROLL & GSAP TICKER BINDING
  // ==========================================================================
  let lenis = null;

  function initLenisScroll() {
    if (prefersReducedMotion || typeof window.Lenis === 'undefined') return;

    lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // Exponential ease-out
      direction: 'vertical',
      gestureDirection: 'vertical',
      smooth: true,
      mouseMultiplier: 1.0,
      smoothTouch: false, // Maintain native touch on mobile
      touchMultiplier: 2,
      infinite: false,
    });

    if (window.ScrollTrigger) {
      lenis.on('scroll', ScrollTrigger.update);

      gsap.ticker.add((time) => {
        lenis.raf(time * 1000);
      });

      gsap.ticker.lagSmoothing(0);
    }
  }

  // ==========================================================================
  // 2. CUSTOM MAGNETIC CURSOR ENGINE
  // ==========================================================================
  function initMagneticCursor() {
    const cursor = document.getElementById('custom-cursor');
    const cursorDot = document.getElementById('custom-cursor-dot');
    if (!cursor || !cursorDot || prefersReducedMotion || window.innerWidth <= 992) return;

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let cursorX = mouseX;
    let cursorY = mouseY;

    window.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      gsap.to(cursorDot, { x: mouseX, y: mouseY, duration: 0.1, ease: 'power2.out' });
    });

    // Lerp loop for smooth cursor trailing
    gsap.ticker.add(() => {
      cursorX += (mouseX - cursorX) * 0.18;
      cursorY += (mouseY - cursorY) * 0.18;
      cursor.style.transform = `translate3d(${cursorX}px, ${cursorY}px, 0) translate(-50%, -50%)`;
    });

    // Cursor Hover Expansion
    const interactiveTargets = document.querySelectorAll('a, button, .btn, .pillar-luxury-card, .spec-luxury-card, .commitment-card, .codex-luxury-row, input, [data-magnetic]');
    interactiveTargets.forEach(el => {
      el.addEventListener('mouseenter', () => cursor.classList.add('cursor-hover'));
      el.addEventListener('mouseleave', () => cursor.classList.remove('cursor-hover'));
    });

    // Magnetic Button Pull
    const magneticElements = document.querySelectorAll('[data-magnetic]');
    magneticElements.forEach(el => {
      el.addEventListener('mousemove', (e) => {
        const rect = el.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const deltaX = (e.clientX - centerX) * 0.3;
        const deltaY = (e.clientY - centerY) * 0.3;

        gsap.to(el, { x: deltaX, y: deltaY, duration: 0.35, ease: 'power2.out' });
      });

      el.addEventListener('mouseleave', () => {
        gsap.to(el, { x: 0, y: 0, duration: 0.7, ease: 'elastic.out(1, 0.4)' });
      });
    });
  }

  // ==========================================================================
  // 3. GSAP CHOREOGRAPHY & MASK REVEALS
  // ==========================================================================
  function initKinetics() {
    if (!window.gsap) return;
    if (window.ScrollTrigger) gsap.registerPlugin(ScrollTrigger);

    const ctx = gsap.context(() => {

      // A. Opening Hero Choreography
      if (!prefersReducedMotion) {
        const tlHero = gsap.timeline({ defaults: { ease: 'power4.out' } });

        tlHero
          .from('.brand-logo', { opacity: 0, x: -20, duration: 0.8 })
          .from('.nav-links li', { opacity: 0, y: -10, stagger: 0.06, duration: 0.6 }, '-=0.5')
          .from('.hero-hud-tag', { opacity: 0, scale: 0.94, duration: 0.6 }, '-=0.4')
          .to('.sec-hero .split-mask-heading .mask-inner', {
            y: '0%',
            duration: 1.2,
            stagger: 0.12,
            ease: 'power4.out'
          }, '-=0.4')
          .from('.hero-subtext', { opacity: 0, y: 20, duration: 0.8 }, '-=0.6')
          .from('.hero-actions .btn', { opacity: 0, y: 15, stagger: 0.12, duration: 0.7 }, '-=0.5')
          .from('.hero-telemetry-bar', { opacity: 0, y: 20, duration: 0.7 }, '-=0.5')
          .from('.hero-image-frame', { opacity: 0, scale: 0.95, y: 30, duration: 1.2, ease: 'power3.out' }, '-=1.0');

        // Number Counters
        ['counter-sleep', 'counter-strength', 'counter-focus'].forEach(id => {
          const el = document.getElementById(id);
          if (!el) return;
          const target = parseFloat(el.getAttribute('data-target')) || 0;
          const suffix = el.getAttribute('data-suffix') || '';
          const decimals = target % 1 !== 0 ? 1 : 0;
          const obj = { val: 0 };

          gsap.to(obj, {
            val: target,
            duration: 1.8,
            ease: 'power2.out',
            delay: 0.6,
            onUpdate: () => {
              el.textContent = decimals ? obj.val.toFixed(decimals) + suffix : Math.round(obj.val) + suffix;
            }
          });
        });
      } else {
        // Immediate reveal for reduced motion
        document.querySelectorAll('.split-mask-heading .mask-inner').forEach(el => {
          el.style.transform = 'translateY(0%)';
        });
      }

      // B. Split-Mask Headline Reveals on Scroll
      if (!prefersReducedMotion && window.ScrollTrigger) {
        document.querySelectorAll('section:not(.sec-hero) .split-mask-heading').forEach(heading => {
          const inners = heading.querySelectorAll('.mask-inner');
          gsap.to(inners, {
            y: '0%',
            duration: 1.1,
            stagger: 0.1,
            ease: 'power4.out',
            scrollTrigger: {
              trigger: heading,
              start: 'top 85%',
              toggleActions: 'play none none none'
            }
          });
        });

        // C. Section Stagger Reveals
        gsap.from('.commitment-card', {
          scrollTrigger: {
            trigger: '.manifesto-commitments-col',
            start: 'top 80%'
          },
          opacity: 0,
          x: 30,
          stagger: 0.15,
          duration: 0.8,
          ease: 'power3.out'
        });

        gsap.from('.pillar-luxury-card', {
          scrollTrigger: {
            trigger: '.pillars-luxury-grid',
            start: 'top 80%'
          },
          opacity: 0,
          y: 40,
          stagger: 0.12,
          duration: 0.8,
          ease: 'power3.out'
        });

        gsap.from('.spec-luxury-card', {
          scrollTrigger: {
            trigger: '.arsenal-grid',
            start: 'top 80%'
          },
          opacity: 0,
          y: 35,
          stagger: 0.1,
          duration: 0.7,
          ease: 'power3.out'
        });

        gsap.from('.codex-luxury-row', {
          scrollTrigger: {
            trigger: '.codex-luxury-list',
            start: 'top 80%'
          },
          opacity: 0,
          x: -25,
          stagger: 0.12,
          duration: 0.7,
          ease: 'power3.out'
        });
      }

      // D. Horizontal Pinned 7-Day Protocol Scrollytelling Track
      const track = document.getElementById('horizontal-track');
      const scrollyOuter = document.getElementById('horizontal-scrolly-outer');
      const protocolSec = document.getElementById('sec-protocol');

      if (track && scrollyOuter && protocolSec && window.innerWidth > 992 && !prefersReducedMotion && window.ScrollTrigger) {
        const totalWidth = track.scrollWidth - window.innerWidth + 140;

        gsap.to(track, {
          x: () => -totalWidth,
          ease: 'none',
          scrollTrigger: {
            trigger: protocolSec,
            pin: true,
            scrub: 1.2,
            start: 'top 10%',
            end: () => `+=${totalWidth}`,
            invalidateOnRefresh: true
          }
        });
      }

      // E. Nav Scroll & Active Section Spy
      const navEl = document.querySelector('.tactical-nav');
      const navLinks = document.querySelectorAll('.nav-link');
      const sections = document.querySelectorAll('section[id]');

      window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
          navEl.classList.add('scrolled');
        } else {
          navEl.classList.remove('scrolled');
        }

        let currentSectionId = '';
        sections.forEach(sec => {
          const secTop = sec.offsetTop - 150;
          const secHeight = sec.offsetHeight;
          if (window.scrollY >= secTop && window.scrollY < secTop + secHeight) {
            currentSectionId = sec.getAttribute('id');
          }
        });

        navLinks.forEach(link => {
          const href = link.getAttribute('href');
          if (href === '#' + currentSectionId) {
            link.classList.add('active-section');
          } else {
            link.classList.remove('active-section');
          }
        });
      }, { passive: true });

    });

    window.__gsapContext = ctx;
  }

  // ==========================================================================
  // 4. ARSENAL FILTER TABS
  // ==========================================================================
  function initArsenalFilters() {
    const buttons = document.querySelectorAll('.filter-tab-btn');
    const cards = document.querySelectorAll('.spec-luxury-card');

    buttons.forEach(btn => {
      btn.addEventListener('click', function () {
        const filter = this.getAttribute('data-filter');

        buttons.forEach(b => b.classList.remove('active'));
        this.classList.add('active');

        cards.forEach(card => {
          const category = card.getAttribute('data-category');
          if (filter === 'all' || category === filter) {
            card.style.display = 'flex';
            gsap.fromTo(card, { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: 0.4, ease: 'power2.out' });
          } else {
            card.style.display = 'none';
          }
        });

        if (window.ScrollTrigger) ScrollTrigger.refresh();
      });
    });
  }

  // ==========================================================================
  // 5. INTERACTIVE CALIBRATION ENGINE
  // ==========================================================================
  function initCalibrationEngine() {
    const sliderAge = document.getElementById('slider-age');
    const sliderTraining = document.getElementById('slider-training');
    const valAge = document.getElementById('val-age');
    const valTraining = document.getElementById('val-training');

    const resCadence = document.getElementById('res-cadence');
    const resSleep = document.getElementById('res-sleep');
    const resProtein = document.getElementById('res-protein');
    const resFocus = document.getElementById('res-focus');

    if (!sliderAge || !sliderTraining) return;

    function updateCalculator() {
      const age = parseInt(sliderAge.value, 10);
      const hours = parseInt(sliderTraining.value, 10);

      valAge.textContent = `${age} YRS`;
      valTraining.textContent = `${hours} HOURS / WK`;

      // Reactive Calculation Logic
      if (hours <= 3) {
        resCadence.textContent = '2 Heavy Axial Days';
      } else if (hours <= 5) {
        resCadence.textContent = '3 Compound Lifting Days';
      } else {
        resCadence.textContent = '4 Split Hypertrophy Days';
      }

      if (age >= 45) {
        resSleep.textContent = '66°F Deep Cold Floor';
        resProtein.textContent = '200g High-Leucine Target';
      } else {
        resSleep.textContent = '68°F Optimal Ambient';
        resProtein.textContent = '180g Balanced Animal Base';
      }

      if (hours >= 5) {
        resFocus.textContent = '3x 90m Monotask Blocks';
      } else {
        resFocus.textContent = '2x 90m Deep Work Blocks';
      }
    }

    sliderAge.addEventListener('input', updateCalculator);
    sliderTraining.addEventListener('input', updateCalculator);
    updateCalculator();
  }

  // ==========================================================================
  // 6. DOSSIER DISPATCH FORM
  // ==========================================================================
  function initDispatchForm() {
    const form = document.getElementById('reset-form');
    const feedback = document.getElementById('reset-feedback');

    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        const input = document.getElementById('reset-email');
        if (input && input.value.trim()) {
          input.value = '';
          if (feedback) {
            feedback.textContent = '✓ 7-DAY RESET DOSSIER DISPATCHED // CHECK INBOX';
            feedback.style.color = 'var(--accent-gold)';
            feedback.style.display = 'block';
          }
        }
      });
    }
  }

  // ==========================================================================
  // INITIALIZATION
  // ==========================================================================
  document.addEventListener('DOMContentLoaded', () => {
    initLenisScroll();
    initMagneticCursor();
    initKinetics();
    initArsenalFilters();
    initCalibrationEngine();
    initDispatchForm();
  });

})();
