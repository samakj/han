from decimal import Decimal
from typing import Any

from models.colour import Colour


def convert_metric_value(value_type: str, value: str) -> Any:
    if value_type == "integer":
        return int(value)
    if value_type == "float":
        return Decimal(value)
    if value_type == "boolean":
        return bool(value)
    if value_type == "colour":
        return Colour.from_hex(value)
    return value
