class Grip < Formula
  desc "See which processes are using your files"
  homepage "https://github.com/karimz1/open-file-lock-handle"
  version "0.0.4"
  license "MIT"
  conflicts_with "homebrew/core/grip", because: "both install a grip executable"

  on_macos do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.4/grip_v0.0.4_darwin_arm64.tar.gz"
      sha256 "cebb7a2fc08242e7bfe0ce713915a235ce8149d65fa3d7484f5ad8e7d17f0ca0"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.4/grip_v0.0.4_darwin_amd64.tar.gz"
      sha256 "04267a82b1795bdb0f813a5eb58ad549bd10b3237d870810e1630df17953c0be"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.4/grip_v0.0.4_linux_arm64.tar.gz"
      sha256 "b2447fa91d2838571e742c3aa655023b9131a9230aa89ce34d73d9835d30939e"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.4/grip_v0.0.4_linux_amd64.tar.gz"
      sha256 "ba59dba8a7ec0848156ebe88e3eff8ddd9e64057b04dfbb964bcf50f1f6ccb41"
    end
  end

  def install
    bin.install "grip"
  end

  test do
    assert_match "grip #{version}", shell_output("#{bin}/grip --version")
  end
end
