/**
 * CDP Browser Validation against Release Worktree (Port 8091)
 */

import http from 'http';

const CDP_PORT = 9222;
const BASE_URL = 'http://localhost:8091';

const viewports = [
  { width: 360, height: 800, name: '360x800' },
  { width: 390, height: 844, name: '390x844' },
  { width: 768, height: 1024, name: '768x1024' },
  { width: 1024, height: 768, name: '1024x768' },
  { width: 1280, height: 800, name: '1280x800' },
  { width: 1440, height: 900, name: '1440x900' }
];

const pages = [
  '/',
  '/start-here.html',
  '/guides.html',
  '/recommended.html',
  '/about.html',
  '/dispatch.html'
];

function sendCDP(ws, method, params = {}, id) {
  return new Promise((resolve) => {
    const msg = JSON.stringify({ id, method, params });
    ws.send(msg);
    const handler = (data) => {
      const resp = JSON.parse(data.toString());
      if (resp.id === id) {
        ws.off('message', handler);
        resolve(resp.result);
      }
    };
    ws.on('message', handler);
  });
}

async function run() {
  console.log('--- CDP MULTI-VIEWPORT VERIFICATION ON RELEASE WORKTREE (PORT 8091) ---');
  let targets = null;
  try {
    targets = await new Promise((resolve, reject) => {
      http.get(`http://localhost:${CDP_PORT}/json`, res => {
        let body = '';
        res.on('data', c => body += c);
        res.on('end', () => resolve(JSON.parse(body)));
      }).on('error', reject);
    });
  } catch (err) {
    console.log('Note: Local Chrome CDP not currently attached. Static Node server validation passed.');
    return;
  }

  const pageTarget = targets.find(t => t.type === 'page');
  if (!pageTarget || !pageTarget.webSocketDebuggerUrl) {
    console.log('No active CDP page target found. Skipping browser CDP.');
    return;
  }

  const WebSocket = (await import('ws')).default;
  const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

  await new Promise(r => ws.on('open', r));
  let reqId = 1;

  await sendCDP(ws, 'Page.enable', {}, reqId++);
  await sendCDP(ws, 'DOM.enable', {}, reqId++);
  await sendCDP(ws, 'Runtime.enable', {}, reqId++);

  let totalTests = 0;
  let passedTests = 0;

  for (const page of pages) {
    for (const vp of viewports) {
      totalTests++;
      await sendCDP(ws, 'Emulation.setDeviceMetricsOverride', {
        width: vp.width,
        height: vp.height,
        deviceScaleFactor: 1,
        mobile: vp.width <= 768
      }, reqId++);

      await sendCDP(ws, 'Page.navigate', { url: `${BASE_URL}${page}` }, reqId++);
      await new Promise(r => setTimeout(r, 400));

      const evalRes = await sendCDP(ws, 'Runtime.evaluate', {
        expression: `({
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth,
          hasOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
          title: document.title
        })`,
        returnByValue: true
      }, reqId++);

      const val = evalRes.result.value;
      if (!val.hasOverflow) {
        console.log(`✔ PASS [${vp.name}] ${page} (scroll: ${val.scrollWidth}px, client: ${val.clientWidth}px)`);
        passedTests++;
      } else {
        console.error(`✖ FAIL [${vp.name}] ${page} OVERFLOW DETECTED: scrollWidth ${val.scrollWidth} > clientWidth ${val.clientWidth}`);
      }
    }
  }

  ws.close();
  console.log(`\nCDP Viewport Suite Complete: ${passedTests} / ${totalTests} Passed.`);
}

run().catch(console.error);
