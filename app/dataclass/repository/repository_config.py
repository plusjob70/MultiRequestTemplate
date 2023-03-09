from dataclasses import dataclass


class RepositoryConfig:
    pass


@dataclass
class CSVRepositoryConfig(RepositoryConfig):
    project: str


@dataclass
class MongoRepositoryConfig(RepositoryConfig):
    project: str
    host: str
    port: int
    username: str = None
    password: str = None
    option: dict = None

    def get_connection_uri(self):
        uri = ["mongodb://"]
        if self.username and self.password:
            uri.append(f"{self.username}:{self.password}@")

        uri.append(f"{self.host}:{self.port}")

        if self.option:
            uri.append(f"/{self._option_to_string()}")
        return "".join(uri)

    def _option_to_string(self):
        result: list[str] = []
        for k, v in self.option.items():
            result.append(f"{k}={v}")
            result.append("&")

        result.pop()
        return "".join(result)
