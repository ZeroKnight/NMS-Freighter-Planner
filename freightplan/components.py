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

"""components.py

A component is anything that can be placed in a freighter, thus by extension
can be placed in a plan. Components consist of rooms, corridors, refiners,
terminals and so on.

This module defines all components and can provide information about them to
the other modules of freightplan.
"""

from enum import Enum, unique

from PySide2.QtGui import QIcon

import freightplan.gui.iconmanager as IconManager

_componentNameMap = {}
_componentIDMap = {}

@unique
class ComponentID(Enum):
  """Enumeration of Component IDs.

  Each component is assigned a unique ID, which is mapped in this enumeration.
  """

  RoomLarge        = 1
  RoomStorage      = 2
  RoomFleet        = 3
  CorridorStraight = 4
  CorridorCurved   = 5
  Junction         = 6
  JunctionCross    = 7
  Stairs           = 8


class Component():
  """A freighter component."""

  def __init__(self, cid: ComponentID, name: str):
    """Constructor. Creates a new component.

    Args:
      cid: The unique ID to assign this component. Must be from the
          ComponentID enumeration.
      name: The friendly name of the component. Will eventually take a
            translation key name.
      icon: The icon to associate this component with.
    """

    if isinstance(cid, ComponentID):
      self._cid = cid
    else:
      raise TypeError(f'cid argument must be a ComponentID, not {type(cid)}')

    self._name = name


  def cid(self) -> ComponentID:
    """Return this component's ComponentID."""

    return self._cid


  def name(self) -> str:
    """Return this component's name."""

    return self._name


  def icon(self) -> QIcon:
    """Return this component's icon."""

    return IconManager.getIcon(self._cid.name)


def _validID(cid: ComponentID) -> bool:
  """Return whether the given cid is a valid ComponentID."""

  if isinstance(cid, ComponentID):
    return True
  else:
    raise TypeError(f'cid argument must be a ComponentID, not {type(cid)}')
    return False


def _validName(name: str) -> bool:
  """Return whether the given name exists."""

  if name in _componentNameMap:
    return _componentNameMap[name]
  else:
    raise ValueError(f"No Component exists with name '{name}'")


def componentByID(cid: ComponentID) -> Component:
  """Return the component specified by its ComponentID."""

  if _validID(cid):
    return _componentIDMap[cid]
  else:
    return None


def componentByName(name: str) -> Component:
  """Return the component specified by its name."""

  if _validName(name):
    return _componentNameMap[name]
  else:
    return None


def componentList() -> list:
  """Return a list of all components."""

  return [_componentIDMap[x] for x in ComponentID]


# TEMP: Kludge until QTranslate is implemented
_nameMap = {
  'RoomLarge': 'Large Room',
  'RoomStorage': 'Storage Room',
  'RoomFleet': 'Fleet Command Room',
  'CorridorStraight': 'Straight Corridor',
  'CorridorCurved': 'Curved Corridor',
  'Junction': 'T-Junction',
  'JunctionCross': 'Cross Junction',
  'Stairs': 'Stairs',
}

for cid in ComponentID:
  name = _nameMap[cid.name]
  c = Component(cid, name)
  _componentIDMap[cid] = c
  _componentNameMap[name] = c