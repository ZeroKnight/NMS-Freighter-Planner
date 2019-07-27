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

"""plan.py

A plan is the typical "document" in freightplan; it represents everything
about a given freighter layout.
"""

from freightplan import Floor

class Plan():
  """A freighter plan. The typical "document" in freightplan."""

  # list or set containing the layers of the plan. Must be limited to 14, and the
  # first layer is special in that it has 3 unmodifiable spaces

  # TODO: parameters
  def __init__(self):
    """Constructor."""

    self._floors = []
    self._nextFloorId = 0

    self.addFloor(1)


  def addFloor(self, level: int, name: str=None):
    """Add a floor to the plan.

    Args:
      level: The level that the floor should be added as.
      name: The name of the floor. If unspecified, defaults to "Floor n"
            where n = level.
    """

    if not name:
      name = f'Floor {level}'

    floor = Floor(name, level, self, visible=True, locked=False)
    floor.setID(self.claimNextFloorId())
    self._floors.append(floor)


  def removeFloor(self, index: int):
    """Remove a floor from the plan.

    Args:
      index: The index to the plan's floor list of the floor to remove.
    """
    del self._floors[index]


  def floorAt(self, index: int) -> Floor:
    """Return the floor at the given index of the Plan's floor list."""

    return self._floors[index]


  def claimNextFloorId(self):
    """Return the next available floor id."""

    nextId = self._nextFloorId
    self._nextFloorId += 1
    return nextId