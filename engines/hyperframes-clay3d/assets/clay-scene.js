// src/main.mjs
import * as THREE2 from "./vendor/three.min.js";

// src/scene.mjs
import * as THREE from "./vendor/three.min.js";

// node_modules/three/examples/jsm/geometries/RoundedBoxGeometry.js
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
  constructor(width2 = 1, height2 = 1, depth = 1, segments = 2, radius = 0.1) {
    const totalSegments = segments * 2 + 1;
    radius = Math.min(width2 / 2, height2 / 2, depth / 2, radius);
    super(1, 1, 1, totalSegments, totalSegments, totalSegments);
    this.type = "RoundedBoxGeometry";
    this.parameters = {
      width: width2,
      height: height2,
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
    const box = new Vector3(width2, height2, depth).divideScalar(2).subScalar(radius);
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
          uvs[j + 1] = 1 - getUv(faceDirVector, normal, "y", "z", radius, height2);
          break;
        case 1:
          faceDirVector.set(-1, 0, 0);
          uvs[j + 0] = 1 - getUv(faceDirVector, normal, "z", "y", radius, depth);
          uvs[j + 1] = 1 - getUv(faceDirVector, normal, "y", "z", radius, height2);
          break;
        case 2:
          faceDirVector.set(0, 1, 0);
          uvs[j + 0] = 1 - getUv(faceDirVector, normal, "x", "z", radius, width2);
          uvs[j + 1] = getUv(faceDirVector, normal, "z", "x", radius, depth);
          break;
        case 3:
          faceDirVector.set(0, -1, 0);
          uvs[j + 0] = 1 - getUv(faceDirVector, normal, "x", "z", radius, width2);
          uvs[j + 1] = 1 - getUv(faceDirVector, normal, "z", "x", radius, depth);
          break;
        case 4:
          faceDirVector.set(0, 0, 1);
          uvs[j + 0] = 1 - getUv(faceDirVector, normal, "x", "y", radius, width2);
          uvs[j + 1] = 1 - getUv(faceDirVector, normal, "y", "x", radius, height2);
          break;
        case 5:
          faceDirVector.set(0, 0, -1);
          uvs[j + 0] = getUv(faceDirVector, normal, "x", "y", radius, width2);
          uvs[j + 1] = 1 - getUv(faceDirVector, normal, "y", "x", radius, height2);
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

// src/motion.mjs
var DURATION = 15;
var CLAY_HZ = 12;
var RELEASE = 8.65;
var CATCH = 9.9;
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
var localPoint = (root2, xyz) => add(root2.position, rotateY(xyz, root2.yaw));
function solveTwoBone(origin, target, pole, upper, lower) {
  const delta = sub(target, origin);
  const raw = length(delta);
  const d = clamp(raw, Math.abs(upper - lower) + 1e-6, upper + lower - 1e-6);
  const direction = normalized(delta);
  const perpendicular = sub(pole, mul(direction, dot(pole, direction)));
  const side = normalized(length(perpendicular) < 1e-6 ? [0, 0, 1] : perpendicular);
  const along = (upper * upper - lower * lower + d * d) / (2 * d);
  const height2 = Math.sqrt(Math.max(0, upper * upper - along * along));
  return { joint: add(add(origin, mul(direction, along)), mul(side, height2)), end: add(origin, mul(direction, d)), requestedDistance: raw, reachable: raw < upper + lower };
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
var FLOOR_BALL = [0.4, 0.17, 1.05];
function heldBall(t, actor = actorAt(t)) {
  const inspect = ease(t, 6.8, 7.4) * (1 - ease(t, 7.7, 8.2));
  return localPoint(actor, [0.44 * (1 - actor.sitting), 0.32 + 0.23 * inspect - 0.17 * actor.sitting, 0.35]);
}
function ballAt(t, actor = actorAt(t)) {
  if (t < 5.65) return { position: [...FLOOR_BALL], held: false, phase: "floor" };
  if (t < 6.65) return { position: mix(FLOOR_BALL, heldBall(t, actor), ease(t, 5.65, 6.65)), held: true, phase: "lift" };
  if (t >= RELEASE && t < CATCH) {
    const u = (t - RELEASE) / (CATCH - RELEASE);
    const position = mix(heldBall(RELEASE), heldBall(CATCH), u);
    position[1] += 4 * 1.5 * u * (1 - u);
    return { position, held: false, phase: "flight" };
  }
  return { position: heldBall(t, actor), held: true, phase: "held" };
}
function poseAt(seconds, { stepped = true } = {}) {
  const time = clamp(seconds, 0, DURATION);
  const t = stepped ? Math.floor((time + 1e-7) * CLAY_HZ) / CLAY_HZ : time;
  const actor = actorAt(t);
  const ball = ballAt(t, actor);
  const walking = actor.left.moving || actor.right.moving;
  const swing = Math.sin(t * Math.PI * 2 / 1.1);
  const restRight = localPoint(actor, [0.39, 0.08, 0.12 + (walking ? 0.24 * swing : 0)]);
  const grip = add(ball.position, rotateY([-0.12, 0, 0.02], actor.yaw));
  let rightHand = mix(restRight, grip, ease(t, 4.35, 5.65));
  if (ball.phase === "flight") {
    const u = (t - RELEASE) / (CATCH - RELEASE);
    const releaseHand = add(heldBall(RELEASE), [-0.12, 0, 0.02]);
    const catchHand = add(heldBall(CATCH), [-0.12, 0, 0.02]);
    rightHand = mix(releaseHand, catchHand, u);
    rightHand[1] += 0.2 * Math.sin(Math.PI * u);
  }
  let leftHand = localPoint(actor, [-0.39, 0.08, 0.12 - (walking ? 0.24 * swing : 0)]);
  const balancing = ease(t, 4.3, 5.2) * (1 - ease(t, 6, 6.8));
  leftHand = mix(leftHand, localPoint(actor, [-0.48, 0.15, 0.31]), balancing);
  const shrug = ease(t, 7, 7.5) * (1 - ease(t, 7.8, 8.2));
  leftHand = mix(leftHand, localPoint(actor, [-0.51, 0.37, 0.24]), shrug);
  leftHand = mix(leftHand, localPoint(actor, [-0.22, 0.11, 0.36]), actor.sitting);
  const blink = [1.7, 4, 6.9, 10.3, 14.3].reduce((a, at) => Math.max(a, Math.max(0, 1 - Math.abs(t - at) / 0.1)), 0);
  return { time, t, actor, ball, rightHand, leftHand, blink, smile: ease(t, 9.9, 10.5), shot: t < 4.15 ? "wide" : t < 7.2 ? "pickup" : t < 10.5 ? "toss" : "wide" };
}

// src/scene.mjs
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
  function cylinder(parent, m, pos, radius, height2) {
    const mesh = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, height2, 20), m);
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
  const debug = {};
  function update(pose) {
    const { actor, ball: prop } = pose;
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
      const target = pose[`${side}Hand`];
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
    ball.rotation.set(0.3 + pose.t * 1.2, pose.t * 0.7, 0.15);
    head.rotation.x = clamp(-(prop.position[1] - (actor.position[1] + 0.93)) * 0.15, -0.15, 0.16) - actor.lean * 0.45;
    head.rotation.z = Math.sin(pose.t * 4) * 0.025 * (actor.left.moving || actor.right.moving ? 1 : 0);
    eyes.forEach((eye) => {
      eye.scale.y = 1 - 0.92 * pose.blink;
    });
    brows[0].rotation.z = -0.06 + 0.13 * (pose.t > 6.8 && pose.t < 8.2 ? 1 : 0);
    brows[1].rotation.z = 0.06;
    mouthMaterial.opacity = 1 - pose.smile;
    smileMaterial.opacity = pose.smile;
    if (pose.shot === "wide") {
      camera.left = -4.8;
      camera.right = 4.8;
      camera.top = 2.7;
      camera.bottom = -2.7;
      camera.position.set(6.3, 4.4, 9.4);
      camera.lookAt(0, 1.05, 0);
    } else {
      const halfWidth = pose.shot === "toss" ? 3 : 2.75;
      camera.left = -halfWidth;
      camera.right = halfWidth;
      camera.top = halfWidth * 9 / 16;
      camera.bottom = -halfWidth * 9 / 16;
      camera.position.set(pose.shot === "pickup" ? 3 : 2.2, 3, 6.2);
      camera.lookAt(0.2, pose.shot === "toss" ? 1.45 : 1.3, 0.65);
    }
    camera.updateProjectionMatrix();
    camera.updateMatrixWorld(true);
    scene.updateMatrixWorld(true);
    joints.head = head.localToWorld(new THREE.Vector3(0, 0.37, 0)).toArray();
    joints.ball = prop.position;
    debug.joints = joints;
    debug.reaches = reaches;
    debug.shot = pose.shot;
    debug.pose = pose;
    debug.projected = Object.fromEntries(Object.entries(joints).map(([key2, point]) => [key2, v(point).project(camera).toArray()]));
  }
  return { scene, camera, update, debug };
}

// src/main.mjs
var canvas = document.getElementById("clay-stage");
var root = document.getElementById("clay-room");
var width = Number(root.dataset.width);
var height = Number(root.dataset.height);
var renderer = new THREE2.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, powerPreference: "low-power" });
renderer.setPixelRatio(1);
renderer.setSize(width, height, false);
renderer.outputColorSpace = THREE2.SRGBColorSpace;
renderer.toneMapping = THREE2.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.02;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE2.PCFShadowMap;
var stage = makeScene(renderer);
var shownTime = -1;
var gl = renderer.getContext();
var pixel = new Uint8Array(4);
function draw(seconds) {
  const pose = poseAt(seconds);
  if (shownTime === pose.t) return;
  stage.update(pose);
  renderer.render(stage.scene, stage.camera);
  gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, pixel);
  shownTime = pose.t;
}
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
var ready = (async () => {
  stage.update(poseAt(0));
  if (renderer.extensions.has("KHR_parallel_shader_compile")) await renderer.compileAsync(stage.scene, stage.camera);
  else renderer.compile(stage.scene, stage.camera);
  draw(0);
})();
window.__hf.buildReady["clay3d"] = ready;
window.addEventListener("hf-seek", (event) => {
  const work = ready.then(() => draw(event.detail.time));
  event.detail.waitUntil?.(work);
});
window.__clay3d = {
  ready,
  seek: async (t) => {
    await ready;
    draw(t);
    return JSON.parse(JSON.stringify(stage.debug));
  },
  diagnostics: () => ({ renderer: renderer.info.render, webgl: gl.getParameter(gl.VERSION), size: [width, height] }),
  auditMotion: () => {
    const previous = shownTime;
    const unreachable = [];
    const clipped = [];
    for (let frame = 0; frame < 450; frame++) {
      stage.update(poseAt(frame / 30));
      for (const reach of stage.debug.reaches) if (reach.armError > 0.01 || reach.footError > 0.01) unreachable.push({ frame, ...reach });
      for (const [joint, point] of Object.entries(stage.debug.projected)) if (Math.abs(point[0]) > 0.97 || Math.abs(point[1]) > 0.97) clipped.push({ frame, joint, point });
    }
    shownTime = -1;
    draw(previous);
    return { frames: 450, unreachable, clipped };
  }
};
