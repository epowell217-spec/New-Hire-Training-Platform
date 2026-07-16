---
name: renoise-media
description: >-
  Load when the user wants Bloome-hosted Renoise media generation or editing through
  Bloome's authenticated proxy: text-to-image, image-edit, text-to-video, or
  image-to-video. Mode selection is intent-based: prompt-only image requests use
  text_to_image, changing or restyling provided images uses image_edit, prompt-only
  video requests use text_to_video, and animating a provided image uses
  image_to_video. Video is billed by duration x resolution and can spend real
  credits, so confirm long or high-resolution renders with the owner before
  submitting. Do NOT use for direct provider API calls, direct Renoise keys, or
  face-consistency Characters flows; Characters are not exposed in this first cut.
version: 2
---

# Renoise Media

## Overview

Use Bloome's server-side Renoise proxy for image and video generation. Do not ask
the user for a Renoise API key. The script authenticates with the current Bloome
agent token, and the server handles provider credentials, request ownership,
credit accounting, idempotency, material uploads, and result rehosting.

Results are rehosted to Bloome storage. Use the stable Bloome URL returned by the
poll response; do not rely on expiring provider URLs.

## Quick Start

Run `scripts/renoise_media.py` from an authenticated Bloome agent shell. The shell
must expose:

- `RESON_AGENT_TOKEN` or `RESON_TOKEN`
- `RESON_SERVER_URL` or `RESON_SERVER_WS_URL`

For cloud sandbox agents, use the normal shell/exec tool; these environment
variables are already available in the sandbox runtime.

For ACP agents, run the script from the authenticated Bloome shell environment.
If the ACP agent is launched through Bloome's bridge/runtime, the same `RESON_*`
variables should be available. If the ACP agent is fully external and does not
have those variables, run the script through `bloome_shell` or the existing
Bloome command surface instead of calling it directly.

**Text-to-image:**

```bash
python3 skills/renoise-media/scripts/renoise_media.py \
  --mode text_to_image \
  --model gpt-image-2 \
  --prompt "a clean product photo of a translucent desk lamp" \
  --ratio 1:1 \
  --resolution 1k
```

**Text-to-video:**

```bash
python3 skills/renoise-media/scripts/renoise_media.py \
  --mode text_to_video \
  --model seedance-2.0-mini \
  --prompt "a paper boat drifts down a rain gutter, slow dolly" \
  --duration 5 \
  --ratio 16:9 \
  --resolution 720p
```

**Image-to-video from a local file:**

```bash
python3 skills/renoise-media/scripts/renoise_media.py \
  --mode image_to_video \
  --model seedance-2.0-mini \
  --prompt "gentle wind moves the curtains, subtle camera push-in" \
  --duration 5 \
  --ratio 16:9 \
  --resolution 720p \
  --file role=first_frame,path=./start.png,type=image,index=0
```

**Image edit from a local file:**

```bash
python3 skills/renoise-media/scripts/renoise_media.py \
  --mode image_edit \
  --model gpt-image-2 \
  --prompt "keep the subject, replace the background with a bright studio set" \
  --ratio 1:1 \
  --resolution 1k \
  --file role=reference_image,path=./source.png,type=image,index=0
```

**Use an existing Bloome file key instead of uploading:**

```bash
python3 skills/renoise-media/scripts/renoise_media.py \
  --mode image_to_video \
  --model grok-video-1.5 \
  --prompt "animate this as a slow cinematic reveal" \
  --duration 5 \
  --resolution 720p \
  --material role=first_frame,file_key=files/example.png,type=image,index=0
```

Poll a previous request without submitting a new paid task:

```bash
python3 skills/renoise-media/scripts/renoise_media.py \
  --request-id <request_id>
```

## Mode Selection

Choose the mode from the user's intent, not only from whether an image is present.

| User intent | Mode |
| --- | --- |
| Create an image from a prompt only | `text_to_image` |
| Edit, transform, restyle, or combine supplied images | `image_edit` |
| Create a video from a prompt only | `text_to_video` |
| Animate one supplied image or use it as the first frame | `image_to_video` |

Aliases are accepted by the script: `t2i`, `edit`, `t2v`, and `i2v`.

## Models

