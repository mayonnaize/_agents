#!/usr/bin/env python3
"""Create a bounded project map for architecture investigation.

The report lists discovery targets. It deliberately does not copy file contents:
the agent must open relevant files and trace real flows before treating a claim as
evidence.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence


MAX_DEPTH = 4
TREE_DEPTH = 3
TREE_LIMIT = 250
EXCLUDED_DIRS = {
    ".git", ".cache", ".next", ".nuxt", ".pnp", ".tox", ".turbo",
    ".venv", ".yarn", "__pycache__", "bin", "build", "coverage",
    "dist", "generated", "node_modules", "obj", "out", "target",
    "vendor", "venv",
}

MANIFEST_PATTERNS = {
    "*.cabal", "*.csproj", "*.gemspec", "*.nimble", "*.sln", "*.slnx",
    "BUILD", "BUILD.bazel", "CMakeLists.txt", "Cargo.toml", "DESCRIPTION",
    "Gemfile", "Makefile", "Manifest.toml", "Package.swift", "Pipfile",
    "Project.toml", "WORKSPACE", "build.gradle", "build.gradle.kts",
    "composer.json", "deno.json", "deno.jsonc", "dune-project", "go.mod",
    "mix.exs", "package.json", "pom.xml", "pubspec.yaml", "pyproject.toml",
    "requirements.txt", "setup.cfg", "setup.py",
}
ENTRY_PATTERNS = {
    "Program.cs", "app.py", "cmd/*/main.go", "index.js", "index.ts",
    "main.go", "main.py", "main.swift", "server.py", "src/__main__.py",
    "src/app.js", "src/app.ts", "src/index.js", "src/index.ts",
    "src/lib.rs", "src/main.js", "src/main.py", "src/main.rs",
    "src/main.ts",
}
INSTRUCTION_PATTERNS = {"AGENTS.md", "CLAUDE.md"}
CONFIG_PATTERNS = {
    ".editorconfig", ".env.example", ".env.sample", ".env.template",
    ".eslintrc*", ".flake8", ".gitlab-ci.yml", ".golangci.y*ml",
    ".prettierrc*", "biome.json*", "docker-compose.y*ml",
    "eslint.config.*", "global.json", "jest.config.*", "pytest.ini",
    "tsconfig*.json", "vitest.config.*",
}
CONTAINER_PATTERNS = {"Dockerfile", "Dockerfile.*", "Containerfile", "Containerfile.*"}
TEST_PATTERNS = {
    "*_test.go", "*.spec.js", "*.spec.ts", "*.test.js", "*.test.ts",
    "test_*.py", "tests", "__tests__",
}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Write the report to this file")
    return parser.parse_args(argv)


def _excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def _matches(relative: str, name: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(relative, pattern)
               for pattern in patterns)


def find_files(patterns: Iterable[str], max_depth: int = MAX_DEPTH) -> list[str]:
    found: list[str] = []
    root = Path.cwd()
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        relative_dir = current_path.relative_to(root)
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        if len(relative_dir.parts) >= max_depth:
            dirs[:] = []
        for name in files:
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            if not _excluded(Path(relative)) and _matches(relative, name, patterns):
                found.append(relative)
        for name in dirs:
            relative = (relative_dir / name).as_posix()
            if _matches(relative, name, patterns):
                found.append(relative + "/")
    return sorted(set(found))


def find_manifest_files() -> list[str]:
    return find_files(MANIFEST_PATTERNS)


def find_entry_points() -> list[str]:
    return find_files(ENTRY_PATTERNS)


def find_instruction_files() -> list[str]:
    return find_files(INSTRUCTION_PATTERNS)


def find_container_files() -> list[str]:
    return find_files(CONTAINER_PATTERNS)


def directory_map() -> list[str]:
    root = Path.cwd()
    rows: list[str] = []
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        relative_dir = current_path.relative_to(root)
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS)
        if len(relative_dir.parts) >= TREE_DEPTH:
            dirs[:] = []
        for name in dirs + sorted(files):
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            rows.append(relative + ("/" if path.is_dir() else ""))
            if len(rows) == TREE_LIMIT:
                rows.append(f"[truncated after {TREE_LIMIT} entries]")
                return rows
    return rows


def git_context() -> list[str]:
    commands = {
        "revision": ["git", "rev-parse", "HEAD"],
        "branch": ["git", "branch", "--show-current"],
        "status": ["git", "status", "--short"],
    }
    rows: list[str] = []
    for label, command in commands.items():
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            return ["not a git repository"]
        value = result.stdout.strip() or ("clean" if label == "status" else "(detached)")
        rows.append(f"{label}: {value}")
    return rows


def _section(title: str, rows: Iterable[str]) -> str:
    values = list(rows)
    return "\n".join([f"=== {title} ===", *(values or ["None found."])])


def build_report() -> str:
    sections = [
        _section("REPOSITORY", git_context()),
        _section("AGENT INSTRUCTIONS — READ BEFORE SOURCE", find_instruction_files()),
        _section("DIRECTORY MAP", directory_map()),
        _section("MANIFESTS — OPEN RELEVANT FILES", find_manifest_files()),
        _section("ENTRY-POINT CANDIDATES — VERIFY CALL FLOW", find_entry_points()),
        _section("CONFIGURATION", find_files(CONFIG_PATTERNS)),
        _section("CONTAINERS", find_container_files()),
        _section("TEST SIGNALS", find_files(TEST_PATTERNS)),
    ]
    return "\n\n".join(sections) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report()
    if args.output:
        destination = Path(args.output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(report, encoding="utf-8")
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
