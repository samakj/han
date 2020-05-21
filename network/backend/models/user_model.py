from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    user_id: Optional[int] = None
    username: Optional[str] = None
    mac_address: Optional[str] = None
