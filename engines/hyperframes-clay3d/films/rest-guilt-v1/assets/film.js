// engines/hyperframes-clay3d/films/rest-guilt-v1/src/main.mjs
import * as THREE3 from "./vendor/three.min.js";

// engines/hyperframes-clay3d/src/scene.mjs
import * as THREE from "./vendor/three.min.js";

// engines/hyperframes-clay3d/node_modules/three/examples/jsm/geometries/RoundedBoxGeometry.js
import {
  BoxGeometry,
  Vector3
} from "./vendor/three.min.js";
var _tempNormal = new Vector3();
function getUv(faceDirVector, normal, uvAxis, projectionAxis, radius, sideLength) {
  const totArcLength = 2 * Math.PI * radius / 4;
  const centerLength = Math.max(sideLength - 2 * radius, 0);
  const halfArc = Math.PI / 4;
  _tempNormal.copy(normal);
  _tempNormal[projectionAxis] = 0;
  _tempNormal.normalize();
  const arcUvRatio = 0.5 * totArcLength / (totArcLength + centerLength);
  const arcAngleRatio = 1 - _tempNormal.angleTo(faceDirVector) / halfArc;
  if (Math.sign(_tempNormal[uvAxis]) === 1) {
    return arcAngleRatio * arcUvRatio;
  } else {
    const lenUv = centerLength / (totArcLength + centerLength);
    return lenUv + arcUvRatio + arcUvRatio * (1 - arcAngleRatio);
  }
}
var RoundedBoxGeometry = class _RoundedBoxGeometry extends BoxGeometry {
  /**
   * Constructs a new rounded box geometry.
   *
   * @param {number} [width=1] - The width. That is, the length of the edges parallel to the X axis.
   * @param {number} [height=1] - The height. That is, the length of the edges parallel to the Y axis.
   * @param {number} [depth=1] - The depth. That is, the length of the edges parallel to the Z axis.
   * @param {number} [segments=2] - Number of segments that form the rounded corners.
   * @param {number} [radius=0.1] - The radius of the rounded corners.
   */
  constructor(width = 1, height = 1, depth = 1, segments = 2, radius = 0.1) {
    const totalSegments = segments * 2 + 1;
    radius = Math.min(width / 2, height / 2, depth / 2, radius);
    super(1, 1, 1, totalSegments, totalSegments, totalSegments);
    this.type = "RoundedBoxGeometry";
    this.parameters = {
      width,
      height,
      depth,
      segments,
      radius
    };
    if (totalSegments === 1) return;
    const geometry2 = this.toNonIndexed();
    this.index = null;
    this.attributes.position = geometry2.attributes.position;
    this.attributes.normal = geometry2.attributes.normal;
    this.attributes.uv = geometry2.attributes.uv;
    const position = new Vector3();
    const normal = new Vector3();
    const box = new Vector3(width, height, depth).divideScalar(2).subScalar(radius);
    const positions = this.attributes.position.array;
    const normals = this.attributes.normal.array;
    const uvs = this.attributes.uv.array;
    const faceTris = positions.length / 6;
    const faceDirVector = new Vector3();
    const halfSegmentSize = 0.5 / totalSegments;
    for (let i = 0, j = 0; i < positions.length; i += 3, j += 2) {
      position.fromArray(positions, i);
      normal.copy(position);
      normal.x -= Math.sign(normal.x) * halfSegmentSize;
      normal.y -= Math.sign(normal.y) * halfSegmentSize;
      normal.z -= Math.sign(normal.z) * halfSegmentSize;
      normal.normalize();
      positions[i + 0] = box.x * Math.sign(position.x) + normal.x * radius;
      positions[i + 1] = box.y * Math.sign(position.y) + normal.y * radius;
      positions[i + 2] = box.z * Math.sign(position.z) + normal.z * radius;
      normals[i + 0] = normal.x;
      normals[i + 1] = normal.y;
      normals[i + 2] = normal.z;
      const side = Math.floor(i / faceTris);
      switch (side) {
        case 0:
          faceDirVector.set(1, 0, 0);
          uvs[j + 0] = getUv(faceDirVector, normal, "z", "y", radius, depth);
          uvs[j + 1] = 1 - getUv(faceDirVector, normal, "y", "z", radius, height);
          break;
        case 1:
          faceDirVector.set(-1, 0, 0);
          uvs[j + 0] = 1 - getUv(faceDirVector, normal, "z", "y", radius, depth);
          uvs[j + 1] = 1 - getUv(faceDirVector, normal, "y", "z", radius, height);
          break;
        case 2:
          faceDirVector.set(0, 1, 0);
          uvs[j + 0] = 1 - getUv(faceDirVector, normal, "x", "z", radius, width);
          uvs[j + 1] = getUv(faceDirVector, normal, "z", "x", radius, depth);
          break;
        case 3:
          faceDirVector.set(0, -1, 0);
          uvs[j + 0] = 1 - getUv(faceDirVector, normal, "x", "z", radius, width);
          uvs[j + 1] = 1 - getUv(faceDirVector, normal, "z", "x", radius, depth);
          break;
        case 4:
          faceDirVector.set(0, 0, 1);
          uvs[j + 0] = 1 - getUv(faceDirVector, normal, "x", "y", radius, width);
          uvs[j + 1] = 1 - getUv(faceDirVector, normal, "y", "x", radius, height);
          break;
        case 5:
          faceDirVector.set(0, 0, -1);
          uvs[j + 0] = getUv(faceDirVector, normal, "x", "y", radius, width);
          uvs[j + 1] = 1 - getUv(faceDirVector, normal, "y", "x", radius, height);
          break;
      }
    }
  }
  /**
   * Factory method for creating an instance of this class from the given
   * JSON object.
   *
   * @param {Object} data - A JSON object representing the serialized geometry.
   * @returns {RoundedBoxGeometry} A new instance.
   */
  static fromJSON(data) {
    return new _RoundedBoxGeometry(
      data.width,
      data.height,
      data.depth,
      data.segments,
      data.radius
    );
  }
};

// engines/hyperframes-clay3d/src/motion.mjs
var lerp = (a, b, t) => a + (b - a) * t;
var clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
var ease = (t, a, b) => {
  const u = clamp((t - a) / (b - a));
  return u * u * (3 - 2 * u);
};
var mix = (a, b, u) => a.map((x, i) => lerp(x, b[i], u));
var add = (a, b) => a.map((x, i) => x + b[i]);
var sub = (a, b) => a.map((x, i) => x - b[i]);
var mul = (a, s) => a.map((x) => x * s);
var dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
var length = (a) => Math.hypot(...a);
var normalized = (a) => mul(a, 1 / Math.max(length(a), 1e-9));
var rotateY = ([x, y, z], a) => [x * Math.cos(a) + z * Math.sin(a), y, -x * Math.sin(a) + z * Math.cos(a)];
var localPoint = (root, xyz) => add(root.position, rotateY(xyz, root.yaw));
function solveTwoBone(origin, target, pole, upper, lower) {
  const delta = sub(target, origin);
  const raw = length(delta);
  const d = clamp(raw, Math.abs(upper - lower) + 1e-6, upper + lower - 1e-6);
  const direction = normalized(delta);
  const perpendicular = sub(pole, mul(direction, dot(pole, direction)));
  const side = normalized(length(perpendicular) < 1e-6 ? [0, 0, 1] : perpendicular);
  const along = (upper * upper - lower * lower + d * d) / (2 * d);
  const height = Math.sqrt(Math.max(0, upper * upper - along * along));
  return { joint: add(add(origin, mul(direction, along)), mul(side, height)), end: add(origin, mul(direction, d)), requestedDistance: raw, reachable: raw < upper + lower };
}
var steps = {
  left: [[0.6, 1.1, -2.05], [1.7, 2.2, -1], [2.8, 3.3, 0.05], [10.6, 11.1, 0.8], [11.7, 12.2, 1.92], [12.8, 13.1, 2.15]],
  right: [[1.15, 1.65, -1.55], [2.25, 2.75, -0.45], [3.35, 3.85, 0.2], [11.15, 11.65, 1.35], [12.25, 12.75, 2.45]]
};
function footAt(t, side) {
  let x = -2.7;
  for (const [start, end, next] of steps[side]) {
    if (t < start) break;
    if (t < end) {
      const u = (t - start) / (end - start);
      return { position: [lerp(x, next, ease(t, start, end)), 0.12 + Math.sin(Math.PI * u) * 0.19, side === "left" ? 0.89 : 0.53], moving: true, phase: u };
    }
    x = next;
  }
  return { position: [x, 0.12, side === "left" ? 0.89 : 0.53], moving: false, phase: 0 };
}
function actorAt(t) {
  const left = footAt(t, "left");
  const right = footAt(t, "right");
  const squat = ease(t, 4.25, 5.65) * (1 - ease(t, 5.65, 6.65));
  const tossDip = Math.sin(Math.PI * clamp((t - 8.15) / 0.5)) * 0.07;
  const catchDip = Math.sin(Math.PI * clamp((t - 9.76) / 0.62)) * 0.09;
  const sitting = ease(t, 13.1, 14.25);
  const walkBob = (left.moving ? Math.sin(left.phase * Math.PI) : 0) + (right.moving ? Math.sin(right.phase * Math.PI) : 0);
  const strideDrop = 0.13 * (Math.abs(left.position[0] - right.position[0]) / 1.15) ** 2;
  let yaw = Math.PI / 2 * (1 - ease(t, 3.85, 4.25));
  yaw += Math.PI / 2 * ease(t, 10.2, 10.6) * (1 - ease(t, 12.85, 13.4));
  return {
    position: [(left.position[0] + right.position[0]) / 2, 1.18 - 0.76 * squat - tossDip - catchDip - 0.45 * sitting - strideDrop + 0.012 * walkBob, 0.71 - 0.62 * sitting],
    yaw,
    lean: 0.43 * squat - 0.12 * sitting + 0.04 * Math.sin(t * 4) * (left.moving || right.moving ? 1 : 0),
    squat,
    sitting,
    left,
    right,
    shoeYaw: Math.PI / 2 * (1 - ease(t, 12.85, 13.45))
  };
}

