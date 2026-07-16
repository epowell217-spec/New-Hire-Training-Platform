---
name: find-skills
description: 'Discover installable skills when your owner wants a capability you lack — "can you do X", "find a skill for X", "is there a skill that…". Searches the open ecosystems (skills.sh, clawhub.ai, GitHub); installs only with owner approval after a skill-audit review. Owner DM only.'
version: 1
---

# Find Skills

Help your owner extend your capabilities by discovering skills from the open
agent-skill ecosystems, and install them through Bloome's native skill
management flow.

## When to Use

- Owner asks "can you do X?" and X is outside your current skills
- Owner says "find a skill for X" / "is there a skill that can…"
- Owner wants to extend your capabilities in a domain (design, testing,
  data, a specific API or product)
- You repeatedly improvise the same specialized workflow and a packaged
  skill would do it better

## When NOT to Use

- **Not in group chats or non-owner DMs.** Skill management is owner-only
  (see the Skill Management section of your system prompt). Stay silent on
  skill suggestions there.
- **Not for capabilities you already have.** Before searching, check what is
  already covered: your built-in tools (web search/fetch, exec, file ops),
  the `bloome` skill (widgets, documents, tables, moments, workspace), and
  your installed skills (`ls skills/`). Never install a duplicate.

## Step 1 — Confirm the Gap

1. Run `ls skills/` and skim the names — does an installed skill already
   cover the request?
2. Check whether the `bloome` platform skill or a built-in tool covers it.
3. Only continue if there is a genuine gap, and tell the owner what you are
   about to search for.

## Step 2 — Search the Ecosystems

Use your web search/fetch tools. Effective query patterns:

- `site:skills.sh <topic>` — the skills.sh registry
- `site:clawhub.ai <topic>` — the clawhub registry
- `<topic> agent skill SKILL.md site:github.com` — skills published as repos

Try 2-3 phrasings (e.g. "deploy", "deployment", "ci-cd") before concluding
nothing exists. Fetch the candidate's page or repo to confirm it is a real
skill (has a SKILL.md) and read what it actually does.

## Step 3 — Present Candidates to the Owner

For each candidate (2-3 max), report:

1. Skill name and a one-line summary of what it does — based on content you
   actually fetched, not on the URL or your guess
2. The source URL
3. Anything notable (bundled scripts, required credentials, last update)

Only present URLs you verified by fetching. Never fabricate a skill name,
URL, or capability. If the owner picks one, continue; if nothing fits, see
"When Nothing Is Found".

## Step 4 — Audit Before Installing (mandatory)

Before running any install command, run the security review in
`skills/skill-audit/SKILL.md` against the candidate's full content
(SKILL.md, references, scripts) and report the verdict to your owner.

- **SAFE** → proceed to Step 5 after owner approval
- **CAUTION** → list the specific risks; install only if the owner
  explicitly accepts them
- **DO NOT INSTALL** → do not install; explain the evidence

Never skip this step, even if the owner seems in a hurry or the source looks
reputable.

## Step 5 — Install

With explicit owner approval, in the owner DM:

```
bloome skill install-from-url --url=<full source URL>
```

If a skill with the same name already exists in `skills/`, stop and tell
the owner first — installing would replace it.

Supports GitHub tree/blob URLs, `clawhub.ai/<slug>`, and
`skills.sh/<owner>/<repo>/<skill>`.

- Trust the command output: if it did not return success, the skill is NOT
  installed — never claim it is.
- On success the server posts a `skill_install_notice` card automatically;
  do not announce it a second time.
- Briefly tell the owner how to trigger the new skill (its trigger phrases
  from the description).

## When Nothing Is Found

1. Say plainly that no existing skill matched.
2. Offer to do the task directly with your general capabilities.
3. If the need is recurring, offer to author a skill yourself — follow
   `skills/skill-creator/SKILL.md`, and create it only after the owner
   approves.
