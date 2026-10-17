# The Common Cents — production guide

Malaysian money explainers in a 1930s rubber-hose cartoon style. **YouTube is the priority platform**
(channel "The Common Cents", YouTube channel id `UCHi1aUFPe-cM87lriJhiF9w`, handle is NOT @thecommoncents — that
one belongs to someone else). TikTok (@thecommoncents) is posted **manually by the owner** from a kit we prepare.
The owner has authorised **autonomous weekly production and scheduling on YouTube** (no per-post approval).
Read this whole file before doing anything.

## Non-negotiable rules
1. **Facts:** every number on screen or in the voiceover needs **two independent sources** found that day
   (official sources preferred: DOSM, BNM, MOF, LHDN, Budget documents; reputable news second). If a figure
   can't be confirmed, cut it or reword to something you can confirm. Use "about"/"~" for rounded figures and
   put dates on anything that changes (prices, rates, quotas). Record sources in `episodes/NN-name/SOURCES.md`.
2. **No 3R topics** (race, religion, royalty), no ethnic comparisons, no Bumiputera policy, no party politics or
   election takes, no targeting individuals. Money and policy mechanics only, explained fairly (show both sides
   on contested questions).
3. **AI label on:** every YouTube post sets `"isAiGeneratedContent": true` (and any TikTok post `"isAigc": true`).
4. **No copyrighted characters, logos or music.** Everything is drawn in code; music/SFX are synthesised
   (`audio.py`). Brand names may be mentioned (e.g. Myvi, Grab) but never drawn as logos.
