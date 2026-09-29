# karimz1 Homebrew tap

## Open File Lock Handle (`oflh`)

Find processes using files, directories, and open handles.
[Source and documentation](https://github.com/karimz1/open-file-lock-handle).

Install the CLI/TUI:

```sh
brew install karimz1/tap/oflh-cli
```

`karimz1/tap/oflh` remains available as a compatibility alias.

MIT licensed.

## OFLH Desktop

The tap updater adds an **oflh-desktop** Cask after a stable release with both
macOS DMGs is published. Before updating, it verifies every release download
against the shared `checksums.txt`.

Once available:

```sh
brew install --cask karimz1/tap/oflh-desktop
```

Windows and Linux Desktop users can download the EXE, DEB, or RPM installer from
the [OFLH release page](https://github.com/karimz1/open-file-lock-handle/releases).
Homebrew Cask is available on macOS. The automatic tap updater follows stable
releases only.
