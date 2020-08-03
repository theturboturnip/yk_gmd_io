from typing import NoReturn, Callable, Set

from yk_gmd_blender.yk_gmd.v2.errors.error_classes import GMDImportExportError
from yk_gmd_blender.yk_gmd.v2.errors.error_reporter import ErrorReporter

class BlenderErrorReporter(ErrorReporter):
    def __init__(self, report: Callable[[Set, str], None], base: ErrorReporter):
        self.base = base
        self.report = report

    def recoverable(self, msg: str):
        self.base.recoverable(msg)
        # If this runs, the base ErrorReporter decided that this is indeed recoverable
        self.report({"WARNING"}, msg)

    def fatal(self, msg: str) -> NoReturn:
        self.base.fatal(msg)
        # If this runs, then base.fatal screwed up and didn't throw anything
        raise GMDImportExportError(msg)