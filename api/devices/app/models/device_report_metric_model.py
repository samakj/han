from dataclasses import dataclass
from typing import Optional


@dataclass
class DeviceReportMetric:
    device_report_metric_id: Optional[int] = None
    device_id: Optional[str] = None
    report_metric_id: Optional[int] = None
