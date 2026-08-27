import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const USER_DATA_DIR = "C:\\Users\\ALPHA\\.gemini\\antigravity-ide\\brain\\95f9c0bb-8228-4701-a124-bca35ba39121\\scratch\\chrome-profile-asn-recheck";
const QA_DIR = "C:\\Users\\ALPHA\\Desktop\\VIBE CODING PROJECTS\\WEBSITE-DIRECTOR\\projects\\alpha-starts-now-v1-1\\qa";
const EVIDENCE_DIR = path.join(QA_DIR, "evidence_remediated");
const BASE_URL = "http://localhost:8089";

fs.mkdirSync(EVIDENCE_DIR, { recursive: true });
fs.mkdirSync(USER_DATA_DIR, { recursive: true });

class SimpleCDP {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.id = 1;
    this.callbacks = new Map();
    this.consoleLogs = [];
    this.pageErrors = [];
    this.failedRequests = [];
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (e) => reject(e);
      this.ws.onmessage = (event) => {
        const text = typeof event.data === 'string' ? event.data : event.data.toString();
        const msg = JSON.parse(text);
        
        if (msg.method === "Runtime.consoleAPICalled") {
          this.consoleLogs.push({ type: msg.params.type, args: msg.params.args.map(a => a.value || a.description) });
        }
        if (msg.method === "Runtime.exceptionThrown") {
          this.pageErrors.push(msg.params.exceptionDetails);
        }
        if (msg.method === "Network.loadingFailed") {
          this.failedRequests.push(msg.params);
        }

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
    if (res.exceptionDetails) {
      throw new Error(`Eval error: ${JSON.stringify(res.exceptionDetails)}`);
    }
    return res.result ? res.result.value : undefined;
  }

  async setViewport(width, height, deviceScaleFactor = 1, isMobile = false) {
    await this.send("Emulation.setDeviceMetricsOverride", {
      width,
      height,
      deviceScaleFactor,
      mobile: isMobile
    });
  }

  async navigate(url) {
    await this.send("Page.navigate", { url });
    await new Promise(r => setTimeout(r, 700));
  }

