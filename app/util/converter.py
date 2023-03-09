import json
from json import JSONDecodeError

from app.common.message import Message


class Deserializer:
    @staticmethod
    def json_to_dict(file_path: str) -> dict:
        with open(file_path, mode="r") as file:
            try:
                return json.load(file)
            except JSONDecodeError:
                raise JSONDecodeError(Message.Error.CANNOT_DECODE_JSON, "", 0)

    @staticmethod
    def txt_to_list(file_path: str) -> list[str]:
        with open(file_path) as file:
            return file.read().splitlines()
