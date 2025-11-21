from linkstat import app
import os
import pytest
from tempfile import TemporaryDirectory
from pathlib import Path


class TestValid:
    """正常系"""

    def test_main_with_minimal_arguments(self):
        """環境変数も引数も指定しない一気通貫のテスト"""
        app.main(["tests/sample_doc/"])

    def test_main_with_output_json(self):
        """JSONファイルが出力されている事"""
        with TemporaryDirectory() as dir:
            output_path = Path(dir, "result.json")
            app.main(["tests/sample_doc/", "--report-json", str(output_path)])

            assert os.path.isfile(output_path) is True

    def test_main_report_path_directory(self):
        """出力パスとしてファイルではなくディレクトリで指定されていた場合、エラーが発生する事
        ERROR: --report-path must be a filename, given: tmp/
        """
        with TemporaryDirectory() as dir:
            with pytest.raises(
                ValueError, match="ERROR: --report-path must be a filename"
            ):
                app.main(["tests/sample_doc/", "--report-json", str(dir)])

    def test_main_single_file(self):
        """単体のファイルを指定した場合も正しく動作する事"""
        app.main(["tests/sample_doc/doc1.md"])
