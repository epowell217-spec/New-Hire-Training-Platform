---
name: skill-creator
description: 'Guide for creating a NEW skill (SKILL.md + references/ + scripts/ + assets/) from scratch, in your own workspace. Use when the owner says "create a skill", "make a skill for X", "turn this into a reusable skill", or describes a repeated multi-step workflow worth codifying ("every Monday I do X, Y, Z — just know how to do this next time") — even without the word "skill". Do NOT use for editing or patching an existing skill (that is skill-evolve). Owner DM only.'
license: Complete terms in LICENSE.txt
version: 1
---

# Skill Creator

Guidance for creating effective skills. A skill is a set of instructions, references, and scripts loaded into an agent's context window so it can do a specialized task. Every token competes with the owner's real work, so **SKILL.md is a navigator — details live in `references/` and `scripts/`**.

Skill creation is an owner-only action: only in a DM with your owner, with their explicit approval, same as the Skill Management rules in your system prompt.

## Reference dispatch

Load only the references you need for this step:

| What you are doing                                                                                      | Read                              |
| ------------------------------------------------------------------------------------------------------- | --------------------------------- |
| Writing / editing SKILL.md body or description                                                          | `references/design-principles.md` |
| Choosing skill structure (Simple / Workflow+Scripts / Domain-Expert / Argument-Accepting)               | `references/skill-patterns.md`    |
| Sequencing multi-step work (Sequential / Conditional / Feedback loop / Plan-Validate-Execute / Ratchet) | `references/workflow-patterns.md` |
| Designing output (Template / Examples / Decision table / Structured JSON)                               | `references/output-patterns.md`   |
| Classifying the skill and checking required artifacts per class                                         | `references/skill-classes.md`     |
| Self-scoring the finished skill (8-dimension rubric)                                                    | `references/quality-rubric.md`    |

## Anatomy

```
skill-name/
├── SKILL.md              required — frontmatter (name, description) + body (navigator)
├── references/           (optional) detailed docs loaded on demand
├── scripts/              (optional) executable code invoked deterministically
└── assets/               (optional) templates, images, fixtures used in output
```

Do NOT ship `README.md`, `INSTALLATION_GUIDE.md`, `CHANGELOG.md`, or any user-facing docs inside a skill — they just burn context when the agent activates the skill.

Frontmatter the Bloome runtime interprets: `name` and `description` (these drive when the skill is offered). Fields like `allowed-tools` or `model` from other agent platforms are ignored here — don't rely on them.

## Creation process

### Step 1: Understand the skill with concrete examples

Before writing anything, get 2–3 concrete requests this skill should handle. Ask:

- "What functionality should this skill support?"
- "Can you give me examples of how you'd use it?"
- "What would you say that should trigger this skill?"

Avoid overwhelming the owner — one or two questions per turn. Done when you can state the skill's scope in one sentence and cite 2+ example requests.

**Trigger-phrase expansion**: after the owner gives 2–3 real phrasings, do not stop there. Auto-expand the set:

- Generate **≥3 additional paraphrases** the owner is likely to say (synonyms, indirect requests, "even when not using the word X")
- Generate **≥2 should-NOT-trigger phrases** that look adjacent but belong to another skill or your default behavior
- Present the full set in one block for owner approval ("Here's what I'd target for trigger and SKIP — confirm or correct")

This is one extra turn, not five. The owner knows their real phrasing (ground truth); you are good at expansion. The approved set feeds the description in Step 4.

Also check you are not duplicating something that exists: `ls skills/` for an installed skill that already covers it, and consider `find-skills` if a public skill might fit better than authoring from scratch.

### Step 2: Plan reusable resources

Map each concrete example to the smallest useful bundled resource:

- **Repeated code path** → `scripts/` (e.g. `scripts/rotate_pdf.py`)
- **Repeated reference lookup** → `references/` (e.g. `references/schema.md`)
- **Repeated output boilerplate** → `assets/` (e.g. `assets/hello-world/`)

If a category adds no value, skip it — don't create empty placeholders.

### Step 3: Initialize

Create the skill directly in your own workspace:

```bash
python3 skills/skill-creator/scripts/init_skill.py <skill-name> --path skills/
```

This creates `skills/<skill-name>/` with a SKILL.md template, `scripts/`, `references/`, and `assets/`. Delete the example files you won't use. (If python is unavailable, create the directory and files by hand — the structure above is all there is.)

For a trivial single-file skill, `bloome skill create --name=<slug> --content=<full SKILL.md>` works too; the directory route is better the moment references or scripts exist.

### Step 4: Edit the skill

Before writing SKILL.md, load `references/design-principles.md` and `references/skill-patterns.md`. Key rules (full content in those files):

- **SKILL.md under 500 lines** — the validator warns at 500
- **description must be pushy on TRIGGER, explicit on SKIP, no workflow leak** — agents undertrigger by default; cover paraphrases aggressively; pair every TRIGGER with a SKIP clause; never summarize the workflow in the description (it leaks, and the agent executes the summary without reading the body)
- **description in third person + trigger phrases the owner actually says** — no first/second person, no vague "a helpful skill for X"
- **imperative voice** — "Read the diff", not "This skill reads the diff"
- **portable paths** — paths relative to the skill directory, never absolute machine paths
- **avoid duplication** — information lives in SKILL.md OR references, not both
- **conditional reference loading** — table-driven, not "read all references"

Start with the bundled resources (scripts/references/assets), then write SKILL.md as the navigator that tells the agent when to reach for them.

**Scripts must be tested** — actually run them and check the output matches what the skill promises. Never ship a script you haven't executed.

### Step 5: Self-check against the quality rubric

Read `references/quality-rubric.md` and score the skill across 8 dimensions (Structure 60 pts + Effectiveness 40 pts).

```
Self-check: 84/100
- Weakest: D3 Edge Cases (6/10) — no fallback for missing input files
- Test prompts designed: 2 (happy path + ambiguous input)
- Verdict: ship
```

**Target ≥ 80.** Below 70 = don't ship; fix the weakest dimension first.

### Step 6: Validate and confirm

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/<skill-name>
```

Frontmatter + naming + portability lint. Fix what it flags. Then walk the owner through what was created (name, trigger phrases, what it will do) and confirm it matches what they asked for. Prove it on one real task before calling it done.

### Step 7: Iterate

After real usage, switch to the `skill-evolve` skill for patches — detect friction, propose a diff to the owner, apply on approval. Do not re-create a skill that needs editing.
