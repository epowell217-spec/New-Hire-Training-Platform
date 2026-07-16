---
name: skill-evolve
description: 'Load when you notice repeated work, an owner correction, an owner gold quote, or your own recurring gap that is worth codifying into a skill. Do NOT use for: one-off owner requests, ordinary memory (that belongs in MEMORY.md / daily notes), or modifying skills the owner has not yet approved.'
version: 1
---

# Skill Evolve

## Core purpose

Turn repeated agent work, owner corrections, owner gold, and agent observed gaps into better skills.

This is a meta skill for any Bloome agent.

The owner is the approver.
The agent may detect, draft, and propose.
The agent may not write or edit skills until the owner explicitly approves the proposal.

The skill is pure prompt work.
Do not add scripts.
Do not require external tools beyond the Bloome file tools already available to the agent.

---

## When to use

Use this skill when any of these signals appears.

- The agent did the same kind of work 3 or more times in this conversation.
- The agent sees the same pattern across conversations through its memory (MEMORY.md, daily notes, `history --conv`).
- The owner says "remember this".
- The owner says "next time do X".
- The owner says "you always forget Y".
- The owner corrects the agent with a process rule.
- The owner rejects an output and explains the correct method.
- The owner approves a better pattern and wants it reused.
- The agent notices a repeated manual step.
- The agent notices it keeps asking for the same owner input.
- The agent notices it keeps reconstructing the same template from scratch.
- The agent notices an existing skill is close but missing one edge case.
- The agent finishes another skill and sees a reusable lesson from the work.

Use at reflection moments after the main work is done: owner feedback, repeated formats, failed handoffs, or memory recall that shows the same correction in multiple threads.

Do not use this skill for ordinary memory.
If the owner simply shares a preference, fact, or relationship note, record it through your normal memory mechanics (MEMORY.md, daily notes, user profiles).
Use this skill only when that memory should change how a skill runs.

Do not use this skill for one isolated request.
One request can be remembered, but it should not become a reusable skill rule unless it is durable, specific, and future useful.

Do not use this skill to bypass approval.
No approval means no skill change.

---

## Reference skills surveyed

1. https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md
   Strong: it treats skill folders as `SKILL.md` plus optional resources, and keeps the description focused on trigger selection.
   Borrow: progressive disclosure, pushy trigger descriptions, and examples as reusable resources.
   Drop: broad evaluation harness steps that do not fit Bloome's in sandbox, owner gated workflow.

2. https://github.com/anthropics/skills
   Strong: the public skill repository shows the portable folder convention and keeps skills self contained.
   Borrow: one folder per capability, `references/` for detail, and no surprise resources.
   Drop: any assumption that a shared bundle can write to an agent's local files without local governance.

3. https://arxiv.org/abs/2305.16291
   Strong: Voyager demonstrates an agent that builds a growing skill library and reuses learned procedures in new situations.
   Borrow: "encounter repeated or new work -> codify reusable capability -> retrieve later" as the core loop.
   Drop: automatic commitment of code to the library without an owner approval gate.

4. https://arxiv.org/abs/2310.08560
   Strong: MemGPT frames memory as tiered context management and uses interrupts when the agent needs user control.
   Borrow: separate fast working context from durable stores, and interrupt the owner when durable change requires consent.
   Drop: treating memory updates and skill edits as the same operation.

5. https://docs.letta.com/guides/agents/memory-blocks
   Strong: Letta memory blocks separate persona, human, shared, and read only context, and describe why labels matter.
   Borrow: explicit block purpose, agent editable versus read only boundaries, and shared memory discipline.
   Drop: unrestricted self editing of identity style blocks; Bloome skills require owner approval before file changes.

---

## Reference files

Load only the reference needed for the current moment.

- Read [detection-signals.md](./references/detection-signals.md) when deciding whether a moment deserves codification.
- Read [edit-vs-create-rubric.md](./references/edit-vs-create-rubric.md) when choosing between a targeted edit and a new skill.
- Read [owner-approval-protocol.md](./references/owner-approval-protocol.md) before asking the owner to approve any proposal.
- Read [proposal-format.md](./references/proposal-format.md) when drafting a proposed edit, new skill, or pending proposal.
- Read [audit-log-format.md](./references/audit-log-format.md) before appending to `skills/SKILL_EVOLUTION_LOG.md`.
- Read [anti-patterns.md](./references/anti-patterns.md) when the proposed change feels broad, vague, self referential, or too eager.
- Read [example-walkthrough.md](./references/example-walkthrough.md) for a complete worked example (it follows a fictional product-team agent called Mia).

Do not load every reference file by default.

---

## The four capabilities

### 1. Detection

Detect moments where a future run would be better if the agent had a clearer skill.
The signal must be stronger than "this happened once".
Look for repeated work, owner gold, owner correction, or the agent's own repeated gap.

The detection question is:

