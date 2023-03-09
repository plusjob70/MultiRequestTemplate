from app.client.client_manager import ClientManager
from app.common.message import Message
from app.config import AppConfig
from app.repository.repository_manager import RepositoryManager
from app.resolver.file_resolver import RequestFileResolver
from app.util.decorator import trace_function_execution_time
from app.util.logger import logger


class Dispatcher:

    def __init__(self, num_process, num_connection):
        self.client_manager: ClientManager = ClientManager(num_process)
        self.repository_manager: RepositoryManager = RepositoryManager(num_connection)

    @trace_function_execution_time()
    def dispatch(self) -> None:
        resolver = self._resolve_file()
        self.client_manager.execute(resolver)

        if failed := self.client_manager.failed_request_names:
            logger.info(Message.Info.FAILED_REQUEST.format(failed=failed))

        if request_result := self.client_manager.request_result:
            repository_schemata = self.client_manager.repository_schemata
            self.repository_manager.execute(resolver.result_repository, request_result, repository_schemata)

    @staticmethod
    def _resolve_file() -> RequestFileResolver:
        resolver = RequestFileResolver()
        resolver.resolve(
            file_name=AppConfig.REQUEST_FILE_PATH,
            parser_dir_abs_path=AppConfig.PARSER_DIR_ABS_PATH,
            parser_pkg=AppConfig.PARSER_PACKAGE,
            methods=AppConfig.SUPPORT_METHOD_LIST,
            repositories=AppConfig.SUPPORT_DATA_REPOSITORIES
        )
        return resolver
