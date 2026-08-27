import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const USER_DATA_DIR = "C:\\Users\\ALPHA\\.gemini\\antigravity-ide\\brain\\95f9c0bb-8228-4701-a124-bca35ba39121\\scratch\\chrome-test-vp";
const EVIDENCE_DIR = "C:\\Users\\ALPHA\\Desktop\\VIBE CODING PROJECTS\\WEBSITE-DIRECTOR\\projects\\alpha-starts-now-v1-1\\qa\\evidence_remediated";
const BASE_URL = "http://localhost:8089";

async function main() {
  const chrome = spawn(CHROME_PATH, [
    "--headless=new",
    "--remote-debugging-port=9228",
    "--remote-allow-origins=*",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    `--user-data-dir=${USER_DATA_DIR}`
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const listRes = await fetch("http://127.0.0.1:9228/json/list");
    const targets = await listRes.json();
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);

    let idCounter = 1;
    function send(method, params = {}) {
      return new Promise((res, rej) => {
        const id = idCounter++;
        const handler = (event) => {
          const msg = JSON.parse(event.data.toString());
          if (msg.id === id) {
            ws.removeEventListener('message', handler);
            if (msg.error) rej(new Error(JSON.stringify(msg.error)));
            else res(msg.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    await send('Page.enable');
    await send('Runtime.enable');

    // Desktop 1440x900
    await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
    await send('Page.navigate', { url: `${BASE_URL}/index.html` });
    await new Promise(r => setTimeout(r, 1200));

    // Section 05 Documentary Desktop
    await send('Runtime.evaluate', { expression: 'document.querySelector(".section-documentary").scrollIntoView({block: "center"});' });
    await new Promise(r => setTimeout(r, 600));
    const shotDoc = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(EVIDENCE_DIR, 'recheck_02_home_documentary_desktop.png'), Buffer.from(shotDoc.data, 'base64'));

    // Section 06 Recommended Desktop
    await send('Runtime.evaluate', { expression: 'document.querySelector(".section-recommended").scrollIntoView({block: "center"});' });
    await new Promise(r => setTimeout(r, 600));
    const shotRec = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(EVIDENCE_DIR, 'recheck_03_home_recommended_desktop.png'), Buffer.from(shotRec.data, 'base64'));

    // Mobile 390x844
    await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
    await send('Page.navigate', { url: `${BASE_URL}/index.html` });
    await new Promise(r => setTimeout(r, 1200));

    await send('Runtime.evaluate', { expression: 'document.querySelector(".section-documentary").scrollIntoView({block: "center"});' });
    await new Promise(r => setTimeout(r, 600));
    const shotMobDoc = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(EVIDENCE_DIR, 'recheck_06_home_documentary_mobile.png'), Buffer.from(shotMobDoc.data, 'base64'));

    console.log("All viewport screenshots saved successfully!");
    ws.close();
  } finally {
    chrome.kill();
  }
}

main();
