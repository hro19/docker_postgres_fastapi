from datetime import datetime

from pydantic import BaseModel


class ChibaSunTimes(BaseModel):
    today_sunset: datetime
    tomorrow_sunrise: datetime
