class Oflh < Formula
  desc "Find processes using files, directories, and open handles"
  homepage "https://github.com/karimz1/open-file-lock-handle"
  version "0.1.1"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.1.1/oflh-darwin-arm64"
      sha256 "197dc25f75a819cc09c0bd876cf10ab00d58f292e48f43563b1e0576c5c2bc69"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.1.1/oflh-darwin-amd64"
      sha256 "2c4709e348c4e9e5ec003791d405da932b9ef0fdd585a2ac93564e7dfca3d493"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.1.1/oflh-linux-arm64"
      sha256 "d36cf3bdf3521a168c573faa620ab95ab5b5881415149a6318fbe258dbe2bf49"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.1.1/oflh-linux-amd64"
      sha256 "6b66bb1aadd678834a2bdad5224c87d409d344ad07db6dc88c73f9fd60e1533e"
    end
  end

  def install
    bin.install Dir["oflh-*"][0] => "oflh"
  end

  test do
    assert_match "oflh #{version}", shell_output("#{bin}/oflh --version")
  end
end
