from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from enums import Result
from report import ReportData
import dataclasses


@dataclasses.dataclass
class AnalyzeResponse:
    """リンクにアクセスした結果"""

    result: Result
    code: str | None
    url: str
    reason: str | None


@dataclasses.dataclass
class LinkInfo:
    """ドキュメントから抽出したリンク情報"""

    line: int
    url: str
    duplicate: bool


def request(url: str) -> AnalyzeResponse:
    try:
        res = urlopen(url, timeout=5)
        return AnalyzeResponse(Result.OK, res.code, res.url, None)
    except HTTPError as e:
        # アクセスできて400や500系が来た時はこっち
        return AnalyzeResponse(Result.NG, e.code, url, e.reason)
    except URLError as e:
        # そもそもアクセスすらできなかった場合はこっち
        return AnalyzeResponse(Result.NG, None, url, e.reason)


def check_links(links: dict[str, LinkInfo]) -> list[ReportData]:
    # リンクをチェックします。
    # チェックすべきなのはFalseのものだけ。
    results = []
    for file_path, link_items in links.items():
        for item in link_items:
            if not item.duplicate:
                res = request(item.url)
                data = ReportData(
                    file_path, item.line, item.url, res.result, res.code, res.reason
                )
                results.append(data)
    return results


def search(path: str, filter="*.md"):
    # 指定したディレクトリから検査対象のファイルを抽出します。デフォルトはmdです。
    p = Path(path)
    files = [str(item) for item in p.rglob(filter)]
    return files


def extract_link(files: list) -> dict[str, LinkInfo]:
    # 各ファイルからリンクを抽出します。
    # 重複しているリンクはフラグがTrueになります。
    links = {}
    seen_urls = set()
    for file_path in files:
        with open(file_path, "r") as f:
            lines = f.read().splitlines()
            links[f"{file_path}"] = []
            for i, line in enumerate(lines):
                if "http" in line:
                    url = line.split("](")[1].rstrip(")")
                    if url in seen_urls:
                        duplicate = True
                    else:
                        duplicate = False
                        seen_urls.add(url)
                    data = LinkInfo(i + 1, url, duplicate)
                    links[f"{file_path}"].append(data)
    return links
