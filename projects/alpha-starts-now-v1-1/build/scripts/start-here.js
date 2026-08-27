/**
 * Alpha Starts Now (V1.1) — Start Here Interactive Orientation
 */

document.addEventListener('DOMContentLoaded', () => {
  const pathwayButtons = document.querySelectorAll('[data-pathway-target]');
  const resultPanels = document.querySelectorAll('.pathway-result-panel');

  if (!pathwayButtons.length || !resultPanels.length) return;

  pathwayButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-pathway-target');

      // Update button active state
      pathwayButtons.forEach(b => {
        b.classList.remove('is-active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('is-active');
      btn.setAttribute('aria-selected', 'true');

      // Show matching result panel
      resultPanels.forEach(panel => {
        if (panel.id === targetId) {
          panel.style.display = 'block';
          panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
          panel.style.display = 'none';
        }
      });
    });
  });
});
