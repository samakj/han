from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from models.location_tag_model import LocationTag
from models.device_type_model import DeviceType


@dataclass
class Device:
    device_id: Optional[str] = None
    device_type_id: Optional[int] = None
    latest_ping: Optional[datetime] = None
    location_tags: Optional[List[LocationTag]] = None
    device_type: Optional[DeviceType] = None