  async captureScreenshot(filepath, clip = null) {
    const params = { format: "png" };
    if (clip) params.clip = clip;
    const res = await this.send("Page.captureScreenshot", params);
    fs.writeFileSync(filepath, Buffer.from(res.data, 'base64'));
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

async function runRecheck() {
  console.log("Launching Chrome for Independent Remediation Recheck...");
  const chrome = spawn(CHROME_PATH, [
    "--headless=new",
    "--remote-debugging-port=9225",
    "--remote-allow-origins=*",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    `--user-data-dir=${USER_DATA_DIR}`
  ]);

  let targets = null;
  for (let i = 0; i < 10; i++) {
    await new Promise(r => setTimeout(r, 600));
    try {
      const listRes = await fetch("http://127.0.0.1:9225/json/list");
      targets = await listRes.json();
      if (targets && targets.length > 0) break;
    } catch (e) {
      // retry
    }
  }

  try {
    if (!targets || targets.length === 0) {
      throw new Error("Could not connect to Chrome debugging targets after retries.");
    }
    const pageTarget = targets.find(t => t.type === "page") || targets[0];

    const cdp = new SimpleCDP(pageTarget.webSocketDebuggerUrl);
    await cdp.connect();

    await cdp.send("Page.enable");
    await cdp.send("DOM.enable");
    await cdp.send("CSS.enable");
    await cdp.send("Runtime.enable");
    await cdp.send("Network.enable");

    const recheckData = {
      timestamp: new Date().toISOString(),
      hero_kicker_rendered: "",
      hero_media_rendered: "",
      section_05_images_rendered: [],
      recommended_page_state: {},
      overflow_check: {},
      console_logs: [],
      page_errors: [],
      screenshots: []
    };

    // 1. Desktop 1440x900 - Home Hero & Body
    await cdp.setViewport(1440, 900, 1, false);
    await cdp.navigate(`${BASE_URL}/index.html`);

    recheckData.hero_kicker_rendered = await cdp.eval("return document.querySelector('.hero-section .section-kicker')?.innerText;");
    recheckData.hero_media_rendered = await cdp.eval("return window.getComputedStyle(document.querySelector('.hero-media-backdrop') || document.body).backgroundImage;");

    // Capture Hero Desktop
    const heroShot = path.join(EVIDENCE_DIR, "recheck_01_home_hero_desktop.png");
    await cdp.captureScreenshot(heroShot);
    recheckData.screenshots.push("recheck_01_home_hero_desktop.png");

    // Scroll to Section 05 Documentary Break
    await cdp.eval("document.querySelector('.section-documentary')?.scrollIntoView({behavior: 'instant', block: 'center'});");
    await new Promise(r => setTimeout(r, 800));
    const docShot = path.join(EVIDENCE_DIR, "recheck_02_home_documentary_desktop.png");
    await cdp.captureScreenshot(docShot);
    recheckData.screenshots.push("recheck_02_home_documentary_desktop.png");

    recheckData.section_05_images_rendered = await cdp.eval(`
      return Array.from(document.querySelectorAll('.section-documentary img')).map(img => ({
        src: img.getAttribute('src'),
        alt: img.getAttribute('alt'),
        complete: img.complete,
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight
      }));
    `);

    // Scroll to Section 06 Recommended Desk
    await cdp.eval("document.querySelector('.section-recommended')?.scrollIntoView({behavior: 'instant', block: 'center'});");
    await new Promise(r => setTimeout(r, 800));
    const recSectionShot = path.join(EVIDENCE_DIR, "recheck_03_home_recommended_desktop.png");
    await cdp.captureScreenshot(recSectionShot);
    recheckData.screenshots.push("recheck_03_home_recommended_desktop.png");

    // 2. Recommended Page Desktop
    await cdp.navigate(`${BASE_URL}/recommended.html`);
    await new Promise(r => setTimeout(r, 800));
    const recPageShot = path.join(EVIDENCE_DIR, "recheck_04_recommended_page_desktop.png");
    await cdp.captureScreenshot(recPageShot);
    recheckData.screenshots.push("recheck_04_recommended_page_desktop.png");

    recheckData.recommended_page_state = await cdp.eval(`
      return {
        title: document.title,
        h1: document.querySelector('h1')?.innerText,
        calloutTitle: document.querySelector('.callout-title')?.innerText,
        hasFakeAmazonLinks: Array.from(document.querySelectorAll('a')).some(a => a.href.includes('amazon.com')),
        totalSpecCards: document.querySelectorAll('.spec-card').length
      };
    `);

    // 3. Mobile Viewport 390x844 - Home Hero, Doc, Recommended
    await cdp.setViewport(390, 844, 2, true);
    await cdp.navigate(`${BASE_URL}/index.html`);
    await new Promise(r => setTimeout(r, 600));

    const mobHeroShot = path.join(EVIDENCE_DIR, "recheck_05_home_hero_mobile.png");
    await cdp.captureScreenshot(mobHeroShot);
    recheckData.screenshots.push("recheck_05_home_hero_mobile.png");

    // Mobile Section 05 Doc Break
    await cdp.eval("document.querySelector('.section-documentary')?.scrollIntoView({behavior: 'instant', block: 'center'});");
    await new Promise(r => setTimeout(r, 800));
    const mobDocShot = path.join(EVIDENCE_DIR, "recheck_06_home_documentary_mobile.png");
    await cdp.captureScreenshot(mobDocShot);
    recheckData.screenshots.push("recheck_06_home_documentary_mobile.png");

    // Mobile Recommended Page
    await cdp.navigate(`${BASE_URL}/recommended.html`);
    await new Promise(r => setTimeout(r, 800));
    const mobRecShot = path.join(EVIDENCE_DIR, "recheck_07_recommended_mobile.png");
    await cdp.captureScreenshot(mobRecShot);
    recheckData.screenshots.push("recheck_07_recommended_mobile.png");

    // 4. Accessibility & Reduced Motion
    await cdp.setViewport(1440, 900, 1, false);
    await cdp.send("Emulation.setEmulatedMedia", {
      features: [{ name: "prefers-reduced-motion", value: "reduce" }]
    });
    await cdp.navigate(`${BASE_URL}/index.html`);
    await new Promise(r => setTimeout(r, 800));
    const reducedShot = path.join(EVIDENCE_DIR, "recheck_08_reduced_motion_hero.png");
    await cdp.captureScreenshot(reducedShot);
    recheckData.screenshots.push("recheck_08_reduced_motion_hero.png");

    // 5. Multi-viewport overflow audit
    const viewports = [
      { name: "360x800", w: 360, h: 800 },
      { name: "390x844", w: 390, h: 844 },
      { name: "768x1024", w: 768, h: 1024 },
      { name: "1024x768", w: 1024, h: 768 },
      { name: "1280x800", w: 1280, h: 800 },
      { name: "1440x900", w: 1440, h: 900 }
    ];
    const pages = ["index.html", "start-here.html", "guides.html", "recommended.html", "about.html", "dispatch.html"];

    for (const vp of viewports) {
      await cdp.setViewport(vp.w, vp.h, 1, vp.w < 800);
      recheckData.overflow_check[vp.name] = {};
      for (const pg of pages) {
        await cdp.navigate(`${BASE_URL}/${pg}`);
        const ovf = await cdp.eval(`
          return {
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            hasOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
          };
        `);
        recheckData.overflow_check[vp.name][pg] = ovf;
      }
    }

    recheckData.console_logs = cdp.consoleLogs;
    recheckData.page_errors = cdp.pageErrors;

    fs.writeFileSync(path.join(QA_DIR, "asn_recheck_results.json"), JSON.stringify(recheckData, null, 2));
    console.log("Remediation Recheck finished successfully!");

    cdp.close();
  } catch (err) {
    console.error("Recheck execution error:", err);
    fs.writeFileSync(path.join(QA_DIR, "asn_recheck_error.json"), JSON.stringify({ err: err.message, stack: err.stack }));
  } finally {
    chrome.kill();
  }
}

runRecheck();
