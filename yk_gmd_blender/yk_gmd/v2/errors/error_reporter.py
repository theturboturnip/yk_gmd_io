import abc
from typing import NoReturn

from yk_gmd_blender.yk_gmd.v2.errors.error_classes import GMDImportExportError


class ErrorReporter(abc.ABC):
    def recoverable(self, msg: str):
        raise NotImplementedError()

    def fatal(self, msg: str) -> NoReturn:
        raise NotImplementedError()


class StrictErrorReporter(ErrorReporter):
    def recoverable(self, msg: str):
        raise GMDImportExportError(msg)

    def fatal(self, msg: str) -> NoReturn:
        raise GMDImportExportError(msg)


class LenientErrorReporter(ErrorReporter):
    def recoverable(self, msg: str):
        print(f"GMDImportExportError - {msg}")

    def fatal(self, msg: str) -> NoReturn:
        raise GMDImportExportError(msg)