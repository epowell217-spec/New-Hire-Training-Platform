# Proposal Format

Use these formats for owner visible proposals and pending proposal files.

Every proposal must answer five questions:

1. What signal triggered this?
2. What skill or new bundle is affected?
3. What exact file content would change?
4. Why is this worth codifying?
5. What owner approval is required?

## Pending file path

Save unanswered proposals under:

```text
skills/.pending-skill-proposals/<timestamp>-<slug>.md
```

Timestamp format:

```text
YYYY-MM-DDTHH-MM-SSZ
```

Slug rules:

- lowercase,
- words separated with hyphens,
- no owner names unless necessary,
- no secrets,
- no local absolute paths.

## Existing skill edit proposal

````markdown
# Skill evolution proposal

Status: pending
Kind: edit-existing
Proposal id: <YYYY-MM-DDTHH-MM-SSZ-slug>
Target skill: <skill-name>
Target files:

- skills/<skill-name>/SKILL.md
- skills/<skill-name>/references/<file>.md

## Trigger evidence

Pattern: <repeated work | owner gold | owner correction | self gap>
Owner quote: "<exact quote or redacted summary>"
Observed count: <number or unknown>
Source: <current conversation | memory recall | owner correction | self observation>

## Why this matters

<one short paragraph>

## Proposed diff

```diff
--- skills/<skill-name>/SKILL.md
+++ skills/<skill-name>/SKILL.md
@@
+<new text>
```

## Owner decision needed

Approve this exact edit, revise it, or reject it.
No file will be changed until approval.
````

## New skill proposal

````markdown
# Skill evolution proposal

Status: pending
Kind: create-new
Proposal id: <YYYY-MM-DDTHH-MM-SSZ-slug>
New skill: <skill-name>

## Trigger evidence

Pattern: <repeated work | owner gold | owner correction | self gap>
Owner quote: "<exact quote or redacted summary>"
Observed count: <number or unknown>

## Scope

This skill handles:

- <trigger>
- <workflow>
- <output>

This skill does not handle:

- <adjacent case>
- <normal memory>

## Proposed file tree

```text
skills/<skill-name>/
  SKILL.md
  references/
    <file>.md
```

## Bundle preview

### SKILL.md frontmatter

```yaml
name: <skill-name>
description: '<trigger description with clear skip clause>'
```

### Core sections

- When to use
- Reference files
- Workflow
- Outputs
- Edge cases
- Anti patterns
- Integration

## Owner decision needed

Approve creating this bundle, revise it, or reject it.
No file will be changed until approval.
````

## Pending status updates

If the owner ignores the proposal:

```markdown
Status: pending
Last owner prompt: <timestamp>
Next action: wait for explicit approval
```

If the owner rejects:

```markdown
Status: rejected
Owner response: "<quote>"
Decision timestamp: <timestamp>
```

If the owner asks for revision:

```markdown
Status: revised
Revision reason: "<quote>"
Decision timestamp: <timestamp>
Needs approval: yes
```

If the owner approves and the change is written:

```markdown
Status: applied
Approval evidence: "<quote or UI action>"
Applied timestamp: <timestamp>
Audit log id: <id>
```

## Proposal quality checklist

Before showing the owner, check:

- Is the proposal smaller than the problem?
- Does it name the trigger evidence?
- Does it preserve the owner quote when safe?
- Does it show exactly what would change?
- Does it avoid unrelated private context?
- Does it state that approval is required?
- Does it avoid creating a duplicate skill?
- Does it keep normal memory separate from skill evolution?
