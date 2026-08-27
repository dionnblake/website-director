/**
 * Alpha Starts Now (V1.1) — The ASN Dispatch Form Handler
 */

window.ASN_SITE = window.ASN_SITE || {};
window.ASN_SITE.config = Object.assign({ leadEndpoint: '/api/subscribe' }, window.ASN_SITE.config);

document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('.dispatch-form');

  forms.forEach(form => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const emailInput = form.querySelector('input[type="email"]');
      const submitBtn = form.querySelector('button[type="submit"]');
      const statusMsg = form.querySelector('.form-status-message');

      if (!emailInput || !submitBtn || !statusMsg) return;

      const email = emailInput.value.trim();
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!email || !emailRegex.test(email)) {
        statusMsg.textContent = 'Please enter a valid email address.';
        statusMsg.className = 'form-status-message is-error';
        emailInput.focus();
        return;
      }

      submitBtn.disabled = true;
      const originalBtnText = submitBtn.textContent;
      submitBtn.textContent = 'Subscribing...';

      const leadEndpoint = window.ASN_SITE?.config?.leadEndpoint;

      if (leadEndpoint) {
        try {
          const res = await fetch(leadEndpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, source: window.location.pathname })
          });

          if (res.ok) {
            statusMsg.textContent = 'Thank you for subscribing to The ASN Dispatch. Check your inbox for confirmation.';
            statusMsg.className = 'form-status-message is-success';
            emailInput.value = '';
          } else {
            throw new Error('Subscription endpoint returned an error.');
          }
        } catch (err) {
          statusMsg.textContent = 'Unable to connect to subscription service. Please try again later.';
          statusMsg.className = 'form-status-message is-error';
        } finally {
          submitBtn.disabled = false;
          submitBtn.textContent = originalBtnText;
        }
      } else {
        // Safe preflight simulated confirmation
        setTimeout(() => {
          statusMsg.textContent = 'Thank you for subscribing to The ASN Dispatch. (Preflight Mode: Endpoint unconfigured).';
          statusMsg.className = 'form-status-message is-success';
          emailInput.value = '';
          submitBtn.disabled = false;
          submitBtn.textContent = originalBtnText;
        }, 400);
      }
    });
  });
});