> Would a future agent predictably do better if this lived as a skill instruction, example, rubric, template, or anti pattern?

If yes, move to triage.
If no, use normal memory or do nothing.

### 2. Triage

Decide whether the learning belongs inside an existing skill or in a new skill bundle.
First scan the agent's own `skills/` directory.
Look at skill names, descriptions, `SKILL.md` headings, and reference file names.

Platform-seeded skills (`bloome`, `find-skills`, `skill-audit`, `skill-creator`, `skill-evolve`, and anything else the platform installed for you) are read-only — the system enforces this. Never propose edits to them. If the learning would improve a platform skill, tell the owner so they can pass it to the platform; codify your local version of the lesson in your own skill or memory instead.

Prefer a targeted edit when a related skill already owns the workflow.
Create a new skill only when no existing skill has a clear home for the behavior.
Skill count is a cost.
The best evolution often adds one sharp paragraph, one edge case, or one example to an existing bundle.

### 3. Owner approval gate

Never write the skill change first.
Always show the owner a proposal before writing.
The proposal can be a diff for an existing skill or a complete new bundle draft.

Owner approval must be explicit.
Accept "yes", "approved", "ship it", "write it", "go ahead", or an equivalent direct instruction.
Do not treat silence, a topic change, or general enthusiasm as approval.

### 4. Audit log

After an approved change is written, append one machine readable line to `skills/SKILL_EVOLUTION_LOG.md`.
The log records what changed, why, the owner quote that triggered it, and the approval evidence.

The log is append only.
Do not rewrite old entries.
If a past change becomes wrong, append a superseding entry.

---

## Detection signals

There are four primary patterns.
Use the full examples in `references/detection-signals.md` when the signal is ambiguous.

1. Repeated work: the agent performs the same workflow 3 or more times in one conversation or across conversations (check your memory).
2. Owner gold quote: the owner says "remember this", "next time do it this way", "this is the standard", or similar.
3. Owner correction: the owner corrects the agent's trigger, sequence, scope, output, tone, or safety boundary.
4. Agent self gap: the agent notices it keeps rebuilding a template, asking for the same input, or missing the same log step.

Codify only the reusable part.
Preserve the owner's wording when safe.
Self gaps still need owner approval.

---

## Edit-vs-create decision tree

Start by listing `skills/`, reading candidate descriptions, reading the closest `SKILL.md`, and searching only that skill's `references/`.

Edit an existing skill when the learning affects a named workflow, belongs to an existing trigger, adds one edge case, adds one decision rule, adds one template, adds one anti pattern, or corrects behavior inside that skill.

Create a new skill when no existing skill owns the trigger, the workflow has a distinct start and output, the agent would otherwise need several unrelated skills, and the behavior is repeated enough to justify a new trigger surface.

Similarity rule: 0.80 or higher means edit; 0.50 to 0.79 means show edit and new bundle options; below 0.50 means propose a new skill only if detection evidence is strong.

When in doubt, propose the smaller edit.

---

## Owner-approval protocol

Approval happens after proposal and before file write.

The owner should see:

- the trigger evidence,
- the target skill or new skill name,
- the proposed change,
- why it matters,
- what will be written,
- where pending proposals live if the owner does not answer.

Use one concise owner message.
Do not nag.
Do not ask for approval while the owner is waiting on the main task unless the skill change is the task.

### Owner message template 1: targeted edit

```text
I noticed a reusable correction worth codifying:
"[owner quote]"

Proposal: update `[skill-name]` with [one sentence change].
I will write only the diff below and append one audit log entry.

Approve this skill edit?
```

### Owner message template 2: new skill

```text
I have seen this workflow repeat [count] times, and no current skill owns it.

Proposal: create `[new-skill-name]` with a `SKILL.md` and `references/` for [scope].
I will keep it pending until you approve.

Approve creating this skill bundle?
```

### Owner message template 3: ignored proposal

```text
I will not write the skill change without approval.
I saved the proposal under `skills/.pending-skill-proposals/`.
We can approve, revise, or discard it later.
```

If the owner approves, write the change and log it.
If the owner rejects, do not write the change.
If the owner modifies the proposal, revise and ask once more if the modification changes the file content.
If the owner ignores it, save only a pending proposal.

---

## Proposal format

Use markdown proposals.
The proposal should be readable by the owner and easy for another agent to apply later.
See `references/proposal-format.md` for full shapes.

Proposed edit shape:

- title: `Skill evolution proposal`,
- status: `pending`,
- kind: `edit-existing`,
- target skill and files,
- trigger evidence with owner quote,
- one paragraph on why it matters,
- proposed diff,
- explicit approval question.

Proposed new skill shape:

- title: `Skill evolution proposal`,
- status: `pending`,
- kind: `create-new`,
- new skill name,
- trigger evidence,
- scope and non scope,
- proposed file tree,
- brief bundle preview,
- explicit approval question.

---

## Workflow

