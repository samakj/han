from dataclasses import dataclass
from typing import Optional


@dataclass
class ReportMetric:
    report_metric_id: Optional[int] = None
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    unit: Optional[str] = None
    report_value_type: Optional[str] = None
