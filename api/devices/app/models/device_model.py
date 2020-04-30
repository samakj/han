from dataclasses import dataclass
from typing import List, Optional

from models.location_tag_model import LocationTag
from models.report_metric_model import ReportMetric


@dataclass
class Device:
    device_id: Optional[int] = None
    location_tags: Optional[List[LocationTag]] = None
    report_metrics: Optional[List[ReportMetric]] = None
