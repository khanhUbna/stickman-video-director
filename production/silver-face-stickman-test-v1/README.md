# Cartoon face + stickman: 20-second prototype

Creator requested a simpler stickman body after rejecting the textured leather-jacket rig. During this task, the creator rejected the detailed portrait head as visually mismatched, specifically the neck/collar join, and explicitly allowed a less exact likeness. The final version therefore uses an original procedural cartoon face: silver swept hair, glasses, flat colors, simple eyes and a speaking mouth. No portrait texture or old black collar is composited into the final video. Original detailed-face preview is preserved in reports/rejected-detailed-face.png as a rejected design, not the final face.

The body is a slim plain dark torso and connected rounded vector limbs. There are no raster sleeve/pants fragments, circular seam covers or warped leather textures. Short skin-colored neck is drawn behind the head and collar. Shoulder/elbow/wrist and hip/knee/ankle positions control complete connected polylines; two-bone IK keeps limb lengths fixed. Feet have individual world-space contact/swing tracks. Cup ownership follows the actual wrist through reach, lift, carry, placement and release. Stationary cup bottom sits on the tabletop at y=409. Head/face movement is procedural, with mouth energy from the unchanged existing voice.

Sequence: walk to table; reach and lift cup; speak and gesture; carry cup a few steps; second line; return; place and release; nod. All dialogue, timing and audio are reused byte-for-byte from silver-jacket-motion-test-v1. Voice is free local Kokoro am_michael, a generic synthetic English demo, not a cloned real person's voice. Voice/model license and provenance records remain in the earlier source project. No paid APIs, new image generation or YouTube publication.

Reproduce using Python with Pillow/NumPy and FFmpeg:
```
python3 production/silver-face-stickman-test-v1/render.py --sheets
python3 production/silver-face-stickman-test-v1/render.py
python3 production/silver-face-stickman-test-v1/verify.py
```

Outputs: deliveries/silver-face-stickman-test-v1/cartoon-stickman-coffee-20s.mp4 (20 seconds, 1280×720, 30fps), English burned captions, English/Vietnamese SRT and QA. Source and measured checks do not prove fully natural motion or replace human full-speed playback/creator acceptance. The face is a new stylized design in response to the latest steering, not the exact earlier portrait.
