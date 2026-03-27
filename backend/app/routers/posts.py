import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Post
from app.schemas.posts import PaginatedPosts, PostOut

router = APIRouter(prefix="/posts", tags=["posts"])


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
