# docker_postgres_fastapi

モノレポ構成: **FastAPI**（`backend/`）・**PostgreSQL**・**Next.js**（`frontend/`）を `docker compose` で一括起動します。

## 前提

- Docker / Docker Compose v2

## セットアップ

```bash
cp .env.example .env   # 任意
docker compose up --build
```

- Next.js: http://localhost:3000（投稿一覧: http://localhost:3000/posts）  
- FastAPI OpenAPI: http://localhost:8000/docs  
- 投稿 API（ページング）: `GET /posts?page=1&perPage=10`（`perPage` は 1〜100、既定 10）  
- PostgreSQL: ホストから `localhost:${POSTGRES_PORT:-5432}`（`.env` で変更可）

## 構成

| パス | 内容 |
|------|------|
| `backend/` | FastAPI（`uvicorn`、ホットリロード） |
| `frontend/` | Next.js（開発サーバー、ボリュームでホットリロード） |
| `infra/init.sql` | DB 初回初期化用（空ボリューム時のみ実行） |
| `docker-compose.yml` | `db` / `backend` / `frontend` |

フロントからブラウザで API を叩く URL は `NEXT_PUBLIC_API_URL`（既定: `http://localhost:8000`）です。

## 開発メモ

- 依存を変えたらイメージの再ビルドが必要です: `docker compose build --no-cache` など。
- フロントの `package-lock.json` を更新したあと、コンテナ起動時に **`npm ci` が自動実行**されます（`frontend/docker-entrypoint.sh`）。それでも解消しない場合はボリュームを捨ててから再ビルドしてください:  
  `docker volume rm docker_postgres_fastapi_frontend_node_modules`（プロジェクト名が違う場合は `docker volume ls` で名前を確認）。
- ホストで直接 `next build` する場合は、リポジトリ直下で `cd frontend && npm install` 済みである必要があります。
- DB のデータは名前付きボリューム `pgdata` に保持されます。
