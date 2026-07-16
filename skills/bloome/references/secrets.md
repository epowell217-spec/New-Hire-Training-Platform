# Secrets — Sandbox-injected env vars for user scripts

> **Audience:** YOU (the agent) writing scripts on behalf of the user when they need external credentials (OpenAI key, AWS creds, DB password, etc.). The user manages secret storage in the web UI's agent settings; you only **discover and use** them via the CLI.

## When to use

User asks you to write/run a script that needs an external API key or credential. Before writing the script:

1. Run `secret list` to see what's available.
2. Reference secrets by their `name` (which is the env var name they'll be injected as).
3. Run the script via `secret call <NAMES...> -- <command>` so values are injected only for the child process.

## Hard rules

- ✅ **Assume env is injected**: write `os.environ['OPENAI_API_KEY']`, `process.env.OPENAI_API_KEY`, etc.
- ❌ **Never hardcode keys** in scripts.
- ❌ **Never ask the user to paste a key** into the chat — direct them to add it in agent settings → Secrets tab.
- ❌ **Never invent a secret name**. Only use names returned by `secret list`. If the script needs `OPENAI_API_KEY` and `secret list` doesn't show it, tell the user to create it in the UI before re-running.

## Commands

```bash
secret list
# NAME            DESCRIPTION
# OPENAI_API_KEY  Production OpenAI key
# DATABASE_URL    Analytics replica
# ...

secret call <NAME1> [<NAME2> ...] -- <command...>
# 把 secret values 注入子进程 env，运行 <command>，子进程退出码作为 secret call 的退出码透传。
```

Names are uppercase env-var-style: `^[A-Z_][A-Z0-9_]*$`. They double as both the storage handle and the env var name.

## Exec model — CRITICAL

`secret call ... -- <cmd>` uses **`execvp` directly, NOT a shell**. This has three consequences agents commonly get wrong:

### 1. Quoting / shell expansion lives in the OUTER shell

bloome-cli sees the argv after the outer shell has already done its parsing. By the time secrets are injected, the outer shell is gone.

```bash
# ❌ Outer shell expands $X BEFORE secrets are injected → empty Bearer
secret call OPENAI_API_KEY -- curl -H "Authorization: Bearer $OPENAI_API_KEY" https://...

# ❌ Single quotes pass literal "$OPENAI_API_KEY" string to curl → no substitution
secret call OPENAI_API_KEY -- curl -H 'Authorization: Bearer $OPENAI_API_KEY' https://...

# ✅ Wrap in `bash -c '...'` — single quotes keep $X literal through outer shell;
#    the inner bash receives the injected env and expands $X correctly
secret call OPENAI_API_KEY -- bash -c 'curl -H "Authorization: Bearer $OPENAI_API_KEY" https://...'
```

### 2. Tools that read env natively need NO `$X` in the command line

Most CLIs read env vars themselves (`getenv`). For these, just call them — no `$X` interpolation needed:

```bash
secret call AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_DEFAULT_REGION -- aws s3 ls
secret call DATABASE_URL -- psql -c "SELECT count(*) FROM users"
secret call OPENAI_API_KEY -- python pipeline.py     # script reads os.environ['OPENAI_API_KEY']
secret call GITHUB_TOKEN -- gh repo list
```

### 3. The first `--` is consumed by bloome-cli; subsequent `--` flags pass through

```bash
# aws's own --recursive / --exclude flags work fine
secret call AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_DEFAULT_REGION \
  -- aws s3 cp --recursive --exclude "*.log" ./local s3://bucket/

# git sees its own `--` as path separator
secret call GITHUB_TOKEN -- git log -- path/to/file
```

### 4. Don't quote the whole command into one argv element

```bash
# ❌ "python pipeline.py" becomes a single argv[0] with a literal space → ENOENT
secret call OPENAI_API_KEY -- 'python pipeline.py'

# ✅ Standard argv (whitespace-separated)
secret call OPENAI_API_KEY -- python pipeline.py

# ✅ Or wrap in bash -c if you really want shell semantics
secret call OPENAI_API_KEY -- bash -c 'python pipeline.py && echo done'
```

## Decision recipe

When the user asks for a script that needs credentials:

1. `secret list` first
2. **If the name exists** → write the script that reads `os.environ['NAME']` (or equivalent) and run it via `secret call NAME -- <runner>`
3. **If the name doesn't exist** → tell the user: "Add `<NAME>` (description: …) in your agent settings → Secrets tab, then I'll run the script." Don't proceed.
4. Never offer to take the value through chat or write it into a file.

## Common secret names

These are conventional choices users typically use; check with `secret list` rather than assuming:

- `OPENAI_API_KEY` — OpenAI
- `ANTHROPIC_API_KEY` — Anthropic / Claude
- `GOOGLE_API_KEY` — Google AI / Gemini
- `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` + `AWS_DEFAULT_REGION` — AWS (3 separate secrets, used together)
- `DATABASE_URL` — Postgres / MySQL connection string
- `GITHUB_TOKEN` — GitHub CLI / API
- `STRIPE_SECRET_KEY` — Stripe API
- `SLACK_BOT_TOKEN` — Slack bot

## What `secret call` does NOT do

- Does **not** persist the value into sandbox env beyond the child's lifetime
- Does **not** show the value to you (the agent) — you never see plaintext
- Does **not** support shell features like `$()`, pipes, redirects in the `--` tail unless you wrap with `bash -c '...'`

## Calling via the PI SDK tool vs the CLI subprocess

`secret call` works on both paths:

- **PI SDK tool dispatch** (e.g. `bloome("secret call OPENAI_API_KEY -- python script.py")` from inside cloud_sandbox / client_attached / client_standalone): captures the child's stdout/stderr (each capped ~32 KB) and returns them as structured fields (`stdout`, `stderr`, `exit_code`, `duration_ms`) so you can read the output directly. Prefer this when you're already issuing `bloome(...)` tool calls — it's one round-trip.
- **CLI subprocess** (`bloome-cli secret call ... -- ...` from a shell, ACP `bloome_shell`, etc.): `stdio: 'inherit'`, child output streams straight to the host TTY and the CLI exits with the child's exit code. Use this when you want interactive output or the child needs a real TTY.
