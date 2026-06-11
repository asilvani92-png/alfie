# 🤖 PART 9 — THE AI PROMPT LIBRARY
## Copy-paste prompts for every step. Use any chat AI (Claude / ChatGPT / Gemini).

> **House rules for all prompts:**
> 1. Paste the prompt, then your data where marked `<<< >>>`.
> 2. AI drafts, YOU verify — every fact/number gets checked before publishing.
> 3. If output is generic, reply: *"Sharper. Shorter sentences. More specific. No clichés ('rollercoaster', 'fairytale', 'the beautiful game' are banned)."*

---

## PART 2 PROMPTS — Event indexer

### Prompt 2A — Turn the index into a story map
```
You are a football documentary producer. Below is JSON of highlight clips and
events for Raúl Jiménez (Wolves/Fulham/Mexico). 

1) Rank the 15 highest STORY-VALUE moments (not just goals — drama, emotion,
   context). For each: one-line description, why it matters emotionally, and
   which of these assets it serves best:
   [skull-injury arc short / comeback-goal short / 57-goals reel /
    homecoming doc act 1-5 / World Cup reactive].
2) Flag which entries have direct .mp4 urls vs page links.
3) List the 5 biggest GAPS (moments I likely need but this data doesn't cover).
Output as a table.

DATA:
<<<paste the relevant chunk of data/jimenez_index.json>>>
```

### Prompt 2B — Fix an API/script error
```
This Python script calls the Highlightly Football Highlights API (RapidAPI).
This command failed. Diagnose and give me the minimal patch (changed lines only).

COMMAND: <<<the command you ran>>>
ERROR OUTPUT: <<<paste full error>>>
RELEVANT CODE: <<<paste the function that failed>>>
```

---

## PART 3 PROMPTS — Footage sourcing

### Prompt 3A — Map footage to assets
```
I'm producing 8 shorts + 1 documentary about Raúl Jiménez's return to Wolves
(June 2026). Below is my footage inventory. Map each file to the assets it
serves, identify gaps, and for every gap give me: (a) a stills+narration
treatment, or (b) 4 stock-footage search keywords that could cover the beat.

ASSETS: [#1 shirt gesture, #2 skull arc, #3 57-goals reel, #4 why he chose
Wolves, #5 comeback goal, #6 announcement reaction, #7 debate, #8 WC reactive,
DOC acts 1-5 (rise/fall/road/redemption/homecoming)]

MY FOOTAGE:
<<<list filenames + 1-line description of each>>>
```

### Prompt 3B — Stills + narration treatment for a missing moment
```
I have NO video footage of this moment but need it as a 20-30 second beat in
an emotional football documentary: <<<describe the moment>>>.

Write the treatment: 
1) Shot list using only still photos (describe each still + the Ken Burns
   move: zoom in/out, pan direction, duration)
2) The exact narration lines over each still (slow, documentary register)
3) One text overlay if needed
4) Music/silence direction.
```

---

## PART 4-5 PROMPTS — Cutting & packaging clips

### Prompt 4A — Rank clips + write hooks/captions
```
You are a short-form football editor who understands TikTok retention.
Below: an auto-generated clip report (timestamps + scores) and the commentary
lines detected near each clip. For each clip:
1) Emotional value score 1-10 with one-line reason
2) Which asset it serves [#2/#3/#5/reactive/doc/none]
3) HOOK TEXT for the first 1.5 seconds (max 9 words, curiosity or emotion)
4) One caption per platform (TikTok: punchy+question / Reels: emotive /
   Shorts: search-keyword-rich)
Output: table.

CLIP REPORT: <<<paste clips_report.json>>>
COMMENTARY HITS: <<<paste the keyword-hit lines from the cutter output>>>
```

### Prompt 4B — Tune a bad cutter run
```
My auto-cutter (audio RMS peaks + Whisper keyword spotting, flags: --top N,
--pre s, --post s, --keywords list, weights 0.5*audio+0.8*keywords) produced
these problems on this footage: <<<describe what it missed/got wrong, and
what the footage is (full match? compilation? language of commentary?)>>>.
Recommend exact flag/keyword changes to re-run with, and explain why in one
line each.
```

### Prompt 5A — Full caption/hashtag/pin pack for finished verticals
```
For each finished clip below, give me the complete posting pack:
1) Hook text overlay (≤9 words)
2) TikTok caption (hook + question, ≤120 chars) + 5 hashtags from this bank:
   #RaulJimenez #Wolves #WWFC #WelcomeHome #FootballTok #Mexico #ElTri
   #SeleccionMexicana #Mundial2026 #Championship #PremierLeague #FootballStories
3) Reels caption (more emotive, 1-2 lines) + 6 hashtags
4) Shorts title (≤60 chars, search-keyword first: "Raul Jimenez...")
5) Pinned comment question
Tone: emotional but never cheesy. UK football-native voice.

CLIPS: <<<list: filename + what happens in it + which asset>>>
```

---

## PART 6 PROMPTS — The documentary

