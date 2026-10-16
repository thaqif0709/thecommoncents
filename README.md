# The Common Cents

Money, explained — 1930s rubber-hose cartoon shorts (TikTok @thecommoncents).

## Layout
- `engine.py` — stage, old-film look, word-timed captions, render loop (`run(DRAW, subs, sfx)`)
- `props.py` — reusable cartoon props (burger, pump, cars, notes, stamp, train, …)
- `audio.py` — procedural ragtime bed, cartoon sound effects, ducked mix (levels at the top)
- `tools/make_voice.py` — narration + word timings from `script.json` (edge-tts)
- `episodes/NN-name/` — `script.json`, `audio/`, `episode.py` (scenes, caption subs, sound cues)
- `videos/` — upload-size MP4s (public links used for scheduling)
- `logo.py` — profile picture

## Make an episode
```bash
cd episodes/NN-name
python3 ../../tools/make_voice.py --rate +28%   # after writing script.json
python3 episode.py --preview                    # one still per scene
python3 episode.py out.mp4                      # full render with music + sfx
python3 episode.py out.mp4 --audio-only         # re-mix sound onto an existing render
```
Requires Python 3 with numpy, Pillow, edge-tts, plus ffmpeg.
