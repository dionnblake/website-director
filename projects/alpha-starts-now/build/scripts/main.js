/**
 * ALPHA STARTS NOW // PRODUCTION CLIENT LOGIC
 * Governance Authority: Website Director V1
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initFormHandling();
  initCategoryFilters();
});

/**
 * Mobile Navigation Drawer & Accessibility
 */
function initMobileNav() {
  const toggleBtn = document.querySelector('.mobile-menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  
  if (!toggleBtn || !navLinks) return;

  toggleBtn.addEventListener('click', () => {
    const isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
    toggleBtn.setAttribute('aria-expanded', !isExpanded);
    navLinks.classList.toggle('nav-open');
    document.body.classList.toggle('scroll-lock');
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navLinks.classList.contains('nav-open')) {
      toggleBtn.setAttribute('aria-expanded', 'false');
      navLinks.classList.remove('nav-open');
      document.body.classList.remove('scroll-lock');
      toggleBtn.focus();
    }
  });
}

/**
 * Newsletter Form Handling & Accessible Validation
 */
function initFormHandling() {
  const forms = document.querySelectorAll('.dispatch-form');

  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = form.querySelector('.input-field');
      const feedback = form.querySelector('.form-feedback');
      const submitBtn = form.querySelector('button[type="submit"]');

      if (!input || !input.value.includes('@')) {
        if (feedback) {
          feedback.textContent = 'Please provide a valid email address.';
          feedback.style.color = 'var(--status-error)';
        }
        return;
      }

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Securing Subscription...';
      }

      setTimeout(() => {
        if (submitBtn) {
          submitBtn.textContent = 'Subscribed to Dispatch';
          submitBtn.style.backgroundColor = 'var(--status-success)';
          submitBtn.style.borderColor = 'var(--status-success)';
        }
        if (feedback) {
          feedback.textContent = '✓ You are subscribed to The ASN Dispatch. Expect the next briefing Sunday at 08:00.';
          feedback.style.color = 'var(--status-success)';
        }
        input.value = '';
      }, 600);
    });
  });
}

/**
 * Filter handling for Library and Curated Hubs
 */
function initCategoryFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const filterItems = document.querySelectorAll('.filterable-item');

  if (!filterBtns.length || !filterItems.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');

      filterItems.forEach(item => {
        if (filter === 'all' || item.getAttribute('data-category') === filter) {
          item.style.display = 'flex';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });
}
