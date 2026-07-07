#!/usr/bin/env bash
# Install driftlight to ~/.local/bin (no root needed).
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)/driftlight"
DEST="${1:-$HOME/.local/bin}"

mkdir -p "$DEST"
install -m 0755 "$SRC" "$DEST/driftlight"
echo "installed -> $DEST/driftlight"

case ":$PATH:" in
  *":$DEST:"*) : ;;
  *) echo "note: $DEST is not on your PATH. Add this to your shell rc:"
     echo "      export PATH=\"$DEST:\$PATH\"" ;;
esac

echo "run it:  driftlight --breath 4-7-8"
