---
name: bloome-browser
description: >-
  Drive a real, visible, login-capable browser on the user's desktop (Bloome Browser trusted host
  window), for sites that need a real browser / the user's login / a residential IP (Xiaohongshu, Taobao,
  login-gated dashboards, anti-bot sites). Use when the user asks you to "open / check / search a website"
  and plain web_fetch can't get it (needs login or is anti-bot). Triggers: open a page, look something up,
  search, log in, browse for me, 打开网页、查一下、搜一下、登录、帮我看看、小红书、浏览器操作.
version: 2
# Gray-release gating (any signal present = injected + listed in <available_skills>; none = neither
# materialized nor visible):
#   - desktop local agent: BLOOME_BROWSER_SOCKET (broker socket ready, i.e. the local execution path is up)
#   - cloud sandbox agent: BLOOME_AGENT_BROWSER (injected at server spawn per hasFeature(owner,'agent_browser'))
# Both appear only when the owner has the agent_browser gray-release, so skill visibility == user
# gray-release (forward-compatible, zero behavior change).
requires:
  anyEnv:
    - BLOOME_BROWSER_SOCKET
    - BLOOME_AGENT_BROWSER
---

# Bloome Browser (`browser` command)

Pop up a **trusted browser window** on the user's desktop: the user can see what you're doing, log in
themselves, and stop it with one click. Under the hood it's the **user's own local Chromium (residential
IP + real logged-in state)**, which gets past anti-bot — a cloud sandbox browser can't.

> **This is a Bloome command, run via your `bloome` tool / `bloome_shell`, not a plain shell program.**
>
> - With the `bloome` tool → pass the command **as-is**: `browser start <url>`
> - With `bloome_shell` → prefix `bloome-cli`: `bloome-cli browser start <url>`
>
> Examples below are written in the **as-is** form (`bloome` tool usage); over shell, prefix each with `bloome-cli`.

## ⛔ Never run `agent-browser` directly

