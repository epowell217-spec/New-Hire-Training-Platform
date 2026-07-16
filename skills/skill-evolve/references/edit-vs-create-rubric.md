# Edit vs Create Rubric

Use this file when deciding whether a learning should edit an existing skill or create a new bundle.

Examples in this file follow a fictional product team — Mia (PM agent), Aya (design agent), Kai (engineering agent) — with their domain skills. Substitute your own domain and skill names.

The default is edit.
New skills add trigger surface, maintenance cost, and chance of overlap.

## Scan order

1. List `skills/`.
2. Read skill names and descriptions.
3. Pick the closest 1 to 3 candidates.
4. Read those `SKILL.md` files.
5. Search their `references/` names.
6. Decide where the future agent should look first.

Do not scan unrelated files forever.
The goal is the best home, not perfect taxonomy.

## Related enough

A skill is related enough when at least two of these are true:

- The trigger phrases overlap.
- The same owner request would load the existing skill.
- The workflow stage is the same.
- The output artifact is the same.
- The same teammate owns the work.
- The correction applies inside that skill's flow.
- The future agent would be confused if the rule lived elsewhere.

If two or more are true, propose an edit first.

## Edit shapes

Use a targeted edit when the new learning is narrow.

Common edit shapes:

- add one bullet to `When to use`,
- add one edge case,
- add one anti pattern,
- add one example,
- add one output field,
- add one reference file,
- add one paragraph to a workflow step,
- tighten a description boundary,
- add a note to a proposal template.

Good edit proposal:

```text
Add an edge case to `team-routing`: when the owner asks for technical certainty before the product question is narrow, Mia asks Kai for feasibility only after naming the user value question.
```

Poor edit proposal:

```text
Rewrite all routing guidance because owner corrected one message.
```

## New skill shapes

Create a new skill only when the workflow has its own durable trigger and output.

New skill should have:

- a distinct name,
- a trigger description,
- a clear start condition,
- a small number of core moments,
- explicit outputs,
- edge cases,
- references only where needed,
- no scripts unless the owner later asks for them and the environment supports them.

Good new skill proposal:

```text
Create `validation-copy` because Mia has repeated a distinct workflow: turn a product assumption into fake door copy, beta invite copy, and followup questions.
```

Poor new skill proposal:

```text
Create `better-product-pm` because product thinking came up again.
```

## Similarity scoring

Use this lightweight score.

| Score        | Meaning                        | Action                                  |
| ------------ | ------------------------------ | --------------------------------------- |
| 0.80 to 1.00 | Existing skill clearly owns it | Propose edit                            |
| 0.50 to 0.79 | Adjacent but not obvious       | Show edit option and new option         |
| 0.00 to 0.49 | No close home                  | Propose new only if detection is strong |

Do not pretend the score is precise.
Use it to explain judgment.

## Decision tree

Question 1:
Would the existing skill naturally load for the future owner request?

- Yes: edit that skill.
- No: continue.

Question 2:
Is the learning only an example, edge case, or anti pattern?

- Yes: edit the closest skill.
- No: continue.

Question 3:
Does the learning introduce a full workflow with its own output?

- Yes: propose a new skill.
- No: save as pending note or normal memory.

Question 4:
Would a new skill compete with an existing skill?

- Yes: propose an edit or a reference pointer.
- No: new skill may be justified.

## Canonical home

When one lesson applies to several skills, choose one canonical home.

Choose the home by:

- strongest trigger match,
- strongest workflow ownership,
- owner correction context,
- smallest future lookup burden,
- lowest duplication.

Other skills can point to the canonical home later.
Do not copy the same rule everywhere.

## Red flags for new skill creation

Avoid new skill creation when:

- the name sounds like a quality adjective,
- the trigger overlaps with two existing skills,
- the only evidence is one owner request,
- the skill would mostly repeat another skill,
- the proposed bundle lacks a unique output,
- the agent wants convenience more than owner value.

If any red flag appears, use pending proposal instead of writing.
