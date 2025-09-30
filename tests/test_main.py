import app
import pytest
from pprint import pprint as pp


def test_extract_link():
    file_list = app.lookup_file("tests/doc/")
    links = app.extract_link(file_list[0])
    assert len(links) == 1

    links = app.extract_link(file_list[1])
    assert len(links) == 2


@pytest.mark.parametrize(
    ["path"], [pytest.param(".\\tests\\doc\\"), pytest.param("tests/doc/")]
)
def test_check(path: str):
    files = app.lookup_file(path)

    pp(files)

    assert len(files) == 2


def test_main():
    res = app.main(["tests/doc/"])
