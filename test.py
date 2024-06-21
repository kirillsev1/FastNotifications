import json
from datetime import datetime, timedelta, timezone

import pytz

local = pytz.timezone("America/Los_Angeles")
naive = datetime.now()
local_dt = local.localize(naive, is_dst=None)
utc_dt = local_dt.astimezone(pytz.utc)

from datetime import datetime

import pytz


def convert_timezone(input_datetime, target_timezone):
    # Проверяем, является ли объект datetime
    if not isinstance(input_datetime, datetime):
        raise ValueError("Input should be a datetime object")

    converted_time = input_datetime.astimezone(target_timezone)
    return converted_time


if __name__ == "__main__":
    input_datetime = datetime.now()
    print(json.dumps([input_datetime.isoformat()]))
    print(datetime.fromisoformat(input_datetime.isoformat()))
    target_timezone = pytz.timezone('Europe/Moscow')

    converted_time = convert_timezone(input_datetime, target_timezone)

    print("Исходное время:", input_datetime)
    print(target_timezone.zone)
    print(converted_time)
