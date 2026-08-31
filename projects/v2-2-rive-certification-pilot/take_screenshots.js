import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';

const PILOT_DIR = 'C:\\Users\\ALPHA\\Desktop\\VIBE CODING PROJECTS\\WEBSITE-DIRECTOR\\projects\\v2-2-rive-certification-pilot';
const EVIDENCE_DIR = path.join(PILOT_DIR, 'evidence');
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const USER_DATA = 'C:\\Users\\ALPHA\\.gemini\\antigravity\\brain\\cd78e55d-acb8-4e22-8479-68acd50d474e\\scratch\\chrome-rive-standalone';

const mimeTypes = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.wasm': 'application/wasm',
  '.riv': 'application/octet-stream',
  '.css': 'text/css'
};

const server = http.createServer((req, res) => {
  let reqPath = req.url.split('?')[0];
  if (reqPath === '/') reqPath = '/index.html';
  const filePath = path.join(PILOT_DIR, reqPath);
  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = path.extname(filePath);
    res.setHeader('Content-Type', mimeTypes[ext] || 'application/octet-stream');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.end(fs.readFileSync(filePath));
  } else {
    res.statusCode = 404;
    res.end();
  }
});

server.listen(8098, '127.0.0.1', async () => {
  const chrome = spawn(CHROME_PATH, [
    '--headless=new',
    '--remote-debugging-port=9246',
    '--remote-allow-origins=*',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    '--user-data-dir=' + USER_DATA
  ]);

  await new Promise(r => setTimeout(r, 2500));

  try {
    const listRes = await fetch('http://127.0.0.1:9246/json/list');
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

    const viewports = [
      { name: 'desktop-1440x900.png', w: 1440, h: 900, url: 'http://127.0.0.1:8098/index.html', redMot: false },
      { name: 'tablet-768x1024.png', w: 768, h: 1024, url: 'http://127.0.0.1:8098/index.html', redMot: false },
      { name: 'mobile-375x812.png', w: 375, h: 812, url: 'http://127.0.0.1:8098/index.html', redMot: false },
      { name: 'fallback-1440x900.png', w: 1440, h: 900, url: 'http://127.0.0.1:8098/index.html?forceRiveFallback=1', redMot: false },
      { name: 'reduced-motion-1440x900.png', w: 1440, h: 900, url: 'http://127.0.0.1:8098/index.html', redMot: true }
    ];

    for (const vp of viewports) {
      await send('Emulation.setDeviceMetricsOverride', {
        width: vp.w,
        height: vp.h,
        deviceScaleFactor: 1,
        mobile: (vp.w < 768)
      });

      if (vp.redMot) {
        await send('Emulation.setEmulatedMedia', {
          features: [{ name: 'prefers-reduced-motion', value: 'reduce' }]
        });
      } else {
        await send('Emulation.setEmulatedMedia', { features: [] });
      }

      await send('Page.navigate', { url: vp.url });
      await new Promise(r => setTimeout(r, 2000));

      const shot = await send('Page.captureScreenshot', { format: 'png' });
      const outPath = path.join(EVIDENCE_DIR, vp.name);
      fs.writeFileSync(outPath, Buffer.from(shot.data, 'base64'));
      console.log('Saved ' + vp.name + ' (' + fs.statSync(outPath).size + ' bytes)');
    }

    ws.close();
  } catch (err) {
    console.error('Error during screenshot capture:', err);
  } finally {
    chrome.kill();
    server.close();
    process.exit(0);
  }
});
