# 📤 PART 8 — PUBLISHING SYSTEM + WORLD CUP REACTIVE PROTOCOL

---

## 8.1 STANDARD PUBLISHING FLOW (planned content)

**Posting order per short:** TikTok (native) → YouTube Shorts → Instagram Reels. Same file, no watermarks (export clean from CapCut; never download from TikTok to repost).

**Times (UK):** TikTok 19:00 · Shorts 12:00 or 19:00 · Reels 20:00 · Spanish variants 01:00–03:00 (Mexico evening).

**Per-post checklist (5 min):**
- [ ] Caption = hook line + question + hashtag stack (from Prompt 5A output)
- [ ] "Red Days" added in-app (TikTok/Reels) if using
- [ ] Pin the comment question immediately
- [ ] Reply to every comment for 60 min
- [ ] Log the row in the slate scorecard

**Scheduling:** planned/evergreen posts can go through **Postiz** (self-hosted, free) or Metricool free tier across your channels. **Reactive posts are ALWAYS native** — speed + in-app sounds + slightly better distribution.

## 8.2 🚨 THE WORLD CUP REACTIVE PROTOCOL (every Mexico match)

This is where the project compounds. Jiménez is Mexico's striker at a HOME World Cup — every match is a potential lightning strike, and you're holding the rod.

### T-minus (morning of the match)
1. Run **Prompt 8A** → it returns TWO pre-written 120-word reactive scripts:
   - **Script A (he scores/stars):** *"The man who just came home to Wolves is having the World Cup of his life…"*
   - **Script B (quiet game/Mexico story instead):** pivot angle on Mexico/the tournament with a Jiménez thread
2. Pre-pick 4–6 stock visuals + have the announcement-week imagery folder open
3. Set alarms: kickoff −15 min, full-time

### Full-time (the 30-minute turnaround)
```
0–5 min   : Confirm what happened (event feed / indexer):
            python3 jimenez_indexer_v2.py --match-detail <MATCH_ID>
            (find the match id first: --date $(date +%F))
5–10 min  : Paste the right script (A or B) + 2 real details from the match
            into the final cut. Tweak hook to the specific moment.
10–20 min : Build: CapCut template (hook text → narration → stills/stock
            → end card). NO waiting for highlight video — stills win on speed.
20–30 min : Post native to TikTok + Shorts. Reels after. Pin comment.
```

### T+24–48h (the second wave)
- Highlightly adds verified clips 0–48h post-match → run the indexer search, feed any [MP4] through auto-cutter → reframe → publish the **real-footage version** of the moment: *"48 hours ago I told you about this man. Watch what he did."*
- If he scored: link EVERYTHING back to the doc (pinned comments across the slate). A goal = the whole portfolio gets a second life. This is the pre-positioning payoff.

### If the big one happens (Jiménez scores a big WC goal)
Drop all planned content. That day becomes: reactive short (30 min) → follow-up angle (evening) → doc re-push (pin swap + Community post: *"The documentary half a million people need today"*) → next morning: real-clip version. Four assets from one moment.

## 8.3 CROSS-PROMOTION MAP
```
Every short  ──pin──▶  Hero doc
Hero doc     ──end screen──▶ your channel's other docs
Carousel     ──last slide──▶ doc + follow
Newsletter   ──▶ doc + best short of the week
Poll/debate  ──▶ comment war ▶ feature best takes in next short
Spanish posts──▶ same doc (add Spanish subtitle file on YouTube!)
```
**YouTube tip:** upload Spanish subtitles (auto-translate then fix with Prompt 8B) on the doc — it makes the doc surface for Spanish-language search during a Mexican home World Cup. Near-zero effort, whole new audience.

## 8.4 METRICS THAT MATTER (this project only)
| Metric | Target |
|---|---|
| Short published within 24h of the news | ✅ Day 1 (non-negotiable) |
| Reactive turnaround time | ≤30 min from full-time |
| 1 breakout short (>100K) within 10 days | the slate has 3 candidates (#2, #5, #6) |
| Doc retention | >50% (emotion docs over-perform; the bar is high deliberately) |
| Mexican-audience share | visible in analytics by Day 7 → if >15%, double Spanish output |
| Channel strikes | 0 (rights playbook followed) |
