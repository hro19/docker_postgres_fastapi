from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from astral import LocationInfo
from astral.sun import sun
from fastapi import APIRouter

from app.schemas.chiba import ChibaSunTimes

# 千葉市付近の代表座標（緯度・経度は必要に応じて調整してください）
_LOCATION = LocationInfo("Chiba", "Japan", "Asia/Tokyo", 35.6074, 140.1065)
_JST = ZoneInfo("Asia/Tokyo")

router = APIRouter(prefix="/chiba", tags=["chiba"])


@router.get("/sun-times", response_model=ChibaSunTimes)
def chiba_sun_times() -> ChibaSunTimes:
    today_jst = datetime.now(_JST).date()
    tomorrow_jst = today_jst + timedelta(days=1)

    today_sun = sun(_LOCATION.observer, date=today_jst, tzinfo=_JST)
    tomorrow_sun = sun(_LOCATION.observer, date=tomorrow_jst, tzinfo=_JST)

    return ChibaSunTimes(
        today_sunset=today_sun["sunset"],
        tomorrow_sunrise=tomorrow_sun["sunrise"],
    )
