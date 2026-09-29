# karimz1 Homebrew tap

## Open File Lock Handle (`oflh`)

Find processes using files, directories, and open handles.
[Source and documentation](https://github.com/karimz1/open-file-lock-handle).

Install the CLI/TUI:

```sh
brew install karimz1/tap/oflh-cli
```

`karimz1/tap/oflh` remains available as a compatibility alias.
After `brew update`, `brew upgrade` migrates an existing `oflh` installation to
the canonical `oflh-cli` formula.

For a published prerelease, install the separate RC formula:

```sh
brew install karimz1/tap/oflh-cli-rc
```

The stable and RC formulae both provide `oflh`. Do not install both at the same
time.

MIT licensed.

## OFLH Desktop

The tap updater publishes **oflh-desktop** from stable releases and
**oflh-desktop-rc** from published prereleases. It verifies every download
against the release's shared `checksums.txt` before updating either Cask.

Once available:

```sh
brew install --cask karimz1/tap/oflh-desktop
```

Published prereleases use a separate Cask:

```sh
brew install --cask karimz1/tap/oflh-desktop-rc
```

The stable and RC Casks install the same application and cannot be installed
side by side.

Windows and Linux Desktop users can download the EXE, DEB, or RPM installer from
the [OFLH release page](https://github.com/karimz1/open-file-lock-handle/releases).
Homebrew Cask is available on macOS. Release events update the matching stable
or RC entry. Scheduled updates continue to follow stable releases only.
