import csv
from typing import Iterable, Any, TextIO


class ToCsvPresenter:

    def present(self, data: Iterable[Any], output: TextIO) -> None:
        iter_data = iter(data)
        first_element = next(iter_data, None)
        if first_element is None:
            raise ValueError("No data to present")

        writer = csv.DictWriter(output, fieldnames=first_element.keys())
        writer.writeheader()
        writer.writerow(first_element)
        writer.writerows(iter_data)
