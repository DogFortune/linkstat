import argparse
from pathlib import Path
import re


def extract_link(file_path: str):
    links = []
    # 指定したファイルからリンクを抽出します。重複はこの時点で除外しますが、ファイルをまたいだリンクの重複チェックはしない。
    # 欲しいのはファイル名と行数とリンク

    with open(file_path, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            print(f"{i+1}: {line}")
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
