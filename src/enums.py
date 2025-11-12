from enum import StrEnum, Enum, auto


class OutputType(Enum):
    Console = auto()
    Json = auto()


class Result(StrEnum):
    OK = "OK"
    NG = "NG"
