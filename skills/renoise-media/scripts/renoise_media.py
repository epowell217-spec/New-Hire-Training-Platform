#!/usr/bin/env python3
"""Call Bloome's authenticated Renoise media proxy."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import pathlib
import sys
import time
import uuid
import urllib.error
import urllib.parse
import urllib.request


USER_AGENT = "BloomeAgent/1.0 (renoise-media)"
TERMINAL_STATUSES = {"completed", "failed", "cancelled"}
TOPUP_REQUIRED = "topup_required"

MODE_ALIASES = {
    "text_to_image": "text_to_image",
    "t2i": "text_to_image",
    "image_edit": "image_edit",
    "edit": "image_edit",
    "text_to_video": "text_to_video",
    "t2v": "text_to_video",
    "image_to_video": "image_to_video",
    "i2v": "image_to_video",
}

MATERIAL_TYPES = {"image", "video", "audio"}
VIDEO_MODES = {"text_to_video", "image_to_video"}
TEXT_ONLY_MODES = {"text_to_video", "text_to_image"}
MATERIAL_REQUIRED_MODES = {"image_to_video", "image_edit"}
IMAGE_REFERENCE_ROLES = {"reference_image", "ref_image", "first_frame", "last_frame"}
# Models that only support image-to-video (need image references) — mirrors the server.
I2V_ONLY_MODELS = {"kling-3.0-omni", "grok-video-1.5"}


def http_base_from_env() -> str:
    explicit = os.environ.get("RESON_SERVER_URL")
    if explicit:
        return explicit.rstrip("/")

    ws_url = os.environ.get("RESON_SERVER_WS_URL")
    if not ws_url:
        raise SystemExit("missing RESON_SERVER_URL or RESON_SERVER_WS_URL")

    if ws_url.startswith("wss://"):
        base = "https://" + ws_url[len("wss://") :]
    elif ws_url.startswith("ws://"):
        base = "http://" + ws_url[len("ws://") :]
    else:
        base = ws_url
    if base.endswith("/ws/agent"):
        base = base[: -len("/ws/agent")]
    return base.rstrip("/")


def agent_token_from_env() -> str:
    token = os.environ.get("RESON_TOKEN") or os.environ.get("RESON_AGENT_TOKEN")
    if not token:
        raise SystemExit(
            "missing RESON_TOKEN or RESON_AGENT_TOKEN; run in an authenticated Bloome agent shell"
        )
    return token


def http_error_message(prefix: str, exc: urllib.error.HTTPError) -> str:
    error_body = exc.read().decode("utf-8", errors="replace")
    request_id = exc.headers.get("x-request-id")
    request_hint = f"\nx-request-id: {request_id}" if request_id else ""
    # If the server persisted a paid request before failing (e.g. a transient
    # provider error after the credit reservation), it returns a recovery handle in
    # the body. Surface it so the caller polls/replays the SAME request instead of
    # re-submitting and creating a second paid task.
    recovery = ""
    try:
        parsed = json.loads(error_body)
    except (ValueError, TypeError):
        parsed = None
    if isinstance(parsed, dict) and parsed.get("request_id"):
        rid = parsed["request_id"]
        idem = parsed.get("idempotency_key")
        lines = [
            "",
            "RECOVERABLE: this request was already reserved/billed server-side.",
            "Do NOT resubmit (that creates a second paid task). Instead:",
            f"  poll it:   {sys.argv[0]} --request-id {rid}",
        ]
        if idem:
            lines.append(f"  or replay: rerun with --idempotency-key {idem} (returns this same request)")
        recovery = "\n".join(lines)
    return f"{prefix}: HTTP {exc.code}{request_hint}\n{error_body}{recovery}"


def request_json(
    url: str,
    method: str,
    body: dict | None = None,
    timeout: float = 60,
    url_error_hint: str | None = None,
) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    headers = {
        "x-api-key": agent_token_from_env(),
        "content-type": "application/json",
        "user-agent": USER_AGENT,
    }
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise SystemExit(http_error_message("Bloome Renoise proxy failed", exc)) from exc
    except urllib.error.URLError as exc:
        # No HTTP body to carry a recovery handle. If the caller passed a hint
        # (paid submit path), append it so a lost response is still recoverable.
        hint = f"\n{url_error_hint}" if url_error_hint else ""
        raise SystemExit(f"Bloome Renoise proxy failed: {exc.reason}{hint}") from exc


def quote_header_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def upload_file(path: str, timeout: float = 300) -> dict:
    file_path = pathlib.Path(path)
    if not file_path.is_file():
        raise SystemExit(f"material file not found: {path}")

    boundary = f"----BloomeRenoiseBoundary{uuid.uuid4().hex}"
    content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    filename = quote_header_value(file_path.name)
    head = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode("utf-8")
    tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
    body = head + file_path.read_bytes() + tail
    headers = {
        "x-api-key": agent_token_from_env(),
        "content-type": f"multipart/form-data; boundary={boundary}",
        "content-length": str(len(body)),
        "user-agent": USER_AGENT,
    }
    request = urllib.request.Request(
        f"{http_base_from_env()}/api/agent/upload",
        data=body,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise SystemExit(http_error_message("Bloome agent upload failed", exc)) from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Bloome agent upload failed: {exc.reason}") from exc

    key = result.get("key") or result.get("file_key")
    if not isinstance(key, str) or not key:
        raise SystemExit(f"Bloome upload did not return a file key: {json.dumps(result)}")
    return {"file_key": key, "upload": result}


def parse_int(value: str, label: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise SystemExit(f"{label} must be an integer: {value}") from exc
    if parsed < 0:
        raise SystemExit(f"{label} must be non-negative: {value}")
    return parsed


def split_key_value_spec(spec: str, value_key: str) -> dict[str, str]:
    if "=" not in spec and ":" in spec:
        role, value = spec.split(":", 1)
        return {"role": role.strip(), value_key: value.strip()}

    fields: dict[str, str] = {}
    for chunk in spec.split(","):
        part = chunk.strip()
        if not part:
            continue
        if "=" not in part:
            raise SystemExit(
                f"invalid material spec {spec!r}; use role=<role>,{value_key}=<value>"
            )
        key, value = part.split("=", 1)
        fields[key.strip()] = value.strip()
    return fields


def material_from_fields(fields: dict[str, str], source: str, value_key: str) -> dict:
    role = fields.get("role")
    if not role:
        raise SystemExit(f"{source} material is missing role")
    value = fields.get(value_key)
    if not value:
        raise SystemExit(f"{source} material is missing {value_key}")

    material: dict = {"role": role}
    material_type = fields.get("type")
    if material_type:
        if material_type not in MATERIAL_TYPES:
            raise SystemExit(f"invalid material type {material_type!r}; use image, video, or audio")
        material["type"] = material_type

    if value_key == "file_key":
        material["file_key"] = value
    else:
        uploaded = upload_file(value)
        material["file_key"] = uploaded["file_key"]

    if "index" in fields:
        material["index"] = parse_int(fields["index"], "material index")
    return material


def parse_material_specs(args: argparse.Namespace) -> list[tuple[dict[str, str], str, str]]:
    specs: list[tuple[dict[str, str], str, str]] = []
    for spec in args.file or []:
        specs.append((split_key_value_spec(spec, "path"), "--file", "path"))
    for spec in args.material or []:
        specs.append((split_key_value_spec(spec, "file_key"), "--material", "file_key"))
    return specs


def validate_material_specs_for_mode(
    mode: str, model: str, specs: list[tuple[dict[str, str], str, str]]
) -> None:
    if mode in TEXT_ONLY_MODES and specs:
        raise SystemExit(f"{mode} does not accept --file or --material")
    if mode in MATERIAL_REQUIRED_MODES and not specs:
        raise SystemExit(f"{mode} requires at least one --file or --material")

    # i2v-only models must not be used in text_to_* modes (mirrors the server 400).
    if model in I2V_ONLY_MODELS and mode != "image_to_video":
        raise SystemExit(f"{model} only supports --mode image_to_video (needs an image reference)")

    if model == "kling-3.0-omni":
        # i2v with 1–7 image references.
        if not (1 <= len(specs) <= 7):
            raise SystemExit("kling-3.0-omni requires 1 to 7 image materials")
        for fields, _source, _key in specs:
            material_type = fields.get("type")
            if material_type is not None and material_type != "image":
                raise SystemExit("kling-3.0-omni accepts image references only")
        return

    if model != "grok-video-1.5":
        return
    if mode != "image_to_video":
        raise SystemExit("grok-video-1.5 is supported only with --mode image_to_video")
    if len(specs) != 1:
        raise SystemExit("grok-video-1.5 requires exactly one image material")

    fields = specs[0][0]
    material_type = fields.get("type")
    if material_type is not None and material_type != "image":
        raise SystemExit("grok-video-1.5 requires an image material")
    if fields.get("role") not in IMAGE_REFERENCE_ROLES:
        raise SystemExit("grok-video-1.5 requires one image-reference role such as first_frame")


def build_materials(specs: list[tuple[dict[str, str], str, str]]) -> list[dict]:
    materials: list[dict] = []
    for fields, source, value_key in specs:
        materials.append(material_from_fields(fields, source, value_key))
    return materials


def api_mode(mode: str | None) -> str:
    if not mode:
        raise SystemExit("--mode is required when submitting a new request")
    return MODE_ALIASES[mode]


def validate_submit_args(args: argparse.Namespace, mode: str) -> None:
    if not args.model:
        raise SystemExit("--model is required when submitting a new request")
    if not args.prompt:
        raise SystemExit("--prompt is required when submitting a new request")
    if mode in VIDEO_MODES:
        if args.duration is None:
            raise SystemExit("--duration is required for video modes")
        if args.duration < 1 or args.duration > 15:
            raise SystemExit("--duration must be an integer between 1 and 15 seconds")
    elif args.duration is not None:
        raise SystemExit("--duration is only valid for video modes")


def build_submit_body(args: argparse.Namespace) -> dict:
    mode = api_mode(args.mode)
    validate_submit_args(args, mode)
    material_specs = parse_material_specs(args)
    validate_material_specs_for_mode(mode, args.model, material_specs)
    materials = build_materials(material_specs)

    input_body: dict = {"prompt": args.prompt}
    if args.duration is not None:
        input_body["duration"] = args.duration
    if args.ratio:
        input_body["ratio"] = args.ratio
    if args.resolution:
        input_body["resolution"] = args.resolution
    if args.watermark:
        input_body["watermark"] = True
    if args.audio_generation:
        input_body["audio_generation"] = True
    if materials:
        input_body["materials"] = materials

    # Resolve the idempotency key ONCE onto args so it is known/stable even if the
    # HTTP response is later lost (timeout / dropped connection / process killed).
    if not args.idempotency_key:
        args.idempotency_key = str(uuid.uuid4())
    body: dict = {
        "idempotency_key": args.idempotency_key,
        "mode": mode,
        "model": args.model,
        "input": input_body,
    }
    conversation_id = args.conversation_id or os.environ.get("RESON_CONVERSATION_ID")
    thread_root_id = args.thread_root_id or os.environ.get("RESON_THREAD_ROOT_ID")
    if conversation_id:
        body["conversation_id"] = conversation_id
    if thread_root_id:
        body["thread_root_id"] = thread_root_id
    return body


def submit_request(args: argparse.Namespace) -> dict:
    body = build_submit_body(args)
    # Print the key to stderr BEFORE the paid POST. If the response never arrives
    # (timeout / dropped connection / the shell/exec tool kills the process), the
    # caller still has the key: rerun with --idempotency-key <key> to replay the SAME
    # request (no second charge), or poll it once the request_id is known.
    print(
        f"[renoise] submitting idempotency_key={args.idempotency_key} "
        f"(save it — replay with --idempotency-key to recover if the response is lost)",
        file=sys.stderr,
    )
    return request_json(
        f"{http_base_from_env()}/api/agent/media/renoise/tasks",
        "POST",
        body,
        timeout=120,
        url_error_hint=(
            "The request may have been reserved/billed. Do NOT resubmit with a new key; "
            f"replay with --idempotency-key {args.idempotency_key} to recover the same request."
        ),
    )


def status_request(request_id: str) -> dict:
    encoded = urllib.parse.quote(request_id)
    return request_json(
        f"{http_base_from_env()}/api/agent/media/renoise/tasks/{encoded}",
        "GET",
        None,
        timeout=60,
    )


def billing_state(result: dict) -> str | None:
    billing = result.get("billing")
    if not isinstance(billing, dict):
        return None
    state = billing.get("state")
    return state if isinstance(state, str) else None


def annotate_topup_required(result: dict) -> dict:
    result["action_required"] = (
        "Bloome credit balance is insufficient to settle this Renoise generation; "
        "no output is available until the owner tops up and retries or settlement is handled."
    )
    return result


# Cap the poll backoff so a finished task is never left waiting long for the next poll.
POLL_MAX_INTERVAL_S = 20.0
# How often to emit a liveness line to stderr while waiting.
PROGRESS_EVERY_S = 15.0


def wait_for_result(args: argparse.Namespace, request_id: str) -> dict:
    if args.no_wait:
        return {"request_id": request_id, "status": "submitted", "timed_out": False}

    timeout_s = args.timeout_ms / 1000
    started = time.monotonic()
    deadline = started + timeout_s
    latest: dict = {"request_id": request_id, "status": "queued"}
    # The caller owns the shell exec timeout; warn once so an exec timeout shorter than
    # --timeout-ms does not silently kill us mid-wait (SKILL.md documents this trap).
    sys.stderr.write(
        f"[renoise] waiting up to {int(timeout_s)}s for generation; if your exec "
        f"timeout is shorter, re-run with --no-wait and poll separately via --request-id.\n"
    )
    sys.stderr.flush()
    # Gentle exponential backoff: short at first, capped — a multi-minute video should
    # not poll every few seconds, but the cap bounds post-completion latency.
    interval = max(0.5, args.poll_interval_ms / 1000)
    next_progress = started + PROGRESS_EVERY_S
    while time.monotonic() < deadline:
        latest = status_request(request_id)
        if billing_state(latest) == TOPUP_REQUIRED:
            return annotate_topup_required(latest)
        status = str(latest.get("status", "")).lower()
        if status in TERMINAL_STATUSES:
            return latest
        now = time.monotonic()
        # Periodic liveness so a long generation does not look hung.
        if now >= next_progress:
            sys.stderr.write(
                f"[renoise] still generating... {int(now - started)}s elapsed "
                f"(status={status or 'queued'})\n"
            )
            sys.stderr.flush()
            next_progress = now + PROGRESS_EVERY_S
        time.sleep(min(interval, max(0.0, deadline - now)))
        interval = min(interval * 1.5, POLL_MAX_INTERVAL_S)

    latest["timed_out"] = True
    return latest


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""examples:
  text-to-image:
    python3 scripts/renoise_media.py --mode text_to_image --model gpt-image-2 --prompt "..." --resolution 1k

  text-to-video:
    python3 scripts/renoise_media.py --mode t2v --model sd-2.0-mini --prompt "..." --duration 5 --resolution 720p

  image-to-video with upload:
    python3 scripts/renoise_media.py --mode i2v --model grok-video-1.5 --prompt "..." --duration 5 --file role=first_frame,path=./start.png,type=image,index=0

  poll existing request:
    python3 scripts/renoise_media.py --request-id 00000000-0000-0000-0000-000000000000
""",
    )
    parser.add_argument(
        "--request-id",
        help="poll an existing Bloome Renoise request instead of submitting a new paid task",
    )
    parser.add_argument("--mode", choices=sorted(MODE_ALIASES))
    parser.add_argument("--model")
    parser.add_argument("--prompt")
    parser.add_argument("--duration", type=int, help="video duration in seconds, 1-15")
    parser.add_argument(
        "--ratio",
        help="aspect ratio; allowed values are PER-MODEL (see the model table in SKILL.md). "
        "Omit to use the model default. A value the model does not allow is a hard 400.",
    )
    parser.add_argument(
        "--resolution",
        help="resolution; allowed values are PER-MODEL (see SKILL.md). Images use 1k/2k/4k, "
        "video uses 480p/720p/1080p/4k, and some models (midjourney) take none. Omit for the default.",
    )
    parser.add_argument(
        "--file",
        action="append",
        metavar="SPEC",
        help=(
            "upload a local material; format role=<role>,path=<path>,type=<image|video|audio>,index=<n> "
            "or shorthand role:path"
        ),
    )
    parser.add_argument(
        "--material",
        action="append",
        metavar="SPEC",
        help=(
            "use an existing Bloome file key; format "
            "role=<role>,file_key=files/<key>,type=<image|video|audio>,index=<n> "
            "or shorthand role:files/<key>"
        ),
    )
    parser.add_argument(
        "--idempotency-key",
        help=(
            "retry-safe key; defaults to a fresh uuid per submit. Reuse only for "
            "the same exact request."
        ),
    )
    parser.add_argument("--watermark", action="store_true")
    parser.add_argument("--audio-generation", action="store_true")
    parser.add_argument("--timeout-ms", type=int, default=600_000)
    parser.add_argument("--poll-interval-ms", type=int, default=5_000)
    parser.add_argument("--no-wait", action="store_true")
    parser.add_argument("--conversation-id")
    parser.add_argument("--thread-root-id")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    # `--no-wait` only makes sense for a fresh submit ("fire and poll later"). In
    # explicit poll mode (`--request-id`) it would fabricate a synthetic
    # `{"status":"submitted"}` and exit 0 without ever calling the server, hiding real
    # completed/failed/topup_required state. Reject the contradiction outright.
    if args.request_id and args.no_wait:
        raise SystemExit(
            "--no-wait cannot be combined with --request-id; polling an existing "
            "request always contacts the server. Drop --no-wait to poll."
        )
    # Guard polling knobs: zero/negative values otherwise cause an immediate synthetic
    # timeout, a tight zero-sleep poll loop, or a divide/sleep traceback.
    if args.timeout_ms <= 0:
        raise SystemExit("--timeout-ms must be a positive integer")
    if args.poll_interval_ms <= 0:
        raise SystemExit("--poll-interval-ms must be a positive integer")
    if args.request_id:
        result = wait_for_result(args, args.request_id)
    else:
        submit_result = submit_request(args)
        request_id = submit_result.get("request_id")
        if not isinstance(request_id, str) or not request_id:
            raise SystemExit(
                f"Bloome Renoise proxy did not return request_id: {json.dumps(submit_result)}"
            )
        result = wait_for_result(args, request_id)
        if args.no_wait:
            result.update(
                {
                    "provider": submit_result.get("provider", "renoise"),
                    "model": submit_result.get("model"),
                    "mode": submit_result.get("mode"),
                    "quoted_credit": submit_result.get("quoted_credit"),
                    "quoted_micro_dollars": submit_result.get("quoted_micro_dollars"),
                }
            )
            # Preserve a submit-time billing signal so --no-wait still surfaces
            # topup_required (output withheld) instead of exiting 0 silently. The
            # server returns this block on the initial submit AND on replay.
            submit_billing = submit_result.get("billing")
            if isinstance(submit_billing, dict):
                result["billing"] = submit_billing
                if billing_state(result) == TOPUP_REQUIRED:
                    annotate_topup_required(result)
            # Preserve a submit-time TERMINAL status (the provider can reject a task
            # in the immediate submit response) so --no-wait surfaces failed/cancelled
            # and exits non-zero instead of fabricating a bare "submitted".
            submit_status = str(submit_result.get("status", "")).lower()
            if submit_status in {"failed", "cancelled", "canceled"}:
                result["status"] = "cancelled" if submit_status != "failed" else "failed"

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if billing_state(result) == TOPUP_REQUIRED:
        return 3
    if result.get("timed_out"):
        return 2
    status = str(result.get("status", "")).lower()
    if status in {"failed", "cancelled"}:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
