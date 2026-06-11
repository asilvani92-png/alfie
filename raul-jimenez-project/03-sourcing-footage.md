# 🎞️ PART 3 — SOURCING FOOTAGE + THE RIGHTS PLAYBOOK
**Read this whole doc once before downloading anything. It decides what goes on which platform.**

---

## 3.1 WHAT YOU NEED, BY ASSET

| Asset | Footage need |
|---|---|
| Shorts #1, #4, #6, #7 | **None** — stock B-roll + narration (Pexels/Pixabay: "wolf", "stadium night", "gold black", "mexico flag", "molineux exterior") |
| Shorts #2, #3, #5 | Real Jiménez moments — short clips (the skull arc, goals reel, comeback goal) |
| Hero doc | Mix: narration + stills + **brief** real clips + stock connective tissue |
| WC reactive | Whatever exists fastest — even a still + narration beats waiting for video |

## 3.2 SOURCE LIST (best → fallback)
1. **Index MP4s** — anything `[MP4]` from Part 2 → direct candidates for the cutter
2. **Official channel uploads** (Wolves, FIFA, EFL, Fulham, CONCACAF have official YouTube compilations of Jiménez goals) — these are the cleanest visual quality. Use `yt-dlp` to obtain working copies:
   ```bash
   yt-dlp -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 \
     -o "../footage/%(title).50B.%(ext)s" "<VIDEO_URL>"
   ```
   (`--merge-output-format mp4` = always ends .mp4, never .webm; `%(title).50B` = truncates long titles with weird characters. The cutter reads .webm fine too if you forget.)
3. **The announcement-day material** — Wolves' social posts (the "Welcome home" video). Screen-record what you need for reference; on TikTok, **use the native Stitch/repost tools where possible** — in-app reuse is the platform-sanctioned route.
4. **Stills** — match photos via fair-dealing-style commentary use, Ken Burns zoom in CapCut. A still + great narration is often MORE emotional than video (the doc's skull-injury act should be mostly stills + slow zooms anyway — it's tasteful and rights-light).

## 3.3 ⚖️ THE RIGHTS PLAYBOOK (the honest rules of this game)

**The reality:** PL/EFL/FIFA footage is owned and enforced. You cannot make claims/blocks impossible — you can make them *survivable and rare*. The faceless-highlights ecosystem runs on exactly these rules:

### Platform risk ladder
| Platform | Risk | Strategy |
|---|---|---|
| **TikTok** | Lowest | Real-clip shorts live here first. Add "Red Days" FROM THE IN-APP LIBRARY (licensed in-app + joins the sound page) |
| **Instagram Reels** | Low-mid | Same files; in-app music again; IG may occasionally mute — re-post with different track if so |
| **YouTube Shorts** | Mid | Content ID scans Shorts; keep real-clip portions ≤ ~5–7s per clip, narration always on top |
| **YouTube long-form** | Highest | The doc must be TRANSFORMED (below). Expect a claim (revenue share) at worst on a well-made doc; blocks happen when you use long untouched sequences |

### The transformation checklist (YouTube doc)
- [ ] No raw clip runs longer than ~5–7 seconds before a cut/overlay/still
- [ ] **Your narration is continuous** — the footage illustrates YOUR story, never replaces it
- [ ] Stats overlays, maps, your own graphics between clips
- [ ] Stills with Ken Burns zooms wherever a still can carry the beat
- [ ] Total real-footage share of the doc: aim under ~30%
- [ ] Commentary/critique framing in the script ("what this signing MEANS" — analysis, not re-broadcast)
- [ ] Royalty-free music on the YT version (NOT "Red Days" — Content ID flags commercial tracks). Free sources: YouTube Audio Library, Pixabay Music, Uppbeat
- [ ] Publish on the channel you're willing to absorb a claim on; if you're protective of your main brand, this project runs on its own channel (you wanted multiple channels anyway — this is the use case)

### If a claim/block happens
- **Claim (most common):** video stays up, claimant takes the ad revenue. Acceptable — this project's ROI is audience, not AdSense. Move on.
- **Block:** trim/replace the flagged segment in YouTube Studio's editor, or re-cut and re-upload more transformed.
- **Strike (rare with the checklist):** delete the video, take the lesson, never appeal-fight a league. Three strikes kills a channel — hence the secondary-channel rule.

## 3.4 ORGANIZE THE FOOTAGE
```
raul-jimenez-project/
  footage/            # raw downloads (never edit these)
  clips/              # auto-cutter output (per-source subfolders)
  verticals/          # reframed + captioned, ready to post
  stills/             # photos for Ken Burns segments
  music/              # royalty-free tracks for YT
```
```bash
mkdir -p footage clips verticals stills music
```

## 🤖 AI STEPS FOR THIS PART
- **Prompt 3A** (`09-ai-prompt-library.md`): paste a list of the footage you found → AI maps each file to the 8 shorts + doc acts, flags gaps, and suggests the stock-keyword fill for each gap.
- **Prompt 3B**: describe a moment you have NO footage for → AI writes the "stills + narration" treatment for that beat (shot list of zooms, text overlays, narration lines).

**Next →** `04-auto-cutter.md`
