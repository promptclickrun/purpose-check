#!/usr/bin/env python3
"""Build target-specific Purpose Check skill packages."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "SKILL.md"
STRICT = ROOT / "variants" / "agent-skills" / "SKILL.md"
DIST = ROOT / "dist"
VERSION = "1.3.0"

STRICT_FRONTMATTER = """---
name: purpose-check
description: \"Use when ambiguity about the audience, intended outcome, constraints, consequences, or materially different approaches could change the deliverable; when the requested output likely does not fit the underlying goal; at consequential mid-task forks; or when the work touches consequential domains such as money, privacy, safety, authorization, legal constraints, or irreversible actions.\"
license: MIT
metadata:
  version: \"1.3.0\"
  author: \"Hermes Agent\"
  platforms: \"linux, macos, windows\"
  hermes-tags: \"purpose, judgment, requirements, decision-making, alignment\"
  hermes-category: \"productivity\"
  hermes-related-skills: \"plan\"
---
"""


def split_body(text: str) -> str:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    marker = text.find("\n---\n", 4)
    if marker < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    return text[marker + len("\n---\n") :]


def package(source: Path, output: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="purpose-check-build-") as tmp:
        root = Path(tmp) / "purpose-check"
        root.mkdir()
        shutil.copy2(source, root / "SKILL.md")
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.write(root / "SKILL.md", "purpose-check/SKILL.md")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build() -> dict[str, str]:
    canonical_text = CANONICAL.read_text(encoding="utf-8")
    strict_text = STRICT_FRONTMATTER + "\n" + split_body(canonical_text)

    STRICT.parent.mkdir(parents=True, exist_ok=True)
    DIST.mkdir(parents=True, exist_ok=True)
    STRICT.write_text(strict_text, encoding="utf-8")

    canonical_package = DIST / f"purpose-check-v{VERSION}.skill"
    strict_package = DIST / f"purpose-check-v{VERSION}-agent-skills.skill"
    package(CANONICAL, canonical_package)
    package(STRICT, strict_package)

    manifest = {
        "SKILL.md": sha256(CANONICAL),
        "variants/agent-skills/SKILL.md": sha256(STRICT),
        canonical_package.relative_to(ROOT).as_posix(): sha256(canonical_package),
        strict_package.relative_to(ROOT).as_posix(): sha256(strict_package),
    }
    lines = [f"{digest}  {name}" for name, digest in manifest.items()]
    (DIST / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest


def snapshot() -> dict[str, bytes]:
    targets = [
        STRICT,
        DIST / f"purpose-check-v{VERSION}.skill",
        DIST / f"purpose-check-v{VERSION}-agent-skills.skill",
        DIST / "SHA256SUMS",
    ]
    return {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in targets if path.exists()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale")
    args = parser.parse_args()

    before = snapshot() if args.check else {}
    manifest = build()
    if args.check:
        after = snapshot()
        if before != after:
            print("Generated artifacts are stale. Run: python3 scripts/build.py")
            return 1

    for name, digest in manifest.items():
        print(f"{digest}  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
