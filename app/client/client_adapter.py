import asyncio
from asyncio import Task
from typing import Type

from app.client.http_request_client import AbstractHTTPRequestClient
from app.dataclass.client.client_request_result import ClientRequestResult
from app.dataclass.request.request_data import RequestData
from app.parser.parser import AbstractParser
from app.util.decorator import trace_function_execution_time


class ClientAdapter:

    REQUEST_TIMEOUT = 3.0

    def __init__(self, client_cls: Type[AbstractHTTPRequestClient], request_data: RequestData):
        self.client_cls = client_cls
        self.request_data = request_data

        self.request_name: str = request_data.name
        self.parser_cls: Type[AbstractParser] = request_data.parser_cls
        self.wait_delay: float = request_data.request_delay_second

    @trace_function_execution_time(attr_name="request_name")
    def run(self) -> list[dict]:
        client = self.client_cls(**self.request_data.base_setting.to_dict())
        return asyncio.run(self._request_async(client))

    async def _request_async(self, client) -> list[dict]:
        tasks: list[Task] = await self._create_tasks(client)
        results: list[dict] = self._get_results(tasks)
        return results

    async def _create_tasks(self, client) -> list[Task]:
        tasks: list[Task] = []
        async with asyncio.TaskGroup() as task_group:
            for variable in self.request_data.variables:
                coroutine = client.request(*variable, timeout=ClientAdapter.REQUEST_TIMEOUT)
                task = task_group.create_task(coroutine)
                tasks.append(task)
                if self.wait_delay > 0:
                    await asyncio.sleep(self.wait_delay)
        await client.close_session()
        return tasks

    def _get_results(self, tasks: list[Task]) -> list[dict]:
        results: list[dict] = []
        for task in tasks:
            if task.done() and (result := self._get_parsed_result_from_task(task)):
                results.append(result)
        return results

    def _get_parsed_result_from_task(self, task: Task) -> dict:
        try:
            request_result: ClientRequestResult = task.result()
            if request_result.success:
                return self.parser_cls.parse(request_result.content)
            else:
                return dict()
        except asyncio.CancelledError:
            return dict()
