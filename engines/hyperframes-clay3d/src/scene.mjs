import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { solveTwoBone, rotateY, add, sub, clamp } from './motion.mjs';

const v = p => new THREE.Vector3(...p);
const up = new THREE.Vector3(0, 1, 0);

function clayTexture() {
  const canvas = document.createElement('canvas'); canvas.width = canvas.height = 128;
  const ctx = canvas.getContext('2d'); const pixels = ctx.createImageData(128, 128);
  let seed = 77123;
  for (let i = 0; i < 128 * 128; i++) {
    seed ^= seed << 13; seed ^= seed >>> 17; seed ^= seed << 5;
    const x = i % 128; const y = Math.floor(i / 128);
    const value = 130 + ((seed >>> 0) % 29) + 7 * Math.sin(x / 8 + Math.sin(y / 9));
    pixels.data.set([value, value, value, 255], i * 4);
  }
  ctx.putImageData(pixels, 0, 0);
  const texture = new THREE.CanvasTexture(canvas); texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(2.3, 2.3); return texture;
}

export function makeScene(renderer) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color('#e9dccc');
  const bump = clayTexture();
  const material = (color, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.94, metalness: 0, bumpMap: bump, bumpScale: 0.017, ...extra });
  const mat = {
    skin: material('#e9a67d'), cream: material('#f8e3b4'), vest: material('#2f6556'), pants: material('#354a62'),
    shoe: material('#8b4a37'), hair: material('#747776'), white: material('#fff8eb'), ink: material('#332e2b'),
    ball: material('#ed9b37'), wall: material('#e6d0b5'), floor: material('#b98259'), trim: material('#f2d6a3'),
    sofa: material('#d37c6f'), cushion: material('#e29584'), sage: material('#8faaa0'), leaf: material('#59794f'),
  };
  const sphere = new THREE.SphereGeometry(1, 24, 16);
  function ellipsoid(parent, m, pos, scale) {
    const mesh = new THREE.Mesh(sphere, m); mesh.position.set(...pos); mesh.scale.set(...scale);
    mesh.castShadow = mesh.receiveShadow = true; parent.add(mesh); return mesh;
  }
  function box(parent, m, pos, size, radius = 0.10) {
    const mesh = new THREE.Mesh(new RoundedBoxGeometry(...size, 3, radius), m);
    mesh.position.set(...pos); mesh.castShadow = mesh.receiveShadow = true; parent.add(mesh); return mesh;
  }
  function cylinder(parent, m, pos, radius, height) {
    const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, height, 20), m);
    mesh.position.set(...pos); mesh.castShadow = mesh.receiveShadow = true; parent.add(mesh); return mesh;
  }
  function segment(m, radius) {
    const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius * 0.88, radius, 1, 14), m);
    mesh.castShadow = mesh.receiveShadow = true; scene.add(mesh); return mesh;
  }
  function connect(mesh, from, to) {
    const a = v(from); const b = v(to); const delta = b.clone().sub(a);
    mesh.position.copy(a.add(b).multiplyScalar(0.5)); mesh.scale.y = delta.length();
    mesh.quaternion.setFromUnitVectors(up, delta.normalize());
  }

  // A handmade miniature set. All meshes and textures are original procedural assets.
  box(scene, mat.floor, [0, -0.14, 0], [9.3, 0.28, 4.8], 0.10);
  for (let i = 0; i < 9; i++) box(scene, material(i % 2 ? '#b27c54' : '#c58f63'), [-4.05 + i * 1.02, 0.002, 0], [0.99, 0.018, 4.5], 0.02);
  box(scene, mat.wall, [0, 1.90, -1.85], [9.3, 3.8, 0.18], 0.10);
  box(scene, material('#dbc2a3'), [-4.55, 1.90, -0.30], [0.18, 3.8, 3.0], 0.09);
  box(scene, mat.trim, [0, 0.12, -1.7], [9.0, 0.15, 0.10], 0.025);
  const windowGroup = new THREE.Group(); windowGroup.position.set(-2.5, 2.35, -1.72); scene.add(windowGroup);
  const sky = new THREE.Mesh(new THREE.CircleGeometry(0.75, 64), material('#a9cfd3', { bumpScale: 0 })); windowGroup.add(sky);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.79, 0.08, 12, 64), mat.trim); ring.castShadow = true; windowGroup.add(ring);
  box(windowGroup, mat.trim, [0, 0, 0.03], [0.045, 1.45, 0.06], 0.02);
  box(windowGroup, mat.trim, [0, 0, 0.03], [1.45, 0.045, 0.06], 0.02);
  ellipsoid(windowGroup, material('#f6dfab'), [0.35, 0.35, 0.015], [0.18, 0.18, 0.02]);

  const rug = new THREE.Mesh(new THREE.CircleGeometry(1, 64), material('#ddd0a7'));
  rug.rotation.x = -Math.PI / 2; rug.scale.set(3.65, 1.5, 1); rug.position.set(0.25, 0.028, 0.55); rug.receiveShadow = true; scene.add(rug);
  const sofa = new THREE.Group(); sofa.position.set(2.4, 0, -0.45); scene.add(sofa);
  box(sofa, mat.sofa, [0, 0.29, 0], [2.65, 0.48, 1.30], 0.18);
  box(sofa, mat.cushion, [0, 0.54, 0.05], [2.18, 0.25, 1.12], 0.15);
  box(sofa, mat.sofa, [0, 1.01, -0.59], [2.60, 1.18, 0.30], 0.17);
  box(sofa, mat.cushion, [-1.25, 0.78, 0], [0.30, 0.62, 1.34], 0.14);
  box(sofa, mat.cushion, [1.25, 0.78, 0], [0.30, 0.62, 1.34], 0.14);
  const pillow = box(sofa, mat.sage, [0.72, 1.05, -0.27], [0.50, 0.52, 0.20], 0.13); pillow.rotation.z = -0.16;
  for (const x of [-1.05, 1.05]) for (const z of [-0.4, 0.4]) cylinder(sofa, mat.shoe, [x, 0.12, z], 0.07, 0.24);
  const pot = cylinder(scene, material('#cd8359'), [-3.7, 0.30, -0.8], 0.30, 0.55);
  ellipsoid(scene, material('#765039'), [-3.7, 0.57, -0.8], [0.28, 0.03, 0.28]);
  for (let i = 0; i < 7; i++) {
    const a = i * 2.4; const h = 0.85 + i * 0.13;
    const leaf = ellipsoid(scene, mat.leaf, [-3.7 + Math.sin(a) * 0.22, h, -0.8 + Math.cos(a) * 0.17], [0.13, 0.39, 0.07]);
    leaf.rotation.set(Math.cos(a) * 0.4, a, Math.sin(a) * 0.55);
  }
  cylinder(scene, mat.shoe, [-1.22, 0.42, -1.0], 0.07, 0.84);
  cylinder(scene, mat.trim, [-1.22, 0.88, -1.0], 0.49, 0.10);
  cylinder(scene, mat.sage, [-1.22, 1.14, -1.0], 0.08, 0.45);
  const shade = new THREE.Mesh(new THREE.ConeGeometry(0.28, 0.35, 24, 1, true), material('#f2cc85', { side: THREE.DoubleSide })); shade.position.set(-1.22, 1.47, -1.0); scene.add(shade);
  box(scene, mat.trim, [2.65, 2.55, -1.70], [1.35, 0.96, 0.10], 0.08);
  box(scene, mat.sage, [2.65, 2.55, -1.63], [1.18, 0.80, 0.025], 0.04);
  ellipsoid(scene, material('#f3d9ac'), [2.48, 2.64, -1.60], [0.22, 0.22, 0.02]);

  scene.add(new THREE.HemisphereLight('#fff6e4', '#8d7b68', 2.0));
  const key = new THREE.DirectionalLight('#ffe3bb', 3.2); key.position.set(-3.5, 6.5, 6); key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024); key.shadow.camera.left = -5; key.shadow.camera.right = 5; key.shadow.camera.top = 4; key.shadow.camera.bottom = -4;
  key.shadow.normalBias = 0.025; key.shadow.bias = -0.0002; key.shadow.radius = 3; scene.add(key);
  const rim = new THREE.DirectionalLight('#bddde0', 1.3); rim.position.set(4, 4, -2); scene.add(rim);

  // Public handles for story-specific films; the default demo's drawing is unchanged.
  const environmentObjects = scene.children.filter(object => !object.isLight);
  const characterStart = scene.children.length;
  const torso = new THREE.Group(); scene.add(torso);
  ellipsoid(torso, mat.vest, [0, 0.28, 0], [0.30, 0.37, 0.22]);
  ellipsoid(torso, mat.cream, [0, 0.53, 0.025], [0.27, 0.13, 0.19]);
  box(torso, mat.vest, [-0.12, 0.33, 0.168], [0.19, 0.45, 0.10], 0.04);
  box(torso, mat.vest, [0.12, 0.33, 0.168], [0.19, 0.45, 0.10], 0.04);
  for (const y of [0.18, 0.32, 0.46]) ellipsoid(torso, mat.trim, [0.025, y, 0.24], [0.025, 0.025, 0.014]);
  cylinder(torso, mat.skin, [0, 0.67, 0], 0.10, 0.18);
  const head = new THREE.Group(); head.position.set(0, 0.93, 0.025); torso.add(head);
  ellipsoid(head, mat.skin, [0, 0, 0], [0.34, 0.37, 0.31]);
  for (const x of [-0.34, 0.34]) ellipsoid(head, mat.skin, [x, -0.015, 0.01], [0.072, 0.11, 0.08]);
  ellipsoid(head, mat.skin, [0, -0.025, 0.31], [0.074, 0.084, 0.075]);
  for (let i = 0; i < 10; i++) {
    const a = i / 10 * Math.PI * 2;
    ellipsoid(head, mat.hair, [Math.cos(a) * 0.225, 0.255 + 0.04 * Math.sin(a * 3), Math.sin(a) * 0.18 - 0.04], [0.145, 0.135, 0.15]);
  }
  const eyes = []; const pupils = []; const brows = [];
  for (const x of [-0.13, 0.13]) {
    const eye = new THREE.Group(); eye.position.set(x, 0.055, 0.283); head.add(eye); eyes.push(eye);
    ellipsoid(eye, mat.white, [0, 0, 0], [0.075, 0.095, 0.045]);
    pupils.push(ellipsoid(eye, mat.ink, [0.008, 0, 0.044], [0.031, 0.042, 0.015]));
    const brow = ellipsoid(head, mat.hair, [x, 0.19, 0.265], [0.085, 0.022, 0.025]); brows.push(brow);
  }
  const mouthMaterial = mat.ink.clone();
  const smileMaterial = mat.ink.clone(); smileMaterial.transparent = mouthMaterial.transparent = true;
  const mouth = new THREE.Mesh(new THREE.TubeGeometry(new THREE.QuadraticBezierCurve3(v([-0.075, -0.12, 0.29]), v([0, -0.135, 0.32]), v([0.075, -0.12, 0.29])), 12, 0.013, 6, false), mouthMaterial); head.add(mouth);
  const smile = new THREE.Mesh(new THREE.TubeGeometry(new THREE.QuadraticBezierCurve3(v([-0.095, -0.10, 0.29]), v([0, -0.21, 0.33]), v([0.095, -0.10, 0.29])), 16, 0.014, 6, false), smileMaterial); head.add(smile);
  const hips = ellipsoid(scene, mat.pants, [0, 0, 0], [0.265, 0.20, 0.20]);
  const limbs = {};
  for (const side of ['left', 'right']) {
    limbs[side] = {
      thigh: segment(mat.pants, 0.105), shin: segment(mat.pants, 0.088), knee: ellipsoid(scene, mat.pants, [0, 0, 0], [0.10, 0.10, 0.10]),
      shoe: ellipsoid(scene, mat.shoe, [0, 0, 0], [0.14, 0.12, 0.23]),
      upperArm: segment(mat.cream, 0.095), forearm: segment(mat.skin, 0.075), elbow: ellipsoid(scene, mat.skin, [0, 0, 0], [0.078, 0.078, 0.078]),
      hand: ellipsoid(scene, mat.skin, [0, 0, 0], [0.095, 0.105, 0.075]),
    };
  }
  const ball = ellipsoid(scene, mat.ball, [0, 0, 0], [0.15, 0.16, 0.15]);
  const seam = new THREE.Mesh(new THREE.TorusGeometry(0.15, 0.009, 5, 24), material('#c5772c')); ball.add(seam); seam.scale.setScalar(1 / 0.15); seam.rotation.x = 0.25;

  const camera = new THREE.OrthographicCamera(-4.8, 4.8, 2.7, -2.7, 0.1, 100);
  const debug = {};
  function update(pose) {
    const { actor, ball: prop } = pose;
    torso.position.set(...actor.position); torso.rotation.set(actor.lean, actor.yaw, 0, 'YXZ'); torso.updateMatrixWorld(true);
    hips.position.set(...actor.position); hips.rotation.y = actor.yaw;
    const joints = {}; const reaches = [];
    for (const [side, sign] of [['left', -1], ['right', 1]]) {
      const limb = limbs[side]; const ankle = actor[side].position;
      const hip = add(actor.position, rotateY([sign * 0.165, -0.08, 0], actor.yaw));
      const leg = solveTwoBone(hip, ankle, rotateY([0, 0, 1], actor.yaw), 0.53, 0.51);
      connect(limb.thigh, hip, leg.joint); connect(limb.shin, leg.joint, leg.end); limb.knee.position.set(...leg.joint);
      limb.shoe.position.set(...ankle); limb.shoe.rotation.y = actor.shoeYaw;
      const shoulder = torso.localToWorld(new THREE.Vector3(sign * 0.26, 0.52, 0)).toArray();
      const target = pose[`${side}Hand`];
      const arm = solveTwoBone(shoulder, target, rotateY([sign, -0.25, -0.15], actor.yaw), 0.46, 0.44);
      connect(limb.upperArm, shoulder, arm.joint); connect(limb.forearm, arm.joint, arm.end);
      limb.elbow.position.set(...arm.joint); limb.hand.position.set(...arm.end);
      joints[`${side}Shoulder`] = shoulder; joints[`${side}Elbow`] = arm.joint; joints[`${side}Hand`] = arm.end;
      joints[`${side}Hip`] = hip; joints[`${side}Knee`] = leg.joint; joints[`${side}Ankle`] = ankle;
      reaches.push({ side, arm: arm.reachable, leg: leg.reachable, armError: v(arm.end).distanceTo(v(target)), footError: v(leg.end).distanceTo(v(ankle)) });
    }
    ball.position.set(...prop.position); ball.rotation.set(0.3 + pose.t * 1.2, pose.t * 0.7, 0.15);
    head.rotation.x = clamp(-(prop.position[1] - (actor.position[1] + 0.93)) * 0.15, -0.15, 0.16) - actor.lean * 0.45;
    head.rotation.z = Math.sin(pose.t * 4) * 0.025 * (actor.left.moving || actor.right.moving ? 1 : 0);
    eyes.forEach(eye => { eye.scale.y = 1 - 0.92 * pose.blink; });
    brows[0].rotation.z = -0.06 + 0.13 * (pose.t > 6.8 && pose.t < 8.2 ? 1 : 0); brows[1].rotation.z = 0.06;
    mouthMaterial.opacity = 1 - pose.smile; smileMaterial.opacity = pose.smile;
    if (pose.shot === 'wide') {
      camera.left = -4.8; camera.right = 4.8; camera.top = 2.7; camera.bottom = -2.7;
      camera.position.set(6.3, 4.4, 9.4); camera.lookAt(0, 1.05, 0);
    } else {
      const halfWidth = pose.shot === 'toss' ? 3.0 : 2.75;
      camera.left = -halfWidth; camera.right = halfWidth; camera.top = halfWidth * 9 / 16; camera.bottom = -halfWidth * 9 / 16;
      camera.position.set(pose.shot === 'pickup' ? 3.0 : 2.2, 3.0, 6.2); camera.lookAt(0.2, pose.shot === 'toss' ? 1.45 : 1.30, 0.65);
    }
    camera.updateProjectionMatrix(); camera.updateMatrixWorld(true); scene.updateMatrixWorld(true);
    joints.head = head.localToWorld(new THREE.Vector3(0, 0.37, 0)).toArray(); joints.ball = prop.position;
    debug.joints = joints; debug.reaches = reaches; debug.shot = pose.shot; debug.pose = pose;
    debug.projected = Object.fromEntries(Object.entries(joints).map(([key, point]) => [key, v(point).project(camera).toArray()]));
  }
  return {
    scene, camera, update, debug,
    environmentObjects,
    actorObjects: scene.children.slice(characterStart),
    materials: mat,
    helpers: { material, ellipsoid, box, cylinder },
    objects: { torso, head, hips, limbs, ball, sofa, eyes, pupils, brows, mouth, smile },
  };
}
