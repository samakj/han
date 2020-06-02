from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, Union

from models.metric_model import ReportMetric


@dataclass
class Report:
    report_id: Optional[int] = None
    report_metric_id: Optional[int] = None
    report_metric: Optional[ReportMetric] = None
    reported_at: Optional[datetime] = None
    device_id: Optional[str] = None
    value: Optional[Union[bool, Decimal]] = None
