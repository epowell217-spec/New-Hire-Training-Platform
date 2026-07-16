# Skill Quality Rubric (8 Dimensions)

Inspired by Karpathy's autoresearch methodology (via darwin-skill). Use this rubric to self-check a newly created skill or diagnose an existing one.

**Total: 100 points** (Structure 60 + Effectiveness 40)

## Structure Dimensions (60 pts) — Static Analysis

| #   | Dimension                   | Weight | Scoring Criteria                                                    |
| --- | --------------------------- | ------ | ------------------------------------------------------------------- |
| 1   | **Frontmatter Quality**     | 8      | name 规范、description 包含「做什么 + 何时用 + 触发词」、≤1024 字符 |
| 2   | **Workflow Clarity**        | 15     | 步骤明确可执行、有序号、每步有明确输入/输出                         |
| 3   | **Edge Case Coverage**      | 10     | 处理异常情况、有 fallback 路径、错误恢复                            |
| 4   | **Checkpoint Design**       | 7      | 关键决策前有用户确认、防止自主失控                                  |
| 5   | **Instruction Specificity** | 15     | 不模糊、有具体参数/格式/示例、可直接执行                            |
| 6   | **Resource Integration**    | 5      | references/scripts/assets 引用正确、路径可达                        |

## Effectiveness Dimensions (40 pts) — Requires Testing

| #   | Dimension                 | Weight | Scoring Criteria                                          |
| --- | ------------------------- | ------ | --------------------------------------------------------- |
| 7   | **Architecture Quality**  | 15     | 结构层次清晰、不冗余不遗漏、SKILL.md 是导航图不是百科全书 |
| 8   | **Empirical Performance** | 25     | 用测试 prompt 跑一遍，输出质量是否符合 skill 宣称的能力   |

## Scoring Rules

- Dimensions 1–7: Score each 1–10, multiply by weight
- Dimension 8: Run 2–3 test prompts, score output quality 1–10
- **Total = Σ(dimension × weight) / 10**, max 100
- For improvements: new score must be **strictly higher** than baseline to keep

## Empirical Performance — Testing Method

This is where the rubric differs from pure static review. Evaluation steps:

1. **Design 2–3 test prompts** per skill (common-use scenarios, not edge cases)
2. **A/B compare** (when possible): one run with the skill, one without (baseline)
3. **Score the output** against:
   - Did it complete user intent?
   - Is quality noticeably better than baseline?
   - Any negative side effects (bloat, drift, odd format)?

If running subagents is impractical (time/resource limits), fall back to **dry-run simulation**: read the skill, mentally execute a typical prompt, judge flow quality. Mark as `dry_run` in logs.

## Common Issues by Dimension

### D1: Frontmatter

- Missing trigger words (both English + Chinese for local users)
- Description only says what, not when
- Over-1024 characters
- Includes "When to Use This Skill" in body instead of description

### D2: Workflow

- No numbered phases/steps
- Steps don't specify input/output
- Parallel steps not marked as such

### D3: Edge Cases

- No "if X fails, do Y" branches
- No assumption validation
- No retry/fallback paths

### D4: Checkpoints

- No user confirmation before destructive actions
- Chains many autonomous steps without pause
- No preview before commit/deploy

### D5: Specificity

- Vague verbs ("process the file") without parameters
- Missing output format specifications
- No concrete examples of input/output

### D6: Resource Integration

- references/ files mentioned but paths broken
- Scripts referenced but not explained how to invoke
- Assets used in output but not listed

### D7: Architecture

- SKILL.md > 500 lines (should split to references/)
- Duplicate content in SKILL.md and references/
- Deeply nested references (> 1 level from SKILL.md)
- Encyclopedia-style instead of navigator-style

### D8: Empirical

- Baseline (no skill) produces equivalent output → skill adds no value
- Skill-induced bloat (over-verbose output)
- Skill drifts off-intent ("helpful" additions user didn't ask for)

## Self-Check After Creation

Before packaging a new skill, run through this rubric:

```
For each dimension 1-7:
  - Read relevant section of SKILL.md
  - Score 1-10 with one-line justification

For dimension 8:
  - Design 2 test prompts representative of typical use
  - Mentally simulate execution (or run actual subagent test)
  - Score output quality
  - If score < 7, revisit workflow before packaging
```

A skill scoring < 70 should not be packaged. Target is 80+ for production use.

## Reference

Adapted from `alchaincyf/darwin-skill` (autoresearch-inspired self-optimizing skill evaluator).