There **is** an `agent-browser` on PATH inside the cloud sandbox, but **running it directly = opening a
browser in the sandbox = a data-center IP**. Sites like Xiaohongshu/Taobao return "IP at risk" and block
it — **exactly what you must avoid**. This skill's `browser` command **dispatches the action to the user's
desktop** (residential IP + the user's logged-in state). So: **always use `browser ...`, never
`agent-browser ...`**. (Likewise don't `agent-browser install` to set up Chrome in the sandbox — dead end.)

## When the desktop app is unavailable

If a `browser ...` result contains `desktop_required` / `desktop` / `offline` / `reach the desktop` /
`broker not running`:

- **Do not retry**, and do not fall back to running `agent-browser` in the sandbox.
- Send the user a short message that this browser task **needs the Bloome desktop app**, and why it's
  worth it: the browser runs on the user's own computer — real network and logged-in sessions, data and
  files stay on their machine, and they can watch and take over at any time; a residential IP is far less
  likely to be blocked by a site's anti-bot checks. **Avoid hard claims like "zero cloud" / "end-to-end" /
  "data never touches us"** (the agent's commands still relay through Bloome — just don't bring it up).
- **Point the user to install/open the desktop app**: on a Mac/Windows computer's web page there is a
  **"Get desktop app" button at the bottom-right** (it picks the right installer for their OS); once the
  desktop app is open, this browser task can continue. **Do not send a widget card** — reuse the existing
  download entry point.
- **If they already have the desktop app, they just need to open it** (it may be closed, or running on
  another computer) — no need to reinstall. Phrase it as "install **or open**", not only "download", so
  existing users aren't told to re-download.
- **If the user is on a phone/tablet (or doesn't see that button):** the Bloome desktop app is
  **macOS / Windows only**, and that download button only shows on desktop-OS web. So tell them to
  **open the Bloome web app on a Mac or Windows computer** and use the bottom-right "Get desktop app"
  button there. (There is no universal download landing page, and a phone can't install it anyway.)

Minimal command (adapt the message to the user's own language):

```bash
bloome-cli send "This browser task needs the Bloome desktop app: the browser runs on your own computer, using your network and logged-in sessions, data stays local, and you can watch and take over anytime. If you already installed it, just open it and I'll continue. Otherwise, on a Mac/Windows computer there's a 'Get desktop app' button at the bottom-right of the Bloome web page — install it, open it, done. (On phone/tablet, open Bloome on a computer first — the desktop app is macOS/Windows only.)"
```

## When to use / not

- ✅ Sites needing login / with anti-bot (Xiaohongshu etc.); reading content under the user's account;
  clicking / filling on the page.
- ❌ Public pages, plain text scraping → `web_fetch` is faster.

## Standard flow (e.g. "find Shenzhen attractions on Xiaohongshu for me")

```
browser start https://www.xiaohongshu.com   # pops the trusted window (top: Controlled by you + Stop)
# if login is needed, have the user log in themselves in the window — don't enter their credentials for them
browser exec -- snapshot -i                  # read the page (interactive elements with @ref)
browser exec -- fill @e2 "深圳 景点"
browser exec -- click @e3
browser exec -- snapshot -i                  # refs go stale after navigation/click — you MUST re-snapshot
browser exec -- get text "body"              # read the result to answer the user
browser stop                                 # stop when done (or let the user click "Stop" on the window)
```

(Over shell: `bloome-cli browser start ...` / `bloome-cli browser exec -- snapshot -i` …)

## Multiple desktop devices

If you do not pass `--device`, Bloome chooses the user's configured default online desktop first,
then falls back through the user's priority order for online desktops. Do **not** add `--device`
just because multiple desktops exist.

Use `browser devices` and then pass `--device` only when:

- The user asks you to use a specific machine.
- A command says the requested device is offline.
- A command says a hostname is ambiguous.

```bash
browser devices
browser start --device <id-or-hostname> https://www.xiaohongshu.com
browser exec --device <id-or-hostname> -- snapshot -i
```

`browser devices` shows device id, hostname, online/default state, priority, and last-seen time.
Use the exact device id when hostnames are ambiguous. For `browser exec`, `--device` must appear
before the raw `--` separator; everything after `--` is passed to the browser engine.

## Profiles

A browser profile is the login jar used by browser commands. The owner can enable a **unified
profile**: when it is on, all parent agents inherit one owner-wide login jar by default. The owner
can still set a specific agent to **Own**, which means that agent always uses its private profile
instead of the unified jar.

If the user asks how to set this up, explain it this way:

- Turn on the unified profile in **Browser management** when agents should share the same website
  login state.
- Set an individual agent to **Own** when it should keep separate website sessions.
- Use the visible desktop browser to seed login. The user logs in themselves; you do not ask for
  passwords, verification codes, cookie exports, or browser state files.

```bash
browser profiles
```

- `browser profiles` shows whether unified profile is on, this agent's configured mode, this
  agent's effective mode, and the effective partition key.
- `--profile <agentId>` is deprecated. It is kept so old commands parse, but browser profile v2
  rejects cross-agent borrowed profiles. Prefer the owner-managed unified profile or Own override.
- If a result contains `profile_forbidden`, do not keep retrying `--profile`; ask the owner to use
  Browser management to enable unified profile or set this agent to Own.
- If a result contains `profile_not_found`, run `browser profiles` and use the current policy.
- If a result contains `browser_policy_unavailable`, retry shortly; if it persists, ask the owner
  to check Browser management and the desktop app.
- If a result contains `browser_policy_changed`, run `browser start <url>` again so the desktop
  opens the correct profile under the latest policy.

## Command vocabulary after `exec --`

Everything after `--` in `browser exec -- <args>` is **passed through as-is to the underlying browser
engine**; the vocabulary is `open` / `snapshot -i` / `click @ref` / `fill @ref` / `get text` / `wait` /
`screenshot` etc. (same vocabulary as the global `agent-browser` — you may consult that for the vocabulary,
but **always execute via `browser exec --`**, never call `agent-browser` directly).

## Subcommands (as-is form)

| Command                  | Purpose                                 |
| ------------------------ | --------------------------------------- |
| `browser start [url]`    | Start a session, pop the trusted window |
| `browser exec -- <args>` | Pass-through to drive the engine        |
| `browser stop`           | Stop the session                        |
| `browser status`         | Check availability / active session     |
| `browser devices`        | List online desktop browser devices with default/priority |
| `browser profiles`       | Show effective browser profile policy   |

## Notes

- **The first step is always `browser start`**: `status` is only for checking; to actually open a page you
  must `start <url>` first (or `start` then `exec -- open <url>`).
- **Leave login to the user**: account / password / verification codes are always for the user to enter in
  the visible window.
- **Re-`snapshot -i` after every navigation / tab switch** (refs go stale).
- **Cookie/session export is hard-blocked** (`state save` is rejected to prevent login-state leakage —
  expected).
- Commands **return results synchronously** (same whether local-direct or cloud via server relay polling):
  just read the command output and continue — you won't and needn't wait for a "next message". The first
  cloud `start` may take a few seconds (the desktop spins up the session).
- If a command reports "user stopped" / "desktop offline" / "gray-release not enabled": don't blindly retry
  or switch to the sandbox browser — follow the guidance to tell the user (needs the Bloome desktop app
  online + the `agent_browser` gray-release enabled), or ask whether to continue.
