import os
from pathlib import Path
from . import analyzer
from . import reporter
import argparse
from .enums import OutputType
from .reporter import ReportData


def __output(data: list[ReportData], format: OutputType, args):
    """出力

    :param data: 確認結果リスト
    :type data: list[ReportData]
    :param format: 出力形式
    :type format: OutputType
    :param args: 結果
    :type args:
    """
    match format:
        case OutputType.Console:
            line = reporter.console(data)
            print(line)
        case OutputType.Json:
            output_path = args.report_json
            reporter.dump_json(data, output_path)


def __format_setting(args) -> OutputType:
    """結果の出力形式の設定

    :param args: Arguments
    :type args: _type_
    :return: 出力形式
    :rtype: OutputType
    """
    if args.report_json:
        if Path(args.report_json).is_dir():
            raise ValueError(
                f"ERROR: --report-path must be a filename, given: {args.report_json}"
            )
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

    format = __format_setting(parsed_args)
    src = parsed_args.src

    files = analyzer.search(src)
    links = analyzer.extract_url(files)
    report_data_list = analyzer.check_links(links)
    __output(report_data_list, format, parsed_args)


if __name__ == "__main__":
    main()
