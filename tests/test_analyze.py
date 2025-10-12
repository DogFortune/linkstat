import pytest
import analyze


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
    res = analyze.request(url)

    assert type(res) is dict
    assert res["result"] == expected_result
    assert res["code"] == expected_status_code
    assert res["url"] == url
    if not res["result"]:
        assert "reason" in res


def test_check_links():
    files = analyze.search("tests/doc/")
    links = analyze.extract_link(files)
    result = analyze.check_links(links)

    # 重複しているリンクは結果に含まれていない事（ドキュメントに記載されているリンクの数 - 重複しているリンクの数になっている事）
    assert len(result) == 3

    # 形式チェック
    for item in result:
        assert "file" in item and item["file"] is not None
        assert "line" in item and item["line"] is not None
        assert "url" in item and item["url"] is not None
        assert "result" in item and item["result"] is not None
        assert "code" in item

        if item["result"].upper() == "OK":
            assert item["code"] is not None
        else:
            assert item["code"] is None
            assert "reason" in item and item["reason"] is not None


@pytest.mark.parametrize(["path"], [pytest.param("tests/doc/")])
def test_search(path: str):
    files = analyze.search(path)
    assert len(files) == 2


def test_extract_link():
    # ファイルからリンクを抽出するテスト。対象のドキュメントすべてのリンクを抽出する。
    # データ構造としてはdictのKeyにファイルのパス、Valueにリンクに関する情報が入っている。
    # これは1ファイルの中に大量のリンクがあった時、すべてがフラットなリストだとファイル名を1つ1つ持つ事になるのでデータ量が増えてしまう。ファイル名は値として重複しやすいので、Keyという形で1つにまとめたのが理由。
    # 重複リンクにはフラグをつける。2つ目以降はFalseになるのでTrueのものだけリンクチェックすればOK
    files = analyze.search("tests/doc/")
    links = analyze.extract_link(files)

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
