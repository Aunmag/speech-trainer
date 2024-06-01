from datetime import datetime
from typing import Optional


class Line:
    def __init__(self, number: int, raw: str, values: list[str]):
        self.number = number
        self.raw = raw
        self.values = values

    def get_as_str(self, index) -> Optional[str]:
        if index >= len(self.values):
            return None

        value = self.values[index]

        if value == "":
            value = None

        return value

    def get_as_int(self, index) -> Optional[int]:
        raw = self.get_as_str(index)

        if raw:
            return int(raw)
        else:
            return None

    def get_as_float(self, index) -> Optional[float]:
        raw = self.get_as_str(index)

        if raw:
            return float(raw)
        else:
            return None

    def get_as_date(self, index) -> Optional[datetime]:
        raw = self.get_as_str(index)

        if raw:
            return datetime.strptime(raw, "%Y-%m-%d")
        else:
            return None


def read(path: str, include_first_line: bool) -> list[Line]:
    with open(path, "r", encoding="UTF-8") as file:
        for i, line in enumerate(file):
            if (include_first_line or i != 0) and line != "":
                if line[0] != "#":
                    yield Line(i, line, line.split(";"))
