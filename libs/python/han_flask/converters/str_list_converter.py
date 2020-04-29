from typing import List

from werkzeug.routing import BaseConverter


class StrListConverter(BaseConverter):
    regex = r"\d+(?:,\d+)*,?"

    def to_python(self, value) -> List[str]:
        return value.split(",")

    def to_url(self, value) -> str:
        return ",".join(value)
