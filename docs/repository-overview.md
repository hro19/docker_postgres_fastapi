# リポジトリ構成の概要

このドキュメントは、`docker_postgres_fastapi` モノレポ内の **Docker サービス**・**通信**・**主なディレクトリ**の関係を図で示します。

## Docker Compose 上のサービスとデータの流れ

ブラウザは **ホスト** 上のポート経由でフロントと API にアクセスします。フロントからの API 呼び出しは、ブラウザが `NEXT_PUBLIC_API_URL`（既定 [`http://localhost:8000`](http://localhost:8000)）へ直接リクエストする形です（フロントコンテナ経由ではない）。

```mermaid
flowchart LR
  subgraph hostLayer [ホスト]
    Browser[ブラウザ]
  end

  subgraph compose [Docker Compose]
    FE[frontend_Next.js]
    BE[backend_FastAPI]
    DB[(PostgreSQL_db)]
    volPg[ボリューム_pgdata]
    volNm[ボリューム_frontend_node_modules]
    volNext[ボリューム_frontend_next]
  end

  Browser -->|"localhost:3000"| FE
  Browser -->|"localhost:8000"| BE
  FE -->|"fetch_JSON_CORS許可"| BE
  BE -->|"DATABASE_URL"| DB
  DB --- volPg
  FE --- volNm
  FE --- volNext
```

## ディレクトリと責務

アプリ本体・インフラ初期化・Docker 定義の対応関係です。

```mermaid
flowchart TB
  subgraph repo [リポジトリルート]
    DC[docker-compose.yml]
    INF[infra_init.sql]
    BK[backend_FastAPI_alembic_tests]
    FR[frontend_Next.js]
  end

  DC --> BK
  DC --> FR
  DC --> INF
  INF -->|"初回のみ_DBボリューム空時"| DBConcept[(PostgreSQL_初期化)]
```

## 補足

| 項目 | 内容 |
| --- | --- |
| バックエンド | `backend/` … FastAPI ルーティングは `backend/app/routers/` に分割 |
| フロント | `frontend/` … `app/posts`・`app/posts/add` など App Router |
| 参照 | 運用手順はリポジトリルートの [README.md](../README.md) を参照 |
| DB テーブル | [database-er.md](database-er.md)（ER 図） |
