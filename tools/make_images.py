"""Generate an episode's painted scenes with Cloudflare Workers AI (FLUX.2 klein). Run from the episode folder:
    python3 ../../tools/make_images.py [--max 45] [--model klein-4b|klein-9b|dev] [--only key1,key2] [--redo]
Reads images.json ({key: prompt}), writes images/<key>.jpg (1920x1080). Skips keys that already exist unless --redo.
Needs env CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID. Prints neurons used (free tier = 10,000/day)."""
import argparse, base64, io, json, os, sys, time
import requests
from PIL import Image

MODELS = {"klein-4b": "@cf/black-forest-labs/flux-2-klein-4b", "klein-9b": "@cf/black-forest-labs/flux-2-klein-9b",
          "dev": "@cf/black-forest-labs/flux-2-dev"}
ap = argparse.ArgumentParser()
ap.add_argument("--max", type=int, default=45, help="max images this run (stay under the free daily budget)")
ap.add_argument("--model", default="klein-4b", choices=MODELS)
ap.add_argument("--only", default="")
ap.add_argument("--redo", action="store_true")
ap.add_argument("--budget", type=int, default=8000, help="stop before this many neurons are used this run")
args = ap.parse_args()

acct, tok = os.environ.get("CLOUDFLARE_ACCOUNT_ID"), os.environ.get("CLOUDFLARE_API_TOKEN")
if not acct or not tok: sys.exit("CLOUDFLARE_ACCOUNT_ID / CLOUDFLARE_API_TOKEN not set in this session")
url = f"https://api.cloudflare.com/client/v4/accounts/{acct}/ai/run/{MODELS[args.model]}"
prompts = json.load(open("images.json"))
os.makedirs("images", exist_ok=True)
keys = [k for k in (args.only.split(",") if args.only else prompts) if k]
todo = [k for k in keys if args.redo or not os.path.exists(f"images/{k}.jpg")]
print(f"{len(todo)} to make ({len(keys) - len(todo)} already exist), model {args.model}, max {args.max}")

used, made = 0.0, 0
for k in todo[:args.max]:
    t0 = time.time()
    for attempt in range(3):
        try:
            r = requests.post(url, headers={"Authorization": f"Bearer {tok}"}, timeout=180,
                              files={"prompt": (None, prompts[k]), "width": (None, "1920"), "height": (None, "1088")})
            if r.status_code == 200: break
            print(f"  {k}: HTTP {r.status_code} {r.text[:200]}")
            if r.status_code in (400, 401, 403, 429) or "allocation" in r.text.lower() or "limit" in r.text.lower():
                sys.exit("stopping: auth error or daily free allowance used up (try again later)")
        except requests.RequestException as e:
            print(f"  {k}: {e}")
        time.sleep(3 * (attempt + 1))
    else:
        print(f"  {k}: giving up"); continue
    img = Image.open(io.BytesIO(base64.b64decode(r.json()["result"]["image"]))).convert("RGB")
    if img.size != (1920, 1080):                                       # klein rounds height to 1072/1088
        s = max(1920 / img.width, 1080 / img.height)
        img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
        x, y = (img.width - 1920) // 2, (img.height - 1080) // 2
        img = img.crop((x, y, x + 1920, y + 1080))
    img.save(f"images/{k}.jpg", quality=88)
    n = float(r.headers.get("cf-ai-neurons", 0) or 0); used += n; made += 1
    print(f"  {k}: ok {time.time() - t0:.1f}s, {n:.0f} neurons (run total {used:.0f})", flush=True)
    if used >= args.budget: print("budget reached for this run"); break
left = [k for k in keys if not os.path.exists(f"images/{k}.jpg")]
print(f"made {made}, neurons this run {used:.0f}; still missing {len(left)}: {', '.join(left[:20])}")
