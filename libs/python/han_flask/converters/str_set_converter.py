from typing import Set

from werkzeug.routing import BaseConverter


class StrSetConverter(BaseConverter):
    regex = r"\d+(?:,\d+)*,?"

    def to_python(self, value) -> Set[str]:
        return set(value.split(","))

    def to_url(self, value) -> str:
        return ",".join(value)
