/**
 * Alpha Starts Now (V1.1) — Secure GetResponse Serverless Subscription Handler
 * Route: POST /api/subscribe
 * Architecture: Vercel / Standard Node Serverless Function
 */

const GETRESPONSE_API_BASE = 'https://api.getresponse.com/v3';
const MAX_PAYLOAD_BYTES = 10240; // 10 KB limit

function isValidEmail(email) {
  if (!email || typeof email !== 'string') return false;
  if (email.length > 254) return false;
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function sanitizeSource(src) {
  if (!src || typeof src !== 'string') return '/';
  return src.slice(0, 128).replace(/[^\w\-/.]/g, '');
}

export default async function handler(req, res) {
  // 1. Enforce POST method
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ success: false, error: 'Method Not Allowed' });
  }

  // 2. Enforce request size & parse payload
  let body = req.body;
  if (typeof body === 'string') {
    if (body.length > MAX_PAYLOAD_BYTES) {
      return res.status(413).json({ success: false, error: 'Payload Too Large' });
    }
    try {
      body = JSON.parse(body);
    } catch {
      return res.status(400).json({ success: false, error: 'Invalid JSON payload' });
    }
  }

  if (!body || typeof body !== 'object') {
    return res.status(400).json({ success: false, error: 'Malformed request body' });
  }

  const email = (body.email || '').trim().toLowerCase();
  const source = sanitizeSource(body.source);

  if (!isValidEmail(email)) {
    return res.status(400).json({ success: false, error: 'Please provide a valid email address.' });
  }

  // 3. Verify server-side secrets
  const apiKey = process.env.GETRESPONSE_API_KEY;
  const campaignId = process.env.GETRESPONSE_CAMPAIGN_ID;

  if (!apiKey || !campaignId) {
    console.error('[ASN Subscribe] Server Error: GETRESPONSE_API_KEY or GETRESPONSE_CAMPAIGN_ID not configured in environment.');
    return res.status(503).json({
      success: false,
      error: 'Subscription service configuration is currently pending. Please try again later.'
    });
  }

  // 4. Dispatch minimal production payload to GetResponse API v3 (POST /contacts)
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 8000);

  try {
    const grResponse = await fetch(`${GETRESPONSE_API_BASE}/contacts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Auth-Token': `api-key ${apiKey}`
      },
      body: JSON.stringify({
        email: email,
        campaign: {
          campaignId: campaignId
        }
      }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    // GetResponse returns HTTP 202 Accepted for newly queued subscribers
    if (grResponse.status === 202 || grResponse.status === 200 || grResponse.status === 201) {
      return res.status(200).json({
        success: true,
        status: 'queued',
        message: 'Thanks. Your signup was received. If confirmation is required for this list, check your inbox.'
      });
    }

    // Inspect error response for duplicate contact
    let errorData = null;
    try {
      errorData = await grResponse.json();
    } catch {
      // Non-JSON error payload
    }

    const message = errorData?.message || '';
    const code = errorData?.code || 0;

    // GetResponse duplicate contact check (code 1008 or message indicates contact already exists)
    if (grResponse.status === 400 || grResponse.status === 409) {
      if (code === 1008 || message.toLowerCase().includes('already added') || message.toLowerCase().includes('exists')) {
        return res.status(200).json({
          success: true,
          status: 'existing',
          message: 'You are already subscribed to The ASN Dispatch.'
        });
      }
    }

    // Log sanitized error without exposing API key or campaign secrets
    console.error(`[ASN Subscribe] GetResponse HTTP ${grResponse.status}: code=${code}, message=${message}`);

    return res.status(502).json({
      success: false,
      error: 'Unable to connect to the subscription service. Please try again later.'
    });

  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === 'AbortError') {
      console.error('[ASN Subscribe] Request timeout after 8000ms');
      return res.status(504).json({ success: false, error: 'Subscription service timed out. Please try again later.' });
    }
    console.error('[ASN Subscribe] Unexpected error:', err.message);
    return res.status(500).json({ success: false, error: 'An unexpected error occurred. Please try again later.' });
  }
}
