"""Generate narration for an episode: one mp3 + word-timed srt per scene in script.json.
Run from the episode folder:  python3 ../../tools/make_voice.py [--voice en-US-RogerNeural] [--rate +15%]"""
import argparse, asyncio, json, os, subprocess
import certifi
certifi.where = lambda: os.environ.get("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt")   # agent proxy CA
import edge_tts

ap = argparse.ArgumentParser()
ap.add_argument("--voice", default="en-US-RogerNeural")
ap.add_argument("--rate", default="+15%")
ap.add_argument("--pitch", default="+0Hz")
args = ap.parse_args()

async def scene(key, text):
    c = edge_tts.Communicate(text, args.voice, rate=args.rate, pitch=args.pitch, boundary="WordBoundary")
    sub = edge_tts.SubMaker()
    with open(f"audio/{key}.mp3", "wb") as f:
        async for ch in c.stream():
            if ch["type"] == "audio": f.write(ch["data"])
            elif ch["type"] == "WordBoundary": sub.feed(ch)
    open(f"audio/{key}.srt", "w").write(sub.get_srt())

os.makedirs("audio", exist_ok=True)
total = 0.0
for key, text in json.load(open("script.json")):
    asyncio.run(scene(key, text))
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"audio/{key}.mp3"],
                             capture_output=True, text=True).stdout)
    total += d + 0.3
    print(f"{key:8s} {d:5.2f}s")
print(f"total ~{total:.1f}s")
