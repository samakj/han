from dataclasses import dataclass
from typing import Optional


@dataclass
class Metric:
    metric_id: Optional[int] = None
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    value_type: Optional[str] = None
    unit: Optional[str] = None
