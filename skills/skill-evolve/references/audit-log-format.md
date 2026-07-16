# Audit Log Format

Use this schema for `skills/SKILL_EVOLUTION_LOG.md`.

Examples in this file follow a fictional product team — Mia (PM agent), Aya (design agent), Kai (engineering agent) — with their domain skills. Substitute your own domain and skill names.

The file is append only.
Each applied skill change appends one JSON object on one line.
This makes the log readable by agents and parsable by tools.

## File header

If the file does not exist, create it with:

```markdown
# Skill Evolution Log

Append only JSON Lines.
Each non comment line after this header is one JSON object.
```

Then append JSON lines below the header.

## JSON Lines schema

Required fields:

```json
{
  "schema": "bloome-skill-evolution-log/v1",
  "id": "2026-06-07T10-20-30Z-skill-routing-approval",
  "timestamp": "2026-06-07T10:20:30Z",
  "agent": "Mia",
  "change_kind": "edit-existing",
  "skill": "team-routing",
  "files_changed": ["skills/team-routing/SKILL.md"],
  "why": "Owner corrected delegation boundary for design briefs.",
  "trigger_pattern": "owner_correction",
  "owner_quote": "No, ask Aya for states, not colors.",
  "approval_evidence": "Owner said: approve the edit.",
  "proposal_path": "skills/.pending-skill-proposals/2026-06-07T10-18-00Z-team-routing-states.md",
  "status": "applied"
}
```

Field rules:

- `schema`: always `bloome-skill-evolution-log/v1`.
- `id`: timestamp plus short slug.
- `timestamp`: ISO 8601 UTC.
- `agent`: agent display name, or role if display name is unavailable.
- `change_kind`: `edit-existing`, `create-new`, `supersede`, or `reject-record`.
- `skill`: target skill name.
- `files_changed`: array of relative paths under `skills/`.
- `why`: one sentence.
- `trigger_pattern`: `repeated_work`, `owner_gold`, `owner_correction`, or `self_gap`.
- `owner_quote`: exact quote or redacted summary.
- `approval_evidence`: exact approval phrase or approval UI action.
- `proposal_path`: relative path to the proposal, or `null` if proposal was shown inline.
- `status`: `applied`, `superseded`, or `rejected`.

## Rejection records

Usually a rejected proposal does not need the audit log.
Write a rejection record only when the owner explicitly wants durable history or when a proposal was previously pending and could confuse future agents.

```json
{
  "schema": "bloome-skill-evolution-log/v1",
  "id": "2026-06-07T11-00-00Z-reject-validation-copy",
  "timestamp": "2026-06-07T11:00:00Z",
  "agent": "Mia",
  "change_kind": "reject-record",
  "skill": "validation-copy",
  "files_changed": [],
  "why": "Owner decided the pattern belongs in idea-discovery, not a new skill.",
  "trigger_pattern": "repeated_work",
  "owner_quote": "Do not make a new skill for this yet.",
  "approval_evidence": "Owner rejected the proposal.",
  "proposal_path": "skills/.pending-skill-proposals/2026-06-07T10-55-00Z-validation-copy.md",
  "status": "rejected"
}
```

## Superseding entries

Do not edit old lines.
If an old rule is wrong, append a new entry:

```json
{
  "schema": "bloome-skill-evolution-log/v1",
  "id": "2026-06-08T09-10-00Z-supersede-routing-states",
  "timestamp": "2026-06-08T09:10:00Z",
  "agent": "Mia",
  "change_kind": "supersede",
  "skill": "team-routing",
  "files_changed": ["skills/team-routing/SKILL.md"],
  "why": "Owner narrowed the earlier routing rule to dashboard work only.",
  "trigger_pattern": "owner_correction",
  "owner_quote": "That rule only applies to dashboard states.",
  "approval_evidence": "Owner said: yes, update it that way.",
  "proposal_path": "skills/.pending-skill-proposals/2026-06-08T09-05-00Z-routing-dashboard-states.md",
  "status": "applied",
  "supersedes": "2026-06-07T10-20-30Z-skill-routing-approval"
}
```

## Validation checks

Before appending:

- confirm explicit owner approval,
- confirm files changed match the approved proposal,
- confirm no secrets are included,
- confirm paths are relative,
- confirm JSON is valid,
- confirm one object per line.

If JSON cannot be validated by the agent's available tools, keep the object simple and avoid trailing commas.
