# Cloudflare Workers AI: text-to-image test (18 Oct 2026)

Both secrets were present (`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`) and the token worked: every model returned an image.
Endpoint: `POST https://api.cloudflare.com/client/v4/accounts/<ID>/ai/run/<model>`, `Authorization: Bearer <token>`.

Prompt: *"detailed painted documentary illustration, warm muted colours, a crowded city street market in 2008, people
carrying huge stacks of paper banknotes, empty shop shelves, cinematic lighting, no text"*

| Model | Request | Output | Time | Neurons* (cost) | Prompt-following / quality (judged by eye) |
|---|---|---|---|---|---|
| `@cf/black-forest-labs/flux-2-klein-9b` | multipart, 1920×1080 | **1920×1072** | 3.4 s | 1,541 | **Best all-rounder.** Clear bundled banknote bricks carried in arms, sparse shelves, modern 2008 clothing, warm painted look. Some gibberish shop signs. |
| `@cf/black-forest-labs/flux-2-dev` | multipart, 1920×1080 | **1920×1080** | 18.5 s | 14,832 | Most cinematic: strong light, clearly **empty shelves**, people carrying piles of notes (notes look a bit like loose paper). Over the whole free daily allowance in one image. |
| `@cf/black-forest-labs/flux-2-klein-4b` | multipart, 1920×1080 | 1920×1072 | 13.2 s | 206 | Very good and very cheap. Banknote stacks on stalls and in hands, rich painted style. Shelves still stocked; prominent gibberish signs. |
| `@cf/leonardo/phoenix-1.0` | JSON, 1920×1080 | 1920×1080 | 9.5 s | ~6,500 (est.: 12 tiles × 530 + steps; no header returned) | Lovely loose painterly style, people carrying huge stacks, but they read as **paper/newspapers, not money**. Shelves not empty. |
| `@cf/leonardo/lucid-origin` | JSON, 1920×1080 | 1920×1080 | 7.3 s | 6,503 | Dense crowd with money stacks on tables, but looks 1940s (coats, hats), nobody carries money, shelves full, fake signature in corner. Weak prompt-following. |
| `@cf/black-forest-labs/flux-1-schnell` | JSON, `steps: 8` | 1024×1024 only (square) | 3.1 s | 326 | Good painted look and people carrying note stacks, but square, has a torn-paper border, shelves stocked, gibberish signs. |
| `@cf/bytedance/stable-diffusion-xl-lightning` | JSON, 1344×768 | 1344×768 | 5.2 s | 0 (beta, free) | Weakest: flat comic look, boxes of paper, lots of garbled lettering. |

\* Neurons = the `cf-ai-neurons` response header. JSON models return `result.image` (base64); the flux-2 models need
`multipart/form-data` (fields `prompt`, `width`, `height`) and also return `result.image` base64. Klein models round
height to a multiple of 16 (1072), so crop/scale to 1080 when using them.

## Limits and pricing (Cloudflare docs, pricing page dated 15 Oct 2026)
- **Free allocation: 10,000 neurons per day** (Workers Free and Paid). Above that you need Workers Paid at **$0.011 per 1,000 neurons**.
- What 10,000 free neurons buys per day: klein-4b ≈ 48 images, flux-1-schnell ≈ 30, **klein-9b ≈ 6**, lucid-origin/phoenix ≈ 1, flux-2-dev 0 (one image is ~1.5 days of allowance). SDXL-lightning is currently priced at 0.
- On Paid, per 16:9 image: klein-4b ≈ $0.002, klein-9b ≈ $0.017, phoenix/lucid ≈ $0.07, flux-2-dev ≈ $0.16.
- This test used ~30,000 neurons in total and all calls still succeeded, so either the account is on Workers Paid or the daily cap is not enforced instantly. Worth checking in the Cloudflare dashboard.

## Recommendation
- **Default: `flux-2-klein-9b`** for 16:9 documentary illustrations: best prompt-following (actual banknotes, carried, modern setting), native ~1080p, 3–4 s per image. ~6 free images a day, or about 2 cents each on Paid.
- **Bulk/cheap: `flux-2-klein-4b`** (≈48 free a day) when a long-form video needs many background plates; quality is close to 9b.
- **Hero shots/thumbnails only: `flux-2-dev`**: best lighting and mood, but it costs ~15k neurons per image.
- Skip lucid-origin, phoenix, schnell (square) and SDXL-lightning for this use.
- All models write fake lettering on signs even with "no text": add "blank signs" to prompts or cover signs with our own captions. Images are AI-generated, so keep the YouTube AI label on (rule 3).
