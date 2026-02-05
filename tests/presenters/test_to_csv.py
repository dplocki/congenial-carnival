import io
from presenters.to_csv import ToCsvPresenter
from tests.utils.data_providers import generate_int, generate_str


def build_presenter(data):
    presenter = ToCsvPresenter()
    output = io.StringIO()
    presenter.present(data, output)
    return output.getvalue()


def test_presenter_should_generate_csv_headers():
    data = [{"id": generate_int(), "name": generate_str(), "category": generate_str()}]

    result = build_presenter(data)

    assert result.splitlines()[0] == "id,name,category"


def test_presenter_should_generate_csv_rows():
    data = [
        {"id": 1, "name": "Game A", "category": "Action"},
        {"id": 2, "name": "Game B", "category": "Adventure"},
    ]

    result = build_presenter(data)

    assert result.splitlines() == ["id,name,category", "1,Game A,Action", "2,Game B,Adventure"]
