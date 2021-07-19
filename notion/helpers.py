from typing import Any, Dict


def pick(base: Dict[str, Any], *keys: str) -> Dict[str, Any]:
    """
    Helper to select keys from an arbitrary dictionnary of keyword
    arguments when key is defined and not null.
    """

    return {key: base[key] for key in keys if key in base and base[key] is not None}
