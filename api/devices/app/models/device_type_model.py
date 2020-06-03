from dataclasses import dataclass
from typing import List, Optional

from models.metric_model import Metric


@dataclass
class DeviceType:
    device_type_id: Optional[int] = None
    name: Optional[str] = None
    report_period: Optional[int] = None
    metrics: Optional[List[Metric]] = None
