
import { spawn } from 'node:child_process';

const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
  '--headless=new',
  '--remote-debugging-port=9252',
  '--remote-allow-origins=*',
  '--disable-gpu',
  '--no-first-run',
  '--user-data-dir=C:\\Users\\ALPHA\\.gemini\\antigravity\\brain\\cd78e55d-acb8-4e22-8479-68acd50d474e\\scratch\\chrome-probe3'
]);

await new Promise(r => setTimeout(r, 2000));

const listRes = await fetch('http://127.0.0.1:9252/json/list');
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

await send('Page.navigate', { url: 'http://127.0.0.1:8104/index.html' });
await new Promise(r => setTimeout(r, 2500));

const expr = (() => {
  return new Promise((resolve) => {
    const r = new window.rive.Rive({
      src: './assets/vehicles.riv',
      canvas: document.createElement('canvas'),
      autoplay: false,
      onLoad: () => {
        const smNames = r.stateMachineNames;
        const bumpyInputs = r.stateMachineInputs('bumpy') || [];
        resolve({
          stateMachineNames: smNames,
          bumpyInputs: bumpyInputs.map(i => ({ name: i.name, type: typeof i.fire === 'function' ? 'Trigger' : typeof i.value }))
        });
      },
      onError: (e) => resolve({ error: String(e) })
    });
  });
})();

const evalRes = await send('Runtime.evaluate', {
  expression: expr,
  awaitPromise: true,
  returnByValue: true
});

console.log('PROBE_RESULT:', JSON.stringify(evalRes.result.value, null, 2));

ws.close();
chrome.kill();
process.exit(0);
