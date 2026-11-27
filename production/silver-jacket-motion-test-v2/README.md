# Corrected 20-second character test V2

The creator rejected V1 because arms and legs looked detached. V1 rigidly rotated independently cut polygons, clipped shoulder/hip artwork, and covered shoulder seams with visible dark circles. Its checks measured foot/prop coordinates without measuring the rendered body silhouette. That was insufficient visual QA.

V2 replaces those body pieces with a shared-vertex textured mesh and blended skinning over elbow, knee, shoulder, hip and ankle regions. It renders the original suit and limbs as a continuous surface, without circular shoulder covers or separate rigid limb outlines. The face is kept as a separate overlapping neck/head element to retain facial animation. Step lift and foot rotation are reduced. The original 20-second timeline, source portrait artwork, voice and caption files are reused, with no TTS or image-generation calls.

Local runtime: opencv-python-headless 4.11.0.86 installed under /workspace/.cache/silver-jacket-mesh-deps; Python/Pillow/NumPy and FFmpeg. `mesh.py` is the complete deterministic deformation/rasterization source. Art/audio provenance and voice/model license documents remain in ../silver-jacket-motion-test-v1/. Original voice is free local Kokoro am_michael, not impersonation.

Reproduction:
```
python3 -m pip install --target /workspace/.cache/silver-jacket-mesh-deps --no-deps opencv-python-headless==4.11.0.86
python3 production/silver-jacket-motion-test-v2/render.py
python3 production/silver-jacket-motion-test-v2/verify.py
```

QA now checks alpha coverage at the actual 10 rendered body joint cores on all 600 frames, disconnected silhouette components, world-space planted feet, hand/cup ownership, exact reused audio, complete MP4 decode and actual encoded frame crops. Before/after comparison uses the same 7-second moment in both MP4s. These checks do not replace human full-speed playback or creator acceptance. This remains a front-view cutout/mesh prototype; it is not a complete naturalistic locomotion library or continuous 3D turn.

Final MP4 and SRT files are under deliveries/silver-jacket-motion-test-v2/. No paid service calls and no YouTube publication.
