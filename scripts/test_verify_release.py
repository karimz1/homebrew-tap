import hashlib
from pathlib import Path
import tempfile
import unittest
from release import TARGETS, binary_name, cask
from verify_release import verify


class VerifyTests(unittest.TestCase):
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
            package = root / "oflh-desktop.linux.amd64.deb"
            package.write_bytes(b"tampered")
            with self.assertRaisesRegex(ValueError, "Checksum mismatch"):
                verify(root, "v1.2.3", "")
            package.write_bytes(package.name.encode())
            (root / "checksums.txt").write_text("".join(entries[:-1]))
            with self.assertRaisesRegex(ValueError, "complete"):
                verify(root, "v1.2.3", "")
