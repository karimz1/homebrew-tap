"""Verify published executables and generate the formula locally."""
import hashlib
from pathlib import Path
import re
import sys
from release import TARGETS, binary_name, formula, cask


def verify(root, tag, current):
    if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise ValueError("Only stable semantic versions can update the tap")
    sums = {}
    for line in (root / "checksums.txt").read_text().splitlines():
        digest, name = line.split("  ", 1)
        if not re.fullmatch(r"[0-9a-f]{64}", digest) or Path(name).name != name or name in sums:
            raise ValueError("Invalid or duplicate checksum entry")
        sums[name] = digest
    modern = "oflh-cli.linux.amd64" in sums
    expected = {binary_name(system, arch, modern=modern) for system, arch in TARGETS}
    if modern:
        for system, arch in TARGETS:
            extensions = {"linux": ["deb", "rpm"], "darwin": ["dmg"], "windows": ["exe"]}[system]
            expected.update(f"oflh-desktop.{system}.{arch}.{ext}" for ext in extensions)
    if set(sums) != expected:
        raise ValueError("Expected a complete CLI release or combined CLI/Desktop release")
    for name, expected_digest in sums.items():
        artifact = root / name
        if not artifact.is_file() or hashlib.sha256(artifact.read_bytes()).hexdigest() != expected_digest:
            raise ValueError(f"Checksum mismatch: {name}")
    old = re.search(r'^  version "(\d+\.\d+\.\d+)"', current, re.M)
    if old and tuple(map(int, old[1].split('.'))) > tuple(map(int, tag[1:].split('.'))):
        raise ValueError("Refusing to downgrade the formula")
    return formula(tag, sums)


if __name__ == '__main__':
    root, tag = Path(sys.argv[1]), sys.argv[2]
    current = Path('Formula/oflh-cli.rb')
    if not current.exists():
        current = Path('Formula/oflh.rb')
    generated = verify(root, tag, current.read_text())
    (root / 'oflh-cli.rb').write_text(generated)
    checksum_entries = dict(
        (name, digest) for digest, name in
        (line.split("  ", 1) for line in (root / "checksums.txt").read_text().splitlines())
    )
    if "oflh-desktop.darwin.arm64.dmg" in checksum_entries:
        (root / "oflh-desktop.rb").write_text(cask(tag, checksum_entries))
    print(f"Verified {tag}; generated formula and any available Desktop cask")
