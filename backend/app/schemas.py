from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    thumbnail: str
    created_at: datetime
    edited_at: datetime
    categories: list[CategoryOut]


class PaginatedPosts(BaseModel):
    items: list[PostOut]
    total: int
    page: int
    per_page: int
    total_pages: int


class ChibaSunTimes(BaseModel):
    today_sunset: datetime
    tomorrow_sunrise: datetime
