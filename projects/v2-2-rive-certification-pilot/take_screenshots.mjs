import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';

const PILOT_DIR = 'C:\\Users\\ALPHA\\Desktop\\VIBE CODING PROJECTS\\WEBSITE-DIRECTOR\\projects\\v2-2-rive-certification-pilot';
const EVIDENCE_DIR = path.join(PILOT_DIR, 'evidence');
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const USER_DATA = 'C:\\Users\\ALPHA\\.gemini\\antigravity\\brain\\cd78e55d-acb8-4e22-8479-68acd50d474e\\scratch\\chrome-rive-mjs';

const server = http.createServer((req, res) => {
  let reqPath = req.url.split('?')[0];
  if (reqPath === '/') reqPath = '/index.html';
  const filePath = path.join(PILOT_DIR, reqPath);
  if (fs.existsSync(filePath)) {
    if (filePath.endsWith('.wasm')) res.setHeader('Content-Type', 'application/wasm');
    else if (filePath.endsWith('.js')) res.setHeader('Content-Type', 'application/javascript');
    else if (filePath.endsWith('.html')) res.setHeader('Content-Type', 'text/html');
    else if (filePath.endsWith('.riv')) res.setHeader('Content-Type', 'application/octet-stream');
    res.end(fs.readFileSync(filePath));
  } else {
    res.statusCode = 404;
    res.end();
  }
});

server.listen(8097, '127.0.0.1', async () => {
  const chrome = spawn(CHROME_PATH, [
    '--headless=new',
    '--remote-debugging-port=9245',
    '--remote-allow-origins=*',
    '--disable-gpu',
    '--no-first-run',
    '--user-data-dir=' + USER_DATA
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const listRes = await fetch('http://127.0.0.1:9245/json/list');
    const targets = await listRes.json();
    const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);

    let msgId = 1;
    function send(method, params = {}) {
      return new Promise((resolve, reject) => {
        const id = msgId++;
        const handler = (evt) => {
          const data = JSON.parse(evt.data.toString());
          if (data.id === id) {
            ws.removeEventListener('message', handler);
            if (data.error) reject(data.error);
            else resolve(data.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id, method, params }));
      });
    }

    await send('Page.enable');
    await send('DOM.enable');

    const viewports = [
      ['desktop-1440x900.png', 1440, 900, 'http://127.0.0.1:8097/index.html', false],
      ['tablet-768x1024.png', 768, 1024, 'http://127.0.0.1:8097/index.html', false],
      ['mobile-375x812.png', 375, 812, 'http://127.0.0.1:8097/index.html', false],
      ['fallback-1440x900.png', 1440, 900, 'http://127.0.0.1:8097/index.html?forceRiveFallback=1', false],
      ['reduced-motion-1440x900.png', 1440, 900, 'http://127.0.0.1:8097/index.html', true]
    ];

    for (const [name, w, h, url, redMot] of viewports) {
      await send('Emulation.setDeviceMetricsOverride', {
        width: w,
        height: h,
        deviceScaleFactor: 1,
        mobile: (w < 768)
      });

      if (redMot) {
        await send('Emulation.setEmulatedMedia', {
          features: [{ name: 'prefers-reduced-motion', value: 'reduce' }]
        });
      } else {
        await send('Emulation.setEmulatedMedia', { features: [] });
      }

      await send('Page.navigate', { url });
      await new Promise(r => setTimeout(r, 2000));

      const shot = await send('Page.captureScreenshot', { format: 'png' });
      const buf = Buffer.from(shot.data, 'base64');
      const outPath = path.join(EVIDENCE_DIR, name);
      fs.writeFileSync(outPath, buf);
      console.log('Captured ' + name + ': ' + buf.length + ' bytes');
    }

    ws.close();
    chrome.kill();
    server.close();
    process.exit(0);
  } catch (e) {
    console.error(e);
    chrome.kill();
    server.close();
    process.exit(1);
  }
});
