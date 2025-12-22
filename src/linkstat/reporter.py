from dataclasses import dataclass
from dataclasses_json import dataclass_json
from linkstat.enums import Result
from typing import List
import json
import os
import shutil


@dataclass_json
@dataclass
class ReportData:
    file: str
    line: int
    url: str
    result: Result
    code: int
    reason: str | None


@dataclass_json
@dataclass
class ReportCollection:
    Reports: List[ReportData]


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # 例外オブジェクトを文字列に変換
        if isinstance(obj, Exception):
            return str(obj)
        return super().default(obj)


class Colors:
    """カラーコード"""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"


def get_fill_plain_message(msg: str) -> str:
    """区切り線が入ったメッセージテキストを作成します。
    メソッド自体はメッセージを作るだけで、出力は呼び出し側が行って下さい。

    :param msg: _description_
    :type msg: str
    :return: _description_
    :rtype: str
    """
    fill_char = "="
    terminal_width = shutil.get_terminal_size(fallback=(80, 24)).columns
    if terminal_width < 40:
        terminal_width = 80

    total_fill = terminal_width - len(msg)
    left_fill = total_fill // 2
    right_fill = total_fill - left_fill

    start_message = f"{fill_char*left_fill}{msg}{fill_char*right_fill}"
    return start_message


def get_summary_message(data: list[ReportData]):
    """レポート内容を元にサマリーを作成します。
    チェックしたURLの数、OK,NGの数、NGのものはURLを出す。

    :param data: _description_
    :type data: list[ReportData]
    :return: _description_
    :rtype: _type_
    """
    total_count = len(data)
    ok_count = sum(item.result == Result.OK for item in data)
    ng_items = [item for item in data if item.result == Result.NG]

    total_part = f"{Colors.GREEN}{total_count} Total{Colors.RESET}"
    ok_part = f"{Colors.GREEN}{ok_count} OK{Colors.RESET}"

    color_message = f" {total_part}, {ok_part}"
    plain_message = f" {total_count} Total, {ok_count} OK"
    summary_message = ""

    if (ng_count := len(ng_items)) == 0:
        fill_char = f"{Colors.GREEN}={Colors.RESET}"
    else:
        print(get_fill_plain_message(" FAILURES "))
        ng_detail = "\n".join([f"{item.url}: {item.reason}" for item in ng_items])
        summary_message += f"{ng_detail}" + "\n"
        ng_part = f"{Colors.RED}{ng_count} NG{Colors.RESET}"
        fill_char = f"{Colors.RED}={Colors.RESET}"
        color_message += f", {ng_part} "
        plain_message += f", {ng_count} NG "

    terminal_width = shutil.get_terminal_size(fallback=(80, 24)).columns
    if terminal_width < 40:
        terminal_width = 80

    total_fill = terminal_width - len(plain_message)
    left_fill = total_fill // 2
    right_fill = total_fill - left_fill

    summary_message += f"{fill_char*left_fill}{color_message}{fill_char*right_fill}"
    return summary_message


def dump_json(data: list[ReportData], output_path: str):
    if os.path.splitext(output_path)[-1].lower() != ".json":
        raise ValueError
    collection = ReportCollection(Reports=data)
    json_str = json.dumps(
        collection.to_dict(), indent=4, ensure_ascii=False, cls=CustomEncoder
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json_str)
