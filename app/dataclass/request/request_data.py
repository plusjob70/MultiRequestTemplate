from dataclasses import dataclass
from typing import Type

from app.dataclass.client.client_base_variable import ClientBaseVariable
from app.parser.parser import AbstractParser
from app.dataclass.repository.repository_schema import RepositorySchema
from app.util.zipper import RequestVariableZipper


@dataclass
class RequestData:
    name: str
    parser_cls: Type[AbstractParser]
    base_setting: ClientBaseVariable
    variables: RequestVariableZipper
    repository_schema: RepositorySchema
    request_delay_second: float
