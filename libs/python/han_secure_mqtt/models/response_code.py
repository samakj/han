from dataclasses import dataclass
from typing import Optional


@dataclass
class ResponseCode:
    code: int
    message: str
    description: Optional[str] = None
