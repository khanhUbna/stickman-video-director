# Silver-jacket character: 20-second animation test

Creator requested a 20-second test of the silver-haired, glasses-wearing black-leather-jacket cartoon, walking, holding a cup and talking. This project retains that appearance as a separate cutout rig, not the prior stick figure.

Sequence: enter with separately scheduled footsteps; reach and grasp the cup handle; lift; speak and gesture; walk with the held cup; speak again; return; place cup; release and nod. Mouth openings follow voice RMS. Foot contacts are independently scheduled in world space. Two-bone IK preserves source limb lengths. The cup is bound to the hand during ownership and remains on the table before pickup and after placement.

Art: image-generation tool, character asset generated from the preceding cartoon reference, saved as assets/character-source.png. Animation, scene and Foley are original project-local code. Voice: local Kokoro ONNX am_michael, cached Apache-2.0 model; generic synthetic American English, not an imitation of the photographed person's voice. No paid TTS, cloud render or voice-cloning service. The dialogue is original fictional demonstration, not a statement attributed to the pictured real person. No YouTube publication.

This is a simple front-view cutout prototype, not continuous 3D rotation or hand-drawn frame-by-frame animation. It can show whether this art direction is worth pursuing; it does not establish final production acceptance. Visual contact-sheet inspection and technical decode/geometry tests are separate from full-speed human playback and creator approval.

Reproduce with existing local model/venv:
```
/workspace/.venvs/clay-narration/bin/python production/silver-jacket-motion-test-v1/speech.py
python3 production/silver-jacket-motion-test-v1/render.py --sheets
python3 production/silver-jacket-motion-test-v1/render.py
```

Deliverables: deliveries/silver-jacket-motion-test-v1/ with MP4, English/Vietnamese captions and actual QA report. No speech speed changes after synthesis. Original footage/source artwork from earlier projects are preserved.
