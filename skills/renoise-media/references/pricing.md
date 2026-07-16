# Renoise media — indicative pricing

**The authoritative price is always the `billing.quoted_micro_dollars` returned at submit.**
The provider locks the quote at submit time, so `final == quoted` — there is no post-hoc
drift. The numbers below are indicative anchors from real production quotes to help you set
owner expectations and pick cheap defaults; do not treat them as exact.

## Anchors (real production quotes)

| Kind | Model | Params | Approx. cost |
| --- | --- | --- | --- |
| Image | `gpt-image-2`, `grok-image` | `text_to_image` / `image_edit`, 1k | **~$0.06** per image |
| Video | `seedance-2.0-fast` | 5s @ 720p | **~$1.60** per clip |

## Rules of thumb

- A short (5s / 720p) video is roughly **25× the cost of one image**.
- Video cost scales up with `--duration` and higher `--resolution` (`1080p`, `4k`).
- Because a single video can spend real owner credits, **confirm with the owner before a
  long or high-resolution render**, and prefer a 5s / 720p draft first.
- Other video models (`seedance-2.0`, `seedance-2.0-mini`, `kling-3.0-omni`,
  `grok-video-1.5`) and other image models (`nano-banana-2`, `nano-banana-pro`,
  `midjourney-v7`, `seedream-5-0-lite`) have their own provider pricing — **read the
  returned quote** rather than assuming it matches the anchors above.

## How to see the exact price

1. Submit the job; the response carries `billing.quoted_micro_dollars`.
2. `quoted_micro_dollars / 1_000_000` = USD. (e.g. `1_600_000` → `$1.60`.)
3. On completion, `billing.final_micro_dollars` equals the quote (locked at submit).
