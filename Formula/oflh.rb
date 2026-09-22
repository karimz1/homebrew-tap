class Oflh < Formula
  desc "Find processes using files, directories, and open handles"
  homepage "https://github.com/karimz1/open-file-lock-handle"
  version "0.0.9"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.9/oflh-darwin-arm64"
      sha256 "58088e1bb4ef95b3d63c7736c487e7272ab688d9fa18e7ebc77c8617e14e9a2d"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.9/oflh-darwin-amd64"
      sha256 "d0d24da0210b1f059898ba12ec8e02b857a305831d89b3df5d6bcd0c6319bbb2"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.9/oflh-linux-arm64"
      sha256 "dba6b7077c6e33afd3d2d4266c11fd2faaeacd6263ff86d6ee8d898912c662b1"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.9/oflh-linux-amd64"
      sha256 "4b3b7faee00a292b5099efa0a232beb3515c65544ca7c569fe5d053adc40df67"
    end
  end

  def install
    bin.install Dir["oflh-*"][0] => "oflh"
  end

  test do
    assert_match "oflh #{version}", shell_output("#{bin}/oflh --version")
  end
end
