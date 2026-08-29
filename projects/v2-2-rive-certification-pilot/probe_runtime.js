import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const PILOT_DIR = 'C:\\Users\\ALPHA\\Desktop\\VIBE CODING PROJECTS\\WEBSITE-DIRECTOR\\projects\\v2-2-rive-certification-pilot';
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const USER_DATA = 'C:\\Users\\ALPHA\\.gemini\\antigravity\\brain\\cd78e55d-acb8-4e22-8479-68acd50d474e\\scratch\\chrome-probe-final';

const mimeTypes = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.wasm': 'application/wasm',
  '.riv': 'application/octet-stream'
};

const server = http.createServer((req, res) => {
  let reqPath = req.url.split('?')[0];
  if (reqPath === '/') reqPath = '/index.html';
  const filePath = path.join(PILOT_DIR, reqPath);
  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    res.setHeader('Content-Type', mimeTypes[path.extname(filePath)] || 'application/octet-stream');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.end(fs.readFileSync(filePath));
  } else {
    res.statusCode = 404;
    res.end();
  }
});

server.listen(8105, '127.0.0.1', async () => {
  const chrome = spawn(CHROME_PATH, [
    '--headless=new',
    '--remote-debugging-port=9255',
    '--remote-allow-origins=*',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    '--user-data-dir=' + USER_DATA
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const listRes = await fetch('http://127.0.0.1:9255/json/list');
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

    await send('Page.navigate', { url: 'http://127.0.0.1:8105/index.html' });
    await new Promise(r => setTimeout(r, 2000));

    // Evaluate in browser
    const code = 
      new Promise((resolve) => {
        const r = new window.rive.Rive({
          src: './assets/vehicles.riv',
          canvas: document.createElement('canvas'),
          autoplay: false,
          stateMachines: 'bumpy',
          onLoad: () => {
            const smNames = r.stateMachineNames;
            const inputs = r.stateMachineInputs('bumpy');
            const bump = inputs ? inputs.find(i => i.name === 'bump') : null;
            
            const events = [];
            r.on('statechange', (evt) => {
              events.push(evt.data);
            });

            // Fire trigger twice
            if (bump) {
              bump.fire();
              setTimeout(() => {
                bump.fire();
                setTimeout(() => {
                  resolve({
                    stateMachineNames: smNames,
                    inputs: inputs ? inputs.map(i => ({ name: i.name, type: typeof i.fire === 'function' ? 'Trigger' : typeof i.value })) : [],
                    events: events
                  });
                }, 300);
              }, 300);
            } else {
              resolve({
                stateMachineNames: smNames,
                inputs: inputs ? inputs.map(i => ({ name: i.name, type: typeof i.fire === 'function' ? 'Trigger' : typeof i.value })) : [],
                events: events
              });
            }
          },
          onError: (e) => resolve({ error: String(e) })
        });
      })
    ;

    const res = await send('Runtime.evaluate', {
      expression: code,
      awaitPromise: true,
      returnByValue: true
    });

    console.log('RUNTIME_INSPECTION_RESULT:', JSON.stringify(res.result.value, null, 2));

    ws.close();
  } catch (err) {
    console.error('Probe error:', err);
  } finally {
    chrome.kill();
    server.close();
    process.exit(0);
  }
});
