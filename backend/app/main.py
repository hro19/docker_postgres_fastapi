import math
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from astral import LocationInfo
from astral.sun import sun
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Post
from app.schemas import ChibaSunTimes, PaginatedPosts

app = FastAPI(title="API")

origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHIBA_LOCATION = LocationInfo("Chiba", "Japan", "Asia/Tokyo", 35.6074, 140.1065)
JST = ZoneInfo("Asia/Tokyo")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "FastAPI is running"}


@app.get("/chiba/sun-times", response_model=ChibaSunTimes)
def chiba_sun_times() -> ChibaSunTimes:
    today_jst = datetime.now(JST).date()
    tomorrow_jst = today_jst + timedelta(days=1)

    today_sun = sun(CHIBA_LOCATION.observer, date=today_jst, tzinfo=JST)
    tomorrow_sun = sun(CHIBA_LOCATION.observer, date=tomorrow_jst, tzinfo=JST)

    return ChibaSunTimes(
        today_sunset=today_sun["sunset"],
        tomorrow_sunrise=tomorrow_sun["sunrise"],
    )


@app.get("/posts", response_model=PaginatedPosts)
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
    items = list(db.scalars(stmt).all())

    return PaginatedPosts(
        items=items,
        total=total,
        page=page,
        per_page=perPage,
        total_pages=total_pages,
    )
