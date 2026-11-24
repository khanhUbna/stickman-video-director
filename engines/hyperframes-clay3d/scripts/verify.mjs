import { spawnSync } from 'node:child_process';
import { readFile, writeFile } from 'node:fs/promises';
import { engineRoot, localEnvironment } from './hf.mjs';
import path from 'node:path';

const folder = path.join(engineRoot, 'output'); const file = path.join(folder, 'clay-animation-15s.mp4');
const env = localEnvironment();
function ffmpeg(args) {
  const result = spawnSync(env.HYPERFRAMES_FFMPEG_PATH, ['-hide_banner', '-v', 'error', ...args], { maxBuffer: 16 * 1024 * 1024 });
  if (result.status !== 0) throw new Error(result.stderr.toString() || 'FFmpeg failed');
  return result.stdout;
}
const probe = spawnSync(env.HYPERFRAMES_FFPROBE_PATH, ['-v', 'error', '-count_frames', '-show_format', '-show_streams', '-of', 'json', file], { encoding: 'utf8' });
if (probe.status !== 0) throw new Error(probe.stderr);
const metadata = JSON.parse(probe.stdout); const video = metadata.streams.find(x => x.codec_type === 'video'); const audio = metadata.streams.find(x => x.codec_type === 'audio');
ffmpeg(['-i', file, '-f', 'null', '-']);
const rgb = (input, time) => ffmpeg([...(time === undefined ? [] : ['-ss', String(time)]), '-i', input, '-frames:v', '1', '-vf', 'scale=480:270', '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-']);
function mae(a, b) { if (a.length !== b.length) throw new Error('Frame size mismatch'); let sum = 0; for (let i = 0; i < a.length; i++) sum += Math.abs(a[i] - b[i]); return sum / a.length; }
const fidelity = [];
for (const t of [2.5, 7.5, 14.6]) fidelity.push({ time: t, meanAbsoluteRgbError: mae(rgb(file, t), rgb(path.join(folder, `browser-${t.toFixed(2)}.png`))) });
const wideShotChange = mae(rgb(file, 0.1), rgb(file, 3.0));
const pcm = ffmpeg(['-i', file, '-map', '0:a:0', '-ac', '1', '-ar', '48000', '-f', 'f32le', '-']);
let sum = 0; let peak = 0;
for (let i = 0; i < pcm.length; i += 4) { const value = pcm.readFloatLE(i); sum += value * value; peak = Math.max(peak, Math.abs(value)); }
const rms = Math.sqrt(sum / (pcm.length / 4));
ffmpeg(['-i', file, '-vf', 'fps=1,scale=480:270,tile=5x3', '-frames:v', '1', '-y', path.join(folder, 'decoded-contact-sheet.jpg')]);
const browser = JSON.parse(await readFile(path.join(folder, 'browser-qa.json'), 'utf8'));
const report = {
  duration: Number(metadata.format.duration), width: video.width, height: video.height,
  fps: video.avg_frame_rate, frames: Number(video.nb_read_frames), codec: video.codec_name, pixelFormat: video.pix_fmt,
  audioCodec: audio?.codec_name, audioRms: rms, audioPeak: peak, fullDecodeErrors: 0,
  fidelity, wideShotPixelChange: wideShotChange, browserMotionAudit: browser.fullMotion,
  browserPageErrors: browser.pageErrors, browserExternalRequests: browser.blockedExternalRequests,
  notes: ['Decoded MP4 frames compared against independent browser captures.', 'Wide-shot camera is fixed; changing joint poses and planted feet are audited separately from pixel changes.', 'Movement is authored at twelve poses per second for a clay stop-motion cadence in a thirty-fps file.'],
};
report.ok = Math.abs(report.duration - 15) <= 0.05 && report.width === 1920 && report.height === 1080 && report.frames === 450 && report.codec === 'h264' && report.pixelFormat === 'yuv420p' && !!audio && rms > 0.001 && peak < 0.99 && fidelity.every(x => x.meanAbsoluteRgbError < 10) && wideShotChange > 0.8 && browser.ok;
await writeFile(path.join(folder, 'video-quality.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
if (!report.ok) process.exitCode = 1;
