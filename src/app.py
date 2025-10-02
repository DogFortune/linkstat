import argparse
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError, URLError


def check_link(url: str):
    try:
        res = urlopen(url, timeout=5)
        return {"result": True, "code": res.code, "url": res.url}
    except HTTPError as e:
        # アクセスできて400や500系が来た時はこっち
        return {"result": False, "code": e.code, "url": url, "reason": e.reason}
    except URLError as e:
        # そもそもアクセスすらできなかった場合はこっち
        return {"result": False, "code": None, "url": url, "reason": e.reason}


def extract_link(files: list):
    # 各ファイルからリンクを抽出します。
    # 重複しているリンクはフラグがTrueになります。
    # チェックすべきなのはこのフラフが
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
                        {"line": i + 1, "link": url, "duplicate": duplicate}
                    )
    return links


def lookup_file(path: str, filter="*.md"):
    # 指定したディレクトリから検査対象のファイルを抽出します。デフォルトはmdです。
    p = Path(path)
    files = [str(item) for item in p.rglob(filter)]
    return files


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--verbose", action="store_true", help="Increase verbosity")
    group.add_argument("--quiet", action="store_true", help="Decrease verbosity")
    return parser


def main(args=None):
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    files = lookup_file(parsed_args.src)
    return files


if __name__ == "__main__":
    main()
