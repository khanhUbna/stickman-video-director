# Local repair record

These findings were retained instead of describing the first pose scan as a pass.

- Basket stacking: late left-arm target reached the solver's extension limit. Moved the placement 20 world pixels closer; fixed bone lengths and reach limits unchanged.
- Rope rescue: two-handed targets crossed too far across the torso. Restaged grips nearer the body and raised the first pull. Rear workers use the same continuous drawn rope through their real hand targets.
- Blank stone: lowering it toward ground from a standing pose required excessive reach. Added a supported crouch, a low stool, placement, shared contact/release, and the hand's return.
- Roof repair still: a foreground straw patch crossed Nim's face. Moved the patch onto the actual upper roof region, keeping the working rope separate.
- Storm transition: a completed rescue repeated across two consecutive narrative beats. The chapter-four beat now shows Nim approaching the drifting basket; chapter five contains the actual pull.
- Fruit gathering: added a grounded approach before the reach, pick and lowering sequence. Preserved the final stance foot positions.
- Council: changed the standing group into a seated gathering with a foreground fire and the empty bowl between them.
- Framing: close work and reactions use tighter native landscape cameras; village and shared-rescue scenes retain wider space. The small final-canvas reframes are not represented as 3D camera moves.
- Near-caption feet: the first close-camera framing placed ankles too near the fixed subtitle line. Raised the ground within the close view while keeping the same full-body art; stopped the superseded render and preserved its intermediate files locally under `output/rejected-framing-v1`. Final encodes use the revised framing throughout.
- Concat timestamp: the approved preview's unused AAC priming shifted the first mux's video start by 21 ms. Its decoded pictures matched, but only 539 fell inside the first 18 seconds. Losslessly remuxed the hook to picture-only before concatenation, then rechecked all 540 decoded opening frames and the whole final file. No speech or animation regeneration was required.

The initial geometry failures are in `output/pose-scan-rejected-v1.json`. Later representative scans passed; all actual rendered frames are checked by `finish.py` using the drawn chains. Numerical validity is distinct from naturalness, reference fidelity and user approval.
