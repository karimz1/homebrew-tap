class Grip < Formula
  desc "See which processes are using your files"
  homepage "https://github.com/karimz1/grip"
  version "0.0.2"
  license "MIT"
  conflicts_with "homebrew/core/grip", because: "both install a grip executable"

  on_macos do
    on_arm do
      url "https://github.com/karimz1/grip/releases/download/v0.0.2/grip_v0.0.2_darwin_arm64.tar.gz"
      sha256 "866a5cd8e881696f0ed148157ab8ecaf6ea9afbaae3c27f37504f5c2a4e28900"
    end
    on_intel do
      url "https://github.com/karimz1/grip/releases/download/v0.0.2/grip_v0.0.2_darwin_amd64.tar.gz"
      sha256 "04b3ae5e848614b2cf5f25f59145021e0f5f10a28316cb0e128af3f0d5630e07"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/karimz1/grip/releases/download/v0.0.2/grip_v0.0.2_linux_arm64.tar.gz"
      sha256 "4ec3490109b0968f34fccf8f4045cdeeafa8ae58a35a56fd587773ba5dea58f5"
    end
    on_intel do
      url "https://github.com/karimz1/grip/releases/download/v0.0.2/grip_v0.0.2_linux_amd64.tar.gz"
      sha256 "dc840a003d216d79af254167965b0903f5a1d87ae26c5c094138e9d715095cab"
    end
  end

  def install
    bin.install "grip"
  end

  test do
    assert_match "grip #{version}", shell_output("#{bin}/grip --version")
  end
end
