import app
import pytest


@pytest.mark.skip()
def test_awesome():
    """awesomeを使ったほぼ実環境に近いパターン"""
    app.main(["submodules/awesome/"])
