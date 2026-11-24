import { build } from 'esbuild';
import { mkdir, copyFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { engineRoot } from './hf.mjs';
import path from 'node:path';

await mkdir(path.join(engineRoot, 'assets/vendor'), { recursive: true });
// Keep the upstream library separate: its unused clocks/UUID helpers are not composition logic.
// The authored module remains readable and fully checked by HyperFrames' script linter.
await build({ stdin: { contents: "export * from 'three';", resolveDir: engineRoot }, bundle: true, format: 'esm', target: 'chrome140', outfile: path.join(engineRoot, 'assets/vendor/three.min.js'), minify: true, legalComments: 'linked' });
await copyFile(path.join(engineRoot, 'node_modules/three/LICENSE'), path.join(engineRoot, 'assets/vendor/LICENSE-three.txt'));
await build({ entryPoints: [path.join(engineRoot, 'src/main.mjs')], bundle: true, plugins: [{ name: 'local-three-library', setup(build) { build.onResolve({ filter: /^three$/ }, () => ({ path: './vendor/three.min.js', external: true })); } }], format: 'esm', target: 'chrome140', outfile: path.join(engineRoot, 'assets/clay-scene.js'), minify: false, legalComments: 'linked' });
const sound = spawnSync('python3', [path.join(engineRoot, 'scripts/make_sound.py')], { cwd: engineRoot, stdio: 'inherit' });
if (sound.status !== 0) throw new Error('Original local sound generation failed');
console.log('Built local Three.js composition and original procedural sound. No external media requests.');
