# Skill Design Principles

Principles for writing effective skills. A skill is a set of instructions injected into an agent's context window — every line competes for space with the user's actual task.

## Conciseness

The context window is shared between the skill instructions and the agent's working memory. **Default assumption: the agent is already smart.** Only include what the agent doesn't already know.

**Include:**

- Domain knowledge specific to this task
- Decision logic the agent can't infer
- Output format requirements
- Concrete examples of correct behavior

**Omit:**

- General programming knowledge
- How to use standard tools (Read, Grep, Bash)
- Obvious instructions ("be thorough", "check for errors")
- Lengthy explanations when a table or example suffices

**Rule of thumb:** If a senior engineer would skip reading it, the agent doesn't need it either.

## Degrees of Freedom

Match the specificity of your instructions to the fragility of the task.

| Fragility                              | Instruction Style                 | Example                                        |
| -------------------------------------- | --------------------------------- | ---------------------------------------------- |
| **High** — wrong output is costly      | Prescriptive steps, exact formats | Commit message format, API output schema       |
| **Medium** — multiple valid approaches | Guidelines with examples          | Code review priorities, refactoring strategy   |
| **Low** — many correct answers         | Goals and constraints only        | "Explain this code", "Summarize these changes" |

Think of the agent as exploring a path: a narrow bridge with cliffs needs specific guardrails (low freedom), while an open field allows many routes (high freedom). Over-constraining low-fragility tasks wastes context. Under-constraining high-fragility tasks produces inconsistent results.

## Progressive Disclosure

Structure skills so the agent loads only what it needs, when it needs it.

**Three-tier loading:**

1. **Metadata** (always loaded) — frontmatter `name` + `description` determine whether the skill activates
2. **Instructions** (loaded on activation) — the SKILL.md body with the core workflow
3. **Resources** (loaded on demand) — reference files, loaded conditionally based on task context

```markdown
## Step 3: Load Language Guide

| File Extension | Read This Reference        |
| -------------- | -------------------------- |
| `.py`          | `references/python.md`     |
| `.js`, `.ts`   | `references/javascript.md` |
```

Keep SKILL.md body under 500 lines. If it crosses that line, extract detail into references/ — SKILL.md is a navigator, not an encyclopedia.

**Conditional loading pattern:**

```markdown
## Advanced features

- **Form filling**: See `references/forms.md`
- **Tracked changes**: See `references/redlining.md`
- **OOXML details**: See `references/ooxml.md`
```

Avoid nested reference chains — keep all references one level deep from SKILL.md.

## Description as Trigger

The `description` field determines when agents activate the skill. It must contain phrases users actually say.

**Write in third person** — the description is injected into the system prompt; inconsistent point-of-view causes discovery problems:

```yaml
# Good — third person
description: Processes Excel files and generates reports. Use when working with spreadsheets.

# Bad — first person
description: I can help you process Excel files.

# Bad — second person
description: You can use this to process Excel files.
```

**Include all "when to use" information in the description**, not in the body. The body is only loaded after triggering, so "When to Use This Skill" sections in the body never help with selection.

### Be pushy: cover paraphrases aggressively

An agent's default failure mode is **undertrigger** — failing to invoke a skill that would have helped. Anthropic's official skill-creator says:

> Currently Claude has a tendency to "undertrigger" skills... please make the skill descriptions a little bit "pushy".

Practical translation: list the exact phrases users say, plus paraphrases, plus implicit signals. Don't trust the agent to generalize from a single literal trigger.

```yaml
# Weak — single literal, undertrigger risk
description: Build a fast dashboard for internal data.

# Pushy — covers paraphrases + implicit triggers
description: Build a fast dashboard for internal data. Use whenever the user
mentions dashboards, data visualization, internal metrics, or wants to display
any kind of company data, even if they don't explicitly ask for a "dashboard".
```

### Pair TRIGGER with explicit SKIP

A pushy description without SKIP overshoots into adjacent skills. Always pair positive triggers with negative-trigger boundaries that disambiguate from confusable siblings:

```yaml
description: Edit, patch, or fix an EXISTING skill's SKILL.md / references / scripts.
Strongly prefer when the user says: "fix this skill", "update the skill", "patch
the skill", "this skill is outdated"... Do NOT use for creating a new skill from
scratch (that's skill-creator).
```

The SKIP clause stops the agent from picking this skill when the request belongs to a sibling. Negative examples anchor the classification boundary more reliably than positive examples alone — fixing overtrigger by adding SKIP is more reliable than fixing undertrigger by adding triggers.

### Don't leak workflow into description

The description is part of the system prompt. If the description summarizes the skill's _workflow_ (what the skill does step-by-step), the agent executes that summary directly **without reading SKILL.md**. Concrete failure mode (observed in real skill testing):

> Description said `"dispatches subagent per task with code review between tasks"`. The agent did one review and stopped — even though SKILL.md flowchart required two reviews. The description had become the source of truth; the body was skipped.

**Description is for triggering, NOT for instructing.** Triggers, scope, and SKIP belong in description; everything procedural belongs in the body or references.

