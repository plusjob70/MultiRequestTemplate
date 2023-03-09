from dataclasses import dataclass, asdict

from app.common.types import Types


@dataclass
class ClientBaseVariable:
    host: str
    method: str
    base_path: Types.PathType
    base_query: Types.QueryType
    base_header: Types.HeaderType
    base_cookie: Types.CookieType

    def to_dict(self):
        return asdict(self)
