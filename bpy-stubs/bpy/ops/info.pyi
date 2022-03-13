"""


Info Operators
**************

:func:`report_copy`

:func:`report_delete`

:func:`report_replay`

:func:`reports_display_update`

:func:`select_all`

:func:`select_box`

:func:`select_pick`

"""

import typing

def report_copy() -> None:

  """

  Copy selected reports to clipboard

  """

  ...

def report_delete() -> None:

  """

  Delete selected reports

  """

  ...

def report_replay() -> None:

  """

  Replay selected reports

  """

  ...

def reports_display_update() -> None:

  """

  Update the display of reports in Blender UI (internal use)

  """

  ...

def select_all(action: str = 'SELECT') -> None:

  """

  Change selection of all visible reports

  """

  ...

def select_box(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Toggle box selection

  """

  ...

def select_pick(report_index: int = 0, extend: bool = False) -> None:

  """

  Select reports by index

  """

  ...
