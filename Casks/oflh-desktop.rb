cask "oflh-desktop" do
  arch arm: "arm64", intel: "amd64"

  version "0.2.0"
  sha256 arm:   "3926bb63d8a2c6d21ee09cde54109d779acfcd2661fa14e77c3668009efe7ab3",
         intel: "8d515e04368b498a2325545eea91d755fbe6dd081b5518c5631c77c1e4ab7c2f"

  url "https://github.com/karimz1/open-file-lock-handle/releases/download/v#{version}/oflh-desktop.darwin.#{arch}.dmg"
  name "OFLH Desktop"
  desc "Find processes using files, folders, and local ports"
  homepage "https://github.com/karimz1/open-file-lock-handle"

  depends_on :macos

  app "OFLH Desktop.app"
end
