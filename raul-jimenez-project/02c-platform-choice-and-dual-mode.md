# ⚖️ PART 2C — RAPIDAPI vs HIGHLIGHTLY DIRECT (and dual-platform mode)
**Answering: "Is Highlightly direct better for free? Do I need to amend anything to search both?"**

---

## 1️⃣ THE SHORT ANSWER

**It's the SAME API either way** — same endpoints, same data, same free Basic tier (100 requests/day). Highlightly direct (`soccer.highlightly.net`) and RapidAPI (`football-highlights-api.p.rapidapi.com`) are just two doors into the same building.

Confirmed from the official docs:
- Same endpoint names, parameters and JSON responses on both
- Same `x-rapidapi-key` header on both; the `x-rapidapi-host` header is **only** needed via RapidAPI
- **Accounts are NOT synced across platforms** — separate signups, separate keys, separate quotas
- Differences: Highlightly direct offers **custom plans + long-term plan discounts** (RapidAPI doesn't); RapidAPI gives you their familiar hub/playground UI

## 2️⃣ SO WHICH IS "BETTER" FOR FREE?

| Factor | RapidAPI | Highlightly direct | Winner |
|---|---|---|---|
| Free quota | 100 req/day | 100 req/day | tie |
| Data/coverage | identical | identical | tie |
| Testing UI | RapidAPI playground | Redoc docs + own dashboard | mild RapidAPI |
| Future paid upgrade | standard pricing | custom plans + discounts | Highlightly |
| 🏆 **The real play** | — | — | **BOTH: two accounts = 200 req/day free** |

Since accounts aren't synced, registering on **both** platforms legitimately doubles your free daily budget — RapidAPI key for one pool, Highlightly key for the other. For your usage (reactive WC pulls + archive indexing), 200/day means you can index historical seasons AND run match-day reactive pulls on the same day without rationing.

## 3️⃣ WHAT I AMENDED (already done — `jimenez_indexer_v2.py` updated & tested ✅)

The script now has a `--platform` flag:

```bash
--platform rapidapi      # default — uses RAPIDAPI_KEY
--platform highlightly   # uses HIGHLIGHTLY_KEY (falls back to RAPIDAPI_KEY)
--platform both          # runs the SAME query on each platform back-to-back,
                         # merging everything into the same local index
```

### One-time setup for dual mode
1. Create a second free account at **highlightly.net/login** (Basic plan, no card)
2. Copy the API key from the Highlightly dashboard
3. Add it next to your existing key:
```bash
echo 'export HIGHLIGHTLY_KEY="paste-highlightly-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### Usage examples
```bash
# Burn only the RapidAPI quota (default, unchanged behaviour):
python3 jimenez_indexer_v2.py --date 2026-06-11 --league-name "FIFA World Cup"

# Burn only the Highlightly quota (e.g. save RapidAPI for match day):
python3 jimenez_indexer_v2.py --platform highlightly --team-id <WOLVES_ID> --season 2026

# Query both platforms in one go (belt & braces on a big match day):
python3 jimenez_indexer_v2.py --platform both --date 2026-06-11
```

Everything still lands in the same `data/jimenez_index.json` (deduped by highlight/match id), local search (`--highlights-search`) costs zero requests as before, and the per-run safety budget still applies.

## 4️⃣ RECOMMENDED QUOTA STRATEGY (200/day total)

| Pool | Reserve for |
|---|---|
| **RapidAPI (100/day)** | Match-day reactive pulls (WC `--date` + `--match-detail`) — your time-critical lane |
| **Highlightly (100/day)** | Background archive indexing (Wolves/Fulham historical seasons), team lookups, experiments |

Why split rather than always `--platform both`: running both doubles the cost of every query. Use `both` only when a specific query matters enough to double-check (e.g., "did a Jiménez clip land yet?" an hour after full-time). Routine work goes to one pool.

## 5️⃣ DO THE RESULTS DIFFER BETWEEN PLATFORMS?
They shouldn't — it's one backend. If you ever see a difference (one returns clips the other hides), it'd be a plan/coverage quirk, and the `[plan notice]` line the script prints will say so. If you see that, trust whichever shows more and tell me — that would be worth investigating.

## ⚠️ ONE THING THAT DOESN'T CHANGE
Free-tier limitations are identical on both doors: some leagues' results hidden on Basic, VERIFIED clips arrive 1–48h post-match, geo-restriction endpoint locked. Two accounts double your *request budget*, not your *coverage*. If a specific competition stays hidden on both, that's a tier restriction — then the decision is whether one month of a paid plan (cheaper via Highlightly's custom plans, per their docs) is worth it during the World Cup window.
