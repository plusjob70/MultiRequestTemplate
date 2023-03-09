from typing import Type

from app.dataclass.repository.repository_config import RepositoryConfig
from app.dataclass.repository.result_repository import ResultRepository
from app.dataclass.request.request_data import RepositorySchema
from app.repository.repository import AbstractRepository
from app.repository.repository_adapter import RepositoryAdapter
from app.util.decorator import trace_function_execution_time


class RepositoryManager:

    def __init__(self, num_connection: int = 1):
        self.num_connection = num_connection

    @trace_function_execution_time()
    def execute(
            self,
            result_repository: ResultRepository,
            request_result: dict[str, list[dict]],
            repository_schemata: dict[str, RepositorySchema]
    ) -> None:
        repo_cls: Type[AbstractRepository] = result_repository.repository_cls
        repo_cfg: RepositoryConfig = result_repository.repository_config
        repository: AbstractRepository = repo_cls(repo_cfg)

        adapter = RepositoryAdapter(self.num_connection, repository, request_result, repository_schemata)
        return adapter.run()
