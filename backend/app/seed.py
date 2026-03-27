"""開発用: Post / Category の初期データ投入（既に投稿がある場合はスキップ）。"""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Category, Post


def run() -> None:
    db: Session = SessionLocal()
    try:
        existing = db.scalar(select(func.count(Post.id)))
        if existing and existing > 0:
            return

        tech = Category(name="Tech")
        life = Category(name="Life")
        news = Category(name="News")
        tutorial = Category(name="Tutorial")
        db.add_all([tech, life, news, tutorial])
        db.flush()

        def cat(*names: str) -> list[Category]:
            name_map = {c.name: c for c in (tech, life, news, tutorial)}
            return [name_map[n] for n in names]

        posts = [
            Post(
                title="Docker で開発環境をそろえる",
                content=(
                    "docker compose で API・DB・フロントを一括起動する構成のメモ。"
                    "ボリュームマウントと環境変数の整理がポイント。"
                ),
                thumbnail="https://picsum.photos/id/180/800/500",
                categories=cat("Tech", "Tutorial"),
            ),
            Post(
                title="週末の読書ノート",
                content="積読を減らすために、短い感想だけでも残すようにしている。",
                thumbnail="https://picsum.photos/id/433/800/500",
                categories=cat("Life", "News"),
            ),
            Post(
                title="PostgreSQL インデックス入門メモ",
                content="B-Tree と部分インデックスの使い分けを調べた。EXPLAIN ANALYZE を毎回確認。",
                thumbnail="https://picsum.photos/id/866/800/500",
                categories=cat("Tech", "News"),
            ),
        ]
        db.add_all(posts)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run()
