import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from release import TARGETS, binary_name, cask
from verify_release import verify


class VerifyTests(unittest.TestCase):
    def test_prerelease_verification_writes_separate_rc_entries(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            names = [binary_name(system, arch, modern=True) for system, arch in TARGETS]
            for system, arch in TARGETS:
                extensions = {"linux": ["deb", "rpm"], "darwin": ["dmg"], "windows": ["exe"]}[system]
                names.extend(f"oflh-desktop.{system}.{arch}.{ext}" for ext in extensions)
            entries = []
            for name in names:
                data = name.encode()
                (root / name).write_bytes(data)
                entries.append(f"{hashlib.sha256(data).hexdigest()}  {name}\n")
            (root / "checksums.txt").write_text("".join(entries))
            tap_root = Path(__file__).resolve().parents[1]
            script = Path(__file__).with_name("verify_release.py")
            stable_result = subprocess.run(
                [sys.executable, str(script), str(root), "v0.1.1"],
                cwd=tap_root,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(stable_result.returncode, 0, stable_result.stderr)
            stable_formula = (root / "oflh-cli.rb").read_text()
            stable_cask = (root / "oflh-desktop.rb").read_text()
            prerelease_result = subprocess.run(
                [sys.executable, str(script), str(root), "v0.2.0-rc.1"],
                cwd=tap_root,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(prerelease_result.returncode, 0, prerelease_result.stderr)
            self.assertEqual((root / "oflh-cli.rb").read_text(), stable_formula)
            self.assertEqual((root / "oflh-desktop.rb").read_text(), stable_cask)
            self.assertTrue((root / "oflh-cli-rc.rb").is_file())
            self.assertTrue((root / "oflh-desktop-rc.rb").is_file())

    def test_integrity_and_downgrade(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            entries = []
            for system, arch in TARGETS:
                name = binary_name(system, arch)
                data = name.encode()
                (root / name).write_bytes(data)
                entries.append(f'{hashlib.sha256(data).hexdigest()}  {name}\n')
            (root / 'checksums.txt').write_text(''.join(entries))
            self.assertIn('class Oflh', verify(root, 'v0.0.5', ''))
            with self.assertRaisesRegex(ValueError, 'downgrade'):
                verify(root, 'v0.0.5', '  version "0.0.6"')
            (root / 'oflh-linux-arm64').write_bytes(b'corrupted')
            with self.assertRaisesRegex(ValueError, 'Checksum mismatch'):
                verify(root, 'v0.0.5', '')

    def test_combined_release_uses_only_cli_in_formula(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            names = [binary_name(system, arch, modern=True) for system, arch in TARGETS]
            for system, arch in TARGETS:
                extensions = {"linux": ["deb", "rpm"], "darwin": ["dmg"], "windows": ["exe"]}[system]
                names.extend(f"oflh-desktop.{system}.{arch}.{ext}" for ext in extensions)
            entries = []
            for name in names:
                data = name.encode()
                (root / name).write_bytes(data)
                entries.append(f"{hashlib.sha256(data).hexdigest()}  {name}\n")
            (root / "checksums.txt").write_text("".join(entries))
            formula = verify(root, "v1.2.3", "")
            self.assertIn("oflh-cli.darwin.arm64", formula)
            self.assertNotIn("oflh-desktop", formula)
            sums = {name: hashlib.sha256(name.encode()).hexdigest() for name in names}
            desktop_cask = cask("v1.2.3", sums)
            self.assertIn('version "1.2.3"', desktop_cask)
            self.assertIn('app "OFLH Desktop.app"', desktop_cask)
            self.assertIn(sums["oflh-desktop.darwin.arm64.dmg"], desktop_cask)
            self.assertIn(sums["oflh-desktop.darwin.amd64.dmg"], desktop_cask)
            prerelease_formula = verify(root, "v0.2.0-rc.1", "")
            self.assertIn("class OflhCliRc < Formula", prerelease_formula)
            prerelease_cask = cask("v0.2.0-rc.1", sums)
            self.assertIn('cask "oflh-desktop-rc"', prerelease_cask)
            with self.assertRaisesRegex(ValueError, "downgrade"):
                verify(root, "v0.2.0-rc.1", '  version "0.2.0-rc.2"')
            package = root / "oflh-desktop.linux.amd64.deb"
            package.write_bytes(b"tampered")
            with self.assertRaisesRegex(ValueError, "Checksum mismatch"):
                verify(root, "v1.2.3", "")
            package.write_bytes(package.name.encode())
            (root / "checksums.txt").write_text("".join(entries[:-1]))
            with self.assertRaisesRegex(ValueError, "complete"):
                verify(root, "v1.2.3", "")
