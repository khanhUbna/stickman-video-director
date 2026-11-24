import test from 'node:test';
import assert from 'node:assert/strict';
import { poseAt, ballAt, actorAt, solveTwoBone, length, sub, RELEASE, CATCH } from '../src/motion.mjs';
import { validateArgs, localEnvironment } from '../scripts/hf.mjs';

test('random-access seeking gives the same state before and after arbitrary other seeks', () => {
  const expected = poseAt(5.75); poseAt(14.9); poseAt(0.2); poseAt(9.1);
  assert.deepEqual(poseAt(5.75), expected);
});

test('stance feet remain fixed and do not penetrate the floor; real foot lifts occur', () => {
  let lifts = 0;
  for (let t = 0; t < 15; t += 1 / 120) {
    const now = actorAt(t); const next = actorAt(t + 1 / 120);
    for (const side of ['left', 'right']) {
      assert.ok(now[side].position[1] >= 0.12 - 1e-9);
      if (now[side].moving) lifts++;
      if (!now[side].moving && !next[side].moving) assert.deepEqual(now[side].position, next[side].position);
    }
  }
  assert.ok(lifts > 100);
});

test('the prop is lifted, travels independently during the toss and returns continuously to the hand', () => {
  assert.equal(ballAt(4).phase, 'floor');
  assert.equal(ballAt(6).held, true);
  const peak = ballAt((RELEASE + CATCH) / 2);
  assert.equal(peak.held, false); assert.ok(peak.position[1] > 2.1);
  for (const edge of [5.65, 6.65, RELEASE, CATCH]) {
    assert.ok(length(sub(ballAt(edge + 1e-5).position, ballAt(edge - 1e-5).position)) < 0.001);
  }
});

test('inverse kinematics preserves both bone lengths', () => {
  const origin = [0, 1, 0]; const target = [0.2, 0.2, 0.2];
  const solved = solveTwoBone(origin, target, [0, 0, 1], 0.53, 0.51);
  assert.ok(solved.reachable);
  assert.ok(Math.abs(length(sub(origin, solved.joint)) - 0.53) < 1e-6);
  assert.ok(Math.abs(length(sub(solved.joint, solved.end)) - 0.51) < 1e-6);
});

test('the tossed ball clears the head rather than passing through the character', () => {
  for (let t = RELEASE; t < CATCH; t += 1 / 120) {
    const actor = actorAt(t); const ball = ballAt(t);
    const head = [actor.position[0], actor.position[1] + 0.93, actor.position[2] + 0.025];
    assert.ok(length(sub(ball.position, head)) > 0.53);
  }
});

test('the local-only gateway refuses remote media, account and billing paths', () => {
  for (const verb of ['cloud', 'cloudrun', 'lambda', 'auth', 'billing', 'tts', 'media-use', 'events', 'usage', 'share', 'publish']) {
    assert.throws(() => validateArgs([verb]), /Local-only policy/);
  }
  assert.doesNotThrow(() => validateArgs(['render', '--workers', '1']));
  const env = localEnvironment();
  assert.equal(env.HYPERFRAMES_NO_TELEMETRY, '1'); assert.equal(env.DO_NOT_TRACK, '1');
});
