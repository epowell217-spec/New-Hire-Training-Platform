# Group Workspace

Use group workspace commands when the user asks you to save, share, update, delete, retrieve, or download durable artifacts/files for the current group conversation. Workspace items are conversation-scoped collaborative records, separate from your private agent workspace files.

Run commands through the `bloome` tool by passing the command body as-is. If you only have shell access, run the same command with `bloome-cli` prefixed.

## Constraints

- Workspace commands require the current conversation context. If the tool says `Workspace commands require RESON_CONVERSATION_ID`, you are not in a usable conversation context.
- Prefer the current conversation. Use `--conversation <groupConversationId>` only when the user explicitly points at another group and you have the id.
- In a DM, you can still read a group workspace when the user asks about a group both you and the DM human can access. First discover the group id with `conversations` or history context, then use `workspace items list --conversation <groupConversationId>` to find the item. After you have an item id, item-specific reads infer the target group from that item id: use `workspace items get <itemId>`, `workspace items read <itemId> --text-only`, or `workspace items download <itemId> --output <path>` without adding `--conversation`.
- Every create, update, upload, and delete requires `--event-summary`. Write it like a short commit message.
- Updates, replacement uploads, and deletes require `--version <currentVersion>`.
  This is the current item version you last read with `workspace items get <itemId>`.
  It is an optimistic concurrency guard, not the target version to write.
  Reload with `workspace items get <itemId>` if unsure.
- Active lists exclude archived and superseded items. Use `--include-inactive` only when you need tombstones/history.
- File upload uses direct signed storage behind the command. Do not ask the human to run the signed URL or upload manually.
- Keep user-facing replies focused on the result. Do not paste CLI commands as instructions to the user.

## Best-Fit Use Cases

Use workspace when the request matches one of these durable shared-asset patterns:

- **Group project deliverable repository:** final or replaceable outputs such as reports, proposals, PRDs, PDFs, design drafts, code bundles, or generated assets that the group should be able to find and download later.
- **Shared reference library:** long-lived source material for the group or its agents, such as competitor notes, customer background, meeting materials, research sources, or reference documents.
- **Plans and decision records:** durable collaboration records such as weekly plans, final decisions, risk lists, summaries, and agreed next steps that should survive beyond the chat scrollback.
- **Datasets and source files:** CSV, JSON, PDFs, images, archives, source code, or other files that do not fit inline chat or a markdown document surface.
- **Agent handoff artifacts:** intermediate research, generated files, or structured notes that another agent, a future turn, or a later group member should retrieve by item id and continue from.

## Commands

```bash
# Workspace overview and recent events
workspace status
workspace status --event-limit 50
workspace status --conversation <groupConversationId>

# List and inspect items
workspace items list
workspace items list --include-inactive
workspace items list --conversation <groupConversationId>
workspace items get <itemId>

# Read inline text items
workspace items read <itemId>
workspace items read <itemId> --text-only

# DM -> group workspace read path:
# conversations -> identify groupConversationId
# workspace items list --conversation <groupConversationId>
# workspace items read <itemId> --text-only

# Create an inline text item from a local file
workspace items create \
  --title "Plan" \
  --type text \
  --kind artifact \
  --event-summary "Created the initial plan" \
  --text-file plan.md

# Upload a binary or large file
workspace items upload report.pdf \
  --title "Report" \
  --type file \
  --kind artifact \
  --event-summary "Uploaded the report"

# Replace/update an existing file item
workspace items get <itemId>  # Read current version first
workspace items upload report.pdf \
  --item-id <itemId> \
  --version <currentVersion> \
  --title "Report" \
  --event-summary "Replaced the report"

# Download an R2-backed file item into your local agent workspace
workspace items download <itemId> --output report.pdf

# Update inline text item metadata/content
workspace items get <itemId>  # Read current version first
workspace items update <itemId> \
  --version <currentVersion> \
  --event-summary "Updated the plan" \
  --text-file plan.md

# Delete an obsolete item and release its active storage quota
workspace items get <itemId>  # Read current version first
workspace items delete <itemId> \
  --version <currentVersion> \
  --event-summary "Deleted the obsolete export"
```

Delete uses the same optimistic concurrency guard as update/replacement upload.
If another upload is actively completing, delete can return
`workspace_upload_in_progress`; reload the item and retry only after the upload
settles.

## Choosing Workspace vs Other Surfaces

Use workspace for durable shared artifacts and files that agents or group members may need to find later: reports, source files, datasets, exported PDFs, plans, summaries, reference material, and handoff artifacts.

Use text reply for one-off answers. Use documents when the user specifically wants a collaborative editable document surface. Use widgets/surfaces when the result should be visually embedded or interactive in the conversation.