// engines/hyperframes-clay3d/src/scene.mjs
var v = (p) => new THREE.Vector3(...p);
var up = new THREE.Vector3(0, 1, 0);
function clayTexture() {
  const canvas2 = document.createElement("canvas");
  canvas2.width = canvas2.height = 128;
  const ctx = canvas2.getContext("2d");
  const pixels = ctx.createImageData(128, 128);
  let seed = 77123;
  for (let i = 0; i < 128 * 128; i++) {
    seed ^= seed << 13;
    seed ^= seed >>> 17;
    seed ^= seed << 5;
    const x = i % 128;
    const y = Math.floor(i / 128);
    const value = 130 + (seed >>> 0) % 29 + 7 * Math.sin(x / 8 + Math.sin(y / 9));
    pixels.data.set([value, value, value, 255], i * 4);
  }
  ctx.putImageData(pixels, 0, 0);
  const texture = new THREE.CanvasTexture(canvas2);
  texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(2.3, 2.3);
  return texture;
}
function makeScene(renderer2) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color("#e9dccc");
  const bump = clayTexture();
  const material = (color, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.94, metalness: 0, bumpMap: bump, bumpScale: 0.017, ...extra });
  const mat = {
    skin: material("#e9a67d"),
    cream: material("#f8e3b4"),
    vest: material("#2f6556"),
    pants: material("#354a62"),
    shoe: material("#8b4a37"),
    hair: material("#747776"),
    white: material("#fff8eb"),
    ink: material("#332e2b"),
    ball: material("#ed9b37"),
    wall: material("#e6d0b5"),
    floor: material("#b98259"),
    trim: material("#f2d6a3"),
    sofa: material("#d37c6f"),
    cushion: material("#e29584"),
    sage: material("#8faaa0"),
    leaf: material("#59794f")
  };
  const sphere = new THREE.SphereGeometry(1, 24, 16);
  function ellipsoid(parent, m, pos, scale) {
    const mesh = new THREE.Mesh(sphere, m);
    mesh.position.set(...pos);
    mesh.scale.set(...scale);
    mesh.castShadow = mesh.receiveShadow = true;
    parent.add(mesh);
    return mesh;
  }
  function box(parent, m, pos, size, radius = 0.1) {
    const mesh = new THREE.Mesh(new RoundedBoxGeometry(...size, 3, radius), m);
    mesh.position.set(...pos);
    mesh.castShadow = mesh.receiveShadow = true;
    parent.add(mesh);
    return mesh;
  }
  function cylinder(parent, m, pos, radius, height) {
    const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, height, 20), m);
    mesh.position.set(...pos);
    mesh.castShadow = mesh.receiveShadow = true;
    parent.add(mesh);
    return mesh;
  }
  function segment(m, radius) {
    const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius * 0.88, radius, 1, 14), m);
    mesh.castShadow = mesh.receiveShadow = true;
    scene.add(mesh);
    return mesh;
  }
  function connect(mesh, from, to) {
    const a = v(from);
    const b = v(to);
    const delta = b.clone().sub(a);
    mesh.position.copy(a.add(b).multiplyScalar(0.5));
    mesh.scale.y = delta.length();
    mesh.quaternion.setFromUnitVectors(up, delta.normalize());
  }
  box(scene, mat.floor, [0, -0.14, 0], [9.3, 0.28, 4.8], 0.1);
  for (let i = 0; i < 9; i++) box(scene, material(i % 2 ? "#b27c54" : "#c58f63"), [-4.05 + i * 1.02, 2e-3, 0], [0.99, 0.018, 4.5], 0.02);
  box(scene, mat.wall, [0, 1.9, -1.85], [9.3, 3.8, 0.18], 0.1);
  box(scene, material("#dbc2a3"), [-4.55, 1.9, -0.3], [0.18, 3.8, 3], 0.09);
  box(scene, mat.trim, [0, 0.12, -1.7], [9, 0.15, 0.1], 0.025);
  const windowGroup = new THREE.Group();
  windowGroup.position.set(-2.5, 2.35, -1.72);
  scene.add(windowGroup);
  const sky = new THREE.Mesh(new THREE.CircleGeometry(0.75, 64), material("#a9cfd3", { bumpScale: 0 }));
  windowGroup.add(sky);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.79, 0.08, 12, 64), mat.trim);
  ring.castShadow = true;
  windowGroup.add(ring);
  box(windowGroup, mat.trim, [0, 0, 0.03], [0.045, 1.45, 0.06], 0.02);
  box(windowGroup, mat.trim, [0, 0, 0.03], [1.45, 0.045, 0.06], 0.02);
  ellipsoid(windowGroup, material("#f6dfab"), [0.35, 0.35, 0.015], [0.18, 0.18, 0.02]);
  const rug = new THREE.Mesh(new THREE.CircleGeometry(1, 64), material("#ddd0a7"));
  rug.rotation.x = -Math.PI / 2;
  rug.scale.set(3.65, 1.5, 1);
  rug.position.set(0.25, 0.028, 0.55);
  rug.receiveShadow = true;
  scene.add(rug);
  const sofa = new THREE.Group();
  sofa.position.set(2.4, 0, -0.45);
  scene.add(sofa);
  box(sofa, mat.sofa, [0, 0.29, 0], [2.65, 0.48, 1.3], 0.18);
  box(sofa, mat.cushion, [0, 0.54, 0.05], [2.18, 0.25, 1.12], 0.15);
  box(sofa, mat.sofa, [0, 1.01, -0.59], [2.6, 1.18, 0.3], 0.17);
  box(sofa, mat.cushion, [-1.25, 0.78, 0], [0.3, 0.62, 1.34], 0.14);
  box(sofa, mat.cushion, [1.25, 0.78, 0], [0.3, 0.62, 1.34], 0.14);
  const pillow = box(sofa, mat.sage, [0.72, 1.05, -0.27], [0.5, 0.52, 0.2], 0.13);
  pillow.rotation.z = -0.16;
  for (const x of [-1.05, 1.05]) for (const z of [-0.4, 0.4]) cylinder(sofa, mat.shoe, [x, 0.12, z], 0.07, 0.24);
  const pot = cylinder(scene, material("#cd8359"), [-3.7, 0.3, -0.8], 0.3, 0.55);
  ellipsoid(scene, material("#765039"), [-3.7, 0.57, -0.8], [0.28, 0.03, 0.28]);
  for (let i = 0; i < 7; i++) {
    const a = i * 2.4;
    const h = 0.85 + i * 0.13;
    const leaf = ellipsoid(scene, mat.leaf, [-3.7 + Math.sin(a) * 0.22, h, -0.8 + Math.cos(a) * 0.17], [0.13, 0.39, 0.07]);
    leaf.rotation.set(Math.cos(a) * 0.4, a, Math.sin(a) * 0.55);
  }
  cylinder(scene, mat.shoe, [-1.22, 0.42, -1], 0.07, 0.84);
  cylinder(scene, mat.trim, [-1.22, 0.88, -1], 0.49, 0.1);
  cylinder(scene, mat.sage, [-1.22, 1.14, -1], 0.08, 0.45);
  const shade = new THREE.Mesh(new THREE.ConeGeometry(0.28, 0.35, 24, 1, true), material("#f2cc85", { side: THREE.DoubleSide }));
  shade.position.set(-1.22, 1.47, -1);
  scene.add(shade);
  box(scene, mat.trim, [2.65, 2.55, -1.7], [1.35, 0.96, 0.1], 0.08);
  box(scene, mat.sage, [2.65, 2.55, -1.63], [1.18, 0.8, 0.025], 0.04);
  ellipsoid(scene, material("#f3d9ac"), [2.48, 2.64, -1.6], [0.22, 0.22, 0.02]);
  scene.add(new THREE.HemisphereLight("#fff6e4", "#8d7b68", 2));
  const key = new THREE.DirectionalLight("#ffe3bb", 3.2);
  key.position.set(-3.5, 6.5, 6);
  key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  key.shadow.camera.left = -5;
  key.shadow.camera.right = 5;
  key.shadow.camera.top = 4;
  key.shadow.camera.bottom = -4;
  key.shadow.normalBias = 0.025;
  key.shadow.bias = -2e-4;
  key.shadow.radius = 3;
  scene.add(key);
  const rim = new THREE.DirectionalLight("#bddde0", 1.3);
  rim.position.set(4, 4, -2);
  scene.add(rim);
  const environmentObjects = scene.children.filter((object) => !object.isLight);
  const characterStart = scene.children.length;
  const torso = new THREE.Group();
  scene.add(torso);
  ellipsoid(torso, mat.vest, [0, 0.28, 0], [0.3, 0.37, 0.22]);
  ellipsoid(torso, mat.cream, [0, 0.53, 0.025], [0.27, 0.13, 0.19]);
  box(torso, mat.vest, [-0.12, 0.33, 0.168], [0.19, 0.45, 0.1], 0.04);
  box(torso, mat.vest, [0.12, 0.33, 0.168], [0.19, 0.45, 0.1], 0.04);
  for (const y of [0.18, 0.32, 0.46]) ellipsoid(torso, mat.trim, [0.025, y, 0.24], [0.025, 0.025, 0.014]);
  cylinder(torso, mat.skin, [0, 0.67, 0], 0.1, 0.18);
  const head = new THREE.Group();
  head.position.set(0, 0.93, 0.025);
  torso.add(head);
  ellipsoid(head, mat.skin, [0, 0, 0], [0.34, 0.37, 0.31]);
  for (const x of [-0.34, 0.34]) ellipsoid(head, mat.skin, [x, -0.015, 0.01], [0.072, 0.11, 0.08]);
  ellipsoid(head, mat.skin, [0, -0.025, 0.31], [0.074, 0.084, 0.075]);
  for (let i = 0; i < 10; i++) {
    const a = i / 10 * Math.PI * 2;
    ellipsoid(head, mat.hair, [Math.cos(a) * 0.225, 0.255 + 0.04 * Math.sin(a * 3), Math.sin(a) * 0.18 - 0.04], [0.145, 0.135, 0.15]);
  }
  const eyes = [];
  const pupils = [];
  const brows = [];
  for (const x of [-0.13, 0.13]) {
    const eye = new THREE.Group();
    eye.position.set(x, 0.055, 0.283);
    head.add(eye);
    eyes.push(eye);
    ellipsoid(eye, mat.white, [0, 0, 0], [0.075, 0.095, 0.045]);
    pupils.push(ellipsoid(eye, mat.ink, [8e-3, 0, 0.044], [0.031, 0.042, 0.015]));
    const brow = ellipsoid(head, mat.hair, [x, 0.19, 0.265], [0.085, 0.022, 0.025]);
    brows.push(brow);
  }
  const mouthMaterial = mat.ink.clone();
  const smileMaterial = mat.ink.clone();
  smileMaterial.transparent = mouthMaterial.transparent = true;
  const mouth = new THREE.Mesh(new THREE.TubeGeometry(new THREE.QuadraticBezierCurve3(v([-0.075, -0.12, 0.29]), v([0, -0.135, 0.32]), v([0.075, -0.12, 0.29])), 12, 0.013, 6, false), mouthMaterial);
  head.add(mouth);
  const smile = new THREE.Mesh(new THREE.TubeGeometry(new THREE.QuadraticBezierCurve3(v([-0.095, -0.1, 0.29]), v([0, -0.21, 0.33]), v([0.095, -0.1, 0.29])), 16, 0.014, 6, false), smileMaterial);
  head.add(smile);
  const hips = ellipsoid(scene, mat.pants, [0, 0, 0], [0.265, 0.2, 0.2]);
  const limbs = {};
  for (const side of ["left", "right"]) {
    limbs[side] = {
      thigh: segment(mat.pants, 0.105),
      shin: segment(mat.pants, 0.088),
      knee: ellipsoid(scene, mat.pants, [0, 0, 0], [0.1, 0.1, 0.1]),
      shoe: ellipsoid(scene, mat.shoe, [0, 0, 0], [0.14, 0.12, 0.23]),
      upperArm: segment(mat.cream, 0.095),
      forearm: segment(mat.skin, 0.075),
      elbow: ellipsoid(scene, mat.skin, [0, 0, 0], [0.078, 0.078, 0.078]),
      hand: ellipsoid(scene, mat.skin, [0, 0, 0], [0.095, 0.105, 0.075])
    };
  }
  const ball = ellipsoid(scene, mat.ball, [0, 0, 0], [0.15, 0.16, 0.15]);
  const seam = new THREE.Mesh(new THREE.TorusGeometry(0.15, 9e-3, 5, 24), material("#c5772c"));
  ball.add(seam);
  seam.scale.setScalar(1 / 0.15);
  seam.rotation.x = 0.25;
  const camera = new THREE.OrthographicCamera(-4.8, 4.8, 2.7, -2.7, 0.1, 100);
  const debug2 = {};
  function update(pose2) {
    const { actor, ball: prop } = pose2;
    torso.position.set(...actor.position);
    torso.rotation.set(actor.lean, actor.yaw, 0, "YXZ");
    torso.updateMatrixWorld(true);
    hips.position.set(...actor.position);
    hips.rotation.y = actor.yaw;
    const joints = {};
    const reaches = [];
    for (const [side, sign] of [["left", -1], ["right", 1]]) {
      const limb = limbs[side];
      const ankle = actor[side].position;
      const hip = add(actor.position, rotateY([sign * 0.165, -0.08, 0], actor.yaw));
      const leg = solveTwoBone(hip, ankle, rotateY([0, 0, 1], actor.yaw), 0.53, 0.51);
      connect(limb.thigh, hip, leg.joint);
      connect(limb.shin, leg.joint, leg.end);
      limb.knee.position.set(...leg.joint);
      limb.shoe.position.set(...ankle);
      limb.shoe.rotation.y = actor.shoeYaw;
      const shoulder = torso.localToWorld(new THREE.Vector3(sign * 0.26, 0.52, 0)).toArray();
      const target = pose2[`${side}Hand`];
      const arm = solveTwoBone(shoulder, target, rotateY([sign, -0.25, -0.15], actor.yaw), 0.46, 0.44);
      connect(limb.upperArm, shoulder, arm.joint);
      connect(limb.forearm, arm.joint, arm.end);
      limb.elbow.position.set(...arm.joint);
      limb.hand.position.set(...arm.end);
      joints[`${side}Shoulder`] = shoulder;
      joints[`${side}Elbow`] = arm.joint;
      joints[`${side}Hand`] = arm.end;
      joints[`${side}Hip`] = hip;
      joints[`${side}Knee`] = leg.joint;
      joints[`${side}Ankle`] = ankle;
      reaches.push({ side, arm: arm.reachable, leg: leg.reachable, armError: v(arm.end).distanceTo(v(target)), footError: v(leg.end).distanceTo(v(ankle)) });
    }
    ball.position.set(...prop.position);
    ball.rotation.set(0.3 + pose2.t * 1.2, pose2.t * 0.7, 0.15);
    head.rotation.x = clamp(-(prop.position[1] - (actor.position[1] + 0.93)) * 0.15, -0.15, 0.16) - actor.lean * 0.45;
    head.rotation.z = Math.sin(pose2.t * 4) * 0.025 * (actor.left.moving || actor.right.moving ? 1 : 0);
    eyes.forEach((eye) => {
      eye.scale.y = 1 - 0.92 * pose2.blink;
    });
    brows[0].rotation.z = -0.06 + 0.13 * (pose2.t > 6.8 && pose2.t < 8.2 ? 1 : 0);
    brows[1].rotation.z = 0.06;
    mouthMaterial.opacity = 1 - pose2.smile;
    smileMaterial.opacity = pose2.smile;
    if (pose2.shot === "wide") {
      camera.left = -4.8;
      camera.right = 4.8;
      camera.top = 2.7;
      camera.bottom = -2.7;
      camera.position.set(6.3, 4.4, 9.4);
      camera.lookAt(0, 1.05, 0);
    } else {
      const halfWidth = pose2.shot === "toss" ? 3 : 2.75;
      camera.left = -halfWidth;
      camera.right = halfWidth;
      camera.top = halfWidth * 9 / 16;
      camera.bottom = -halfWidth * 9 / 16;
      camera.position.set(pose2.shot === "pickup" ? 3 : 2.2, 3, 6.2);
      camera.lookAt(0.2, pose2.shot === "toss" ? 1.45 : 1.3, 0.65);
    }
    camera.updateProjectionMatrix();
    camera.updateMatrixWorld(true);
    scene.updateMatrixWorld(true);
    joints.head = head.localToWorld(new THREE.Vector3(0, 0.37, 0)).toArray();
    joints.ball = prop.position;
    debug2.joints = joints;
    debug2.reaches = reaches;
    debug2.shot = pose2.shot;
    debug2.pose = pose2;
    debug2.projected = Object.fromEntries(Object.entries(joints).map(([key2, point]) => [key2, v(point).project(camera).toArray()]));
  }
  return {
    scene,
    camera,
    update,
    debug: debug2,
    environmentObjects,
    actorObjects: scene.children.slice(characterStart),
    materials: mat,
    helpers: { material, ellipsoid, box, cylinder },
    objects: { torso, head, hips, limbs, ball, sofa, eyes, pupils, brows, mouth, smile }
  };
}

