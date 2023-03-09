import importlib
import os
from types import ModuleType


class DynamicImporter:

    PYTHON_EXT = ".py"
    INIT_FILE = "__init__.py"

    @classmethod
    def do_import(cls, path_package: str, prefix_module: str) -> list[ModuleType]:
        """
        @param path_package: An absolute path of python package to import
        @param prefix_module: A prefix of module name such as 'app.client'
        """
        imported_modules: list[ModuleType] = []
        for module in cls.__get_modules(path_package):
            try:
                imported_module = importlib.import_module(f"{prefix_module}.{module}")
                imported_modules.append(imported_module)
            except ImportError:
                pass
        return imported_modules

    @classmethod
    def __get_modules(cls, path_package: str) -> list[str]:
        modules: list[str] = os.listdir(path_package)
        modules = cls.__remove_ignore_files(modules)
        return cls.__strip_python_extension(modules)

    @classmethod
    def __remove_ignore_files(cls, package: list[str]) -> list[str]:
        return [
            module
            for module in package
            if module.endswith(cls.PYTHON_EXT) and module != cls.INIT_FILE
        ]

    @classmethod
    def __strip_python_extension(cls, package: list[str]) -> list[str]:
        return [module.rstrip(cls.PYTHON_EXT) for module in package]
    