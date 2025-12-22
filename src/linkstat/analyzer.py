from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from linkstat.enums import Result
from linkstat.reporter import ReportData
from dataclasses import dataclass
import re

URL_PATTERN = r'https?://[^\s\)\]>"]+'
URL_RE = re.compile(URL_PATTERN)


@dataclass
class AnalyzeResponse:
    """リンクにアクセスした結果"""

    result: Result
    code: str | None
    url: str
    reason: str | None


@dataclass
class URLInfo:
    """ドキュメントから抽出したURL情報"""

    line: int
    url: str
    duplicate: bool


def request(url: str) -> AnalyzeResponse:
    """疎通確認処理

    :param url: 確認対象URL
    :type url: str
    :return: 結果
    :rtype: AnalyzeResponse
    """
    try:
        with urlopen(url, timeout=3) as res:
            return AnalyzeResponse(Result.OK, res.code, res.url, None)
    except HTTPError as e:
        # アクセスできて400や500系が来た時はこっち
        return AnalyzeResponse(Result.NG, e.code, url, e.reason)
    except URLError as e:
        # そもそもアクセスすらできなかった場合はこっち
        return AnalyzeResponse(Result.NG, None, url, e.reason)
    except TimeoutError:
        return AnalyzeResponse(Result.NG, None, url, "Timeout")


def check_links(links: dict[str, URLInfo]) -> list[ReportData]:
    """URLの疎通確認を行います。確認を行うのは重複していないものだけ。

    :param links: URLリスト
    :type links: dict[str, URLInfo]
    :return: 確認結果（重複したURLは除く）
    :rtype: list[ReportData]
    """
    results = []
    for file_path, link_items in links.items():
        for item in link_items:
            if not item.duplicate:
                res = request(item.url)
                data = ReportData(
                    file_path,
                    item.line,
                    item.url,
                    res.result,
                    res.code,
                    res.reason,
                )
                print(f"{data.url}: {data.result}")
                results.append(data)
    return results


def search(path: str, filter="*.md") -> list:
    """指定したディレクトリからMarkdownドキュメントを抽出します。

    :param path: 検索対象
    :type path: str
    :param filter: _description_, defaults to "*.md"
    :type filter: str, optional
    :return: ファイルパスのリスト
    :rtype: list
    """
    p = Path(path)
    if p.is_file():
        return [str(p)]
    files = [str(item) for item in p.rglob(filter)]
    return files


def extract_url(files: list) -> dict[str, URLInfo]:
    """ファイルからURLを抽出します。重複しているリンクも含まれます。

    :param files: _description_
    :type files: list
    :return: _description_
    :rtype: dict[str, LinkInfo]
    """
    links = {}
    duplicated_urls = set()
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            links[f"{file_path}"] = []
            for i, line in enumerate(lines):
                result = URL_RE.search(line)
                if result:
                    url = result.group()
                    if url in duplicated_urls:
                        duplicate = True
                    else:
                        duplicate = False
                        duplicated_urls.add(url)
                    data = URLInfo(i + 1, url, duplicate)
                    links[f"{file_path}"].append(data)
    return links
