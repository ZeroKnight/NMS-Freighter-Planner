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

"""iconmanager.py

Loads the icons used by the GUI and provides an interface for accessing them.
"""

from PySide2.QtGui import QIcon, QPixmap

import freightplan.gui.resources_rc

_iconCache = {}

def getIcon(name: str) -> QIcon:
  """Return the icon with the given name."""

  if name not in _iconCache:
    _iconCache[name] = QIcon(f':/images/components/{name}')

  return _iconCache[name]

def getPixmap(name: str) -> QPixmap:
  """Return the icon with the given name as a pixmap."""

  return getIcon(name).pixmap()