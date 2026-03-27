"""開発用: Post / Category の初期データ投入。投稿が目標件数未満なら追加分だけ追加する。"""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Category, Post

TARGET_POST_COUNT = 26


def _post_specs() -> list[dict]:
    """目標件数ぶんの投稿定義（順序固定。既存件数より後ろだけが挿入される）。"""
    specs: list[dict] = [
        {
            "title": "Docker で開発環境をそろえる",
            "content": (
                "docker compose で API・DB・フロントを一括起動する構成のメモ。"
                "ボリュームマウントと環境変数の整理がポイント。"
            ),
            "thumbnail": "https://picsum.photos/id/180/800/500",
            "categories": ("Tech", "Tutorial"),
        },
        {
            "title": "週末の読書ノート",
            "content": "積読を減らすために、短い感想だけでも残すようにしている。",
            "thumbnail": "https://picsum.photos/id/433/800/500",
            "categories": ("Life", "News"),
        },
        {
            "title": "PostgreSQL インデックス入門メモ",
            "content": "B-Tree と部分インデックスの使い分けを調べた。EXPLAIN ANALYZE を毎回確認。",
            "thumbnail": "https://picsum.photos/id/866/800/500",
            "categories": ("Tech", "News"),
        },
    ]
    # 23 件追加（計 26 件）
    cat_rotations = [
        ("Tech", "Tutorial"),
        ("Life", "News"),
        ("Tech", "News"),
        ("News", "Tutorial"),
        ("Tech", "Life"),
    ]
    for i in range(4, TARGET_POST_COUNT + 1):
        thumbs = [201, 237, 292, 318, 367, 388, 429, 512, 582, 611, 628, 659, 682, 693, 718, 729, 742, 766, 804, 822, 835, 852, 867]
        thumb_id = thumbs[i - 4]
        cats = cat_rotations[(i - 4) % len(cat_rotations)]
        specs.append(
            {
                "title": f"シード記事（追加 {i - 3:02d} / 23）",
                "content": (
                    f"ダミー本文です。記事 ID 相当 {i}。"
                    "一覧・ページング確認用のデータ。"
                ),
                "thumbnail": f"https://picsum.photos/id/{thumb_id}/800/500",
                "categories": cats,
            }
        )
    return specs


def _ensure_categories(db: Session) -> dict[str, Category]:
    names = ["Tech", "Life", "News", "Tutorial"]
    out: dict[str, Category] = {}
    for name in names:
        found = db.scalar(select(Category).where(Category.name == name))
        if found:
            out[name] = found
        else:
            c = Category(name=name)
            db.add(c)
            db.flush()
            out[name] = c
    return out


def run() -> None:
    db: Session = SessionLocal()
    try:
        specs = _post_specs()
        current_count = db.scalar(select(func.count(Post.id))) or 0

        if current_count >= len(specs):
            return

        cats = _ensure_categories(db)

        def pick_categories(names: tuple[str, ...]) -> list[Category]:
            return [cats[n] for n in names]

        for spec in specs[current_count:]:
            db.add(
                Post(
                    title=spec["title"],
                    content=spec["content"],
                    thumbnail=spec["thumbnail"],
                    categories=pick_categories(spec["categories"]),
                )
            )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run()
