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

"""tile.py

Represents a placed component on the Editor grid, contained within a Cell
object. Consists of a pixmap to visually represent a component.
"""

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QGraphicsItem, QGraphicsPixmapItem

class Tile(QGraphicsPixmapItem):
  """Represents a placed component on the Editor grid."""

  def __init__(self, pixmap: QPixmap, parent: QGraphicsItem):
    """Constructor.

    Args:
      pixmap: The QPixmap to display for the tile.
      parent: The QGraphicsItem that this tile is a child of.
    """

    super().__init__(pixmap, parent)

    # Ensure the shape consists of the whole pixmap and not just the opaque
    # portion to ensure we select the Tile.
    self.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)