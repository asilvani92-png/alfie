# ✂️ PART 4 — THE AUTO-CUTTER
## AI finds the big moments and cuts the clips for you
**Time: first run ~15 min on a 10-min video (Whisper is the slow part). Tested logic: the detector found 2/2 synthetic crowd-roars in validation.**

---

## HOW IT WORKS (so you can trust/tune it)
Two detection layers produce a per-second score; the top-scoring seconds become clips:

1. **Crowd-roar detection** — rolling loudness (RMS) of the audio. Stadiums *announce* goals acoustically. No ML needed, catches ~90% of big moments.
2. **Whisper keyword spotting** (`--whisper`) — transcribes commentary and scores every mention of "Jiménez / Raúl / goal / scores / header / penalty". This turns generic "loud moments" into **Jiménez-specific moments**. Keyword mentions outweigh raw noise in the combined score (0.5×audio + 0.8×keywords).

Clips are cut ~10s before → 8s after each moment (tunable), minimum 45s apart so one goal doesn't produce 3 overlapping clips.

## STEP 1 — First run (audio-only, fast sanity check)

```bash
rj   # alias: activates .venv + cd /Users/alfie/Downloads/faceless-football/raul-jimenez-project/scripts
python3 auto_cutter.py ../footage/your_video.mp4
```

Output → `clips/your_video/clip_01_score92_t0834.mp4` etc + `clips_report.json` (timestamps + scores). Watch the clips: are they goals? If yes, layer on Whisper.

## STEP 2 — Full run with keyword spotting

```bash
python3 auto_cutter.py ../footage/your_video.mp4 --whisper --top 8
```

It prints every keyword hit with its timestamp and text — a free **moment log** for your script-writing too. Spanish-commentary footage? Add Spanish keywords:

```bash
python3 auto_cutter.py ../footage/mexico_match.mp4 --whisper \
  --keywords "jimenez,jiménez,raul,raúl,gol,golazo,cabezazo,penal"
```

## STEP 3 — Tune (only if needed)
| Want | Flag |
|---|---|
| More/fewer clips | `--top 10` / `--top 4` |
| Longer build-up before the moment | `--pre 15` |
| More celebration after | `--post 12` |
| Faster (worse) / slower (better) transcription | `--model tiny` / `--model small` |

## STEP 4 — Select with taste (the human 10 minutes)
Open the clips folder, watch everything (it's minutes, not hours), and shortlist per asset:
- Best **single goal with the loudest roar** → Short #5 (comeback goal) / reactive template
- Best 5–6 varied goals → Short #3 (57 goals reel)
- Anything where commentary says his name with emotion → doc act openers

> 🧠 Score ≠ taste. The machine finds candidates; YOU pick the goosebumps. The `clips_report.json` timestamps let you re-cut any moment longer/shorter manually:
> ```bash
> ffmpeg -ss 832 -i ../footage/your_video.mp4 -t 25 -c copy better_cut.mp4
> ```

## 🤖 AI STEPS FOR THIS PART
- **Prompt 4A**: paste `clips_report.json` + the Whisper keyword-hit lines → AI ranks clips by emotional value, assigns each to a slate asset, and drafts the hook line + caption for each clip.
- **Prompt 4B** (when a run misses an obvious moment): describe what it missed → AI suggests the exact flag changes / keyword additions to re-run with.

## TROUBLESHOOTING
| Problem | Fix |
|---|---|
| "ffmpeg failed" | `brew install ffmpeg`; check the input file plays in QuickTime |
| "whisper not installed — skipping keyword pass" | Your `.venv` isn't active (prompt must show `(.venv)`) → `rj` first. Then `pip install openai-whisper` (or `pip install faster-whisper` — script auto-detects either) |
| `torch`/whisper won't install | You're on system Python (3.14). Activate the `.venv` (Python 3.11) — never `pip3 install` outside it |
| Whisper very slow | Use `--model tiny` for triage, re-run `base` on keepers |
| Clips start mid-replay | Broadcasters replay goals: raise `--pre` to 15, or use the report timestamp − 30s manually |
| Everything scores low | Crowd audio mixed quiet in some compilations → rely on `--whisper` keywords instead. NOTE: match *recaps* (pre-condensed) have weaker roar peaks — keywords are the main signal there |
| Spanish commentary | add keywords: `gol,golazo,cabezazo,penal` and consider `--model small` for accuracy |

**Next →** `05-vertical-and-captions.md`
