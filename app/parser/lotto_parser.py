from bs4 import BeautifulSoup

from app.parser.json_parser import JSONOriginalParser
from app.parser.parser import AbstractParser


class LottoAPIParser(JSONOriginalParser):

    @classmethod
    def parse(cls, data: bytes) -> dict[str, str | int | float]:
        original: dict = super().parse(data)
        original.pop("randomNumber")
        return original


class LottoViewParser(AbstractParser):
    KEYS = [
        "week", "drawDate",
        "firstNumber", "secondNumber", "thirdNumber", "fourthNumber", "fifthNumber", "sixthNumber",
        "bonusNumber"
    ]

    @classmethod
    def parse(cls, data: bytes) -> dict[str, str | int | float]:
        html = BeautifulSoup(data, "html.parser")
        result = {}
        values = [td.get_text() for td in html.find_all("td")]
        result.update(zip(cls.KEYS, values))
        return result
