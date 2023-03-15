import httpx
from httpx import AsyncClient

from app.client.http_request_client import AbstractHTTPRequestClient
from app.common.types import Types
from app.dataclass.client.client_request_result import ClientRequestResult
from app.util.logger import logger


class HTTPXRequestClient(AbstractHTTPRequestClient):

    def __init__(
            self,
            url: str,
            method: str,
            base_path: Types.PathType = "",
            base_query: Types.QueryType = None,
            base_header: Types.HeaderType = None,
            base_cookie: Types.CookieType = None,
            **kwargs
    ):
        self.method = method
        self.__session: AsyncClient = AsyncClient(
            base_url=self.resolve_url(url, base_path),
            params=base_query,
            headers=base_header,
            cookies=base_cookie,
            **kwargs
        )

    async def request(
            self,
            path: Types.PathType = None,
            query: Types.QueryType = None,
            header: Types.HeaderType = None,
            cookie: Types.CookieType = None,
            timeout: float = None,
            **kwargs
    ) -> ClientRequestResult:
        try:
            if path is None:
                path = ""
            elif not isinstance(path, str):
                path = str(path)

            response = await self.__session.request(method=self.method, url=path, params=query,
                                                    headers=header, cookies=cookie, timeout=timeout, **kwargs)
            if not response.is_success:
                logger.info(f"{response.url} request failed.")

        except httpx.HTTPError as e:
            logger.error(e)
            return ClientRequestResult(success=False, content=bytes(str(e).encode("utf-8")))

        return ClientRequestResult(success=response.is_success, content=response.content)

    def set_session(
            self,
            base_url: Types.URLType,
            base_path: Types.PathType,
            base_query: Types.QueryType,
            base_header: Types.HeaderType,
            base_cookie: Types.CookieType,
            **kwargs
    ) -> None:
        self.__session = AsyncClient(
            base_url=self.resolve_url(base_url, base_path),
            params=base_query,
            headers=base_header,
            cookies=base_cookie,
            **kwargs
        )

    async def close_session(self) -> None:
        await self.__session.aclose()

    @staticmethod
    def resolve_url(base_url: str, base_path: str) -> str:
        if base_url[-1] == "/":
            base_url = base_url[:-1]
        if base_path[0] == "/":
            base_path = base_path[1:]
        return base_url + "/" + base_path
