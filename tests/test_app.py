import app
import pytest
from unittest.mock import patch


class TestValid:
    """正常系"""

    def test_main_with_minimal_arguments(self):
        """環境変数も引数も指定しない場合、コンソールモードで動作する事"""
        app.main(["tests/sample_doc/"])

    @pytest.mark.parametrize(
        ["format"],
        [
            pytest.param("CONSOLE"),
            pytest.param("console"),
        ],
    )
    def test_main_with_valid_command_line_arguments(self, format: str):
        """フォーマット込みで行う一貫テスト。

        :param format: _description_
        :type format: str
        """
        app.main(["--format", format, "tests/sample_doc/"])


class TestInValid:
    @pytest.fixture
    def setup_environ(self):
        with patch.dict("os.environ", {"OUTPUT_FORMAT": "consol"}):
            yield

    """異常系"""

    @pytest.mark.parametrize(
        ["format"],
        [
            pytest.param("JSON"),
            pytest.param("json"),
            pytest.param("YAML"),
            pytest.param("yaml"),
        ],
    )
    def test_raise_NotImplemented_format_args(self, format: str):
        """未対応フォーマットを指定した場合、未実装を表す例外発生。
        :param format: _description_
        :type format: str
        """
        with pytest.raises(NotImplementedError):
            app.main(["--format", format, "tests/sample_doc/"])

    @pytest.mark.parametrize(
        ["format"],
        [pytest.param("consol"), pytest.param("sample")],
    )
    def test_raise_ValueError_format_args(self, format: str):
        """適切ではない値が来た場合、例外発生。
        :param format: _description_
        :type format: str
        """
        with pytest.raises(ValueError):
            app.main(["--format", format, "tests/sample_doc/"])

    @pytest.mark.usefixtures("setup_environ")
    def test_raise_format_args_use_environment(self):
        """環境変数でフォーマット指定をした時に適切ではない値が入っていた場合、例外発生。

        :param format: _description_
        :type format: str
        """
        with pytest.raises(ValueError):
            app.main(["tests/sample_doc/"])
