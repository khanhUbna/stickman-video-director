// Authored, seekable character choreography. Units: metres and seconds. No clock or simulation state.
export const DURATION = 15;
export const FPS = 30;
export const CLAY_HZ = 12;
export const RELEASE = 8.65;
export const CATCH = 9.9;
export const lerp = (a, b, t) => a + (b - a) * t;
export const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const ease = (t, a, b) => { const u = clamp((t - a) / (b - a)); return u * u * (3 - 2 * u); };
export const mix = (a, b, u) => a.map((x, i) => lerp(x, b[i], u));
export const add = (a, b) => a.map((x, i) => x + b[i]);
export const sub = (a, b) => a.map((x, i) => x - b[i]);
export const mul = (a, s) => a.map(x => x * s);
export const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
export const length = a => Math.hypot(...a);
export const normalized = a => mul(a, 1 / Math.max(length(a), 1e-9));
export const rotateY = ([x, y, z], a) => [x * Math.cos(a) + z * Math.sin(a), y, -x * Math.sin(a) + z * Math.cos(a)];
export const localPoint = (root, xyz) => add(root.position, rotateY(xyz, root.yaw));

export function solveTwoBone(origin, target, pole, upper, lower) {
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

// Every stance foot stays on one world-space anchor while the other foot takes a step.
const steps = {
  left: [[0.60, 1.10, -2.05], [1.70, 2.20, -1.00], [2.80, 3.30, 0.05], [10.60, 11.10, 0.80], [11.70, 12.20, 1.92], [12.80, 13.10, 2.15]],
  right: [[1.15, 1.65, -1.55], [2.25, 2.75, -0.45], [3.35, 3.85, 0.20], [11.15, 11.65, 1.35], [12.25, 12.75, 2.45]],
};

function footAt(t, side) {
  let x = -2.70;
  for (const [start, end, next] of steps[side]) {
    if (t < start) break;
    if (t < end) {
      const u = (t - start) / (end - start);
      return { position: [lerp(x, next, ease(t, start, end)), 0.12 + Math.sin(Math.PI * u) * 0.19, side === 'left' ? 0.89 : 0.53], moving: true, phase: u };
    }
    x = next;
  }
  return { position: [x, 0.12, side === 'left' ? 0.89 : 0.53], moving: false, phase: 0 };
}

export function actorAt(t) {
  const left = footAt(t, 'left'); const right = footAt(t, 'right');
  const squat = ease(t, 4.25, 5.65) * (1 - ease(t, 5.65, 6.65));
  const tossDip = Math.sin(Math.PI * clamp((t - 8.15) / 0.50)) * 0.07;
  const catchDip = Math.sin(Math.PI * clamp((t - 9.76) / 0.62)) * 0.09;
  const sitting = ease(t, 13.1, 14.25);
  const walkBob = (left.moving ? Math.sin(left.phase * Math.PI) : 0) + (right.moving ? Math.sin(right.phase * Math.PI) : 0);
  const strideDrop = 0.13 * (Math.abs(left.position[0] - right.position[0]) / 1.15) ** 2;
  let yaw = Math.PI / 2 * (1 - ease(t, 3.85, 4.25));
  yaw += Math.PI / 2 * ease(t, 10.20, 10.60) * (1 - ease(t, 12.85, 13.4));
  return {
    position: [(left.position[0] + right.position[0]) / 2, 1.18 - 0.76 * squat - tossDip - catchDip - 0.45 * sitting - strideDrop + 0.012 * walkBob, 0.71 - 0.62 * sitting],
    yaw, lean: 0.43 * squat - 0.12 * sitting + 0.04 * Math.sin(t * 4) * (left.moving || right.moving ? 1 : 0),
    squat, sitting, left, right,
    shoeYaw: Math.PI / 2 * (1 - ease(t, 12.85, 13.45)),
  };
}

const FLOOR_BALL = [0.40, 0.17, 1.05];
function heldBall(t, actor = actorAt(t)) {
  const inspect = ease(t, 6.8, 7.4) * (1 - ease(t, 7.7, 8.2));
  return localPoint(actor, [0.44 * (1 - actor.sitting), 0.32 + 0.23 * inspect - 0.17 * actor.sitting, 0.35]);
}

export function ballAt(t, actor = actorAt(t)) {
  if (t < 5.65) return { position: [...FLOOR_BALL], held: false, phase: 'floor' };
  if (t < 6.65) return { position: mix(FLOOR_BALL, heldBall(t, actor), ease(t, 5.65, 6.65)), held: true, phase: 'lift' };
  if (t >= RELEASE && t < CATCH) {
    const u = (t - RELEASE) / (CATCH - RELEASE);
    const position = mix(heldBall(RELEASE), heldBall(CATCH), u);
    position[1] += 4 * 1.50 * u * (1 - u);
    return { position, held: false, phase: 'flight' };
  }
  return { position: heldBall(t, actor), held: true, phase: 'held' };
}

export function poseAt(seconds, { stepped = true } = {}) {
  const time = clamp(seconds, 0, DURATION);
  const t = stepped ? Math.floor((time + 1e-7) * CLAY_HZ) / CLAY_HZ : time;
  const actor = actorAt(t); const ball = ballAt(t, actor);
  const walking = actor.left.moving || actor.right.moving;
  const swing = Math.sin(t * Math.PI * 2 / 1.1);
  const restRight = localPoint(actor, [0.39, 0.08, 0.12 + (walking ? 0.24 * swing : 0)]);
  const grip = add(ball.position, rotateY([-0.12, 0, 0.02], actor.yaw));
  let rightHand = mix(restRight, grip, ease(t, 4.35, 5.65));
  if (ball.phase === 'flight') {
    const u = (t - RELEASE) / (CATCH - RELEASE);
    const releaseHand = add(heldBall(RELEASE), [-0.12, 0, 0.02]);
    const catchHand = add(heldBall(CATCH), [-0.12, 0, 0.02]);
    rightHand = mix(releaseHand, catchHand, u);
    rightHand[1] += 0.20 * Math.sin(Math.PI * u);
  }
  let leftHand = localPoint(actor, [-0.39, 0.08, 0.12 - (walking ? 0.24 * swing : 0)]);
  const balancing = ease(t, 4.3, 5.2) * (1 - ease(t, 6.0, 6.8));
  leftHand = mix(leftHand, localPoint(actor, [-0.48, 0.15, 0.31]), balancing);
  const shrug = ease(t, 7.0, 7.5) * (1 - ease(t, 7.8, 8.2));
  leftHand = mix(leftHand, localPoint(actor, [-0.51, 0.37, 0.24]), shrug);
  leftHand = mix(leftHand, localPoint(actor, [-0.22, 0.11, 0.36]), actor.sitting);
  const blink = [1.7, 4.0, 6.9, 10.3, 14.3].reduce((a, at) => Math.max(a, Math.max(0, 1 - Math.abs(t - at) / 0.10)), 0);
  return { time, t, actor, ball, rightHand, leftHand, blink, smile: ease(t, 9.9, 10.5), shot: t < 4.15 ? 'wide' : t < 7.2 ? 'pickup' : t < 10.5 ? 'toss' : 'wide' };
}
