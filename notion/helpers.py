from typing import Any, Dict

from notion.types import BLOCK_MAPPING, Block


def pick(base: Dict[str, Any], *keys: str) -> Dict[str, Any]:
    """
    Helper to select keys from an arbitrary dictionnary of keyword
    arguments when key is defined and not null.
    """

    return {key: base[key] for key in keys if key in base and base[key] is not None}


def parse_block_obj(response: Dict) -> Block:
    block_type = response.get("type", None)
    if block_type is None or block_type not in BLOCK_MAPPING:
        raise ValueError("Block type not supported. Please, check notion-sdk updates.")
    return BLOCK_MAPPING[block_type].parse_obj(response)
