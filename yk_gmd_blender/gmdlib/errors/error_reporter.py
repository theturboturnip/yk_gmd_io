import abc
from typing import NoReturn, Set

from .error_classes import GMDImportExportError


class ErrorReporter(abc.ABC):
    def recoverable(self, msg: str):
        raise NotImplementedError()

    def fatal_exception(self, ex: Exception) -> NoReturn:
        raise NotImplementedError()

    def fatal(self, msg: str) -> NoReturn:
        raise NotImplementedError()

    def info(self, msg: str):
        raise NotImplementedError()

    def debug(self, category: str, msg: str) -> bool:
        """Prints a category/msg pair if the category is accepted by a filter

        :param category:
        :param msg:
        :return: True if the category was accepted and the message was printed
        """
        raise NotImplementedError()


class StrictErrorReporter(ErrorReporter):
    allowed_categories: Set[str]

    def __init__(self, allowed_categories: Set[str]):
        self.allowed_categories = allowed_categories

    def recoverable(self, msg: str):
        raise GMDImportExportError(msg)

    def fatal_exception(self, ex: Exception) -> NoReturn:
        raise ex

    def fatal(self, msg: str) -> NoReturn:
        raise GMDImportExportError(msg)

    def info(self, msg: str):
        print(f"[YKGMD] [INFO ] {msg}")

    def debug(self, category: str, msg: str) -> bool:
        if category in self.allowed_categories or "ALL" in self.allowed_categories:
            print(f"[YKGMD] [DEBUG] [{category}] {msg}")
            return True
        return False


class LenientErrorReporter(ErrorReporter):
    allowed_categories: Set[str]

    def __init__(self, allowed_categories: Set[str] = None):
        if allowed_categories is None:
            allowed_categories = {"ALL"}
        self.allowed_categories = allowed_categories

    def recoverable(self, msg: str):
        print(f"[YKGMD] [RECOV] {msg}")

    def fatal_exception(self, ex: Exception) -> NoReturn:
        raise ex

    def fatal(self, msg: str) -> NoReturn:
        raise GMDImportExportError(msg)

    def info(self, msg: str):
        print(f"[YKGMD] [INFO ] {msg}")

    def debug(self, category: str, msg: str) -> bool:
        if category in self.allowed_categories or "ALL" in self.allowed_categories:
            print(f"[YKGMD] [DEBUG] [{category}] {msg}")
            return True
        return False
