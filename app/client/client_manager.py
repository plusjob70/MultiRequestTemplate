from concurrent.futures import ProcessPoolExecutor, Future, CancelledError
from typing import Type

from app.client.client_adapter import ClientAdapter
from app.client.http_request_client import AbstractHTTPRequestClient
from app.client.httpx_request_client import HTTPXRequestClient
from app.dataclass.request.request_data import RepositorySchema
from app.resolver.file_resolver import RequestFileResolver
from app.util.decorator import trace_function_execution_time


class ClientManager:

    def __init__(
            self,
            num_process: int = 1,
            timeout: float = None,
            request_client_cls: Type[AbstractHTTPRequestClient] = HTTPXRequestClient
    ):
        self.num_process = num_process
        self.timeout = timeout
        self.request_client_cls = request_client_cls

        self.future_map: dict[int, str] = {}
        self.request_result: dict[str, list[dict]] = {}
        self.repository_schemata: dict[str, RepositorySchema] = {}
        self.failed_request_names: list = []

    @trace_function_execution_time()
    def execute(self, resolver: RequestFileResolver) -> None:
        with ProcessPoolExecutor(self.num_process) as pool:
            for request_data in resolver.request_data_iter:
                adapter = ClientAdapter(self.request_client_cls, request_data)
                request_name = request_data.name

                future: Future[list[dict]] = pool.submit(adapter.run)
                self.future_map[id(future)] = request_name
                self.repository_schemata[request_name] = request_data.repository_schema
                future.add_done_callback(fn=self._add_request_result)
        return

    def _add_request_result(self, future: Future) -> None:
        request_name = self.future_map.get(id(future))
        try:
            result: list[dict] = future.result(timeout=self.timeout)
            self.request_result[request_name] = result
        except (TimeoutError, CancelledError):
            self.failed_request_names.append(request_name)
