# Long-form playbook (16:9) — copied from the formats of breakout videos

The owner decided on 18 Oct 2026: **long-form only** (Shorts paused), global English audience, any brand-safe
topic that can get the channel monetised. Topics come from the outlier method in `CLAUDE.md`.
This file is the *format* we copy from the best performers. We copy structure, pacing and packaging — never
their scripts, artwork, thumbnails or exact titles.

## What the winners do (studied 18 Oct 2026 with vidIQ `vidiq_video_watch`)
Studied: "Why Did Human Progress EXPLODE in the Last 100 Years" (8.6K subs, 870K views, AI-labelled, cartoon
stick figures), "What Actually Survived Weimar's Hyperinflation" (1.6K subs, 119K, AI-labelled, engravings +
parallax), thumbnails of 12 money/history outliers.

| Element | What breakout videos do | Our version |
|---|---|---|
| Length | 15–32 min (most 16–28) | **14–18 min** to start (~2,000–2,400 words) |
| Hook (0:00–1:30) | Puts *you* in a scene, then a paradox ("savers ruined, one man owned 1,500 companies"); states the big question + 2–3 open questions the video will answer; ties it to the viewer's money today | Same structure. First 10 s must already show the paradox on screen |
| Chapters | 4–6 chapters, each opens with a question (open loop) and a title card; one recurring metaphor ties them together ("two locks", "the ledger") | 5 chapters + verdict; each chapter = an act of our stage show with a title card; one recurring prop as the metaphor |
| Visual pace | Something changes every **2–4 s**; constant micro-motion (push-in, sliding labels, dust) even on holds | Each spoken sentence = a new beat (prop pops, label, chart step); slow camera push-in on every hold |
| On-screen info | Dates/years in a corner ("YEAR: 1923"), big numbers, timelines, maps, simple charts, comparisons into relatable units ("1 horse = 7 light bulbs"), **source tags** at the bottom | Year badge in a corner, number cards, timelines, maps, charts, price-in-today's-money cards, small source tag on screen for every figure |
| Narration | 130–150 words/min, calm, curious documentary voice, lots of "you", deliberate pauses before reveals | Roger at `--rate +4%` (≈145 wpm), no rushed Shorts pace |
| Sound | Low underscore that swells at reveals; foley for every graphic (paper, typewriter, cash bell, whoosh) | Our ragtime, quieter and slower per chapter; existing SFX on every beat |
| Ending | Callback to the opening scene, an open question, one short CTA, point to a related video | Same; "Which video should we make next? Tell us in the comments." End screen 20 s for YouTube end cards |
| Captions | Word-by-word subtitles, lower third | Captions in the orchestra pit strip at the bottom |

## Packaging (decides whether anyone clicks)
- **Title shapes that win:** "X Had No Y Until [year] — So How/What…?", "What Actually Survived [crisis]",
  "How [empire/family/company] Actually Made Its Money", "What Happened to [person], the Richest Man on Earth?",
  "The ENTIRE History of [company] in N Minutes", "Why Did [big thing] Happen in Just N Years?"
- **Thumbnail pattern:** 2–4 word question or claim in huge bold caps (cream/yellow on a red or black banner,
  top), a small era tag above it ("BEFORE 1913"), one expressive character or face on one side, one money
  visual (notes, coins, gold) on the other. Warm vintage palette — which is already ours. Make it in code
  (`thumbnail.py` per episode, 1280×720) and check it at 320×180 (phone size) before upload.

## Production specifics
- Widescreen engine mode: put `{"format": "wide"}` in the episode's `config.json`; the engine switches to
  1920×1080 with its own stage, curtains and caption lane (see `engine.py`).
- Script: `script.json` scenes ≈ one sentence or two each (3–8 s) so visuals change often. Chapter titles are their
  own short scenes.
- Fact rule unchanged: two independent sources per number, listed in `SOURCES.md`; on-screen source tags.
- Render ≈ 1 h for 15 min; render chapter by chapter if needed.
- Upload: long-form files are too big for raw GitHub (100 MB limit) — see the upload section in `CLAUDE.md`.
