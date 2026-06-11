#!/usr/bin/env python3
"""
JIMENEZ EVENT INDEXER v2 — corrected to the official Highlightly docs
=====================================================================
https://highlightly.net/football-api/documentation/

FIXES vs v1:
  - /highlights & /matches have NO `teamId` param -> uses homeTeamId+awayTeamId
    (two calls, merged) or homeTeamName/awayTeamName.
  - /highlights max limit is 40; /matches max is 100. Responses are enveloped:
    {data: [...], pagination: {...}, plan: {...}} -> parsed properly.
  - Events for finished matches come from /matches/{id} ("events" array),
    NOT a /events endpoint.
  - Saves embedUrl / source / channel fields on highlights.
  - Surfaces plan.message so you can SEE when the free tier hides results.
  - Supports both platforms: RapidAPI key (default) or Highlightly-direct.

Usage:
  export RAPIDAPI_KEY="your-key"
  # optional, if your account is highlightly.net instead of RapidAPI:
  # export HIGHLIGHTLY_PLATFORM="highlightly"

  python3 jimenez_indexer_v2.py --find-teams
  python3 jimenez_indexer_v2.py --team-id 123456 --season 2026
  python3 jimenez_indexer_v2.py --team-name "Wolverhampton Wanderers" --season 2026
  python3 jimenez_indexer_v2.py --match-detail 1002433681
  python3 jimenez_indexer_v2.py --highlights-search "Jimenez"
  python3 jimenez_indexer_v2.py --date 2026-06-11 --league-name "FIFA World Cup"

Output: data/jimenez_index.json (merged on every run)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: pip3 install requests")

PLATFORM = os.environ.get("HIGHLIGHTLY_PLATFORM", "rapidapi").lower()
RAPID_HOST = "football-highlights-api.p.rapidapi.com"


def base_url() -> str:
    return ("https://soccer.highlightly.net" if PLATFORM == "highlightly"
            else f"https://{RAPID_HOST}")


def _clean_key(raw: str | None) -> str | None:
    """Sanitize env keys: strip whitespace/newlines and accidental
    'export VAR=' junk from botched ~/.zshrc lines."""
    if not raw:
        return None
    # take first line only, drop anything after whitespace/newline
    key = raw.strip().splitlines()[0].strip()
    # if someone pasted 'export RAPIDAPI_KEY=abc', salvage the value
    if "=" in key and "export" in key.lower():
        key = key.split("=", 1)[1].strip().strip('"').strip("'")
    return key or None


def platform_key() -> str | None:
    """Each platform has its OWN key (accounts are not synced)."""
    if PLATFORM == "highlightly":
        return _clean_key(os.environ.get("HIGHLIGHTLY_KEY") or os.environ.get("RAPIDAPI_KEY"))
    return _clean_key(os.environ.get("RAPIDAPI_KEY"))
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
INDEX_FILE = DATA_DIR / "jimenez_index.json"
REQUEST_BUDGET = 40  # free tier = 100/day total; protect the quota

_req_count = 0
_plan_msg_shown = False


def api_get(path: str, params: dict | None = None):
    """GET with correct headers, budget guard, retry, envelope passthrough."""
    global _req_count
    if _req_count >= REQUEST_BUDGET:
        print(f"[!] Budget ({REQUEST_BUDGET} req/run) reached — stopping to protect daily quota.")
        return None
    key = platform_key()
    if not key:
        sys.exit("Set your key first:  export RAPIDAPI_KEY='...' (and/or HIGHLIGHTLY_KEY='...')")
    headers = {"x-rapidapi-key": key}
    if PLATFORM != "highlightly":
        headers["x-rapidapi-host"] = RAPID_HOST
    for attempt in range(4):
        try:
            r = requests.get(f"{base_url()}{path}", headers=headers,
                             params=params or {}, timeout=(10, 60))
            _req_count += 1
            remaining = r.headers.get("x-ratelimit-requests-remaining")
            if remaining is not None:
                print(f"    [quota remaining today: {remaining}]")
            if r.status_code == 429:
                wait = 2 ** (attempt + 1)
                print(f"[!] Rate limited, waiting {wait}s ...")
                time.sleep(wait)
                continue
            if r.status_code != 200:
                print(f"[!] {path} -> HTTP {r.status_code}: {r.text[:300]}")
                return None
            return r.json()
        except requests.Timeout:
            wait = 3 * (attempt + 1)
            print(f"[!] Timed out (attempt {attempt+1}/4) — server slow, retrying in {wait}s ...")
            time.sleep(wait)
        except requests.RequestException as e:
            print(f"[!] Network error: {e}")
            time.sleep(2)
    print(f"[!] Giving up on {path} after 4 attempts — try again in a minute, "
          f"or test the same query in the RapidAPI playground to compare.")
    return None


def unwrap(payload) -> list:
    """API list responses are {data:[...], pagination:{...}, plan:{...}}."""
    global _plan_msg_shown
    if payload is None:
        return []
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        plan = payload.get("plan") or {}
        if plan.get("message") and not _plan_msg_shown:
            print(f"    [plan notice] {plan.get('tier','?')}: {plan['message'][:160]}")
            _plan_msg_shown = True
        return payload.get("data", []) or []
    return []


def paged(path: str, params: dict, max_limit: int, max_pages: int = 3) -> list:
    out, offset = [], 0
    for _ in range(max_pages):
        payload = api_get(path, {**params, "limit": max_limit, "offset": offset})
        rows = unwrap(payload)
        if not rows:
            break
        out.extend(rows)
        total = 0
        if isinstance(payload, dict):
            total = (payload.get("pagination") or {}).get("totalCount", 0)
        offset += max_limit
        if offset >= total:
            break
    return out


def load_index() -> dict:
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text())
    return {"teams": {}, "matches": {}, "highlights": {}, "events": {}}


def save_index(index: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(index, indent=2, ensure_ascii=False))
    print(f"[ok] Saved -> {INDEX_FILE}")


def tag_jimenez(h: dict) -> bool:
    text = f"{h.get('title','')} {h.get('description','')}".lower()
    return any(k in text for k in ["jimenez", "jiménez", "raul", "raúl"])


def find_teams() -> None:
    index = load_index()
    for name in ["Wolverhampton Wanderers", "Wolverhampton", "Fulham", "Mexico"]:
        print(f"\n=== /teams?name={name} ===")
        rows = unwrap(api_get("/teams", {"name": name}))
        if not rows:
            print("  (no results)")
            continue
        for t in rows:
            print(f"  id={t.get('id'):<10} {t.get('name')}  [{t.get('type','?')}]")
            index["teams"][str(t.get("id"))] = t
    save_index(index)
    print("\nNOTE: for Mexico pick the NATIONAL team (type usually 'national').")
    print("Next: python3 jimenez_indexer_v2.py --team-id <ID> --season 2026")


def index_team_season(team_id: int | None, team_name: str | None, season: int) -> None:
    """Matches + highlights for a team/season.
    API has no teamId param -> query home and away separately and merge."""
    index = load_index()
    if team_id:
        home_p, away_p = {"homeTeamId": team_id}, {"awayTeamId": team_id}
        label = f"team {team_id}"
    else:
        home_p, away_p = {"homeTeamName": team_name}, {"awayTeamName": team_name}
        label = team_name

    print(f"=== Matches: {label}, season {season} ===")
    matches = (paged("/matches", {**home_p, "season": season}, 100)
               + paged("/matches", {**away_p, "season": season}, 100))
    for m in matches:
        index["matches"][str(m.get("id"))] = m
    print(f"  stored {len(matches)} matches")

    print(f"=== Highlights: {label}, season {season} ===  (limit max 40/page)")
    highlights = (paged("/highlights", {**home_p, "season": season}, 40)
                  + paged("/highlights", {**away_p, "season": season}, 40))
    hits = 0
    for h in highlights:
        h["_jimenez"] = tag_jimenez(h)
        hits += h["_jimenez"]
        index["highlights"][str(h.get("id"))] = h
    print(f"  stored {len(highlights)} highlights ({hits} mention Jimenez)")
    if not highlights:
        print("  [hint] 0 highlights can mean: free-tier league restriction (watch the")
        print("         plan notice above), season number mismatch, or no coverage.")
        print("         Try: --date YYYY-MM-DD for a specific recent match day instead.")
    save_index(index)


def index_by_date(date: str, league_name: str | None) -> None:
    """Date-based pull — most reliable on the free tier for recent matches."""
    index = load_index()
    params = {"date": date, "timezone": "Europe/London"}
    if league_name:
        params["leagueName"] = league_name
    print(f"=== Highlights for {date} {('('+league_name+')') if league_name else ''} ===")
    highlights = paged("/highlights", params, 40)
    hits = 0
    for h in highlights:
        h["_jimenez"] = tag_jimenez(h)
        hits += h["_jimenez"]
        index["highlights"][str(h.get("id"))] = h
        if h["_jimenez"]:
            print(f"  ★ {h.get('title')}  [{h.get('source','?')}]")
    print(f"  stored {len(highlights)} highlights ({hits} mention Jimenez)")
    save_index(index)


def match_detail(match_id: int) -> None:
    """Full match info incl. the events array (goals, cards, VAR...)."""
    index = load_index()
    payload = api_get(f"/matches/{match_id}")
    rows = payload if isinstance(payload, list) else unwrap(payload) or ([payload] if payload else [])
    if not rows:
        print("[!] No match detail returned — check the match id.")
        return
    detail = rows[0] if isinstance(rows, list) else rows
    index["matches"][str(match_id)] = detail
    events = detail.get("events", []) or []
    index["events"][str(match_id)] = events
    print(f"=== {detail.get('homeTeam',{}).get('name','?')} vs "
          f"{detail.get('awayTeam',{}).get('name','?')}  "
          f"({(detail.get('state') or {}).get('score',{}).get('current','-')}) ===")
    if not events:
        print("  (no events array — match may be too old or not covered)")
    for e in events:
        print(f"  {e.get('time','?')}'  {e.get('type','?'):<22} {e.get('player','')}"
              f"{('  (assist: ' + e['assist'] + ')') if e.get('assist') else ''}")
    save_index(index)


def list_stored() -> None:
    """Summarize what's in the local index: leagues + sample titles. No API cost."""
    index = load_index()
    highlights = list(index["highlights"].values())
    print(f"=== Local index summary: {len(highlights)} highlights ===\n")
    by_league: dict = {}
    for h in highlights:
        league = ((h.get("match") or {}).get("league") or {}).get("name", "?unknown?")
        by_league.setdefault(league, []).append(h)
    for league, items in sorted(by_league.items(), key=lambda kv: -len(kv[1])):
        print(f"[{len(items):>3}] {league}")
        for h in items[:3]:
            print(f"       - {h.get('title','?')[:80]}  [{h.get('source','?')}]")
    print("\n[i] If the league you need isn't listed, the free tier is hiding it.")


