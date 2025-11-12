import reporter
import analyzer
from pprint import pprint as pp
from tempfile import TemporaryDirectory
from pathlib import Path
import os


class TestValid:
    """正常系"""

    def test_console(self):
        """コンソール出力テスト。文字列が想定している形である事"""
        files = analyzer.search("tests/sample_doc/")
        links = analyzer.extract_link(files)
        results_report_data = analyzer.check_links(links)

        output_line = reporter.console(results_report_data)

        assert output_line is not None

    def test_json(self):
        files = analyzer.search("tests/sample_doc/")
        links = analyzer.extract_link(files)
        results_report_data = analyzer.check_links(links)
        with TemporaryDirectory() as dir:
            output_path = Path(dir, "result.json")

            reporter.dump_json(results_report_data, output_path)

            assert os.path.isfile(output_path) is True
