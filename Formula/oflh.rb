class Oflh < Formula
  desc "Find processes using files, directories, and open handles"
  homepage "https://github.com/karimz1/open-file-lock-handle"
  version "0.1.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.1.0/oflh-darwin-arm64"
      sha256 "24148e09c3337109a9b8d66ba7bbf52b0158b6f2d9880bd803063ebaaec5cdd5"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.1.0/oflh-darwin-amd64"
      sha256 "22360c1ce394702e25b87a7f821a23c8f13567f6146fdd5776cd8241cf0d44ee"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.1.0/oflh-linux-arm64"
      sha256 "8fd199921fbeb1575e882d02badaffc5f9eca63029044649996c51aa844f01fe"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.1.0/oflh-linux-amd64"
      sha256 "78b8d72caddaa4b031ba56dd80cb7ca126af5e126a46747de07bd966fb3b4d39"
    end
  end

  def install
    bin.install Dir["oflh-*"][0] => "oflh"
  end

  test do
    assert_match "oflh #{version}", shell_output("#{bin}/oflh --version")
  end
end
