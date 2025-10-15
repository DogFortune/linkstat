import os
import analyze
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("src", default=os.environ.get("SRC_DIR", "."))
    parser.add_argument("--format", default=os.environ.get("OUTPUT_FORMAT", "CONSOLE"))
    return parser


def main(args=None):
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    files = analyze.search(parsed_args.src)
    links = analyze.extract_link(files)
    report_data_list = analyze.check_links(links)


if __name__ == "__main__":
    main()
