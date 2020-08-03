import abc
from typing import NoReturn

from yk_gmd_blender.yk_gmd.v2.errors.error_classes import GMDImportExportError


class ErrorReporter(abc.ABC):
    def report_recoverable_error(self, msg: str):
        raise NotImplementedError()

    def report_fatal_error(self, msg: str) -> NoReturn:
        raise NotImplementedError()


class StrictErrorReporter(ErrorReporter):
    def report_recoverable_error(self, msg: str):
        raise GMDImportExportError(msg)

    def report_fatal_error(self, msg: str) -> NoReturn:
        raise GMDImportExportError(msg)


class LenientErrorReporter(ErrorReporter):
    def report_recoverable_error(self, msg: str):
        print(f"GMDImportExportError - {msg}")

    def report_fatal_error(self, msg: str) -> NoReturn:
        raise GMDImportExportError(msg)