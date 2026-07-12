#!/usr/bin/env python3
"""Validate the Purpose Check repository and release artifacts."""

from __future__ import annotations

import hashlib
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.3.0"
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
    "variants/agent-skills/SKILL.md",
    f"dist/purpose-check-v{VERSION}.skill",
    f"dist/purpose-check-v{VERSION}-agent-skills.skill",
    "dist/SHA256SUMS",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path}: missing byte-zero frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        fail(f"{path}: unclosed frontmatter")
    raw = text[4:end]
    body = text[end + 5 :]
    values: dict[str, str] = {}
    for line in raw.splitlines():
        match = re.match(r"^(name|description|license):\s*[\"']?(.*?)[\"']?$", line)
        if match:
            values[match.group(1)] = match.group(2)
    return values, raw, body


def validate_skill(path: Path, strict: bool) -> None:
    values, raw, body = parse_frontmatter(path)
    if values.get("name") != "purpose-check":
        fail(f"{path}: wrong name")
    description = values.get("description", "")
    if not description or len(description) > 1024:
        fail(f"{path}: invalid description")
    if "consequential mid-task forks" not in description:
        fail(f"{path}: trigger description regressed")
    if "purpose anchor" not in body.lower():
        fail(f"{path}: purpose anchor missing")
    if "Stage 1 block" in body:
        fail(f"{path}: stale Stage 1 block reference")
    if strict:
        top_level = {
            line.split(":", 1)[0]
            for line in raw.splitlines()
            if line and not line.startswith(" ") and ":" in line
        }
        allowed = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
        if top_level - allowed:
            fail(f"{path}: unexpected strict frontmatter keys: {sorted(top_level - allowed)}")
        for line in raw.splitlines():
            if line.startswith("  ") and ("[" in line or "{" in line):
                fail(f"{path}: structured metadata must be flattened")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_package(path: Path, expected_skill: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if names != ["purpose-check/SKILL.md"]:
            fail(f"{path}: unexpected archive members: {names}")
        payload = archive.read(names[0])
    if hashlib.sha256(payload).hexdigest() != sha256(expected_skill):
        fail(f"{path}: packaged SKILL.md differs from source")


def validate_links() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for target in re.findall(r"\[[^]]+\]\((?!https?://|#)([^)]+)\)", readme):
        clean = target.split("#", 1)[0]
        if clean and not (ROOT / clean).exists():
            fail(f"README link target missing: {clean}")
    required_phrases = [
        "GPT 5.6",
        "Claude Opus 4.8",
        "Claude Fable 5",
        "Gemini 3.1 Pro",
        "MAI Code 1 Flash",
        "Sterling Crispin",
        "Prompt your agent",
        "Manual",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in readme]
    if missing:
        fail(f"README is missing required content: {missing}")


def validate_manifest() -> None:
    manifest = ROOT / "dist" / "SHA256SUMS"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        path = ROOT / name
        if not path.exists() or sha256(path) != digest:
            fail(f"Manifest mismatch: {name}")


def main() -> int:
    for name in EXPECTED:
        if not (ROOT / name).exists():
            fail(f"Missing required file: {name}")

    canonical = ROOT / "SKILL.md"
    strict = ROOT / "variants" / "agent-skills" / "SKILL.md"
    validate_skill(canonical, strict=False)
    validate_skill(strict, strict=True)
    validate_package(ROOT / "dist" / f"purpose-check-v{VERSION}.skill", canonical)
    validate_package(ROOT / "dist" / f"purpose-check-v{VERSION}-agent-skills.skill", strict)
    validate_links()
    validate_manifest()

    print("PASS: source, variants, packages, hashes, review archive, and README links are valid")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
