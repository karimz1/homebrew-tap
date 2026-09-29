"""Package six standalone executables and generate a Homebrew formula."""
import argparse
import hashlib
from pathlib import Path
import re

TARGETS = [("linux", "amd64"), ("linux", "arm64"), ("darwin", "amd64"),
           ("darwin", "arm64"), ("windows", "amd64"), ("windows", "arm64")]


def version(value):
    if value != "dev" and not re.fullmatch(r"v\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", value):
        raise ValueError("version must be dev or a v-prefixed semantic version")
    return value


def binary_name(system, arch, modern=False):
    if (system, arch) not in TARGETS:
        raise ValueError("unsupported target")
    if modern:
        return f"oflh-cli.{system}.{arch}" + (".exe" if system == "windows" else "")
    return f"oflh-{system}-{arch}" + (".exe" if system == "windows" else "")


def is_prerelease(tag):
    return "-" in tag[1:]


def package(binary, output, tag, system, arch):
    version(tag)
    name = binary_name(system, arch)
    data = binary.read_bytes()
    if not data:
        raise ValueError("empty executable")
    output.mkdir(parents=True, exist_ok=True)
    destination = output / name
    destination.write_bytes(data)
    destination.chmod(0o755)
    return destination


def formula(tag, checksums, repository="karimz1/open-file-lock-handle", prerelease=False):
    version(tag)
    if tag == "dev":
        raise ValueError("Homebrew requires a tagged release")
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", repository):
        raise ValueError("invalid GitHub repository")
    modern = "oflh-cli.linux.amd64" in checksums
    prerelease = prerelease or is_prerelease(tag)
    formula_class = "OflhCliRc" if prerelease else "OflhCli"
    executable_glob = "oflh-cli.*" if modern else "oflh-*"
    result = [f'class {formula_class} < Formula', '  desc "Find processes using files, directories, and open handles"',
              f'  homepage "https://github.com/{repository}"', f'  version "{tag[1:]}"',
              '  license "MIT"', '']
    for system, block in [("darwin", "macos"), ("linux", "linux")]:
        result.append(f"  on_{block} do")
        for arch, brewarch in [("arm64", "arm"), ("amd64", "intel")]:
            name = binary_name(system, arch, modern=modern)
            digest = checksums[name]
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise ValueError("invalid SHA-256 digest")
            result += [f"    on_{brewarch} do", f'      url "https://github.com/{repository}/releases/download/{tag}/{name}"',
                       f'      sha256 "{digest}"', '    end']
        result += ['  end', '']
    result += ['  def install', f'    bin.install Dir["{executable_glob}"][0] => "oflh"', '  end', '', '  test do',
               '    assert_match "oflh #{version}", shell_output("#{bin}/oflh --version")', '  end', 'end', '']
    return "\n".join(result)


def cask(tag, checksums, repository="karimz1/open-file-lock-handle", prerelease=False):
    """Generate the macOS Desktop cask from verified release DMG hashes."""
    version(tag)
    if tag == "dev" or not re.fullmatch(r"[\w.-]+/[\w.-]+", repository):
        raise ValueError("Cask requires a tagged release and valid repository")
    prerelease = prerelease or is_prerelease(tag)
    arm = checksums["oflh-desktop.darwin.arm64.dmg"]
    intel = checksums["oflh-desktop.darwin.amd64.dmg"]
    if not all(re.fullmatch(r"[0-9a-f]{64}", digest) for digest in [arm, intel]):
        raise ValueError("invalid SHA-256 digest")
    cask_token = "oflh-desktop-rc" if prerelease else "oflh-desktop"
    return f'''cask "{cask_token}" do
  arch arm: "arm64", intel: "amd64"

  version "{tag[1:]}"
  sha256 arm:   "{arm}",
         intel: "{intel}"

  url "https://github.com/{repository}/releases/download/v#{{version}}/oflh-desktop.darwin.#{{arch}}.dmg"
  name "OFLH Desktop"
  desc "Find processes using files, folders, and local ports"
  homepage "https://github.com/{repository}"

  depends_on :macos

  app "OFLH Desktop.app"
end
'''


def assemble(output, tag):
    version(tag)
    expected = [binary_name(system, arch) for system, arch in TARGETS]
    missing = [name for name in expected if not (output / name).is_file() or not (output / name).stat().st_size]
    if missing:
        raise ValueError(f"missing tested artifacts: {missing}")
    unexpected = {p.name for p in output.iterdir()} - set(expected) - {"checksums.txt"}
    if unexpected:
        raise ValueError(f"unexpected release artifacts: {sorted(unexpected)}")
    sums = {name: hashlib.sha256((output / name).read_bytes()).hexdigest() for name in sorted(expected)}
    (output / "checksums.txt").write_text("".join(f"{digest}  {name}\n" for name, digest in sorted(sums.items())), encoding="utf-8")
    return formula(tag, sums)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["package", "assemble", "validate"])
    parser.add_argument("--version", required=True, type=version)
    parser.add_argument("--os")
    parser.add_argument("--arch")
    parser.add_argument("--binary", type=Path)
    parser.add_argument("--output", type=Path, default=Path("dist"))
    parser.add_argument("--formula", type=Path)
    args = parser.parse_args()
    if args.action == "package":
        package(args.binary, args.output, args.version, args.os, args.arch)
    elif args.action == "assemble":
        result = assemble(args.output, args.version)
        if args.formula:
            args.formula.write_text(result, encoding="utf-8")