// engines/hyperframes-clay3d/films/rest-guilt-v1/src/sets.mjs
import * as THREE2 from "./vendor/three.min.js";
function createWorld(stage2) {
  const { scene, helpers: h, materials: m } = stage2;
  const groups = {};
  const prop = {};
  const ui = {};
  const ink = "#283b3b";
  function group(name) {
    const g = new THREE2.Group();
    g.name = name;
    scene.add(g);
    groups[name] = g;
    return g;
  }
  function board(width = 1024, height = 640) {
    const canvas2 = document.createElement("canvas");
    canvas2.width = width;
    canvas2.height = height;
    const context = canvas2.getContext("2d");
    const texture = new THREE2.CanvasTexture(canvas2);
    texture.colorSpace = THREE2.SRGBColorSpace;
    const material = new THREE2.MeshBasicMaterial({ map: texture, side: THREE2.DoubleSide });
    let signature = "";
    return { canvas: canvas2, context, texture, material, paint(key2, draw) {
      if (key2 === signature) return;
      signature = key2;
      draw(context, width, height);
      texture.needsUpdate = true;
    } };
  }
  function words(ctx, text, x, y, maxWidth, line = 62) {
    let row = "";
    let cy = y;
    for (const word of text.split(" ")) {
      const trial = row ? `${row} ${word}` : word;
      if (ctx.measureText(trial).width > maxWidth && row) {
        ctx.fillText(row, x, cy);
        row = word;
        cy += line;
      } else row = trial;
    }
    if (row) ctx.fillText(row, x, cy);
    return cy;
  }
  function room(name, wall = "#dfd2bc", openBack = false) {
    const g = group(name);
    h.box(g, m.floor, [0, -0.12, 0], [8.5, 0.24, 4.7], 0.08);
    if (!openBack) h.box(g, h.material(wall), [0, 1.9, -1.85], [8.5, 3.8, 0.14], 0.06);
    h.box(g, h.material(wall), [-4.2, 1.9, -0.4], [0.14, 3.8, 2.9], 0.06);
    return g;
  }
  const living = group("living");
  h.cylinder(living, m.shoe, [1.25, 0.36, 0.82], 0.065, 0.72);
  h.cylinder(living, m.trim, [1.25, 0.76, 0.82], 0.55, 0.09);
  const work = room("work", "#d6ddd1", true);
  prop.workFrontWall = h.box(work, h.material("#d6ddd1"), [0, 1.9, 1.85], [8.5, 3.8, 0.14], 0.06);
  prop.workBackWall = h.box(work, h.material("#d6ddd1"), [0, 1.9, -1.85], [8.5, 3.8, 0.14], 0.06);
  h.box(work, m.trim, [0, 0.86, 0.65], [2.7, 0.12, 1.1], 0.05);
  for (const x of [-1.1, 1.1]) for (const z of [0.24, 1.06]) h.cylinder(work, m.shoe, [x, 0.42, z], 0.06, 0.84);
  const chair = new THREE2.Group();
  work.add(chair);
  prop.chair = chair;
  h.box(chair, m.sage, [0, 0.55, 0], [0.78, 0.15, 0.72], 0.08);
  h.box(chair, m.sage, [0, 1, -0.33], [0.78, 0.85, 0.12], 0.08);
  for (const x of [-0.28, 0.28]) for (const z of [-0.24, 0.24]) h.cylinder(chair, m.shoe, [x, 0.25, z], 0.045, 0.5);
  const laptop = new THREE2.Group();
  laptop.position.set(0, 0.95, 0.7);
  work.add(laptop);
  prop.laptop = laptop;
  h.box(laptop, h.material("#70837f"), [0, 0, 0], [1.04, 0.035, 0.7], 0.025);
  for (let y = 0; y < 3; y++) for (let x = 0; x < 9; x++) h.box(laptop, m.cream, [-0.4 + x * 0.1, 0.025, -0.04 + y * 0.09], [0.075, 0.018, 0.06], 8e-3);
  const lid = new THREE2.Group();
  lid.position.set(0, 0.02, 0.32);
  laptop.add(lid);
  prop.lid = lid;
  h.box(lid, h.material("#70837f"), [0, 0.34, 0], [1.04, 0.68, 0.045], 0.025);
  ui.laptop = board();
  const display = new THREE2.Mesh(new THREE2.PlaneGeometry(0.96, 0.59), ui.laptop.material);
  display.rotation.y = Math.PI;
  display.position.set(0, 0.34, -0.026);
  lid.add(display);
  h.cylinder(work, m.sage, [-1, 1.1, 0.95], 0.055, 0.42);
  const lampShade = new THREE2.Mesh(new THREE2.ConeGeometry(0.23, 0.28, 20), h.material("#d4b678"));
  lampShade.position.set(-1, 1.42, 0.95);
  work.add(lampShade);
  const kitchen = room("kitchen", "#cbd7c7");
  h.box(kitchen, m.sage, [0, 0.47, 1.3], [3.55, 0.94, 0.94], 0.07);
  h.box(kitchen, m.cream, [0, 0.99, 1.3], [3.72, 0.1, 1.06], 0.045);
  for (const x of [-1.15, 0, 1.15]) {
    h.box(kitchen, h.material("#9ab5a0"), [x, 0.47, 0.82], [1.05, 0.77, 0.04], 0.03);
    h.cylinder(kitchen, m.shoe, [x + 0.32, 0.55, 0.78], 0.025, 0.16).rotation.z = Math.PI / 2;
  }
  h.box(kitchen, h.material("#526d71"), [0.05, 1.05, 1.25], [0.92, 0.05, 0.63], 0.09);
  h.box(kitchen, h.material("#a2bab7"), [0.05, 1.078, 1.25], [0.74, 0.025, 0.49], 0.08);
  const faucetCurve = new THREE2.CatmullRomCurve3([[0.4, 1.04, 1.58], [0.4, 1.6, 1.58], [0.22, 1.65, 1.32], [0.12, 1.46, 1.16]].map((p) => new THREE2.Vector3(...p)));
  kitchen.add(new THREE2.Mesh(new THREE2.TubeGeometry(faucetCurve, 20, 0.035, 10, false), h.material("#789995")));
  const valve = h.box(kitchen, m.shoe, [0.55, 1.1, 1.05], [0.16, 0.045, 0.045], 0.02);
  prop.valve = valve;
  h.box(kitchen, m.shoe, [-0.9, 1.06, 1.19], [0.75, 0.04, 0.52], 0.025);
  for (let i = 0; i < 5; i++) h.box(kitchen, m.trim, [-1.15 + i * 0.13, 1.13, 1.19], [0.02, 0.15, 0.47], 8e-3);
  const water = h.cylinder(kitchen, h.material("#9bced1", { transparent: true, opacity: 0.62, roughness: 0.3 }), [0.12, 1.27, 1.16], 0.018, 0.4);
  water.visible = false;
  prop.water = water;
  for (let i = 0; i < 3; i++) h.box(kitchen, m.cream, [-1.2 + i * 1.12, 2.4, -1.65], [0.92, 0.96, 0.18], 0.06);
  const entry = room("entry", "#d9c3a8");
  h.box(entry, m.shoe, [0, 1.3, -1.6], [1.65, 2.6, 0.15], 0.04);
  h.box(entry, h.material("#c89968"), [0, 1.3, -1.48], [1.42, 2.4, 0.075], 0.03);
  const knob = h.ellipsoid(entry, m.trim, [0.5, 1.2, -1.4], [0.075, 0.075, 0.06]);
  prop.doorKnob = knob;
  const key = new THREE2.Group();
  scene.add(key);
  prop.key = key;
  const brass = h.material("#b67f21");
  const keyring = new THREE2.Mesh(new THREE2.TorusGeometry(0.065, 0.014, 8, 32), brass);
  keyring.position.z = 0.16;
  key.add(keyring);
  h.box(key, brass, [0, 0, 0.025], [0.032, 0.032, 0.24], 5e-3);
  for (const z of [-0.055, -0.015]) h.box(key, brass, [0.027, -0.012, z], [0.035, 0.035, 0.022], 3e-3);
  h.ellipsoid(entry, m.ink, [0.5, 1.2, -1.332], [0.017, 0.027, 4e-3]);
  h.box(entry, m.trim, [-2.1, 1.65, -1.57], [0.8, 0.1, 0.1], 0.02);
  for (const x of [-2.35, -2.1, -1.85]) h.ellipsoid(entry, m.shoe, [x, 1.59, -1.47], [0.035, 0.07, 0.04]);
  const friend = room("friend", "#b9cdd2");
  h.box(friend, m.sage, [0, 0.34, 0], [2.45, 0.48, 1.35], 0.12);
  h.box(friend, h.material("#d0b7a3"), [0, 0.64, 0], [2.36, 0.21, 1.26], 0.12);
  h.box(friend, m.cream, [0.7, 0.88, -0.2], [0.64, 0.23, 0.7], 0.1);
  h.box(friend, h.material("#84a6a6"), [-0.4, 0.83, 0.12], [1.4, 0.18, 1.15], 0.1);
  h.box(friend, m.trim, [-2.3, 0.6, -0.8], [0.75, 1.2, 0.55], 0.05);
  for (let i = 0; i < 5; i++) h.box(friend, h.material(["#9d6652", "#c6a872", "#4f6c70"][i % 3]), [-2.52 + i * 0.11, 1.37, -0.8], [0.08, 0.3, 0.3], 0.015);
  const inspection = room("inspection", "#bfc7c3");
  h.box(inspection, h.material("#718b85"), [0.5, 0.65, 0.7], [2.8, 1.3, 0.65], 0.07);
  const inspectionSign = board(800, 400);
  ui.inspection = inspectionSign;
  const sign = new THREE2.Mesh(new THREE2.PlaneGeometry(1.5, 0.75), inspectionSign.material);
  sign.position.set(0.5, 1.25, 1.04);
  inspection.add(sign);
  inspectionSign.paint("receipt", (ctx) => {
    ctx.fillStyle = "#f4e4c6";
    ctx.fillRect(0, 0, 800, 400);
    ctx.fillStyle = ink;
    ctx.textAlign = "center";
    ctx.font = "800 80px Nunito";
    ctx.fillText("REST DESK", 400, 140);
    ctx.font = "700 52px Nunito";
    ctx.fillText("Receipt required", 400, 260);
  });
  function loose(name) {
    const g = new THREE2.Group();
    g.name = name;
    scene.add(g);
    prop[name] = g;
    return g;
  }
  const phone = loose("phone");
  h.box(phone, m.ink, [0, 0, 0], [0.25, 0.45, 0.035], 0.025);
  ui.phone = board(500, 900);
  const phoneScreen = new THREE2.Mesh(new THREE2.PlaneGeometry(0.224, 0.404), ui.phone.material);
  phoneScreen.position.z = 0.019;
  phone.add(phoneScreen);
  prop.phoneScreen = phoneScreen;
  const remote = loose("remote");
  h.box(remote, m.ink, [0, 0, 0], [0.085, 0.035, 0.23], 0.023);
  for (let i = 0; i < 3; i++) h.ellipsoid(remote, i ? m.cream : m.sofa, [0, 0.021, -0.06 + i * 0.06], [0.014, 8e-3, 0.014]);
  const bowl = loose("bowl");
  const half = new THREE2.Mesh(new THREE2.SphereGeometry(1, 24, 12, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), h.material("#b0c7bd", { side: THREE2.DoubleSide }));
  half.scale.set(0.2, 0.14, 0.2);
  bowl.add(half);
  const rim = new THREE2.Mesh(new THREE2.TorusGeometry(0.2, 0.018, 6, 32), m.cream);
  rim.rotation.x = Math.PI / 2;
  bowl.add(rim);
  for (let i = 0; i < 12; i++) {
    const a = i * 2.4;
    h.ellipsoid(bowl, m.cream, [Math.sin(a) * 0.13, 0.015 + Math.floor(i / 5) * 0.025, Math.cos(a) * 0.11], [0.038, 0.043, 0.038]);
  }
  const snack = loose("snack");
  h.ellipsoid(snack, h.material("#d3a56a"), [0, 0, 0], [0.055, 0.025, 0.052]);
  const plate = loose("plate");
  h.cylinder(plate, m.white, [0, 0, 0], 0.235, 0.018);
  const edge = new THREE2.Mesh(new THREE2.TorusGeometry(0.22, 0.018, 8, 32), m.white);
  edge.rotation.x = Math.PI / 2;
  plate.add(edge);
  const pen = loose("pen");
  h.cylinder(pen, m.vest, [0, 0, 0], 0.014, 0.24);
  const tip = new THREE2.Mesh(new THREE2.ConeGeometry(0.012, 0.045, 8), m.ink);
  tip.rotation.x = Math.PI;
  tip.position.y = -0.14;
  pen.add(tip);
  const paper = loose("paper");
  ui.paper = board(900, 600);
  const page = new THREE2.Mesh(new THREE2.PlaneGeometry(0.78, 0.52), ui.paper.material);
  page.rotation.x = -Math.PI / 2;
  paper.add(page);
  const basket = loose("basket");
  h.box(basket, m.sage, [0, 0, 0], [0.7, 0.36, 0.46], 0.07);
  for (let i = 0; i < 4; i++) h.ellipsoid(basket, h.material(["#d5b88f", "#e4d5b4", "#a9b9b4"][i % 3]), [-0.2 + i * 0.13, 0.17, 0], [0.16, 0.1, 0.15]);
  const cup = loose("cup");
  h.cylinder(cup, m.cream, [0, 0, 0], 0.09, 0.2);
  h.cylinder(cup, h.material("#9abcc0"), [0, 0.101, 0], 0.075, 8e-3);
  const receipt = loose("receipt");
  ui.receipt = board(700, 700);
  const receiptFace = new THREE2.Mesh(new THREE2.PlaneGeometry(0.62, 0.62), ui.receipt.material);
  receipt.add(receiptFace);
  ui.receipt.paint("receipt", (ctx) => {
    ctx.fillStyle = "#f5e4bf";
    ctx.fillRect(0, 0, 700, 700);
    ctx.fillStyle = ink;
    ctx.textAlign = "center";
    ctx.font = "800 75px Nunito";
    ctx.fillText("YOUR RECEIPT?", 350, 180);
    ctx.font = "600 53px Nunito";
    ctx.fillText("Permission to rest", 350, 360);
    ctx.fillText("Not found", 350, 500);
  });
  const insertHands = loose("insertHands");
  h.ellipsoid(insertHands, m.skin, [-0.162, -0.18, 0.015], [0.045, 0.075, 0.05]);
  h.ellipsoid(insertHands, m.skin, [0.162, -0.18, 0.015], [0.045, 0.075, 0.05]);
  prop.insertFinger = h.ellipsoid(insertHands, m.skin, [0.105, -0.205, 0.05], [0.022, 0.03, 0.025]);
  function show(set) {
    for (const [name, g] of Object.entries(groups)) g.visible = name === set;
    stage2.environmentObjects.forEach((o) => {
      o.visible = set === "living";
    });
    for (const object of Object.values(prop)) if (object.parent === scene) object.visible = false;
  }
  function phoneText(message, draft = "", mode = "message", progress = 1) {
    const text = draft.slice(0, Math.round(draft.length * progress));
    ui.phone.paint(`${message}|${text}|${mode}`, (ctx) => {
      ctx.fillStyle = "#f4eddf";
      ctx.fillRect(0, 0, 500, 900);
      ctx.fillStyle = "#315f55";
      ctx.fillRect(0, 0, 500, 120);
      ctx.font = "800 52px Nunito";
      ctx.fillStyle = "#fff9e9";
      ctx.fillText(mode === "timer" ? "Timer" : "Messages", 30, 80);
      if (mode === "timer") {
        ctx.fillStyle = ink;
        ctx.textAlign = "center";
        ctx.font = "800 104px Nunito";
        ctx.fillText(message, 250, 400);
        ctx.textAlign = "left";
        ctx.font = "600 44px Nunito";
        words(ctx, "Your break", 70, 530, 360, 56);
        return;
      }
      ctx.fillStyle = "#dce5da";
      ctx.fillRect(25, 170, 450, 300);
      ctx.fillStyle = ink;
      ctx.font = "700 48px Nunito";
      words(ctx, message, 45, 235, 410, 64);
      if (draft) {
        ctx.fillStyle = "#fffdf5";
        ctx.fillRect(25, 515, 450, 285);
        ctx.fillStyle = ink;
        ctx.font = "700 47px Nunito";
        words(ctx, text, 45, 575, 410, 60);
        ctx.font = "800 36px Nunito";
        ctx.fillStyle = "#90664c";
        ctx.fillText(mode === "unsent" ? "UNSENT" : "Reply", 45, 845);
      }
    });
  }
  function laptopText(mode, progress = 1) {
    ui.laptop.paint(`${mode}|${Math.floor(progress * 40)}`, (ctx) => {
      ctx.fillStyle = "#f2ebd7";
      ctx.fillRect(0, 0, 1024, 640);
      ctx.fillStyle = "#315f55";
      ctx.fillRect(0, 0, 1024, 95);
      ctx.fillStyle = "#fff9eb";
      ctx.font = "800 48px Nunito";
      ctx.fillText(mode === "document" ? "Document" : "Inbox", 42, 65);
      ctx.fillStyle = ink;
      if (mode === "document") {
        ctx.font = "800 53px Nunito";
        ctx.fillText("A small correction", 42, 180);
        ctx.font = "600 44px Nunito";
        words(ctx, "Fix this paragraph tomorrow. The urgent work is done.", 42, 275, 910, 70);
        ctx.fillStyle = "#b95f4f";
        ctx.fillRect(42, 360, 650, 10);
        return;
      }
      ctx.font = "800 53px Nunito";
      ctx.fillText("One last email", 42, 185);
      ctx.font = "600 44px Nunito";
      words(ctx, mode === "reply" ? "Thanks, I will send the update tomorrow.".slice(0, Math.round(progress * 43)) : "Quick question about the document.", 42, 280, 910, 65);
      if (mode === "overflow") {
        ctx.fillStyle = "#d9e2d6";
        for (let i = 0; i < 3; i++) {
          ctx.fillRect(40, 245 + i * 112, 940, 88);
          ctx.fillStyle = ink;
          ctx.font = "700 38px Nunito";
          ctx.fillText(["Another message", "A document to check", "One small change"][i], 60, 302 + i * 112);
          ctx.fillStyle = "#d9e2d6";
        }
      } else {
        ctx.fillStyle = "#315f55";
        ctx.fillRect(760, 500, 200, 85);
        ctx.fillStyle = "#fff9eb";
        ctx.font = "800 42px Nunito";
        ctx.fillText(mode === "sent" ? "Sent" : "Send", 795, 557);
      }
    });
  }
  function noteText(progress = 1) {
    const text = "FIX PARAGRAPH\nTomorrow\nAfter breakfast";
    ui.paper.paint(`note|${Math.floor(progress * text.length)}`, (ctx) => {
      ctx.fillStyle = "#f8ebca";
      ctx.fillRect(0, 0, 900, 600);
      ctx.fillStyle = ink;
      ctx.font = "800 66px Nunito";
      text.slice(0, Math.round(progress * text.length)).split("\n").forEach((line, i) => ctx.fillText(line, 60, 140 + i * 140));
    });
  }
  return { groups, prop, ui, show, phoneText, laptopText, noteText };
}

