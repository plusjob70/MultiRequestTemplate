from typing import Optional


class Types:

    URLType = str
    ParamType = str | int | float | bool
    StrMapType = dict[str, ParamType]

    PathType = Optional[ParamType]
    QueryType = Optional[StrMapType]
    HeaderType = Optional[StrMapType]
    CookieType = Optional[StrMapType]

    PathsType = Optional[list[PathType]]
    QueriesType = Optional[list[QueryType]]
    HeadersType = Optional[list[HeaderType]]
    CookiesType = Optional[list[CookieType]]
