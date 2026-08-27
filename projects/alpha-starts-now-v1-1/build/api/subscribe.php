<?php
/**
 * Alpha Starts Now (V1.1) — Hostinger Native GetResponse Subscription Bridge
 * Route: POST /api/subscribe
 * Implementation: Native PHP / cURL
 */

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');

// 1. Enforce POST method
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    header('Allow: POST');
    echo json_encode([
        'success' => false,
        'error' => 'Method Not Allowed'
    ]);
    exit;
}

// 2. Enforce request size bound (10 KB max)
$maxBytes = 10240;
$rawInput = file_get_contents('php://input');

if (strlen($rawInput) > $maxBytes) {
    http_response_code(413);
    echo json_encode([
        'success' => false,
        'error' => 'Payload Too Large'
    ]);
    exit;
}

// 3. Parse and validate JSON body
$data = json_decode($rawInput, true);

if (!is_array($data)) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'error' => 'Invalid JSON payload'
    ]);
    exit;
}

$email = isset($data['email']) ? strtolower(trim((string)$data['email'])) : '';
$source = isset($data['source']) ? trim((string)$data['source']) : '/';

// Normalize source string
$source = preg_replace('/[^\w\-\/.]/', '', substr($source, 0, 128));

// Validate email format and length
if (empty($email) || strlen($email) > 254 || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'error' => 'Please provide a valid email address.'
    ]);
    exit;
}

// 4. Secure Secrets Retrieval
// Priority 1: Server environment variables
// Priority 2: Private secrets file outside public_html
$apiKey = getenv('GETRESPONSE_API_KEY') ?: (isset($_ENV['GETRESPONSE_API_KEY']) ? $_ENV['GETRESPONSE_API_KEY'] : null);
$campaignId = getenv('GETRESPONSE_CAMPAIGN_ID') ?: (isset($_ENV['GETRESPONSE_CAMPAIGN_ID']) ? $_ENV['GETRESPONSE_CAMPAIGN_ID'] : null);

if (!$apiKey || !$campaignId) {
    // Attempt to load from private storage outside public_html
    $privatePaths = [
        dirname($_SERVER['DOCUMENT_ROOT'] ?? '') . '/private/asn-secrets.php',
        __DIR__ . '/../../private/asn-secrets.php',
        __DIR__ . '/../config/asn-secrets.php'
    ];

    foreach ($privatePaths as $path) {
        if (!empty($path) && file_exists($path) && is_readable($path)) {
            $secrets = include $path;
            if (is_array($secrets)) {
                $apiKey = $apiKey ?: ($secrets['GETRESPONSE_API_KEY'] ?? null);
                $campaignId = $campaignId ?: ($secrets['GETRESPONSE_CAMPAIGN_ID'] ?? null);
            }
            if ($apiKey && $campaignId) {
                break;
            }
        }
    }
}

if (!$apiKey || !$campaignId) {
    error_log('[ASN Subscribe] Server Error: GETRESPONSE_API_KEY or GETRESPONSE_CAMPAIGN_ID not configured.');
    http_response_code(503);
    echo json_encode([
        'success' => false,
        'error' => 'Subscription service configuration is currently pending. Please try again later.'
    ]);
    exit;
}

// 5. Build minimal GetResponse v3 payload
$grPayload = json_encode([
    'email' => $email,
    'campaign' => [
        'campaignId' => $campaignId
    ]
]);

// 6. Dispatch via PHP cURL
$ch = curl_init('https://api.getresponse.com/v3/contacts');
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $grPayload,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 8,
    CURLOPT_CONNECTTIMEOUT => 5,
    CURLOPT_SSL_VERIFYPEER => true,
    CURLOPT_HTTPHEADER => [
        'Content-Type: application/json',
        'X-Auth-Token: api-key ' . $apiKey
    ]
]);

$responseBody = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlError = curl_error($ch);
$curlErrno = curl_errno($ch);
curl_close($ch);

// 7. Handle cURL network failures / timeouts
if ($curlErrno !== 0) {
    error_log('[ASN Subscribe] cURL error (' . $curlErrno . '): ' . $curlError);
    if ($curlErrno === CURLE_OPERATION_TIMEDOUT) {
        http_response_code(504);
        echo json_encode([
            'success' => false,
            'error' => 'Subscription service timed out. Please try again later.'
        ]);
    } else {
        http_response_code(502);
        echo json_encode([
            'success' => false,
            'error' => 'Unable to connect to subscription service. Please try again later.'
        ]);
    }
    exit;
}

// 8. Map GetResponse HTTP status codes
// Upstream 202 Accepted (or 200/201)
if ($httpCode === 202 || $httpCode === 200 || $httpCode === 201) {
    http_response_code(200);
    echo json_encode([
        'success' => true,
        'status' => 'queued',
        'message' => 'Thanks. Your signup was received. If confirmation is required for this list, check your inbox.'
    ]);
    exit;
}

// Parse error response for duplicate contact detection
$errorData = json_decode($responseBody, true);
$message = is_array($errorData) && isset($errorData['message']) ? (string)$errorData['message'] : '';
$code = is_array($errorData) && isset($errorData['code']) ? (int)$errorData['code'] : 0;

// Duplicate contact check (Code 1008 or message contains 'already added' / 'exists')
if ($httpCode === 400 || $httpCode === 409) {
    if ($code === 1008 || stripos($message, 'already added') !== false || stripos($message, 'exists') !== false) {
        http_response_code(200);
        echo json_encode([
            'success' => true,
            'status' => 'existing',
            'message' => 'You are already subscribed to The ASN Dispatch.'
        ]);
        exit;
    }
}

// Log sanitized diagnostic to server log without exposing secrets
error_log('[ASN Subscribe] GetResponse HTTP ' . $httpCode . ': code=' . $code . ', message=' . $message);

// Return generic safe failure to client
http_response_code(502);
echo json_encode([
    'success' => false,
    'error' => 'Unable to process subscription request. Please try again later.'
]);
exit;
