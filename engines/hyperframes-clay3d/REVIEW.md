# Actual clay animation trial review

The final composition was rendered with HyperFrames 0.9.88 on Codex Cloud and the **encoded MP4** was inspected, not only a preview image.

## Technical result

- 15.000 seconds, 1920×1080, 30/1 fps, **450 decoded frames**.
- H.264 / yuv420p video and AAC audio; full FFmpeg decode returned no errors.
- Final HyperFrames check: `ok: true`, zero errors and zero warnings. Runtime/browser audits actually ran.
- Browser QA: 13 image samples, all 450 pose states checked; no unreachable hand/foot targets or out-of-frame tracked joints/prop centers.
- Repeated random-access seek produced identical joint states and identical PNGs.
- MP4/browser RGB mean absolute differences at 2.5, 7.5 and 14.6 seconds: approximately **2.19, 2.12 and 2.19 / 255** after small-frame decoding. These are comparison measurements, not aesthetic scores.
- Constant-camera wide-shot pixel change: 4.67 / 255, with independent articulated-joint/stance-foot checks. Movement is not explained by camera zoom.
- Decoded audio RMS: 0.0726; sample peak: 0.9591. No clipping was found by the peak threshold. Original local synthesis only.
- Final render used software WebGL/screenshot capture and took approximately **3 minutes 39 seconds** including CLI overhead. This is measured render time on this host, not playback speed or a performance guarantee.

## Visual review

Inspected the full browser contact sheet, close views at the lift and toss, the actual local editor preview, and the MP4-derived fifteen-frame contact sheet. The cloth/hair identity is preserved as a procedural clay interpretation. The feet lift alternately; torso, shoulders, elbows and knees change relative pose; the character squats to pick up the ball, separates the prop from the hand for the toss, catches it and sits on the sofa.

An early preview's toss passed too close to the head. The final trajectory was moved outward and raised, the toss framing was widened, a head-clearance test was added, and the MP4 was rendered again. Three.js capability/deprecation warnings were fixed with an explicit supported shadow map and conditional shader compilation. Intentional full-bleed set art is declared as such; character/prop framing is checked separately.

The image is deliberately a matte, simplified clay miniature and the 12-Hz posing deliberately has a stop-motion cadence inside the 30-fps file. This is a reusable procedural character demo, not a claim of photoreal motion capture or automatic scene creation from narration. Technical/visual review does not replace the creator's artistic approval.

## Existing tooling and limits

All 763 recorded old renderer/YouTube support files stayed byte-identical; all 333 original HyperFrames skill files matched upstream, and all 12 YouTube skills passed the installation check. The npm audit reported zero known vulnerabilities at installation time.

Node.js, Chromium, FFmpeg and FFprobe worked in the real local render. The general doctor report lists missing optional voice/transcription/music packages; they are not necessary for this composition and were not installed.

The optional online registry search returned `ECONNREFUSED` on this host. This did not affect the pinned npm installation, installed local skills, local preview, Three.js engine, or MP4 render. It is recorded as an unavailable optional online utility; do not bypass HTTPS/SSRF protections or switch to a paid generation service to work around it. Source reference blocks remain available in the inspected upstream Git checkout, and a later registry request needs working supported HTTPS connectivity.

No HeyGen service, paid API, account login, credit purchase, cloud render, external media generation or telemetry report was invoked. No API key was displayed or committed.
