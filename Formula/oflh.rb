class Oflh < Formula
  desc "Find processes using files, directories, and open handles"
  homepage "https://github.com/karimz1/open-file-lock-handle"
  version "0.0.7"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.7/oflh-darwin-arm64"
      sha256 "262f50a12a95c9414744cb05dfa648e7956d1a4984a2d5bb8ef73cb482f3f934"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.7/oflh-darwin-amd64"
      sha256 "36885cfe77d75f628ba8d7efbfccb05845d3d469c3a3bc2e38a790563eb7ce8b"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.7/oflh-linux-arm64"
      sha256 "004a2d4c07653b2806d6e76bf074cdcc8c0546f0061d117db61fc25dfd90d9e6"
    end
    on_intel do
      url "https://github.com/karimz1/open-file-lock-handle/releases/download/v0.0.7/oflh-linux-amd64"
      sha256 "1411ffa98a26743b9155f2a6aa55b28cf1e163ae39fa26787fb5f9c4f9cab297"
    end
  end

  def install
    bin.install Dir["oflh-*"][0] => "oflh"
  end

  test do
    assert_match "oflh #{version}", shell_output("#{bin}/oflh --version")
  end
end
