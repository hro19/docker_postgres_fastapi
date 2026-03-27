from datetime import datetime

from fastapi import FastAPI
from fastapi.testclient import TestClient

import app.routers.chiba as chiba_router


class _FixedDateTime(datetime):
    @classmethod
    def now(cls, tz=None) -> datetime:
        return cls(2026, 3, 27, 9, 0, 0, tzinfo=tz)


def test_千葉の当日日没と翌日夜明けを返す(monkeypatch) -> None:
    expected_sunset = datetime(2026, 3, 27, 17, 56, 28, tzinfo=chiba_router._JST)
    expected_sunrise = datetime(2026, 3, 28, 5, 32, 43, tzinfo=chiba_router._JST)

    def fake_sun(observer, date, tzinfo):
        if date.day == 27:
            return {"sunset": expected_sunset}
        return {"sunrise": expected_sunrise}

    monkeypatch.setattr(chiba_router, "datetime", _FixedDateTime)
    monkeypatch.setattr(chiba_router, "sun", fake_sun)

    app = FastAPI()
    app.include_router(chiba_router.router)
    client = TestClient(app)

    response = client.get("/chiba/sun-times")

    assert response.status_code == 200
    assert response.json() == {
        "today_sunset": "2026-03-27T17:56:28+09:00",
        "tomorrow_sunrise": "2026-03-28T05:32:43+09:00",
    }


def test_sun関数は当日と翌日の2回呼ばれる(monkeypatch) -> None:
    called_dates: list[str] = []

    def fake_sun(observer, date, tzinfo):
        called_dates.append(date.isoformat())
        if len(called_dates) == 1:
            return {"sunset": datetime(2026, 3, 27, 18, 0, 0, tzinfo=chiba_router._JST)}
        return {"sunrise": datetime(2026, 3, 28, 5, 0, 0, tzinfo=chiba_router._JST)}

    monkeypatch.setattr(chiba_router, "datetime", _FixedDateTime)
    monkeypatch.setattr(chiba_router, "sun", fake_sun)

    app = FastAPI()
    app.include_router(chiba_router.router)
    client = TestClient(app)

    client.get("/chiba/sun-times")

    assert called_dates == ["2026-03-27", "2026-03-28"]
