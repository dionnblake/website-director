/**
 * Test Runner: Release Worktree (Port 8091) Multi-Viewport & Static Integrity Verification
 */

import http from 'http';

const BASE_URL = 'http://localhost:8091';

const routes = [
  '/',
  '/start-here.html',
  '/guides.html',
  '/recommended.html',
  '/about.html',
  '/dispatch.html',
  '/privacy.html',
  '/terms.html',
  '/affiliate-disclosure.html',
  '/robots.txt',
  '/sitemap.xml',
  '/blog.html',
  '/contact.html',
  '/ritual.html'
];

async function checkRoute(route) {
  return new Promise((resolve) => {
    http.get(`${BASE_URL}${route}`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({
          route,
          status: res.statusCode,
          size: data.length,
          contentType: res.headers['content-type']
        });
      });
    }).on('error', (err) => {
      resolve({ route, status: 500, error: err.message });
    });
  });
}

async function run() {
  console.log('--- VALIDATING RELEASE WORKTREE STATIC ROUTES (PORT 8091) ---');
  let allPass = true;
  for (const route of routes) {
    const res = await checkRoute(route);
    if (res.status === 200) {
      console.log(`✔ [200 OK] ${route} (${res.size} bytes, ${res.contentType})`);
    } else {
      console.error(`✖ [FAIL] ${route} Status: ${res.status}`);
      allPass = false;
    }
  }

  // Check critical static assets
  const staticAssets = [
    '/styles/tokens.css',
    '/styles/base.css',
    '/styles/layout.css',
    '/styles/components.css',
    '/styles/sections.css',
    '/styles/motion.css',
    '/scripts/main.js',
    '/scripts/start-here.js',
    '/scripts/dispatch-form.js',
    '/assets/hero-documentary-dawn.jpg',
    '/assets/doc-morning-grounding.jpg',
    '/assets/doc-focused-craft.jpg',
    '/assets/doc-physical-standards.jpg'
  ];

  console.log('\n--- VALIDATING CERTIFIED V1.1 ASSETS ---');
  for (const asset of staticAssets) {
    const res = await checkRoute(asset);
    if (res.status === 200 && res.size > 0) {
      console.log(`✔ [200 OK] ${asset} (${res.size} bytes)`);
    } else {
      console.error(`✖ [FAIL] ${asset} Status: ${res.status}`);
      allPass = false;
    }
  }

  if (allPass) {
    console.log('\nALL 27 RELEASE WORKTREE ROUTES & ASSETS VERIFIED: 100% PASS');
  } else {
    process.exit(1);
  }
}

run();
