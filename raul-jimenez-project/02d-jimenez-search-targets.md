    # 🎯 PART 2D — JIMÉNEZ SEARCH TARGETS
## Exact matches, dates & API queries — what to search, where it lives, and what the API will/won't have

> **Reality check first:** Highlightly's deep coverage skews recent (their own examples start ~2023). Expect: **2023–2026 = good API territory · 2018–2022 = thin/hidden on free tier · pre-2018 = not API material.** That's fine — the doc plan uses stills/narration for old beats and `yt-dlp` for archive footage. The World Cup 2026 only started **today (11 June)**, so there are no Jiménez WC2026 highlights *yet* — his value there is the **reactive pipeline** for upcoming Mexico matches, not the archive.

---

## 🥇 TIER 1 — HIGH API PROBABILITY (2023–2026, query these FIRST)

| Date | Match | Why it matters (asset) | Verified detail |
|---|---|---|---|
| **2025-07-06** | 🏆 **Gold Cup FINAL: Mexico 2–1 USA** | His 27' equalizer en route to the trophy + the **Diogo Jota tribute celebration** (his ex-Wolves teammate died 3 July 2025) — emotional crossover of the Wolves + Mexico story. Doc Act 4 + standalone short | Scored 27', named in team of the tournament, 3 goals that Gold Cup |
| **2025-03 (CNL final vs Panama)** | 🏆 **CONCACAF Nations League FINAL: Mexico 2–1 Panama** | **Both goals incl. a 92nd-minute winner** — "the clutch gene" beat for Act 4 | Tournament top scorer with 5 |
| **2024-09 (3 consecutive PL games)** | Fulham vs **West Ham → Newcastle → Nottingham Forest** | Scored in 3 straight; the Forest goal = **50th PL goal + 100th European club goal** (3rd Mexican ever after Hugo Sánchez & Chicharito) | Sept 2024 |
| **2025-05-18** | Brentford 2–3 Fulham | Goal in Fulham's record PL points season — "resurrected at 34" proof | |
| **2026 June+** | 🌍 **Mexico WC2026 group matches** | LIVE reactive lane — opened at the Azteca yesterday/today | Use date-mode on every match day |

### Ready-made commands (Tier 1)
```bash
rj   # alias: activates .venv + cd /Users/alfie/Downloads/faceless-football/raul-jimenez-project/scripts

# Gold Cup final + Jota tribute (the big one)
python3 jimenez_indexer_v2.py --date 2025-07-06
python3 jimenez_indexer_v2.py --date 2025-07-06 --league-name "CONCACAF Gold Cup"

# Nations League final (Mar 2025 — if date pull is empty, try the season route)
python3 jimenez_indexer_v2.py --date 2025-03-23
python3 jimenez_indexer_v2.py --team-name "Mexico" --season 2025 --platform highlightly

# Fulham 2024-25 era (background pool)
python3 jimenez_indexer_v2.py --team-name "Fulham" --season 2024 --platform highlightly
python3 jimenez_indexer_v2.py --team-name "Fulham" --season 2025 --platform highlightly
python3 jimenez_indexer_v2.py --date 2025-05-18

# Then, free local search:
python3 jimenez_indexer_v2.py --highlights-search "Jimenez"
```

## 🥈 TIER 2 — WORTH ONE PROBE EACH (2021–2022, may be hidden on free tier)

| Date | Match | Why it matters | Verified detail |
|---|---|---|---|
| **2021-09-26** | ⭐ **Southampton 0–1 Wolves** | **THE COMEBACK GOAL** — first goal 336 days after the fractured skull. Solo run, beat Bednarek twice, finished past McCarthy, 61'. Short #5's entire reason to exist | BBC/Sky verified; "Watch out, Jimenez is back!" — Don Goodman commentary line = perfect script quote |
| **2022-11-22 / 11-26 / 11-30** | WC2022: Mexico vs Poland / Argentina / Saudi Arabia | His World Cup return post-injury (barely fit, came on as sub) — the "he never gave up on Qatar" beat | Squad member, limited minutes, no goals |

