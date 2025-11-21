import os
import pytest
from linkstat import analyzer
from linkstat.reporter import ReportData


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
    res = analyzer.request(url)

    assert type(res) is analyzer.AnalyzeResponse
    assert res.result == expected_result
    assert res.code == expected_status_code
    assert res.url == url
    if res.result.upper() == "NG":
        assert res.reason is not None


@pytest.mark.parametrize(
    ["path", "report_data_count"],
    [
        # ディレクトリ指定パターン
        pytest.param("tests/sample_doc/", 3),
        # 単体ファイル指定パターン
        pytest.param("tests/sample_doc/doc1.md", 1),
        pytest.param("tests/sample_doc/doc2.md", 3),
    ],
)
def test_check_links(path: str, report_data_count: int):
    files = analyzer.search(path)
    links = analyzer.extract_url(files)
    results_report_data = analyzer.check_links(links)

    # 重複しているリンクは結果に含まれていない事（ドキュメントに記載されているリンクの数 - 重複しているリンクの数になっている事）
    assert len(results_report_data) == report_data_count

    # 形式チェック
    for item in results_report_data:
        assert type(item) is ReportData
        assert item.file is not None
        assert item.line is not None
        assert item.url is not None
        assert item.result is not None

        if item.result.upper() == "OK":
            assert item.code is not None
            assert item.reason is None
        else:
            assert item.code is None
            assert item.reason is not None


@pytest.mark.parametrize(["path"], [pytest.param("tests/sample_doc/")])
def test_search(path: str):
    files = analyzer.search(path)
    assert len(files) == 2


def test_search_single_file():
    """単一のファイルを指定した場合、指定したファイルのパスだけが入っているリストが返ってくる事"""
    files = analyzer.search("tests/sample_doc/doc1.md")

    assert len(files) == 1
    assert os.path.basename(files[0]) == "doc1.md"


def test_extract_link():
    # ファイルからリンクを抽出するテスト。対象のドキュメントすべてのリンクを抽出する。
    # データ構造としてはdictのKeyにファイルのパス、Valueにリンクに関する情報が入っている。
    # これは1ファイルの中に大量のリンクがあった時、すべてがフラットなリストだとファイル名を1つ1つ持つ事になるのでデータ量が増えてしまう。ファイル名は値として重複しやすいので、Keyという形で1つにまとめたのが理由。
    # 重複リンクにはフラグをつける。2つ目以降はFalseになるのでTrueのものだけリンクチェックすればOK
    files = analyzer.search("tests/sample_doc/")

    links = analyzer.extract_url(files)

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
    duplicated_link_list = [item for item in doc2_result if item.duplicate]
    assert len(duplicated_link_list) == 2
    assert duplicated_link_list[0].url == duplicated_link_list[1].url
    assert duplicated_link_list[0].url == "https://example.com"
