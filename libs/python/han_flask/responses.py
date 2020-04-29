import json
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, Optional

from flask import Response

TYPES_TO_STRING = (Decimal,)


class JSONResponse(Response):
    def __init__(
        self,
        data: Any,
        *,
        status_code: int = 200,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.raw_data = self.coerce_type(data)
        super().__init__(
            json.dumps(self.raw_data),
            status=status_code,
            headers=headers,
            mimetype="application/json",
        )

    def coerce_type(self, value: Any) -> Any:
        if isinstance(value, (tuple, list, set)):
            return [self.coerce_type(val) for val in value]
        elif isinstance(value, dict):
            return {
                key: self.coerce_type(val)
                for key, val in value.items()
                if val is not None
            }
        elif is_dataclass(value):
            return self.coerce_type(asdict(value))
        elif isinstance(value, Enum):
            return value.name
        elif isinstance(value, (date, datetime)):
            return value.isoformat()
        elif isinstance(value, TYPES_TO_STRING):
            return str(value)
        else:
            return value
