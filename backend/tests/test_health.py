from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers.health import router


def test_ルートエンドポイントは稼働メッセージを返す() -> None:
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI is running"}
