import argparse
from pathlib import Path
from urllib.request import urlopen
from urllib.error import HTTPError, URLError


def check_link(url: str):
    try:
        res = urlopen(url, timeout=5)
        return {"result": True, "code": res.code, "url": res.url}
    except HTTPError as e:
        return {"result": False, "code": e.code, "url": e.url}
    except URLError as e:
        return {"result": False, "code": e.code, "url": e.url}


def extract_link(file_path: str):
    links = []
    # 指定したファイルからリンクを抽出します。重複はこの時点で除外しますが、ファイルをまたいだリンクの重複チェックはしない。
    # 欲しいのはファイル名と行数とリンク
    with open(file_path, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if "http" in line:
                links.append({"line": i + 1, "link": line})
    return links


def lookup_file(path: str, filter="*.md"):
    # 指定したディレクトリから検査対象のファイルを抽出します。デフォルトはmdです。
    p = Path(path)
    files = [str(item) for item in p.rglob(filter)]
    return files


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    return parser


def main(args=None):
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    files = lookup_file(parsed_args.src)
    return files


if __name__ == "__main__":
    main()