// engines/hyperframes-clay3d/films/rest-guilt-v1/src/acting.mjs
var ROOMATE_ACTIONS = /* @__PURE__ */ new Set(["roommate_arrive", "almost_excuse", "faucet_off", "honest", "roommate_question", "snack_grab"]);
var move = (a, b, u) => mix(a, b, clamp(u));
function stand(x = 0, z = 0.5, yaw = 0) {
  return { position: [x, 1.18, z], yaw, lean: 0, sitting: 0, squat: 0, left: { position: add([x, 0.12, z], rotateY([-0.18, 0, 0], yaw)), moving: false }, right: { position: add([x, 0.12, z], rotateY([0.18, 0, 0], yaw)), moving: false }, shoeYaw: yaw };
}
function seated(x = 0, z = -0.25, height = 0.83) {
  const a = stand(x, z);
  a.position[1] = height;
  a.sitting = 1;
  a.left.position = [x - 0.2, 0.12, z + 0.7];
  a.right.position = [x + 0.2, 0.12, z + 0.7];
  return a;
}
function walk(from, to, u) {
  const raw = actorAt(0.6 + clamp(u) * 3.25), dx = to[0] - from[0], dz = to[1] - from[1], distance = Math.hypot(dx, dz), yaw = Math.atan2(dx, dz);
  const along = [Math.sin(yaw), 0, Math.cos(yaw)], side = [Math.cos(yaw), 0, -Math.sin(yaw)];
  const foot = (f) => {
    const q = (f.position[0] + 2.7) / 2.825;
    return { position: [from[0] + along[0] * q * distance + side[0] * (f.position[2] - 0.71), f.position[1], from[1] + along[2] * q * distance + side[2] * (f.position[2] - 0.71)], moving: f.moving, phase: f.phase };
  };
  const left = foot(raw.left), right = foot(raw.right);
  const span = Math.hypot(left.position[0] - right.position[0], left.position[2] - right.position[2]);
  return { position: [(left.position[0] + right.position[0]) / 2, 1.18 - 0.13 * (span / 1.15) ** 2, (left.position[2] + right.position[2]) / 2], yaw, lean: 0.065, sitting: 0, squat: 0, left, right, shoeYaw: yaw };
}
function sitMotion(u) {
  const a = seated(2.3, -0.05, 0.84);
  const q = ease(u, 0.08, 0.83);
  a.position = move([2.3, 1.18, 0.45], [2.3, 0.84, -0.05], q);
  a.sitting = q;
  a.lean = 0.28 * Math.sin(Math.PI * q) - 0.07 * q;
  return a;
}
function pose(actor, t, smile = 0) {
  const swing = Math.sin(t * 13);
  return { time: t, t, actor, ball: { position: localPoint(actor, [0, 0.65, 3]) }, leftHand: localPoint(actor, [-0.38, actor.sitting ? 0.18 : 0.04, 0.2 - (actor.left.moving ? 0.2 * swing : 0)]), rightHand: localPoint(actor, [0.38, actor.sitting ? 0.18 : 0.04, 0.2 + (actor.right.moving ? 0.2 * swing : 0)]), blink: Math.max(0, 1 - Math.abs((t + 1.1) % 4.7 - 2.1) / 0.1), smile, shot: "wide" };
}
function frameState(shot, time) {
  const local = time - shot.start, duration = shot.end - shot.start, u = clamp(local / duration), a = shot.action, p = shot.paragraph;
  const out = { set: shot.set, action: a, camera: shot.camera, heroVisible: true, buddyVisible: false, role: "roommate", mood: "neutral", props: {}, water: false, typing: 0, progress: u, shotId: shot.id };
  let hero = pose(shot.set === "living" ? seated(2.3, -0.05, 0.84) : shot.set === "work" ? seated(0, -0.25, 0.83) : stand(-0.2, 0.5), time);
  let buddy2 = pose(stand(1.9, 0.1), time, 0.45);
  const own = (name, who, hand, offset = [0, 0, 0], rotation = [0, 0, 0]) => {
    out.props[name] = { position: add((who === "hero" ? hero : buddy2)[`${hand}Hand`], offset), rotation, owner: `${who}.${hand}`, offset };
  };
  const fixed = (name, position, rotation = [0, 0, 0]) => {
    out.props[name] = { position, rotation, owner: null };
  };
  const gaze = (point, who = hero) => {
    who.ball.position = point;
  };
  const kitchenBowl = [-1.35, 1.2, 1.12], tableBowl = [1, 0.9, 0.82], tableRemote = [1.62, 0.84, 0.7], rackPlate = [-0.85, 1.28, 1.19], heldPlate = [-0.12, 1.22, 1.12], restPlate = [-0.4, 1.06, 1.12];
  if (shot.set === "living") {
    fixed("bowl", p >= 11 ? tableBowl : [1, 0.9, 0.82]);
    fixed("remote", tableRemote);
    if (p < 11 && a !== "uneasy_movie") out.props.bowl.visible = false;
  }
  if (shot.set === "kitchen") {
    fixed("bowl", kitchenBowl);
    out.props.bowl.visible = p >= 2 && p <= 11;
    fixed("plate", p >= 13 ? restPlate : rackPlate, p >= 13 ? [0, 0, 0] : [Math.PI / 2, 0, 0]);
  }
  out.chairZ = -0.25;
  out.lidAngle = p >= 12 ? -Math.PI / 2 : 0.12;
  if (["couch_guilt", "couch_movie", "uneasy_movie", "still_guilty", "stay", "watch", "rest_end"].includes(a)) {
    hero = pose(seated(2.3, -0.05, 0.84), time, a === "rest_end" ? 0.72 : a === "watch" ? 0.6 : 0.1);
    hero.leftHand = localPoint(hero.actor, [-0.28, 0.2, 0.35]);
    own("remote", "hero", "left", [0, 0.01, 0.02]);
    if (a === "couch_guilt" || a === "still_guilty" || a === "uneasy_movie") {
      hero.actor.lean = 0.06 + 0.08 * Math.sin(Math.PI * u);
      hero.rightHand = localPoint(hero.actor, [0.34, 0.25 + 0.12 * Math.sin(Math.PI * u), 0.31]);
      out.mood = "guilty";
      gaze([-0.6, 2, 1.2]);
    } else {
      hero.actor.lean = -0.04 * ease(u, 0.2, 0.8);
      hero.rightHand = localPoint(hero.actor, [0.34, 0.16, 0.26]);
      gaze([1.6, 1.7, 3.5]);
    }
  }
  if (a === "keys") {
    out.heroVisible = false;
    fixed("key", [0.5, 1.2, -1.28], [0, 0, 0.4 * Math.sin(Math.PI * u)]);
    out.keyHand = true;
  }
  if (["dinner_done", "prepare_snack", "set_snack", "pickup_snack"].includes(a)) {
    hero = pose(stand(-1.2, 0.5), time, 0.15);
    hero.actor.lean = 0.23;
    const contact = [-1.35, 1.04, 1.12], carry = localPoint(hero.actor, [-0.3, 0.25, 0.38]);
    if (a === "dinner_done") {
      hero.leftHand = move(localPoint(hero.actor, [-0.35, 0.1, 0.3]), [-1.35, 1.09, 1.08], ease(u, 0.05, 0.55));
      hero.rightHand = localPoint(hero.actor, [0.31, 0.12, 0.37]);
      fixed("plate", [-1.2, 1.06, 1.3]);
    } else if (a === "set_snack") {
      hero.leftHand = move(carry, contact, ease(u, 0.04, 0.7));
      if (u < 0.72) own("bowl", "hero", "left", [0, 0.16, 0]);
      else fixed("bowl", kitchenBowl);
    } else {
      hero.leftHand = move(localPoint(hero.actor, [-0.35, 0.1, 0.3]), contact, ease(u, 0.02, 0.35));
      if (u > 0.36) {
        hero.leftHand = move(contact, carry, ease(u, 0.38, 0.95));
        own("bowl", "hero", "left", [0, 0.16, 0]);
      } else fixed("bowl", kitchenBowl);
      hero.rightHand = localPoint(hero.actor, [0.25, 0.17, 0.35]);
    }
    gaze(kitchenBowl);
  }
  if (a === "walk_pull") {
    if (u < 0.67) hero = pose(walk([1.65, -0.3], [0, -0.75], u / 0.67), time);
    else {
      hero = pose(stand(0, -0.75), time);
      out.chairZ = 0.05 - 0.3 * ease(u, 0.67, 0.95);
      hero.leftHand = [-0.27, 1.37, out.chairZ - 0.33];
    }
    gaze([0, 1.3, 0.8]);
  }
  if (["typing_reply", "file_check", "inbox_overflow", "reach_work", "alarm_off", "missed_break", "hesitate", "realize", "leave_desk", "useful_pause", "hover_couch", "urgent_done", "close_laptop", "write_note", "phone_reply"].includes(a)) {
    hero = pose(seated(0, -0.25, 0.83), time);
    hero.actor.lean = 0.24;
    gaze([0, 1.35, 0.92]);
    hero.leftHand = [-0.2, 1.075, 0.71];
    hero.rightHand = [0.22, 1.075, 0.71];
    if (["typing_reply", "inbox_overflow", "file_check", "reach_work"].includes(a)) {
      hero.leftHand[1] += 0.012 * Math.sin(local * 14 + 0.5);
      hero.rightHand[1] += 0.012 * Math.sin(local * 17);
      out.typing = u;
      if (a === "file_check") hero.rightHand = [0.5, 1.07, 0.63];
    }
    if (["missed_break", "hesitate", "realize", "useful_pause", "urgent_done"].includes(a)) {
      hero.actor.lean = 0.08;
      hero.leftHand = localPoint(hero.actor, [-0.34, 0.16, 0.3]);
      hero.rightHand = move([0.2, 1.04, 0.5], localPoint(hero.actor, [0.25, 0.77, -0.04]), ease(u, 0.15, 0.7));
      out.mood = a === "realize" ? "recognition" : "guilty";
      if (a === "realize") hero.rightHand = localPoint(hero.actor, [0.3, 0.35, 0.4]);
    }
    if (a === "useful_pause") {
      hero.actor.lean = 0.24 - 0.2 * ease(u, 0.4, 0.9);
      hero.rightHand = move([0.22, 1.12, 0.58], [0.2, 1.12, 0.6], ease(u, 0.05, 0.32));
      if (u > 0.38) hero.rightHand = move([0.2, 1.12, 0.6], localPoint(hero.actor, [0.34, 0.16, 0.3]), ease(u, 0.42, 0.88));
      gaze(move([0, 1.35, 0.92], [2.3, 1.6, 1.2], ease(u, 0.5, 0.9)));
    }
    if (a === "leave_desk") {
      hero = pose(stand(0.2, -0.35), time);
      hero.actor.yaw = -0.5 * ease(u, 0.1, 0.8);
      hero.leftHand = [-0.27, 1.37, -0.58];
      gaze([1.5, 1.3, 1]);
    }
    if (a === "hover_couch") {
      hero = pose(stand(0.1, -0.4), time);
      hero.actor.position[1] -= 0.16 * Math.sin(Math.PI * u);
      hero.leftHand = [-0.27, 1.34, -0.58];
      hero.rightHand = localPoint(hero.actor, [0.38, 0.1, 0.25]);
      gaze([0, 1.4, 0.8]);
    }
    if (a === "alarm_off") {
      hero.rightHand = move([0.22, 1.075, 0.71], [0.7, 1.025, 0.55], ease(u, 0.1, 0.5));
      fixed("phone", [0.7, 0.99, 0.55], [-Math.PI / 2, 0, 0]);
      out.phoneMode = "timer";
      out.message = "00:00";
    }
    if (a === "close_laptop") {
      hero = pose(stand(0, -0.1), time);
      hero.actor.position[1] = 1.1;
      hero.actor.lean = 0.64;
      gaze([0, 1.3, 0.8]);
      const q = ease(u, 0.15, 0.8);
      out.lidAngle = 0.12 + (-Math.PI / 2 - 0.12) * q;
      const angle = out.lidAngle;
      hero.leftHand = [-0.2, 0.97 + 0.64 * Math.cos(angle), 1.02 + 0.64 * Math.sin(angle)];
      hero.rightHand = localPoint(hero.actor, [0.35, 0.12, 0.3]);
    }
    if (a === "write_note") {
      fixed("paper", [0.92, 0.925, 0.57]);
      out.props.paper.scale = 0.75;
      const q = clamp((u - 0.06) / 0.58);
      hero.actor.position[0] = 0.25;
      hero.actor.lean = 0.34;
      hero.rightHand = [0.72 + 0.22 * (q * 3 % 1), 1.08, 0.46 + Math.floor(Math.min(0.999, q) * 3) * 0.085];
      hero.leftHand = localPoint(hero.actor, [-0.34, 0.14, 0.3]);
      if (u > 0.72) hero.rightHand = move(hero.rightHand, localPoint(hero.actor, [0.34, 0.23, 0.3]), ease(u, 0.72, 0.92));
      own("pen", "hero", "right", [0, -0.02, 0]);
      out.noteProgress = q;
    }
    if (a === "phone_reply" || a === "realize") {
      hero.actor.lean = 0.1;
      hero.rightHand = localPoint(hero.actor, [0.3, 0.35, 0.4]);
      hero.leftHand = localPoint(hero.actor, [-0.03, 0.28, 0.46]);
      own("phone", "hero", "right", [0, 0.1, 0], [0, Math.PI, 0]);
      gaze(out.props.phone.position);
      out.message = "I did nothing all afternoon. I feel awful.";
      out.draft = "You were exhausted. You needed a break.";
    }
  }
  if (["phone_movie", "phone_question", "unsent_insert", "thumb_stop", "timer_insert", "email_insert", "document_insert", "remote_insert", "empty_movie"].includes(a)) {
    out.heroVisible = false;
    if (["phone_movie", "phone_question", "unsent_insert", "thumb_stop", "timer_insert"].includes(a)) {
      fixed("phone", [0, 1.5, 0.5]);
      out.insertHands = true;
      out.message = a === "phone_movie" ? "Finally, movie time." : a === "timer_insert" ? "00:00" : "How's the movie?";
      out.draft = ["unsent_insert", "thumb_stop"].includes(a) ? "Haven't earned it yet." : "";
      out.phoneMode = a === "timer_insert" ? "timer" : out.draft ? "unsent" : "message";
      out.phoneProgress = a === "thumb_stop" ? 1 : clamp(u * 1.6);
    }
    if (a === "remote_insert" || a === "empty_movie") {
      fixed("remote", tableRemote);
      if (p < 11) out.props.bowl = { position: kitchenBowl, visible: false };
    }
    if (a === "timer_insert") {
      fixed("phone", [0.7, 0.99, 0.55], [-Math.PI / 2, 0, 0]);
      out.insertHands = false;
    }
  }
  if (a === "snack_cooling") {
    out.heroVisible = false;
    fixed("bowl", kitchenBowl);
  }
  if (["friend_rest", "friend_kindness", "leisure", "boss"].includes(a)) {
    out.heroVisible = false;
    out.buddyVisible = true;
    out.role = "friend";
    buddy2 = pose(seated(0, -0.05, 0.84), time, a === "friend_kindness" ? 0.55 : 0.08);
    buddy2.actor.lean = a === "friend_rest" ? -0.11 : 0.1;
    if (a === "boss") buddy2 = pose(seated(0, -0.25, 0.83), time, 0.02);
    buddy2.rightHand = localPoint(buddy2.actor, [0.3, 0.36, 0.42]);
    buddy2.leftHand = localPoint(buddy2.actor, [-0.1, 0.28, 0.42]);
    own("phone", "buddy", "right", [0, 0.1, 0], [0, Math.PI, 0]);
    gaze(out.props.phone.position, buddy2);
    out.message = a === "boss" ? "Please reply tonight." : a === "friend_kindness" ? "You needed a break." : "I feel bad about doing nothing.";
  }
  if (["inspection", "receipt"].includes(a)) {
    hero = pose(stand(-1.05, 0.65), time, 0.05);
    buddy2 = pose(seated(0.95, 0, 0.84), time, 0.1);
    out.buddyVisible = true;
    out.role = "clerk";
    hero.rightHand = [-0.26, 1.32, 0.85];
    buddy2.leftHand = [0.36, 1.32, 0.85];
    buddy2.rightHand = localPoint(buddy2.actor, [0.4, 0.2, 0.4]);
    fixed("receipt", [0.05, 1.32, 0.87], [0, -0.06, 0]);
    hero.leftHand = localPoint(hero.actor, [-0.32, 0.25, 0.3]);
    own("remote", "hero", "left");
    gaze([0.95, 1.8, 0.4]);
    gaze([-1, 2, 0.65], buddy2);
  }
  if (a === "laundry") {
    out.heroVisible = false;
    out.buddyVisible = true;
    out.role = "friend";
    buddy2 = pose(walk([-0.9, 0.5], [0.5, 0.5], clamp(u * 1.25)), time, 0.05);
    buddy2.leftHand = localPoint(buddy2.actor, [-0.29, 0.23, 0.43]);
    buddy2.rightHand = localPoint(buddy2.actor, [0.29, 0.23, 0.43]);
    fixed("basket", localPoint(buddy2.actor, [0, 0.24, 0.46]));
  }
  if (a === "care") {
    out.buddyVisible = true;
    out.role = "friend";
    hero = pose(seated(0.65, -0.05, 0.84), time, 0.25);
    buddy2 = pose(stand(-0.65, 0.5), time, 0.3);
    hero.leftHand = [0.18, 1.2, 0.75];
    buddy2.rightHand = move(localPoint(buddy2.actor, [0.3, 0.08, 0.3]), [-0.02, 1.15, 0.75], ease(u, 0.1, 0.65));
    own("cup", "buddy", "right", [0, 0.1, 0]);
    gaze(out.props.cup.position);
    gaze([0.65, 1.8, 0.3], buddy2);
  }
  if (a === "walk_snack") {
    hero = pose(walk([-0.1, 0.5], [1.25, 0.35], clamp(u * 1.08)), time, 0.12);
    hero.leftHand = localPoint(hero.actor, [-0.3, 0.22, 0.36]);
    own("bowl", "hero", "left", [0, 0.16, 0]);
    gaze([2.3, 1.2, 0]);
  }
  if (a === "sit_play") {
    if (u < 0.25) {
      hero = pose(stand(1.25, 0.35), time, 0.1);
      hero.actor.position[1] = 0.98;
      hero.actor.lean = 0.3;
      hero.leftHand = move(localPoint(hero.actor, [-0.3, 0.22, 0.36]), [1, 0.74, 0.82], ease(u, 0, 0.22));
      if (u < 0.22) own("bowl", "hero", "left", [0, 0.16, 0]);
      else fixed("bowl", tableBowl);
    } else if (u < 0.5) {
      hero = pose(walk([1.25, 0.35], [2.3, 0.45], (u - 0.25) / 0.25), time, 0.1);
      fixed("bowl", tableBowl);
    } else {
      hero = pose(sitMotion((u - 0.5) / 0.5), time, 0.2);
      fixed("bowl", tableBowl);
      hero.actor.lean += 0.43 * ease(u, 0.76, 0.9);
      hero.leftHand = move(localPoint(hero.actor, [-0.28, 0.2, 0.35]), [1.62, 0.82, 0.7], ease(u, 0.76, 0.91));
      if (u > 0.91) {
        hero.leftHand = move([1.62, 0.82, 0.7], localPoint(hero.actor, [-0.28, 0.2, 0.35]), ease(u, 0.91, 1));
        own("remote", "hero", "left", [0, 0.01, 0.02]);
      }
    }
  }
  if (a === "startle") {
    const q = ease(u, 0.26, 0.9);
    hero = pose(sitMotion(1 - q), time, 0);
    hero.actor.lean += 0.4 * (1 - q);
    out.mood = "guilty";
    hero.leftHand = move(localPoint(hero.actor, [-0.28, 0.2, 0.35]), [1.62, 0.82, 0.7], ease(u, 0, 0.22));
    if (u < 0.22) own("remote", "hero", "left", [0, 0.01, 0.02]);
    if (u > 0.25) hero.leftHand = localPoint(hero.actor, [-0.39, 0.06, 0.16]);
    gaze([-0.3, 2, 1.5]);
  }
  if (a === "hurry") {
    if (u < 0.4) hero = pose(walk([1.85, 0.5], [-0.2, 0.5], u / 0.4), time, 0);
    else {
      hero = pose(stand(-0.2, 0.5), time, 0);
      const end = walk([1.85, 0.5], [-0.2, 0.5], 1);
      hero.actor.left = end.left;
      hero.actor.right = end.right;
      hero.actor.lean = 0.2;
      const handAtRack = [-1, 1.28, 1.19], holding = [-0.28, 1.2, 1.12];
      hero.leftHand = move(localPoint(hero.actor, [-0.35, 0.12, 0.35]), handAtRack, ease(u, 0.4, 0.62));
      if (u > 0.64) {
        hero.leftHand = move(handAtRack, holding, ease(u, 0.64, 0.96));
        own("plate", "hero", "left", [0.16, 0.02, 0], [Math.PI / 3, 0, 0.1]);
      } else fixed("plate", rackPlate, [Math.PI / 2, 0, 0]);
    }
    gaze([-0.6, 1.2, 1.16]);
  }
  if (["wash", "roommate_arrive", "almost_excuse", "faucet_off", "honest", "roommate_question"].includes(a)) {
    hero = pose(stand(-0.2, 0.5), time, a === "honest" ? 0.35 : 0);
    hero.actor.lean = 0.2;
    out.water = true;
    hero.leftHand = [-0.28, 1.2, 1.12];
    hero.rightHand = [-0.03 + 0.045 * Math.sin(local * 7), 1.245, 1.205];
    own("plate", "hero", "left", [0.16, 0.02, 0], [Math.PI / 3, 0, 0.1]);
    gaze(heldPlate);
    out.mood = a === "almost_excuse" ? "guilty" : "neutral";
    if (ROOMATE_ACTIONS.has(a)) {
      out.buddyVisible = true;
      buddy2 = pose(a === "roommate_arrive" ? walk([2.8, 0.3], [1.75, 0.35], clamp(u * 1.3)) : stand(1.75, 0.35), time, 0.3);
      gaze([-0.2, 2, 0.5], buddy2);
    }
    if (a === "faucet_off") {
      hero.rightHand = move([-0.02, 1.245, 1.205], [0.55, 1.13, 1.05], ease(u, 0.02, 0.28));
      out.water = u < 0.36;
      if (u > 0.4) {
        hero.leftHand = move([-0.28, 1.2, 1.12], [-0.56, 1.07, 1.12], ease(u, 0.4, 0.72));
        if (u < 0.74) own("plate", "hero", "left", [0.16, 0.02, 0], [Math.PI / 3 * (1 - ease(u, 0.4, 0.72)), 0, 0]);
        else fixed("plate", restPlate);
      }
    }
    if (a === "honest" || a === "roommate_question") {
      out.water = false;
      fixed("plate", restPlate);
      hero.actor.lean = 0.02;
      hero.leftHand = localPoint(hero.actor, [-0.38, 0.05, 0.18]);
      hero.rightHand = localPoint(hero.actor, [0.38, 0.05, 0.18]);
      gaze([1.75, 2, 0.35]);
      out.mood = "relief";
    }
    if (a === "roommate_question") buddy2.rightHand = localPoint(buddy2.actor, [0.45, 0.28, 0.38]);
  }
  if (a === "sit_back") hero = pose(sitMotion(u), time, 0.4);
  if (a === "snack_grab") {
    hero = pose(seated(2.3, -0.05, 0.84), time, 0.45);
    out.buddyVisible = true;
    buddy2 = pose(stand(0.55, 0.55), time, 0.5);
    buddy2.actor.position[1] -= 0.13 * Math.sin(Math.PI * clamp(u * 1.6));
    buddy2.actor.lean = 0.17;
    const table = [1.05, 0.98, 0.82], mouth = localPoint(buddy2.actor, [0.17, 0.79, 0.27]);
    buddy2.rightHand = move(localPoint(buddy2.actor, [0.38, 0.1, 0.2]), table, ease(u, 0.02, 0.3));
    if (u > 0.34) {
      buddy2.rightHand = move(table, mouth, ease(u, 0.35, 0.78));
      own("snack", "buddy", "right", [0, 0.02, 0.02]);
      if (u > 0.85) out.props.snack.scale = 1 - ease(u, 0.85, 1);
    }
    if (u > 0.62) {
      buddy2 = pose(walk([0.55, 0.55], [-1.65, -0.5], (u - 0.62) / 0.38), time, 0.4);
      out.props.snack.visible = false;
    }
    fixed("bowl", tableBowl);
    gaze([2.3, 1.8, 0.4], buddy2);
  }
  if (a === "find_place") {
    hero = pose(seated(2.3, -0.05, 0.84), time, 0.5);
    hero.actor.lean = 0.43;
    hero.leftHand = move([1.62, 0.82, 0.7], localPoint(hero.actor, [-0.28, 0.2, 0.35]), ease(u, 0.1, 0.7));
    own("remote", "hero", "left", [0, 0.01, 0.02]);
    gaze([1.6, 1.7, 3.5]);
  }
  out.hero = hero;
  out.buddy = buddy2;
  if (a === "inbox_overflow") out.laptopMode = "overflow";
  else if (["file_check", "document_insert", "write_note", "close_laptop", "urgent_done"].includes(a)) out.laptopMode = "document";
  else out.laptopMode = a === "typing_reply" ? "reply" : "email";
  return out;
}

