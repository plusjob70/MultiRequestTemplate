from abc import ABCMeta, abstractmethod

from app.common.types import Types
from app.dataclass.client.client_request_result import ClientRequestResult


class AbstractHTTPRequestClient(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, **kwargs) -> None:
        pass

    @abstractmethod
    async def request(
            self,
            path: Types.PathType = "",
            query: Types.QueryType = None,
            header: Types.HeaderType = None,
            cookie: Types.CookieType = None,
            timeout: float = None,
            **kwargs
    ) -> ClientRequestResult:
        pass

    @abstractmethod
    def set_session(
            self,
            base_url: Types.URLType,
            base_path: Types.PathType,
            base_query: Types.QueryType,
            base_header: Types.HeaderType,
            base_cookie: Types.CookieType,
            **kwargs
    ) -> None:
        pass

    @abstractmethod
    async def close_session(self) -> None:
        pass
