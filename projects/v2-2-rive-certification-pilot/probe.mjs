
import http from 'node:http';
import { spawn } from 'node:child_process';

const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
  '--headless=new',
  '--remote-debugging-port=9250',
  '--remote-allow-origins=*',
  '--disable-gpu',
  '--no-first-run',
  '--user-data-dir=C:\\Users\\ALPHA\\.gemini\\antigravity\\brain\\cd78e55d-acb8-4e22-8479-68acd50d474e\\scratch\\chrome-probe'
]);

await new Promise(r => setTimeout(r, 2000));

const listRes = await fetch('http://127.0.0.1:9250/json/list');
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

await send('Page.navigate', { url: 'http://127.0.0.1:8102/index.html' });
await new Promise(r => setTimeout(r, 3000));

const evalRes = await send('Runtime.evaluate', {
  expression: (() => {
    const r = window.riveInstance;
    const smNames = r ? r.stateMachineNames : [];
    const inputs = r ? r.stateMachineInputs('bumpy') : [];
    return {
      hasRive: !!window.rive,
      hasInstance: !!r,
      stateMachineNames: smNames,
      bumpyInputs: inputs ? inputs.map(i => ({ name: i.name, type: i.type, value: i.value })) : []
    };
  })(),
  returnByValue: true
});

console.log('PROBE_RESULT:', JSON.stringify(evalRes.result.value, null, 2));

ws.close();
chrome.kill();
process.exit(0);