```yaml
# Bad — workflow leaked, body will be skipped
description: Reads diff, identifies risks, drafts review comments, posts to PR.

# Good — pure trigger, body stays authoritative
description: Review pull requests for risk. Use when asked to "review PR", "code
review this", "look at this diff". Pulls scoring rubric from references/.
```

### Pattern

```
<What it does>. Use when <trigger phrases incl. paraphrases>.
[Strongly prefer when <high-confidence signals>.] SKIP when <adjacent confusables>.
<Key capabilities or scope clarifications — not workflow steps>.
```

### Effective examples

```yaml
description: Create commit messages following Sentry conventions. Use when
committing code changes, writing commit messages, or formatting git history.
SKIP for generic commit-message styles — this skill enforces Sentry-specific format.

description: Security code review for vulnerabilities. Use when asked to "security
review", "find vulnerabilities", "check for security issues", "audit security",
"OWASP review". SKIP for general code review (use code-reviewer).
```

### Ineffective examples

```yaml
# Too vague, no trigger phrases
description: A helpful skill for code quality.

# Describes internals, not when to use
description: Runs a Python script that parses AST and generates reports.

# Workflow leaked — the agent executes the description and skips the body
description: Reads diff, identifies risks, drafts review comments, posts to PR.

# Too short, won't match varied phrasing
description: Code review.

# Pushy without SKIP — will overtrigger into sibling skills
description: Use whenever the user mentions code, files, repositories, or
programming tasks of any kind.
```

### Verification

After writing the description, ask:

1. Does it cover ≥3 paraphrases of the same user intent? (pushy check)
2. Does it have an explicit "Do NOT use for X" or "SKIP for Y" clause? (boundary check)
3. Could the agent execute the description as-is and produce the right output? If yes, you've leaked workflow — strip it back to triggers + scope.

If `Step 4.6` empirical trigger gate (in skill-creator SKILL.md) fails after these checks, escalate to the iterative loop in `description-iteration.md`.

### YAML caveat

If your description contains a colon followed by a space and a value (e.g. `... ANY of: "create a skill"`), quote the whole description or it breaks YAML parsing. Prefer single quotes if the description itself contains double-quoted phrases.

## Imperative Voice

Skills are instructions to an agent, not documentation for humans. Write in imperative voice throughout.

| Imperative (correct)                        | Descriptive (avoid)                                           |
| ------------------------------------------- | ------------------------------------------------------------- |
| Read the diff and identify changes          | This skill reads the diff and identifies changes              |
| Report findings in the table format below   | Findings should be reported in the table format below         |
| Ask the user before destructive changes     | The agent may want to ask the user before destructive changes |
| Skip test files unless explicitly requested | Test files are generally skipped unless explicitly requested  |

The agent interprets imperative instructions as direct commands. Descriptive language introduces ambiguity about whether an action is required or optional.

## Consistent Terminology

Pick one term for each concept and use it throughout the skill. Inconsistent terminology confuses agents and leads to inconsistent behavior.

| Do (pick one)             | Don't (mix these)                          |
| ------------------------- | ------------------------------------------ |
| "API endpoint" everywhere | "API endpoint", "URL", "API route", "path" |
| "field" everywhere        | "field", "box", "element", "control"       |
| "extract" everywhere      | "extract", "pull", "get", "retrieve"       |

## Avoid Duplication

Information should live in either SKILL.md **or** a reference file, not both. Prefer reference files for detailed content; keep SKILL.md for the core procedural workflow.

Don't repeat conventions already in project agent docs such as `AGENTS.md` or `CLAUDE.md`. Reference them instead of copying the entire format spec.

## Avoid Time-Sensitive Information

Don't include information that will become outdated:

```markdown
# Bad — will become wrong

If you're doing this before August 2025, use the old API.

# Good — frame as legacy

## Current method

Use the v2 API endpoint.

## Legacy patterns (deprecated)

The v1 API is no longer supported.
```

## Portable Paths

Do not bake host-specific filesystem paths into skills. These make the skill non-portable.

```
# Bad (raw absolute paths trip the portability lint)
Read /Users/<name>/projects/foo/README.md
Run python /home/<user>/tool.py

# Good
Read <repo-root>/README.md
Run python <skill-dir>/scripts/tool.py
```

The `quick_validate.py` script greps for absolute paths starting with `/Users/`, `/home/`, `/var/folders/`, and `C:\Users\` — use portable placeholders like `<repo-root>/…` or paths relative to the skill directory.

## Long Reference Files

For reference files longer than 100 lines, include a table of contents at the top so the agent can see the full scope when previewing:

```markdown
# API Reference

## Contents

- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features (batch operations, webhooks)
- Error handling patterns
```

For very large reference files (>10k words), include grep patterns in SKILL.md so the agent can jump to relevant sections:

```markdown
Find specific metrics using grep:

- Revenue data: `grep -i "revenue" references/finance.md`
- Pipeline data: `grep -i "pipeline" references/sales.md`
```
