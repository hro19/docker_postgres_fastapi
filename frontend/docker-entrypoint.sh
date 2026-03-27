#!/bin/sh
set -e
cd /app

# 名前付きボリュームの node_modules が package-lock より古いと新パッケージが無い。
# lock のハッシュが変わったときだけ npm ci する。
LOCK_HASH="$(sha256sum package-lock.json | awk '{print $1}')"
STAMP_FILE="node_modules/.lock-hash"
if [ ! -f "$STAMP_FILE" ] || [ "$(cat "$STAMP_FILE" 2>/dev/null)" != "$LOCK_HASH" ]; then
  echo "Installing npm dependencies (package-lock changed or first run)..."
  npm ci
  echo "$LOCK_HASH" >"$STAMP_FILE"
fi

exec "$@"
