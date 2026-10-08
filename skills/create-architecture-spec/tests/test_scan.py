import contextlib
import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location(
    "architecture_scan",
    Path(__file__).parents[1] / "scripts" / "scan.py",
)
scan = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(scan)


@contextlib.contextmanager
def in_directory(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


class ScanTests(unittest.TestCase):
    def test_discovers_nested_manifests_and_glob_entrypoints(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "apps" / "api").mkdir(parents=True)
            (root / "apps" / "api" / "package.json").write_text("{}", encoding="utf-8")
            (root / "cmd" / "worker").mkdir(parents=True)
            (root / "cmd" / "worker" / "main.go").write_text("package main", encoding="utf-8")

            with in_directory(root):
                self.assertIn("apps/api/package.json", scan.find_manifest_files())
                self.assertIn("cmd/worker/main.go", scan.find_entry_points())

    def test_discovers_instruction_and_container_variants(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "AGENTS.md").write_text("# Rules", encoding="utf-8")
            (root / "backend").mkdir()
            (root / "backend" / "AGENTS.md").write_text("# Backend rules", encoding="utf-8")
            (root / "Dockerfile.dev").write_text("FROM python:3.13", encoding="utf-8")

            with in_directory(root):
                self.assertEqual(
                    ["AGENTS.md", "backend/AGENTS.md"],
                    scan.find_instruction_files(),
                )
                self.assertIn("Dockerfile.dev", scan.find_container_files())

    def test_cli_report_is_a_map_not_manifest_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            secret = "do-not-copy-manifest-values"
            (root / "package.json").write_text(secret, encoding="utf-8")

            output = io.StringIO()
            with in_directory(root), contextlib.redirect_stdout(output):
                self.assertEqual(0, scan.main([]))

            report = output.getvalue()
            self.assertIn("package.json", report)
            self.assertNotIn(secret, report)


if __name__ == "__main__":
    unittest.main()
