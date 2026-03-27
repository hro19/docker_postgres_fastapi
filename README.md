# docker_postgres_fastapi

モノレポ構成: **FastAPI**（`backend/`）・**PostgreSQL**・**Next.js**（`frontend/`）を `docker compose` で一括起動します。

## 前提

- Docker / Docker Compose v2

## セットアップ

```bash
cp .env.example .env   # 任意
docker compose up --build
```

- Next.js: http://localhost:3000  
- FastAPI OpenAPI: http://localhost:8000/docs  
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
- DB のデータは名前付きボリューム `pgdata` に保持されます。
