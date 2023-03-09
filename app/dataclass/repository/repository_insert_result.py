from dataclasses import dataclass


@dataclass
class RepositoryInsertResult:
    success: bool
    detail: dict = None
