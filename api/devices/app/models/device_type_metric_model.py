from dataclasses import dataclass
from typing import Optional


@dataclass
class DeviceTypeMetric:
    device_type_metric_id: Optional[int] = None
    device_type_id: Optional[str] = None
    metric_id: Optional[int] = None
    reportable: Optional[bool] = None
    commandable: Optional[bool] = None
