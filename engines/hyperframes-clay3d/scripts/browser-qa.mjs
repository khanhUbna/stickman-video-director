import puppeteer from 'puppeteer-core';
import { createServer } from 'node:http';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { engineRoot, localEnvironment } from './hf.mjs';

const output = path.join(engineRoot, 'output'); await mkdir(output, { recursive: true });
const server = createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const relative = decodeURIComponent(url.pathname).replace(/^\/+/, '') || 'index.html';
  if (relative !== 'index.html' && !relative.startsWith('assets/')) { res.writeHead(404).end(); return; }
  const file = path.resolve(engineRoot, relative);
  if (!file.startsWith(engineRoot + path.sep)) { res.writeHead(403).end(); return; }
  try {
    const body = await readFile(file);
    res.setHeader('Content-Type', file.endsWith('.js') ? 'text/javascript' : file.endsWith('.wav') ? 'audio/wav' : 'text/html'); res.end(body);
  } catch { res.writeHead(404).end(); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
let browser;
try {
  browser = await puppeteer.launch({ executablePath: localEnvironment().HYPERFRAMES_BROWSER_PATH, headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--disable-background-networking'], defaultViewport: { width: 1920, height: 1080, deviceScaleFactor: 1 } });
  const page = await browser.newPage(); const failures = []; const external = [];
  page.on('pageerror', error => { failures.push(error.message); console.error('Browser page error:', error.message); });
  await page.setRequestInterception(true);
  page.on('request', req => {
    if (req.url().startsWith(`http://127.0.0.1:${server.address().port}/`) || /^(data:|blob:)/.test(req.url())) req.continue();
    else { external.push(req.url()); req.abort(); }
  });
  const response = await page.goto(`http://127.0.0.1:${server.address().port}/`, { waitUntil: 'load', timeout: 60000 });
  if (!response.ok()) throw new Error(`Composition HTTP ${response.status()}`);
  if (failures.length) throw new Error(failures.join('\n'));
  await page.waitForFunction(() => !!window.__clay3d, { timeout: 60000 });
  await page.evaluate(() => window.__clay3d.ready);
  const samples = [];
  for (const t of [0, 1.2, 2.5, 4.8, 5.65, 6.8, 7.5, 8.7, 9.3, 10, 11.6, 13.1, 14.6]) {
    const state = await page.evaluate(t => window.__clay3d.seek(t), t);
    samples.push({ time: t, joints: state.joints, projected: state.projected, reaches: state.reaches, shot: state.shot });
    await page.screenshot({ path: path.join(output, `browser-${t.toFixed(2)}.png`) });
  }
  const timeA = await page.evaluate(() => window.__clay3d.seek(6.8));
  const frameA = await page.screenshot();
  await page.evaluate(() => window.__clay3d.seek(14.6));
  const timeB = await page.evaluate(() => window.__clay3d.seek(6.8));
  const frameB = await page.screenshot();
  const digest = buffer => createHash('sha256').update(buffer).digest('hex');
  const unreachable = samples.flatMap(sample => sample.reaches.filter(r => !r.arm || !r.leg || r.armError > 0.01 || r.footError > 0.01).map(r => ({ time: sample.time, ...r })));
  const clipped = samples.flatMap(sample => Object.entries(sample.projected).filter(([_, point]) => Math.abs(point[0]) > 0.97 || Math.abs(point[1]) > 0.97).map(([joint, point]) => ({ time: sample.time, joint, point })));
  const diagnostics = await page.evaluate(() => window.__clay3d.diagnostics());
  const fullMotion = await page.evaluate(() => window.__clay3d.auditMotion());
  const report = { browser: await browser.version(), diagnostics, canvas: [1920, 1080], samples: samples.length, pageErrors: failures, blockedExternalRequests: external, unreachable, clipped, fullMotion, deterministicImage: digest(frameA) === digest(frameB), deterministicJoints: JSON.stringify(timeA.joints) === JSON.stringify(timeB.joints), states: samples };
  report.ok = !failures.length && !external.length && !unreachable.length && !clipped.length && !fullMotion.unreachable.length && !fullMotion.clipped.length && report.deterministicImage && report.deterministicJoints;
  await writeFile(path.join(output, 'browser-qa.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify({ ...report, states: undefined }, null, 2));
  if (!report.ok) process.exitCode = 1;
} finally { await browser?.close(); await new Promise(resolve => server.close(resolve)); }
