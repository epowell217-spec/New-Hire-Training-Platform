# Skill Classes

Classify the skill **before** writing it — the class determines which artifacts are mandatory and how depth is judged. Ambiguous class? Ask one direct question, then state an explicit assumption.

Inspired by Sentry's skill-writer taxonomy (https://github.com/getsentry/skills/blob/main/skills/skill-writer/references/mode-selection.md), adapted for our validator + auto-eval pipeline.

## The 5 classes

| Class                       | Request shape                                          | Required coverage dimensions                                                                                           |
| --------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| `workflow-process`          | Repeatable operation / CI / task orchestration         | Preconditions, ordered flow, failure handling, safety boundaries                                                       |
| `integration-documentation` | Library / SDK / framework integration, API correctness | API surface, config/runtime options, common use cases, known issues & workarounds, version/migration variance          |
| `security-review`           | Vulnerability finding / exploitability review          | Vulnerability classes, exploit paths, false-positive controls, remediations                                            |
| `skill-authoring`           | Creating / updating / evaluating other skills          | Source provenance, depth gates, transformed examples (happy-path + robust + anti-pattern+fix), registration/validation |
| `generic`                   | Does not match the above                               | Explicit dimensions chosen and justified in the skill body                                                             |

## Required artifacts by class

### `integration-documentation`

Must ship these reference files (validator `--strict-depth` mode enforces):

- `references/api-surface.md` — public exports, method signatures, return types
- `references/common-use-cases.md` — **≥ 6** concrete downstream use cases
- `references/troubleshooting-workarounds.md` — **≥ 8** issue / fix entries
- `SOURCES.md` — provenance table, `## Coverage matrix`, `## Open gaps` (actionable if any row is partial)

### `skill-authoring`

Must include transformed example triplets in `references/examples/` (or equivalent):

- **Happy-path** — the normal case done correctly
- **Secure / robust** — the same case hardened against edge cases
- **Anti-pattern + corrected version** — a wrong approach paired with the fix

Case studies > generic tips. Abstract principles alone fail the gate.

### `workflow-process`

Must include:

- Entry conditions (what state must be true before running)
- Numbered flow with explicit input/output per step
- Failure handling section (what to do when a step fails)
- Safety boundaries (which actions are reversible vs which need confirmation)

### `security-review`

Must include:

- Vulnerability class table (what's being looked for)
- False-positive controls (when NOT to flag something)
- Remediation patterns (what to do when found)
- Language / framework breakouts if the skill spans more than one

### `generic`

No mandatory artifacts, but SKILL.md must contain an explicit "Coverage" section listing the dimensions the skill chose to cover and why.

## Checking yourself

Before packaging, ask: does this skill match one of the 4 classes above, or is it genuinely `generic`?

- If yes to a specific class → open the corresponding required-artifact list and tick each item
- If `generic` → document the dimensions covered so reviewers can judge fit

Use `quick_validate.py --skill-class integration-documentation --strict-depth` to enforce the integration-documentation contract. Other classes are enforced by peer review against this file.

## For skill-evolve cycles

When improving an existing skill, re-classify first:

- Has the skill's purpose drifted? → class may have shifted (e.g., `workflow-process` → `integration-documentation` when you added API docs)
- Does it still have all required artifacts for its class? → if no, that's likely the weakest dimension; fix in this cycle
- Class-mismatched artifacts (`integration-documentation` class skill with no `SOURCES.md`) = high-priority fix

When running a `skill-evolve` improvement cycle, do the class check alongside the rubric scoring.
