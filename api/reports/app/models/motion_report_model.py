from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from models.report_model import Report


@dataclass
class MotionReport(Report):
    value: Optional[Decimal] = None
