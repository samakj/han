from dataclasses import dataclass
from typing import Optional


@dataclass
class DeviceTypeReportMetric:
    device_type_report_metric_id: Optional[int] = None
    device_type_id: Optional[str] = None
    report_metric_id: Optional[int] = None
