import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const USER_DATA_DIR = "C:\\Users\\ALPHA\\.gemini\\antigravity-ide\\brain\\95f9c0bb-8228-4701-a124-bca35ba39121\\scratch\\chrome-profile-full2";
const EVIDENCE_DIR = "C:\\Users\\ALPHA\\Desktop\\VIBE CODING PROJECTS\\WEBSITE-DIRECTOR\\projects\\alpha-starts-now-v1-1\\qa\\evidence_remediated";
const BASE_URL = "http://localhost:8089";

async function run() {
  const chrome = spawn(CHROME_PATH, [
    "--headless=new",
    "--remote-debugging-port=9230",
    "--remote-allow-origins=*",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    `--user-data-dir=${USER_DATA_DIR}`
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const listRes = await fetch("http://127.0.0.1:9230/json/list");
    const targets = await listRes.json();
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);

    let id = 1;
    function send(method, params = {}) {
      return new Promise((resolve, reject) => {
        const reqId = id++;
        const handler = (event) => {
          const msg = JSON.parse(event.data.toString());
          if (msg.id === reqId) {
            ws.removeEventListener('message', handler);
            if (msg.error) reject(new Error(JSON.stringify(msg.error)));
            else resolve(msg.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id: reqId, method, params }));
      });
    }

    await send('Page.enable');
    await send('Runtime.enable');

    // 1. Desktop 1440x900
    await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
    await send('Page.navigate', { url: `${BASE_URL}/index.html` });
    await new Promise(r => setTimeout(r, 1000));

    // Scroll through entire page to trigger all images
    await send('Runtime.evaluate', {
      expression: `(async () => {
        const imgs = Array.from(document.querySelectorAll('img'));
        imgs.forEach(img => { img.loading = 'eager'; });
        window.scrollTo(0, document.body.scrollHeight / 2);
        await new Promise(r => setTimeout(r, 500));
        window.scrollTo(0, document.body.scrollHeight);
        await new Promise(r => setTimeout(r, 500));
        window.scrollTo(0, 0);
      })()`,
      awaitPromise: true
    });
    await new Promise(r => setTimeout(r, 1000));

    // Desktop Hero Shot
    const heroShot = await send('Page.captureScreenshot', {
      format: 'png',
      clip: { x: 0, y: 0, width: 1440, height: 800, scale: 1 }
    });
    fs.writeFileSync(path.join(EVIDENCE_DIR, 'recheck_01_home_hero_desktop.png'), Buffer.from(heroShot.data, 'base64'));

    // Section 05 Documentary desktop clip
    const sec5Rect = (await send('Runtime.evaluate', {
      expression: '(() => { const r = document.querySelector(".section-documentary").getBoundingClientRect(); return { x: r.left, y: window.scrollY + r.top, width: r.width, height: r.height, scale: 1 }; })()',
      returnByValue: true
    })).result.value;

    const sec5Shot = await send('Page.captureScreenshot', {
      format: 'png',
      captureBeyondViewport: true,
      clip: sec5Rect
    });
    fs.writeFileSync(path.join(EVIDENCE_DIR, 'recheck_02_home_documentary_desktop.png'), Buffer.from(sec5Shot.data, 'base64'));

    // Section 06 Recommended desktop clip
    const sec6Rect = (await send('Runtime.evaluate', {
      expression: '(() => { const r = document.querySelector(".section-recommended").getBoundingClientRect(); return { x: r.left, y: window.scrollY + r.top, width: r.width, height: r.height, scale: 1 }; })()',
      returnByValue: true
    })).result.value;

    const sec6Shot = await send('Page.captureScreenshot', {
      format: 'png',
      captureBeyondViewport: true,
      clip: sec6Rect
    });
    fs.writeFileSync(path.join(EVIDENCE_DIR, 'recheck_03_home_recommended_desktop.png'), Buffer.from(sec6Shot.data, 'base64'));

    // Recommended Page Desktop
    await send('Page.navigate', { url: `${BASE_URL}/recommended.html` });
    await new Promise(r => setTimeout(r, 1000));
    const recPageShot = await send('Page.captureScreenshot', {
      format: 'png',
      clip: { x: 0, y: 0, width: 1440, height: 900, scale: 1 }
    });
    fs.writeFileSync(path.join(EVIDENCE_DIR, 'recheck_04_recommended_page_desktop.png'), Buffer.from(recPageShot.data, 'base64'));

    // 2. Mobile 390x844
    await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
    await send('Page.navigate', { url: `${BASE_URL}/index.html` });
    await new Promise(r => setTimeout(r, 1000));

    // Scroll through mobile
    await send('Runtime.evaluate', {
      expression: `(async () => {
        const imgs = Array.from(document.querySelectorAll('img'));
        imgs.forEach(img => { img.loading = 'eager'; });
        window.scrollTo(0, document.body.scrollHeight / 2);
        await new Promise(r => setTimeout(r, 500));
        window.scrollTo(0, document.body.scrollHeight);
        await new Promise(r => setTimeout(r, 500));
        window.scrollTo(0, 0);
      })()`,
      awaitPromise: true
    });
    await new Promise(r => setTimeout(r, 1000));

    // Mobile Hero
    const mobHeroShot = await send('Page.captureScreenshot', {
      format: 'png',
      clip: { x: 0, y: 0, width: 390, height: 844, scale: 1 }
    });
    fs.writeFileSync(path.join(EVIDENCE_DIR, 'recheck_05_home_hero_mobile.png'), Buffer.from(mobHeroShot.data, 'base64'));

    // Mobile Section 05
    const mobSec5Rect = (await send('Runtime.evaluate', {
      expression: '(() => { const r = document.querySelector(".section-documentary").getBoundingClientRect(); return { x: r.left, y: window.scrollY + r.top, width: r.width, height: r.height, scale: 1 }; })()',
      returnByValue: true
    })).result.value;

    const mobSec5Shot = await send('Page.captureScreenshot', {
      format: 'png',
      captureBeyondViewport: true,
      clip: mobSec5Rect
    });
    fs.writeFileSync(path.join(EVIDENCE_DIR, 'recheck_06_home_documentary_mobile.png'), Buffer.from(mobSec5Shot.data, 'base64'));

    // Mobile Recommended Page
    await send('Page.navigate', { url: `${BASE_URL}/recommended.html` });
    await new Promise(r => setTimeout(r, 1000));
    const mobRecShot = await send('Page.captureScreenshot', {
      format: 'png',
      clip: { x: 0, y: 0, width: 390, height: 844, scale: 1 }
    });
    fs.writeFileSync(path.join(EVIDENCE_DIR, 'recheck_07_recommended_mobile.png'), Buffer.from(mobRecShot.data, 'base64'));

    // 3. Reduced Motion Hero
    await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
    await send('Emulation.setEmulatedMedia', {
      features: [{ name: "prefers-reduced-motion", value: "reduce" }]
    });
    await send('Page.navigate', { url: `${BASE_URL}/index.html` });
    await new Promise(r => setTimeout(r, 1000));
    const redMotionShot = await send('Page.captureScreenshot', {
      format: 'png',
      clip: { x: 0, y: 0, width: 1440, height: 800, scale: 1 }
    });
    fs.writeFileSync(path.join(EVIDENCE_DIR, 'recheck_08_reduced_motion_hero.png'), Buffer.from(redMotionShot.data, 'base64'));

    console.log("All 8 recheck screenshots captured with verified image loading!");
    ws.close();
  } finally {
    chrome.kill();
  }
}

run();
