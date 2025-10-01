import app
import pytest
from pprint import pprint as pp


class TestExtractLink:
    def test_extract_link(self):
        # ファイルからリンクを抽出するテスト。対象のドキュメントすべてのリンクを抽出する。
        # 重複リンクにはフラグをつける。2つ目移行はFalseになるのでTrueのものだけリンクチェックすればOK
        files = app.lookup_file("tests/doc/")
        links = app.extract_link(files)

        assert len(links) == 2

        doc1_result = [
            item for key, value in links.items() if "doc1.md" in key for item in value
        ]
        doc2_result = [
            item for key, value in links.items() if "doc2.md" in key for item in value
        ]

        assert len(doc1_result) == 1
        assert len(doc2_result) == 4


@pytest.mark.parametrize(
    ["url", "expected_result", "expected_status_code"],
    [
        pytest.param("http://127.0.0.1:8000/status/200", True, 200),
        pytest.param("http://127.0.0.1:8000/status/404", False, 404),
        pytest.param("http://127.0.0.1:8000/status/500", False, 500),
        pytest.param("http://127.0.0.1:800", False, None),
    ],
)
def test_check_link(url: str, expected_result: bool, expected_status_code: int):
    res = app.check_link(url)

    assert type(res) is dict
    assert res["result"] == expected_result
    assert res["code"] == expected_status_code
    assert res["url"] == url


@pytest.mark.parametrize(["path"], [pytest.param("tests/doc/")])
def test_check(path: str):
    files = app.lookup_file(path)
    assert len(files) == 2


def test_main():
    res = app.main(["tests/doc/"])
