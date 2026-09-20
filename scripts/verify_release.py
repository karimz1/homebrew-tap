"""Check the four binary archives and formula before updating this tap."""
import hashlib
from pathlib import Path
import re
import sys

root, tag = Path(sys.argv[1]), sys.argv[2]
if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
    raise SystemExit("Only stable semantic versions can update the tap")
sums = {}
for line in (root / "checksums.txt").read_text().splitlines():
    digest, name = line.split("  ", 1)
    if not re.fullmatch(r"[0-9a-f]{64}", digest) or Path(name).name != name:
        raise SystemExit("Invalid checksum entry")
    if name in sums:
        raise SystemExit("Duplicate checksum entry")
    sums[name] = digest
names = [f"grip_{tag}_{system}_{arch}.tar.gz" for system in ("linux", "darwin") for arch in ("amd64", "arm64")]
for name in ["grip.rb"] + names:
    if hashlib.sha256((root / name).read_bytes()).hexdigest() != sums.get(name):
        raise SystemExit(f"Checksum mismatch: {name}")
formula = (root / "grip.rb").read_text()
if f'  version "{tag[1:]}"' not in formula:
    raise SystemExit("Formula version differs from the release")
for name in names:
    url = f'https://github.com/karimz1/grip/releases/download/{tag}/{name}'
    if f'url "{url}"' not in formula or f'sha256 "{sums[name]}"' not in formula:
        raise SystemExit(f"Formula does not match archive: {name}")
current = Path("Formula/grip.rb").read_text()
old = re.search(r'^  version "(\d+\.\d+\.\d+)"', current, re.M)
if old and tuple(map(int, old[1].split('.'))) > tuple(map(int, tag[1:].split('.'))):
    raise SystemExit("Refusing to downgrade the formula")
print(f"Verified {tag}: four archives and formula")
