from abc import ABCMeta, abstractmethod

from app.dataclass.repository.repository_config import RepositoryConfig
from app.dataclass.repository.repository_insert_result import RepositoryInsertResult
from app.dataclass.repository.repository_schema import RepositorySchema


class AbstractRepository(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, config: RepositoryConfig) -> None:
        pass

    @abstractmethod
    async def insert(self, table: str, data: list[dict], schema: RepositorySchema) -> RepositoryInsertResult:
        pass
