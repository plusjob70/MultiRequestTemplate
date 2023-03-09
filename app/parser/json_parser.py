import json

from app.parser.parser import AbstractParser


class JSONOriginalParser(AbstractParser):

    ENCODING = "utf-8"

    @classmethod
    def parse(cls, data: bytes) -> dict[str, str | int | float]:
        return json.loads(data.decode(cls.ENCODING))
