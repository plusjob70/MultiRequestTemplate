import os
from typing import Iterable

from app.common.exception import ValidateError
from app.common.message import Message


class ResolverValidator:

    @staticmethod
    def validate_required_key(dict_: dict, key: str):
        if key not in dict_:
            raise ValidateError(Message.Error.NO_REQUIRED_KEY.format(dict_=dict_, key=key))

    @classmethod
    def validate_required_keys(cls, dict_: dict, *keys: str):
        for key in keys:
            cls.validate_required_key(dict_, key)

    @staticmethod
    def validate_exist_value(value: str | list | dict | int | bool, name: str):
        if not value:
            raise ValidateError(Message.Error.NOT_EXIST_VALUE.format(name=name))

    @staticmethod
    def validate_support(obj: object, support_list: list[object]):
        if obj not in support_list:
            raise ValidateError(Message.Error.NOT_SUPPORT.format(obj_=obj, support_list=support_list))

    @staticmethod
    def validate_type(obj: object, type_: type):
        if not isinstance(obj, type_):
            raise ValidateError(Message.Error.INVALID_TYPE.format(obj=obj, type_=type_))

    @staticmethod
    def validate_types(obj: object, *types: type):
        if not isinstance(obj, types):
            raise ValidateError(Message.Error.INVALID_MULTIPLE_TYPE.format(obj=obj, types=types))

    @staticmethod
    def validate_type_in_iterable(objs: Iterable, *types: type):
        for obj in objs:
            if not isinstance(obj, types):
                raise ValidateError(Message.Error.INVALID_TYPE.format(obj=obj, type_=types))

    @staticmethod
    def validate_directory(dir_path: str):
        if not os.path.exists(dir_path):
            raise ValidateError(Message.Error.NOT_EXIST_DIRECTORY.format(dir_path=dir_path))
        if not os.path.isdir(dir_path):
            raise ValidateError(Message.Error.NOT_DIRECTORY.format(dir_path=dir_path))

    @staticmethod
    def validate_mapping_lists(*lists: list):
        lengths = set()
        for list_ in lists:
            lengths.add(len(list_))
        if len(lengths) > 1:
            raise ValidateError(Message.Error.CANNOT_MAP_LISTS)