```bash
python3 jimenez_indexer_v2.py --date 2021-09-26                      # the comeback goal
python3 jimenez_indexer_v2.py --date 2022-11-26 --league-name "FIFA World Cup"  # vs Argentina
```
If these return empty/hidden on both platforms → it's a tier restriction; source via yt-dlp instead (official Wolves YouTube has the Southampton goal).

## 🥉 TIER 3 — DON'T SPEND API REQUESTS (pre-2021: yt-dlp + stills territory)

| Date | Match/Moment | Why it matters (asset) |
|---|---|---|
| **2020-11-29** | Arsenal 1–2 Wolves | ⚠️ The skull fracture (David Luiz collision). **Doc Act 2 — STILLS ONLY, no impact replays (taste rule)** |
| **2020-10-25** | Wolves vs Newcastle | His last goal before the injury — "frozen in time" beat |
| **2019-2020 season** | Europa League run (e.g. Olympiacos R16 pen, Sevilla QF 2020-08-11) | Peak-era proof — Act 1 |
| **2019-04-07** | FA Cup semi: Watford 3–2 Wolves | Scored + the famous **lucha libre mask celebration** — iconic Act 1 imagery |
| **2019-03-16** | Wolves 2–1 Man Utd (FA Cup QF) | Big-scalp era goal |
| **2018-08-11** | Wolves 2–2 Everton | First Wolves goal, day one of the love affair |
| **2018 WC (Jun 17/23/27, Jul 2)** | Mexico's Germany win era — he featured, no goals | Context beat only — one line + a still |
| **2013-10-11** | 🇲🇽 Mexico 2–1 Panama (WC qualifier, Azteca) | THE overhead kick that saved Mexico's 2014 qualification — his national-hero origin story. Gorgeous doc cold-open candidate for the Mexico thread |

**Sourcing for Tier 3:** official Wolves/FIFA/Fulham YouTube channels via yt-dlp (Part 3), plus press stills with Ken Burns. The API simply won't carry 2013–2020 reliably — don't burn quota proving it. One probe on the comeback goal (Tier 2) is the only pre-2023 API spend I'd justify.

---

## 🌍 WORLD CUP ANSWER SPECIFICALLY
- **WC2026:** starts today — nothing to search YET. Your play: `--date` pull after every Mexico match (schedule them in your calendar; the reactive protocol in Part 8 takes over). Highlights will appear 0–48h post-match, UNVERIFIED ones sometimes during the game.
- **WC2022 (Qatar):** he was there but injured — subs' minutes, no goals. Worth ONE probe (command above) for "he dragged himself to Qatar" footage; expect thin results.
- **WC2018 (Russia):** featured in Mexico's famous run (the Germany win) but scored 0. Context beat — not worth API spend.
- **WC2014:** squad member, minimal minutes. Skip.
- His REAL international gold is **not** at World Cups — it's the **2025 Gold Cup final + 2025 CNL final** (Tier 1, recent, API-friendly) and the **2013 Panama overhead kick** (yt-dlp). The narrative writes itself: *"He's won everything with Mexico except the one thing starting now — at home."*

## 📋 SUGGESTED REQUEST BUDGET FOR THIS SWEEP (~30–40 total across 2 platforms)
| Pool | Spend |
|---|---|
| RapidAPI (~15) | Tier 1 date pulls: Gold Cup final, CNL final, 2025-05-18 + today's WC date |
| Highlightly (~20) | Fulham/Mexico season indexes + the 2 Tier 2 probes |
| Reserve | Keep ≥50/day combined free for tonight's/tomorrow's WC reactive pulls |

After the sweep, run the free local search and feed the results to **Prompt 2A** (prompt library) to map clips → assets.
