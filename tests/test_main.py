import main
import pytest
import os


class TestValid:
    """正常系"""

    def test_main(self):
        """環境変数も引数も指定しない場合、コンソールモードで動作する事"""
        main.main(["tests/doc/"])

    @pytest.mark.parametrize(
        ["format"],
        [
            pytest.param("CONSOLE"),
            pytest.param("console"),
        ],
    )
    def test_format_args(self, format: str):
        """フォーマット込みで行って最後まで完了する事。

        :param format: _description_
        :type format: str
        """
        main.main(["--format", format, "tests/doc/"])


class TestInValid:
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
            main.main(["--format", format, "tests/doc/"])

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
            main.main(["--format", format, "tests/doc/"])

    def test_raise_format_args_use_environment(self):
        """環境変数でフォーマット指定をした時に適切ではない値が入っていた場合、例外発生。

        :param format: _description_
        :type format: str
        """
        os.environ["OUTPUT_FORMAT"] = "consol"
        with pytest.raises(ValueError):
            main.main(["tests/doc/"])
