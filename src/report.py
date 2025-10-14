import dataclasses


@dataclasses.dataclass
class ReportData:
    file: str
    line: int
    url: str
    result: str
    code: int
    reason: str


def console(data: ReportData):
    line = ""
