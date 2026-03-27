import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Category, Post
from app.schemas.posts import CategoryOut, PaginatedPosts, PostCreateIn, PostOut

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)) -> list[CategoryOut]:
    rows = list(db.scalars(select(Category).order_by(Category.name.asc())).all())
    return [CategoryOut.model_validate(c) for c in rows]


@router.get("", response_model=PaginatedPosts)
def list_posts(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="1 始まりのページ番号"),
    perPage: int = Query(
        10,
        ge=1,
        le=100,
        alias="perPage",
        description="1 ページあたりの件数（既定 10）",
    ),
) -> PaginatedPosts:
    total = db.scalar(select(func.count(Post.id))) or 0
    total_pages = math.ceil(total / perPage) if total else 0

    stmt = (
        select(Post)
        .options(selectinload(Post.categories))
        .order_by(Post.created_at.desc(), Post.id.desc())
        .offset((page - 1) * perPage)
        .limit(perPage)
    )
    rows = list(db.scalars(stmt).all())
    items = [PostOut.model_validate(p) for p in rows]

    return PaginatedPosts(
        items=items,
        total=total,
        page=page,
        per_page=perPage,
        total_pages=total_pages,
    )


@router.post("", response_model=PostOut, status_code=201)
def create_post(payload: PostCreateIn, db: Session = Depends(get_db)) -> PostOut:
    category_ids = sorted(set(payload.category_ids))
    categories = list(
        db.scalars(select(Category).where(Category.id.in_(category_ids))).all()
    )
    if len(categories) != len(category_ids):
        raise HTTPException(
            status_code=422,
            detail="category_ids に存在しないIDが含まれています",
        )

    post = Post(
        title=payload.title.strip(),
        content=payload.content.strip(),
        thumbnail=payload.thumbnail or "",
        categories=categories,
    )
    db.add(post)
    db.commit()

    created = db.scalar(
        select(Post).options(selectinload(Post.categories)).where(Post.id == post.id)
    )
    if created is None:
        raise HTTPException(status_code=500, detail="投稿の作成に失敗しました")
    return PostOut.model_validate(created)
