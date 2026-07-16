# Skill Patterns

Concrete examples of skill structures at each complexity tier, plus anti-patterns to avoid.

## Simple: SKILL.md Only

Use when the entire skill fits in under ~200 lines with no external resources needed.

**Examples:** brand-guidelines, commit, pr-writer

**Structure:**

```
brand-guidelines/
└── SKILL.md
```

**Pattern highlights:**

- Frontmatter with `name` and `description` only
- Body organized with `##` sections for different aspects
- Heavy use of tables for decision logic and examples
- No external files

**Use when:** The skill provides a single coherent set of rules or a short procedural workflow that fits comfortably in one file.

## Workflow: SKILL.md + Scripts

Use when the skill automates a multi-step workflow with structured data processing.

**Structure:**

```
iterate-pr/
├── SKILL.md
└── scripts/
    ├── fetch_pr_checks.py
    └── fetch_pr_feedback.py
```

**Pattern highlights:**

- SKILL.md documents each script's interface (arguments, output JSON schema)
- Scripts use PEP 723 inline metadata for dependencies:
  ```python
  # /// script
  # requires-python = ">=3.12"
  # dependencies = ["requests"]
  # ///
  ```
- Invoke with `uv run <skill-dir>/scripts/script_name.py` or `python3 <skill-dir>/scripts/…`
- Scripts output structured JSON for agent consumption
- Scripts handle errors explicitly — don't punt to the agent
- SKILL.md includes a fallback section for when scripts fail

**Use when:** The workflow benefits from structured data extraction, API calls, or processing that would be fragile as inline bash commands.

## Domain Expert: SKILL.md + References

Use when the skill covers a broad domain with conditional knowledge loading.

**Structure:**

```
security-review/
├── SKILL.md
├── references/
│   ├── injection.md
│   ├── xss.md
│   ├── authentication.md
│   └── … (17 reference files)
├── languages/
│   ├── python.md
│   └── javascript.md
└── infrastructure/
    ├── docker.md
    └── kubernetes.md
```

**Pattern highlights:**

- SKILL.md contains the core workflow and quick-reference tables
- Reference files loaded **conditionally** based on detected context:
  ```markdown
  | Code Type     | Load These References                                    |
  | ------------- | -------------------------------------------------------- |
  | API endpoints | `references/authorization.md`, `references/injection.md` |
  | Frontend      | `references/xss.md`, `references/csrf.md`                |
  ```
- Each reference file is self-contained and focused on one topic
- SKILL.md includes a file index so the agent knows what's available
- References are one level deep from SKILL.md (no nested chains)

**Use when:** The domain is too large for one file, but the agent only needs a subset for any given task. Progressive disclosure keeps context small.

## Argument-Accepting Skills

Use when the skill takes user input as parameters.

**Structure:**

```yaml
---
name: fix-issue
description: Fix a GitHub issue by number. Use when asked to fix, resolve, or address a GitHub issue.
disable-model-invocation: true
argument-hint: '[issue-number]'
---
Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Implement the fix
3. Write tests
4. Create a commit
```

**Pattern highlights:**

- `$ARGUMENTS` is replaced with whatever follows `/fix-issue` (e.g., `/fix-issue 123`)
- `argument-hint` provides autocomplete guidance
- `disable-model-invocation: true` prevents automatic triggering (appropriate for side-effect-heavy workflows)
- If `$ARGUMENTS` is absent from the body, arguments are appended as `ARGUMENTS: <value>`

**Note:** These frontmatter features come from other agent platforms (e.g. Claude Code). The Bloome runtime interprets only `name` and `description` — do not rely on the rest here.

## Anti-Patterns

### Over-long SKILL.md

**Problem:** SKILL.md exceeds 500 lines, consuming excessive context window.

**Fix:** Extract reference material into `references/` files. Keep SKILL.md focused on the procedural workflow and load references conditionally.

The validator warns at 500 lines and errors at 800. Use those as your ratchet.

### Missing Trigger Keywords

**Problem:** Description says "A skill for helping with code" — the agent can't match this to user requests like "review my PR" or "check for bugs".

**Fix:** Include the actual phrases users say: `Use when asked to "review code", "find bugs", "check for issues"`.

### Trigger Info in Body Instead of Description

**Problem:** The body includes a "When to Use This Skill" section, but the description is vague. The body is only loaded _after_ triggering, so this information never helps with skill selection.

**Fix:** Move all "when to use" information into the `description` field. The body contains _how_ to execute, not _when_ to activate.

### Duplicating CLAUDE.md / AGENTS.md

**Problem:** SKILL.md repeats repo conventions already in CLAUDE.md (commit format, PR process, etc.).

**Fix:** Reference CLAUDE.md where needed. Skills should add domain knowledge, not repeat general conventions. Example: "Follow the commit conventions in CLAUDE.md" instead of copying the entire spec.

### Unconditional Reference Loading

**Problem:** SKILL.md says "Read all reference files before starting" — loads 20+ files into context regardless of the task.

**Fix:** Use a decision table to load only relevant references:

```markdown
| Detected Language | Read                       |
| ----------------- | -------------------------- |
| Python            | `references/python.md`     |
| JavaScript        | `references/javascript.md` |
```

### Large References Without Navigation

**Problem:** A reference file is 500+ lines with no table of contents. The agent previews with partial reads and misses important sections.

**Fix:** Add a table of contents at the top of files over 100 lines. For very large files (>10k words), include grep patterns in SKILL.md.

### Extraneous Files

**Problem:** The skill directory includes README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, or other docs.

**Fix:** A skill should only contain files an agent needs to do the job: SKILL.md, references, scripts, assets, and LICENSE. Remove user-facing docs, development history, and setup guides.

### Scripts Without Documentation

**Problem:** SKILL.md says `uv run <skill-dir>/scripts/tool.py` but doesn't document arguments or output.

**Fix:** Document every script's interface in SKILL.md:

````markdown
### `scripts/tool.py`

Fetches X and returns structured data.

    uv run <skill-dir>/scripts/tool.py --flag VALUE

Returns JSON:
\```json
{"key": "value", "items": [...]}
\```
````

### Hardcoded Absolute Paths

**Problem:** SKILL.md references a hardcoded host-specific path (e.g., `/Users/<name>/projects/foo/…`).

**Fix:** Use portable placeholders (`<skill-dir>/…`, `<repo-root>/…`). The `quick_validate.py` portability lint catches these.

### First/Second Person Descriptions

**Problem:** Description says "I can help you process files" or "You can use this to process files."

**Fix:** Write in third person: "Processes files and generates reports. Use when working with data files."

### Time-Sensitive Information

**Problem:** SKILL.md includes "If before August 2025, use the old API" — will become wrong.

**Fix:** Use a "Legacy patterns" section with the deprecated method noted, or remove time-sensitive content entirely.