// engines/hyperframes-clay3d/films/rest-guilt-v1/assets/timeline.json
var timeline_default = {
  title: "Why You Feel Guilty When You Rest",
  duration: 277.1666666666667,
  pose_hz: 12,
  capture_fps: 12,
  delivery_fps: 30,
  script_sha256: "30f4fbc4dc8da1f6d4c4b99e42882a7da065e15018f4edd21e7b66a7196fa27d",
  shots: [
    {
      id: "p01-s01",
      paragraph: 1,
      anchor: "Why does",
      action: "couch_guilt",
      set: "living",
      camera: "face",
      start: 0,
      source_word: 0,
      end: 3.71,
      duration: 3.71
    },
    {
      id: "p01-s02",
      paragraph: 1,
      anchor: "Picture this.",
      action: "keys",
      set: "entry",
      camera: "key",
      start: 3.71,
      source_word: 11,
      end: 7.37,
      duration: 3.66
    },
    {
      id: "p01-s03",
      paragraph: 1,
      anchor: "A second ago,",
      action: "couch_movie",
      set: "living",
      camera: "living",
      start: 7.37,
      source_word: 20,
      end: 10.33,
      duration: 2.96
    },
    {
      id: "p01-s04",
      paragraph: 1,
      anchor: "Now you're washing",
      action: "wash",
      set: "kitchen",
      camera: "sink",
      start: 10.33,
      source_word: 28,
      end: 15.822,
      duration: 5.492
    },
    {
      id: "p02-s01",
      paragraph: 2,
      anchor: "An hour earlier,",
      action: "dinner_done",
      set: "kitchen",
      camera: "kitchen",
      start: 15.822,
      source_word: 38,
      end: 23.002,
      duration: 7.18
    },
    {
      id: "p02-s02",
      paragraph: 2,
      anchor: "You texted",
      action: "phone_movie",
      set: "living",
      camera: "phone",
      start: 23.002,
      source_word: 53,
      end: 26.482,
      duration: 3.48
    },
    {
      id: "p02-s03",
      paragraph: 2,
      anchor: "You made a snack,",
      action: "prepare_snack",
      set: "kitchen",
      camera: "kitchen",
      start: 26.482,
      source_word: 60,
      end: 31.102,
      duration: 4.62
    },
    {
      id: "p02-s04",
      paragraph: 2,
      anchor: "Then you noticed",
      action: "email_insert",
      set: "work",
      camera: "laptop",
      start: 31.102,
      source_word: 72,
      end: 34.204667,
      duration: 3.102667
    },
    {
      id: "p03-s01",
      paragraph: 3,
      anchor: "One unanswered email.",
      action: "email_insert",
      set: "work",
      camera: "laptop",
      start: 34.204667,
      source_word: 80,
      end: 39.844667,
      duration: 5.64
    },
    {
      id: "p03-s02",
      paragraph: 3,
      anchor: "But answering",
      action: "hesitate",
      set: "work",
      camera: "face",
      start: 39.844667,
      source_word: 91,
      end: 45.584667,
      duration: 5.74
    },
    {
      id: "p03-s03",
      paragraph: 3,
      anchor: "You put the snack down,",
      action: "set_snack",
      set: "kitchen",
      camera: "kitchen",
      start: 45.584667,
      source_word: 107,
      end: 47.224667,
      duration: 1.64
    },
    {
      id: "p03-s04",
      paragraph: 3,
      anchor: "crossed the room,",
      action: "walk_pull",
      set: "work",
      camera: "work",
      start: 47.224667,
      source_word: 112,
      end: 50.091333,
      duration: 2.866666
    },
    {
      id: "p04-s01",
      paragraph: 4,
      anchor: "You sent the reply.",
      action: "typing_reply",
      set: "work",
      camera: "work",
      start: 50.091333,
      source_word: 120,
      end: 53.991333,
      duration: 3.9
    },
    {
      id: "p04-s02",
      paragraph: 4,
      anchor: "Apparently",
      action: "inbox_overflow",
      set: "work",
      camera: "laptop",
      start: 53.991333,
      source_word: 127,
      end: 59.571333,
      duration: 5.58
    },
    {
      id: "p04-s03",
      paragraph: 4,
      anchor: "Now you needed",
      action: "file_check",
      set: "work",
      camera: "work_ots",
      start: 59.571333,
      source_word: 139,
      end: 64.071333,
      duration: 4.5
    },
    {
      id: "p04-s04",
      paragraph: 4,
      anchor: "Your movie",
      action: "empty_movie",
      set: "living",
      camera: "empty",
      start: 64.071333,
      source_word: 149,
      end: 67.391333,
      duration: 3.32
    },
    {
      id: "p04-s05",
      paragraph: 4,
      anchor: "The snack",
      action: "snack_cooling",
      set: "kitchen",
      camera: "snack",
      start: 67.391333,
      source_word: 159,
      end: 69.796667,
      duration: 2.405334
    },
    {
      id: "p05-s01",
      paragraph: 5,
      anchor: "Your phone rang.",
      action: "timer_insert",
      set: "work",
      camera: "timer",
      start: 69.796667,
      source_word: 164,
      end: 74.516667,
      duration: 4.72
    },
    {
      id: "p05-s02",
      paragraph: 5,
      anchor: "You had successfully",
      action: "missed_break",
      set: "work",
      camera: "face",
      start: 74.516667,
      source_word: 173,
      end: 79.036667,
      duration: 4.52
    },
    {
      id: "p05-s03",
      paragraph: 5,
      anchor: "You silenced",
      action: "alarm_off",
      set: "work",
      camera: "work_ots",
      start: 79.036667,
      source_word: 184,
      end: 82.896667,
      duration: 3.86
    },
    {
      id: "p05-s04",
      paragraph: 5,
      anchor: "Just finish this.",
      action: "reach_work",
      set: "work",
      camera: "work",
      start: 82.896667,
      source_word: 194,
      end: 88.139333,
      duration: 5.242666
    },
    {
      id: "p06-s01",
      paragraph: 6,
      anchor: "Then your friend",
      action: "friend_rest",
      set: "friend",
      camera: "friend",
      start: 88.139333,
      source_word: 205,
      end: 94.699333,
      duration: 6.56
    },
    {
      id: "p06-s02",
      paragraph: 6,
      anchor: "Your reply",
      action: "phone_reply",
      set: "work",
      camera: "face",
      start: 94.699333,
      source_word: 220,
      end: 101.279333,
      duration: 6.58
    },
    {
      id: "p06-s03",
      paragraph: 6,
      anchor: "A moment later,",
      action: "phone_question",
      set: "work",
      camera: "phone",
      start: 101.279333,
      source_word: 234,
      end: 104.639333,
      duration: 3.36
    },
    {
      id: "p06-s04",
      paragraph: 6,
      anchor: "You looked",
      action: "remote_insert",
      set: "living",
      camera: "remote",
      start: 104.639333,
      source_word: 242,
      end: 107.204667,
      duration: 2.565334
    },
    {
      id: "p07-s01",
      paragraph: 7,
      anchor: "You started typing:",
      action: "unsent_insert",
      set: "work",
      camera: "phone",
      start: 107.204667,
      source_word: 248,
      end: 110.184667,
      duration: 2.98
    },
    {
      id: "p07-s02",
      paragraph: 7,
      anchor: "Then stopped.",
      action: "thumb_stop",
      set: "work",
      camera: "phone",
      start: 110.184667,
      source_word: 255,
      end: 115.464667,
      duration: 5.28
    },
    {
      id: "p07-s03",
      paragraph: 7,
      anchor: "But looking",
      action: "realize",
      set: "work",
      camera: "face",
      start: 115.464667,
      source_word: 265,
      end: 119.484667,
      duration: 4.02
    },
    {
      id: "p07-s04",
      paragraph: 7,
      anchor: "Your friend could rest",
      action: "friend_kindness",
      set: "friend",
      camera: "friend",
      start: 119.484667,
      source_word: 277,
      end: 125.824667,
      duration: 6.34
    },
    {
      id: "p08-s01",
      paragraph: 8,
      anchor: "Maybe that's",
      action: "leave_desk",
      set: "work",
      camera: "work",
      start: 125.824667,
      source_word: 292,
      end: 129.624667,
      duration: 3.8
    },
    {
      id: "p08-s02",
      paragraph: 8,
      anchor: "If being useful",
      action: "useful_pause",
      set: "work",
      camera: "face",
      start: 129.624667,
      source_word: 300,
      end: 138.184667,
      duration: 8.56
    },
    {
      id: "p08-s03",
      paragraph: 8,
      anchor: "The document",
      action: "document_insert",
      set: "work",
      camera: "laptop",
      start: 138.184667,
      source_word: 318,
      end: 141.004667,
      duration: 2.82
    },
    {
      id: "p08-s04",
      paragraph: 8,
      anchor: "But can you",
      action: "hover_couch",
      set: "work",
      camera: "work",
      start: 141.004667,
      source_word: 324,
      end: 144.911333,
      duration: 3.906666
    },
    {
      id: "p09-s01",
      paragraph: 9,
      anchor: "Research has linked",
      action: "leisure",
      set: "friend",
      camera: "friend",
      start: 144.911333,
      source_word: 334,
      end: 150.891333,
      duration: 5.98
    },
    {
      id: "p09-s02",
      paragraph: 9,
      anchor: "That doesn't explain",
      action: "uneasy_movie",
      set: "living",
      camera: "face",
      start: 150.891333,
      source_word: 346,
      end: 153.831333,
      duration: 2.94
    },
    {
      id: "p09-s03",
      paragraph: 9,
      anchor: "In this story,",
      action: "inspection",
      set: "inspection",
      camera: "inspection",
      start: 153.831333,
      source_word: 351,
      end: 161.931333,
      duration: 8.1
    },
    {
      id: "p09-s04",
      paragraph: 9,
      anchor: "Imagine watching",
      action: "receipt",
      set: "inspection",
      camera: "receipt",
      start: 161.931333,
      source_word: 368,
      end: 166.344667,
      duration: 4.413334
    },
    {
      id: "p10-s01",
      paragraph: 10,
      anchor: "Sometimes the pressure",
      action: "boss",
      set: "work",
      camera: "work_ots",
      start: 166.344667,
      source_word: 379,
      end: 171.524667,
      duration: 5.18
    },
    {
      id: "p10-s02",
      paragraph: 10,
      anchor: "Housework isn't",
      action: "laundry",
      set: "living",
      camera: "living",
      start: 171.524667,
      source_word: 390,
      end: 175.024667,
      duration: 3.5
    },
    {
      id: "p10-s03",
      paragraph: 10,
      anchor: "Someone depends",
      action: "care",
      set: "friend",
      camera: "friend",
      start: 175.024667,
      source_word: 394,
      end: 181.424667,
      duration: 6.4
    },
    {
      id: "p10-s04",
      paragraph: 10,
      anchor: "But tonight,",
      action: "urgent_done",
      set: "work",
      camera: "work",
      start: 181.424667,
      source_word: 406,
      end: 187.948667,
      duration: 6.524
    },
    {
      id: "p11-s01",
      paragraph: 11,
      anchor: "You look",
      action: "document_insert",
      set: "work",
      camera: "laptop",
      start: 187.948667,
      source_word: 422,
      end: 191.988667,
      duration: 4.04
    },
    {
      id: "p11-s02",
      paragraph: 11,
      anchor: "You write yourself",
      action: "write_note",
      set: "work",
      camera: "note",
      start: 191.988667,
      source_word: 431,
      end: 196.348667,
      duration: 4.36
    },
    {
      id: "p11-s03",
      paragraph: 11,
      anchor: "Then you close",
      action: "close_laptop",
      set: "work",
      camera: "work_ots",
      start: 196.348667,
      source_word: 441,
      end: 198.428667,
      duration: 2.08
    },
    {
      id: "p11-s04",
      paragraph: 11,
      anchor: "You take the snack",
      action: "pickup_snack",
      set: "kitchen",
      camera: "kitchen",
      start: 198.428667,
      source_word: 446,
      end: 199.288667,
      duration: 0.86
    },
    {
      id: "p11-s05",
      paragraph: 11,
      anchor: "back to the couch.",
      action: "walk_snack",
      set: "living",
      camera: "living",
      start: 199.288667,
      source_word: 450,
      end: 201.248667,
      duration: 1.96
    },
    {
      id: "p11-s06",
      paragraph: 11,
      anchor: "This time,",
      action: "sit_play",
      set: "living",
      camera: "living",
      start: 201.248667,
      source_word: 454,
      end: 206.032667,
      duration: 4.784
    },
    {
      id: "p12-s01",
      paragraph: 12,
      anchor: "And right then,",
      action: "keys",
      set: "entry",
      camera: "key",
      start: 206.032667,
      source_word: 465,
      end: 210.912667,
      duration: 4.88
    },
    {
      id: "p12-s02",
      paragraph: 12,
      anchor: "The familiar thought",
      action: "startle",
      set: "living",
      camera: "living",
      start: 210.912667,
      source_word: 476,
      end: 214.212667,
      duration: 3.3
    },
    {
      id: "p12-s03",
      paragraph: 12,
      anchor: "You hurry",
      action: "hurry",
      set: "kitchen",
      camera: "kitchen",
      start: 214.212667,
      source_word: 482,
      end: 218.452667,
      duration: 4.24
    },
    {
      id: "p12-s04",
      paragraph: 12,
      anchor: "Under the running water,",
      action: "wash",
      set: "kitchen",
      camera: "plate",
      start: 218.452667,
      source_word: 495,
      end: 223.714,
      duration: 5.261333
    },
    {
      id: "p13-s01",
      paragraph: 13,
      anchor: "Your roommate walks in.",
      action: "roommate_arrive",
      set: "kitchen",
      camera: "kitchen",
      start: 223.714,
      source_word: 507,
      end: 227.794,
      duration: 4.08
    },
    {
      id: "p13-s02",
      paragraph: 13,
      anchor: "You almost say",
      action: "almost_excuse",
      set: "kitchen",
      camera: "face",
      start: 227.794,
      source_word: 516,
      end: 230.274,
      duration: 2.48
    },
    {
      id: "p13-s03",
      paragraph: 13,
      anchor: "Instead,",
      action: "faucet_off",
      set: "kitchen",
      camera: "sink",
      start: 230.274,
      source_word: 524,
      end: 234.554,
      duration: 4.28
    },
    {
      id: "p13-s04",
      paragraph: 13,
      anchor: "Your mouth",
      action: "honest",
      set: "kitchen",
      camera: "face",
      start: 234.554,
      source_word: 534,
      end: 241.608667,
      duration: 7.054667
    },
    {
      id: "p14-s01",
      paragraph: 14,
      anchor: "Any good?",
      action: "roommate_question",
      set: "kitchen",
      camera: "buddy_face",
      start: 241.608667,
      source_word: 550,
      end: 245.968667,
      duration: 4.36
    },
    {
      id: "p14-s02",
      paragraph: 14,
      anchor: "You sit back down.",
      action: "sit_back",
      set: "living",
      camera: "living",
      start: 245.968667,
      source_word: 563,
      end: 247.768667,
      duration: 1.8
    },
    {
      id: "p14-s03",
      paragraph: 14,
      anchor: "Your roommate takes",
      action: "snack_grab",
      set: "living",
      camera: "living",
      start: 247.768667,
      source_word: 567,
      end: 251.848667,
      duration: 4.08
    },
    {
      id: "p14-s04",
      paragraph: 14,
      anchor: "That's it.",
      action: "find_place",
      set: "living",
      camera: "remote",
      start: 251.848667,
      source_word: 580,
      end: 257.559333,
      duration: 5.710666
    },
    {
      id: "p15-s01",
      paragraph: 15,
      anchor: "The guilt hasn't",
      action: "still_guilty",
      set: "living",
      camera: "face",
      start: 257.559333,
      source_word: 593,
      end: 263.159333,
      duration: 5.6
    },
    {
      id: "p15-s02",
      paragraph: 15,
      anchor: "But this time,",
      action: "stay",
      set: "living",
      camera: "living",
      start: 263.159333,
      source_word: 602,
      end: 267.439333,
      duration: 4.28
    },
    {
      id: "p15-s03",
      paragraph: 15,
      anchor: "You let the movie",
      action: "watch",
      set: "living",
      camera: "face",
      start: 267.439333,
      source_word: 614,
      end: 270.239333,
      duration: 2.8
    },
    {
      id: "p15-s04",
      paragraph: 15,
      anchor: "And you let someone",
      action: "rest_end",
      set: "living",
      camera: "living",
      start: 270.239333,
      source_word: 621,
      end: 277.1666666666667,
      duration: 6.927334
    }
  ]
};

