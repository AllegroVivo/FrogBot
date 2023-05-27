from __future__ import annotations

from typing     import List, Optional
################################################################################

__all__ = (
    "convert_db_list",
)

################################################################################
def convert_db_list(data: Optional[str]) -> List[str]:

    if data is None or not data or data == "{}":
        return []

    base_list = [i for i in data.lstrip("{").rstrip("}").split(",")]

    return [i.strip("'").strip('"') for i in base_list]

################################################################################
