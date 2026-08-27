import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const USER_DATA_DIR = "C:\\Users\\ALPHA\\.gemini\\antigravity-ide\\brain\\95f9c0bb-8228-4701-a124-bca35ba39121\\scratch\\chrome-profile-asn-qa";
const QA_DIR = "C:\\Users\\ALPHA\\Desktop\\VIBE CODING PROJECTS\\WEBSITE-DIRECTOR\\projects\\alpha-starts-now-v1-1\\qa";
const EVIDENCE_DIR = path.join(QA_DIR, "evidence");
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
    this.networkRequests = [];
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
          this.consoleLogs.push(msg.params);
        }
        if (msg.method === "Runtime.exceptionThrown") {
          this.pageErrors.push(msg.params);
        }
        if (msg.method === "Network.requestWillBeSent") {
          this.networkRequests.push(msg.params);
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

  send(method, params = {}, timeoutMs = 15000) {
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
      expression,
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
    await new Promise(r => setTimeout(r, 1200));
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

async function runIndependentQA() {
  console.log("Starting Chrome instance for Independent QA...");
  const chrome = spawn(CHROME_PATH, [
    "--headless=new",
    "--remote-debugging-port=9223",
    "--remote-allow-origins=*",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    `--user-data-dir=${USER_DATA_DIR}`,
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
  ]);

  await new Promise(r => setTimeout(r, 2500));

  const auditReport = {
    timestamp: new Date().toISOString(),
    server_verified: false,
    page_identities: {},
    console_logs: [],
    page_errors: [],
    failed_requests: [],
    font_status: {},
    viewport_tests: {},
    interactive_tests: {},
    recommended_cards: [],
    screenshots_captured: []
  };

  try {
    const listRes = await fetch("http://127.0.0.1:9223/json/list");
    const targets = await listRes.json();
    const pageTarget = targets.find(t => t.type === "page") || targets[0];

    const cdp = new SimpleCDP(pageTarget.webSocketDebuggerUrl);
    await cdp.connect();

    await cdp.send("Page.enable");
    await cdp.send("DOM.enable");
    await cdp.send("CSS.enable");
    await cdp.send("Runtime.enable");
    await cdp.send("Network.enable");

    // 1. Verify Home Page on Desktop 1440x900
    await cdp.setViewport(1440, 900, 1, false);
    await cdp.navigate(`${BASE_URL}/index.html`);

    const title = await cdp.eval("document.title");
    const h1Text = await cdp.eval("document.querySelector('h1')?.innerText");
    const kickerText = await cdp.eval("document.querySelector('.hero-section .section-kicker')?.innerText");
    const brandTitle = await cdp.eval("document.querySelector('.brand-title')?.innerText");

    console.log(`Verified Home: Title="${title}", H1="${h1Text}", Kicker="${kickerText}"`);
    auditReport.server_verified = title.includes("Alpha Starts Now") && brandTitle.includes("ALPHA STARTS NOW");
    auditReport.page_identities["index.html"] = { title, h1Text, kickerText, brandTitle };

    // Capture 01_home_hero_desktop
    const heroShot = path.join(EVIDENCE_DIR, "01_home_hero_desktop.png");
    await cdp.captureScreenshot(heroShot, { x: 0, y: 0, width: 1440, height: 800, scale: 1 });
    auditReport.screenshots_captured.push("01_home_hero_desktop.png");

    // Scroll to middle and capture 02_home_body_desktop
    await cdp.eval("window.scrollTo(0, 1000)");
    await new Promise(r => setTimeout(r, 400));
    const bodyShot = path.join(EVIDENCE_DIR, "02_home_body_desktop.png");
    await cdp.captureScreenshot(bodyShot, { x: 0, y: 0, width: 1440, height: 900, scale: 1 });
    auditReport.screenshots_captured.push("02_home_body_desktop.png");

    // Scroll to section 6 (recommended) and capture 03_home_recommended_desktop
    await cdp.eval("document.querySelector('.section-recommended')?.scrollIntoView({behavior: 'instant'})");
    await new Promise(r => setTimeout(r, 400));
    const homeRecShot = path.join(EVIDENCE_DIR, "03_home_recommended_desktop.png");
    await cdp.captureScreenshot(homeRecShot, { x: 0, y: 0, width: 1440, height: 900, scale: 1 });
    auditReport.screenshots_captured.push("03_home_recommended_desktop.png");

    // 2. Start Here Page Desktop
    await cdp.navigate(`${BASE_URL}/start-here.html`);
    const startHereTitle = await cdp.eval("document.title");
    auditReport.page_identities["start-here.html"] = { title: startHereTitle };
    const startHereShot = path.join(EVIDENCE_DIR, "04_start_here_desktop.png");
    await cdp.captureScreenshot(startHereShot, { x: 0, y: 0, width: 1440, height: 900, scale: 1 });
    auditReport.screenshots_captured.push("04_start_here_desktop.png");

    // Test all 5 Start Here tabs
    const tabTestResults = [];
    const tabSelectors = [
      { key: "pathway-health", name: "01 Health & Strength" },
      { key: "pathway-style", name: "02 Style & Grooming" },
      { key: "pathway-systems", name: "03 Discipline & Systems" },
      { key: "pathway-tech", name: "04 Work & Technology" },
      { key: "pathway-env", name: "05 Life & Environment" }
    ];

    for (const tab of tabSelectors) {
      await cdp.eval(`
        (() => {
          const btn = document.querySelector('[data-pathway-target="${tab.key}"]');
          if (btn) btn.click();
        })()
      `);
      await new Promise(r => setTimeout(r, 200));
      const isVisible = await cdp.eval(`
        (() => {
          const p = document.getElementById("${tab.key}");
          return !!(p && window.getComputedStyle(p).display !== 'none');
        })()
      `);
      const heading = await cdp.eval(`
        (() => {
          const p = document.getElementById("${tab.key}");
          return p ? p.querySelector('h2')?.innerText : '';
        })()
      `);
      tabTestResults.push({ tab: tab.name, key: tab.key, isVisible, heading });
    }
    auditReport.interactive_tests["start_here_tabs"] = tabTestResults;

    // 3. Guides Page Desktop
    await cdp.navigate(`${BASE_URL}/guides.html`);
    const guidesTitle = await cdp.eval("document.title");
    auditReport.page_identities["guides.html"] = { title: guidesTitle };
    const guidesShot = path.join(EVIDENCE_DIR, "05_guides_desktop.png");
    await cdp.captureScreenshot(guidesShot, { x: 0, y: 0, width: 1440, height: 900, scale: 1 });
    auditReport.screenshots_captured.push("05_guides_desktop.png");

    // Test Guides filters
    const filterTests = [];
    for (const p of ["all", "health", "style", "discipline", "tech", "life"]) {
      await cdp.eval(`
        (() => {
          const btn = document.querySelector('.filter-btn[data-pillar="${p}"]');
          if (btn) btn.click();
        })()
      `);
      await new Promise(r => setTimeout(r, 200));
      const visibleCount = await cdp.eval(`
        (() => {
          return Array.from(document.querySelectorAll('.guide-article-card')).filter(c => !c.classList.contains('is-hidden') && window.getComputedStyle(c).display !== 'none').length;
        })()
      `);
      filterTests.push({ filter: p, visibleCards: visibleCount });
    }
    auditReport.interactive_tests["guides_filters"] = filterTests;

    // 4. Recommended Page Desktop
    await cdp.navigate(`${BASE_URL}/recommended.html`);
    const recTitle = await cdp.eval("document.title");
    auditReport.page_identities["recommended.html"] = { title: recTitle };
    const recShot = path.join(EVIDENCE_DIR, "06_recommended_desktop.png");
    await cdp.captureScreenshot(recShot, { x: 0, y: 0, width: 1440, height: 900, scale: 1 });
    auditReport.screenshots_captured.push("06_recommended_desktop.png");

    // Inspect all recommended items
    const recCards = await cdp.eval(`
      (() => {
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
      })()
    `);
    auditReport.recommended_cards = recCards;

    // 5. About Page Desktop
    await cdp.navigate(`${BASE_URL}/about.html`);
    const aboutTitle = await cdp.eval("document.title");
    auditReport.page_identities["about.html"] = { title: aboutTitle };
    const aboutShot = path.join(EVIDENCE_DIR, "07_about_desktop.png");
    await cdp.captureScreenshot(aboutShot, { x: 0, y: 0, width: 1440, height: 900, scale: 1 });
    auditReport.screenshots_captured.push("07_about_desktop.png");

    // 6. Dispatch Page Desktop
    await cdp.navigate(`${BASE_URL}/dispatch.html`);
    const dispatchTitle = await cdp.eval("document.title");
    auditReport.page_identities["dispatch.html"] = { title: dispatchTitle };
    const dispatchShot = path.join(EVIDENCE_DIR, "08_dispatch_desktop.png");
    await cdp.captureScreenshot(dispatchShot, { x: 0, y: 0, width: 1440, height: 900, scale: 1 });
    auditReport.screenshots_captured.push("08_dispatch_desktop.png");

    // Test form submissions
    // Empty submit
    await cdp.eval(`
      (() => {
        const form = document.querySelector('.dispatch-form');
        const input = form.querySelector('input[type="email"]');
        input.value = '';
        form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
      })()
    `);
    await new Promise(r => setTimeout(r, 200));
    const emptyMsg = await cdp.eval("document.querySelector('.form-status-message')?.innerText");

    // Invalid submit
    await cdp.eval(`
      (() => {
        const form = document.querySelector('.dispatch-form');
        const input = form.querySelector('input[type="email"]');
        input.value = 'invalid-email-test';
        form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
      })()
    `);
    await new Promise(r => setTimeout(r, 200));
    const invalidMsg = await cdp.eval("document.querySelector('.form-status-message')?.innerText");

    // Valid submit (boundary check)
    await cdp.eval(`
      (() => {
        const form = document.querySelector('.dispatch-form');
        const input = form.querySelector('input[type="email"]');
        input.value = 'audit.qa@alphastartsnow.com';
        form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
      })()
    `);
    await new Promise(r => setTimeout(r, 200));
    const validMsg = await cdp.eval("document.querySelector('.form-status-message')?.innerText");
    auditReport.interactive_tests["dispatch_form"] = { emptyMsg, invalidMsg, validMsg };

    // 7. Check Font Loading
    const fontCheck = await cdp.eval(`
      ({
        newsreaderLoaded: document.fonts.check('16px Newsreader'),
        plusJakartaLoaded: document.fonts.check('16px "Plus Jakarta Sans"'),
        h1FontFamily: window.getComputedStyle(document.querySelector('h1') || document.body).fontFamily,
        bodyFontFamily: window.getComputedStyle(document.body).fontFamily,
        heroTitleFontFamily: window.getComputedStyle(document.querySelector('.dispatch-title') || document.body).fontFamily
      })
    `);
    auditReport.font_status = fontCheck;

    // 8. Mobile Viewport QA (390x844)
    await cdp.setViewport(390, 844, 2, true);
    await cdp.navigate(`${BASE_URL}/index.html`);

    const mobHeroShot = path.join(EVIDENCE_DIR, "09_home_hero_mobile.png");
    await cdp.captureScreenshot(mobHeroShot, { x: 0, y: 0, width: 390, height: 844, scale: 1 });
    auditReport.screenshots_captured.push("09_home_hero_mobile.png");

    // Mobile Hamburger drawer test
    await cdp.eval("document.querySelector('.mobile-menu-toggle')?.click()");
    await new Promise(r => setTimeout(r, 400));
    const drawerOpenShot = path.join(EVIDENCE_DIR, "10_mobile_nav_open.png");
    await cdp.captureScreenshot(drawerOpenShot, { x: 0, y: 0, width: 390, height: 844, scale: 1 });
    auditReport.screenshots_captured.push("10_mobile_nav_open.png");

    const drawerAria = await cdp.eval("document.querySelector('.mobile-menu-toggle')?.getAttribute('aria-expanded')");
    const drawerClass = await cdp.eval("document.querySelector('.mobile-drawer')?.classList.contains('is-open')");
    auditReport.interactive_tests["mobile_drawer"] = { ariaExpanded: drawerAria, hasClassIsOpen: drawerClass };

    // Close drawer
    await cdp.eval("document.querySelector('.mobile-menu-toggle')?.click()");
    await new Promise(r => setTimeout(r, 300));

    // Scroll mobile body
    await cdp.eval("window.scrollTo(0, 1100)");
    await new Promise(r => setTimeout(r, 400));
    const mobBodyShot = path.join(EVIDENCE_DIR, "11_home_body_mobile.png");
    await cdp.captureScreenshot(mobBodyShot, { x: 0, y: 0, width: 390, height: 844, scale: 1 });
    auditReport.screenshots_captured.push("11_home_body_mobile.png");

    // Mobile Start Here
    await cdp.navigate(`${BASE_URL}/start-here.html`);
    const mobStartShot = path.join(EVIDENCE_DIR, "12_start_here_mobile.png");
    await cdp.captureScreenshot(mobStartShot, { x: 0, y: 0, width: 390, height: 844, scale: 1 });
    auditReport.screenshots_captured.push("12_start_here_mobile.png");

    // Mobile Guides
    await cdp.navigate(`${BASE_URL}/guides.html`);
    const mobGuidesShot = path.join(EVIDENCE_DIR, "13_guides_mobile.png");
    await cdp.captureScreenshot(mobGuidesShot, { x: 0, y: 0, width: 390, height: 844, scale: 1 });
    auditReport.screenshots_captured.push("13_guides_mobile.png");

    // Mobile Recommended
    await cdp.navigate(`${BASE_URL}/recommended.html`);
    const mobRecShot = path.join(EVIDENCE_DIR, "14_recommended_mobile.png");
    await cdp.captureScreenshot(mobRecShot, { x: 0, y: 0, width: 390, height: 844, scale: 1 });
    auditReport.screenshots_captured.push("14_recommended_mobile.png");

    // Mobile Dispatch
    await cdp.navigate(`${BASE_URL}/dispatch.html`);
    const mobDispatchShot = path.join(EVIDENCE_DIR, "15_dispatch_mobile.png");
    await cdp.captureScreenshot(mobDispatchShot, { x: 0, y: 0, width: 390, height: 844, scale: 1 });
    auditReport.screenshots_captured.push("15_dispatch_mobile.png");

    // 9. Accessibility: Reduced Motion & Keyboard Focus
    // Reduced motion test on home hero
    await cdp.setViewport(1440, 900, 1, false);
    await cdp.send("Emulation.setEmulatedMedia", {
      features: [{ name: "prefers-reduced-motion", value: "reduce" }]
    });
    await cdp.navigate(`${BASE_URL}/index.html`);
    const reducedMotionShot = path.join(EVIDENCE_DIR, "16_reduced_motion_hero.png");
    await cdp.captureScreenshot(reducedMotionShot, { x: 0, y: 0, width: 1440, height: 800, scale: 1 });
    auditReport.screenshots_captured.push("16_reduced_motion_hero.png");

    // Keyboard focus test
    await cdp.eval(`
      const cta = document.querySelector('.hero-actions .btn-primary');
      if (cta) cta.focus();
    `);
    await new Promise(r => setTimeout(r, 200));
    const focusShot = path.join(EVIDENCE_DIR, "17_keyboard_focus_example.png");
    await cdp.captureScreenshot(focusShot, { x: 0, y: 0, width: 1440, height: 800, scale: 1 });
    auditReport.screenshots_captured.push("17_keyboard_focus_example.png");

    // 10. Multi-viewport overflow test (360, 390, 768, 1024, 1280, 1440, 1600)
    const viewports = [
      { name: "360x800", w: 360, h: 800, mob: true },
      { name: "390x844", w: 390, h: 844, mob: true },
      { name: "768x1024", w: 768, h: 1024, mob: true },
      { name: "1024x768", w: 1024, h: 768, mob: false },
      { name: "1280x800", w: 1280, h: 800, mob: false },
      { name: "1440x900", w: 1440, h: 900, mob: false },
      { name: "1600x1000", w: 1600, h: 1000, mob: false }
    ];

    const pages = ["index.html", "start-here.html", "guides.html", "recommended.html", "about.html", "dispatch.html", "privacy.html", "terms.html", "affiliate-disclosure.html"];

    for (const vp of viewports) {
      await cdp.setViewport(vp.w, vp.h, 1, vp.mob);
      auditReport.viewport_tests[vp.name] = {};
      for (const pg of pages) {
        await cdp.navigate(`${BASE_URL}/${pg}`);
        const overflow = await cdp.eval(`
          ({
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            hasHorizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
          })
        `);
        auditReport.viewport_tests[vp.name][pg] = overflow;
      }
    }

    // 11. Collect Console Logs & Errors
    auditReport.console_logs = cdp.consoleLogs;
    auditReport.page_errors = cdp.pageErrors;
    auditReport.failed_requests = cdp.failedRequests;

    // Save full JSON audit data
    fs.writeFileSync(path.join(QA_DIR, "asn_qa_audit_results.json"), JSON.stringify(auditReport, null, 2));
    console.log("Independent QA Runner successfully completed!");

    cdp.close();
  } catch (err) {
    console.error("QA Execution Error:", err);
    fs.writeFileSync(path.join(QA_DIR, "asn_qa_error.json"), JSON.stringify({ error: err.message, stack: err.stack }));
  } finally {
    chrome.kill();
  }
}

runIndependentQA();