// engines/hyperframes-clay3d/films/rest-guilt-v1/assets/captions.json
var captions_default = [
  {
    start: 0.25,
    end: 2.16,
    text: "Why does resting in your own home",
    id: 1
  },
  {
    start: 2.17,
    end: 3.74,
    text: "feel like getting caught?",
    id: 2
  },
  {
    start: 3.75,
    end: 6.8,
    text: "Picture this. You hear keys at the",
    id: 3
  },
  {
    start: 6.81,
    end: 9.3,
    text: "front door. A second ago, you were",
    id: 4
  },
  {
    start: 9.31,
    end: 10.36,
    text: "watching a movie.",
    id: 5
  },
  {
    start: 10.37,
    end: 12.44,
    text: "Now you're washing a plate.",
    id: 6
  },
  {
    start: 12.45,
    end: 14.729999999999999,
    text: "The plate was already clean.",
    id: 7
  },
  {
    start: 15.862,
    end: 18.542,
    text: "An hour earlier, this evening looked different.",
    id: 8
  },
  {
    start: 19.042,
    end: 20.042,
    text: "Dinner was done.",
    id: 9
  },
  {
    start: 20.742,
    end: 22.342000000000002,
    text: "The urgent stuff was handled.",
    id: 10
  },
  {
    start: 23.042,
    end: 25.902,
    text: "You texted a friend: finally, movie time.",
    id: 11
  },
  {
    start: 26.522,
    end: 28.602,
    text: "You made a snack, found the remote,",
    id: 12
  },
  {
    start: 28.802,
    end: 30.402,
    text: "and gave yourself twenty minutes.",
    id: 13
  },
  {
    start: 31.142,
    end: 33.052,
    text: "Then you noticed your laptop was still",
    id: 14
  },
  {
    start: 33.062,
    end: 33.582,
    text: "open.",
    id: 15
  },
  {
    start: 34.244667,
    end: 35.844666999999994,
    text: "One unanswered email.",
    id: 16
  },
  {
    start: 36.564667,
    end: 38.164666999999994,
    text: "It could wait until tomorrow.",
    id: 17
  },
  {
    start: 38.704667,
    end: 39.324667,
    text: "You knew that.",
    id: 18
  },
  {
    start: 39.884667,
    end: 41.844666999999994,
    text: "But answering it would take two minutes.",
    id: 19
  },
  {
    start: 42.644667,
    end: 44.434667,
    text: "Then you could relax without it hanging",
    id: 20
  },
  {
    start: 44.444666999999995,
    end: 47.06466699999999,
    text: "over you. You put the snack down,",
    id: 21
  },
  {
    start: 47.264667,
    end: 49.074667,
    text: "crossed the room, and pulled the chair",
    id: 22
  },
  {
    start: 49.084666999999996,
    end: 49.544667,
    text: "out.",
    id: 23
  },
  {
    start: 50.131333,
    end: 51.19133299999999,
    text: "You sent the reply.",
    id: 24
  },
  {
    start: 52.011333,
    end: 53.091333,
    text: "Another message arrived.",
    id: 25
  },
  {
    start: 54.031333,
    end: 56.69133299999999,
    text: "Apparently your inbox had learned to reproduce.",
    id: 26
  },
  {
    start: 57.671333,
    end: 59.031333,
    text: "You opened that one too.",
    id: 27
  },
  {
    start: 59.611333,
    end: 61.131333,
    text: "Now you needed a document.",
    id: 28
  },
  {
    start: 61.691333,
    end: 63.37133299999999,
    text: "The document needed a correction.",
    id: 29
  },
  {
    start: 64.111333,
    end: 65.98133299999999,
    text: "Your movie was still waiting for you",
    id: 30
  },
  {
    start: 65.991333,
    end: 66.831333,
    text: "to press play.",
    id: 31
  },
  {
    start: 67.431333,
    end: 68.951333,
    text: "The snack was getting cold.",
    id: 32
  },
  {
    start: 69.836667,
    end: 71.01666700000001,
    text: "Your phone rang.",
    id: 33
  },
  {
    start: 71.836667,
    end: 72.31666700000001,
    text: "The timer.",
    id: 34
  },
  {
    start: 72.89666700000001,
    end: 74.03666700000001,
    text: "Twenty minutes were up.",
    id: 35
  },
  {
    start: 74.556667,
    end: 76.826667,
    text: "You had successfully completed your break without",
    id: 36
  },
  {
    start: 76.836667,
    end: 78.63666700000002,
    text: "experiencing any of it.",
    id: 37
  },
  {
    start: 79.076667,
    end: 81.266667,
    text: "You silenced the alarm and reached for",
    id: 38
  },
  {
    start: 81.276667,
    end: 82.276667,
    text: "the laptop again.",
    id: 39
  },
  {
    start: 82.936667,
    end: 83.95666700000001,
    text: "Just finish this.",
    id: 40
  },
  {
    start: 84.576667,
    end: 86.686667,
    text: "Then you could finally stop thinking about",
    id: 41
  },
  {
    start: 86.696667,
    end: 87.21666700000002,
    text: "work.",
    id: 42
  },
  {
    start: 88.179333,
    end: 89.399333,
    text: "Then your friend texted.",
    id: 43
  },
  {
    start: 90.359333,
    end: 92.789333,
    text: "They'd spent the afternoon lying around and",
    id: 44
  },
  {
    start: 92.799333,
    end: 94.299333,
    text: "felt terrible about it.",
    id: 45
  },
  {
    start: 94.739333,
    end: 97.55933300000001,
    text: "Your reply came easily: you were exhausted.",
    id: 46
  },
  {
    start: 98.459333,
    end: 99.27933300000001,
    text: "You needed a break.",
    id: 47
  },
  {
    start: 99.919333,
    end: 100.61933300000001,
    text: "You hit send.",
    id: 48
  },
  {
    start: 101.319333,
    end: 102.77933300000001,
    text: "A moment later, they asked:",
    id: 49
  },
  {
    start: 103.279333,
    end: 104.299333,
    text: "how's the movie?",
    id: 50
  },
  {
    start: 104.679333,
    end: 106.459333,
    text: "You looked at the untouched remote.",
    id: 51
  },
  {
    start: 107.244667,
    end: 109.684667,
    text: "You started typing: haven't earned it yet.",
    id: 52
  },
  {
    start: 110.22466700000001,
    end: 110.66466700000001,
    text: "Then stopped.",
    id: 53
  },
  {
    start: 111.604667,
    end: 113.08466700000001,
    text: "You wouldn't actually send that.",
    id: 54
  },
  {
    start: 113.38466700000001,
    end: 114.58466700000001,
    text: "It sounded ridiculous.",
    id: 55
  },
  {
    start: 115.50466700000001,
    end: 117.494667,
    text: "But looking at your evening, wasn't that",
    id: 56
  },
  {
    start: 117.50466700000001,
    end: 119.044667,
    text: "the rule you were following?",
    id: 57
  },
  {
    start: 119.52466700000001,
    end: 121.534667,
    text: "Your friend could rest because they were",
    id: 58
  },
  {
    start: 121.544667,
    end: 122.12466700000002,
    text: "tired.",
    id: 59
  },
  {
    start: 122.844667,
    end: 124.88466700000001,
    text: "You needed evidence that you'd done enough.",
    id: 60
  },
  {
    start: 125.864667,
    end: 127.81466699999999,
    text: "Maybe that's part of what makes rest",
    id: 61
  },
  {
    start: 127.82466699999999,
    end: 128.724667,
    text: "uncomfortable.",
    id: 62
  },
  {
    start: 129.664667,
    end: 131.694667,
    text: "If being useful has become a condition",
    id: 63
  },
  {
    start: 131.704667,
    end: 134.044667,
    text: "for feeling okay about yourself,",
    id: 64
  },
  {
    start: 134.704667,
    end: 137.464667,
    text: "an unfinished task can feel personal.",
    id: 65
  },
  {
    start: 138.224667,
    end: 140.444667,
    text: "The document can wait until morning.",
    id: 66
  },
  {
    start: 141.044667,
    end: 143.074667,
    text: "But can you feel okay about yourself",
    id: 67
  },
  {
    start: 143.084667,
    end: 144.144667,
    text: "while it waits?",
    id: 68
  },
  {
    start: 144.951333,
    end: 147.90133300000002,
    text: "Research has linked seeing leisure as wasted",
    id: 69
  },
  {
    start: 147.911333,
    end: 150.09133300000002,
    text: "time with enjoying it less.",
    id: 70
  },
  {
    start: 150.931333,
    end: 153.131333,
    text: "That doesn't explain everyone's guilt.",
    id: 71
  },
  {
    start: 153.871333,
    end: 156.56133300000002,
    text: "In this story, though, every attempt to",
    id: 72
  },
  {
    start: 156.571333,
    end: 158.37133300000002,
    text: "relax comes with an inspection:",
    id: 73
  },
  {
    start: 159.171333,
    end: 160.831333,
    text: "have I justified this yet?",
    id: 74
  },
  {
    start: 161.97133300000002,
    end: 164.18133300000002,
    text: "Imagine watching a movie while somebody keeps",
    id: 75
  },
  {
    start: 164.19133300000001,
    end: 165.611333,
    text: "asking for your receipt.",
    id: 76
  },
  {
    start: 166.384667,
    end: 168.664667,
    text: "Sometimes the pressure comes from outside.",
    id: 77
  },
  {
    start: 169.604667,
    end: 171.55466700000002,
    text: "A boss expects evening replies.",
    id: 78
  },
  {
    start: 171.56466700000001,
    end: 174.30466700000002,
    text: "Housework isn't shared fairly.",
    id: 79
  },
  {
    start: 175.06466700000001,
    end: 176.56466700000001,
    text: "Someone depends on you.",
    id: 80
  },
  {
    start: 177.06466700000001,
    end: 179.87466700000002,
    text: "Those situations may need practical help or",
    id: 81
  },
  {
    start: 179.884667,
    end: 180.46466700000002,
    text: "boundaries.",
    id: 82
  },
  {
    start: 181.46466700000002,
    end: 183.62466700000002,
    text: "But tonight, the urgent work is done.",
    id: 83
  },
  {
    start: 184.584667,
    end: 186.254667,
    text: "Nobody has asked you to open that",
    id: 84
  },
  {
    start: 186.264667,
    end: 187.30466700000002,
    text: "laptop again.",
    id: 85
  },
  {
    start: 187.988667,
    end: 189.24866699999998,
    text: "You look at the document.",
    id: 86
  },
  {
    start: 190.068667,
    end: 191.288667,
    text: "One correction can wait.",
    id: 87
  },
  {
    start: 192.02866699999998,
    end: 194.058667,
    text: "You write yourself a note: fix this",
    id: 88
  },
  {
    start: 194.068667,
    end: 195.52866699999998,
    text: "tomorrow after breakfast.",
    id: 89
  },
  {
    start: 196.388667,
    end: 197.608667,
    text: "Then you close the laptop.",
    id: 90
  },
  {
    start: 198.46866699999998,
    end: 200.018667,
    text: "You take the snack back to the",
    id: 91
  },
  {
    start: 200.02866699999998,
    end: 200.508667,
    text: "couch.",
    id: 92
  },
  {
    start: 201.288667,
    end: 203.818667,
    text: "This time, you press play before finding",
    id: 93
  },
  {
    start: 203.828667,
    end: 205.268667,
    text: "another reason to leave.",
    id: 94
  },
  {
    start: 206.072667,
    end: 207.982667,
    text: "And right then, keys turn in the",
    id: 95
  },
  {
    start: 207.99266699999998,
    end: 208.372667,
    text: "door.",
    id: 96
  },
  {
    start: 209.032667,
    end: 210.072667,
    text: "Your shoulders tighten.",
    id: 97
  },
  {
    start: 210.952667,
    end: 212.332667,
    text: "The familiar thought arrives:",
    id: 98
  },
  {
    start: 213.032667,
    end: 213.452667,
    text: "look busy.",
    id: 99
  },
  {
    start: 214.252667,
    end: 215.902667,
    text: "You hurry to the sink and grab",
    id: 100
  },
  {
    start: 215.912667,
    end: 217.83266700000001,
    text: "a plate from the drying rack.",
    id: 101
  },
  {
    start: 218.49266699999998,
    end: 220.592667,
    text: "Under the running water, you notice it.",
    id: 102
  },
  {
    start: 221.012667,
    end: 222.572667,
    text: "This plate was already clean.",
    id: 103
  },
  {
    start: 223.754,
    end: 225.314,
    text: "Your roommate walks in.",
    id: 104
  },
  {
    start: 225.914,
    end: 227.194,
    text: "Hey. How was your night?",
    id: 105
  },
  {
    start: 227.834,
    end: 229.464,
    text: "You almost say you were just cleaning",
    id: 106
  },
  {
    start: 229.474,
    end: 232.414,
    text: "up. Instead, you turn off the faucet.",
    id: 107
  },
  {
    start: 232.834,
    end: 234.014,
    text: "Set the plate down.",
    id: 108
  },
  {
    start: 234.594,
    end: 236.754,
    text: "Your mouth starts forming an explanation.",
    id: 109
  },
  {
    start: 237.654,
    end: 238.79399999999998,
    text: "You let that go too.",
    id: 110
  },
  {
    start: 239.314,
    end: 240.73399999999998,
    text: "I was watching a movie.",
    id: 111
  },
  {
    start: 241.648667,
    end: 243.368667,
    text: "Any good? You shake your head.",
    id: 112
  },
  {
    start: 243.608667,
    end: 244.30866699999999,
    text: "You don't know yet.",
    id: 113
  },
  {
    start: 244.56866699999998,
    end: 245.588667,
    text: "You've barely started.",
    id: 114
  },
  {
    start: 246.008667,
    end: 247.068667,
    text: "You sit back down.",
    id: 115
  },
  {
    start: 247.80866699999999,
    end: 249.478667,
    text: "Your roommate takes a piece of your",
    id: 116
  },
  {
    start: 249.488667,
    end: 251.30866699999999,
    text: "snack and heads down the hall.",
    id: 117
  },
  {
    start: 251.888667,
    end: 252.52866699999998,
    text: "That's it.",
    id: 118
  },
  {
    start: 253.208667,
    end: 253.928667,
    text: "No inspection.",
    id: 119
  },
  {
    start: 254.668667,
    end: 256.238667,
    text: "You pick up the remote and find",
    id: 120
  },
  {
    start: 256.248667,
    end: 256.908667,
    text: "your place.",
    id: 121
  },
  {
    start: 257.599333,
    end: 259.899333,
    text: "The guilt hasn't magically disappeared.",
    id: 122
  },
  {
    start: 260.859333,
    end: 262.499333,
    text: "Neither has tomorrow's work.",
    id: 123
  },
  {
    start: 263.199333,
    end: 264.789333,
    text: "But this time, you stay for the",
    id: 124
  },
  {
    start: 264.799333,
    end: 265.499333,
    text: "next scene.",
    id: 125
  },
  {
    start: 266.119333,
    end: 266.87933300000003,
    text: "Then the next.",
    id: 126
  },
  {
    start: 267.479333,
    end: 269.539333,
    text: "You let the movie hold your attention.",
    id: 127
  },
  {
    start: 270.279333,
    end: 272.019333,
    text: "And you let someone see you resting,",
    id: 128
  },
  {
    start: 272.299333,
    end: 273.709333,
    text: "without trying to make it look like",
    id: 129
  },
  {
    start: 273.719333,
    end: 274.499333,
    text: "something else.",
    id: 130
  }
];

