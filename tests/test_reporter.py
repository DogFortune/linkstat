import reporter
import analyzer
from pprint import pprint as pp


class TestValid:
    """正常系"""

    def test_console(self):
        """コンソール出力テスト。文字列が想定している形である事"""
        files = analyzer.search("tests/doc/")

        links = analyzer.extract_link(files)
        results_report_data = analyzer.check_links(links)
        report = reporter.Console(results_report_data)
        output_line = report.generate()
        assert output_line is not None
