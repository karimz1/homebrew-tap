class Oflh < Formula
  desc "Find processes using files, directories, and open handles"
  homepage "https://github.com/karimz1/open-file-lock-handle"
  version "0.0.5"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.5/oflh-darwin-arm64"
      sha256 "01aef4a88d9c22c5ea13c22088903793e536cf42d91360aac0fc821537bf720d"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.5/oflh-darwin-amd64"
      sha256 "7c84cf5625ada5ca2508190eb130b63e5b610592e210c173734ca0f42bceeefb"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.5/oflh-linux-arm64"
      sha256 "b465ae175292243670400ca8fe0470d8f22d2d14f5a1403eebf19d4d52476c78"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.5/oflh-linux-amd64"
      sha256 "b90d7bb1ace29b44cae7602e5eb58133bf9b7f3ae9cb66c353bc5884a59d8570"
    end
  end

  def install
    bin.install Dir["oflh-*"][0] => "oflh"
  end

  test do
    assert_match "oflh #{version}", shell_output("#{bin}/oflh --version")
  end
end
