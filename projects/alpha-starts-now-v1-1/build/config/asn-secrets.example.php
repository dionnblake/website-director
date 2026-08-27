<?php
/**
 * Alpha Starts Now — Private Secrets Configuration Template
 * 
 * INSTRUCTIONS FOR HOSTINGER DEPLOYMENT:
 * 1. In Hostinger hPanel File Manager, navigate to `/domains/alphastartsnow.com/` (outside `public_html`).
 * 2. Create a folder named `private` if it does not already exist: `/domains/alphastartsnow.com/private/`.
 * 3. Create a file inside that directory named `asn-secrets.php`.
 * 4. Paste the structure below into `asn-secrets.php` with your real GetResponse credentials.
 * 5. DO NOT commit the real file with live keys into Git or place it inside `public_html`.
 */

return [
    // Private GetResponse API key (GetResponse Account -> Integrations and API -> API)
    'GETRESPONSE_API_KEY' => 'YOUR_GETRESPONSE_API_KEY_HERE',

    // The alphanumeric Contact List / Campaign token (not the numeric display ID)
    'GETRESPONSE_CAMPAIGN_ID' => 'YOUR_GETRESPONSE_CAMPAIGN_ID_TOKEN_HERE',
];
