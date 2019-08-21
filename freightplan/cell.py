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

"""cell.py

A cell is the atomic unit of a grid; that is to say, a grid is made up of
cells. Each cell can display a Tile, which is an image representing a
particular component that can be placed on the freighter at the grid level,
e.g. corridors and rooms.
"""

from PySide2.QtCore import QPoint, QRect

from freightplan.gui.tile import Tile

class Cell():
  """A single grid cell. Can contain a Tile."""

  def __init__(self, parent, pos: QPoint, size: int=32):
    """Constructor.

    Args:
      parent: The grid that this cell belongs to.
      pos: The position of this cell on the grid as a QPoint.
      size: The size of this cell in pixels. Defaults to 32px.
    """

    self._parent = parent
    self._pos = pos
    self._rect = QRect(pos, size, size)
    self._tile = None


  def parent(self):
    """Return the parent grid that this cell belongs to."""

    return self._parent


  def pos(self) -> QPoint:
    """Return the cell's grid position as a QPoint."""

    return QPoint(self._pos)


  def x(self) -> int:
    """Return the cell's X grid coordinate."""

    return self._pos.x()


  def y(self) -> int:
    """Return the cell's Y grid coordinate."""

    return self._pos.y()


  def size(self) -> int:
    """Return the cell's size."""

    return self._rect.height()


  def tile(self) -> Tile:
    """Return this cell's Tile object."""

    return self._tile


  def setTile(self, tile: Tile):
    """Set this cell's Tile."""

    if isinstance(tile, Tile):
      self._tile = tile
    else:
      raise TypeError('Must be a Tile object')


  def clearTile(self):
    """Removes the cell's current Tile."""

    self._tile = None


  def isEmpty(self) -> bool:
    """Return whether or not the cell is empty, i.e. has a Tile."""

    return self._tile == None