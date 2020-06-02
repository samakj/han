from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.device_model import Device
from models.metric_model import Metric


@dataclass
class Report:
    report_id: Optional[int] = None
    reported_at: Optional[datetime] = None
    device_id: Optional[str] = None
    device: Optional[Device] = None
    metric_id: Optional[int] = None
    metric: Optional[Metric] = None
    value: Optional[str] = None
