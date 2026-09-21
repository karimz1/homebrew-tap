import hashlib
from pathlib import Path
import tempfile
import unittest
from release import TARGETS, binary_name
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
