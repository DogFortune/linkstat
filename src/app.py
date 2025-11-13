import os
import analyzer
import reporter
import argparse
from enums import OutputType
from reporter import ReportData


def __output(data: list[ReportData], format: OutputType, args):
    match format:
        case OutputType.Console:
            line = reporter.console(data)
            print(line)
        case OutputType.Json:
            output_path = args.report_json
            reporter.dump_json(data, output_path)


def __format__setting(args):
    if args.report_json:
        return OutputType.Json
    else:
        return OutputType.Console


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("src", default=os.environ.get("SRC_DIR", "."))
    parser.add_argument(
        "--report-json", type=str, help="Create json report file at given path"
    )
    return parser


def main(args=None):
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    format = __format__setting(parsed_args)
    src = parsed_args.src

    files = analyzer.search(src)
    links = analyzer.extract_link(files)
    report_data_list = analyzer.check_links(links)
    __output(report_data_list, format, parsed_args)
