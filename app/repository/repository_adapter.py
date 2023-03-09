import asyncio
from asyncio import Task

from app.dataclass.repository.repository_insert_result import RepositoryInsertResult
from app.dataclass.repository.repository_schema import RepositorySchema
from app.repository.repository import AbstractRepository
from app.util.logger import logger


class RepositoryAdapter:

    def __init__(
            self,
            num_connection: int,
            repository: AbstractRepository,
            request_result: dict[str, list[dict]],
            repository_schemata: dict[str, RepositorySchema]
    ):
        asyncio.Semaphore(num_connection)

        self.repository = repository
        self.request_result = request_result
        self.repository_schemata = repository_schemata

    def run(self) -> None:
        return asyncio.run(self._insert_all())

    async def _insert_all(self) -> None:
        tasks: list[Task] = await self._create_tasks()
        return self._get_results(tasks)

    async def _create_tasks(self) -> list[Task]:
        tasks: list[Task] = []
        async with asyncio.TaskGroup() as task_group:
            for request_name in self.request_result.keys():
                result = self.request_result.get(request_name)
                schema = self.repository_schemata.get(request_name)
                coroutine = self.repository.insert(table=request_name, data=result, schema=schema)
                task = task_group.create_task(coroutine)
                tasks.append(task)
        return tasks

    @staticmethod
    def _get_results(tasks: list[Task]) -> None:
        for task in tasks:
            if task.done():
                result: RepositoryInsertResult = task.result()
                if not result.success:
                    logger.info(f"insert failed - {result.detail}")
