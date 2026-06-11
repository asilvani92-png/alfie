# ⚙️ PART 1 — ONE-TIME SETUP (MacBook)
**Time: 30–40 min, mostly waiting on downloads. Do once, never again.**

---

## STEP 1 — Homebrew + core tools (10 min)

Open **Terminal** (Cmd+Space → "Terminal") and paste each line, pressing Enter after each:

```bash
# 1. Homebrew (skip if you have it — check with: brew --version)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. The video engine + downloader
brew install ffmpeg yt-dlp

# 3. Verify (both must print versions)
ffmpeg -version | head -1
yt-dlp --version
```

## STEP 2 — Python environment + packages (10 min)

> ✅ **DONE on your machine:** `.venv` with Python **3.11.11** at the project root.
> ⚠️ **Rule #1: ALWAYS activate it first.** System Python (3.14) is too new for
> torch/whisper — that's what caused the install errors. The prompt must show
> `(.venv)` before you run pip or any script.

```bash
# Activate (every new Terminal session):
source /Users/alfie/Downloads/faceless-football/raul-jimenez-project/.venv/bin/activate

# Install/verify packages INSIDE it:
pip install requests numpy openai-whisper
# Optional, YOLO smart-crop only:
pip install ultralytics opencv-python
```

**One-time shortcut so you never forget:**
```bash
echo 'alias rj="source /Users/alfie/Downloads/faceless-football/raul-jimenez-project/.venv/bin/activate && cd /Users/alfie/Downloads/faceless-football/raul-jimenez-project/scripts"' >> ~/.zshrc
source ~/.zshrc
```
From now on: open Terminal → type `rj` → ready.

## STEP 3 — Project folder (2 min)

> ✅ **DONE on your machine:** `/Users/alfie/Downloads/faceless-football/raul-jimenez-project`

```bash
rj    # (or activate + cd manually)
python3 jimenez_indexer_v2.py --help     # should print usage = working
```

## STEP 4 — Free API keys (5 min)

1. Go to **rapidapi.com** → sign up free (Google login is fine)
2. Search **"Football Highlights API"** (by Highlightly) → open it
3. Click **Subscribe to Test** → choose **BASIC (free — 100 requests/day, no card)**
   ⚠️ You MUST complete the Subscribe step — just having a key gives `403 "not subscribed"`.
4. On the API's **Endpoints** tab, copy the **x-rapidapi-key** from the code snippet panel
   (that's the key belonging to the app that holds the subscription)
5. Optional but recommended (dual quota = 200 req/day): also create a free account at
   **highlightly.net/login** and copy its key from the dashboard.
6. Save them into your shell — **each on ONE line, no line breaks inside the quotes**
   (a broken multi-line entry here caused the "Invalid header value" error):

```bash
echo 'export RAPIDAPI_KEY="PASTE-RAPIDAPI-KEY-HERE"' >> ~/.zshrc
echo 'export HIGHLIGHTLY_KEY="PASTE-HIGHLIGHTLY-KEY-HERE"' >> ~/.zshrc
source ~/.zshrc
echo "$RAPIDAPI_KEY"      # must print the key ONCE, on one line
grep -c RAPIDAPI_KEY ~/.zshrc   # should print 1 — if more, clean up duplicates: open -e ~/.zshrc
```

## STEP 5 — Free AI accounts (5 min, all free tiers)

| Tool | For | Where |
|---|---|---|
| **Claude / ChatGPT / Gemini** (any one) | Scripts, hooks, captions — all prompts in `09-ai-prompt-library.md` | claude.ai / chatgpt.com / gemini.google.com |
| **ElevenLabs free tier** | Documentary voiceover (10 min/month free — enough for 1 doc) | elevenlabs.io |
| **CapCut desktop** | Final polish + trending captions | capcut.com |
| **Canva free** | Thumbnail + carousel | canva.com |

## STEP 6 — Whisper warm-up (one command, downloads the model once)

```bash
# inside the activated .venv:
python3 -c "import whisper; whisper.load_model('base'); print('Whisper ready')"
```
> If openai-whisper ever fails to install, `pip install faster-whisper` works as a
> drop-in — the scripts auto-detect whichever engine is present.

---

## ✅ DONE WHEN
- [ ] Prompt shows `(.venv)` and `python3 --version` says 3.11.x
- [ ] `ffmpeg -version` works
- [ ] `yt-dlp --version` works
- [ ] `python3 jimenez_indexer_v2.py --help` prints usage
- [ ] `echo "$RAPIDAPI_KEY"` prints your key once, one line
- [ ] Whisper model downloaded
- [ ] ElevenLabs + one AI chat account ready

**Next →** `02b-event-indexer-v2-CORRECTED.md` (NOT 02 — that's superseded)
