#!/usr/bin/env python3
"""Validate skill structure, portability, and (optionally) depth gates.

Base mode — always runs:
    - YAML frontmatter exists and parses
    - `name`: kebab-case, ≤64 chars, matches directory name
    - `description`: ≤1024 chars, no angle brackets
    - Only allowed frontmatter fields
    - SKILL.md line count (warns ≥500, errors ≥800)
    - Portability lint: no host-specific absolute paths in SKILL.md or references/

Depth mode (--strict-depth) — adds:
    - Requires SOURCES.md for integration-documentation class skills
    - Parses `## Coverage matrix` table; all required dimensions present
    - If any dimension is partial, `## Open gaps` must contain actionable lines

Usage:
    python3 quick_validate.py <skill_dir>
    python3 quick_validate.py <skill_dir> --skill-class integration-documentation --strict-depth

Exit 0 = valid, 1 = errors, 2 = bad invocation.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
SKILL_LINES_WARN = 500
SKILL_LINES_ERROR = 800

ALLOWED_FRONTMATTER_FIELDS = {
    "name", "description", "license", "allowed-tools", "metadata",
    "argument-hint", "disable-model-invocation", "model",
    # Bloome runtime fields
    "version", "always", "unlisted", "presets", "primary-only", "requires",
}

SKILL_CLASSES = {
    "auto", "workflow-process", "integration-documentation",
    "security-review", "skill-authoring", "generic",
}

INTEGRATION_REQUIRED_DIMENSIONS = [
    ("API surface", ("api surface", "api contract", "public api")),
    ("Config/runtime options", ("config", "runtime option", "configuration", "option")),
    ("Common use cases", ("common use", "usage pattern", "use case")),
    ("Known issues/workarounds", ("known issue", "failure mode", "troubleshooting", "workaround")),
    ("Version/migration variance", ("version", "migration", "deprecation", "variance")),
]

INTEGRATION_REQUIRED_REFERENCES = {
    "references/api-surface.md": None,
    "references/common-use-cases.md": 6,
    "references/troubleshooting-workarounds.md": 8,
}

PARTIAL_STATUS_TOKENS = ("partial", "missing", "incomplete", "todo", "unknown")
ACTION_TOKENS = (
    "add", "collect", "document", "retrieve", "validate",
    "test", "confirm", "expand", "review", "map",
)

MACHINE_SPECIFIC_PATH_PATTERNS = (
    re.compile(r"/Users/[^/\s`\"'<>)](?:[^\s`\"'<>)]*)"),
    re.compile(r"/home/[^/\s`\"'<>)](?:[^\s`\"'<>)]*)"),
    re.compile(r"/var/folders/[^/\s`\"'<>)](?:[^\s`\"'<>)]*)"),
    re.compile(r"/private/var/folders/[^/\s`\"'<>)](?:[^\s`\"'<>)]*)"),
    re.compile(r"[A-Za-z]:\\Users\\[^\s`\"'<>)](?:[^\s`\"'<>)]*)"),
)


def strip_inline_code(text: str) -> str:
    """Remove fenced and inline code so deliberately-wrong path examples don't trip the lint."""
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"~~~[\s\S]*?~~~", "", text)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def find_machine_specific_paths(text: str) -> list[str]:
    scrubbed = strip_inline_code(text)
    matches: list[str] = []
    for pattern in MACHINE_SPECIFIC_PATH_PATTERNS:
        for match in pattern.finditer(scrubbed):
            value = match.group(0)
            if value not in matches:
                matches.append(value)
    return matches


def infer_skill_class(description: str, body: str) -> str:
    text = f"{description}\n{body}".lower()
    if any(k in text for k in ("create a skill", "write a skill", "skill-writer", "skill-creator")):
        return "skill-authoring"
    if any(k in text for k in ("api surface", "public api", "sdk", "library integration")):
        return "integration-documentation"
    if any(k in text for k in ("vulnerability", "owasp", "security review", "security audit")):
        return "security-review"
    if any(k in text for k in ("workflow", "checklist", "runbook", "ci/cd", "pipeline")):
        return "workflow-process"
    return "generic"


