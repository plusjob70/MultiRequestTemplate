from types import ModuleType, NoneType
from typing import Iterator, Type, Optional, Any

from app.common.exception import DuplicateNameError, ParserNotFoundError, RequestFileError
from app.common.message import Message
from app.common.types import Types
from app.dataclass.repository.repository_config import RepositoryConfig
from app.dataclass.repository.result_repository import ResultRepository
from app.dataclass.request.request_data import RequestData, ClientBaseVariable, RepositorySchema
from app.parser.parser import AbstractParser
from app.repository.repository import AbstractRepository
from app.resolver.validator import ResolverValidator as RV
from app.util.converter import Deserializer
from app.util.importer import DynamicImporter
from app.util.zipper import RequestVariableZipper


class RequestFileResolver:

    def __init__(self):
        self.request_names: list = []
        self.result_repository: Optional[ResultRepository] = None
        self.request_data_iter: Iterator[RequestData] = iter([])

    def resolve(self, file_name: str, parser_dir_abs_path: str, parser_pkg: str, methods: list, repositories: list[str]) -> None:
        parser_modules: list[ModuleType] = self._import_parser_modules(parser_dir_abs_path, parser_pkg)

        request: dict[str, Any] = self._open_request_file(file_name)
        result_repository_attr: dict[str, Any] = self._extract_result_repository_attr(request)
        request_list_attr: list[dict] = self._extract_request_list_attr(request)

        self._set_result_repository(result_repository_attr, repositories)
        self._set_request_data_iter(request_list_attr, parser_modules, methods)

    @staticmethod
    def _import_parser_modules(parser_dir_abs_path: str, parser_pkg: str) -> list[ModuleType]:
        """ Import Parser from package. """
        return DynamicImporter.do_import(parser_dir_abs_path, parser_pkg)

    @staticmethod
    def _open_request_file(file_name: str) -> dict:
        """ Open request json file and convert to dictionary. """
        return Deserializer.json_to_dict(file_name)

    def _set_result_repository(self, result_repository_attr: dict[str, Any], support_repositories: list[str]) -> None:
        """ Set self.result_repository. """
        repository_cls: Type[AbstractRepository] = self._extract_repository_attr(result_repository_attr, support_repositories)
        repository_config: RepositoryConfig = self._extract_repository_config_attr(result_repository_attr)
        self.result_repository = ResultRepository(repository_cls, repository_config)

    def _set_request_data_iter(self, request_list: list[dict[str, Any]], parser_modules: list[ModuleType], methods: list[str]) -> None:
        """ Set self.request_data_iter. """
        request_data_list: list[RequestData] = []
        for idx, request in enumerate(request_list, start=1):
            try:
                request_name: str = self._extract_name_attr(request, idx)
                parser_cls: Type[AbstractParser] = self._extract_parser_attr(request, parser_modules)
                base_setting: ClientBaseVariable = self._extract_base_setting_attr(request, methods)
                zipper: RequestVariableZipper = self._extract_variables_attr(request)
                schema: RepositorySchema = self._extract_repository_schema_attr(request)
                request_delay: float = self._extract_request_delay_second_attr(request)

                request_data_list.append(
                    RequestData(request_name, parser_cls, base_setting, zipper, schema, request_delay)
                )
            except RequestFileError:
                raise RuntimeError(Message.Error.INVALID_REQUEST_IN_REQUEST_FILE.format(idx=idx))

        self.request_data_iter = iter(request_data_list)

    def _extract_name_attr(self, request: dict[str, Any], idx: int) -> str:
        """ Extract "name" in request and append request name to self.request_names. """
        request_name: str = request.get("name", f"request#{idx}")
        if request_name in self.request_names:
            raise DuplicateNameError(Message.Error.DUPLICATE_PARSER_NAME.format(parser_cls_name=request_name))
        self.request_names.append(request_name)
        return request_name

    @staticmethod
    def _extract_result_repository_attr(request: dict[str, Any]) -> dict[str, Any]:
        """ Extract "result_repository" in request. """
        result_repository_attr: dict[str, Any] = request.get("result_repository", {})
        RV.validate_type(result_repository_attr, dict)
        RV.validate_exist_value(result_repository_attr, "result_repository")
        return result_repository_attr

    @staticmethod
    def _extract_request_list_attr(request: dict[str, Any]) -> list[dict[str, Any]]:
        """ Extract "request_list" in request. """
        request_list_attr: list[dict[str, Any]] = request.get("request_list", [])
        RV.validate_type(request_list_attr, list)
        RV.validate_exist_value(request_list_attr, "request_list")
        return request_list_attr

    @staticmethod
    def _extract_request_delay_second_attr(request: dict[str, Any]) -> float:
        """ Extract "request_delay_second" in request. """
        request_delay = request.get("request_delay_second", 0.0)
        RV.validate_types(request_delay, int, float)
        return float(request_delay)

    @staticmethod
    def _extract_repository_schema_attr(request: dict[str, Any]) -> RepositorySchema:
        """ Extract "repository_schema" in request. """
        repository_schema_attr = request.get("repository_schema", {})
        RV.validate_type(repository_schema_attr, dict)
        RV.validate_required_keys(repository_schema_attr, "columns", "types")

        columns = repository_schema_attr.get("columns", [])
        RV.validate_type(columns, list)
        RV.validate_exist_value(columns, "columns")
        RV.validate_type_in_iterable(columns, str)

        types = repository_schema_attr.get("types", [])
        RV.validate_type(columns, list)
        RV.validate_exist_value(types, "types")
        RV.validate_type_in_iterable(types, str)

        RV.validate_mapping_lists(columns, types)
        return RepositorySchema(columns, types)

    @staticmethod
    def _extract_variables_attr(request: dict[str, Any]) -> RequestVariableZipper:
        """ Extract "variables" in request. """
        variables_attr: dict[str, list] = request.get("variables", {})
        RV.validate_type(variables_attr, dict)
        RV.validate_exist_value(variables_attr, "variables")

        paths: Types.PathsType = variables_attr.get("paths", None)
        RV.validate_types(paths, list, NoneType)
        if paths is not None:
            RV.validate_type_in_iterable(paths, Types.PathType)

        queries: Types.QueriesType = variables_attr.get("queries", None)
        RV.validate_types(queries, list, NoneType)
        if queries is not None:
            RV.validate_type_in_iterable(queries, dict)

        headers: Types.HeadersType = variables_attr.get("headers", None)
        RV.validate_types(headers, list, NoneType)
        if headers is not None:
            RV.validate_type_in_iterable(headers, dict)

        cookies: Types.CookiesType = variables_attr.get("cookies", None)
        RV.validate_types(cookies, list, NoneType)
        if cookies is not None:
            RV.validate_type_in_iterable(cookies, dict)
        return RequestVariableZipper(paths, queries, headers, cookies)

    @classmethod
    def _extract_parser_attr(cls, request: dict[str, Any], parser_modules: list[ModuleType]) -> Type[AbstractParser]:
        """ Extract "parser" in request. """
        parser_attr: str = request.get("parser", "")
        RV.validate_type(parser_attr, str)
        return cls._fetch_parser_cls(parser_modules, parser_attr)

    @staticmethod
    def _extract_base_setting_attr(request: dict[str, Any], methods: list[str]) -> ClientBaseVariable:
        """ Extract "base_setting" in request. """
        base_setting_attr: dict = request.get("base_setting", {})
        RV.validate_type(base_setting_attr, dict)

        RV.validate_required_keys(base_setting_attr, "url", "method")
        url: str = base_setting_attr.get("url")
        RV.validate_type(url, str)

        method = base_setting_attr.get("method")
        RV.validate_type(method, str)
        RV.validate_support(method, methods)

        path: Types.PathType = base_setting_attr.get("path", None)
        RV.validate_types(path, str, NoneType)

        query = base_setting_attr.get("query", None)
        RV.validate_types(query, dict, NoneType)

        header = base_setting_attr.get("header", None)
        RV.validate_types(header, dict, NoneType)

        cookie = base_setting_attr.get("cookie", None)
        RV.validate_types(cookie, dict, NoneType)
        return ClientBaseVariable(url, method, path, query, header, cookie)

    @staticmethod
    def _extract_repository_attr(result_repository: dict[str, Any], support_repositories: list[str]) -> Type[AbstractRepository]:
        """ Extract "result_repository" > "repository" and get repository class. """
        repository: str = result_repository.get("repository", "")
        RV.validate_type(repository, str)
        RV.validate_exist_value(repository, "repository")
        RV.validate_support((repository := repository.lower()), support_repositories)

        match repository:
            case "csv":
                from app.repository.local.csv_repository import CSVRepository
                return CSVRepository
            case "mongo":
                from app.repository.mongo.mongo_repository import MongoRepository
                return MongoRepository
            case "bigquery":
                raise NotImplementedError

    @staticmethod
    def _extract_repository_config_attr(result_repository: dict[str, Any]) -> RepositoryConfig:
        """ Extract "result_repository" > "repository_config" and get repository config. """
        repository: str = result_repository.get("repository", "")
        repository_config: dict[str, Any] = result_repository.get("repository_config", {})
        RV.validate_type(repository_config, dict)
        RV.validate_exist_value(repository_config, "repository_config")

        match repository:
            case "csv":
                from app.dataclass.repository.repository_config import CSVRepositoryConfig
                RV.validate_required_key(repository_config, "project")

                project = repository_config.get("project", "")
                RV.validate_type(project, str)
                RV.validate_exist_value(project, "project")
                RV.validate_directory(project)

                return CSVRepositoryConfig(project=project)
            case "mongo":
                from app.dataclass.repository.repository_config import MongoRepositoryConfig
                RV.validate_required_keys(repository_config, "project", "host", "port")

                project: str = repository_config.get("project", "")
                RV.validate_type(project, str)
                RV.validate_exist_value(project, "project")
                repository_config.pop("project")

                host: str = repository_config.get("host", "")
                RV.validate_type(host, str)
                RV.validate_exist_value(host, "host")
                repository_config.pop("host")

                port: int = repository_config.get("port", 0)
                RV.validate_type(port, int)
                RV.validate_exist_value(port, "port")
                repository_config.pop("port")

                username: Optional[str] = repository_config.get("username", None)
                RV.validate_types(username, str, NoneType)
                password: Optional[str] = repository_config.get("password", None)
                RV.validate_types(password, str, NoneType)

                if username is not None:
                    repository_config.pop("username")
                if password is not None:
                    repository_config.pop("password")
                if not username or not password:
                    username = None
                    password = None

                option: Optional[dict] = repository_config if repository_config else None
                return MongoRepositoryConfig(project=project, host=host, port=port, username=username, password=password, option=option)
            case "bigquery":
                raise NotImplementedError

    @staticmethod
    def _fetch_parser_cls(parser_modules: list[ModuleType], parser_cls_name: str) -> Type[AbstractParser]:
        """ Fetch parser class in parser module list. """
        for module in parser_modules:
            parser_cls = getattr(module, parser_cls_name, None)
            if parser_cls is not None:
                return parser_cls
        raise ParserNotFoundError(Message.Error.PARSER_NOT_FOUND_IN_MODULE.format(parser_cls_name=parser_cls_name))
