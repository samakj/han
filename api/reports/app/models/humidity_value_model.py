from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class HumidityValue:
    humidity_value_id: Optional[int] = None
    report_id: Optional[int] = None
    value: Optional[Decimal] = None
