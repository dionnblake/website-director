import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const CHROME_PATH = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const USER_DATA_DIR = "C:\\Users\\ALPHA\\.gemini\\antigravity-ide\\brain\\076d5d28-af05-42d6-938a-6823b74e3c1b\\scratch\\chrome-recon-asn";
const RESEARCH_DIR = "C:\\Users\\ALPHA\\Desktop\\VIBE CODING PROJECTS\\WEBSITE-DIRECTOR\\projects\\alpha-starts-now-v1-1\\research";

fs.mkdirSync(RESEARCH_DIR, { recursive: true });
fs.mkdirSync(USER_DATA_DIR, { recursive: true });

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

  send(method, params = {}, timeoutMs = 25000) {
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

async function runRecon() {
  console.log("Launching headless Chrome for live deep recon...");
  const chromeProcess = spawn(CHROME_PATH, [
    "--headless=new",
    "--remote-debugging-port=9222",
    "--remote-allow-origins=*",
    `--user-data-dir=${USER_DATA_DIR}`,
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-features=Translate",
    "--window-size=1440,900"
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const listRes = await fetch("http://127.0.0.1:9222/json/list");
    const targetsList = await listRes.json();
    const pageTarget = targetsList.find(t => t.type === "page") || targetsList[0];

    console.log("Connected to Chrome Page Target:", pageTarget.webSocketDebuggerUrl);
    const cdp = new SimpleCDP(pageTarget.webSocketDebuggerUrl);
    await cdp.connect();

    await cdp.send("Page.enable");
    await cdp.send("Runtime.enable");
    await cdp.send("DOM.enable");
    await cdp.send("CSS.enable");

    // 1. Audit Landbook live
    console.log("Auditing Landbook live access...");
    await cdp.send("Page.navigate", { url: "https://land-book.com/" });
    await new Promise(r => setTimeout(r, 4500));
    const landbookDoc = await cdp.send("Runtime.evaluate", {
      expression: `JSON.stringify({
        title: document.title,
        url: window.location.href,
        bodyTextSnippet: document.body ? document.body.innerText.substring(0, 300) : "",
        isCloudflare: document.title.includes("Just a moment") || (document.body && document.body.innerText.includes("Cloudflare")) || (document.body && document.body.innerText.includes("Turnstile"))
      })`,
      returnByValue: true
    });
    const landbookResult = JSON.parse(landbookDoc.result.value);
    console.log("Landbook audit result:", landbookResult);

    const landbookShot = await cdp.send("Page.captureScreenshot", { format: "png" });
    fs.writeFileSync(path.join(RESEARCH_DIR, "landbook_rendered_evidence.png"), Buffer.from(landbookShot.data, "base64"));
    fs.writeFileSync(path.join(RESEARCH_DIR, "landbook_audit_result.json"), JSON.stringify(landbookResult, null, 2));

    // Targets for deep DOM measurement
    const targets = [
      { name: "resend_com", url: "https://resend.com" },
      { name: "linear_app", url: "https://linear.app" },
      { name: "gearpatrol_com", url: "https://www.gearpatrol.com" }
    ];

    const rawReconData = [];

    for (const target of targets) {
      console.log(`\nReconnaissance on ${target.name} (${target.url})...`);
      
      // Desktop Viewport (1440x900)
      await cdp.send("Emulation.setDeviceMetricsOverride", {
        width: 1440,
        height: 900,
        deviceScaleFactor: 1,
        mobile: false
      });

      try {
        await cdp.send("Page.navigate", { url: target.url });
        await new Promise(r => setTimeout(r, 5500));

        const desktopShot = await cdp.send("Page.captureScreenshot", { format: "png" });
        const desktopShotPath = path.join(RESEARCH_DIR, `recon_${target.name}_desktop_1440.png`);
        fs.writeFileSync(desktopShotPath, Buffer.from(desktopShot.data, "base64"));

        const desktopMetrics = await cdp.send("Runtime.evaluate", {
          expression: `(() => {
            const h1 = document.querySelector('h1');
            const h1Style = h1 ? window.getComputedStyle(h1) : null;
            const bodyStyle = window.getComputedStyle(document.body);
            const header = document.querySelector('header') || document.querySelector('nav') || document.querySelector('section');
            const headerStyle = header ? window.getComputedStyle(header) : null;
            const button = document.querySelector('button') || document.querySelector('a.button') || document.querySelector('a[href*="sign"]') || document.querySelector('a[href*="get"]');
            const buttonStyle = button ? window.getComputedStyle(button) : null;

            return JSON.stringify({
              title: document.title,
              bodyBg: bodyStyle.backgroundColor,
              bodyColor: bodyStyle.color,
              bodyFont: bodyStyle.fontFamily,
              h1: h1 ? {
                text: h1.innerText.substring(0, 100),
                fontFamily: h1Style.fontFamily,
                fontSize: h1Style.fontSize,
                fontWeight: h1Style.fontWeight,
                lineHeight: h1Style.lineHeight,
                letterSpacing: h1Style.letterSpacing,
                color: h1Style.color
              } : null,
              layout: header ? {
                tagName: header.tagName,
                width: headerStyle.width,
                maxWidth: headerStyle.maxWidth,
                padding: headerStyle.padding,
                display: headerStyle.display
              } : null,
              button: button ? {
                text: button.innerText.substring(0, 50),
                fontFamily: buttonStyle.fontFamily,
                fontSize: buttonStyle.fontSize,
                backgroundColor: buttonStyle.backgroundColor,
                color: buttonStyle.color,
                borderRadius: buttonStyle.borderRadius,
                padding: buttonStyle.padding
              } : null
            });
          })()`,
          returnByValue: true
        });

        const parsedDesktop = JSON.parse(desktopMetrics.result.value);

        // Mobile Viewport (390x844)
        await cdp.send("Emulation.setDeviceMetricsOverride", {
          width: 390,
          height: 844,
          deviceScaleFactor: 2,
          mobile: true
        });
        await new Promise(r => setTimeout(r, 3000));

        const mobileShot = await cdp.send("Page.captureScreenshot", { format: "png" });
        const mobileShotPath = path.join(RESEARCH_DIR, `recon_${target.name}_mobile_390.png`);
        fs.writeFileSync(mobileShotPath, Buffer.from(mobileShot.data, "base64"));

        const mobileMetrics = await cdp.send("Runtime.evaluate", {
          expression: `(() => {
            const h1 = document.querySelector('h1');
            const h1Style = h1 ? window.getComputedStyle(h1) : null;
            const mobileMenu = document.querySelector('[aria-label*="menu"]') || document.querySelector('.menu-button') || document.querySelector('button[aria-expanded]') || document.querySelector('svg');
            return JSON.stringify({
              h1: h1 ? {
                fontSize: h1Style.fontSize,
                lineHeight: h1Style.lineHeight
              } : null,
              mobileMenuDetected: !!mobileMenu
            });
          })()`,
          returnByValue: true
        });

        const parsedMobile = JSON.parse(mobileMetrics.result.value);

        rawReconData.push({
          targetName: target.name,
          url: target.url,
          timestamp: new Date().toISOString(),
          desktop: {
            screenshot: desktopShotPath,
            metrics: parsedDesktop
          },
          mobile: {
            screenshot: mobileShotPath,
            metrics: parsedMobile
          }
        });

        console.log(`Successfully extracted raw DOM for ${target.name}`);
      } catch (err) {
        console.error(`Error measuring ${target.name}:`, err.message);
      }
    }

    fs.writeFileSync(
      path.join(RESEARCH_DIR, "deep_recon_raw_data.json"),
      JSON.stringify(rawReconData, null, 2)
    );
    console.log("Raw deep recon JSON persisted successfully.");

    cdp.close();
  } finally {
    chromeProcess.kill();
  }
}

runRecon().catch(console.error);
