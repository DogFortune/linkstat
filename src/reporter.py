import dataclasses
from pprint import pprint as pp


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
        pp(self.data_list)
        line = ""

        return line
