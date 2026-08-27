import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const USER_DATA_DIR = "C:\\Users\\ALPHA\\.gemini\\antigravity-ide\\brain\\95f9c0bb-8228-4701-a124-bca35ba39121\\scratch\\chrome-profile-asn-audit";
const QA_DIR = "C:\\Users\\ALPHA\\Desktop\\VIBE CODING PROJECTS\\WEBSITE-DIRECTOR\\projects\\alpha-starts-now-v1-1\\qa";
const BASE_URL = "http://localhost:8089";

fs.mkdirSync(USER_DATA_DIR, { recursive: true });

class SimpleCDP {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.id = 1;
    this.callbacks = new Map();
    this.consoleLogs = [];
    this.pageErrors = [];
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

        if (msg.id && this.callbacks.has(msg.id)) {
          const cb = this.callbacks.get(msg.id);
          this.callbacks.delete(msg.id);
          if (msg.error) cb.reject(new Error(JSON.stringify(msg.error)));
          else cb.resolve(msg.result);
        }
      };
    });
  }

  send(method, params = {}, timeoutMs = 5000) {
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

  async navigate(url) {
    await this.send("Page.navigate", { url });
    await new Promise(r => setTimeout(r, 600));
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

async function runDataAudit() {
  console.log("Launching Chrome for Data Audit...");
  const chrome = spawn(CHROME_PATH, [
    "--headless=new",
    "--remote-debugging-port=9224",
    "--remote-allow-origins=*",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    `--user-data-dir=${USER_DATA_DIR}`
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const listRes = await fetch("http://127.0.0.1:9224/json/list");
    const targets = await listRes.json();
    const pageTarget = targets.find(t => t.type === "page") || targets[0];

    const cdp = new SimpleCDP(pageTarget.webSocketDebuggerUrl);
    await cdp.connect();

    await cdp.send("Page.enable");
    await cdp.send("DOM.enable");
    await cdp.send("CSS.enable");
    await cdp.send("Runtime.enable");

    const audit = {
      pages_tested: {},
      start_here_tabs: [],
      guides_filter_results: [],
      dispatch_form_results: {},
      recommended_inventory: [],
      font_status: {},
      overflow_results: {},
      console_logs: [],
      page_errors: []
    };

    // 1. Index Page
    await cdp.navigate(`${BASE_URL}/index.html`);
    audit.pages_tested["index.html"] = await cdp.eval(`
      return {
        title: document.title,
        h1: document.querySelector('h1')?.innerText,
        kicker: document.querySelector('.section-kicker')?.innerText,
        heroBackdropStyle: window.getComputedStyle(document.querySelector('.hero-media-backdrop') || document.body).backgroundImage
      };
    `);

    // 2. Start Here Tabs
    await cdp.navigate(`${BASE_URL}/start-here.html`);
    for (const key of ["pathway-health", "pathway-style", "pathway-systems", "pathway-tech", "pathway-env"]) {
      const tabRes = await cdp.eval(`
        const btn = document.querySelector('[data-pathway-target="${key}"]');
        if (btn) btn.click();
        const panel = document.getElementById("${key}");
        return {
          key: "${key}",
          buttonFound: !!btn,
          panelFound: !!panel,
          panelVisible: panel ? window.getComputedStyle(panel).display !== 'none' : false,
          heading: panel ? panel.querySelector('h2')?.innerText : ''
        };
      `);
      audit.start_here_tabs.push(tabRes);
    }

    // 3. Guides Filters
    await cdp.navigate(`${BASE_URL}/guides.html`);
    for (const f of ["all", "health", "style", "discipline", "tech", "life"]) {
      const filterRes = await cdp.eval(`
        const btn = document.querySelector('.filter-btn[data-pillar="${f}"]');
        if (btn) btn.click();
        const cards = Array.from(document.querySelectorAll('.guide-article-card'));
        const visible = cards.filter(c => !c.classList.contains('is-hidden') && window.getComputedStyle(c).display !== 'none');
        return {
          filter: "${f}",
          totalCards: cards.length,
          visibleCards: visible.length
        };
      `);
      audit.guides_filter_results.push(filterRes);
    }

    // 4. Recommended Inventory
    await cdp.navigate(`${BASE_URL}/recommended.html`);
    audit.recommended_inventory = await cdp.eval(`
      return Array.from(document.querySelectorAll('.spec-card')).map(card => {
        return {
          tag: card.querySelector('.spec-tag')?.innerText || '',
          title: card.querySelector('.spec-title')?.innerText || '',
          details: card.querySelector('.spec-details')?.innerText || '',
          tradeoff: card.querySelector('.spec-tradeoff')?.innerText || '',
          linkHref: card.querySelector('a')?.getAttribute('href') || '',
          linkText: card.querySelector('a')?.innerText || ''
        };
      });
    `);

    // 5. Dispatch Form
    await cdp.navigate(`${BASE_URL}/dispatch.html`);
    audit.dispatch_form_results.empty = await cdp.eval(`
      const form = document.querySelector('.dispatch-form');
      const input = form.querySelector('input[type="email"]');
      input.value = '';
      form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
      return document.querySelector('.form-status-message')?.innerText || '';
    `);

    audit.dispatch_form_results.invalid = await cdp.eval(`
      const form = document.querySelector('.dispatch-form');
      const input = form.querySelector('input[type="email"]');
      input.value = 'invalid-email-string';
      form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
      return document.querySelector('.form-status-message')?.innerText || '';
    `);

    audit.dispatch_form_results.valid = await cdp.eval(`
      const form = document.querySelector('.dispatch-form');
      const input = form.querySelector('input[type="email"]');
      input.value = 'reader@alphastartsnow.com';
      form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
      return document.querySelector('.form-status-message')?.innerText || '';
    `);

    // 6. Font Check
    audit.font_status = await cdp.eval(`
      return {
        newsreaderLoaded: document.fonts.check('16px Newsreader'),
        plusJakartaLoaded: document.fonts.check('16px "Plus Jakarta Sans"'),
        h1FontFamily: window.getComputedStyle(document.querySelector('h1') || document.body).fontFamily,
        bodyFontFamily: window.getComputedStyle(document.body).fontFamily
      };
    `);

    // 7. Multi-viewport overflow
    const viewports = [
      { name: "360x800", w: 360, h: 800 },
      { name: "390x844", w: 390, h: 844 },
      { name: "768x1024", w: 768, h: 1024 },
      { name: "1024x768", w: 1024, h: 768 },
      { name: "1280x800", w: 1280, h: 800 },
      { name: "1440x900", w: 1440, h: 900 }
    ];
    const pages = ["index.html", "start-here.html", "guides.html", "recommended.html", "about.html", "dispatch.html", "privacy.html", "terms.html", "affiliate-disclosure.html"];

    for (const vp of viewports) {
      await cdp.send("Emulation.setDeviceMetricsOverride", {
        width: vp.w,
        height: vp.h,
        deviceScaleFactor: 1,
        mobile: vp.w < 800
      });
      audit.overflow_results[vp.name] = {};
      for (const pg of pages) {
        await cdp.navigate(`${BASE_URL}/${pg}`);
        const ovf = await cdp.eval(`
          return {
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            hasOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
          };
        `);
        audit.overflow_results[vp.name][pg] = ovf;
      }
    }

    audit.console_logs = cdp.consoleLogs;
    audit.page_errors = cdp.pageErrors;

    fs.writeFileSync(path.join(QA_DIR, "asn_data_audit_results.json"), JSON.stringify(audit, null, 2));
    console.log("Data audit completed successfully!");

    cdp.close();
  } catch (err) {
    console.error("Audit error:", err);
    fs.writeFileSync(path.join(QA_DIR, "asn_data_audit_error.json"), JSON.stringify({ err: err.message, stack: err.stack }));
  } finally {
    chrome.kill();
  }
}

runDataAudit();
