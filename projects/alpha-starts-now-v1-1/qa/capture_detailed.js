import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const USER_DATA_DIR = "C:\\Users\\ALPHA\\.gemini\\antigravity-ide\\brain\\95f9c0bb-8228-4701-a124-bca35ba39121\\scratch\\chrome-profile-asn-shots";
const QA_DIR = "C:\\Users\\ALPHA\\Desktop\\VIBE CODING PROJECTS\\WEBSITE-DIRECTOR\\projects\\alpha-starts-now-v1-1\\qa";
const EVIDENCE_DIR = path.join(QA_DIR, "evidence_remediated");
const BASE_URL = "http://localhost:8089";

class SimpleCDP {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.id = 1;
    this.callbacks = new Map();
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (e) => reject(e);
      this.ws.onmessage = (event) => {
        const text = typeof event.data === 'string' ? event.data : event.data.toString();
        const msg = JSON.parse(text);
        if (msg.id && this.callbacks.has(msg.id)) {
          const cb = this.callbacks.get(msg.id);
          this.callbacks.delete(msg.id);
          if (msg.error) cb.reject(new Error(JSON.stringify(msg.error)));
          else cb.resolve(msg.result);
        }
      };
    });
  }

  send(method, params = {}, timeoutMs = 6000) {
    return new Promise((resolve, reject) => {
      const id = this.id++;
      const timer = setTimeout(() => {
        this.callbacks.delete(id);
        reject(new Error(`Timeout after ${timeoutMs}ms for ${method}`));
      }, timeoutMs);
      this.callbacks.set(id, {
        resolve: (res) => { clearTimeout(timer); resolve(res); },
        reject: (err) => { clearTimeout(timer); reject(err); }
      });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async eval(expression) {
    const res = await this.send("Runtime.evaluate", {
      expression: `(() => { ${expression} })()`,
      returnByValue: true,
      awaitPromise: true
    });
    return res.result ? res.result.value : undefined;
  }

  async captureElementScreenshot(selector, filepath) {
    const rect = await this.eval(`
      const el = document.querySelector('${selector}');
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return { x: window.scrollX + r.left, y: window.scrollY + r.top, width: r.width, height: r.height, scale: 1 };
    `);
    if (rect && rect.width > 0 && rect.height > 0) {
      const res = await this.send("Page.captureScreenshot", {
        format: "png",
        clip: { x: rect.x, y: rect.y, width: rect.width, height: rect.height, scale: 1 }
      });
      fs.writeFileSync(filepath, Buffer.from(res.data, 'base64'));
    }
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

async function captureDetailed() {
  const chrome = spawn(CHROME_PATH, [
    "--headless=new",
    "--remote-debugging-port=9226",
    "--remote-allow-origins=*",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    `--user-data-dir=${USER_DATA_DIR}`
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const listRes = await fetch("http://127.0.0.1:9226/json/list");
    const targets = await listRes.json();
    const cdp = new SimpleCDP(targets[0].webSocketDebuggerUrl);
    await cdp.connect();

    await cdp.send("Page.enable");
    await cdp.send("Runtime.enable");

    // Desktop
    await cdp.send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
    await cdp.send("Page.navigate", { url: `${BASE_URL}/index.html` });
    await new Promise(r => setTimeout(r, 1000));

    await cdp.captureElementScreenshot(".section-documentary", path.join(EVIDENCE_DIR, "recheck_02_home_documentary_desktop.png"));
    await cdp.captureElementScreenshot(".section-recommended", path.join(EVIDENCE_DIR, "recheck_03_home_recommended_desktop.png"));

    // Mobile
    await cdp.send("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
    await cdp.send("Page.navigate", { url: `${BASE_URL}/index.html` });
    await new Promise(r => setTimeout(r, 1000));

    await cdp.captureElementScreenshot(".section-documentary", path.join(EVIDENCE_DIR, "recheck_06_home_documentary_mobile.png"));

    console.log("Detailed section shots captured successfully!");
    cdp.close();
  } finally {
    chrome.kill();
  }
}

captureDetailed();
