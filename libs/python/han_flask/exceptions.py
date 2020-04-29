from http import HTTPStatus
from typing import Any, Optional


class APIError(Exception):
    def __init__(
        self,
        status_code: int,
        error_type: Optional[str] = None,
        data: Optional[Any] = None,
    ) -> None:
        super().__init__()
        http_status = HTTPStatus(value=status_code)
        self.status_code = status_code
        self.error_type = error_type or http_status.name
        self.data = {
            "description": http_status.description,
            "error_type": self.error_type,
            "status_code": self.status_code,
            **(data or {}),
        }

    def __eq__(self, obj: object) -> bool:
        return (
            isinstance(obj, APIError)
            and obj.status_code == self.status_code
            and obj.error_type == self.error_type
        )

    def __hash__(self) -> int:
        return hash((self.status_code, self.error_type))
