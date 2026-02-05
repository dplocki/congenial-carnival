import io
from typing import Dict, Generator, List, Union
from presenters.to_csv import ToCsvPresenter
from tests.utils.data_providers import generate_int, generate_str


def build_presenter(data: Generator[Dict, None, None]) -> str:
    presenter = ToCsvPresenter()
    output = io.StringIO()
    presenter.present(data, output)
    return output.getvalue()


def build_input_data(
    headers: List[str], rows: List[List[Union[int, str]]]
) -> Generator[Dict, None, None]:
    for row in rows:
        yield {header: value for header, value in zip(headers, row)}


def test_presenter_should_generate_csv_headers():
    headers = [generate_str() for _ in range(3)]
    data = build_input_data(headers, [[generate_int(), generate_str(), generate_str()]])

    result = build_presenter(data)

    assert result.splitlines()[0].split(",") == headers


def test_presenter_should_generate_csv_rows():
    headers = [generate_str() for _ in range(3)]
    rows = [(generate_int(), generate_str(), generate_str()) for _ in range(5)]

    data = build_input_data(headers, rows)
    result = build_presenter(data)

    for line, row in zip(result.splitlines()[1:], rows):
        assert line.split(",") == list(map(str, row))
