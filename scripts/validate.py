#!/usr/bin/env python3
"""Validate the portable Purpose Check SKILL.md repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "SKILL.md",
    "README.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "reviews/README.md",
    "reviews/01-original-review-85.pdf",
    "reviews/02-v1.1-review-96.pdf",
    "reviews/03-v1.2-review-89.pdf",
    "reviews/04-v1.3-review-95.pdf",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def parse_skill(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with byte-zero YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        fail("SKILL.md frontmatter is not closed")
    return text[4:end], text[end + 5 :]


def validate_skill() -> None:
    frontmatter, body = parse_skill(ROOT / "SKILL.md")
    name = re.search(r"^name:\s*([^\n]+)$", frontmatter, re.MULTILINE)
    description_match = re.search(r'^description:\s*["\']?(.*?)["\']?$', frontmatter, re.MULTILINE)
    if not name or name.group(1).strip() != "purpose-check":
        fail("skill name must be purpose-check")
    if description_match is None:
        fail("skill description is missing")
    assert description_match is not None
    description_text = description_match.group(1)
    if len(description_text) > 1024:
        fail("skill description is too long")
    if "consequential mid-task forks" not in description_text:
        fail("trigger description regressed")
    if "version: 1.3.0" not in frontmatter:
        fail("version 1.3.0 metadata missing")
    if body.lower().count("purpose anchor") < 4:
        fail("purpose anchor contract is incomplete")
    if "Stage 1 block" in body:
        fail("stale Stage 1 block reference remains")
    required = [
        "Explicit, current, supplied context satisfies that confirmation",
        "routine work ships quietly",
        "Material mid-task forks were checked against the purpose anchor",
    ]
    for phrase in required:
        if phrase not in body:
            fail(f"required behavioral contract missing: {phrase}")


def validate_readme() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    required = [
        "GPT 5.6",
        "Claude Opus 4.8",
        "Claude Fable 5",
        "Gemini 3.1 Pro",
        "MAI Code 1 Flash",
        "Sterling Crispin",
        "Prompt your agent",
        "Manual install",
        "any agent harness",
        "SKILL.md",
    ]
    missing = [phrase for phrase in required if phrase not in readme]
    if missing:
        fail(f"README is missing required content: {missing}")
    proprietary_suffix = "." + "skill"
    if proprietary_suffix in readme:
        fail("README still references a proprietary package suffix")
    for target in re.findall(r"\[[^]]+\]\((?!https?://|#)([^)]+)\)", readme):
        clean = target.split("#", 1)[0]
        if clean and not (ROOT / clean).exists():
            fail(f"README link target missing: {clean}")


def main() -> int:
    for name in EXPECTED:
        if not (ROOT / name).exists():
            fail(f"missing required file: {name}")
    forbidden = [ROOT / "dist", ROOT / "variants", ROOT / "scripts" / "build.py"]
    for path in forbidden:
        if path.exists():
            fail(f"vendor-specific build artifact remains: {path.relative_to(ROOT)}")
    validate_skill()
    validate_readme()
    print("PASS: portable SKILL.md, review archive, behavioral contracts, and README links are valid")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
