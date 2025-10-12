from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from enums import Result


def request(url: str):
    try:
        res = urlopen(url, timeout=5)
        return {"result": Result.OK, "code": res.code, "url": res.url}
    except HTTPError as e:
        # アクセスできて400や500系が来た時はこっち
        return {"result": Result.NG, "code": e.code, "url": url, "reason": e.reason}
    except URLError as e:
        # そもそもアクセスすらできなかった場合はこっち
        return {"result": Result.NG, "code": None, "url": url, "reason": e.reason}


def check_links(links: dict) -> list:
    # リンクをチェックします。
    # チェックすべきなのはFalseのものだけ。
    results = []
    for file_path, link_items in links.items():
        for item in link_items:
            if not item["duplicate"]:
                res = request(item["url"])
                data = {
                    "file": file_path,
                    "line": item["line"],
                    "url": item["url"],
                    "result": res["result"],
                    "code": res["code"],
                }
                if "reason" in res:
                    data["reason"] = res["reason"]
                results.append(data)
    return results


def search(path: str, filter="*.md"):
    # 指定したディレクトリから検査対象のファイルを抽出します。デフォルトはmdです。
    p = Path(path)
    files = [str(item) for item in p.rglob(filter)]
    return files


def extract_link(files: list) -> dict:
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
                    links[f"{file_path}"].append(
                        {"line": i + 1, "url": url, "duplicate": duplicate}
                    )
    return links
