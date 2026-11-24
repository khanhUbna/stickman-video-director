import * as THREE from 'three';
import { makeScene } from './scene.mjs';
import { poseAt } from './motion.mjs';

const canvas = document.getElementById('clay-stage');
const root = document.getElementById('clay-room');
const width = Number(root.dataset.width); const height = Number(root.dataset.height);
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, powerPreference: 'low-power' });
renderer.setPixelRatio(1); renderer.setSize(width, height, false);
renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.02;
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFShadowMap;
const stage = makeScene(renderer); let shownTime = -1;
const gl = renderer.getContext(); const pixel = new Uint8Array(4);
function draw(seconds) {
  const pose = poseAt(seconds);
  if (shownTime === pose.t) return;
  stage.update(pose); renderer.render(stage.scene, stage.camera);
  // A GPU fence via readback prevents blank screenshots on software GL.
  gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, pixel); shownTime = pose.t;
}
window.__hf = window.__hf || {}; window.__hf.buildReady = window.__hf.buildReady || {};
const ready = (async () => {
  stage.update(poseAt(0));
  if (renderer.extensions.has('KHR_parallel_shader_compile')) await renderer.compileAsync(stage.scene, stage.camera);
  else renderer.compile(stage.scene, stage.camera);
  draw(0);
})();
window.__hf.buildReady['clay3d'] = ready;
window.addEventListener('hf-seek', event => {
  const work = ready.then(() => draw(event.detail.time));
  event.detail.waitUntil?.(work);
});
window.__clay3d = {
  ready,
  seek: async t => { await ready; draw(t); return JSON.parse(JSON.stringify(stage.debug)); },
  diagnostics: () => ({ renderer: renderer.info.render, webgl: gl.getParameter(gl.VERSION), size: [width, height] }),
  auditMotion: () => {
    const previous = shownTime; const unreachable = []; const clipped = [];
    for (let frame = 0; frame < 450; frame++) {
      stage.update(poseAt(frame / 30));
      for (const reach of stage.debug.reaches) if (reach.armError > 0.01 || reach.footError > 0.01) unreachable.push({ frame, ...reach });
      for (const [joint, point] of Object.entries(stage.debug.projected)) if (Math.abs(point[0]) > 0.97 || Math.abs(point[1]) > 0.97) clipped.push({ frame, joint, point });
    }
    shownTime = -1; draw(previous);
    return { frames: 450, unreachable, clipped };
  },
};
