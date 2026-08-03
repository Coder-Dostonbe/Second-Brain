#!/bin/sh
# Point git at the versioned hooks in .githooks/ instead of .git/hooks/.
# Run once per clone: sh scripts/install_hooks.sh

set -e
cd "$(dirname "$0")/.."
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit 2>/dev/null || true
echo "Installed: git core.hooksPath -> .githooks"
