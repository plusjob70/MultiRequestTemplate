from typing import Iterator

from app.common.types import Types


class RequestVariableZipper:

    def __init__(
            self,
            paths: Types.PathsType = None,
            queries: Types.QueriesType = None,
            headers: Types.HeadersType = None,
            cookies: Types.CookiesType = None
    ):
        if paths is None:
            paths = []
        if queries is None:
            queries = []
        if headers is None:
            headers = []
        if cookies is None:
            cookies = []

        self.pres_iter = 0
        self.final_iter = max(len(paths), len(queries), len(headers), len(cookies))

        self.paths: Iterator[Types.PathType] = iter(paths)
        self.queries: Iterator[Types.QueryType] = iter(queries)
        self.headers: Iterator[Types.HeaderType] = iter(headers)
        self.cookies: Iterator[Types.CookieType] = iter(cookies)

    def __next__(self):
        if self.pres_iter < self.final_iter:
            self.pres_iter += 1
            return tuple([
                next(self.paths, None),
                next(self.queries, None),
                next(self.headers, None),
                next(self.cookies, None)
            ])
        raise StopIteration

    def __iter__(self):
        return self
