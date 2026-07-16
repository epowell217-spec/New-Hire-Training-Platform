# Detection Signals

Use this file when deciding whether a moment deserves skill evolution.

Examples in this file follow a fictional product team — Mia (PM agent), Aya (design agent), Kai (engineering agent) — with their domain skills. Substitute your own domain and skill names.

A signal is strong when it is durable, specific, and future useful.
If it is only interesting, store it in normal memory or do nothing.

## Pattern 1: repeated work

Repeated work means the agent has performed the same workflow 3 or more times.
The repetitions may appear in one conversation or across conversations (check your memory).

Count work as the same when:

- the same trigger appears,
- the same decision path appears,
- the same output shape appears,
- the same owner question is needed,
- the same correction would prevent future waste.

Do not count surface similarity alone.
Three product ideas are not repeated work if each needs a different method.
Three fake door validation plans with the same fields may be repeated work.

Examples:

- Mia writes a validation plan card for three different feature ideas.
- Mia asks the owner "who pays, user or buyer?" in three similar startup product threads.
- Aya creates the same empty state review checklist every time a dashboard appears.
- Kai reconstructs the same feasibility note for data import, export, auth, and latency.

Good codification:

- Add one reusable test card template to an existing discovery skill.
- Add one routing rule that tells Mia when to ask the owner before mentioning Aya.
- Add one feasibility checklist reference to Kai's existing skill.

Bad codification:

- Create a new skill for every feature category.
- Store the whole conversation as a skill.
- Add a permanent rule from only one occurrence.

## Pattern 2: owner gold quote

Owner gold is a direct owner statement that should shape future agent behavior.

Common phrasings:

- "Remember this."
- "Next time do X."
- "Use this format every time."
- "This is the standard."
- "You always forget Y."
- "Do not do that again."

Owner gold is stronger than agent inference.
Preserve the exact quote in the proposal when safe.

Examples:

- Owner says: "Next time, do not send Aya visual style. Ask her for interaction states."
- Owner says: "Remember, this team moves through widget demo before design polish."
- Owner says: "Use a short owner facing memo, not a big PM doc."

Good codification:

- Add the quote as an example in the relevant skill.
- Add an anti pattern with a correction phrase.
- Add a proposal template that reflects the owner standard.

Bad codification:

- Treat a preference about one product as universal.
- Hide the owner quote in the skill without asking.
- Rewrite persona or identity files as a side effect.

## Pattern 3: owner correction

Owner correction is a high value signal because it marks a real mismatch.

Classify the correction:

- trigger correction: the wrong skill or no skill was used,
- sequence correction: steps happened in the wrong order,
- scope correction: the agent did too much or too little,
- output correction: the artifact shape was wrong,
- tone correction: the agent sounded unlike the intended role,
- safety correction: the agent wrote or proposed something it should not.

Examples:

- "No, do not ask ten questions. Ask one high leverage question."
- "You should have routed that to Kai, not answered the technical part yourself."
- "Do not edit the skill until I approve the diff."
- "This is normal memory, not a new skill."

Good codification:

- Patch the closest existing skill with one corrected decision rule.
- Add an example of the wrong path and the repaired path.
- Add an approval gate reminder if the correction involved file writes.

Bad codification:

- Add a broad rule that blocks useful future flexibility.
- Erase the earlier rule instead of adding a more precise exception.
- Turn owner frustration into a vague "be better" instruction.

## Pattern 4: agent self gap

Self gap means the agent notices friction while working.
The agent can detect the gap, but the owner still approves the change.

Self gap signals:

- "I keep recreating this template."
- "I keep asking for the same approval phrase."
- "I keep forgetting to log the evidence."
- "This existing skill is close, but it lacks this edge case."
- "I keep reading the same reference before making the same decision."

Examples:

- Mia notices every product discovery conversation needs a fake door copy block.
- Aya notices every dashboard handoff needs loading, empty, error, and permission states.
- Kai notices every widget feasibility answer needs backend source, auth, persistence, and rollback checks.

Good codification:

- Draft a small proposal.
- Show evidence from the repeated work.
- Ask the owner to approve before writing.

Bad codification:

- Install the agent's self judgment as a rule with no owner check.
- Create a new skill because the agent is bored with manual work.
- Add private reasoning notes to a shared bundle.

## Threshold guide

Strong signal:

- repeated 3 or more times,
- direct owner correction,
- direct owner standard,
- recurring self gap with visible owner impact.

Medium signal:

- repeated twice,
- owner seems to prefer a format,
- existing skill almost covers the case.

Weak signal:

- one isolated request,
- style preference with no workflow effect,
- agent convenience with no owner benefit.

Action:

- Strong: draft a proposal.
- Medium: save a pending note or ask after the main work.
- Weak: do not evolve a skill.
