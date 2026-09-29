class OflhCli < Formula
  desc "Find processes using files, directories, and open handles"
  homepage "https://github.com/karimz1/open-file-lock-handle"
  version "0.2.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.2.0/oflh-cli.darwin.arm64"
      sha256 "866b9e6b5276a6b33115130c27a00a3ec25468288663eff57d864c1bf5aca1eb"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.2.0/oflh-cli.darwin.amd64"
      sha256 "da64cbf894b4043bc12bd0f372e6144e9f5bfa1bd797f96852136c07165c7387"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.2.0/oflh-cli.linux.arm64"
      sha256 "d7119a6bc9f5850d7a558dcfcf12b5c52f59f949853eb48f967dd0b90d6ea6c7"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.2.0/oflh-cli.linux.amd64"
      sha256 "7a0f813e7b8a9a1388d204ed6049e5164ed98e63bc7392ee8eba5695f9d40832"
    end
  end

  def install
    bin.install Dir["oflh-cli.*"][0] => "oflh"
  end

  test do
    assert_match "oflh #{version}", shell_output("#{bin}/oflh --version")
  end
end
