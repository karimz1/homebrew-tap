import json
import hashlib
from pathlib import Path
import tempfile
import unittest
from release import TARGETS, assemble, binary_name, formula, package, version


class ReleaseTests(unittest.TestCase):
    def test_legacy_formula_name_migrates_to_cli(self):
        manifest = Path(__file__).resolve().parents[1] / "formula_renames.json"
        self.assertEqual(json.loads(manifest.read_text()), {"oflh": "oflh-cli"})

    def test_six_executables_and_formula(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            binary = root / "binary"
            binary.write_bytes(b"test executable")
            output = root / "dist"
            for system, arch in TARGETS:
                path = package(binary, output, "v0.1.0", system, arch)
                self.assertEqual(path.read_bytes(), binary.read_bytes())
                self.assertEqual(path.name, binary_name(system, arch))
            generated = assemble(output, "v0.1.0")
            self.assertEqual(len(list(output.iterdir())), 7)
            self.assertEqual(len(TARGETS), 6)
            for line in (output / "checksums.txt").read_text().splitlines():
                digest, filename = line.split("  ")
                self.assertEqual(digest, hashlib.sha256((output / filename).read_bytes()).hexdigest())
                if not filename.endswith('.exe'):
                    self.assertIn('/' + filename + '"', generated)
                    self.assertIn(digest, generated)
            self.assertEqual(generated.count('sha256 "'), 4)
            self.assertIn('=> "oflh"', generated)
            self.assertIn('class OflhCli < Formula', generated)
            self.assertIn('Dir["oflh-*"]', generated)
            modern_checksums = {
                binary_name(system, arch, modern=True): "a" * 64
                for system, arch in TARGETS
            }
            modern_formula = formula("v0.1.0", modern_checksums)
            self.assertIn('Dir["oflh-cli.*"]', modern_formula)
            (output / "old.zip").write_bytes(b"stale")
            with self.assertRaisesRegex(ValueError, "unexpected"):
                assemble(output, "v0.1.0")

    def test_reject_missing_or_unsafe_input(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                assemble(Path(directory), "v0.1.0")
            binary = Path(directory) / "empty"
            binary.touch()
            with self.assertRaises(ValueError):
                package(binary, Path(directory), "v0.1.0", "linux", "amd64")
        for value in ["v1; rm -rf /", "../v1.0.0", "1.0.0", "v1.0.0\n"]:
            with self.assertRaises(ValueError):
                version(value)
        with self.assertRaises(ValueError):
            formula("dev", {})
        with self.assertRaises(ValueError):
            binary_name("windows", "386")


if __name__ == "__main__":
    unittest.main()
