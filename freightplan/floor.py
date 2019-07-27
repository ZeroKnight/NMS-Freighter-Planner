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

"""floor.py

A Floor object represents a floor on the freighter. Each floor has its own
independent grid of cells representing the layout of the particular floor it
represents. The grid increases to the right and downward, with the origin in
the top left. Grid coordinates are represented as a typical (x,y) coordinate
pair, starting from 0.

Conceptually, floors are essentially "layers", much like those found in
graphics editing software. Much like these layers, floors are "stacked" on
top of one another and can be freely added, removed, and rearranged.

Sectors:

Floors may contain sectors: an abstract region within a Floor. Typically used
to denote "rooms" or arbitrary named areas used for reference purposes. These
regions are purely logical representations for user convenience; they
currently have no parallel in game as of yet.

Sectors are rectangular regions within a Floor's grid space, and are
displayed in the Editor has a transparent colored overlay across the region's
area. Sectors have a name, which appears as a label within the overlay.
"""

from PySide2.QtCore import QPoint, QRect, QSize
from PySide2.QtGui import QColor

from freightplan import GRID_SIZE
from freightplan import Cell, Plan

def mapGridToIndex(pos: QPoint) -> int:
  """Map grid coordinates to a list index."""

  return pos.y() * GRID_SIZE + pos.x()


def mapIndexToGrid(index: int) -> QPoint:
  """Map a list index to a grid coordinate."""

  return QPoint(index % GRID_SIZE, index // GRID_SIZE)


class IdMixin():
  """Mixin for Floor and Sector class objects. Provides unique IDs.

  An identifier that will always uniquely identify a particular floor or
  sector. Names can change for both sectors and floors, and levels can change
  as floors are repositioned, renamed, cloned, and deleted; its ID will never
  change over its lifetime.
  """

  def id(self) -> int:
    """Return the object ID."""

    return self._id


  def setId(self, id):
    """Set the object ID."""

    if isinstance(id, int):
      if id >= 0:
        self._id = id
      else:
        raise ValueError('id must not be negative')
    else:
      raise TypeError('id must be an int')


class Sector(QRect, IdMixin):
  """Named region within a Floor, shown as a transparent, colored overlay.

  Represents an arbitrary "room" or "area" meaningful to the user, e.g.
  "Storage", "Bridge", "Medbay", etc.
  """

  def __init__(self, pos: QPoint, size: QSize, name: str, color: QColor):
    """Constructor.

    Args:
      pos: The position of the sector, which is its top-left corner on the
           grid.
      size: The size of the sector as a QSize.
      name: The name of the sector, which appears as a label within the
            sector on the Editor.
      color: A QColor specifying the color of the sector's overlay on the
             Editor.
    """

    super().__init__(pos, size)

    self.name = name
    self.color = color


class Floor(IdMixin):
  """Primary structure within a plan; represents a single floor of the
  freighter.

  Each floor has a grid of cells and optionally a set of regions defining
  logical "rooms" or "sectors" to break up parts of the floor.
  """

  def __init__(self, name: str, level: int, plan: Plan,
               visible: bool=False, locked: bool=False):
    """Constructor.

    Creates a new floor belonging to a given plan, optionally setting initial
    visibility and lock state.

    Args:
      name: The name of the floor, i.e. what is displayed in the UI.
      level: The specific level of the freighter that this floor represents.
      plan: The Plan that this floor belongs to.
      visible: Whether or not the floor is shown in the editor. Unlike most
               layer implementations, this is false by default as each layer
               represents an independent floor and thus only makes sense to
               have one visible at a time, perhaps with a second as reference
               for alignment and relative positioning.
      locked: Whether or not the floor contents can be changed.
    """

    self.name = name

    if level == None:
      self.floor = self.nextHighestFloor()
    else:
      self.floor = level

    self._state = {'visible': visible, 'locked': locked}
    self._grid = []
    self._sectors = {}


  def name(self) -> str:
    """Return the floor name."""

    return self._name


  def setName(self, name: str):
    """Set the floor name."""

    if isinstance(name, str):
      self._name = name
    else:
      raise TypeError('name must be a string')


  def level(self) -> int:
    """Return the level this floor represents."""

    return self._level


  def setLevel(self, level):
    """Set the level this floor represents."""

    if isinstance(level, int):
      if 1 <= level <= 14:
        self._level = level
      else:
        raise ValueError('level must be between 1 and 14 inclusive')
    else:
      raise TypeError('level must be an int')


  def isVisible(self) -> bool:
    """Return whether the floor is visible."""

    return self._state['visible']


  def isLocked(self) -> bool:
    """Return whether the floor is locked."""

    return self._state['locked']


  def cellAt(self, pos: QPoint) -> Cell:
    """Return the Cell at the specified grid position via a QPoint."""

    return self._grid[mapGridToIndex(pos)]


  def setCell(self, pos: QPoint, cell: Cell):
    """Set the Cell at the specified grid position via a QPoint."""

    self._grid[mapGridToIndex(pos)] = cell


  def isEmpty(self) -> bool:
    """Return whether or not the floor is empty.

    Specifically, whether every cell's isEmpty() method returns true.
    """

    for cell in self._grid:
      if not cell.isEmpty():
        return False
    return True


  def sector(self, id: int) -> Sector:
    """Return the sector specified by id or None if it doesn't exist."""

    return self._sectors.get(id, None)


  def addSector(self, sector: Sector):
    """Add the given sector to the layer."""

    self._sectors[sector.id()] = sector


  def removeSector(self, id: int):
    """Remove the sector with the given id from the layer."""

    del self._sectors[id]


  def clone(self, level: int):
    """Create a clone of this floor on the given level.

    Args:
      level: Target level the clone should occupy.
    """
    pass


  def merge(self, target: 'Floor'):
    """Merge this floor with the target floor."""
    pass


  def destroy(self):
    """Destroys this floor, removing it from the plan's floor list."""
    pass
