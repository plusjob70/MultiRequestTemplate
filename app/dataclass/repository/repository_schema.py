from dataclasses import dataclass


@dataclass
class RepositorySchema:
    columns: list
    types: list
