import pytest
from linkstat import reporter
from linkstat import analyzer
from tempfile import TemporaryDirectory
from pathlib import Path
import os


@pytest.fixture(scope="function")
def setup_report_data():
    """レポート確認用データ作成

    :yield: _description_
    :rtype: _type_
    """
    files = analyzer.search("tests/sample_doc/")
    links = analyzer.extract_url(files)
    results_report_data = analyzer.check_links(links)
    return results_report_data


class TestValid:
    """正常系"""

    def test_console(self, setup_report_data):
        """コンソール出力テスト。文字列が想定している形である事"""
        output_line = reporter.console(setup_report_data)

        assert output_line is not None

    def test_json(self, setup_report_data):
        with TemporaryDirectory() as dir:
            output_path = Path(dir, "result.json")

            reporter.dump_json(setup_report_data, output_path)

            assert os.path.isfile(output_path) is True


class TestInvalid:
    """異常系"""

    def test_raises_exception_for_non_json_extension(self, setup_report_data):
        """拡張子がjson以外だった場合、例外発生"""
        with TemporaryDirectory() as dir:
            output_path = Path(dir, "result.jso")

            with pytest.raises(ValueError):
                reporter.dump_json(setup_report_data, output_path)
