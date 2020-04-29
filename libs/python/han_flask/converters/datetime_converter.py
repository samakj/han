from datetime import datetime

import iso8601
from werkzeug.routing import BaseConverter


class DatetimeConverter(BaseConverter):
    regex = r"\d+(?:,\d+)*,?"

    def to_python(self, value) -> datetime:
        return iso8601.parse_date(value, default_timezone=None)

    def to_url(self, value) -> str:
        return value.isoformat()