def search_local(term: str) -> None:
    """Search the LOCAL index (no API calls)."""
    index = load_index()
    print(f"=== Local highlight search: {term} ===")
    found = 0
    for h in index["highlights"].values():
        text = f"{h.get('title','')} {h.get('description','')}".lower()
        if term.lower() in text:
            found += 1
            url = h.get("url") or ""
            kind = "MP4" if url.endswith(".mp4") else ("EMBED" if h.get("embedUrl") else "PAGE")
            print(f"\n[{kind}] [{h.get('type','?')}] {h.get('title')}")
            print(f"  source : {h.get('source','?')}  channel: {h.get('channel','-')}")
            print(f"  url    : {url}")
            if h.get("embedUrl"):
                print(f"  embed  : {h['embedUrl']}")
    print(f"\n{found} matches in local index ({len(index['highlights'])} highlights stored total).")


def run_actions(a) -> None:
    if a.find_teams:
        find_teams()
    elif a.team_id or a.team_name:
        index_team_season(a.team_id, a.team_name, a.season)
    elif a.date:
        index_by_date(a.date, a.league_name)
    elif a.match_detail:
        match_detail(a.match_detail)


def main() -> None:
    global PLATFORM
    p = argparse.ArgumentParser(description="Jimenez indexer v2 (matches official Highlightly docs)")
    p.add_argument("--find-teams", action="store_true")
    p.add_argument("--team-id", type=int)
    p.add_argument("--team-name", type=str)
    p.add_argument("--season", type=int, default=2026)
    p.add_argument("--date", type=str, help="YYYY-MM-DD highlight pull (best on free tier)")
    p.add_argument("--league-name", type=str)
    p.add_argument("--match-detail", type=int, help="match id -> full detail + events")
    p.add_argument("--highlights-search", type=str, help="search the LOCAL index (free)")
    p.add_argument("--list-stored", action="store_true",
                   help="summarize the local index by league (free, no API)")
    p.add_argument("--platform", choices=["rapidapi", "highlightly", "both"],
                   default=os.environ.get("HIGHLIGHTLY_PLATFORM", "rapidapi").lower(),
                   help="which account/quota to use. 'both' runs the query on each "
                        "(2 separate free accounts = 200 req/day combined)")
    a = p.parse_args()

    if a.highlights_search:           # local search needs no platform/API
        search_local(a.highlights_search)
        return
    if a.list_stored:
        list_stored()
        return

    platforms = ["rapidapi", "highlightly"] if a.platform == "both" else [a.platform]
    for plat in platforms:
        PLATFORM = plat
        if len(platforms) > 1:
            print(f"\n################ PLATFORM: {plat.upper()} ################")
        if plat == "highlightly" and not os.environ.get("HIGHLIGHTLY_KEY") \
                and not os.environ.get("RAPIDAPI_KEY"):
            print("[!] No HIGHLIGHTLY_KEY set — skipping highlightly platform.")
            continue
        run_actions(a)
    print(f"\n[i] API requests used this run: {_req_count}")


if __name__ == "__main__":
    main()
