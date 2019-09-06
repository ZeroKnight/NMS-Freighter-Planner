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

from PySide2 import QtGui
from PySide2.QtCore import QEvent, QObject
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QAction

# TBD: Should we inherit from or compose a QAction to handle icon, shortcut,
# etc.? Would a QAction be correct to use at all in this case?
class Tool(QObject):
  """Base class for an Editor tool.

  Tools interact with the Editor in some way, typically modifying or
  inspecting its contents.
  """

  def __init__(self, name: str, icon: QIcon, shortcut: QKeySequence=None,
               parent: QObject=None):
    """Constructor."""

    super().__init__(parent)
    self._name = name
    self._icon = icon
    self._editor = None
    self._active = False
    self._toolTip = None
    self._statusTip = None

    if shortcut is None:
      self._shortcut = QKeySequence()

    self._eventDict = {
      QEvent.MouseButtonPress: __class__.mousePressEvent,
      QEvent.MouseButtonRelease: __class__.mouseReleaseEvent,
      QEvent.MouseMove: __class__.mouseMoveEvent,
      QEvent.MouseButtonDblClick: __class__.mouseDoubleClickEvent,
      QEvent.Enter: __class__.enterEvent,
      QEvent.Leave: __class__.leaveEvent,
      QEvent.HoverEnter: __class__.hoverEnterEvent,
      QEvent.HoverLeave: __class__.hoverLeaveEvent,
      QEvent.HoverMove: __class__.hoverMoveEvent,
      QEvent.KeyPress: __class__.keyPressEvent,
      QEvent.KeyRelease: __class__.keyReleaseEvent
    }


  def name(self) -> str:
    """Return the name of the Tool."""

    return self._name


  def setName(self, name: str):
    """Set the name of the Tool."""

    self._name = name


  def icon(self) -> QIcon:
    """Return the icon of the Tool."""

    return self._icon


  def setIcon(self, icon: QIcon):
    """Set the icon of the Tool."""

    self._icon = icon


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


  def shortcut(self) -> QKeySequence:
    """Return the shortcut assigned to this Tool as a QKeySequence."""

    return self._shortcut


  def setShortcut(self, shortcut: QKeySequence):
    """Set the shortcut for this Tool, given as a QKeySequence."""

    if isinstance(shortcut, QKeySequence):
      self._shortcut = shortcut
    else:
      raise TypeError(f'shortcut must be a QKeySequence, not {type(shortcut)}')


  def toolTip(self) -> str:
    """Return the tooltip for this Tool."""

    return self._toolTip


  def setToolTip(self, text: str):
    """Set the tooltip for this Tool."""

    if isinstance(text, str):
      self._toolTip = text
    else:
      raise TypeError(f'text must be a str, not {type(text)}')


  def statusTip(self) -> str:
    """Return the status tip for this Tool."""

    return self._statusTip


  def setStatusTip(self, text: str):
    """Set the status tip for this Tool."""

    if isinstance(text, str):
      self._statusTip = text
    else:
      raise TypeError(f'text must be a str, not {type(text)}')


  def event(self, event: QEvent):
    et = event.type()
    if et in self._eventDict:
      self._eventDict[et](event)
      if event.isAccepted():
        return True
    return False


  def mousePressEvent(self, event: QtGui.QMouseEvent):
    event.ignore()


  def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
    event.ignore()


  def mouseMoveEvent(self, event: QtGui.QMouseEvent):
    event.ignore()


  def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
    event.ignore()


  def enterEvent(self, event: QtGui.QEnterEvent):
    event.ignore()


  def leaveEvent(self, event: QEvent):
    event.ignore()


  def hoverEnterEvent(self, event: QtGui.QHoverEvent):
    event.ignore()


  def hoverLeaveEvent(self, event: QtGui.QHoverEvent):
    event.ignore()


  def hoverMoveEvent(self, event: QtGui.QHoverEvent):
    event.ignore()


  def keyPressEvent(self, event: QtGui.QKeyEvent):
    event.ignore()


  def keyReleaseEvent(self, event: QtGui.QKeyEvent):
    event.ignore()