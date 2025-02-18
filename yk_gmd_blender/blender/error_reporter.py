from typing import NoReturn, Callable, Set

from ..gmdlib.errors.error_classes import GMDImportExportError
from ..gmdlib.errors.error_reporter import ErrorReporter


class BlenderErrorReporter(ErrorReporter):
    def __init__(self, report: Callable[[Set, str], None], base: ErrorReporter):
        self.base = base
        self.report = report

    def recoverable(self, msg: str):
        self.base.recoverable(msg)
        # If this runs, the base ErrorReporter decided that this is indeed recoverable
        self.report({"WARNING"}, msg)

    def fatal_exception(self, ex: Exception) -> NoReturn:
        self.base.fatal_exception(ex)
        # If this runs, then base.fatal_exception screwed up and didn't throw anything
        raise GMDImportExportError(ex)

    def fatal(self, msg: str) -> NoReturn:
        self.base.fatal(msg)
        # If this runs, then base.fatal screwed up and didn't throw anything
        raise GMDImportExportError(msg)

    def info(self, msg: str):
        self.base.info(msg)
        self.report({"INFO"}, msg)

    def debug(self, category: str, msg: str) -> bool:
        if self.base.debug(category, msg):
            self.report({"DEBUG"}, msg)
            return True
        return False
