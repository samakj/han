from typing import Any, Dict

from flask import Request


class JSONRequest(Request):  # pylint: disable=too-many-ancestors
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def get_json(  # type: ignore # pylint: disable=arguments-differ
        self, converted: bool = True, **kwargs: Any  # pylint: disable=unused-argument
    ) -> Dict[str, Any]:
        return super().get_json(**kwargs)
