import main
import pytest


def test_main():
    main.main(["tests/doc/"])


@pytest.mark.parametrize(
    ["format"],
    [
        pytest.param("CONSOLE"),
        pytest.param("console"),
        pytest.param("JSON"),
        pytest.param("json"),
    ],
)
def test_format_args(format: str):
    """フォーマットテスト

    :param format: _description_
    :type format: str
    """
    main.main(["--format", format, "tests/doc/"])
