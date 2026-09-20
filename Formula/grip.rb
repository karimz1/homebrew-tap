class Grip < Formula
  desc "See which processes are using your files"
  homepage "https://github.com/karimz1/grip"
  version "0.0.1"
  license "MIT"
  conflicts_with "homebrew/core/grip", because: "both install a grip executable"

  on_macos do
    on_arm do
      url "https://github.com/karimz1/grip/releases/download/v0.0.1/grip_v0.0.1_darwin_arm64.tar.gz"
      sha256 "5dc568b92944d35950c3327ad552f6e526eea52efb486d35c2c7f490cc5d8266"
    end
    on_intel do
      url "https://github.com/karimz1/grip/releases/download/v0.0.1/grip_v0.0.1_darwin_amd64.tar.gz"
      sha256 "bb79180ad685cbf7a8ce814adff12d4fce6ca00a587e767f76ee61e557125416"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/karimz1/grip/releases/download/v0.0.1/grip_v0.0.1_linux_arm64.tar.gz"
      sha256 "e21114a4a5c9df1ec627a7cfd1dc17a2f5b55e7ac4455a09f723d3e4c4716df3"
    end
    on_intel do
      url "https://github.com/karimz1/grip/releases/download/v0.0.1/grip_v0.0.1_linux_amd64.tar.gz"
      sha256 "01b40875f3117f55d04dd0531a8a55b630d9d298f7797dcc4eb97a71ea4095e5"
    end
  end

  def install
    bin.install "grip"
  end

  test do
    assert_match "grip #{version}", shell_output("#{bin}/grip --version")
  end
end
