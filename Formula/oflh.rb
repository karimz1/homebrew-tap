class Oflh < Formula
  desc "Find processes using files, directories, and open handles"
  homepage "https://github.com/karimz1/open-file-lock-handle"
  version "0.0.8"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.8/oflh-darwin-arm64"
      sha256 "a4907a13ead5b829f49f2cfbe81e17c48d5304f33f5f5f66859af55bd7fd0cca"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.8/oflh-darwin-amd64"
      sha256 "c75a2e09eb6238c701b6fb08af7b1b74e5f9991299fd8cbdc409747328aad1f3"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.8/oflh-linux-arm64"
      sha256 "e89063d4f927e41cdcb7943e11b09d7edf85735fb824a1e89970f4afccc9dd31"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.8/oflh-linux-amd64"
      sha256 "b2f1eae2956df4bd9b4de2af7bcbf95dd556b68ac7b3691a627ff88ea13f2402"
    end
  end

  def install
    bin.install Dir["oflh-*"][0] => "oflh"
  end

  test do
    assert_match "oflh #{version}", shell_output("#{bin}/oflh --version")
  end
end