5. **Never delete or edit posts that are already live.** Only create new scheduled posts.
6. If anything blocks you (tool error, unverifiable topic, render bug you can't fix), skip that video, schedule
   the rest, and say so clearly in the run summary.

## Weekly run (scheduled every Sunday)
1. `git pull`. Read `CONTENT_LOG.md` (what's posted, what worked, backlog).
2. **Analytics:** Metricool `getAnalyticsDataByMetrics` for brand `7457468`, TikTok `posts` metrics
   (TKPO02 published, TKPO05 description, TKPO07 views, TKPO08 likes, TKPO09 comments, TKPO10 shares,
   TKPO13 full-watch rate, TKPO15 avg watch time, TKPO9999 engagement) for the last 28 days.
   Append a dated table + 3–5 bullet learnings to `CONTENT_LOG.md`.
3. **Trends:** web-search this week's Malaysian money/economy news and use vidIQ
   `vidiq_instagram_tiktok_outlier_search` (audience: `Culture/Region: Malaysia/Malaysian; Global: false;
   Demographics: young working adults 18-35, personal finance, cost of living;`, last 30 days) to see which money
   topics are over-performing. Prefer timely topics; fall back to the backlog.
4. **Pick the week:** first call Metricool `getScheduledPosts` for the coming Mon–Sat and keep everything already
   scheduled; fill only the free **YouTube** slots so the week has **3 YouTube Shorts** (mix of main episodes,
   45–55 s story format, and the odd quick hit, 15–25 s). If the week is already full, make nothing new.
   **Long-form (8–10 min, 16:9) is NOT automated yet** — the engine has no widescreen mode. Don't make long-form in
   weekly runs until this file says it's ready.
   **Monthly cap:** Metricool's plan allows 20 posts per calendar month (every post counts, any network). Count this month's Metricool posts
   (the "Metricool posts" table in `CONTENT_LOG.md` plus anything in `getScheduledPosts` for the month) and never
   let the month exceed **18**. If a week would cross into the cap, make fewer videos and say so in the summary.
   Count posts by the month they publish in.
   Don't repeat a topic from `CONTENT_LOG.md` unless there's genuinely new news.
5. For each video: research + `SOURCES.md` → `script.json` → voice → `episode.py` → `--preview` stills (look at
   them!) → frame scan (below) → full render → upload version → push → schedule.
6. Commit everything (no big renders — see `.gitignore`), update `CONTENT_LOG.md`, push.
7. Finish with a short summary: what's scheduled when, captions, anything skipped and why, key analytics learnings.

## Posting schedule (Asia/Singapore = Malaysia time)
**YouTube** (Metricool best times for this audience): **4pm daily is the peak**, 10am second; Wed/Thu strongest,
weekends weakest. Default: Shorts **Mon, Wed, Fri at 4pm**; long-form (when ready) every other **Thu 4pm**.
Never two YouTube posts in one day. (Adjust days around posts already scheduled.)
**Always compute weekdays with `date -d YYYY-MM-DD +%a` (and the current Malaysia time with
`TZ=Asia/Kuala_Lumpur date`) — never assume which day a date falls on. Never schedule a slot that has already passed.**
**TikTok** (owner posts manually): suggest 6pm on the same day the Short goes up on YouTube. Re-check `getBestTimeToPostByNetwork` occasionally and adjust.

## Visual style (owner-approved — keep it)
The 1930s rubber-hose stage look (curtains, film grain, Luckiest Guy titles, palette, prop faces, ragtime) is the
brand. Weekly runs must **not** redesign it. Allowed without asking: small, data-driven tweaks (faster first-second
hook frame, pacing, caption wording, new props/backdrops that match the style). Anything bigger — new fonts,
palette, characters, overall look — propose it in the run summary and wait for the owner.
Judge style only on patterns across 10+ videos, not single posts.

## Writing the script (story format — this is what works)
- Hook in the first line: personal, surprising, uses "you" ("You spent 3.5 days in traffic last year").
- Characters/props in a mini story, one twist ("the SUV gets double"), fair "other side", then a **question** to
  the audience. Every ending asks a question and says "Comment below, and follow The Common Cents."
- 8–10 scenes, one idea each, 45–55 s total. Write numbers as words for the voice ("one ringgit ninety-nine") and
  map them back to figures with caption `SUBS`.
- Malaysian English, light local flavour (mamak, Myvi, Causeway). No slang that ages badly.

## Making the video
```bash
cd episodes/NN-name
python3 ../../tools/make_voice.py --rate +28%        # Roger voice; edits script.json → audio/
python3 episode.py --preview                         # one still per scene: preview_<scene>.png
python3 episode.py ep.mp4                            # full render (~5 min) with music + SFX
python3 episode.py ep.mp4 --audio-only               # re-mix sound only
```
- `engine.py`: stage, film look, captions, `run(DRAW, subs=SUBS, sfx=SFX)`. `props.py`: reusable props (burger,
  pump, car(face=…, tall=SUV), banknote/note_rain/notes_fly, moneybag, stamp, price_tag, coin, gauge, train,
  house, station, shop, worker, receipt, shoe, line_chart, seesaw, nasi_lemak, lorry, trolley, end_card…).
  Add new props to `props.py`, not episode files.
- **Layout:** captions sit at `CAPTION_Y = 1000` (screen centre). Keep a clear lane ~930–1080: headlines and main
  visuals at y 200–930, secondary pills/props at y 1080–1540, floor at `FLOOR_Y = 1545`. Curtains cover x < ~110
  and x > ~970. Titles auto-shrink to fit, but keep other elements inside x 130–950.
- Copy an existing episode as a template (02-petrol or 03-jam are the best references). End scenes with
  `end_card(d, t, tf, hero=...)`.
- Props must not crash at tiny scales during pop-in animations: guard with `if s <= 0.05: return`.
- **Frame scan before rendering** (catches crashes mid-render):
  ```python
  # run from the episode folder
  import sys, traceback; sys.argv=["episode.py","--scan"]
  src=open("episode.py").read().replace("run(DRAW, subs=SUBS, sfx=SFX)","")
  g={"__file__":"episode.py"}; exec(compile(src,"episode.py","exec"),g)
  import engine; from PIL import Image, ImageDraw
  for k in range(int(engine.TOTAL*engine.FPS)):
      T=k/engine.FPS; sc=next((s for s in engine.SCENES if s["start"]<=T<s["start"]+s["dur"]),engine.SCENES[-1])
      g["DRAW"][sc["key"]](ImageDraw.Draw(Image.new("RGB",(1080,1920))),T-sc["start"],sc)
  ```
- Audio levels live at the top of `audio.py` (`MUSIC_LEVEL`, `DUCK`, `SFX_LEVEL`); the owner said the first mix was
  too loud, current values are approved — don't raise them.

## Upload + schedule
1. Upload version (< 30 MB, two-pass):
   ```bash
   dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 ep.mp4)
   vb=$(python3 -c "print(int(27.5*8*1024/$dur - 192))")
   ffmpeg -y -i ep.mp4 -c:v libx264 -preset slow -b:v ${vb}k -pass 1 -an -f null /dev/null
   ffmpeg -y -i ep.mp4 -c:v libx264 -preset slow -b:v ${vb}k -pass 2 -pix_fmt yuv420p -c:a aac -b:a 192k \
          -movflags +faststart ../../videos/epNN_name.mp4
   ```
2. Commit + push `videos/epNN_name.mp4`. Public URL:
   `https://raw.githubusercontent.com/thaqif0709/thecommoncents/main/videos/epNN_name.mp4`
3. Metricool `createScheduledPost`, blogId `7457468`, `autoPublish: true`,
   `draft: false`, timezone `Asia/Singapore`, media = the raw URL. TikTok-only fields (only if ever posting to TikTok):
   `tiktokData: {"title": "<short title — required>", "privacyOption": "PUBLIC_TO_EVERYONE", "isAigc": true,
   "disableComment": false, "disableDuet": false, "disableStitch": false, "autoAddMusic": false,
   "commercialContentThirdParty": false, "commercialContentOwnBrand": false, "photoCoverIndex": 0}`.
   Caption: hook line + question + emoji (sparingly) + 5–8 hashtags (#malaysia #duit #ekonomi #fyp + topic tags).
   **YouTube Shorts (default):** providers `[{"network":"youtube"}]`, media = raw URL, `text` = description
   (hook + question + "Educational, not financial advice." + 3–5 hashtags incl. #shorts), and
   `youtubeData: {"title": "<≤70 chars, hook-style, includes the key number>", "type": "short", "privacy": "public",
   "madeForKids": false, "category": "EDUCATION", "tags": [...8–12 keywords incl. malaysia, duit, ekonomi...],
   "isAiGeneratedContent": true}`. Leave `notifySubscribers` out.
4. Confirm each post appears in `getScheduledPosts` and log it in `CONTENT_LOG.md`.
5. **TikTok kit for the owner:** append to `TIKTOK_KIT.md` (newest first) one block per new video: the public raw
   video URL, a TikTok caption (hook + question + 5–8 hashtags), a suggested day/time (6pm), and a pinned-comment
   question. Mention in the run summary that new TikTok kits are ready.
