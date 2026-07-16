# Owner Approval Protocol

Use this file before asking the owner to approve any skill change.

The gate is not ceremony.
It prevents drift, prompt injection, and silent skill bloat.

## Non negotiable rule

No explicit owner approval means no skill file write.

The agent may:

- detect a candidate,
- draft a proposal,
- show a diff,
- save a pending proposal,
- append a log entry after approved write.

The agent may not:

- edit `SKILL.md` first,
- edit references first,
- treat silence as approval,
- treat "nice" or "sounds good" as approval unless it clearly answers the proposal,
- change identity files through this skill,
- remove the approval gate from this skill.

## What counts as approval

Approval examples:

- "yes"
- "approved"
- "ship it"
- "write it"
- "go ahead"
- "apply this"
- "approve the edit"
- "create the bundle"
- a direct instruction that clearly authorizes the proposed file write.

Not approval:

- owner changes topic,
- owner says the idea is interesting,
- owner says "maybe",
- owner praises the proposal,
- owner answers another question,
- owner is silent,
- another agent agrees.

## When to ask

Ask after the main work is done unless the owner specifically asked for skill evolution.

Good moments:

- after a product workflow completes,
- after the owner corrects process,
- after a repeated pattern is visible,
- after a pending proposal becomes relevant again.

Bad moments:

- while the owner is waiting for a concrete deliverable,
- in the middle of an urgent routing decision,
- when the evidence is weak,
- when the proposal would distract from the active product decision.

## Message template: targeted edit

```text
I noticed a reusable correction worth codifying:
"[owner quote]"

Proposal: update `[skill-name]` with [one sentence change].
I will write only the diff below and append one audit log entry.

Approve this skill edit?
```

## Message template: new skill

```text
I have seen this workflow repeat [count] times, and no current skill owns it.

Proposal: create `[new-skill-name]` with a `SKILL.md` and `references/` for [scope].
I will keep it pending until you approve.

Approve creating this skill bundle?
```

## Message template: no answer

```text
I will not write the skill change without approval.
I saved the proposal under `skills/.pending-skill-proposals/`.
We can approve, revise, or discard it later.
```

## Dialog outcomes

Approved:

- apply the approved change,
- do not add extra unapproved edits,
- append one audit log line.

Rejected:

- do not apply,
- mark pending proposal as rejected if it exists,
- optionally log rejection only if the owner wants a durable record.

Modified:

- revise the proposal,
- show the revised version,
- ask for approval again if the file content changed.

Ignored:

- save the proposal under pending,
- stop asking,
- mention the pending proposal only when the same pattern appears again.

## How to avoid nagging

Keep the approval ask short.
Ask once.
Use a pending file for later.

Do not say:

```text
Should I remember this? Should I update the skill? Are you sure?
```

Say:

```text
This is a skill evolution candidate. I will save it pending unless you explicitly approve the write.
```

## Approval evidence

The audit log needs exact approval evidence.

Capture:

- approval phrase,
- timestamp,
- proposal id or pending path,
- owner quote that triggered the change,
- files changed.

If approval happened through a UI action, record the action label and timestamp.
If approval happened in chat, quote the owner phrase.

## Sensitive owner quotes

If the owner quote includes private or secret material, redact the sensitive part.

Example:

```json
{ "owner_quote": "Owner correction redacted; concerns approval gate for private customer data." }
```

Keep enough evidence for future agents to understand why the change happened.
Do not copy unrelated private context.
