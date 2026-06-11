# 🗃️ PART 2B — EVENT INDEXER v2 (CORRECTED)
## ⚠️ Replaces `02-event-indexer.md` + `jimenez_indexer.py` — use `jimenez_indexer_v2.py`
**Why: v1 used parameters that don't exist in the real API, so highlights silently saved nothing. Verified against the official docs: highlightly.net/football-api/documentation/**

---

## 🔍 WHAT WAS WRONG (so you understand the fixes)

| v1 assumed | Official API reality | Consequence in v1 |
|---|---|---|
| `/highlights?teamId=...` | **No `teamId` param exists.** Only `homeTeamId`, `awayTeamId`, `homeTeamName`, `awayTeamName`, `matchId`, `leagueName`, `leagueId`, `date`, `season`, `countryCode/Name` | API ignored the filter or errored → **0 highlights saved** |
| `/events` endpoint | **Doesn't exist.** Events live inside `GET /matches/{id}` (the `events` array) and `GET /events/{matchId}` is only for LIVE matches (`Live Events` endpoint) | Event pulls failed |
| `limit=40` for everything | `/highlights` max **40**, `/matches` max **100**, `/teams` max 500 | Wasted requests |
| Response = `{data:[...]}` or bare list, loosely handled | List endpoints return an **envelope**: `{data:[], pagination:{totalCount}, plan:{tier, message}}` — and the free tier puts a **"results might be hidden"** notice in `plan.message` | Parsed inconsistently; plan warnings invisible |
| One base URL | Two platforms: RapidAPI `https://football-highlights-api.p.rapidapi.com` **or** direct `https://soccer.highlightly.net` (accounts NOT synced; `x-rapidapi-host` header only needed on RapidAPI) | Fine, but v2 now supports both |

**Also confirmed from the docs (useful, new):**
- Highlights carry `source` (youtube/twitter/reddit/espn…), `channel` (e.g. an official league channel), and sometimes **`embedUrl`** for direct embedding.
- `VERIFIED` clips = official/reputable sources, uploaded 1–48h after full-time; `UNVERIFIED` = more real-time, may appear during the match, shorter lifetime.
- The free/Basic plan **hides some results** (leagues/coverage restrictions) — that alone can explain "no highlights" even with correct calls.
- Geo-restriction checking (`/highlights/geo-restrictions/{id}`) is **not available on the free plan**.
- `/matches/{id}` events include types: Goal, Own Goal, Penalty, Missed Penalty, Yellow/Red Card, Substitution, VAR variants — your reactive-trigger vocabulary.

---

## ✅ CORRECT USAGE — `jimenez_indexer_v2.py`

### Step 0 — same key, same env var
```bash
export RAPIDAPI_KEY="your-key"          # already in your ~/.zshrc from setup
# Only if your account is on highlightly.net instead of RapidAPI:
# export HIGHLIGHTLY_PLATFORM="highlightly"
```

### Step 1 — find team IDs (now also prints club vs national `type`)
```bash
rj   # alias: activates .venv + cd /Users/alfie/Downloads/faceless-football/raul-jimenez-project/scripts
python3 jimenez_indexer_v2.py --find-teams
```
Pick the **national** Mexico entry, note Wolves' and Fulham's ids.

### Step 2 — index a team season (the corrected call)
v2 automatically queries **homeTeamId then awayTeamId and merges** — that's the documented way to get "all matches/highlights for a team":
```bash
python3 jimenez_indexer_v2.py --team-id <MEXICO_ID> --season 2026
# or by name if you prefer:
python3 jimenez_indexer_v2.py --team-name "Wolverhampton Wanderers" --season 2026
```
Each response now prints your **live remaining quota** (from the `x-ratelimit-requests-remaining` header) and any **plan notice** about hidden results — so you can finally SEE why something returns empty.

### Step 3 — date-based pull (🏆 most reliable on the free tier)
For recent/live coverage (e.g., World Cup match days), filter by **date**, optionally league:
```bash
python3 jimenez_indexer_v2.py --date 2026-06-11 --league-name "FIFA World Cup"
python3 jimenez_indexer_v2.py --date 2026-06-11        # everything that day
```
Jiménez-mentioning highlights are starred ★ live in the output.

### Step 4 — match detail + events (replaces v1's broken /events)
```bash
python3 jimenez_indexer_v2.py --match-detail <MATCH_ID>
```
Prints the score + full timeline (`23' Goal R. Jimenez (assist: ...)`) and stores it in the index. **This is your reactive trigger source.**

### Step 5 — search your local index (zero API cost)
```bash
python3 jimenez_indexer_v2.py --highlights-search "Jimenez"
python3 jimenez_indexer_v2.py --list-stored     # summary by league — shows what the free tier ISN'T hiding
```
Shows per clip: `[MP4 / EMBED / PAGE]`, `VERIFIED/UNVERIFIED`, **source + channel**, url and embedUrl.

> 🧪 **CONFIRMED on your machine (real test, July 2025 Gold Cup final date):** the free
> tier returned 77+ highlights for the date but **zero** from the Gold Cup/Mexico/USA —
> big competitions are hidden on BASIC. Conclusion: **the API = event data + reactive
> triggers + whatever leagues are open; archive clips of big matches = yt-dlp route**
> (which worked first try on the CONCACAF official recap). Run `--list-stored` to see
> your actual coverage, and test `--date <today>` during the World Cup to check if WC
> highlights are open before considering a paid month.

---

## 🌪️ CORRECTED WORLD CUP REACTIVE FLOW (per Mexico match, ~6–10 requests)
```bash
# 1. After full-time — that day's WC highlights, Jimenez auto-starred:
python3 jimenez_indexer_v2.py --date $(date +%F) --league-name "FIFA World Cup"

# 2. Find the Mexico match id in the output/index, then the timeline:
python3 jimenez_indexer_v2.py --match-detail <MATCH_ID>
#    -> "Goal R. Jimenez 67'" = your trigger. Publish the narrated reactive
#       short NOW (stills + narration). Don't wait for video.

# 3. T+24-48h — VERIFIED clips appear; re-run step 1, then:
python3 jimenez_indexer_v2.py --highlights-search "Jimenez"
#    -> [MP4] entries feed auto_cutter.py; [EMBED] entries feed newsletter/site.
```

## 🩺 IF HIGHLIGHTS ARE STILL EMPTY — DIAGNOSIS ORDER
1. **Watch the `[plan notice]` line.** "Some results might be hidden with FREE tier" = the league you want may be excluded from Basic. Test with a league the free tier definitely covers (the docs' own examples use smaller leagues) to confirm your calls work, then decide if the story justifies one month of the PRO tier.
2. **Check the quota line** — `remaining: 0` means you're done for the day (resets daily).
3. **Try `--date` instead of `--season`** — date queries on recent match days are the most consistently populated route.
4. **Remember the upload lag** — VERIFIED clips land 1–48h after full-time. A match that ended an hour ago legitimately has nothing yet.
5. **Old seasons (2018–2023 Wolves era) will be thin or hidden** — that's expected; the doc plan already covers those beats with stills + narration, and `yt-dlp` sourcing handles archive footage (Part 3).

## 📌 HOUSEKEEPING
- `jimenez_indexer.py` (v1) has been DELETED from the project — only v2 exists now.
- The index file is the same (`data/jimenez_index.json`), so anything v1 did save still merges fine.
- v2 is tested: envelope parsing + Jiménez tagging verified ✅; per-run budget still capped at 40 requests to protect your 100/day.
