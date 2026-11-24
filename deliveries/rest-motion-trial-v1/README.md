# Psychology Facts: faster motion trial

**15-second native 1280x720, 30fps prototype**, with the established painted gray-haired green-waistcoat character. This is an explicitly requested interim movement trial, not a replacement of the complete long film.

- `agile-motion-15s.mp4`: new authored performance, reused native English narration, complete English subtitles and original local sound.
- `previous-vs-new-15s.mp4`: prior picture on the left, new picture on the right, matched to the same narration excerpt. Only the new soundtrack plays. The previous picture is held for the final 0.98s to match the 15s trial; no speed-up is applied.
- `decoded-motion-board.jpg`: inspection samples from the actual final MP4.
- `source-project.zip`: reproducible source with saved speech, actor-performance code, scenes, fonts, exact dependency lock and local reference excerpt.

## What changed

Motion timing is authored in seconds, independently of paragraph duration. Sit: 0.41s; rise: 0.55s; shirt bend: 0.53s; pickup recovery: 0.60s. Fourteen individually timed foot contacts cover two fast approaches and a short backward reaction. Each planted foot stays in world space while the body/camera move. The shirt changes from a floor prop to the actual holding hand at acquisition and stays with that hand. A foreground door jamb, connected room reveal and motivated action/reaction cuts give the travel a destination.

Remotion **4.0.546** composes the layered native scene, tracked camera, new actor pass, captions and audio using the installed Chromium. It does not automatically invent the acting: `performance.py` authors and renders all 450 new articulated poses using the channel's existing project-local painted rig. This is neither a rerender of the old paragraph-length easing nor a claim that changing compositor alone produces human acting. The installed B6 standing-only engine remains unchanged. No strict Sample 1 / 35-subcheck equivalence is claimed.

## Voice and costs

**Zero new paid API calls.** The existing alloy chapter recording is trimmed at native rate, preserving its samples/timbre/pace. There is no voice pitch or speed change. The six reused subtitle phrases follow the saved speech times. Music and material/contact sounds are original local synthesis; footsteps use actual swing-end times. Existing authorized painted scenes/character and Archivo Black typography are reused. Source/font license notices are included.

## Checks and review

QA.json binds the exact movie hash to frame count, full decode, audio/video timing, decoded speech correlation, loudness, all four fixed control chains, zero world-space stance drift and shirt-grip checks. The author inspected actual-MP4 action/reaction samples and relevant native-size details. These are technical/source/frame checks; independent creative review, real-time agent AV listening and user approval are not claimed. The user is reviewing this short trial before any full-film revision.

The first encoded trial showed crossed feet at the first stop and a tight head crop in the last camera shot. `repair-notes.md` records the rejected version and the changed contact/camera staging. The final trial repairs those issues; geometry is not offered as a subjective naturalness score.

## Rebuild

Requires Python with Pillow/NumPy, Node and FFmpeg. Chromium path defaults to `/usr/bin/chromium` and can be changed in package.json for another machine.

```bash
npm ci
python performance.py
python build_media.py
npm run render
python check_delivery.py
```

Ordinary local processes only; no speech/image API is invoked. The reproducible PNG pose cache is omitted from the archive; performance.py rebuilds it locally without API calls. No YouTube publication or environment-configuration change was performed.
