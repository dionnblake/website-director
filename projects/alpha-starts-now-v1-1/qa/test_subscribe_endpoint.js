/**
 * Test Suite: /api/subscribe Serverless Endpoint Unit & Integration Tests
 */

import handler from '../build/api/subscribe.js';

class MockResponse {
  constructor() {
    this.statusCode = 200;
    this.headers = {};
    this.body = null;
  }
  status(code) {
    this.statusCode = code;
    return this;
  }
  setHeader(k, v) {
    this.headers[k] = v;
    return this;
  }
  json(data) {
    this.body = data;
    return this;
  }
}

async function runTests() {
  console.log('--- RUNNING /api/subscribe TEST SUITE ---');
  let passed = 0;
  let total = 0;

  // Test 1: Method not allowed (GET)
  total++;
  const reqGet = { method: 'GET' };
  const resGet = new MockResponse();
  await handler(reqGet, resGet);
  if (resGet.statusCode === 405 && resGet.body.error === 'Method Not Allowed') {
    console.log('✔ Test 1 PASS: Method Not Allowed on GET');
    passed++;
  } else {
    console.error('✖ Test 1 FAIL:', resGet.statusCode, resGet.body);
  }

  // Test 2: Invalid Email
  total++;
  const reqInvalid = { method: 'POST', body: { email: 'not-an-email', source: '/guides' } };
  const resInvalid = new MockResponse();
  await handler(reqInvalid, resInvalid);
  if (resInvalid.statusCode === 400 && resInvalid.body.error.includes('valid email')) {
    console.log('✔ Test 2 PASS: 400 Bad Request on invalid email format');
    passed++;
  } else {
    console.error('✖ Test 2 FAIL:', resInvalid.statusCode, resInvalid.body);
  }

  // Test 3: Missing Server-Side Secrets
  total++;
  delete process.env.GETRESPONSE_API_KEY;
  delete process.env.GETRESPONSE_CAMPAIGN_ID;
  const reqNoSecrets = { method: 'POST', body: { email: 'test@example.com', source: '/dispatch' } };
  const resNoSecrets = new MockResponse();
  await handler(reqNoSecrets, resNoSecrets);
  if (resNoSecrets.statusCode === 503 && !JSON.stringify(resNoSecrets.body).includes('API_KEY')) {
    console.log('✔ Test 3 PASS: 503 Service Unavailable without secret leakage');
    passed++;
  } else {
    console.error('✖ Test 3 FAIL:', resNoSecrets.statusCode, resNoSecrets.body);
  }

  console.log(`\nTests Completed: ${passed} / ${total} passed.`);
  if (passed === total) {
    console.log('ENDPOINT INTEGRITY: 100% PASS');
  } else {
    process.exit(1);
  }
}

runTests();
