from enum import StrEnum, Enum, auto


class OutputType(Enum):
    Console = auto()


class Result(StrEnum):
    OK = "OK"
    NG = "NG"
