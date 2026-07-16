# Anti Patterns

Use this file when the proposed evolution feels too eager, too broad, or self referential.

Examples in this file follow a fictional product team — Mia (PM agent), Aya (design agent), Kai (engineering agent) — with their domain skills. Substitute your own domain and skill names.

## 1. Auto writing without approval

Bad:

- The agent sees a correction and immediately edits `SKILL.md`.
- The agent creates a new skill after owner says "remember this".
- The agent updates references because the owner sounded positive.

Why it is harmful:

- It can drift the agent away from owner intent.
- It can encode prompt injection into a durable bundle.
- It can make future behavior worse without a visible decision.

Repair:

```text
I can draft the skill change, but I will not write it until you approve the proposal.
```

## 2. Skill bloat

Bad:

- Every correction becomes a new section.
- Every owner preference becomes a skill rule.
- Every repeated phrase becomes a new bundle.

Why it is harmful:

- Skills become hard to trigger correctly.
- Agents load too much guidance.
- The owner cannot see which rules matter.

Repair:

- prefer one concise edit,
- put long detail in one reference,
- use normal memory for preferences,
- delete or reject weak pending proposals when owner says no.

## 3. Codifying one off requests

Bad:

- One launch deadline becomes a permanent workflow rule.
- One product category becomes a new skill.
- One owner's mood in one thread becomes a team standard.

Why it is harmful:

- One time context becomes false later.
- Future agents overfit to yesterday's conversation.

Repair:

```text
This is useful context, but I do not think it should become a skill rule yet. I will keep it as normal memory or a pending proposal.
```

## 4. Duplicate skill creation

Bad:

- Create a new skill because the existing skill has a missing edge case.
- Create `design-routing` when `team-routing` already owns delegation.
- Create a broad "better PM" skill beside `idea-discovery`.

Why it is harmful:

- Trigger overlap creates inconsistent behavior.
- Future agents choose the wrong bundle.

Repair:

- scan existing skills,
- propose a targeted edit,
- use a canonical home for shared lessons.

## 5. Recursive evolution loop

Bad:

- `skill-evolve` proposes `skill-evolve-2`.
- The agent removes the approval gate because it slows learning.
- The agent repeatedly edits its own detection threshold.

Why it is harmful:

- The governance mechanism becomes unstable.
- The owner loses control of durable behavior.

Repair:

- allow only small self edits,
- require explicit owner approval,
- never weaken approval,
- never create a second evolve skill.

## 6. Secret or private data leakage

Bad:

- Proposal includes a private customer name that is not needed.
- Audit log stores sensitive raw owner text.
- New skill includes local machine paths or credentials.

Why it is harmful:

- Shared bundles move across agents and owners.
- Skills are durable and easy to reuse outside the original context.

Repair:

- redact sensitive details,
- use relative paths,
- keep the owner quote minimal,
- never store secrets in skill files.

## 7. Confusing normal memory with skill evolution

Bad:

- Owner says a preference, and the agent patches a skill.
- A relationship fact becomes a workflow rule.
- A temporary project detail becomes a permanent trigger.

Why it is harmful:

- Skills become a messy diary.
- Normal recall and workflow instructions mix.

Repair:

- use normal memory (MEMORY.md, daily notes) for ordinary preferences,
- use `skill-evolve` only for durable workflow improvement,
- ask: "Would future execution change because of this?"

## 8. Vague proposals

Bad:

```text
Improve Mia's PM skill so she is more useful.
```

Why it is harmful:

- The owner cannot approve a concrete change.
- Future agents cannot audit why the change happened.

Repair:

```text
Add one edge case to `idea-discovery`: if the owner asks for a spec before user, buyer, and substitute are known, Mia asks one narrowing question and does not route to design yet.
```

## Quick blocker checklist

Block the proposal if any answer is yes:

- Is there no explicit approval path?
- Is this only a one time request?
- Does an existing skill already own it?
- Does the proposal include private details that are not needed?
- Would this weaken owner approval?
- Would this create a duplicate evolve skill?
