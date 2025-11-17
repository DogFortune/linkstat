from linkstat import app
import os
from tempfile import TemporaryDirectory
from pathlib import Path


class TestValid:
    """正常系"""

    def test_main_with_minimal_arguments(self):
        """環境変数も引数も指定しない場合、コンソールモードで動作する事"""
        app.main(["tests/sample_doc/"])

    def test_main_with_output_json(self):
        """JSONファイルが出力されている事"""
        with TemporaryDirectory() as dir:
            output_path = Path(dir, "result.json")
            app.main(["tests/sample_doc/", "--report-json", str(output_path)])

            assert os.path.isfile(output_path) is True

    def test_main_single_file(self):
        app.main(["tests/sample_doc/doc1.md"])
