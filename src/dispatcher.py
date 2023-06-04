import importlib.machinery
import importlib.util
import sys

from aiogram import Dispatcher as adp

import errors


class Dispatcher(adp):
    __middlewares: dict

    def __init__(self, *args, **kwargs):
        self.__middlewares = {}
        super().__init__(*args, **kwargs)

    def add_mw(self, ):

    def _load_from_module_spec(self, spec: importlib.machinery.ModuleSpec, key: str) -> None:
        lib = importlib.util.module_from_spec(spec)
        sys.modules[key] = lib
        try:
            spec.loader.exec_module(lib)  # type: ignore
        except Exception as e:
            del sys.modules[key]
            raise errors.ExtensionFailed(key, e) from e

        try:
            setup = getattr(lib, 'setup')
        except AttributeError:
            del sys.modules[key]
            raise errors.NoEntryPointError(key)

        try:
            await setup(self)
        except Exception as e:
            del sys.modules[key]
            raise errors.ExtensionFailed(key, e) from e
        else:
            self.__middlewares[key] = lib

    def load_middleware(self, name: str):
        name = self._resolve_name(name)
        if name in self.__middlewares:
            raise errors.ExtensionAlreadyLoaded(name)

        spec = importlib.util.find_spec(name)
        if spec is None:
            raise errors.ExtensionNotFound(name)

        self._load_from_module_spec(spec, name)

    @staticmethod
    def _resolve_name(name: str) -> str:
        try:
            return importlib.util.resolve_name(name, None)
        except ImportError:
            raise errors.ExtensionNotFound(name)