### Prompt 6A — Research pack (run FIRST)
```
Build me a verified fact sheet on Raúl Jiménez for a documentary, organized
into these sections. For each fact, note if you're uncertain so I can verify:
1) Wolves spell 2018-2023: arrival, loan→permanent, goals/apps (57 in 166),
   best moments, Europa League run, celebrations/iconography (sombrero, mask)
2) The injury: date, match, what happened, recovery timeline, the 196 days,
   COVID-era Molineux details, the protective headgear
3) Comeback: first goal back (match, date, reaction)
4) Decline + Fulham move 2023 (fee ~£5m), Fulham record (31 in 115),
   2025-26 season role
5) The return: 9 June 2026 details — free transfer, 2yr+1 deal, No 9 / Adam
   Armstrong gesture, chairman Nathan Shi quote, Rob Edwards quote, the
   "never left our hearts" tweet, 150th anniversary, relegation context
6) Mexico: caps/goals (124/45), 2026 home World Cup context
Format: bullet facts with dates. No prose.
```

### Prompt 6B — Script draft
```
You are writing an 8-10 minute YouTube documentary narration:
"WELCOME HOME — The Raúl Jiménez Story." 1,200-1,400 words.

STRUCTURE (locked):
- COLD OPEN 60-80 words: start with the November 2020 hospital stakes, smash
  to the June 2026 homecoming. No channel intro.
- ACT 1 The Rise / ACT 2 The Fall / ACT 3 The Long Road / ACT 4 Redemption /
  ACT 5 The Homecoming — each act ends with a one-line open loop.
- PAYOFF: land on "Football rarely gives you a perfect ending. This might be
  one." (may rephrase slightly)
- CTA: question to comments + subscribe line, ≤30 words.

RULES: present tense for drama moments. Short sentences. Specific numbers
over adjectives. Mark visuals per paragraph as [CLIP]/[STILL]/[STOCK].
Re-hook every 60-90 seconds. Banned words: rollercoaster, fairytale,
emotional rollercoaster, the beautiful game, testament.

FACTS (use ONLY these):
<<<paste verified fact pack from Prompt 6A>>>
```

### Prompt 6C — Polish pass
```
Edit this documentary narration. Do not change the structure or facts:
1) Cut 10% of words (kill redundancy)
2) Strengthen the first line of every act (hooks)
3) Flag any sentence longer than 20 words and split it
4) Mark [PAUSE] where the voiceover should breathe (max 6)
5) Make the cold open's first 8 words impossible to scroll past
Return the full revised script.

SCRIPT: <<<paste Prompt 6B output>>>
```

### Prompt 6D — Packaging (title/description/chapters/tags)
```
For this YouTube documentary about Raúl Jiménez's 2026 return to Wolves:
1) 5 title options ≤60 chars (mix: emotional / curiosity / search-led —
   at least one starting with "Raul Jimenez")
2) Description: first 2 lines hook + keywords ("Raul Jimenez Wolves return,
   Jimenez documentary, Jimenez injury comeback, Wolves 2026"), then chapter
   timestamps template, then CTA + 3 hashtags
3) 15 tags
4) Pinned comment question
5) Thumbnail text ideas (≤4 words each, 5 options)
SCRIPT SUMMARY: <<<paste your final act structure / or the script>>>
```

---

## PART 7 PROMPTS — The shorts slate

### Prompt 7A — Short #6 "He Never Left Our Hearts"
```
Write a 50-second faceless short script (130-145 words) for TikTok about the
Raúl Jiménez return announcement (9 June 2026).
HOOK (line 1, locked): "Grown men cried at a tweet this week. Here's why."
BEATS: 3 years away → Wolves' announcement quote "From Wolverhampton to
Mexico City, he never left our hearts. Welcome home." → why it hits different
(2020 skull injury + the love + 150th anniversary year) → LOOP ending that
ties back to the hook + "Follow — the full story is coming."
RULES: spoken-word rhythm, short lines, one quote max, no hashtags in script.
Then add: 3 text-overlay moments [TEXT: ...] and 4 stock-footage keywords.
```

### Prompt 7B — Short #1 "The Shirt Nobody Would Keep"
```
Same format as before (50s, 130-145 words, faceless narration).
HOOK (locked): "A striker just gave away his shirt number. The reason will
give you chills."
STORY: Adam Armstrong had Wolves' No 9. When he heard Raúl Jiménez was coming
home, he happily handed it over. Explain what the No 9 means at Molineux
(57 goals, the golden mask, the idol years) and why this gesture says
everything about what Jiménez means there.
END: loop line "Some numbers belong to someone." + follow CTA.
Add [TEXT] overlays + stock keywords.
```

### Prompt 7C — Short #4 "Why He Chose Wolves"
```
Same format. HOOK (locked): "He could've gone anywhere. He chose the team
that sang his name to an empty stadium."
ANGLE: free agent at 35, World Cup summer shop window — and he signs for a
RELEGATED Championship club. The answer is 2020: when his skull was fractured,
Molineux (empty, COVID era) sang his name. Tease the full story (doc) without
telling all of it. Loyalty thesis ending: "Loyalty isn't dead. It plays at
Molineux now."
Add [TEXT] overlays + stock keywords.
```

