/**
 * Alpha Starts Now (V1.1) — Core Client Engine
 * Authority: Website Director V1.1
 */

window.ASN_SITE = window.ASN_SITE || {};
window.ASN_SITE.config = {
  version: '2.0.0',
  leadEndpoint: '' // Set to live serverless endpoint in production
};

document.addEventListener('DOMContentLoaded', () => {
  initMobileDrawer();
  initHeroMotionControl();
});

function initMobileDrawer() {
  const toggleBtn = document.querySelector('.mobile-menu-toggle');
  const drawer = document.querySelector('.mobile-drawer');

  if (!toggleBtn || !drawer) return;

  toggleBtn.addEventListener('click', () => {
    const isOpen = drawer.classList.toggle('is-open');
    toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  // Close drawer on ESC key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
      drawer.classList.remove('is-open');
      toggleBtn.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
      toggleBtn.focus();
    }
  });
}

function initHeroMotionControl() {
  const pauseBtn = document.querySelector('.btn-hero-pause');
  const backdrop = document.querySelector('.hero-media-backdrop');

  if (!pauseBtn || !backdrop) return;

  let isPaused = false;
  pauseBtn.addEventListener('click', () => {
    isPaused = !isPaused;
    if (isPaused) {
      backdrop.style.animationPlayState = 'paused';
      backdrop.style.transition = 'none';
      pauseBtn.textContent = 'Resume Motion';
      pauseBtn.setAttribute('aria-pressed', 'true');
    } else {
      backdrop.style.animationPlayState = 'running';
      pauseBtn.textContent = 'Pause Motion';
      pauseBtn.setAttribute('aria-pressed', 'false');
    }
  });
}
