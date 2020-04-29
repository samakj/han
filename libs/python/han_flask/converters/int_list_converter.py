from typing import List

from werkzeug.routing import BaseConverter


class IntListConverter(BaseConverter):
    regex = r"\d+(?:,\d+)*,?"

    def to_python(self, value) -> List[int]:
        return [int(x) for x in value.split(",")]

    def to_url(self, value) -> str:
        return ",".join(str(x) for x in value)
