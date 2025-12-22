import pytest
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


@pytest.fixture()
def use_mock_server():
    """テスト実行前にモックサーバーの起動を確認"""
    mock_server_url = "http://localhost:8000/get"

    try:
        req = Request(mock_server_url)
        with urlopen(req) as res:
            if res.getcode() == 200:
                return
    except (HTTPError, URLError):
        pass

    pytest.exit(
        "\n\n❌ エラー: モックサーバーが起動していません\n"
        "以下のコマンドでモックサーバーを起動してください:\n"
        "  docker-compose up -d\n",
        returncode=1,
    )
