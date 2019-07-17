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

from PySide2.QtWidgets import QGraphicsScene, QGraphicsView

# This will only ever change if Hello Games changes the freighter build area
GRID_SIZE = 21

class Editor(QGraphicsScene):
  """QGraphicsScene containing the editing area.

  Defines the grid-space representing the floor layout of the freighter.
  """

  def __init__(self):
    """blah"""

    super().__init__()

    self.cell_size = 20  # px

    # Draw the grid
    # TBD: Should we use a QRect for the grid border? It could possibly come in
    # handy for bounds checking
    for n in range(GRID_SIZE + 1):
      pos = self.cell_size * n
      length = self.cell_size * GRID_SIZE
      self.addLine(pos, 0, pos, length)
      self.addLine(0, pos, length, pos)


  def view(self) -> QGraphicsView:
    """Return a QGraphicsView object of the Editor."""

    return QGraphicsView(self)