def get_section_lines(markdown: str, heading_name: str) -> list[str]:
    lines = markdown.splitlines()
    needle = heading_name.lower()
    start = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## ") and needle in stripped.lower():
            start = i
            break
    if start is None:
        return []
    out: list[str] = []
    for line in lines[start + 1:]:
        if line.strip().startswith("## "):
            break
        out.append(line)
    return out


def parse_coverage_rows(sources_md: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for line in get_section_lines(sources_md, "coverage matrix"):
        stripped = line.strip()
        if not stripped.startswith("|") or re.match(r"^\|\s*-+\s*\|", stripped):
            continue
        cols = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cols) < 2:
            continue
        if cols[0].lower() in {"dimension", "coverage status"}:
            continue
        rows.append((cols[0].lower(), cols[1].lower()))
    return rows


def count_list_items(markdown: str) -> int:
    count = 0
    in_code = False
    for line in markdown.splitlines():
        if re.match(r"^\s*(```|~~~)", line):
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.match(r"^\s*(?:-|\d+\.)\s+", line):
            count += 1
    return count


def validate_portability(skill_dir: Path, skill_body: str, errors: list[str], warnings: list[str], strict: bool) -> None:
    severity = errors if strict else warnings
    hits: list[str] = []

    skill_hits = find_machine_specific_paths(skill_body)
    if skill_hits:
        hits.append(f"SKILL.md → {', '.join(skill_hits[:3])}")

    refs = skill_dir / "references"
    if refs.exists():
        for ref in sorted(refs.rglob("*.md")):
            ref_hits = find_machine_specific_paths(ref.read_text())
            if ref_hits:
                hits.append(f"{ref.relative_to(skill_dir)} → {', '.join(ref_hits[:3])}")

    if hits:
        severity.append(
            "Machine-specific absolute paths detected (prefer `<repo-root>/…` or `<skill-dir>/…`): "
            + "; ".join(hits)
        )


def validate_integration_depth(skill_dir: Path, errors: list[str], warnings: list[str], strict: bool) -> None:
    severity = errors if strict else warnings
    sources = skill_dir / "SOURCES.md"
    if not sources.exists():
        severity.append(
            "integration-documentation skills should ship SOURCES.md "
            "with `## Coverage matrix` and `## Open gaps` sections"
        )
        return

    text = sources.read_text()
    rows = parse_coverage_rows(text)
    if not rows:
        severity.append("SOURCES.md is missing a parseable `## Coverage matrix` table")
    else:
        missing = []
        for label, tokens in INTEGRATION_REQUIRED_DIMENSIONS:
            if not any(any(tok in dim for tok in tokens) for dim, _ in rows):
                missing.append(label)
        if missing:
            severity.append("Coverage matrix missing dimensions: " + ", ".join(missing))

        partial = [dim for dim, status in rows if any(tok in status for tok in PARTIAL_STATUS_TOKENS)]
        if partial:
            open_gaps = [ln.strip() for ln in get_section_lines(text, "open gaps") if ln.strip()]
            actionable = [
                ln for ln in open_gaps
                if any(tok in ln.lower() for tok in ACTION_TOKENS)
                and (ln.startswith("-") or re.match(r"^\d+\.", ln))
            ]
            if not actionable:
                severity.append(
                    "`## Coverage matrix` has partial dimensions but "
                    "`## Open gaps` lacks actionable next-retrieval steps"
                )

    for rel, min_items in INTEGRATION_REQUIRED_REFERENCES.items():
        ref = skill_dir / rel
        if not ref.exists():
            severity.append(f"Missing required reference for integration-documentation skill: {rel}")
            continue
        if min_items is not None:
            items = count_list_items(ref.read_text())
            if items < min_items:
                severity.append(f"{rel} has {items} list items; expected ≥{min_items} for depth")


