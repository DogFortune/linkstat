import main
import pytest


def test_main():
    main.main(["tests/doc/"])


@pytest.mark.parametrize(
    ["format"],
    [
        pytest.param("CONSOLE"),
        pytest.param("console"),
    ],
)
def test_format_args(format: str):
    """正常系：フォーマット込みで行って最後まで完了する事。

    :param format: _description_
    :type format: str
    """
    main.main(["--format", format, "tests/doc/"])


@pytest.mark.parametrize(
    ["format"],
    [
        pytest.param("JSON"),
        pytest.param("json"),
        pytest.param("YAML"),
        pytest.param("yaml"),
    ],
)
def test_raise_NotImplemented_format_args(format: str):
    """異常系：未対応フォーマットを指定した場合、未実装を表す例外発生。
    :param format: _description_
    :type format: str
    """
    with pytest.raises(NotImplementedError):
        main.main(["--format", format, "tests/doc/"])


@pytest.mark.parametrize(
    ["format"],
    [pytest.param("consol"), pytest.param("sample")],
)
def test_raise_ValueError_format_args(format: str):
    """異常系：適切ではない値が来た場合、例外発生。
    :param format: _description_
    :type format: str
    """
    with pytest.raises(ValueError):
        main.main(["--format", format, "tests/doc/"])
