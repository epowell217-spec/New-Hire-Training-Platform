# Document Operations

Collaborative markdown documents with version-controlled editing.

## Commands

```bash
doc create --title "Meeting Notes" --content-file docs/notes.md   # Preferred: from local file
doc create --title "Notes" --content "# Notes\n\n- ..."           # Inline (only for trivial content)
doc read <id>                                                      # Returns content + version
doc write <id> --content-file docs/notes.md --version N            # Preferred: replace from local file
doc write <id> --content "new content" --version N                 # Inline (only for trivial content)
doc append <id> --content "\n## Section" --version N               # Append a small chunk
doc share <id>                                                     # Send card to conversation
```

## Editing Workflow (file-first — recommended)

For non-trivial markdown (anything with code blocks, lots of formatting, or content that may need successive edits), keep the document in a local file under `docs/<name>.md` and push it via `--content-file`. Same reasoning as the widget skill: building markdown inline as a CLI argument means the "current draft" only exists in chat history and gets lost between turns.

### Create

1. `Write` markdown to `docs/<name>.md`
2. `doc create --title "..." --content-file docs/<name>.md`
3. Note the returned `id` and `version` — local file remains your working copy

### Update (full replace)

1. **Local file present** → `Edit docs/<name>.md`
2. **Local file lost** → `doc read <id>` and write the `content` field back to `docs/<name>.md`, then `Edit`
3. Push: `doc write <id> --content-file docs/<name>.md --version <current>`

### Append (small additions)

`doc append --content "..."` is for small deltas (a paragraph, a log line). If the addition is large enough that escaping is awkward, do a full replace via `doc write` instead — keep the local file authoritative.

## Version Control

The `--version` parameter enables optimistic concurrency:

1. Read: `doc read <id>` → get content + current version
2. Write: `doc write <id> --content-file ... --version N` → pass the version you read
3. If version doesn't match → write fails (someone else edited) — re-read, re-merge, retry

This prevents lost updates in multi-user scenarios.

## Workflow Example

```bash
# Create from local file
Write docs/sprint-plan.md
doc create --title "Sprint Plan" --content-file docs/sprint-plan.md

# Read (returns content + version: 1)
doc read abc-123

# Append a small note
doc append abc-123 --content "\n## Updates\n- Widget v2 shipped" --version 1

# Big rewrite — edit local file, push
Edit docs/sprint-plan.md
doc write abc-123 --content-file docs/sprint-plan.md --version 2

# Share to conversation
doc share abc-123
```
