from itertools import zip_longest
from typing import Any, Iterable


def are_collections_equal(
    collection1: Iterable[Any], collection2: Iterable[Any]
) -> bool:
    for item1, item2 in zip_longest(collection1, collection2):
        if item1 != item2:
            return False

    return True
