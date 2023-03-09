from motor.motor_asyncio import AsyncIOMotorClient

from app.common.metaclass import Singleton
from app.dataclass.repository.repository_config import MongoRepositoryConfig
from app.dataclass.repository.repository_insert_result import RepositoryInsertResult
from app.dataclass.repository.repository_schema import RepositorySchema
from app.repository.repository import AbstractRepository


class MongoRepository(Singleton, AbstractRepository):

    def __init__(self, config: MongoRepositoryConfig):
        self._client: AsyncIOMotorClient = AsyncIOMotorClient(config.get_connection_uri())
        self.project: str = config.project

    async def insert(self, table: str, data: list[dict], schema: RepositorySchema) -> RepositoryInsertResult:
        db = self._client[self.project]
        collection = db[table]
        await collection.insert_many(data)
        return RepositoryInsertResult(success=True)

    def create_project(self):
        pass

    def create_table(self):
        pass