Use only models exposed by the Bloome Renoise route. Use the canonical names below
(they match the route's validation, error messages, and stored records). The `sd-2.0*`,
`renoise-2.0*`, and `youmeng-2.0*` aliases are still accepted and normalized to the
`seedance-2.0*` names, but prefer the canonical form.

Video models:

- `seedance-2.0` (t2v and i2v)
- `seedance-2.0-fast` (t2v and i2v)
- `seedance-2.0-mini` (t2v and i2v)
- `kling-3.0-omni` — **image_to_video only**; requires 1–7 image references (using it
  with `text_to_video` is rejected with a 400 before any charge).
- `grok-video-1.5` — **image_to_video only**; requires exactly 1 image reference.

Image models:

- `gpt-image-2`
- `nano-banana-2`
- `nano-banana-pro`
- `midjourney-v7`
- `seedream-5-0-lite`
- `grok-image`

Image model caveats:

- `nano-banana-2` and `nano-banana-pro` are confirmed for text-to-image only.
  Image edit is unverified for these models in this route; do not use
  nano-banana for `image_edit`. Use `gpt-image-2` for edits.

## Per-Model `--ratio` And `--resolution` (allowed values)

The provider validates `--ratio` and `--resolution` **per model** and rejects an
out-of-range value with a 400 **before** anything is generated. Pass only the values
listed for the model you chose, or **omit the flag** to take the model's default. These
are the values the provider actually honors (kept in sync with the server-side check).

| Model | `--resolution` | `--ratio` |
| --- | --- | --- |
| `gpt-image-2` | `1k` `2k` `4k` | `1:1` `3:2` `2:3` `3:4` `4:3` `16:9` `9:16` `21:9` |
| `nano-banana-2` / `nano-banana-pro` | `1k` `2k` `4k` | `1:1` `2:3` `3:2` `3:4` `4:3` `4:5` `5:4` `9:16` `16:9` `21:9` |
| `midjourney-v7` | **omit** (no resolution) | `1:1` `4:3` `3:4` `16:9` `9:16` `3:2` `2:3` |
| `seedream-5-0-lite` | `2k` `3k` `4k` (default `2k`) | `1:1` `4:3` `3:4` `16:9` `9:16` `3:2` `2:3` `21:9` |
| `grok-image` | `1k` `2k` | `1:1` `3:4` `4:3` `9:16` `16:9` `2:3` `3:2` |
| `seedance-2.0` | `480p` `720p` `1080p` `4k` | `9:16` `16:9` `1:1` `4:3` `3:4` `21:9` |
| `seedance-2.0-fast` / `seedance-2.0-mini` | `480p` `720p` | `9:16` `16:9` `1:1` `4:3` `3:4` `21:9` |
| `kling-3.0-omni` | `720p` `1080p` | `16:9` `9:16` `1:1` (only these three are honored) |
| `grok-video-1.5` | `480p` `720p` | `1:1` `16:9` `9:16` `4:3` `3:4` `3:2` `2:3` |

Rules:

- **Do not send a value outside a model's list** — it is a hard 400, not a fallback. When
  unsure, **omit `--ratio` / `--resolution`** and let the provider default.
- `midjourney-v7` has **no resolution** dimension; never pass `--resolution` to it.
- `kling-3.0-omni` accepts only `16:9` / `9:16` / `1:1`. Other ratios like `4:3` are quietly
  coerced to `16:9`, so do not promise the user `4:3`/`3:4` output on Kling.
- Resolution is a **global** set (`1k 2k 3k 4k 480p 720p 1080p`); a value outside it (e.g.
  `8k`, `1024x1024`) is rejected for every model.

Reference constraints:

- `seedance-2.0` supports up to 9 image references and up to 3 video references;
  `seedance-2.0-fast` / `seedance-2.0-mini` accept image reference materials only in the
  current Bloome route.
- `gpt-image-2` accepts up to 16 reference images; `midjourney-v7` up to 4; `grok-image`
  up to 3.
- `grok-video-1.5` requires exactly one image material for image-to-video;
  `kling-3.0-omni` requires 1–7 image references.
- `text_to_image` and `text_to_video` do not accept file materials.

## Materials

Pass local files with `--file`; the script uploads each file to
`/api/agent/upload` first and sends the returned `file_key` to the Renoise submit
route.

Pass existing Bloome attachment keys with `--material`.

Both flags are repeatable and accept either key-value form or shorthand:

```text
--file role=first_frame,path=./start.png,type=image,index=0
--file first_frame:./start.png
--material role=reference_image,file_key=files/abc.png,type=image,index=0
--material reference_image:files/abc.png
```

Valid material types are `image`, `video`, and `audio`. Always set a role that
matches the mode and model. Common roles are `first_frame`, `last_frame`,
`reference_image`, `reference_video`, and `reference_audio`.

## Cost And Idempotency

Video is billed by duration and resolution. Default to short, moderate-resolution
drafts (`--duration 5`, `--resolution 720p`) unless the user explicitly requests a
longer or higher-resolution result. Confirm before submitting long or high-res
renders such as duration above 5 seconds, `1080p`, or `4k`.

A short video costs roughly **25× one image**, so confirm with the owner before long or
high-resolution renders. Indicative per-model anchors are in
[`references/pricing.md`](references/pricing.md); the authoritative price is always the
`billing.quoted_micro_dollars` returned at submit (the provider locks it, so `final == quoted`).

Every submit sends an `idempotency_key`. The script generates a fresh UUID by
default. Pass `--idempotency-key` only when retrying the same exact request after
losing the response. Do not reuse one key for different generations; the server
will replay the first request.

If polling returns `billing.state == "topup_required"`, the generation has no
output because the owner balance is insufficient to settle the final cost. Stop
polling, report the message, and ask the owner to top up or retry later.

## Timeouts and long jobs

If the script prints `"timed_out": true` (exit code 2), the Renoise task is very
likely still running and **already reserved/billed**. Do **NOT** submit the same
prompt again — that creates a second paid task. Instead poll the existing job by
its returned `request_id`:

```bash
python3 skills/renoise-media/scripts/renoise_media.py \
  --request-id REQUEST_ID
```

Video generation can take minutes. When running through the shell/exec tool, set
the command timeout **longer** than `--timeout-ms`, or submit with `--no-wait` (the
script returns the `request_id` immediately) and poll with `--request-id` afterward,
so the tool does not kill the job while it is still generating.

The script prints the `idempotency_key` to stderr **before** the paid submit. If the
submit response is ever lost (connection dropped, process killed before any output),
the request may already be reserved/billed — do NOT resubmit with a new key. Rerun
with `--idempotency-key <the printed key>` to replay the **same** request (no second
charge). For long paid jobs, prefer passing your own `--idempotency-key` up front.

## Characters

Face-consistency through Renoise Characters is not supported in this first cut.
There is no Bloome route to list or attach Characters yet. Do not tell the agent
to use Characters, do not invent `character_id` materials, and do not claim
identity persistence beyond what the selected model can do with ordinary image
references.

## Output

The script prints JSON. On completion, the important fields are:

- `request_id`: Bloome request UUID.
- `status`: `queued`, `running`, `completed`, `failed`, or `cancelled`.
- `result.video_url`, `result.image_url`, `result.cover_url`, `result.image_urls`:
  stable Bloome URLs when available.
- `billing.state`: `reserved`, `settled`, `refunded`, or `topup_required`.
- `billing.quoted_micro_dollars` and `billing.final_micro_dollars`.

If the script reports an HTTP error, keep the printed `x-request-id` when present.
It lets Bloome server logs be checked directly.

## Deliver to user

A `result.*_url` is a Bloome-hosted media URL — do **NOT** just paste the raw URL as
your reply; deliver the file into the conversation so it renders inline. Download the
result to a local file, then send it:

Set `URL` to the result URL from the JSON (`result.video_url` for video,
`result.image_url` for an image), then download and send it:

```bash
# Video output — save with a video extension:
URL="PASTE result.video_url HERE"
# A result URL may be RELATIVE (e.g. /api/uploads/...) on local/dev servers; if it
# starts with "/", prefix the Bloome server base the skill posts to:
case "$URL" in /*) URL="${RESON_SERVER_URL:-http://localhost:3000}$URL";; esac
curl -sSL "$URL" -o outputs/renoise-result.mp4
bloome-cli send-file outputs/renoise-result.mp4
```

```bash
# Image output — save with an image extension, NOT .mp4:
URL="PASTE result.image_url HERE"
case "$URL" in /*) URL="${RESON_SERVER_URL:-http://localhost:3000}$URL";; esac
curl -sSL "$URL" -o outputs/renoise-result.png
bloome-cli send-file outputs/renoise-result.png
```

Match the file extension to the output type (video → `.mp4`, image → `.png`/`.jpg`);
a wrong extension can make the file render or download incorrectly.

For multiple images (`result.image_urls`), download and `send-file` each. If
`bloome-cli` is not on PATH but `bloome_shell` is available, run it through
`bloome_shell`. Only settled results have output — if `billing.state` is
`topup_required`, there is nothing to deliver until the owner tops up.
