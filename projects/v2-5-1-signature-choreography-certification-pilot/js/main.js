// ARC//FORGE SIGNATURE CHOREOGRAPHY ENGINE (V2.5.1)
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
