# This file is part of freightplan - No Man's Sky Freighter Planner
# Copyright (C) 2019  Alex "ZeroKnight" George
#
# freightplan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# freightplan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# TODO: docstring

from PySide2.QtWidgets import QDockWidget

# create tab bar (All floors, current floor only, etc.)
# interface scrolls as more component types are in use
# each "cell" should probably be a class object
class Sidebar(QDockWidget):
  """Frame acting as the sidebar; holds component breakdown information.

  Shows component counts, their material costs, etc.
  """

  def __init__(self, parent=None):
    """blah"""

    super().__init__('Material Breakdown', parent)