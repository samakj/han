from typing import Optional


def arg_to_bool(arg: Optional[str], default=None) -> Optional[bool]:
    value = default
    if arg is None:
        pass
    elif arg.lower() in {"yes", "y", "true", "t", "1"}:
        value = True
    elif arg.lower() in {"no", "n", "false", "f", "0"}:
        value = False

    return value
