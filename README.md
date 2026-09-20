# karimz1 Homebrew tap

A shared tap for Karim's tools. Each tool has its own file in `Formula/`.

## grip (private development)

See which processes are using your files. Source and documentation:
[karimz1/grip](https://github.com/karimz1/grip).

Both repositories are private for now. If your SSH key has access:

```sh
brew tap karimz1/tap git@github.com:karimz1/homebrew-tap.git
brew install --HEAD karimz1/tap/grip
```

The HEAD formula builds from source with Go. Once grip has a public stable release,
the updater replaces it with a binary formula for Linux and macOS, Intel and ARM:

```sh
brew install karimz1/tap/grip
```

Use the fully qualified name because Homebrew-core has an unrelated `grip` package.
The existing `karimz1/homebrew-dupster` tap is independent and remains unchanged.
Additional formulae can be added here later.

## Updating

**Update grip** runs daily and can be started manually. It reads only stable published
releases from `karimz1/grip`, downloads the generated formula and four Unix archives,
verifies their SHA-256 checksums, and commits only `Formula/grip.rb` when changed.
Drafts and prereleases are never installed automatically. Updates older than the
currently installed formula version are ignored.

While grip is private, the default workflow token cannot read it. The updater reports
that there is no accessible release and leaves the HEAD formula alone. If needed,
set `GRIP_RELEASE_TOKEN` to a fine-grained token with read-only Contents access to
`karimz1/grip`. The updater writes to this tap with its own repository workflow token.
No cross-repository credential is needed once grip becomes public. Downloading private
release archives through Homebrew still requires separate authentication; public
installation is available only after publishing.

No workflow makes either repository public. MIT licensed.
