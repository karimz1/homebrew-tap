# karimz1 Homebrew tap

## Open File Lock Handle (`oflh`)

Find processes using files, directories, and open handles.
[Source and documentation](https://github.com/karimz1/open-file-lock-handle).

Until the first renamed stable release is published, install the new version from source:

```sh
brew install --HEAD karimz1/tap/oflh
oflh .
```

After that release, use `brew install karimz1/tap/oflh` for a prebuilt executable.
Existing `grip` installations will migrate through Homebrew's formula rename mapping
when the first stable `oflh` formula is available. The legacy formula remains usable
until then. This does not affect Homebrew core's unrelated `grip` package.

## Updating

**Update oflh** verifies the four Unix executables against the published SHA-256
checksums and generates the formula locally. It refuses downgrades, drafts, and
prereleases. It touches only this tool's formula and migration entry.

The source repository dispatches this workflow immediately when a stable release is
published. This requires its `HOMEBREW_TAP_TOKEN` Actions secret: a fine-grained token
limited to this tap with **Actions: Read and write** permission. Without the secret,
the source workflow fails with setup instructions; the manual updater and daily
fallback remain available.

```sh
gh workflow run update-oflh.yml --repo karimz1/homebrew-tap
```

Other tools and taps remain independent. MIT licensed.