### Step 1: Detect

Notice the signal.
Classify it as repeated work, owner gold quote, owner correction, or self gap.
If no signal is strong enough, stop.

### Step 2: Preserve evidence

Capture the exact owner quote when one exists.
Capture the conversation pattern when repetition exists.
Capture the agent's self observation when the gap is self detected.

Keep the evidence short.
Do not copy private unrelated context into a skill file.

### Step 3: Scan skills

List the agent's `skills/` directory.
Exclude platform-seeded skills from edit candidates — they are read-only; only skills you authored or installed are valid edit targets.
Read descriptions first.
Read the closest `SKILL.md` only after a candidate appears.
Search references only for the candidate skill.

### Step 4: Choose edit or new bundle

Use the decision tree above.
Prefer a targeted edit when the owner learning belongs to an existing skill.
Create a new bundle only when the trigger and workflow are distinct.

### Step 5: Draft proposal

Draft one proposal.
Show what will change.
Do not write the change yet.

For an existing skill, show the proposed diff.
For a new skill, show the proposed file tree and enough content to judge scope.

### Step 6: Ask owner

Ask with one of the owner message templates.
Wait for explicit approval.

If the owner is busy, save the proposal to pending and continue the main conversation.

### Step 7: Write or shelve

If approved, write the exact approved change.
If rejected, discard or mark the proposal rejected.
If modified, adjust and confirm the final version.
If ignored, save under `skills/.pending-skill-proposals/`.

### Step 8: Log

Append one JSON line to `skills/SKILL_EVOLUTION_LOG.md`.
Use the schema in `references/audit-log-format.md`.
Include timestamp, agent, skill, change kind, why, trigger evidence, approval evidence, files changed, and pending proposal path if any.

### Step 9: Reflect

After logging, check whether the change affects other skills.
If it does, propose only one canonical home.
Do not duplicate the same rule across many skills.

---

## Outputs

### Proposal markdown

Use for every pending or approval ready change.

Fields:

- status,
- kind,
- target skill or new skill,
- trigger evidence,
- owner quote,
- proposed content,
- approval question,
- pending path.

### File write

Only after owner approval.

Valid writes:

- `skills/<skill-name>/SKILL.md`
- `skills/<skill-name>/references/<topic>.md`
- `skills/.pending-skill-proposals/<timestamp>-<slug>.md`
- `skills/SKILL_EVOLUTION_LOG.md`

Do not write outside `skills/` for this skill.

### Audit log entry

Use JSON Lines inside `skills/SKILL_EVOLUTION_LOG.md`.
Each line is one object.
No prose rows.
No hidden edits.

---

## Edge cases

### Owner says yes to everything

Approval is necessary but not sufficient.
Still prevent skill bloat.
If the proposal is weak, say it should remain a pending note or normal memory.

### Owner ignores forever

Do not keep asking.
Keep the pending proposal.
The next time the same signal repeats, mention that a pending proposal already exists.

### Owner contradicts past approval

Do not rewrite history.
Append a superseding log entry.
Update the skill only after new approval.

### Evolve proposes to modify itself or another platform skill

Platform-seeded skills, including this one, are read-only — the system blocks writes to them.
Do not look for workarounds; route the improvement idea to the owner as feedback instead.
Never create `skill-evolve-2` to escape the restriction.
Never weaken the approval gate by cloning this skill's workflow into an editable copy.

### Existing skill is already too large

Do not add a long section to a bloated `SKILL.md`.
Propose a short pointer in `SKILL.md` and put detail in one reference file.

### Owner quote contains sensitive material

Use a minimal excerpt.
Do not place secrets, private identifiers, or unrelated personal facts into the skill.
The log can say "owner correction, redacted" when necessary.

---

## Anti-patterns

Read `references/anti-patterns.md` when the proposed change feels too broad, too eager, or self referential.

Block these inline:

1. Auto writing without owner approval.
2. Turning one request into a permanent skill rule.
3. Creating a new skill when a small edit would work.
4. Encoding every owner preference into a skill instead of normal memory.
5. Creating recursive evolve skills.

Correction template:

```text
I think this is a skill evolution candidate, but not ready to write.
The safer next step is a pending proposal because [reason].
```

---

## Integration

Run this skill after any other skill completes when the agent notices a reusable lesson.
Do not interrupt the main owner request.
Complete the work first, then reflect.

Read your memory only for cross conversation pattern detection.
Do not use this skill as a general memory reader.

Write approved changes to the agent's local `skills/` directory.
Write the log to `skills/SKILL_EVOLUTION_LOG.md`.
Write ignored proposals to `skills/.pending-skill-proposals/`.

Whatever your domain, the pattern is the same: run after a domain skill completes when owner corrections changed its workflow, when repeated delegation or handoff friction appeared, or when a new scoring or scope pattern became stable.

Final rule:

> The agent can learn loudly, but it writes skills only with owner approval.
