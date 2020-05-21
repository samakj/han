from dataclasses import dataclass
from typing import Optional


@dataclass
class AccessControl:
    access_control_id: Optional[int] = None
    user_id: Optional[int] = None
    topic: Optional[str] = None
    action: Optional[int] = None
    action_verbose: Optional[str] = None
