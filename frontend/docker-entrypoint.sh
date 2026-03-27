#!/bin/sh
set -e
cd /app

# 名前付きボリュームの node_modules が lock より古いと新パッケージが無い。
# lock のハッシュが変わったときだけ pnpm install する。
LOCK_HASH="$(sha256sum pnpm-lock.yaml | awk '{print $1}')"
STAMP_FILE="node_modules/.lock-hash"
if [ ! -f "$STAMP_FILE" ] || [ "$(cat "$STAMP_FILE" 2>/dev/null)" != "$LOCK_HASH" ]; then
  echo "Installing pnpm dependencies (pnpm-lock.yaml changed or first run)..."
  pnpm install --frozen-lockfile
  echo "$LOCK_HASH" >"$STAMP_FILE"
fi

exec "$@"
