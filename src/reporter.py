import dataclasses
from pprint import pformat
import json


@dataclasses.dataclass
class ReportData:
    file: str
    line: int
    url: str
    result: str
    code: int
    reason: str


class Console:
    def __init__(self, data: list[ReportData]):
        self.data_list = data

    def generate(self) -> str:
        line = pformat(self.data_list)
        return line


class Json:
    def __init__(self, data: list[ReportData], output_path: str):
        self.data_list = data
        self.path = output_path

    def generate(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data_list, f, indent=4)
