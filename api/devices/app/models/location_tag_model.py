from dataclasses import dataclass
from typing import Optional


@dataclass
class LocationTag:
    location_tag_id: Optional[int] = None
    name: Optional[str] = None
    level: Optional[int] = None
