"""


Spreadsheet Operators
*********************

:func:`add_row_filter_rule`

:func:`change_spreadsheet_data_source`

:func:`remove_row_filter_rule`

:func:`toggle_pin`

"""

import typing

def add_row_filter_rule() -> None:

  """

  Add a filter to remove rows from the displayed data

  """

  ...

def change_spreadsheet_data_source(component_type: int = 0, attribute_domain_type: int = 0) -> None:

  """

  Change visible data source in the spreadsheet

  """

  ...

def remove_row_filter_rule(index: int = 0) -> None:

  """

  Remove a row filter from the rules

  """

  ...

def toggle_pin() -> None:

  """

  Turn on or off pinning

  """

  ...
