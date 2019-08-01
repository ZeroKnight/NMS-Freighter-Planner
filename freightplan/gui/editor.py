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

from PySide2.QtCore import Slot, QMarginsF, QPoint, QPointF, QRectF, Qt
from PySide2.QtGui import QBrush, QPainter, QPen, QPixmap, QTransform
import PySide2.QtWidgets as QtWidgets
from PySide2.QtWidgets import (
  QGraphicsItem, QGraphicsObject, QGraphicsScene, QGraphicsView
)

from freightplan import GRID_SIZE
from freightplan.gui.tile import Tile

cellSize = 32 # TEMP: keep this in Plan or something

# TEMP
import freightplan.gui.resources_rc

# TODO: slots for changing grid color, opacity, style, etc
class EditorGrid(QGraphicsObject):
  """A graphics object responsible for drawing the editor grid."""

  def __init__(self, parent: QGraphicsItem):
    """Constructor."""

    super().__init__(parent)

    self._color = Qt.gray
    self._style = Qt.SolidLine
    self._opacity = 1.0

    self._pen = QPen(self._color)
    self._pen.setStyle(self._style)

    self.setOpacity(self._opacity)


  @Slot(bool)
  def setVisible(self, visible):
    return super().setVisible(visible)


  def boundingRect(self):
    return self.parentItem().boundingRect()


  def paint(self, painter, option, widget):
    painter.setPen(self._pen)
    end = cellSize * GRID_SIZE
    for n in range(cellSize, end, cellSize):
      painter.drawLine(n, 0, n, end)
      painter.drawLine(0, n, end, n)


class Editor(QGraphicsScene):
  """QGraphicsScene containing the editing area.

  Defines the grid-space representing the floor layout of the freighter.
  """

  def __init__(self, parent):
    """Constructor.

    Args:
      parent: The widget that the Editor belongs to. Usually a MainWindow.
    """

    super().__init__(parent)

    self.lastTilePos = None

    # TBD: EditorView class?
    self.view = QGraphicsView(self)
    # TODO: implement drag on middle-mouse
    # self.view.setDragMode(QGraphicsView.ScrollHandDrag)

    self.pix = QPixmap(':/images/corridor')

    length = cellSize * GRID_SIZE

    # Create border for grid area
    border_rect = QRectF(0, 0, length, length)
    pen = QPen(Qt.gray)
    brush = QBrush('#5e6787', Qt.SolidPattern)
    self.setSceneRect(border_rect.marginsAdded(QMarginsF(5, 5, 5, 5)))

    self.editArea = self.addRect(border_rect, pen, brush)
    self.grid = EditorGrid(self.editArea)


  def sceneToGrid(self, pos: QPointF) -> QPoint:
    """Map a scene position to grid coordinates."""

    return QPoint(pos.x() // cellSize, pos.y() // cellSize)


  # TODO: Bound minimum zoom to fit the View area
  # TODO: create a proper view class and forward sceneevents to it
  def wheelEvent(self, event: QtWidgets.QGraphicsSceneWheelEvent):
    """Implementation.

    Handles zooming the editor's view.
    """

    zoom_factor = 1.15

    if event.modifiers() & Qt.ControlModifier:
      if event.delta() > 0:
        self.view.scale(zoom_factor, zoom_factor)
      else:
        self.view.scale(1 / zoom_factor, 1 / zoom_factor)
      event.accept()
    else:
      event.ignore()


  # TODO: Handle things like selection areas and middle-click scrolling
  def mousePressEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
    """Implementation.

    A left-click places a tile on a grid space, while a right-click removes a
    tile.
    """

    pos = event.buttonDownScenePos(event.button())
    item = self.itemAt(pos, QTransform())

    if event.button() is Qt.LeftButton:
      if not isinstance(item, Tile):
        coord = self.sceneToGrid(pos)
        t = Tile(self.pix, self.editArea)
        t.setPos(coord.x() * 32, coord.y() * 32)
        print(f'Placed tile at {coord!s}')
      else:
        event.ignore()
        return
    elif event.button() is Qt.RightButton:
      if isinstance(item, Tile):
        print(f'Removed tile at {self.sceneToGrid(pos)!s}')
        self.removeItem(item)
      else:
        event.ignore()
        return
    event.accept()


  def mouseMoveEvent(self, event: QtWidgets.QGraphicsSceneMouseEvent):
    """Implementation.

    Handles mouse movement events in the editor. Dragging the mouse with a
    button pressed will place or remove all tiles passed over.
    """

    pos = event.scenePos()
    tilePos = self.sceneToGrid(pos)
    item = self.itemAt(pos, QTransform())

    if tilePos != self.lastTilePos:
      self.lastTilePos = tilePos

      if event.buttons() & Qt.LeftButton:
        if not isinstance(item, Tile):
          t = Tile(self.pix, self.editArea)
          t.setPos(tilePos.x() * 32, tilePos.y() * 32)
          print(f'Placed tile at {tilePos!s}')
          # assert item is self.grid.cell(coord)
        else:
          event.ignore()
          return
      elif event.buttons() & Qt.RightButton:
        if isinstance(item, Tile):
          self.removeItem(item)
          print(f'Removed tile at {self.sceneToGrid(pos)!s}')
        else:
          event.ignore()
          return
    else:
      event.ignore()
    event.accept()