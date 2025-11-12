from dataclasses import dataclass
from dataclasses_json import dataclass_json
from pprint import pformat
import json


@dataclass_json
@dataclass
class ReportData:
    file: str
    line: int
    url: str
    result: str
    code: int
    reason: str


def console(data: list[ReportData]):
    # TODO: 出力形式は仮でpformatを設定中。
    line = pformat(data)
    return line


def dump_json(data: list[ReportData], output_path: str):
    json_str = ReportData.schema().dumps(data, many=True, indent=4)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json_str)
