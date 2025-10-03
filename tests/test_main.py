import app
import pytest
from pprint import pprint as pp


class TestCheckLins:
    def test_check_links(self):
        files = app.lookup_file("tests/doc/")
        links = app.extract_link(files)
        result = app.check_links(links)

        pp(result)


class TestExtractLink:
    def test_extract_link(self):
        # ファイルからリンクを抽出するテスト。対象のドキュメントすべてのリンクを抽出する。
        # データ構造としてはdictのKeyにファイルのパス、Valueにリンクに関する情報が入っている。
        # これは1ファイルの中に大量のリンクがあった時、すべてがフラットなリストだとファイル名を1つ1つ持つ事になるのでデータ量が増えてしまう。ファイル名は値として重複しやすいので、Keyという形で1つにまとめたのが理由。
        # 重複リンクにはフラグをつける。2つ目以降はFalseになるのでTrueのものだけリンクチェックすればOK
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

        # ちゃんと重複判定の数が正しいか、重複と見なしたリンクは想定しているものか
        duplicated_link_list = [item for item in doc2_result if item["duplicate"]]
        assert len(duplicated_link_list) == 2
        assert duplicated_link_list[0]["url"] == duplicated_link_list[1]["url"]
        assert duplicated_link_list[0]["url"] == "https://example.com"


@pytest.mark.parametrize(
    ["url", "expected_result", "expected_status_code"],
    [
        pytest.param("http://127.0.0.1:8000/status/200", "OK", 200),
        pytest.param("http://127.0.0.1:8000/status/404", "NG", 404),
        pytest.param("http://127.0.0.1:8000/status/500", "NG", 500),
        pytest.param("http://127.0.0.1:800", "NG", None),
    ],
)
def test_request(url: str, expected_result: str, expected_status_code: int):
    # アクセスチェックした時に想定しているリクエストが返ってくる事。
    # 200系だけTrueで、それ以外はFalseで返ってくる事。
    # URLErrorが発生した（レスポンスが無く、そもそも接続できなかった）場合はFalseでステータスコードがNoneとなる事。
    res = app.request(url)

    pp(res)

    assert type(res) is dict
    assert res["result"] == expected_result
    assert res["code"] == expected_status_code
    assert res["url"] == url
    if not res["result"]:
        assert "reason" in res


@pytest.mark.parametrize(["path"], [pytest.param("tests/doc/")])
def test_check(path: str):
    files = app.lookup_file(path)
    assert len(files) == 2


def test_main():
    app.main(["tests/doc/"])
