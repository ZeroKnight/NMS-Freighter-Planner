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

"""tool.py

Base class for an Editor tool; which is anything that interacts with the
editor in some way. Tools can modify the contents of the Editor, retrieve
some information from it or its contents, or both.

Tools are QObjects, and as such can have Signals and Slots and do anything
else a typical QObject could do.

Classes that subclass Tool will override the usual events in order to define
their behavior. Events are forwarded by the Editor to the active Tool.
"""

from PySide2 import QtGui, QtWidgets
from PySide2.QtCore import QEvent, QObject
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction

class Tool(QObject):
  """Base class for an Editor tool.

  Tools interact with the Editor in some way, typically modifying or
  inspecting its contents.
  """

  def __init__(self, name: str, icon: QIcon,
               shortcut: QKeySequence=QKeySequence(), parent: QObject=None):
    """Constructor."""

    super().__init__(parent)
    self._name = name
    self._editor = None
    self._enabled = False

    self.action = QAction(icon, name, parent)
    self.action.setShortcut(shortcut)

    self._eventDict = {
      QEvent.GraphicsSceneMousePress: self.mousePressEvent,
      QEvent.GraphicsSceneMouseRelease: self.mouseReleaseEvent,
      QEvent.GraphicsSceneMouseMove: self.mouseMoveEvent,
      QEvent.GraphicsSceneMouseDoubleClick: self.mouseDoubleClickEvent,
      QEvent.GraphicsSceneHoverEnter: self.hoverEnterEvent,
      QEvent.GraphicsSceneHoverLeave: self.hoverLeaveEvent,
      QEvent.GraphicsSceneHoverMove: self.hoverMoveEvent,
      QEvent.Enter: self.enterEvent,
      QEvent.Leave: self.leaveEvent,
      QEvent.KeyPress: self.keyPressEvent,
      QEvent.KeyRelease: self.keyReleaseEvent
    }


  def name(self) -> str:
    """Return the name of the Tool."""

    return self._name


  def setName(self, name: str):
    """Set the name of the Tool."""

    self._name = name


  def editor(self) -> str:
    """Return the Editor that the Tool is currently bound to."""

    return self._editor


  def setEditor(self, editor: QIcon):
    """Set the Editor that the Tool is bound to."""

    self._editor = editor


  def enabled(self) -> bool:
    """Return whether or not the Tool is enabled."""

    return self._enabled


  def setEnabled(self, enabled: bool):
    """Set whether or not the Tool is enabled."""

    self._enabled = enabled


  def event(self, event: QEvent):
    et = event.type()
    if et in self._eventDict:
      self._eventDict[et](event)
      if event.isAccepted():
        return True
    return False


  def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
    event.ignore()


  def mouseReleaseEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
    event.ignore()


  def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
    event.ignore()


  def mouseDoubleClickEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
    event.ignore()


  def enterEvent(self, event: QtGui.QEnterEvent):
    event.ignore()


  def leaveEvent(self, event: QEvent):
    event.ignore()


  def hoverEnterEvent(self, event: QtWidgets.QGraphicsSceneHoverEvent):
    event.ignore()


  def hoverLeaveEvent(self, event: QtWidgets.QGraphicsSceneHoverEvent):
    event.ignore()


  def hoverMoveEvent(self, event: QtWidgets.QGraphicsSceneHoverEvent):
    event.ignore()


  def keyPressEvent(self, event: QtGui.QKeyEvent):
    event.ignore()


  def keyReleaseEvent(self, event: QtGui.QKeyEvent):
    event.ignore()
