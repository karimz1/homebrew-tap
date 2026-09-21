"""Verify published executables and generate the formula locally."""
import hashlib
from pathlib import Path
import re
import sys
from release import TARGETS, binary_name, formula


def verify(root, tag, current):
    if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise ValueError("Only stable semantic versions can update the tap")
    sums = {}
    for line in (root / "checksums.txt").read_text().splitlines():
        digest, name = line.split("  ", 1)
        if not re.fullmatch(r"[0-9a-f]{64}", digest) or Path(name).name != name or name in sums:
            raise ValueError("Invalid or duplicate checksum entry")
        sums[name] = digest
    if set(sums) != {binary_name(system, arch) for system, arch in TARGETS}:
        raise ValueError("Expected exactly six executable checksums")
    for system, arch in TARGETS:
        if system == "windows":
            continue
        name = binary_name(system, arch)
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != sums[name]:
            raise ValueError(f"Checksum mismatch: {name}")
    old = re.search(r'^  version "(\d+\.\d+\.\d+)"', current, re.M)
    if old and tuple(map(int, old[1].split('.'))) > tuple(map(int, tag[1:].split('.'))):
        raise ValueError("Refusing to downgrade the formula")
    return formula(tag, sums)


if __name__ == '__main__':
    root, tag = Path(sys.argv[1]), sys.argv[2]
    current = Path('Formula/oflh.rb')
    generated = verify(root, tag, current.read_text())
    (root / 'oflh.rb').write_text(generated)
    print(f"Verified {tag}: four executables; generated formula")
