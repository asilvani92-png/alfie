# 📱 PART 5 — VERTICAL REFRAME + CAPTIONS
## 16:9 clip → 1080×1920 platform-ready short
**Time: centre mode = seconds per clip. YOLO mode = 1–2× clip length.**

---

## STEP 1 — Centre crop (default, fine for most football wide shots)

```bash
rj   # alias: activates .venv + cd /Users/alfie/Downloads/faceless-football/raul-jimenez-project/scripts
python3 reframe_vertical.py ../clips/your_video/clip_01_score92_t0834.mp4
```
→ `clip_01..._vertical.mp4` (1080×1920).

Football's main camera keeps the action near centre ~80% of the time, so START here. Only escalate to YOLO when the action hugs a touchline and gets cropped out.

## STEP 2 — YOLO smart crop (when centre fails)

```bash
python3 reframe_vertical.py ../clips/.../clip_03.mp4 --mode yolo
```
Tracks players + ball (ball weighted 3×) with YOLOv8-nano and slides the crop window to follow play, smoothed so it doesn't jitter. First run auto-downloads the model (~6MB).

## STEP 3 — Burned captions (Whisper, big bold style)

```bash
python3 reframe_vertical.py ../clips/.../clip_01.mp4 --captions
# or both at once:
python3 reframe_vertical.py ../clips/.../clip_03.mp4 --mode yolo --captions
```
Transcribes the audio and burns UPPERCASE Arial-Black subtitles with black outline, positioned for shorts (clear of UI buttons).

> 🎨 **When to use CapCut instead:** for the *hook text* (the first-1.5-seconds line) and trending karaoke-style captions, drop the `_vertical.mp4` into CapCut desktop (free) → Auto captions → pick a bold template → add your hook as a separate big text layer for seconds 0–2. CapCut's caption styles outperform plain burns on TikTok. Use the script's `--captions` for speed; use CapCut for the bangers.

## STEP 4 — The shorts assembly recipe (per clip, in CapCut)
1. Import `_vertical.mp4`
2. **Hook text** on screen 0.0–2.0s (from your AI captions — Prompt 4A output)
3. Your **narration** voice-over (ElevenLabs or your own) — narration over real clips is both the retention play AND the transformation play
4. **Music:** TikTok/Reels → add "Red Days by Telescreens" from the in-app library at ~20% under narration; YouTube → royalty-free track
5. End card 1s: "Follow for the full story 🐺" (loop-friendly: last line answers the hook)
6. Export 1080×1920 → save to `verticals/`

## ✅ QUALITY CHECK (every clip, 30 seconds)
- [ ] Action stays in frame the whole clip (else → YOLO mode)
- [ ] Hook text readable in 1.5s, doesn't cover the ball/player
- [ ] Captions don't overlap platform UI (bottom 15% clear)
- [ ] Narration louder than crowd; music under both
- [ ] First frame is NOT a black/blurry frame (thumbnails matter on Reels)

## 🤖 AI STEP
**Prompt 5A** (`09-ai-prompt-library.md`): paste your clip list + which asset each serves → AI returns per-clip: hook text overlay, 3 caption options per platform, hashtag stack, pinned-comment question.

**Next →** `06-hero-documentary.md`
