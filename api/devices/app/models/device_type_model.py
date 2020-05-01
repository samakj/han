from dataclasses import dataclass
from typing import List, Optional

from models.report_metric_model import ReportMetric


@dataclass
class DeviceType:
    device_type_id: Optional[int] = None
    name: Optional[str] = None
    report_metrics: Optional[List[ReportMetric]] = None
