import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const USER_DATA_DIR = "C:\\Users\\ALPHA\\.gemini\\antigravity-ide\\brain\\4fec1acf-7d52-414f-8c8b-031f73ea902c\\scratch\\chrome-profile-hosp";
const RESEARCH_DIR = "C:\\Users\\ALPHA\\Desktop\\VIBE CODING PROJECTS\\WEBSITE-DIRECTOR\\projects\\v1-1-luxury-hospitality-pilot\\research";

fs.mkdirSync(RESEARCH_DIR, { recursive: true });

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

  send(method, params = {}, timeoutMs = 20000) {
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

  close() {
    if (this.ws) this.ws.close();
  }
}

async function inspectTarget(targetName, url) {
  console.log(`\n========================================\nDeep Recon on: ${targetName} (${url})\n========================================`);
  const chrome = spawn(CHROME_PATH, [
    "--headless=new",
    "--remote-debugging-port=9222",
    "--remote-allow-origins=*",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    `--user-data-dir=${USER_DATA_DIR}`,
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const listRes = await fetch("http://127.0.0.1:9222/json/list");
    const targets = await listRes.json();
    const pageTarget = targets.find(t => t.type === "page") || targets[0];

    const cdp = new SimpleCDP(pageTarget.webSocketDebuggerUrl);
    await cdp.connect();

    await cdp.send("Page.enable");
    await cdp.send("DOM.enable");
    await cdp.send("CSS.enable");
    await cdp.send("Runtime.enable");

    // 1. Desktop Viewport 1440px
    await cdp.send("Emulation.setDeviceMetricsOverride", {
      width: 1440,
      height: 900,
      deviceScaleFactor: 1,
      mobile: false
    });

    console.log(`Navigating to ${url}...`);
    try {
      await cdp.send("Page.navigate", { url }, 15000);
    } catch (e) {
      console.warn("Navigation event warning:", e.message);
    }
    await new Promise(r => setTimeout(r, 5000));

    const ssDesktop = await cdp.send("Page.captureScreenshot", { format: "png" });
    const desktopPath = path.join(RESEARCH_DIR, `recon_${targetName}_desktop_1440.png`);
    fs.writeFileSync(desktopPath, Buffer.from(ssDesktop.data, 'base64'));
    console.log(`Saved Desktop Screenshot: ${desktopPath}`);

    // Capture Real Rendered DOM Typography and Layout
    const desktopMetrics = await cdp.send("Runtime.evaluate", {
      expression: `(() => {
        const title = document.title;
        const h1 = document.querySelector('h1');
        const h1Style = h1 ? window.getComputedStyle(h1) : null;
        
        const hero = document.querySelector('header, main, section, [class*="hero"]') || document.body;
        const heroStyle = window.getComputedStyle(hero);

        const btn = document.querySelector('a[class*="btn"], a[class*="button"], button');
        const btnStyle = btn ? window.getComputedStyle(btn) : null;

        const bodyStyle = window.getComputedStyle(document.body);

        return {
          title,
          bodyBg: bodyStyle.backgroundColor,
          bodyColor: bodyStyle.color,
          h1: h1 ? {
            text: h1.innerText.trim().substring(0, 80),
            fontFamily: h1Style.fontFamily,
            fontSize: h1Style.fontSize,
            fontWeight: h1Style.fontWeight,
            lineHeight: h1Style.lineHeight,
            letterSpacing: h1Style.letterSpacing,
            color: h1Style.color
          } : null,
          heroLayout: {
            tagName: hero.tagName,
            width: heroStyle.width,
            maxWidth: heroStyle.maxWidth,
            padding: \`\${heroStyle.paddingTop} \${heroStyle.paddingRight} \${heroStyle.paddingBottom} \${heroStyle.paddingLeft}\`,
            display: heroStyle.display,
            flexDirection: heroStyle.flexDirection,
            gap: heroStyle.gap
          },
          button: btn ? {
            text: btn.innerText.trim().substring(0, 40),
            fontFamily: btnStyle.fontFamily,
            fontSize: btnStyle.fontSize,
            backgroundColor: btnStyle.backgroundColor,
            color: btnStyle.color,
            borderRadius: btnStyle.borderRadius,
            padding: \`\${btnStyle.paddingTop} \${btnStyle.paddingRight} \${btnStyle.paddingBottom} \${btnStyle.paddingLeft}\`
          } : null
        };
      })()`,
      returnByValue: true
    });

    // 2. Mobile Viewport 390px
    await cdp.send("Emulation.setDeviceMetricsOverride", {
      width: 390,
      height: 844,
      deviceScaleFactor: 3,
      mobile: true
    });
    await new Promise(r => setTimeout(r, 2500));

    const ssMobile = await cdp.send("Page.captureScreenshot", { format: "png" });
    const mobilePath = path.join(RESEARCH_DIR, `recon_${targetName}_mobile_390.png`);
    fs.writeFileSync(mobilePath, Buffer.from(ssMobile.data, 'base64'));
    console.log(`Saved Mobile Screenshot: ${mobilePath}`);

    const mobileMetrics = await cdp.send("Runtime.evaluate", {
      expression: `(() => {
        const h1 = document.querySelector('h1');
        const h1Style = h1 ? window.getComputedStyle(h1) : null;
        const hero = document.querySelector('header, main, section, [class*="hero"]') || document.body;
        const heroStyle = window.getComputedStyle(hero);
        const menuBtn = document.querySelector('button[aria-label*="menu" i], [class*="menu"], [class*="hamburger"]');

        return {
          h1: h1 ? {
            fontSize: h1Style.fontSize,
            lineHeight: h1Style.lineHeight
          } : null,
          heroLayout: {
            width: heroStyle.width,
            padding: \`\${heroStyle.paddingTop} \${heroStyle.paddingRight} \${heroStyle.paddingBottom} \${heroStyle.paddingLeft}\`
          },
          mobileMenuDetected: !!menuBtn
        };
      })()`,
      returnByValue: true
    });

    cdp.close();

    return {
      targetName,
      url,
      timestamp: new Date().toISOString(),
      desktop: {
        screenshot: desktopPath,
        metrics: desktopMetrics.result.value
      },
      mobile: {
        screenshot: mobilePath,
        metrics: mobileMetrics.result.value
      }
    };
  } finally {
    chrome.kill();
  }
}

async function runAll() {
  const targets = [
    { name: "linear_app", url: "https://linear.app" },
    { name: "resend_com", url: "https://resend.com" },
    { name: "stripe_com", url: "https://stripe.com" }
  ];

  const results = [];
  for (const t of targets) {
    try {
      const res = await inspectTarget(t.name, t.url);
      results.push(res);
      await new Promise(r => setTimeout(r, 2000));
    } catch (err) {
      console.error(`Failed on ${t.name}:`, err);
    }
  }

  const outPath = path.join(RESEARCH_DIR, "deep_recon_raw_data.json");
  fs.writeFileSync(outPath, JSON.stringify(results, null, 2));
  console.log(`\nAll Deep Recon Complete! Wrote results to: ${outPath}`);
}

runAll().catch(console.error);
