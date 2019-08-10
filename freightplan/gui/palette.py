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

"""palette.py

Freighter component palette. Holds the various components that may be placed
within a freighter. Each displayed component is a selectable "swatch" that
determines what tile is placed on the grid.
"""

from PySide2.QtCore import Signal, Slot, QObject
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import (
  QDockWidget, QFrame, QGridLayout, QLabel, QPushButton, QVBoxLayout
)

import freightplan.components as Components
import freightplan.gui.iconmanager as IconManager

def _addToGridLayout(widgets: list, grid: QGridLayout, columns: int):
  """Add the list of widgets to the given GridLayout.

  Args:
    widgets: The list of widgets to add to the GridLayout.
    grid: The GridLayout to add the widgets to.
    columns: How many columns will be filled before starting a new row.
    """

  row = col = 0
  for widget in widgets:
    grid.addWidget(widget, row, col)
    col += 1
    if col == columns:
      row += 1
      col = 0


# TBD: Design of the palette
# Simple grid layout with every component, analogous to a color palette? (meh)
# Ideally grouped in some way: sections or as cascading buttons
#   - Sections acting as clusters
#   - Cascading buttons that expand into relevant, more specific components i.e.
#     one for corridor pieces, another for rooms, etc.
#   - Mimic the in-game structure of the components in the GUI?
class Palette(QDockWidget):
  """Frame containing the freighter components palette."""

  componentSelected = Signal(type(Components.ComponentID))

  def __init__(self, parent=None):
    """Constructor.

    Args:
      parent: The parent widget this Palette belongs to."""

    super().__init__('Components', parent)

    self.frame = QFrame(self)
    # self.frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
    self.setWidget(self.frame)
    self.layout = QVBoxLayout(self.frame)

    self.buttons = {}
    for component in Components.componentList():
      button = QPushButton(component.icon(), '', self.frame)
      button.setToolTip(component.name())
      button.setProperty('cid', component.cid())
      button.clicked.connect(self._buttonHandler)
      self.buttons[component.cid().name] = button

    self.layout.addWidget(QLabel('Corridors'))
    self.buttongrid = QGridLayout()
    self.layout.addLayout(self.buttongrid)
    _addToGridLayout(self.buttons.values(), self.buttongrid, 3)
    self.layout.addStretch(99)


  @Slot()
  def _buttonHandler(self):
    """Intermediary function to feed the componentSelected signal the
    button's associated ComponentID.
    """

    self.componentSelected.emit(self.sender().property('cid'))