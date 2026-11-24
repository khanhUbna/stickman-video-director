import { mkdir, writeFile } from 'node:fs/promises';
import { engineRoot, runLocal } from './hf.mjs';
import path from 'node:path';

const folder = path.join(engineRoot, 'output'); await mkdir(folder, { recursive: true });
const start = Date.now();
const args = ['render', '--quality', 'delivery', '--fps', '30', '--workers', '1', '--no-browser-gpu', '--strict', '--output', path.join(folder, 'clay-animation-15s.mp4')];
const code = await runLocal(args);
await writeFile(path.join(folder, 'render-execution.json'), JSON.stringify({ command: ['hyperframes', ...args], exitCode: code, wallSeconds: (Date.now() - start) / 1000, localOnly: true, paidApiCalls: 0 }, null, 2) + '\n');
process.exitCode = code;
