"""Upload a finished video to Cloudflare R2 and print its public URL — with a storage guard.
R2's free tier includes 10 GB of storage; going over it is billed. Before every upload this script totals the bucket:
  - over 8 GB after the upload  -> prints a WARNING (tell the owner in the run summary)
  - over 9.5 GB after the upload -> REFUSES (unless --force), so we never reach the 10 GB billing line by accident
Usage:  python3 tools/r2_upload.py videos/ep07_zimbabwe.mp4 [--key videos/ep07_zimbabwe.mp4] [--force]
        python3 tools/r2_upload.py --status                 # just show usage
        python3 tools/r2_upload.py --prune-days 30 [--yes]  # list (and with --yes delete) videos older than N days
Credentials (env): R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY (or AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY when they are the
32/64-char R2 keys), R2_ENDPOINT (default https://<CLOUDFLARE_ACCOUNT_ID>.r2.cloudflarestorage.com), R2_BUCKET (default
thecommoncents), R2_PUBLIC_URL (the bucket's public r2.dev / custom domain base URL)."""
import argparse, datetime as dt, os, sys
import boto3
from botocore.config import Config

GB = 1024 ** 3
PUBLIC_URL = "https://pub-7a1cea1592884db0a8d119d865487396.r2.dev"   # bucket "thecommoncents" public r2.dev address (not a secret)
FREE_GB, WARN_GB, STOP_GB = 10.0, 8.0, 9.5

def env(*names):
    for n in names:
        if os.environ.get(n): return os.environ[n]
    return None

def client():
    key = env("R2_ACCESS_KEY_ID") or (os.environ.get("AWS_ACCESS_KEY_ID") if len(os.environ.get("AWS_ACCESS_KEY_ID", "")) == 32 else None)
    sec = env("R2_SECRET_ACCESS_KEY") or (os.environ.get("AWS_SECRET_ACCESS_KEY") if len(os.environ.get("AWS_SECRET_ACCESS_KEY", "")) == 64 else None)
    if not key or not sec: sys.exit("R2 credentials not found in this session (need the 32/64-char R2 access key + secret)")
    ep = env("R2_ENDPOINT", "R2_S3_ENDPOINT") or f"https://{os.environ['CLOUDFLARE_ACCOUNT_ID']}.r2.cloudflarestorage.com"
    return boto3.client("s3", endpoint_url=ep, aws_access_key_id=key, aws_secret_access_key=sec, region_name="auto",
                        config=Config(signature_version="s3v4"))

def usage(s3, bucket):
    total, objs = 0, []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket):
        for o in page.get("Contents", []):
            total += o["Size"]; objs.append(o)
    return total, objs

def report(total, n):
    pct = total / (FREE_GB * GB) * 100
    print(f"R2 bucket usage: {total / GB:.2f} GB of {FREE_GB:.0f} GB free ({pct:.0f}%), {n} files")

ap = argparse.ArgumentParser()
ap.add_argument("file", nargs="?")
ap.add_argument("--key")
ap.add_argument("--force", action="store_true")
ap.add_argument("--status", action="store_true")
ap.add_argument("--prune-days", type=int)
ap.add_argument("--yes", action="store_true")
a = ap.parse_args()
bucket = env("R2_BUCKET") or "thecommoncents"
s3 = client()
total, objs = usage(s3, bucket)
report(total, len(objs))

if a.prune_days:
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.prune_days)
    old = [o for o in objs if o["LastModified"] < cutoff and o["Key"].startswith("videos/")]
    for o in old: print(f"  {'deleting' if a.yes else 'would delete'} {o['Key']} ({o['Size'] / GB:.2f} GB, {o['LastModified']:%Y-%m-%d})")
    if a.yes:
        for o in old: s3.delete_object(Bucket=bucket, Key=o["Key"])
        print(f"freed {sum(o['Size'] for o in old) / GB:.2f} GB")
    sys.exit(0)
if a.status or not a.file: sys.exit(0)

size = os.path.getsize(a.file)
after = total + size
print(f"upload: {a.file} ({size / GB:.2f} GB) -> after upload {after / GB:.2f} GB")
if after > STOP_GB * GB and not a.force:
    sys.exit(f"REFUSED: would bring the bucket to {after / GB:.2f} GB (stop line {STOP_GB} GB, billing starts at {FREE_GB} GB). "
             f"Free space first: python3 tools/r2_upload.py --prune-days 30 --yes (videos already on YouTube aren't needed), "
             f"or ask the owner.")
if after > WARN_GB * GB:
    print(f"WARNING: bucket will be at {after / GB:.2f} GB — over {WARN_GB} GB. Tell the owner and prune old videos soon.")
key = a.key or f"videos/{os.path.basename(a.file)}"
ctype = "video/mp4" if a.file.endswith(".mp4") else "application/octet-stream"
s3.upload_file(a.file, bucket, key, ExtraArgs={"ContentType": ctype})
base = env("R2_PUBLIC_URL") or PUBLIC_URL
print("uploaded:", key)
print("public URL:", f"{base.rstrip('/')}/{key}" if base else "(set R2_PUBLIC_URL to print it)")
