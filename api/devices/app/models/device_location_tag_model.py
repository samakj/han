from dataclasses import dataclass
from typing import Optional


@dataclass
class DeviceLocationTag:
    device_location_tag_id: Optional[int] = None
    device_id: Optional[str] = None
    location_tag_id: Optional[int] = None
