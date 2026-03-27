# docker_postgres_fastapi

モノレポ構成: **FastAPI**（`backend/`）・**PostgreSQL**・**Next.js**（`frontend/`）を `docker compose` で一括起動します。

## 前提

- Docker / Docker Compose v2

## ローカル開発ツール（mise）

このリポジトリは **[mise](https://mise.jdx.dev/)** で **Node 22・pnpm 9.15.4・Python 3.12** を揃える想定です。設定はルートの [`.mise.toml`](.mise.toml) です。

```bash
cd /path/to/docker_postgres_fastapi
mise install          # 初回、または .mise.toml 更新後
cd frontend && pnpm install
```

**Volta を入れている場合**、シェルの PATH で Volta の `pnpm` シムが先に効くと、`pnpm install` で次のように失敗することがあります。

```text
Volta error: Could not find executable "pnpm"
```

対処の例は次のいずれかです。

1. **mise を優先する（推奨）**: `~/.bashrc` などで **`eval "$(mise activate …)"` を Volta より後に** 書き、`exec $SHELL` で読み直す。
2. **コマンドを明示**: リポジトリルートで `mise exec -- pnpm -C frontend install`
3. **Volta で pnpm を別途入れる**（mise に完全移行しない場合）: `volta install pnpm@9.15.4`

## Docker の使い方

```bash
cp .env.example .env   # 任意
docker compose up --build
```

- Next.js: [http://localhost:3000](http://localhost:3000)（投稿一覧: [http://localhost:3000/posts](http://localhost:3000/posts)）
- FastAPI OpenAPI: [http://localhost:8000/docs](http://localhost:8000/docs)
- 投稿 API（ページング）: `GET /posts?page=1&perPage=10`（`perPage` は 1〜100、既定 10）  
- PostgreSQL: ホストから `localhost:${POSTGRES_PORT:-5432}`（`.env` で変更可）

よく使う Docker コマンド:

```bash
# バックグラウンド起動
docker compose up -d

# ログを見る
docker compose logs -f frontend
docker compose logs -f backend

# 停止
docker compose down

# イメージ再ビルドして起動
docker compose up --build

# コンテナ内でバックエンドテスト
docker compose exec backend pytest
```

## 構成

| パス | 内容 |
| --- | --- |
| `backend/` | FastAPI（`uvicorn`、ホットリロード） |
| `frontend/` | Next.js（開発サーバー、ボリュームでホットリロード） |
| `infra/init.sql` | DB 初回初期化用（空ボリューム時のみ実行） |
| `docker-compose.yml` | `db` / `backend` / `frontend` |

フロントからブラウザで API を叩く URL は `NEXT_PUBLIC_API_URL`（既定: [http://localhost:8000](http://localhost:8000)）です。

## pnpm の使い方（フロントエンド）

- フロントのパッケージマネージャは **pnpm 固定**です（`npm` / `yarn` は使わない）。
- ロックファイルは **`frontend/pnpm-lock.yaml` のみ**を扱います（`package-lock.json` は作らない）。

基本コマンド:

```bash
cd frontend

# 依存インストール
pnpm install

# 依存追加
pnpm add react-select
pnpm add -D @types/some-package

# 開発サーバー
pnpm run dev

# Lint
pnpm run lint
```

依存を更新したときの Docker 側注意点:

- `pnpm-lock.yaml` 更新後は、コンテナ起動時に `frontend/docker-entrypoint.sh` が `pnpm install --frozen-lockfile` を実行します。
- それでも依存不整合が残る場合は、`frontend_node_modules` ボリュームを削除して再作成します。  
  `docker volume rm docker_postgres_fastapi_frontend_node_modules`  
  （プロジェクト名が違う場合は `docker volume ls` で確認）

補足:

- DB のデータは名前付きボリューム `pgdata` に保持されます。
