import csv
import os

from app.common.message import Message
from app.dataclass.repository.repository_config import CSVRepositoryConfig
from app.dataclass.repository.repository_insert_result import RepositoryInsertResult
from app.dataclass.request.request_data import RepositorySchema
from app.repository.repository import AbstractRepository


class CSVRepository(AbstractRepository):

    READ_MODE = "r"
    APPEND_MODE = "a"
    CREATE_MODE = "x"

    def __init__(self, config: CSVRepositoryConfig):
        self._client = os
        self.project = config.project

    async def insert(self, table: str, data: list[dict], schema: RepositorySchema) -> RepositoryInsertResult:
        cls = self.__class__

        if not self._client.path.isdir(self.project):
            await self.create_project(self.project)

        columns: list = schema.columns
        table_name: str = f"{table}.csv"

        if table_name not in self._client.listdir(self.project):
            await self.create_table(self.project, table, columns)

        file_path: str = f"{self.project}/{table_name}"

        if columns != (header := await self.get_header(file_path)):
            return RepositoryInsertResult(
                success=False,
                detail={"cause": Message.Error.DIFFERENT_OBJECT.format(obj1=columns, obj2=header)}
            )

        with open(file_path, mode=cls.APPEND_MODE) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writerows(data)
        return RepositoryInsertResult(success=True)

    @classmethod
    async def get_header(cls, file_path: str) -> list[str]:
        with open(file_path, mode=cls.READ_MODE) as csvfile:
            return csvfile.readline().strip().split(",")

    async def create_project(self, project: str) -> None:
        self._client.mkdir(project)

    @classmethod
    async def create_table(cls, project: str, table: str, columns: list[str]) -> None:
        with open(f"{project}/{table}.csv", mode=cls.CREATE_MODE) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