### Prompt 7D — Short #2 "The Skull Arc" (the emotional banker)
```
Same format but 55 seconds (145-155 words) and a more solemn register.
HOOK (locked): "Doctors weren't asking if he'd play football again. They
were asking if he'd be okay."
BEATS: Nov 2020 Emirates collision → fractured skull → the football world
holds its breath → empty Molineux singing his name → the protective mask →
196 days → the comeback → and THIS WEEK: he came home to Wolves.
TONE RULES: reverent, no graphic detail, no "horror" language, hope wins.
End loops to the hook: "...and now nobody's asking questions. They're singing
again." + follow CTA. Add [TEXT] overlays + stills/stock suggestions.
```

### Prompt 7E — Real-clip shorts (#3 and #5) caption-only pack
```
These shorts are REAL footage with minimal narration (the clips carry it).
Give me for each:
1) 1-2 narration lines for the SETUP only (before the clip breathes)
2) Hook text overlay ≤9 words
3) Caption + hashtags per platform (TikTok/Reels/Shorts)
4) Pinned comment
SHORT #3: montage of his best Wolves goals ("57 Goals, One Love Affair",
hook: "They didn't sign a striker in 2018. They signed a heartbeat.")
SHORT #5: the comeback goal after the injury ("196 days after his skull was
fractured... listen to this stadium." — crowd audio is the star).
```

### Prompt 7F — Short #7 debate script
```
Same 50s faceless format. This one is DEBATE energy, not tears.
HOOK (locked): "Everyone laughing at this signing is about to learn what
Molineux already knows."
STRUCTURE: steel-man the cynics (35 years old, Championship, wages) →
counter-punch (31 goals at Fulham, proven at 34, the No 9 culture fit,
promotion missions need leaders, 150th-year storyline) → verdict dodge:
"Ask me in May." → CTA: "Genius signing or heart over head? Comments."
Add [TEXT] overlays + stock keywords.
```

### Prompt 7G — The numbers carousel
```
Write an 8-slide Instagram carousel: "Raúl Jiménez's return in 8 numbers."
Numbers: 57 (Wolves goals) · 166 (apps) · 9 (the shirt, Armstrong gesture) ·
196 (days out after the skull fracture) · 31 (Fulham goals) · 124 (Mexico
caps) · 150 (Wolves' anniversary year) · 1 (homecoming).
Per slide: big number + ≤15-word line that lands it emotionally.
Slide 1 = hook cover ("8 numbers that explain why a city is crying").
Slide 8 = CTA (save + follow + "full documentary on YouTube").
Plus: caption + 8 hashtags.
```

### Prompt 7H — Spanish variants 🇲🇽
```
Adapt these shorts for Mexican football TikTok. NOT literal translation —
rewrite in native Mexican Spanish football voice (think how Mexican fan
accounts actually talk; warm, proud, a little poetic about El Tri).
For each: script (same beats/length), hook overlay, caption + these hashtags
(#RaulJimenez #ElTri #SeleccionMexicana #Mundial2026 + 2 you choose),
pinned comment.
SCRIPTS: <<<paste the English scripts for shorts #2, #4, #6>>>
```

### Prompt 7I — Newsletter special
```
Write a 350-400 word newsletter in "The Untold Story" format:
SUBJECT: "The night an empty stadium sang his name"
Story: COVID-era Molineux, Jiménez recovering from the fractured skull, the
fans' tributes, what that bond meant — ending on the June 2026 homecoming
as the payoff, with a cliffhanger pointing to the full documentary [LINK].
Style: narration-like, short paragraphs, ends with "P.S." asking readers to
reply with their favourite Jiménez moment.
```

---

## PART 8 PROMPTS — Reactive protocol

### Prompt 8A — Match-day dual scripts (run every Mexico match morning)
```
Mexico play <<<opponent>>> today at the 2026 home World Cup. Raúl Jiménez
(who re-signed for Wolves on 9 June, my channel's running story) starts/may
play. Write TWO 120-word reactive short scripts I can finish within 10
minutes of full-time:
SCRIPT A — he scores or stars: hook angle "the man who just came home to
Wolves is having the World Cup of his life", leave <<<>>> slots for the
minute/score/one real detail.
SCRIPT B — quiet game or loss: pivot to a Mexico-story angle that still
threads Jiménez + the homecoming, same slot format.
Both: hook ≤10 words, loop ending, follow CTA. Plus caption + hashtags for
each (TikTok).
```

### Prompt 8B — Spanish subtitle fix for the doc
```
Here is YouTube's auto-translated Spanish subtitle file for my Jiménez
documentary. Fix it: natural Mexican Spanish, correct football terms
(cabezazo, golazo, la Selección...), keep timestamps untouched, keep line
lengths subtitle-safe (≤42 chars/line).
<<<paste .srt content>>>
```

---

## 🔁 THE META-PROMPT (when any output disappoints)
```
Rewrite. Rules: cut 20% of words. Shorter sentences. Replace every generic
phrase with a specific fact or image. The first line must be impossible to
scroll past. Keep the structure and facts identical.
```
