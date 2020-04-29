from typing import Set

from werkzeug.routing import BaseConverter


class IntSetConverter(BaseConverter):
    regex = r"\d+(?:,\d+)*,?"

    def to_python(self, value) -> Set[int]:
        return {int(x) for x in value.split(",")}

    def to_url(self, value) -> str:
        return ",".join(str(x) for x in value)
