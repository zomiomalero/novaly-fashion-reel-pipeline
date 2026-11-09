#!/bin/sh
set -eu
REPO_NAME="${1:-novaly-fashion-reel-pipeline}"
OWNER="${2:-zomiomalero}"
if ! command -v gh >/dev/null 2>&1; then
  echo 'ERROR: Install GitHub CLI first: brew install gh' >&2
  exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
  echo 'ERROR: Run gh auth login first.' >&2
  exit 1
fi
HERE=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$HERE"
if [ ! -d .git ]; then
  git init -b main
fi
# Use the authenticated account's identity locally if not already configured.
if ! git config user.name >/dev/null 2>&1; then
  git config user.name "$(gh api user --jq '.login')"
fi
if ! git config user.email >/dev/null 2>&1; then
  git config user.email "$(gh api user --jq '"\(.id)+\(.login)@users.noreply.github.com"')"
fi
git add -A
# Reject ALL unreviewed personal/reference media, but allow our declared, original
# technical plates and procedural material-study images in assets/.
if git diff --cached --name-only | grep -E '(^|/)(private_reference_lab|demo_output|demo_audio|reference_analysis)/|\.(mp4|mov|m4a|wav|mp3)$'; then
  echo 'ERROR: Private study material or video/audio media was staged. Refusing public push.' >&2
  exit 1
fi
if git diff --cached --name-only | grep -E '\.(jpg|jpeg|png|webp)$' | grep -v -E '^assets/(original-material-studies|technical-plates)/'; then
  echo 'ERROR: Unexpected image outside the original, approved art asset folders.' >&2
  exit 1
fi
if ! git diff --cached --quiet; then
  git commit -m "Initial original fashion reel production pipeline"
fi
if git remote get-url origin >/dev/null 2>&1; then
  echo 'ERROR: origin already configured. Check before publishing.' >&2
  exit 1
fi
# The requested destination is PUBLIC. Never include the separate private
# video-analysis archive, original clips, or any keys in this repository.
echo "Publishing PUBLIC GitHub repository: $OWNER/$REPO_NAME"
gh repo create "$OWNER/$REPO_NAME" --public --source=. --remote=origin --push
printf '\nPublished: https://github.com/%s/%s\n' "$OWNER" "$REPO_NAME"