def validate_frontmatter(frontmatter: dict, skill_dir: Path, errors: list[str], warnings: list[str]) -> None:
    unexpected = set(frontmatter.keys()) - ALLOWED_FRONTMATTER_FIELDS
    if unexpected:
        warnings.append(f"Unexpected frontmatter field(s): {', '.join(sorted(unexpected))}")

    if "name" not in frontmatter:
        errors.append("Missing required field: name")
    else:
        name = str(frontmatter["name"]).strip()
        if not name:
            errors.append("name must not be empty")
        elif len(name) > MAX_NAME_LENGTH:
            errors.append(f"name is too long ({len(name)} chars, max {MAX_NAME_LENGTH})")
        elif not re.match(r"^[a-z0-9-]+$", name):
            errors.append(f"name '{name}' must be kebab-case (lowercase + digits + hyphens)")
        elif name.startswith("-") or name.endswith("-") or "--" in name:
            errors.append(f"name '{name}' cannot start/end with a hyphen or contain consecutive hyphens")
        elif name != skill_dir.name:
            errors.append(f"name '{name}' must match directory name '{skill_dir.name}'")

    if "description" not in frontmatter:
        errors.append("Missing required field: description")
    else:
        desc = str(frontmatter["description"]).strip()
        if not desc:
            errors.append("description must not be empty")
        elif len(desc) > MAX_DESCRIPTION_LENGTH:
            errors.append(f"description too long ({len(desc)} chars, max {MAX_DESCRIPTION_LENGTH})")
        elif "<" in desc or ">" in desc:
            errors.append("description cannot contain angle brackets (< or >)")


def validate_skill(skill_dir: Path, declared_class: str, strict_depth: bool) -> tuple[bool, list[str], list[str], str]:
    errors: list[str] = []
    warnings: list[str] = []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, ["SKILL.md not found"], [], "generic"

    content = skill_md.read_text()
    if not content.startswith("---"):
        return False, ["No YAML frontmatter (file must start with ---)"], [], "generic"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, ["Invalid frontmatter (missing closing ---)"], [], "generic"

    try:
        frontmatter = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        return False, [f"Invalid YAML in frontmatter: {exc}"], [], "generic"

    if not isinstance(frontmatter, dict):
        return False, ["Frontmatter must be a YAML mapping"], [], "generic"

    validate_frontmatter(frontmatter, skill_dir, errors, warnings)

    line_count = len(content.splitlines())
    if line_count >= SKILL_LINES_ERROR:
        errors.append(
            f"SKILL.md is {line_count} lines (≥{SKILL_LINES_ERROR}). "
            "Extract detail into references/ — SKILL.md is a navigator, not an encyclopedia."
        )
    elif line_count >= SKILL_LINES_WARN:
        warnings.append(
            f"SKILL.md is {line_count} lines (≥{SKILL_LINES_WARN}). "
            "Consider moving detail into references/."
        )

    validate_portability(skill_dir, content, errors, warnings, strict_depth)

    resolved_class = declared_class
    if resolved_class == "auto":
        resolved_class = infer_skill_class(str(frontmatter.get("description", "")), content)

    if resolved_class == "integration-documentation":
        validate_integration_depth(skill_dir, errors, warnings, strict_depth)

    return len(errors) == 0, errors, warnings, resolved_class


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("skill_directory")
    parser.add_argument("--skill-class", choices=sorted(SKILL_CLASSES), default="auto",
                        help="Force classification. Default: infer from description + body.")
    parser.add_argument("--strict-depth", action="store_true",
                        help="Promote depth + portability warnings to errors.")
    args = parser.parse_args()

    skill_dir = Path(args.skill_directory).expanduser().resolve()
    if not skill_dir.is_dir():
        print(f"ERROR: not a directory: {skill_dir}", file=sys.stderr)
        return 2

    ok, errors, warnings, resolved_class = validate_skill(skill_dir, args.skill_class, args.strict_depth)

    print(f"\n  skill   {skill_dir.name}")
    print(f"  class   {resolved_class}")
    print(f"  mode    {'strict-depth' if args.strict_depth else 'base'}\n")

    if errors:
        print("  ERRORS:")
        for e in errors:
            print(f"    ✗ {e}")
        print()
    if warnings:
        print("  WARNINGS:")
        for w in warnings:
            print(f"    ! {w}")
        print()

    if ok and not warnings:
        print("  ✓ skill is valid (no warnings)\n")
    elif ok:
        print("  ✓ skill is valid (with warnings)\n")
    else:
        print("  ✗ skill has validation errors\n")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
