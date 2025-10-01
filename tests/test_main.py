import app
import pytest


@pytest.mark.parametrize(
    ["url", "expected_result", "expected_status_code"],
    [
        pytest.param("http://127.0.0.1:8000/status/200", True, 200),
        pytest.param("http://127.0.0.1:8000/status/404", False, 404),
        pytest.param("http://127.0.0.1:8000/status/500", False, 500),
    ],
)
def test_check_link(url: str, expected_result: bool, expected_status_code: int):
    res = app.check_link(url)

    assert type(res) is dict
    assert res["result"] == expected_result
    assert res["code"] == expected_status_code
    assert res["url"] == url


def test_extract_link():
    # ファイルからリンクを抽出するテスト。リンクの数、重複したリンクがない事をテストします。
    # TODO: 重複チェックはまだできていない。
    file_list = app.lookup_file("tests/doc/")
    links = app.extract_link(file_list[0])
    assert len(links) == 1

    links = app.extract_link(file_list[1])
    assert len(links) == 2


@pytest.mark.parametrize(["path"], [pytest.param("tests/doc/")])
def test_check(path: str):
    files = app.lookup_file(path)
    assert len(files) == 2


def test_main():
    res = app.main(["tests/doc/"])
