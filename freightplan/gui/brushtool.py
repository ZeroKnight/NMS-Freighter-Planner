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

"""brushtool.py

A Tool that places Tiles on an Editor's editing area.
"""

from PySide2 import QtGui
from PySide2.QtCore import QPointF, Qt
from PySide2.QtGui import QTransform
from PySide2.QtWidgets import QGraphicsSceneMouseEvent

from freightplan.gui.tile import Tile
from freightplan.gui.tool import Tool

class BrushTool(Tool):
  """A Tool that places Tiles on an Editor's editing area."""

  def __init__(self, *args):
    """Constructor."""

    super().__init__(self, *args)
    self.lastTilePos = None


  def handleLeftButton(self, pos: QPointF) -> bool:
    """Handles the left mouse button for the Editor area.

    Returns whether or not the calling event should be accepted.
    """

    editor = self._editor
    coord = editor.sceneToGrid(pos)
    item = editor.itemAtGridPos(coord, QTransform())
    if isinstance(item, Tile):
      # TODO: Handle different rotations
      if item.pixmap().cacheKey() != editor._tileBrush.cacheKey():
        editor.removeTile(coord)
      else:
        return False
    editor.placeTile(Tile(editor._tileBrush, editor.editArea), coord)
    return True


  def handleRightButton(self, pos: QPointF):
    """Handles the right mouse button for the Editor area.

    Returns whether or not the calling event should be accepted.
    """

    editor = self._editor
    coord = editor.sceneToGrid(pos)
    item = editor.itemAtGridPos(coord, QTransform())
    if isinstance(item, Tile):
      editor.removeTile(coord)
      return True
    else:
      return False


  def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
    """Implementation.

    A left-click places a tile on a grid space, while a right-click removes a
    tile.
    """

    editor = self._editor
    pos = event.buttonDownScenePos(event.button())
    if editor.validGridPos(pos, scene=True):
      self.lastTilePos = editor.sceneToGrid(pos)
      if event.button() is Qt.LeftButton:
        return self.handleLeftButton(pos)
      elif event.button() is Qt.RightButton:
        return self.handleRightButton(pos)


  def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
    """Implementation.

    Handles mouse movement events in the editor. Dragging the mouse with a
    button pressed will place or remove all tiles passed over.
    """

    editor = self._editor
    pos = event.scenePos()
    tilePos = editor.sceneToGrid(pos)
    item = editor.itemAt(pos, QTransform())

    if tilePos != self.lastTilePos:
      self.lastTilePos = tilePos
      if editor.validGridPos(tilePos):
        if event.buttons() & Qt.LeftButton:
          return self.handleLeftButton(pos)
        elif event.buttons() & Qt.RightButton:
          return self.handleRightButton(pos)


  def keyPressEvent(self, event):
    """Implementation."""

    editor = self._editor
    if event.key() == Qt.Key_R:
      if event.modifiers() & Qt.ShiftModifier:
        editor._tileRotation -= 90
      else:
        editor._tileRotation += 90
      editor._tileRotation %= 360
      editor.editArea.update()
      return True
    else:
      return False

