# Example Walkthrough

This example shows the full flow.

Examples in this file follow a fictional product team — Mia (PM agent), Aya (design agent), Kai (engineering agent) — with their domain skills. Substitute your own domain and skill names.

## Situation

Mia has handled three startup product threads this week.

In each one:

- the owner asked for design too early,
- Mia first needed to identify the paying actor,
- Aya was mentioned before the validation question was clear,
- the final useful move was a one question pause plus a fake door test card.

Then the owner corrects Mia:

> Next time, do not send Aya a visual brief before we know who pays. Ask me the buyer question first.

## Step 1: Detect

Mia classifies the signal:

- pattern: owner correction,
- repeated work: 3 similar product threads,
- owner quote: exact quote above,
- owner impact: prevents premature design delegation.

This is strong enough to propose skill evolution.

## Step 2: Preserve evidence

Mia captures:

```text
Owner quote: "Next time, do not send Aya a visual brief before we know who pays. Ask me the buyer question first."
Observed count: 3 product threads with premature design routing.
```

Mia does not copy full conversation logs.
Mia does not include unrelated product details.

## Step 3: Scan skills

Mia lists the local skills:

```text
idea-discovery
prioritize-and-shape
team-routing
```

Candidate scan:

- `idea-discovery` owns early product clarity.
- `team-routing` owns whether to mention Aya or Kai.
- `prioritize-and-shape` is not the right home because the issue is not prioritization.

The best home is `team-routing`.
The correction affects when Mia should mention Aya.

## Step 4: Choose edit or new bundle

Mia applies the rubric.

Related enough:

- same trigger: owner wants design or routing,
- same workflow stage: group routing,
- same teammate boundary: Aya,
- correction applies inside `team-routing`.

Decision:

```text
Edit existing skill: team-routing.
```

No new skill is needed.

## Step 5: Draft proposal

Mia drafts:

````markdown
# Skill evolution proposal

Status: pending
Kind: edit-existing
Proposal id: 2026-06-07T10-18-00Z-team-routing-buyer-before-aya
Target skill: team-routing
Target files:

- skills/team-routing/SKILL.md

## Trigger evidence

Pattern: owner_correction
Owner quote: "Next time, do not send Aya a visual brief before we know who pays. Ask me the buyer question first."
Observed count: 3

## Why this matters

This prevents Mia from routing ambiguous product ideas to design before the business actor is known.

## Proposed diff

```diff
--- skills/team-routing/SKILL.md
+++ skills/team-routing/SKILL.md
@@
+If the owner asks for design but the paying actor is unknown, ask the owner one buyer question before mentioning Aya. Do not send a visual brief until user, buyer, or beneficiary boundaries are clear enough for design work.
```

## Owner decision needed

Approve this exact edit, revise it, or reject it.
No file will be changed until approval.
````

## Step 6: Ask owner

Mia sends:

```text
I noticed a reusable correction worth codifying:
"Next time, do not send Aya a visual brief before we know who pays. Ask me the buyer question first."

Proposal: update `team-routing` so Mia asks the buyer question before mentioning Aya when the paying actor is unknown.
I will write only the diff below and append one audit log entry.

Approve this skill edit?
```

## Step 7: Owner approves

Owner replies:

```text
yes, approve it
```

Mia may now write the approved edit.

Mia must not add any extra rule that was not approved.

## Step 8: Write

Mia updates:

```text
skills/team-routing/SKILL.md
```

Only the approved paragraph is added.

## Step 9: Log

Mia appends one JSON line to:

```text
skills/SKILL_EVOLUTION_LOG.md
```

Entry:

```json
{
  "schema": "bloome-skill-evolution-log/v1",
  "id": "2026-06-07T10-20-30Z-team-routing-buyer-before-aya",
  "timestamp": "2026-06-07T10:20:30Z",
  "agent": "Mia",
  "change_kind": "edit-existing",
  "skill": "team-routing",
  "files_changed": ["skills/team-routing/SKILL.md"],
  "why": "Owner corrected premature design routing before paying actor clarity.",
  "trigger_pattern": "owner_correction",
  "owner_quote": "Next time, do not send Aya a visual brief before we know who pays. Ask me the buyer question first.",
  "approval_evidence": "Owner said: yes, approve it",
  "proposal_path": "skills/.pending-skill-proposals/2026-06-07T10-18-00Z-team-routing-buyer-before-aya.md",
  "status": "applied"
}
```

## If owner ignores

If the owner does not answer, Mia writes no skill changes.

Mia saves the proposal:

```text
skills/.pending-skill-proposals/2026-06-07T10-18-00Z-team-routing-buyer-before-aya.md
```

Mia sends:

```text
I will not write the skill change without approval.
I saved the proposal under `skills/.pending-skill-proposals/`.
We can approve, revise, or discard it later.
```

## If owner rejects

Owner says:

```text
No, this belongs in idea-discovery instead.
```

Mia does not edit `team-routing`.
Mia revises the proposal to target `idea-discovery`.
Because the target changed, Mia asks for approval again.

## If Mia wants to modify skill-evolve

Suppose Mia notices this walkthrough misses a rejection case.

Mia may propose a small edit to `skill-evolve`.
Mia must not approve it herself.
Mia must not create another evolve skill.
Mia must not weaken the approval gate.

Correct owner ask:

```text
I noticed `skill-evolve` itself is missing a rejection example.
Proposal: add one short rejection branch to the walkthrough.
Approve this self edit?
```
