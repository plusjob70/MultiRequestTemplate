from dataclasses import dataclass
from typing import Type

from app.dataclass.repository.repository_config import RepositoryConfig
from app.repository.repository import AbstractRepository


@dataclass
class ResultRepository:
    repository_cls: Type[AbstractRepository]
    repository_config: RepositoryConfig
