from collections.abc import Generator

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.models import Category
from app.routers.posts import router


def _make_client_and_session() -> tuple[TestClient, sessionmaker[Session]]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    Base.metadata.create_all(bind=engine)

    app = FastAPI()

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.include_router(router)
    return TestClient(app), TestingSessionLocal


def test_カテゴリ一覧を取得できる() -> None:
    client, SessionLocal = _make_client_and_session()
    db = SessionLocal()
    try:
        db.add_all([Category(name="Zeta"), Category(name="Alpha")])
        db.commit()
    finally:
        db.close()

    response = client.get("/posts/categories")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 2, "name": "Alpha"},
        {"id": 1, "name": "Zeta"},
    ]


def test_投稿を新規作成できる() -> None:
    client, SessionLocal = _make_client_and_session()
    db = SessionLocal()
    try:
        db.add_all([Category(name="Tech"), Category(name="Tutorial")])
        db.commit()
    finally:
        db.close()

    response = client.post(
        "/posts",
        json={
            "title": "新規投稿タイトル",
            "content": "新規投稿本文",
            "thumbnail": "data:image/png;base64,abc123",
            "category_ids": [1, 2],
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["title"] == "新規投稿タイトル"
    assert payload["content"] == "新規投稿本文"
    assert payload["thumbnail"].startswith("data:image/png;base64,")
    assert {c["name"] for c in payload["categories"]} == {"Tech", "Tutorial"}


def test_サムネイルなしで投稿を新規作成できる() -> None:
    client, SessionLocal = _make_client_and_session()
    db = SessionLocal()
    try:
        db.add(Category(name="SoloCat"))
        db.commit()
    finally:
        db.close()

    response = client.post(
        "/posts",
        json={
            "title": "画像なし",
            "content": "本文のみ",
            "category_ids": [1],
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["thumbnail"] == ""


def test_存在しないカテゴリIDを指定すると失敗する() -> None:
    client, SessionLocal = _make_client_and_session()
    db = SessionLocal()
    try:
        db.add(Category(name="OnlyOne"))
        db.commit()
    finally:
        db.close()

    response = client.post(
        "/posts",
        json={
            "title": "invalid",
            "content": "invalid",
            "thumbnail": "data:image/png;base64,abc123",
            "category_ids": [999],
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "category_ids に存在しないIDが含まれています"
