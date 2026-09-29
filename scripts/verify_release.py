"""Verify published executables and generate the formula locally."""
import hashlib
from pathlib import Path
import re
import sys
from release import TARGETS, binary_name, formula, cask, is_prerelease


def version_parts(value):
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?", value)
    if not match:
        return None
    core = tuple(int(part) for part in match.group(1, 2, 3))
    prerelease = match.group(4)
    return core, prerelease.split(".") if prerelease else None


def is_downgrade(current, target):
    current_parts = version_parts(current)
    target_parts = version_parts(target)
    if not current_parts or not target_parts:
        return False
    current_core, current_pre = current_parts
    target_core, target_pre = target_parts
    if current_core != target_core:
        return current_core > target_core
    if current_pre is None:
        return target_pre is not None
    if target_pre is None:
        return False
    for current_id, target_id in zip(current_pre, target_pre):
        if current_id == target_id:
            continue
        current_numeric = current_id.isdigit()
        target_numeric = target_id.isdigit()
        if current_numeric and target_numeric:
            return int(current_id) > int(target_id)
        if current_numeric != target_numeric:
            return not current_numeric
        return current_id > target_id
    return len(current_pre) > len(target_pre)


def verify(root, tag, current):
    if not re.fullmatch(r"v\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", tag):
        raise ValueError("Only semantic-version releases can update the tap")
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
    old = re.search(r'^  version "([0-9A-Za-z.-]+)"', current, re.M)
    if old and is_downgrade(old[1], tag[1:]):
        raise ValueError("Refusing to downgrade the formula")
    return formula(tag, sums, prerelease=is_prerelease(tag))


if __name__ == '__main__':
    root, tag = Path(sys.argv[1]), sys.argv[2]
    suffix = "-rc" if is_prerelease(tag) else ""
    current = Path(f'Formula/oflh-cli{suffix}.rb')
    if not current.exists() and not is_prerelease(tag):
        current = Path('Formula/oflh.rb')
    generated = verify(root, tag, current.read_text() if current.exists() else "")
    (root / f'oflh-cli{suffix}.rb').write_text(generated)
    checksum_entries = dict(
        (name, digest) for digest, name in
        (line.split("  ", 1) for line in (root / "checksums.txt").read_text().splitlines())
    )
    if "oflh-desktop.darwin.arm64.dmg" in checksum_entries:
        (root / f'oflh-desktop{suffix}.rb').write_text(cask(tag, checksum_entries))
    print(f"Verified {tag}; generated formula and any available Desktop cask")
