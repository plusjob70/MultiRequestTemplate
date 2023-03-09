from abc import ABCMeta, abstractmethod


class AbstractParser(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def parse(cls, data: bytes) -> dict[str, str | int | float]:
        pass
