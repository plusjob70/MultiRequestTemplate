class Message:

    class Info:

        COMPLETE_TASK = "{task} complete."
        FAILED_REQUEST = "Request failed - {failed}"

    class Error:

        CANNOT_DECODE_JSON = "Cannot decode file because it is not a valid JSON."
        CANNOT_MAP_LISTS = "Cannot map each list because it is different in length."
        NO_REQUIRED_KEY = "Required key [{key}] does not exist in [{dict_}]."
        NOT_EXIST_VALUE = "[{name}] does not have value."
        NOT_SUPPORT = "[{obj}] is not in support list {support_list}."
        INVALID_TYPE = "[{obj}] is not [{type_}] type."
        INVALID_MULTIPLE_TYPE = "[{obj}] is not in [{types}] types."
        NOT_EXIST_DIRECTORY = "[{dir_path}] No such directory exists."
        NOT_DIRECTORY = "[{dir_path}] is not a directory."
        DUPLICATE_PARSER_NAME = "Parser [{parser_cls_name}] is duplicated."
        PARSER_NOT_FOUND_IN_MODULE = "Parser [{parser_cls_name}] cannot find in parser module."
        INVALID_REQUEST_IN_REQUEST_FILE = "Index [{idx}] of \"request_list\" has problem."
        DIFFERENT_OBJECT = "[{obj1}] is different from [{obj2}]."
