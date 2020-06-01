from dataclasses import dataclass
from typing import Optional


@dataclass
class Superuser:
    superuser_id: Optional[int] = None
    user_id: Optional[int] = None
