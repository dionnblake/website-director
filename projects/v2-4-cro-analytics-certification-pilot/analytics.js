/**
 * Northstar Performance Lab - Governed Analytics Event Bus
 * Schema Version: 2.4.0
 * Governance: CRO-ANALYTICS-EXPERIMENTATION-PROTOCOL.md
 * Invariants: PII Prohibition, Data Minimization, Zero External Requests, Fallback Resilience
 */

(function() {
  'use strict';

  // Check if analytics is disabled via query parameter
  const urlParams = new URLSearchParams(window.location.search);
  const analyticsDisabled = urlParams.get('disableAnalytics') === '1';

  // Global synthetic event store
  window.__analyticsEvents = window.__analyticsEvents || [];
  window.__analyticsActive = !analyticsDisabled;
  window.SYNTHETIC_ANALYTICS_BUS = true;

  // Forbidden PII fields
  const FORBIDDEN_PII_FIELDS = new Set([
    'email', 'phone', 'full_name', 'name', 'address', 'password',
    'message_body', 'message', 'ssn', 'date_of_birth', 'dob', 'credit_card'
  ]);

  // Allowed event contracts
  const VALID_EVENT_SCHEMAS = {
    'page_view': {
      version: 1,
      category: 'navigation',
      allowedProps: ['page_path', 'page_title', 'referrer']
    },
    'navigation_select': {
      version: 1,
      category: 'navigation',
      allowedProps: ['target_path', 'menu_location']
    },
    'pricing_view': {
      version: 1,
      category: 'consideration',
      allowedProps: ['component_id', 'viewport_ratio']
    },
    'case_study_view': {
      version: 1,
      category: 'proof',
      allowedProps: ['study_id', 'client_sector']
    },
    'consultation_start': {
      version: 1,
      category: 'intent',
      allowedProps: ['form_id', 'source_intent']
    },
    'form_validation_error': {
      version: 1,
      category: 'diagnostic',
      allowedProps: ['form_id', 'error_field_category']
    },
    'consultation_submit_success': {
      version: 1,
      category: 'conversion',
      allowedProps: ['form_id', 'qualification_tier']
    },
    'experiment_exposure': {
      version: 1,
      category: 'experiment',
      allowedProps: ['experiment_id', 'variant_id']
    }
  };

  /**
   * Governed Event Dispatcher
   */
  function trackEvent(name, payload) {
    if (!window.__analyticsActive) {
      return { success: false, reason: 'ANALYTICS_DISABLED' };
    }

    // 1. Validate Event Name
    const schema = VALID_EVENT_SCHEMAS[name];
    if (!schema) {
      console.warn(`[Analytics Rejected] Unknown event name: "${name}"`);
      return { success: false, reason: 'UNKNOWN_EVENT_NAME' };
    }

    payload = payload || {};

    // 2. Scan for Forbidden PII Fields
    for (const key of Object.keys(payload)) {
      if (FORBIDDEN_PII_FIELDS.has(key.toLowerCase())) {
        console.error(`[Analytics Rejected] PII Field detected: "${key}" in event "${name}"`);
        return { success: false, reason: 'PII_REJECTED', field: key };
      }
    }

    // 3. Assemble Governed Event Record
    const eventRecord = {
      event_name: name,
      event_version: schema.version,
      timestamp: Date.now(),
      page: window.location.pathname.split('/').pop() || 'index.html',
      payload: Object.freeze({ ...payload })
    };

    window.__analyticsEvents.push(Object.freeze(eventRecord));
    return { success: true, record: eventRecord };
  }

  // Expose trackEvent to global window
  window.trackEvent = trackEvent;

  // Single-Source-of-Truth Page View Deduplication
  let pageViewDispatched = false;
  function handlePageView() {
    if (pageViewDispatched) return;
    pageViewDispatched = true;

    const pagePath = window.location.pathname.split('/').pop() || 'index.html';
    trackEvent('page_view', {
      page_path: pagePath,
      page_title: document.title,
      referrer: document.referrer || 'direct'
    });
  }

  // Settle on DOMContentLoaded / Page Load
  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    handlePageView();
  } else {
    document.addEventListener('DOMContentLoaded', handlePageView, { once: true });
  }

  // Navigation Click Instrumentation
  document.addEventListener('click', function(e) {
    const navLink = e.target.closest('a[data-nav-track]');
    if (navLink) {
      const target = navLink.getAttribute('href');
      const location = navLink.getAttribute('data-nav-track') || 'header';
      trackEvent('navigation_select', {
        target_path: target,
        menu_location: location
      });
    }
  });

})();
