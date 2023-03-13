from abc import ABCMeta, abstractmethod


class AbstractParser(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def parse(cls, response: bytes) -> dict[str, str | int | float | bool]:
        pass
