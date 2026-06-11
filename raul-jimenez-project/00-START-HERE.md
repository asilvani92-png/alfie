# 🐺 RAÚL JIMÉNEZ PROJECT — START HERE
## Your exact steps, in order. Tick them off.

> ## ⚙️ YOUR MACHINE (canonical paths — every doc assumes these)
> - **Project root:** `/Users/alfie/Documents/Apps/faceless-football/raul-jimenez-project`
> - **Scripts:** `/Users/alfie/Documents/Apps/faceless-football/raul-jimenez-project/scripts`
> - **Python env:** `.venv` (Python 3.11.11) — activate with:
>   `source /Users/alfie/Documents/Apps/faceless-football/raul-jimenez-project/.venv/bin/activate`
> - **Shortcut:** type `rj` (alias = activate venv + cd into scripts). Prompt must show `(.venv)` before running anything.
> - **Indexer:** use `jimenez_indexer_v2.py` ONLY (v1 is dead — delete it if you still have it).

> **The clock:** the signing was 9 June. Mexico's home World Cup is LIVE. Every day of delay costs reach. The order below is designed so you **publish TODAY** and automate in parallel.

---

## 🗂️ WHAT'S IN THIS FOLDER

| Doc | Part |
|---|---|
| `01-setup.md` | One-time install on your MacBook (30–40 min) |
| ~~`02-event-indexer.md`~~ | ⛔ SUPERSEDED — see 02b/02c/02d below |
| `02b-event-indexer-v2-CORRECTED.md` | The WORKING indexer guide (`jimenez_indexer_v2.py`) |
| `02c-platform-choice-and-dual-mode.md` | RapidAPI + Highlightly dual quota (200 req/day free) |
| `02d-jimenez-search-targets.md` | Exact matches/dates worth searching + ready commands |
| `03-sourcing-footage.md` | Getting the raw video + the rights playbook |
| `04-auto-cutter.md` | Running the AI cutter (audio peaks + Whisper keywords) |
| `05-vertical-and-captions.md` | 9:16 reframe + burned captions |
| `06-hero-documentary.md` | Producing "WELCOME HOME — The Raúl Jiménez Story" |
| `07-shorts-production.md` | The 8-short slate, one by one |
| `08-publishing-and-reactive.md` | Posting, scheduling, World Cup reactive protocol |
| `09-ai-prompt-library.md` | **Every AI prompt for every step, copy-paste ready** |
| `scripts/` | The 3 working Python tools (indexer, cutter, reframer) |

---

## ✅ THE MASTER CHECKLIST — DO IN THIS ORDER

### 🔥 TODAY (Day 1) — ship before you build
*No pipeline needed. These two shorts are stock-footage + narration, doable with your existing MoneyPrinterTurbo/CapCut flow in ~2 hours.*
- [ ] 1. Read `07-shorts-production.md` → produce **Short #6 "He Never Left Our Hearts"** (announcement reaction) using Prompt 7A from the prompt library
- [ ] 2. Produce **Short #1 "The Shirt Nobody Would Keep"** (Armstrong giving up the No 9) using Prompt 7B
- [ ] 3. Post both: TikTok first, then Shorts, then Reels. Pin a comment question. Reply to every comment for 60 min
- [ ] 4. Tonight: run the setup (`01-setup.md`) while the uploads cook

### ⚙️ DAY 2 — index + source + carousel
- [ ] 5. Get your free RapidAPI key → run the indexer (`02b-event-indexer-v2-CORRECTED.md`, targets in `02d`) → you now have a JSON map of Jiménez matches/highlights/events
- [ ] 6. Source your first raw footage (`03-sourcing-footage.md`) — start with ONE Wolves-era compilation + the announcement-day material
- [ ] 7. Produce **Short #4 "Why He Chose Wolves"** (Prompt 7C) + the **numbers carousel** (Prompt 7G)
- [ ] 8. Start the doc script: run Prompt 6A (research pack) + Prompt 6B (script draft) from the prompt library

### 🤖 DAY 3 — first automated cuts + the emotional banker
- [ ] 9. Run the auto-cutter on your sourced footage (`04-auto-cutter.md`) → inspect the clips it found
- [ ] 10. Reframe the best 3 to vertical + captions (`05-vertical-and-captions.md`)
- [ ] 11. Produce **Short #2 "The Skull Arc"** (Prompt 7D) — your strongest emotional asset. Real-clip opener if your cuts are good, stock narration if not
- [ ] 12. Finish + record the doc voiceover (Prompt 6C for polish, ElevenLabs for voice)

### 🎬 DAY 4 — hero doc launch
- [ ] 13. Assemble the doc (`06-hero-documentary.md`): narration + your auto-cut clips (short, transformed) + stills/stock connective tissue
- [ ] 14. Publish 17:00–19:00 UK + teaser short + first-hour protocol (pin: *"Greatest free transfer in Championship history?"*)

### 📅 DAYS 5–10 — the slate + the machine
- [ ] 15. One short per day from the slate (`07-shorts-production.md` Days 5–7) + poll + newsletter special
- [ ] 16. Batch the **Spanish variants** (Prompt 7H) — Mexican TikTok is your second lottery
- [ ] 17. Set up the **World Cup reactive protocol** (`08-publishing-and-reactive.md`): before every Mexico match, pre-write both outcomes; if Jiménez scores → 30-minute turnaround using the pipeline
- [ ] 18. Wire Postiz/scheduling for the planned posts; keep reactive posts native

---

## ⏱️ TIME BUDGET
| Phase | Time |
|---|---|
| Day 1 ship | ~2.5 h |
| Setup + index | ~1.5 h |
| Doc production | ~4 h across Days 2–4 |
| Daily shorts after | 30–60 min each |
| Reactive WC clip | ≤30 min once pipeline works |

## 🧭 THE THREE RULES OF THIS PROJECT
1. **Emotion ships first, automation second.** Never let a script bug delay a post — fall back to stock + narration.
2. **TikTok/Reels carry the real-clip risk, YouTube gets the transformed doc.** (Full rights logic in `03-sourcing-footage.md`.)
3. **Every Mexico match is a content event.** Calendar them now. Alarm 15 min before kickoff and at full-time.
