from dataclasses import dataclass
from typing import Optional


@dataclass
class HanMqttUserData:
    client_id: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
