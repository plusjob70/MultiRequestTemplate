import os


class AppConfig:

    APP_DIR_NAME = "app"
    PARSER_DIR_NAME = "parser"
    REQUEST_FILE_NAME = "request.json"

    APP_ABS_PATH = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ABS_PATH = "/".join(APP_ABS_PATH.split("/")[:-1])

    PARSER_DIR_ABS_PATH = f"{APP_ABS_PATH}/{PARSER_DIR_NAME}"
    PARSER_PACKAGE = f"{APP_DIR_NAME}.{PARSER_DIR_NAME}"

    REQUEST_FILE_PATH = f"{PROJECT_ABS_PATH}/{REQUEST_FILE_NAME}"

    DEFAULT_HTTP_REQUEST_CLIENT_LIB = "httpx"

    SUPPORT_DATA_REPOSITORIES = ["csv", "bigquery", "mongo"]

    SUPPORT_METHOD_LIST = ["GET", "POST", "PUT", "DELETE"]
