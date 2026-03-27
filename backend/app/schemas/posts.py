from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


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


class PostCreateIn(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    thumbnail: str = Field(default="", max_length=1024)
    category_ids: list[int] = Field(min_length=1)

    @field_validator("thumbnail", mode="before")
    @classmethod
    def thumbnail_coerce(cls, v: object) -> str:
        if v is None:
            return ""
        return str(v).strip()