// engines/hyperframes-clay3d/films/rest-guilt-v1/src/main.mjs
var canvas = document.getElementById("film-canvas");
var renderer = new THREE3.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, powerPreference: "low-power" });
renderer.setPixelRatio(1);
renderer.setSize(1920, 1080, false);
renderer.outputColorSpace = THREE3.SRGBColorSpace;
renderer.toneMapping = THREE3.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.02;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE3.PCFShadowMap;
var stage;
var buddy;
var world;
var lastTime = -1;
var debug = {};
var gl = renderer.getContext();
var pixel = new Uint8Array(4);
var captionElements = [...document.querySelectorAll(".caption-body")];
var V = (p) => new THREE3.Vector3(...p);
function chooseShot(t) {
  return timeline_default.shots.find((s) => t >= s.start && t < s.end) || timeline_default.shots.at(-1);
}
function cameraFor(state, shot) {
  const camera = stage.camera;
  let position, target, width;
  const root = state.hero.actor.position;
  const settings = {
    living: [[6.3, 4.4, 9.4], [0, 1.1, 0], 9.6],
    work: [[4.6, 3.5, 5.5], [0, 1.05, 0.4], 6.5],
    work_ots: [[2.6, 3.1, -3.6], [0, 1.18, 0.55], 4.4],
    kitchen: [[5.4, 3.8, 7.2], [0.1, 1.12, 0.8], 7.4],
    sink: [[-3, 3.1, 4.8], [-0.15, 1.3, 1.02], 4.9],
    plate: [[0.9, 2.4, 3.7], [-0.12, 1.22, 1.12], 2],
    friend: [[4, 3.2, 5.8], [0, 1.08, 0.1], 6.1],
    inspection: [[4.5, 3.1, 6.4], [0, 1.16, 0.7], 6.7],
    receipt: [[1, 2.1, 4], [0.05, 1.32, 0.87], 2.25],
    key: [[1.4, 1.7, 1.3], [0.5, 1.2, -1.3], 1.5],
    phone: [[0, 1.5, 5.1], [0, 1.5, 2.5], 1.1],
    timer: [[1.6, 2.7, 1.3], [0.7, 1, 0.55], 1.1],
    snack: [[-0.2, 2.1, 3.2], [-1.35, 1.2, 1.12], 1.7],
    laptop: [[1, 2.05, -2.8], [0, 1.27, 0.95], 2.3],
    note: [[0.92, 3, 0.9], [0.92, 0.93, 0.57], 1.3],
    empty: [[5, 3.5, 6.6], [2.1, 1.05, 0.2], 6],
    remote: [[2.2, 1.8, 2.8], [1.62, 0.84, 0.7], 1.2]
  };
  if (shot.camera === "face") {
    const y = state.set === "living" ? 0.84 : state.set === "work" && ["leave_desk", "hover_couch"].includes(state.action) ? 1.18 : state.set === "work" ? 0.83 : 1.18;
    target = [root[0], y + 0.72, root[2] + 0.08];
    position = [root[0] + 2.6, y + 1.75, root[2] + 4.7];
    width = 3.35;
  } else if (shot.camera === "buddy_face") {
    const b = state.buddy.actor.position;
    target = [b[0], b[1] + 0.76, b[2]];
    position = [b[0] - 2.1, b[1] + 1.6, b[2] + 4.7];
    width = 3.35;
  } else [position, target, width] = settings[shot.camera] || settings[state.set] || settings.living;
  camera.left = -width / 2;
  camera.right = width / 2;
  camera.top = width * 9 / 32;
  camera.bottom = -width * 9 / 32;
  camera.position.set(...position);
  camera.lookAt(...target);
  camera.updateProjectionMatrix();
  camera.updateMatrixWorld(true);
  world.prop.workFrontWall.visible = position[2] < 1.85;
  world.prop.workBackWall.visible = position[2] > -1.85;
}
function applyProps(state) {
  world.prop.chair.position.z = state.chairZ;
  world.prop.lid.rotation.x = state.lidAngle;
  for (const [name, config] of Object.entries(state.props)) {
    const object = world.prop[name];
    if (!object) continue;
    object.visible = config.visible !== false;
    object.position.set(...config.position);
    object.rotation.set(...config.rotation || [0, 0, 0]);
    object.scale.setScalar(config.scale ?? 1);
  }
  world.prop.water.visible = state.water;
  world.prop.valve.rotation.y = state.water ? 0 : -0.8;
  world.prop.insertHands.visible = !!state.insertHands;
  if (state.insertHands) {
    world.prop.phone.position.set(0, 1.54, 2.5);
    state.props.phone.position = [0, 1.54, 2.5];
    world.prop.insertHands.position.copy(world.prop.phone.position);
    world.prop.insertFinger.position.x = 0.105 + 9e-3 * Math.sin(state.progress * 12);
  }
  world.prop.keyHand.visible = !!state.keyHand;
  if (state.keyHand) {
    world.prop.keyHand.rotation.z = 0.4 * Math.sin(Math.PI * state.progress);
  }
  const a = state.action;
  if (state.props.phone) world.phoneText(state.message || "How's the movie?", state.draft || "", state.phoneMode || "message", state.phoneProgress ?? state.progress);
  world.laptopText(state.laptopMode || (["document_insert", "write_note", "close_laptop"].includes(a) ? "document" : "email"), state.progress);
  if (a === "write_note") world.noteText(state.noteProgress);
  else world.noteText(1);
  const mood = state.mood;
  stage.objects.mouth.scale.y = 1;
  stage.objects.mouth.position.y = 0;
  if (mood === "guilty") {
    stage.objects.brows[0].rotation.z = 0.22;
    stage.objects.brows[1].rotation.z = -0.22;
    stage.objects.head.rotation.z = 0.04;
    stage.objects.mouth.scale.y = -1;
    stage.objects.mouth.position.y = -0.26;
    stage.objects.mouth.material.opacity = 1;
    stage.objects.smile.material.opacity = 0;
  }
  if (mood === "recognition") {
    stage.objects.brows[0].rotation.z = -0.12;
    stage.objects.brows[1].rotation.z = 0.08;
  }
  for (const [rig, pose2] of [[stage, state.hero], [buddy, state.buddy]]) {
    const [x, , z] = pose2.actor.position, focus = pose2.ball.position;
    let angle = Math.atan2(focus[0] - x, focus[2] - z) - pose2.actor.yaw;
    while (angle > Math.PI) angle -= Math.PI * 2;
    while (angle < -Math.PI) angle += Math.PI * 2;
    rig.objects.head.rotation.y = Math.max(-0.55, Math.min(0.55, angle));
  }
  if (state.action === "roommate_question") stage.objects.head.rotation.y += 0.1 * Math.sin(state.progress * Math.PI * 4);
}
function updateScene(seconds, { draw = true } = {}) {
  const t = Math.min(timeline_default.duration - 1 / 240, Math.max(0, Math.floor((seconds + 1e-7) * 12) / 12));
  const shot = chooseShot(t), state = frameState(shot, t);
  world.show(state.set);
  stage.actorObjects.forEach((o) => {
    o.visible = state.heroVisible;
  });
  buddy.actorObjects.forEach((o) => {
    o.visible = state.buddyVisible;
  });
  buddy.materials.vest.color.set(state.role === "friend" ? "#5b7e94" : state.role === "clerk" ? "#686a7d" : "#526d92");
  buddy.materials.hair.color.set(state.role === "friend" ? "#795342" : "#453e39");
  stage.update(state.hero);
  buddy.update(state.buddy);
  stage.objects.ball.visible = false;
  buddy.objects.ball.visible = false;
  applyProps(state);
  cameraFor(state, shot);
  stage.scene.updateMatrixWorld(true);
  const active = state.set === "friend" || state.action === "boss" || state.action === "laundry" ? buddy : stage;
  const relevant = shot.camera === "face" || shot.camera === "buddy_face" ? ["head", "leftShoulder", "rightShoulder"] : ["leftHand", "rightHand", "head"];
  const joints = { hero: stage.debug.joints, buddy: buddy.debug.joints };
  const reachable = [];
  if (state.heroVisible) reachable.push(...stage.debug.reaches.map((r) => ({ ...r, who: "hero" })));
  if (state.buddyVisible) reachable.push(...buddy.debug.reaches.map((r) => ({ ...r, who: "buddy" })));
  const captionsActive = [];
  captions_default.forEach((cue, i) => {
    const visible = t >= cue.start && t < cue.end;
    captionElements[i].style.opacity = visible ? "1" : "0";
    if (visible) captionsActive.push(cue.id);
  });
  const tag = document.getElementById("flashback-tag");
  tag.style.opacity = shot.paragraph === 2 && shot.action === "dinner_done" ? "1" : "0";
  const projected = Object.fromEntries(relevant.filter((k) => active.debug.joints[k]).map((k) => [k, V(active.debug.joints[k]).project(stage.camera).toArray()]));
  debug = { t, shot: shot.id, paragraph: shot.paragraph, action: state.action, set: state.set, camera: shot.camera, heroVisible: state.heroVisible, buddyVisible: state.buddyVisible, reachable, joints, projected, props: state.props, water: state.water, captionsActive, feet: { hero: state.hero.actor, buddy: state.buddy.actor } };
  if (draw) {
    renderer.render(stage.scene, stage.camera);
    gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, pixel);
    lastTime = t;
  }
  return debug;
}
var ready = (async () => {
  await document.fonts.load("700 50px Nunito");
  stage = makeScene(renderer);
  buddy = makeScene(renderer);
  for (const object of buddy.actorObjects) stage.scene.add(object);
  world = createWorld(stage);
  const keyHand = new THREE3.Group();
  world.groups.entry.add(keyHand);
  world.prop.keyHand = keyHand;
  keyHand.position.set(0.595, 1.135, -1.1);
  stage.helpers.ellipsoid(keyHand, stage.materials.skin, [0, 0, 0], [0.06, 0.065, 0.055]);
  stage.helpers.box(keyHand, stage.materials.cream, [0.18, -0.04, 0], [0.28, 0.11, 0.11], 0.04);
  stage.scene.traverse((o) => {
    if (o.isDirectionalLight && o.castShadow) o.shadow.mapSize.set(768, 768);
  });
  updateScene(0, { draw: false });
  renderer.compile(stage.scene, stage.camera);
  updateScene(0);
})();
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__hf.buildReady["rest-film"] = ready;
window.addEventListener("hf-seek", (event) => {
  const work = ready.then(() => updateScene(event.detail.time));
  event.detail.waitUntil?.(work);
});
window.__restFilm = {
  ready,
  timeline: timeline_default,
  seek: async (t) => {
    await ready;
    return JSON.parse(JSON.stringify(updateScene(t)));
  },
  audit: async () => {
    await ready;
    const prior = lastTime;
    const errors = [], landings = [];
    let samples = 0, previous = null;
    for (let frame = 0; frame < Math.round(timeline_default.duration * 12); frame++) {
      const d = updateScene(frame / 12, { draw: false });
      samples++;
      for (const r of d.reachable) if (r.armError > 0.015 || r.footError > 0.015) errors.push({ t: d.t, shot: d.shot, action: d.action, ...r });
      if (previous && previous.shot === d.shot) {
        for (const who of ["hero", "buddy"]) if (d[who + "Visible"]) {
          for (const side of ["left", "right"]) if (previous.feet[who][side].moving && !d.feet[who][side].moving) landings.push({ time: d.t + 1 / 30, who, side, shot: d.shot });
        }
      }
      previous = d;
    }
    updateScene(prior);
    return { samples, errors, landings };
  },
  diagnostics: () => ({ webgl: gl.getParameter(gl.VERSION), width: 1920, height: 1080, calls: renderer.info.render.calls })
};
