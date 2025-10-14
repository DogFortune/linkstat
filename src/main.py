import analyze
import argparse


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

    files = analyze.search(parsed_args.src)
    links = analyze.extract_link(files)
    report_data_list = analyze.check_links(links)


if __name__ == "__main__":
    main()
