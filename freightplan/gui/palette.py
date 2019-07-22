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
"""Freighter component palette."""

from PySide2.QtCore import Slot
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import (
  QDockWidget, QFrame, QGridLayout, QLabel, QPushButton, QVBoxLayout
)

# TODO: Create an icon provider of some nature like qBittorrent?
import freightplan.gui.resources_rc

# TBD: Design of the palette
# Simple grid layout with every component, analogous to a color palette? (meh)
# Ideally grouped in some way: sections or as cascading buttons
#   - Sections acting as clusters
#   - Cascading buttons that expand into relevant, more specific components i.e.
#     one for corridor pieces, another for rooms, etc.
#   - Mimic the in-game structure of the components in the GUI?
class Palette(QDockWidget):
  """Frame containing the freighter components palette."""

  def __init__(self, parent=None):
    """Constructor.

    Args:
      parent: The parent widget this Palette belongs to."""

    super().__init__('Components', parent)

    self.frame = QFrame(self)
    # self.frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
    self.setWidget(self.frame)
    self.layout = QVBoxLayout(self.frame)

    self.corridor = QIcon(':/images/corridor')
    self.xcorridor = QIcon(':/images/junction-cross')
    self.tcorridor = QIcon(':/images/junction')
    self.curved = QIcon(':/images/corridor-curved')
    self.button = QPushButton(self.corridor, '', self.frame)
    self.button.setToolTip('Straight Corridor')
    self.button.pressed.connect(self.foo)

    self.layout.addWidget(QLabel('Corridors'))
    self.buttongrid = QGridLayout()
    self.layout.addLayout(self.buttongrid)
    self.buttongrid.addWidget(self.button)
    self.buttongrid.addWidget(QPushButton(self.xcorridor, '', self.frame), 0, 1)
    self.buttongrid.addWidget(QPushButton(self.tcorridor, '', self.frame), 0, 2)
    self.buttongrid.addWidget(QPushButton(self.curved, '', self.frame), 1, 0)


  @Slot()
  def foo(self):
    pass