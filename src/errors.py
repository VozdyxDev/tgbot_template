from typing import Optional, Any


class BotException(Exception):
    pass


class ExtensionError(BotException):
    def __init__(self, message: Optional[str] = None, *args: Any, name: str) -> None:
        self.name: str = name
        message = message or f'Extension {name!r} had an error.'
        super().__init__(message, *args)


class ExtensionNotFound(ExtensionError):
    def __init__(self, name: str) -> None:
        msg = f'Extension {name!r} could not be loaded.'
        super().__init__(msg, name=name)


class ExtensionAlreadyLoaded(ExtensionError):
    def __init__(self, name: str) -> None:
        super().__init__(f'Extension {name!r} is already loaded.', name=name)


class ExtensionFailed(ExtensionError):
    def __init__(self, name: str, original: Exception) -> None:
        self.original: Exception = original
        msg = f'Extension {name!r} raised an error: {original.__class__.__name__}: {original}'
        super().__init__(msg, name=name)


class NoEntryPointError(ExtensionError):
    def __init__(self, name: str) -> None:
        super().__init__(f"Extension {name!r} has no 'setup' function.", name=name)
