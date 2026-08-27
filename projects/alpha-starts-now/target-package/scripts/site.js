/**
 * ALPHA STARTS NOW // PRODUCTION CLIENT SCRIPT
 * Governance Authority: Website Director V1
 */

(function () {
  'use strict';

  const site = window.ASN_SITE || { config: {}, nav: [], pillars: [], articles: [] };
  const config = site.config || {};
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  const track = (eventName, detail = {}) => {
    try {
      window.dispatchEvent(new CustomEvent('asn:track', { detail: { event: eventName, ...detail, timestamp: Date.now() } }));
    } catch (_) {}
  };

  /**
   * Mobile Navigation & Accessible Keyboard Trap
   */
  const menuButton = document.querySelector('.mobile-menu-toggle');
  const navLinks = document.querySelector('.nav-links');

  const getMenuFocusables = () => {
    if (!navLinks) return [];
    return [...navLinks.querySelectorAll('a, button')].filter((node) => !node.hasAttribute('disabled'));
  };

  const openMenu = () => {
    if (!menuButton || !navLinks) return;
    menuButton.setAttribute('aria-expanded', 'true');
    navLinks.classList.add('nav-open');
    document.body.classList.add('scroll-lock');
    const focusables = getMenuFocusables();
    if (focusables.length) focusables[0].focus();
    track('menu_opened');
  };

  const closeMenu = (options = { restoreFocus: true }) => {
    if (!menuButton || !navLinks) return;
    menuButton.setAttribute('aria-expanded', 'false');
    navLinks.classList.remove('nav-open');
    document.body.classList.remove('scroll-lock');
    if (options.restoreFocus) menuButton.focus();
    track('menu_closed');
  };

  if (menuButton && navLinks) {
    menuButton.addEventListener('click', () => {
      const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
      if (isOpen) closeMenu(); else openMenu();
    });

    navLinks.addEventListener('click', (event) => {
      if (event.target.closest('a')) closeMenu({ restoreFocus: false });
    });

    document.addEventListener('keydown', (event) => {
      if (!navLinks.classList.contains('nav-open')) return;
      if (event.key === 'Escape') {
        event.preventDefault();
        closeMenu();
        return;
      }
      if (event.key !== 'Tab') return;
      const focusables = getMenuFocusables();
      if (!focusables.length) return;
      const first = focusables[0];
      const last = focusables[focusables.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
  }

  /**
   * Filter handling for Library & Articles
   */
  const filterBtns = document.querySelectorAll('.filter-btn');
  const filterItems = document.querySelectorAll('.filterable-item');

  if (filterBtns.length && filterItems.length) {
    filterBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        filterBtns.forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');

        const filter = btn.getAttribute('data-filter');
        filterItems.forEach((item) => {
          if (filter === 'all' || item.getAttribute('data-category') === filter) {
            item.style.display = 'flex';
          } else {
            item.style.display = 'none';
          }
        });
      });
    });
  }

  /**
   * Analytics & Tracking Hooks
   */
  document.addEventListener('click', (event) => {
    const tracked = event.target.closest('[data-track]');
    if (tracked) track(tracked.dataset.track, { href: tracked.getAttribute('href') || '' });
  });

  /**
   * Form Handling & Validation
   */
  const formMessage = (form, state, text) => {
    const status = form.querySelector('[data-form-status]');
    if (!status) return;
    status.dataset.state = state;
    status.textContent = text;
  };

  const showFormFallback = (form) => {
    const fallback = form.querySelector('[data-form-fallback]');
    if (fallback) fallback.hidden = false;
  };

  const submitConfiguredForm = async (form, submitButton) => {
    const formType = form.dataset.formType || 'lead';
    const payload = Object.fromEntries(new FormData(form).entries());
    delete payload.website;
    const response = await fetch(config.leadEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ ...payload, formType, resource: config.leadResource || 'The ASN Dispatch' }),
      signal: AbortSignal.timeout ? AbortSignal.timeout(10000) : undefined
    });
    if (response.status === 409) return { kind: 'duplicate' };
    if (!response.ok) return { kind: 'error' };
    return { kind: 'success' };
  };

  document.querySelectorAll('[data-form]').forEach((form) => {
    let started = false;
    const submitButton = form.querySelector('button[type="submit"]');
    const defaultLabel = submitButton ? submitButton.textContent : '';

    form.addEventListener('input', () => {
      if (!started) {
        started = true;
        track(form.dataset.formType === 'contact' ? 'contact_form_started' : 'lead_form_started');
      }
    });

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const formType = form.dataset.formType || 'lead';
      const isContact = formType === 'contact';
      const invalid = [...form.elements].find((element) => element.willValidate && !element.checkValidity());
      if (invalid) {
        form.classList.add('was-validated');
        formMessage(form, 'error', 'Check the highlighted field and try again.');
        invalid.focus();
        track(isContact ? 'contact_form_failed' : 'lead_form_failed', { reason: 'validation' });
        return;
      }

      const honeypot = form.elements.namedItem('website');
      if (honeypot && honeypot.value) return;

      if (!config.leadEndpoint) {
        formMessage(form, 'error', isContact ? 'This form is not connected yet. Nothing was sent.' : 'Email delivery is not connected yet. Nothing was submitted.');
        showFormFallback(form);
        track(isContact ? 'contact_form_failed' : 'lead_form_failed', { reason: 'endpoint_not_configured' });
        return;
      }

      if (submitButton) {
        submitButton.disabled = true;
        submitButton.textContent = 'Sending...';
      }
      formMessage(form, 'loading', 'Sending securely...');
      track(isContact ? 'contact_form_submitted' : 'lead_form_submitted');

      try {
        const result = await submitConfiguredForm(form, submitButton);
        if (result.kind === 'duplicate') {
          formMessage(form, 'error', 'That email is already subscribed. Check your inbox for the next issue.');
          track('lead_form_failed', { reason: 'duplicate' });
        } else if (result.kind === 'success') {
          form.hidden = true;
          const success = form.parentElement.querySelector('[data-form-success]');
          if (success) success.hidden = false;
          track(isContact ? 'contact_form_succeeded' : 'lead_form_succeeded');
        } else {
          throw new Error('Request failed');
        }
      } catch (error) {
        formMessage(form, 'error', navigator.onLine === false ? 'You appear to be offline. Reconnect and try again.' : 'We could not send that yet. Try again or use the email fallback below.');
        showFormFallback(form);
        track(isContact ? 'contact_form_failed' : 'lead_form_failed', { reason: 'request_error' });
      } finally {
        if (submitButton && !form.hidden) {
          submitButton.disabled = false;
          submitButton.textContent = defaultLabel;
        }
      }
    });
  });

  document.querySelectorAll('[data-lead-view]').forEach((node) => {
    node.addEventListener('focusin', () => track('lead_form_viewed'), { once: true });
  });
})();
