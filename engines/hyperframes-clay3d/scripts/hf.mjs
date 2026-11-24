#!/usr/bin/env node
// Repository-specific local-only guard. No cloud, HeyGen media, auth or billing commands.
import { spawn } from 'node:child_process';
import { readFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

export const engineRoot = path.resolve(fileURLToPath(new URL('../', import.meta.url)));
export const allowedCommands = new Set([
  '--version', '--help', 'doctor', 'browser', 'lint', 'check', 'snapshot',
  'render', 'preview', 'info', 'timeline', 'compositions', 'keyframes', 'catalog',
]);

export function validateArgs(args) {
  if (!allowedCommands.has(args[0])) {
    throw new Error(`Local-only policy: HyperFrames command '${args[0] ?? ''}' is disabled. No paid services or accounts are enabled.`);
  }
  if (args.some(arg => /^(?:cloud|cloudrun|lambda|auth|billing|usage|tts|media-use|share|publish|events|feedback)$/.test(arg))) {
    throw new Error('Local-only policy: remote service commands are disabled.');
  }
}

export function localEnvironment(extra = {}) {
  return {
    ...process.env,
    ...extra,
    HYPERFRAMES_NO_TELEMETRY: '1',
    DO_NOT_TRACK: '1',
    HYPERFRAMES_NO_UPDATE_CHECK: '1',
    HYPERFRAMES_SKIP_SKILLS: '1',
    HYPERFRAMES_CONFIG_DIR: path.join(engineRoot, '.cache', 'hyperframes'),
    HYPERFRAMES_CACHE_DIR: path.join(engineRoot, '.cache', 'hyperframes-cache'),
    HYPERFRAMES_BROWSER_PATH: process.env.HYPERFRAMES_BROWSER_PATH || '/usr/bin/chromium',
    HYPERFRAMES_FFMPEG_PATH: process.env.HYPERFRAMES_FFMPEG_PATH || '/usr/bin/ffmpeg',
    HYPERFRAMES_FFPROBE_PATH: process.env.HYPERFRAMES_FFPROBE_PATH || '/usr/bin/ffprobe',
    npm_config_cache: path.join(engineRoot, '.cache', 'npm'),
  };
}

export function runLocal(args, options = {}) {
  validateArgs(args);
  const pkg = JSON.parse(readFileSync(path.join(engineRoot, 'node_modules/hyperframes/package.json'), 'utf8'));
  if (pkg.version !== '0.9.88' || pkg.license !== 'Apache-2.0') {
    throw new Error('Expected the pinned Apache-2.0 hyperframes@0.9.88. Run npm ci in this engine directory.');
  }
  mkdirSync(path.join(engineRoot, '.cache'), { recursive: true });
  const child = spawn(process.execPath, [path.join(engineRoot, 'node_modules/hyperframes/bin/hyperframes.mjs'), ...args], {
    cwd: engineRoot,
    stdio: 'inherit',
    ...options,
    env: localEnvironment(options.env),
  });
  return new Promise((resolve, reject) => {
    child.on('error', reject);
    child.on('exit', (code, signal) => signal ? reject(new Error(`HyperFrames terminated by ${signal}`)) : resolve(code ?? 1));
  });
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { process.exitCode = await runLocal(process.argv.slice(2)); }
  catch (error) { console.error(error.message); process.exitCode = 1; }
}
