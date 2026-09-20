# karimz1 Homebrew tap

A shared tap for Karim's tools. Each tool has its own file in `Formula/`.

## grip (beta)

See which processes are using your files. Source and documentation:
[karimz1/grip](https://github.com/karimz1/grip).

Install the beta release with:

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

MIT licensed.
