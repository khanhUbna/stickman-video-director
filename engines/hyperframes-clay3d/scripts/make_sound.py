"""Original quiet foley and four-note score, synthesized locally. No samples or APIs."""
from pathlib import Path
import math
import random
import struct
import wave

RATE = 48000
DURATION = 15
samples = [0.0] * (RATE * DURATION)
rng = random.Random(182)

def tone(start, seconds, frequency, amplitude=0.10):
    for i in range(int(seconds * RATE)):
        t = i / RATE
        envelope = min(1.0, t / 0.012) * math.exp(-t * 5 / seconds)
        value = (math.sin(2 * math.pi * frequency * t) + 0.18 * math.sin(4 * math.pi * frequency * t)) * envelope * amplitude
        index = int(start * RATE) + i
        if index < len(samples):
            samples[index] += value

def step(start):
    for i in range(int(0.10 * RATE)):
        t = i / RATE
        index = int(start * RATE) + i
        if index < len(samples):
            samples[index] += (0.6 * math.sin(2 * math.pi * 105 * t) + 0.25 * rng.uniform(-1, 1)) * math.exp(-t * 55) * 0.11

for start in [1.1, 1.65, 2.2, 2.75, 3.3, 3.85, 11.1, 11.65, 12.2, 12.75, 13.1]:
    step(start)
for start, hz in [(0.35, 261.63), (2.6, 329.63), (5.65, 392), (7.1, 440), (8.65, 523.25), (9.9, 659.25), (13.75, 392), (14.2, 523.25)]:
    tone(start, 0.85, hz, 0.045)
tone(8.68, 0.18, 720, 0.06)
tone(9.92, 0.15, 280, 0.08)
path = Path(__file__).resolve().parents[1] / 'assets/clay-sound.wav'
path.parent.mkdir(parents=True, exist_ok=True)
gain = 0.65 / max(abs(sample) for sample in samples)
with wave.open(str(path), 'wb') as output:
    output.setnchannels(1)
    output.setsampwidth(2)
    output.setframerate(RATE)
    output.writeframes(b''.join(struct.pack('<h', int(max(-0.95, min(0.95, sample * gain)) * 32767)) for sample in samples))
print(f'Original local audio: {path.name}, {DURATION}s, {RATE}Hz')
