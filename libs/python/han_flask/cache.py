from typing import Any, Dict, Optional

from flask_caching import Cache

from . import HanFlask


class HanCache(Cache):
    def __init__(
        self, app: Optional[HanFlask] = None, config: Optional[Dict[str, Any]] = None
    ):
        super(HanCache, self).__init__(app, config=config)

    def get(
        self, key: str, key_formatting_kwargs: Optional[Dict[str, Any]] = None
    ) -> Optional[Any]:
        formatted_key = (
            key.format(**key_formatting_kwargs)
            if key_formatting_kwargs is not None
            else key
        )
        value = super(HanCache, self).get(key=formatted_key)
        return value

    def set(
        self,
        key: str,
        value: Any,
        timeout: int,
        key_formatting_kwargs: Optional[Dict[str, Any]] = None,
    ) -> None:
        formatted_key = (
            key.format(**key_formatting_kwargs)
            if key_formatting_kwargs is not None
            else key
        )
        super(HanCache, self).set(key=formatted_key, value=value, timeout=timeout)
